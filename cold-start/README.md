# Cold-Start Starter

Minimal concrete pieces so Grok Build (or any agent) can extend the loop instead of inventing structure from scratch.

## Files
- `skill_schema.json` — required fields for every skill in the library
- `run_record_schema.json` — durable run record format
- `harness.py` — thin skeleton of the retrieve → score → synthesize → validate → record loop
- `example_skill.json` — first skill template (scoped, with success count)
- `config.example.json` — placeholders for decision node, local model, sandbox

## Usage
1. Copy `config.example.json` to `config.json` and fill endpoints/keys.
2. Point Grok Build at `harness.py` and the schemas.
3. Run the first cycle described in `architecture/cold-start.md`.
4. Promote skills only when expected outcome is met; write every cycle to the run-record log.

Canonical data and full weights stay local. This directory is scaffolding only.
