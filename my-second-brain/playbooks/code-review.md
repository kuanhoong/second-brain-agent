---
type: Playbook
title: "Code Review"
description: "How we review pull requests."
status: stable
generated: { by: "human:me", at: 2026-08-24T09:00:00Z }
verified:
  - { by: "human:me", at: 2026-08-24T09:00:00Z }
stale_after: 2027-08-24T00:00:00Z
tags: [playbook, engineering, review]
---

# Code Review

1. Understand the *why* before the *how* — read the PR description first.
2. Correctness, then tests, then readability, then style (in that priority order).
3. Prefer small, reversible PRs; block on missing tests for new behaviour.
4. Comment as a collaborator, not a gatekeeper.
