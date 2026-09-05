---
type: Concept
title: "Retrieval-Augmented Generation (RAG)"
description: "Grounding an LLM's answer in documents retrieved at query time."
status: stable
generated: { by: "human:me", at: 2026-08-21T11:00:00Z }
verified:
  - { by: "human:me", at: 2026-08-21T11:00:00Z }
stale_after: 2027-02-01T00:00:00Z
tags: [ai, rag, llm]
resource: "https://ai.google.dev/gemini-api/docs"
---

# Retrieval-Augmented Generation (RAG)

RAG grounds a model's answer in documents fetched at query time, instead of relying only on the model's parametric memory. Pipeline: embed the corpus, retrieve the nearest chunks to the question, prompt the model with question + chunks, answer with citations.

## Why it matters
- Reduces hallucination by anchoring answers in real sources.
- Keeps answers current without retraining.
- Cheap: only the relevant chunks are sent to the model.

## Related
- Depends on [Vector Embeddings](vector-embeddings.md) and [Gemini Embeddings](gemini-embeddings.md).
