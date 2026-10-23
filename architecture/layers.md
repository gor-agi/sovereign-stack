# Layers

## Core (local, DGX Spark)
Nemotron (3.5 Lightning or current equivalent) as the always-on brain. Owns identity, long-term learning, and proposals. Trained over time on the three-year personal archive (voice, transcripts, articles, decisions) plus selected external traces. Canonical data lives in local storage (Obsidian vault + DGX). 

NeMo Retriever stack (Embed, Rerank, Parse, ingestion library, NIM) is the local data organizer and retrieval layer. Meaning-based lookup into the archive and skill library. Agentic retrieval (ReAct-style iterative query → retrieve → fuse → select) is a first-class capability, not one-shot RAG.

## Decision & Judgment Layer
- Fast gate: Jev or Clef (Cloudflare) — calibrated probabilities (Choice/Score/Noul), low latency. Swappable via compatible API.
- Specialist / simulation nodes (P2P or API, rented per call): Persimmon (human behavior distribution), Ampersand (long-horizon collaboration), frontier models for narrow research or deep review.
- Validation workers: Grok bots and other paid agents in sandbox (isolated, no real connectors). Score proposed skills or actions against expected / positive / enough outcome for the goal.
- Arbitration: multi-node agreement + expected-outcome threshold. Safety-critical or irreversible actions escalate or enter a hold queue for batch review. No single node unilaterally acts.

## Training & Improvement
- Fast loop (local): post-session review extracts patterns, proposes or patches skills, writes to skill library and memory. Skills carry scope + success count. Closest match is retrieved; if confidence clears the bar it applies; otherwise synthesize a new skill, validate via the full stack, and promote only on expected outcome.
- Slow loop: River AI for SFT / LoRA / RL. Prefer local-first small passes on the Spark; use River for heavier runs. Provenance tags (human / model / hybrid) so pure model-authored trajectories are excluded or heavily down-weighted.
- Version manifest per session: pin Nemotron checkpoint hash, decision-model tag, API versions, River adapter ID. Mismatched calls rejected.

## Transport & Connectivity
- Reason Network (open-source, E2E encrypted, P2P via iroh + optional own relay) for agent-to-agent coordination. Inbound policies (accept / hold / refuse), loop guards, and peer-text framing as untrusted input.
- MCP as the universal adapter. Local MCP servers preferred; each scoped per business entity. Every MCP call and Reason Network message treated as untrusted and passed through the judgment layer.
- Real-world connectors (Stripe, smart home, EV, etc.) and Zapier for the long tail. Fail-closed or hold-queue on safety-critical paths.

## Execution & Visualization
- Coding, research, video (OpenMontage + local generation or premium routes), and other work run on the local agent loop. Specialists called when needed, then continue locally.
- Omniverse / Isaac Sim as the live visualization and control surface. Binds to durable run records (skill activations, scores, hold-queue depth, connector status). Passive mirror by default; active intervention only behind judgment gates.
- Power/thermal: start with minimal viable loop. Duty-cycle or shed non-critical workloads. Scale only when a concrete workload demands it.
