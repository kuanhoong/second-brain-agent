---
type: Concept
title: Open Knowledge Format
description: Google Cloud's open, vendor-neutral spec for knowledge as a directory of markdown files with YAML frontmatter.
resource: https://github.com/GoogleCloudPlatform/open-knowledge-format
tags: [okf, markdown, open-standard, agents]
status: stable
generated: { by: human:kuanhoong, at: 2026-11-08T09:30:00Z }
verified: { by: human:kuanhoong, at: 2026-11-08T09:30:00Z }
stale_after: 2027-02-08T00:00:00Z
sources:
  - id: okf-spec
    resource: /references/okf-spec.md
    title: Open Knowledge Format specification v0.2
---

# Summary

OKF represents knowledge as a bundle: a directory tree of markdown files, each with a YAML frontmatter block. It is a format, not a platform: no SDK, no registry, no required tooling.[^okf-spec]

# Key points

- `type` is the only required frontmatter key. `title`, `description`, `resource` and `tags` are recommended.[^okf-spec]
- `index.md` and `log.md` are reserved filenames for directory listings and update history.[^okf-spec]
- Ordinary markdown links between concepts form a graph. Broken links are allowed: they mark knowledge not written yet.[^okf-spec]
- Version 0.2 adds [trust signals](/concepts/okf-trust-signals.md) in frontmatter.[^okf-spec]

# Related

- [LLM Wiki Pattern](/concepts/llm-wiki-pattern.md)
- [Knowledge Graph](/concepts/knowledge-graph.md)

[^okf-spec]: Open Knowledge Format specification v0.2
