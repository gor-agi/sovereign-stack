# Nodes

## Local Core
- **Nemotron** (NVIDIA, DGX Spark): identity, proposals, long-term learning. Preferred base for both inference and River updates.
- **NeMo Retriever** (Embed / Rerank / Parse + library + NIM): local data organizer, agentic retrieval skill, ingestion of PDFs/tables/charts/voice into agent-consumable form.

## Decision Layer
- **Jev** (TypeSafe): calibrated probability gate (Choice/Score/Noul). Fast, schema-bound.
- **Clef / Clef-flash** (Cloudflare): higher precision or lower latency alternative, Jev-API compatible, open weights, image-capable. Clairic for extraction tasks.

## Remote Judgment Utilities (sampled references only)
- **Persimmon** (humans&): user model / human behavior simulation. Primary source of wider human distribution (tone, messiness, pivots) beyond personal data. API gated; use for sparse reference or synthetic checks.
- **Ampersand** (humans&): collaborator model. Collaboration traces (when to speak, when to pass, handling pushback) as preference signal. Open API.
- Frontier models: narrow specialist calls (deep research, second opinion). Never bulk data upload.

## Training
- **River AI**: SFT / LoRA / RL on personal data and goals. Supports Nemotron 3.5 Lightning and other open bases. On-prem option available but treat as residual trust surface; prefer local-first distillation where possible.

## Transport
- **Reason Network** (Reason Machines): P2P encrypted agent mesh. Team directory of live sessions, MCP tools (list_team, send_message, check_inbox). Supports own relay. Use for coordination across machines and with Grok bots / coding agents.

## Execution & Media
- **OpenMontage**: agentic video pipelines. Nemotron as executive producer; local generation (Wan, Hunyuan, LTX, etc.) or premium routes. Hybrid with own footage.
- MCP servers and Zapier: real-world connectors. Scoped per business (floral, Drink Gini, repair platform, e-commerce).

## Validation & Sandbox
- Grok bots and paid agents running in sandbox for shadow trials of proposed skills or actions. Outcomes logged; promotion only on expected/positive outcome.
