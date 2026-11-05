# OpenSearch

Open-source search and analytics engine (Apache 2.0), forked from Elasticsearch 7.10 in 2021 after Elastic changed its license. Now governed by the OpenSearch Software Foundation under the Linux Foundation.

## Core facts

- Built on Apache Lucene — the same indexing foundation Google used in its early search days.
- Fully transparent ranking: you can inspect and tune every scoring rule. No corporate black box.
- Does **not** crawl the open web. It indexes only the data you feed it: documents, logs, databases, or sites you point it at.
- Best fit: internal data systems — log analytics, application monitoring, in-product search bars, security event triage.

## Why it matters for the sovereign stack

Google's index is shaped by corporate policy (demotion, filtering, boosting). OpenSearch gives the same engine class with zero vendor framing — ranking is statistical and inspectable, governed by whoever deploys it.

Comparable open alternatives: Meilisearch (MIT, Rust, typo-tolerant, reorderable ranking rules), Typesense (GPL-3, C++, RAM-resident, built-in vector search), SearXNG (AGPL metasearch aggregator, no own index).

## Planned use

- Internal data search layer for personal/sovereign infrastructure.
- Candidate for indexing vault notes, logs, and agent run records.
- Evaluate alongside Meilisearch for smaller corpora and Typesense for low-latency hybrid search.
