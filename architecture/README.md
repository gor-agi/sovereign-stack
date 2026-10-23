# Sovereign Local Architecture

Local-first personal foundation machine. Nemotron on DGX Spark is the always-on brain that owns identity and long-term learning. External models and services are rented utilities, not landlords. Data stays canonical on local storage (Obsidian vault + DGX). The system compounds under personal goals while collecting issues for batch human review instead of constant stops.

## Principles
- Local Nemotron owns identity, proposals, and final learning.
- External nodes (Persimmon, Ampersand, frontier models, Jev/Clef, River) are per-call utilities.
- Skills are a retrieval library (scoped + validated to expected/positive outcome), not static rules.
- Durable run records make every trajectory replayable and usable for training.
- NVIDIA stack is preferred (NeMo Retriever, Nemotron models, NIM, Omniverse/Isaac Sim) unless a clear superior alternative exists.
- Multi-node judgment + expected-outcome threshold before action. Safety-critical paths escalate or hold for batch review.
- Version pinning, provenance tags, and trust boundaries on MCP and P2P.

## Directory
- [layers.md](layers.md) — core, decision, training, transport, execution, visualization
- [nodes.md](nodes.md) — specific nodes and how they slot in
- [loops.md](loops.md) — fast skill loop + slow River loop + validation
- [policies.md](policies.md) — operational policies from pressure testing and external strengthenings
- [cold-start.md](cold-start.md) — minimal viable loop to exercise first

Canonical archive remains local. This repo is the shareable, versioned reference.
