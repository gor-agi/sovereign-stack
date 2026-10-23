# Loops

## Fast Loop — Skill Retrieval & Synthesis (local)
1. Situation arrives.
2. Retrieve closest skill(s) from library (scope + success count + embeddings via NeMo Retriever).
3. If confidence / fit clears expected-outcome threshold → apply.
4. Else synthesize candidate skill from current context + prior trajectories.
5. Validate via stack: Jev/Clef scores fit and risk; sandbox (Grok bots / paid agents) runs shadow trials; optional River quick pass for high-stakes.
6. Only promote to library when expected / positive / enough outcome for the goal is met. Scope the skill to validated conditions.
7. Write durable run record (inputs, versions, calls, scores, outcome).

Skills are not permanent rules. They are a living retrieval library. Novel situations use sandbox + synthesis rather than immediate escalation.

## Slow Loop — Weight Updates (River + local)
- Periodic or on-plateau: push filtered trajectories to River for LoRA or RL on Nemotron.
- Provenance filter: exclude or heavily down-weight pure model-authored content to avoid self-echo.
- Return new checkpoint; pin it in subsequent session manifests.
- Local small LoRA passes on Spark remain the default for privacy-sensitive slices.

## Validation Loop
Grok sandbox + paid agents run isolated shadow trials. Results scored against goal-relative expected outcome. Multi-node agreement (local Nemotron + decision gate + external simulation) required for promotion. Disagreement is preserved as signal, not averaged away.

## Batch Review
Hold queue and issue log collect low-confidence, safety-critical, or novel items. Mesh continues. Human clears in batches. Absence modes: supervised autonomy (queue consequential actions) or per-entity read-only freeze.
