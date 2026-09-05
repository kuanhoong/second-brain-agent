---
type: Concept
title: "Gemini Embeddings"
description: "Google's gemini-embedding-001 model for turning text into retrieval vectors."
status: stable
generated: { by: "reference_agent/gemini-flash", at: 2026-08-22T14:12:00Z }
verified:
  - { by: "human:me", at: 2026-08-22T15:00:00Z }
stale_after: 2027-03-01T00:00:00Z
tags: [ai, embeddings, gemini, google]
resource: "https://developers.googleblog.com/gemini-embedding-available-gemini-api/"
---

# Gemini Embeddings

`gemini-embedding-001` is Google's embedding model: strong on the MTEB multilingual leaderboard, 100+ languages, Matryoshka output dimensions (3072 / 1536 / 768), ~2048-token input.

## Key points
- Free tier available via Google AI Studio.
- Used to index a vault for semantic search under [RAG](rag.md).
- Pairs with a Gemini Flash model for the reasoning step.
