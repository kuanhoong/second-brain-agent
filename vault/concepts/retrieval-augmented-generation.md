---
type: Concept
title: Retrieval-Augmented Generation
description: Grounding a model's answer in passages retrieved from an external store at query time.
tags: [llm, rag, retrieval]
status: stable
generated: { by: human:kuanhoong, at: 2026-10-21T08:00:00Z }
verified: { by: human:kuanhoong, at: 2026-10-21T08:00:00Z }
stale_after: 2027-04-21T00:00:00Z
---

# Summary

RAG retrieves the passages closest in meaning to a question and hands them to the model as context, so the answer comes from your documents instead of the model's memory. It reads a corpus. It does not maintain one.

# Key points

- Pipeline: chunk, embed, store, retrieve, generate with citations.
- Retrieval quality depends on [Vector Embeddings](/concepts/vector-embeddings.md).
- RAG cannot tell a current note from an outdated one unless the notes carry that signal.

# Related

- [LLM Wiki Pattern](/concepts/llm-wiki-pattern.md)
