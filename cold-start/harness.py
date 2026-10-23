#!/usr/bin/env python3
"""
Cold-start harness.
Loads config, calls an OpenAI-compatible local model (Nemotron), scores with a decision node,
retrieves or synthesizes a skill, validates, and writes a durable run record.

Fill config.json from config.example.json, then run:
  python harness.py "your goal here"
"""

import json
import uuid
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore

ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "config.json"
SKILL_DIR = ROOT / "skills"
RECORD_DIR = ROOT / "run_records"
SKILL_DIR.mkdir(exist_ok=True)
RECORD_DIR.mkdir(exist_ok=True)

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Copy config.example.json to {CONFIG_PATH} and fill it.")
    return json.loads(CONFIG_PATH.read_text())

def get_client(cfg: dict):
    if OpenAI is None:
        raise RuntimeError("pip install openai")
    model_cfg = cfg["local_model"]
    return OpenAI(
        base_url=model_cfg.get("endpoint", "http://localhost:8000/v1"),
        api_key=model_cfg.get("api_key", "not-needed"),
    )

def load_skills() -> list:
    return [json.loads(p.read_text()) for p in SKILL_DIR.glob("*.json")]

def retrieve_closest(skills: list, goal: str) -> Optional[dict]:
    # Stub: replace with NeMo Retriever embedding similarity
    if not skills:
        return None
    # Prefer skills whose scope mentions the goal
    for s in skills:
        if any(goal.lower() in g.lower() for g in s.get("scope", {}).get("goal_types", [])):
            return s
    return skills[0]

def call_local_model(client, cfg: dict, messages: list) -> str:
    model_name = cfg["local_model"].get("name", "nemotron")
    resp = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""

def score_with_decision_node(cfg: dict, skill: Optional[dict], goal: str) -> dict:
    # Stub for Jev / Clef. Replace with real API call.
    # Expected shape: {"fit": float, "risk": float, "confidence": float}
    if skill is None:
        return {"fit": 0.0, "risk": 0.5, "confidence": 0.3, "note": "no skill retrieved"}
    return {
        "fit": 0.75,
        "risk": 0.15,
        "confidence": 0.8,
        "note": "decision-node stub — replace with Jev or Clef",
    }

def synthesize_skill(goal: str, context: str, model_output: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "name": f"gen-{goal[:30].replace(' ', '-')}",
        "scope": {
            "goal_types": [goal],
            "constraints": ["local-first"],
            "notes": "synthesized in cold-start cycle",
        },
        "success_count": 0,
        "expected_outcome_definition": "positive / enough outcome for the stated goal",
        "body": model_output or context,
        "provenance": "model",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

def validate_in_sandbox(skill: dict, goal: str) -> dict:
    # Stub for Grok bot / paid agent shadow trial.
    # For cold start, accept if the body is non-empty.
    met = bool(skill.get("body", "").strip())
    return {"expected_outcome_met": met, "notes": "sandbox stub — replace with real shadow trial"}

def write_run_record(record: dict):
    path = RECORD_DIR / f"{record['session_id']}.json"
    path.write_text(json.dumps(record, indent=2))
    return path

def run_cycle(goal: str, context: str = ""):
    cfg = load_config()
    client = get_client(cfg)

    skills = load_skills()
    skill = retrieve_closest(skills, goal)
    scores = score_with_decision_node(cfg, skill, goal)

    model_messages = [
        {"role": "system", "content": "You are the local Nemotron brain. Propose a concrete next step or skill body for the goal. Stay local-first."},
        {"role": "user", "content": f"Goal: {goal}\nContext: {context}"},
    ]
    model_output = call_local_model(client, cfg, model_messages)

    if skill and scores.get("confidence", 0) >= 0.8:
        outcome = "applied"
        final_skill = skill
        expected_met = True
    else:
        candidate = synthesize_skill(goal, context, model_output)
        sandbox = validate_in_sandbox(candidate, goal)
        if sandbox.get("expected_outcome_met"):
            candidate["success_count"] = 1
            candidate["last_validated"] = datetime.now(timezone.utc).isoformat()
            (SKILL_DIR / f"{candidate['id']}.json").write_text(json.dumps(candidate, indent=2))
            outcome = "synthesized_and_promoted"
            expected_met = True
            final_skill = candidate
        else:
            outcome = "held"
            expected_met = False
            final_skill = candidate

    record = {
        "session_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "manifest": {
            "nemotron_checkpoint": cfg["local_model"].get("checkpoint", "unknown"),
            "decision_node": cfg.get("decision_node", {}).get("type", "stub"),
            "retriever": cfg.get("retriever", {}).get("type", "stub"),
        },
        "inputs": {"goal": goal, "context": context},
        "retrieved_skills": [skill["id"]] if skill else [],
        "decision_scores": scores,
        "model_output": model_output[:2000],
        "outcome": outcome,
        "expected_outcome_met": expected_met,
        "provenance": "hybrid",
        "notes": "cold-start cycle",
    }
    path = write_run_record(record)
    print(f"Wrote {path}")
    print(f"Outcome: {outcome}")
    return record

if __name__ == "__main__":
    import sys
    goal = sys.argv[1] if len(sys.argv) > 1 else "summarize one local article into the vault"
    context = sys.argv[2] if len(sys.argv) > 2 else ""
    result = run_cycle(goal, context)
    print(json.dumps({k: result[k] for k in ("session_id", "outcome", "expected_outcome_met")}, indent=2))
