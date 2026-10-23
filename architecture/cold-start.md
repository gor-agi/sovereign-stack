# Cold Start — Minimal Viable Loop

Exercise a working slice immediately before adding the full mesh.

## Minimal Slice
1. Local Nemotron (or current lightweight equivalent) on DGX Spark / available hardware.
2. One decision node: Jev or Clef (API call).
3. NeMo Retriever (local or NIM) for basic archive + skill lookup.
4. One connector or local tool via MCP.
5. Durable run record writer (simple JSON or SQLite log with versions, calls, scores, outcome).
6. Skill library as plain markdown or JSON with scope + success count. Retrieval via embeddings.
7. Sandbox path: at least one Grok bot or paid agent that can run isolated shadow trials.

## First Cycle
- Ingest a small slice of personal data / articles via NeMo Retriever.
- Define one concrete goal.
- Let Nemotron propose a skill or action.
- Score with decision node.
- Run shadow trial in sandbox.
- Promote only if expected outcome met.
- Write the run record.
- Review the record; note gaps for the next cycle.

## What to Add Later
River weight updates, full Reason Network mesh, Omniverse visualization, multi-business segmentation, Persimmon/Ampersand sampling, OpenMontage video, additional connectors.

The loop must run and produce validated skills or logged issues before the rest of the stack is built. This prevents infrastructure that never gets exercised.
