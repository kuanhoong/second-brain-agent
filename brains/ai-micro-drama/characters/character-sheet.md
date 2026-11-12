---
type: Concept
title: Character Sheet
description: "The visual reference for one AI character: a multi-angle turnaround plus close-ups, locked before any video."
tags: [characters, consistency, reference-images]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: invideo-turnaround
    resource: /references/invideo-turnaround.md
    title: "How do you create a multi-angle character turnaround sheet for consistent AI video generation?"
  - id: invideo-lock
    resource: /references/invideo-lock.md
    title: Using character sheet grid panels to keep AI characters consistent
  - id: invideo-ref-count
    resource: /references/invideo-ref-count.md
    title: "How many reference images do you need for consistent AI video character generation?"
  - id: invideo-nano-banana
    resource: /references/invideo-nano-banana.md
    title: Nano Banana 2 vs Nano Banana Pro for character sheets
---

# Summary

A character sheet for AI video is a multi-angle turnaround of one character: front, three-quarter, side and back views, plus a face close-up and a mid-angle close-up, generated at high resolution with the character's hands empty.[^invideo-turnaround] It becomes the canonical reference attached to every shot.

# How to make one

1. Cast the face first: generate portrait options and pick one the way you would pick an actor.[^invideo-turnaround]
2. Generate the turnaround from that locked portrait, in a neutral pose on a plain background.[^invideo-turnaround]
3. Make about four options per sheet, choose the best, and lock it before any video is generated.[^invideo-lock]
4. Write a short text description to go with it: the same five or six identifying details in every prompt.

# Key points

- Two to six reference images per character is enough: a headshot and a full-body view at minimum, the full turnaround for best results.[^invideo-ref-count]
- Nano Banana Pro is a common choice for sheets because of strong prompt adherence; Nano Banana 2 is faster for exploring options.[^invideo-nano-banana]

# Related

- [Character Consistency](/characters/character-consistency.md)
- [Character Sheet Template](/templates/character-sheet-template.md)

[^invideo-turnaround]: How do you create a multi-angle character turnaround sheet for consistent AI video generation?
[^invideo-lock]: Using character sheet grid panels to keep AI characters consistent
[^invideo-ref-count]: How many reference images do you need for consistent AI video character generation?
[^invideo-nano-banana]: Nano Banana 2 vs Nano Banana Pro for character sheets
