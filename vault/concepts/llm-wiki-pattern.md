---
type: Concept
title: LLM Wiki Pattern
description: A personal knowledge base of interlinked markdown files that an LLM agent writes and maintains over time.
tags: [llm, pkm, agents, markdown]
status: stable
generated: { by: human:kuanhoong, at: 2026-10-20T08:20:00Z }
verified: { by: human:kuanhoong, at: 2026-10-20T08:20:00Z }
stale_after: 2027-04-20T00:00:00Z
---

# Summary

The LLM wiki pattern, popularised by Andrej Karpathy, has three layers: immutable raw sources, a wiki of markdown pages the model writes and links, and a schema file that tells the model how to file things. Instead of rediscovering knowledge on every query, the model compiles it once and keeps it current.

# Key points

- Three operations: ingest a source, query the wiki, lint the wiki for gaps and contradictions.
- Knowledge accumulates between sessions, so the wiki works as agent memory.
- The [Open Knowledge Format](/concepts/open-knowledge-format.md) formalises this pattern as an open spec.

# Related

- [Second Brain](/concepts/second-brain.md)
- [Retrieval-Augmented Generation](/concepts/retrieval-augmented-generation.md)
