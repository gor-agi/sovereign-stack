# Cold-Start Starter

Minimal pieces so the first real cycle can run.

## Quick start
```bash
cd cold-start
pip install openai
cp config.example.json config.json
# edit config.json: set local_model.endpoint to your Nemotron / vLLM / Ollama OpenAI-compatible URL
python harness.py "your goal here"
```

## What it does
1. Loads config.
2. Calls your local OpenAI-compatible model (Nemotron).
3. Retrieves a skill or synthesizes one.
4. Scores with a decision-node stub (replace with Jev or Clef).
5. Writes a durable run record under `run_records/`.
6. Promotes a skill only when the sandbox stub says the expected outcome was met.

## Files
- `harness.py` — the loop
- `skill_schema.json` / `run_record_schema.json` — contracts
- `example_skill.json` — starter skill (copy into `skills/` to seed)
- `config.example.json` — copy to `config.json`

Replace the decision-node and sandbox stubs once the basic cycle writes a real record. Canonical data stays local.
