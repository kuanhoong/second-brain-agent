---
type: Concept
title: "Kubernetes Pods"
description: "The smallest deployable unit in Kubernetes — one or more containers sharing network and storage."
status: stable
generated: { by: "human:me", at: 2026-08-20T09:10:00Z }
verified:
  - { by: "human:me", at: 2026-08-20T09:10:00Z }
stale_after: 2027-08-20T00:00:00Z
tags: [kubernetes, devops, containers]
resource: "https://kubernetes.io/docs/concepts/workloads/pods/"
---

# Kubernetes Pods

A Pod is the smallest deployable unit in Kubernetes. It wraps one or more tightly-coupled containers that share the same network namespace (one IP) and can share storage volumes.

## Key points
- Pods are ephemeral — you rarely create them directly; a Deployment or a controller manages them.
- Containers in a Pod are always co-scheduled on the same node.
- Communication inside a Pod is over `localhost`.

## Related
- Scales via a [CI/CD](../playbooks/code-review.md) pipeline in most teams.
