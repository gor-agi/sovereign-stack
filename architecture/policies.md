# Operational Policies

## Expected Outcome (not absolute 100%)
Validation is goal-relative: positive, expected, or enough outcome for the stated goal. Absolute perfection is not required. Skills are scoped to the conditions under which they were validated. Outside scope → synthesize or hold, do not blindly apply.

## Durable Run Records
Every session produces a replayable log: inputs, pinned node versions, tool/MCP calls, Jev/Clef scores, expected-outcome judgments, final result, provenance tags. This is the substrate for River training, audit, and visualization. Enables self-echo filtering.

## Hold Queues & Batch Review
Safety-critical or low-confidence actions enter a hold queue (accept / hold / refuse style). Mesh continues running. Issues are collected and solved in batches. No constant hard stops. Absence: queue consequential actions for later review; optional read-only freeze per business entity.

## Version Pinning & Manifests
Session manifest pins Nemotron checkpoint hash, decision-model tag, API versions, River adapter ID. Calls with mismatched versions are rejected.

## Timeouts & Partial Results
Per node class: wait-with-deadline, proceed local-only with logged downgrade flag, or fail-closed/hold. Safety-critical connectors fail closed or hold. Research nodes may proceed local-only.

## Provenance & Self-Echo
Tag trajectories human-authored / model-authored / hybrid. Exclude or heavily down-weight pure model-authored content in SFT/RL so the system does not reinforce its own distribution.

## Trust Boundaries
- MCP servers and Reason Network messages are untrusted input. Must pass judgment layer (Jev/Clef + optional sandbox) before execution.
- Inbound policies and loop guards on P2P.
- Separate API keys, MCP scopes, and audit logs per business entity to prevent cross-contamination.
- External calls are sampled references only; canonical archive never bulk-uploaded.

## Cold Start
Define and exercise the minimal viable loop first (see cold-start.md). Avoid building unused infrastructure.

## Power & Thermal
Start small. Duty-cycle or shed non-critical workloads (visualization before training before inference). Scale hardware only when a concrete workload requires it.

## Cost Governor
Meter per workflow category with hard caps. River + decision nodes + simulation + premium routes compound; throttle early.

## Visualization
Omniverse/Isaac binds to run records. Passive by default. Active intervention gated by the same judgment stack.
