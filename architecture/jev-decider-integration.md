# Jev / Cursed UI Decider Integration Plan

**Status:** Plan and research only. No installs, no Spark changes, no runtime wiring until Gor explicitly okays each step that touches infrastructure.

**Repo:** [gor-agi/sovereign-stack](https://github.com/gor-agi/sovereign-stack)
**Focus:** Open-source Cursed UI **Decider** contract (MIT, shadcn registry), not promotion of TypeSafe Jev. Jev is one possible backend; any HTTP endpoint — including a local Nemotron proxy on Spark 1 — can sit behind `createHttpDecider`.

**Sources verified (read-only):**
- Cursed UI registry item: `https://cursed-ui.com/r/predictive-input.json` (ships `predictive-input.tsx` + `registry/default/lib/decider.ts`, license MIT)
- Docs: `https://cursed-ui.com/docs/components/predictive-input`
- This repo @ commit used for line citations below (default branch `main`)
- Related: `gor-agi/universal-plug-protocol`, `gor-agi/creation-of-systems`

---

## 1. The Decider contract (from real `decider.ts`)

Fetched verbatim from the Cursed UI registry. Slightly richer than the shorthand "KeystrokeState in → Prediction out", but that shorthand still captures intent.

### Types

```ts
export type KeystrokeState = {
  value: string
  selection: { start: number; end: number }
  keystroke: string
}

export type DeciderRequest = {
  model: string
  state: KeystrokeState
  candidates: readonly string[]
}

export type Decision = {
  input: string
  probability: number
  model?: string
  probabilities?: Record<string, number>
  confidence?: number
  usage?: { inputTokens: number; outputTokens: number }
  costUsd?: number
}

export type Decider = (
  request: DeciderRequest,
  options?: { signal?: AbortSignal }
) => Promise<Decision>

export type Prediction = {
  keystroke: string
  request: DeciderRequest
  response: Decision
  latencyMs: number
}
```

### Factories

- **`createSimulatedDecider({ latency, spread, random })`** — fake latency/probabilities for local UI/tests; usage/cost fields are synthetic; safe for CI.
- **`createHttpDecider({ endpoint, headers, fetch })`** — `POST` JSON `DeciderRequest` to **any** endpoint; validates that `Decision.input` ∈ `candidates` and `probability` ∈ `[0, 1]`. TypeSafe Jev is a common default behind a server route, but **not hardcoded** in the OSS adapter.

### Mental model for this stack

| Cursed UI (keystroke UI) | Sovereign stack (agent actions) |
| ------------------------ | --------------------------------- |
| `state.keystroke` + `candidates` | Proposed action / skill / tool call + discrete options |
| `Decision.input` + `probability` | Chosen option + calibrated score |
| `Prediction.latencyMs` + `costUsd` | Gate latency + cost in run records |
| Reject / timeout drops keystroke | Hold queue / synthesize / refuse |

**Important mismatch:** Cursed UI is **keystroke-level**; `cold-start/harness.py` is **action-level** (`fit` / `risk` / `confidence`). Integration needs an adapter (`ActionDecider`) that preserves the Decider HTTP shape for the proxy while mapping outputs into the harness score dict.

---

## 2. Four embed points — verification

### 2.1 `cold-start/harness.py` — `score_with_decision_node`

**Claim:** Stub saying "replace with Jev or Clef", returns `fit`, `risk`, `confidence`.

**Verdict: Confirmed**

```66:75:cold-start/harness.py
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
```

Also:

- L111: cycle calls the stub.
- L119: **`if skill and scores.get("confidence", 0) >= 0.8:`** — this is a real apply-vs-synthesize gate (stub scores fake a pass).
- L148: `decision_scores` written into the durable run record.
- `cold-start/config.example.json` already has a `decision_node` block (`type`, `endpoint`, `api_key` placeholder).
- `cold-start/run_record_schema.json` requires `decision_scores` (described as "Jev/Clef outputs").

**Note:** Shape is **not** identical to `Decision` (`input`/`probability`); it is the closest *executable* embed point.

---

### 2.2 `architecture/layers.md` — Decision & Judgment Layer

**Claim:** Defines Jev as swappable fast gate via compatible API.

**Verdict: Confirmed** (documentation only)

```8:9:architecture/layers.md
## Decision & Judgment Layer
- Fast gate: Jev or Clef (Cloudflare) — calibrated probabilities (Choice/Score/Noul), low latency. Swappable via compatible API.
```

No Python yet. Extending this section to name the Decider contract + local HTTP proxy is a docs follow-up after code lands.

---

### 2.3 Fast loop step 5 — Jev before sandbox

**Claim:** `architecture/loops.py` fast loop step 5 scores fit/risk before sandbox validation.

**Verdict: Partly confirmed — path was wrong**

- There is **no** `architecture/loops.py` in this repo.
- Real file: **`architecture/loops.md`**

```3:10:architecture/loops.md
## Fast Loop — Skill Retrieval & Synthesis (local)
1. Situation arrives.
2. Retrieve closest skill(s) from library (scope + success count + embeddings via NeMo Retriever).
3. If confidence / fit clears expected-outcome threshold → apply.
4. Else synthesize candidate skill from current context + prior trajectories.
5. Validate via stack: Jev/Clef scores fit and risk; sandbox (Grok bots / paid agents) runs shadow trials; optional River quick pass for high-stakes.
6. Only promote to library when expected / positive / enough outcome for the goal is met. Scope the skill to validated conditions.
7. Write durable run record (inputs, versions, calls, scores, outcome).
```

Spec is correct; it is not executable code.

---

### 2.4 `architecture/policies.md` — Jev scores in every durable run record

**Claim:** Mandates Jev scores in every durable run record.

**Verdict: Confirmed** (policy text + schema; harness writes stub scores today)

```6:7:architecture/policies.md
## Durable Run Records
Every session produces a replayable log: inputs, pinned node versions, tool/MCP calls, Jev/Clef scores, expected-outcome judgments, final result, provenance tags. This is the substrate for River training, audit, and visualization. Enables self-echo filtering.
```

Also policies L22: MCP / Reason Network traffic must pass the judgment layer before execution — another future wire-in for a Decider gate.

---

### Related repos (brief)

| Repo | Exists? | Claim | Verdict |
| ---- | ------- | ----- | ------- |
| `gor-agi/universal-plug-protocol` | Yes | `examples/agent_evidence.py` deterministic mandate checks | **Holds.** Signed `grant` + `check_authority`; auditor AUTHORIZED/REFUSED. A Decider can **pre-filter**; it must not replace cryptographic checks. |
| `gor-agi/creation-of-systems` | Yes | No clean embed point | **Holds.** Selection log + mirrored `architecture/`; no runnable decision gate. |

---

## 3. Ranking by mistake-reduction value

| Rank | Embed point | Why |
| ---- | ----------- | --- |
| **#1** | `cold-start/harness.py` `score_with_decision_node` | Only **live** control point. Confidence already decides apply vs synthesize (L119). Calibrated reject/fallback here **prevents** a wrong skill application, not just logs it. |
| **#2** | Fast loop contract (`architecture/loops.md` → future code) | Defines validate-before-promote ordering (gate then sandbox). Once harness uses a real Decider, this is the control-flow contract to implement elsewhere (MCP judgment, skill promotion). |
| **#3** | Durable records (`policies.md` + `run_record_schema.json`) | Provenance for River / audit / self-echo filter. Improves *future* decisions; alone does not stop a bad action. Enrich with `latencyMs` / `costUsd` / full candidate distribution. |
| **#4** | `architecture/layers.md` | Architecture narrative. Update after code exists so the "swappable API" names the Decider + Spark 1 proxy. |

**Principle:** A calibrated gate that can **hold / refuse / fallback** reduces mistakes. Logging without a threshold only helps after the fact.

---

## 4. Python port sketch of the contract

Proposed new module (does not exist yet): `sovereign_stack/decider.py`
(or, if keeping the flat layout, `cold-start/decider.py` for the first PR — prefer a package so n8n/MCP workers can import the same types).

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Protocol, Sequence
import json
import random
import time
import urllib.request


@dataclass(frozen=True)
class KeystrokeState:
    value: str
    selection: Mapping[str, int]  # {"start": int, "end": int}
    keystroke: str


@dataclass(frozen=True)
class DeciderRequest:
    model: str
    state: KeystrokeState
    candidates: Sequence[str]


@dataclass(frozen=True)
class Decision:
    input: str
    probability: float
    model: Optional[str] = None
    probabilities: Optional[Mapping[str, float]] = None
    confidence: Optional[float] = None
    usage: Optional[Mapping[str, int]] = None
    cost_usd: Optional[float] = None


@dataclass(frozen=True)
class Prediction:
    """Caller-side meter (matches Cursed UI Prediction)."""
    keystroke: str
    request: DeciderRequest
    response: Decision
    latency_ms: float


class Decider(Protocol):
    def decide(
        self, request: DeciderRequest, *, timeout_s: float = 10.0
    ) -> Decision: ...


def validate_decision(decision: Decision, request: DeciderRequest) -> Decision:
    if decision.input not in request.candidates:
        raise ValueError("Decision.input must be one of candidates")
    if not (0.0 <= decision.probability <= 1.0):
        raise ValueError("probability must be in [0, 1]")
    return decision


class SimulatedDecider:
    """Zero-cost local stand-in; mirrors createSimulatedDecider."""

    def __init__(self, latency_ms: float = 5.0, rng: Optional[random.Random] = None):
        self.latency_ms = latency_ms
        self.rng = rng or random.Random(0)

    def decide(self, request: DeciderRequest, *, timeout_s: float = 10.0) -> Decision:
        time.sleep(self.latency_ms / 1000.0)
        chosen = (
            request.state.keystroke
            if request.state.keystroke in request.candidates
            else request.candidates[0]
        )
        residual = 0.05
        probs = {c: residual / max(len(request.candidates) - 1, 1) for c in request.candidates}
        probs[chosen] = 1.0 - residual
        return validate_decision(
            Decision(
                input=chosen,
                probability=probs[chosen],
                probabilities=probs,
                confidence=0.9,
                model=request.model,
                usage={"inputTokens": 0, "outputTokens": 0},
                cost_usd=0.0,
            ),
            request,
        )


class HttpDecider:
    """Mirrors createHttpDecider: POST DeciderRequest JSON, read Decision."""

    def __init__(self, endpoint: str, headers: Optional[Mapping[str, str]] = None):
        self.endpoint = endpoint
        self.headers = dict(headers or {})

    def decide(self, request: DeciderRequest, *, timeout_s: float = 10.0) -> Decision:
        body = {
            "model": request.model,
            "state": {
                "value": request.state.value,
                "selection": dict(request.state.selection),
                "keystroke": request.state.keystroke,
            },
            "candidates": list(request.candidates),
        }
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json", **self.headers},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        decision = Decision(
            input=payload["input"],
            probability=float(payload["probability"]),
            model=payload.get("model"),
            probabilities=payload.get("probabilities"),
            confidence=payload.get("confidence"),
            usage=payload.get("usage"),
            cost_usd=payload.get("costUsd", payload.get("cost_usd")),
        )
        return validate_decision(decision, request)


class ActionDecider:
    """Adapter: Decider Decision → harness {fit, risk, confidence}.

    For action-level gates, put the proposed action id/name in
    state.keystroke (or state.value) and pass discrete options as candidates.
    Map probability/confidence → fit/confidence; derive risk as 1 - fit
    until a dedicated risk head exists.
    """

    def __init__(self, inner: Decider, fit_threshold: float = 0.8):
        self.inner = inner
        self.fit_threshold = fit_threshold

    def score(self, *, goal: str, skill_id: Optional[str], candidates: Sequence[str]) -> dict[str, Any]:
        chosen = skill_id or "__none__"
        request = DeciderRequest(
            model="action-gate",
            state=KeystrokeState(
                value=goal,
                selection={"start": len(goal), "end": len(goal)},
                keystroke=chosen,
            ),
            candidates=list(candidates) if candidates else [chosen, "__hold__", "__synthesize__"],
        )
        t0 = time.perf_counter()
        decision = self.inner.decide(request)
        latency_ms = (time.perf_counter() - t0) * 1000.0
        fit = float(decision.probability)
        confidence = float(decision.confidence if decision.confidence is not None else fit)
        return {
            "fit": fit,
            "risk": max(0.0, 1.0 - fit),
            "confidence": confidence,
            "chosen": decision.input,
            "probabilities": dict(decision.probabilities or {}),
            "latency_ms": latency_ms,
            "cost_usd": decision.cost_usd or 0.0,
            "model": decision.model,
            "threshold": self.fit_threshold,
            "below_threshold": confidence < self.fit_threshold,
        }
```

Thresholds + fallback (harness):

- `confidence >= threshold` → apply retrieved skill.
- else → synthesize + sandbox (existing path), or push to hold queue for safety-critical scopes.

---

## 5. Step-by-step integration sequence

**Rules:** Start with SimulatedDecider + tests (zero risk). Then wire harness. Then a real backend on **Spark 1 (personal)** only. **Spark 2 (ai-gini / Drink Gini) is business-only — do not route personal Decider traffic there.**

Mark every step that touches Sparks: **needs Gor's explicit okay**.

### Step 0 — Branch (docs/code workstations only)

```bash
git clone git@github.com:gor-agi/sovereign-stack.git
cd sovereign-stack
git checkout -b feat/decider-contract
```

### Step 1 — SimulatedDecider + unit tests (zero risk)

**Create:**

- `sovereign_stack/__init__.py`
- `sovereign_stack/decider.py` (sketch above)
- `tests/test_decider.py`

**Commands:**

```bash
# from repo root; no Spark, no network backends
python -m pytest tests/test_decider.py -q
```

**Test ideas:**

- `Decision.input` must be in `candidates` or `validate_decision` raises.
- `SimulatedDecider` with fixed `Random(0)` is deterministic.
- `cost_usd == 0` for simulated path.
- `ActionDecider.score` returns `fit`/`risk`/`confidence` and sets `below_threshold` correctly.

*Does not touch Sparks.*

### Step 2 — Wire harness to SimulatedDecider

**Edit:** `cold-start/harness.py` (replace body of `score_with_decision_node`, ~L66–75).

**Edit:** `cold-start/config.example.json` — e.g. add `threshold`, keep `endpoint` empty for sim mode:

```json
"decision_node": {
  "type": "simulated",
  "endpoint": "",
  "threshold": 0.8
}
```

**Optional dry run** (only if a local OpenAI-compatible model is already up):

```bash
cp cold-start/config.example.json cold-start/config.json
# fill local_model.endpoint — do not commit secrets
python cold-start/harness.py "summarize one local article into the vault"
```

If that endpoint is on Spark 1: **needs Gor's explicit okay**.

### Step 3 — Docs sync (this file already started it)

**Edit (follow-up PR):**

- `architecture/layers.md` L8–9 — name Decider contract + Spark 1 HTTP proxy as the local "compatible API".
- `architecture/loops.md` L8 — cite `sovereign_stack/decider.py` / ActionDecider.
- `architecture/policies.md` L7 — require `latency_ms` / `cost_usd` / optional full `probabilities` in run records.
- `cold-start/run_record_schema.json` — extend `decision_scores` properties accordingly.

*Docs-only; no Spark.*

### Step 4 — HttpDecider against a local proxy on Spark 1

**needs Gor's explicit okay** (Spark 1 / spark-87d5).

Deploy a thin proxy (design in §6) that accepts `createHttpDecider` / `HttpDecider` POST shape and returns `Decision`.

**Config:**

```json
"decision_node": {
  "type": "http",
  "endpoint": "http://spark-87d5:<proxy-port>/decide",
  "threshold": 0.8
}
```

**Curl check (from Mac head or an allowed host on the personal LAN):**

```bash
curl -sS -X POST "http://spark-87d5:<proxy-port>/decide" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-nemotron",
    "state": {
      "value": "Hell",
      "selection": {"start": 4, "end": 4},
      "keystroke": "o"
    },
    "candidates": ["o", "i", "p", " ", "Backspace", "Delete"]
  }'
```

Expect JSON like:

```json
{
  "input": "o",
  "probability": 0.91,
  "confidence": 0.88,
  "probabilities": {"o": 0.91, "i": 0.03, "p": 0.02},
  "model": "local-nemotron",
  "usage": {"inputTokens": 128, "outputTokens": 1},
  "costUsd": 0.0
}
```

**Harness check:**

```bash
python cold-start/harness.py "test goal after http decider"
# inspect cold-start/run_records/*.json for decision_scores.latency_ms / model
```

### Step 5 — Later: personal n8n + optional cloud Jev

**needs Gor's explicit okay** (Spark 1 personal n8n / "Jev gate").

- Optional: `n8n-nodes-typesafe-ai` Evaluate/Route with confidence thresholds + fallback outputs for orchestration paths that already run through n8n.
- Keep cloud Jev behind a **server-side** route (API key never in the browser / never in git).
- Personal vs business: Spark 2 services (vLLM `:18000`, sommelier `:18110`, n8n `:5678`, MCP `:18130`) stay Drink Gini-only.

### Step 6 — Optional UPP pre-filter

In agent loops that already emit UPP evidence (`universal-plug-protocol/examples/agent_evidence.py`):

1. Decider / ActionDecider scores the proposed tool+purpose.
2. If below threshold → hold (do not call tool).
3. If above threshold → still run `check_authority` (deterministic mandate). Probability never overrides a missing/revoked grant.

---

## 6. Gaps the open source does not cover

### 6.1 Local Nemotron-backed Decider proxy (Spark 1 only)

**Why:** `createHttpDecider` / `HttpDecider` POST to any URL. Missing piece for local-first is a small service that speaks that request/response shape and ranks with a **personal** Nemotron (or future Nemotron clone) on Spark 1 — not Spark 2's business vLLM.

**Placement:**

| Host | Role |
| ---- | ---- |
| Spark 1 (`spark-87d5`) | Personal vault/factory/NemoClaw (`:8030`); **home of the Decider proxy** |
| Spark 2 (`ai-gini`) | Drink Gini only (Nemotron 3.5 Lightning on `gini-vllm` `:18000`, etc.) — **out of scope** for this personal gate |
| Mac | Head machine only; runs git/tests/curl against Spark 1 |

**Suggested API:**

- `POST /decide` — body = `DeciderRequest`, response = `Decision` (Cursed UI-compatible).
- `GET /health` — liveness + upstream model id.
- Optional `POST /score_action` — convenience wrapper returning `{fit, risk, confidence, ...}` for harness without forcing keystroke semantics at the call site.

**Getting probabilities from vLLM / OpenAI-compatible APIs:**

1. Prefer **constrained / candidate-restricted** scoring: for each string in `candidates`, obtain a logprob (or score the next token if candidates are single tokens).
2. Example shape (illustrative — exact fields depend on the serving stack on Spark 1):

```bash
# Illustrative: OpenAI-compatible completions with logprobs on candidate tokens.
# needs Gor's explicit okay — hits Spark 1 inference
curl -sS "http://spark-87d5:<nemotron-port>/v1/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nemotron",
    "prompt": "<ranking prompt with context + candidate list>",
    "max_tokens": 1,
    "logprobs": 5,
    "temperature": 0
  }'
```

3. Convert: `p_i = exp(logprob_i)`, then `normalize` over the candidate set so probabilities sum to 1.
4. Set `Decision.input = argmax(p)`, `probability = p[input]`, optional `confidence` from normalized entropy (as in Cursed UI's simulated helper) or a separate calibration head.
5. `costUsd = 0` for local inference; still fill `usage` for metering.

**Calibration / evaluation (also missing from OSS):**

- Hold-out set of (context, candidate set, gold choice, gold apply/hold).
- Track ECE / Brier; if raw softmax is overconfident, apply temperature scaling or Platt scaling on a validation split.
- Gate promotion of threshold changes via durable run records + batch review (see policies hold queue).

**Security / tenancy:**

- Bind proxy to personal LAN / Tailscale only; no public exposure by default.
- No business (Spark 2) credentials or Gini traffic in this process.
- Never commit API keys; `config.json` stays local (gitignored pattern already implied by `config.example.json`).

### 6.2 Other gaps

| Gap | Detail |
| --- | ------ |
| Keystroke vs action granularity | Need `ActionDecider`; do not pretend every agent tool call is a QWERTY key. |
| Risk head | Harness wants `risk` separately; OSS Decision has probability/confidence only — derive or train a second score. |
| n8n personal instance | Planned later on Spark 1; OSS `n8n-nodes-typesafe-ai` is a path for Evaluate/Route once n8n exists. |
| Cloud Jev | Closed weights; optional utility behind HttpDecider, not required for local-first. |
| UPP | Cryptographic mandates remain authoritative; Decider is advisory pre-filter. |

---

## 7. Suggested first PR after this doc

1. Add `sovereign_stack/decider.py` + `tests/test_decider.py` (SimulatedDecider only).
2. Swap `score_with_decision_node` to `ActionDecider(SimulatedDecider())` behind config `type: simulated`.
3. Leave `type: http` unimplemented-or-stubbed until Gor okays Spark 1 proxy deployment.

Commit discipline for that work: code + tests only when Gor asks; this file is the plan of record.

---

## 8. Summary table

| # | Path | Verdict |
| - | ---- | ------- |
| 1 | `cold-start/harness.py` L66–75, L119, L148 | **Confirmed** — stub + live confidence gate |
| 2 | `architecture/layers.md` L8–9 | **Confirmed** — swappable fast gate (docs) |
| 3 | `architecture/loops.md` L8 (not `loops.py`) | **Partly** — path typo; content confirmed |
| 4 | `architecture/policies.md` L6–7 | **Confirmed** — durable Jev/Clef scores mandated |

**Highest value embed:** #1 harness stub — replace with Decider-backed ActionDecider so calibrated confidence actually prevents wrong applies.
