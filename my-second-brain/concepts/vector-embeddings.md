---
type: Concept
title: "Vector Embeddings"
description: "Meaning represented as a point in high-dimensional space; similar meanings sit close together."
status: stable
generated: { by: "human:me", at: 2026-08-21T11:20:00Z }
verified:
  - { by: "human:me", at: 2026-08-21T11:20:00Z }
stale_after: 2027-08-21T00:00:00Z
tags: [ai, embeddings, search]
resource: "https://ai.google.dev/gemini-api/docs/embeddings"
---

# Vector Embeddings

An embedding maps text (or an image) to a vector of numbers such that semantically similar inputs land near each other. Similarity is measured with cosine distance / dot product.

## Key points
- Enables **semantic search** — matching by meaning, not keywords.
- Dimensionality trades quality for storage/speed.
- The foundation under [RAG](rag.md).
