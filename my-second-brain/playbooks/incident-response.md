---
type: Playbook
title: "Incident Response"
description: "Steps for handling a production incident."
status: stable
generated: { by: "human:me", at: 2026-08-24T09:20:00Z }
verified:
  - { by: "human:me", at: 2026-08-24T09:20:00Z }
stale_after: 2027-08-24T00:00:00Z
tags: [playbook, oncall, sre]
---

# Incident Response

1. **Stabilise** — mitigate first (roll back / feature-flag off), diagnose second.
2. **Communicate** — post status every 15 minutes, even "no change".
3. **Assign roles** — one incident commander, one comms, one investigator.
4. **Blameless postmortem** — capture the timeline and the fix in the second brain within 48h.
