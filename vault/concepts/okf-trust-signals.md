---
type: Concept
title: OKF Trust Signals
description: The optional OKF v0.2 frontmatter families that record provenance, trust and lifecycle for each concept.
tags: [okf, trust, provenance, agents]
status: stable
generated: { by: human:kuanhoong, at: 2026-11-08T09:45:00Z }
verified: { by: human:kuanhoong, at: 2026-11-08T09:45:00Z }
stale_after: 2027-02-08T00:00:00Z
sources:
  - id: okf-spec
    resource: /references/okf-spec.md
    title: Open Knowledge Format specification v0.2
---

# Summary

When agents write most of a knowledge base, a reader needs to know where a concept came from, who confirmed it and whether it is still current. OKF v0.2 answers these from frontmatter.[^okf-spec]

# Key points

- `sources` lists what a concept derives from. Footnotes keyed to a source `id` attribute individual claims.[^okf-spec]
- `generated: { by, at }` records who wrote the current content and when it last changed. `verified` records who confirmed it.[^okf-spec]
- Trust tiers are derived from `verified`: none is unverified, non-human actors only is machine-confirmed, a `human:` actor is human-reviewed.[^okf-spec]
- `status` is draft, stable or deprecated. `stale_after` is an absolute instant after which the content is stale.[^okf-spec]
- Every timestamp is an ISO 8601 datetime with an explicit UTC offset.[^okf-spec]

# Related

- [Open Knowledge Format](/concepts/open-knowledge-format.md)

[^okf-spec]: Open Knowledge Format specification v0.2
