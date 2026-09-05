---
type: Concept
title: "Go Goroutines"
description: "Lightweight, cheaply-multiplexed concurrent functions managed by the Go runtime."
status: stable
generated: { by: "human:me", at: 2026-08-20T09:15:00Z }
verified:
  - { by: "human:me", at: 2026-08-20T09:15:00Z }
stale_after: 2027-08-20T00:00:00Z
tags: [go, concurrency]
resource: "https://go.dev/tour/concurrency/1"
---

# Go Goroutines

A goroutine is a function running concurrently, scheduled by the Go runtime onto OS threads. Start one with the `go` keyword: `go doWork()`.

## Key points
- Cheap: a goroutine starts at a few KB of stack and grows as needed — you can have hundreds of thousands.
- Communicate by **channels**, not shared memory ("share memory by communicating").
- Use `sync.WaitGroup` or a channel to wait for completion; a leaked goroutine that never returns is a common bug.
