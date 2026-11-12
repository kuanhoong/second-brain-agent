---
type: Concept
title: Continuity and the 180 Rule
description: "Screen direction, eyelines and the 30-degree rule, which AI video breaks unless you plan them."
tags: [cinematography, continuity, editing]
status: draft
generated: { by: research-agent, at: 2026-11-10T09:00:00Z }
stale_after: 2027-11-10T09:00:00Z
sources:
  - id: storyblocks-continuity
    resource: /references/storyblocks-continuity.md
    title: Continuity editing in video
  - id: hackernoon-direction
    resource: /references/hackernoon-direction.md
    title: AI Video Generation Forgets Where the Camera Was
---

# Summary

The 180-degree rule keeps the camera on one side of an imaginary line between two characters, so who is on the left and right stays the same across cuts. The eyeline match shows what a character is looking at, and the 30-degree rule says two shots of the same subject should differ by at least 30 degrees.[^storyblocks-continuity]

AI video has no camera that persists between generations, so nothing enforces the line. Decide which side of the action each shot sits on before you generate, and write it down.[^hackernoon-direction]

# Key points

- Add a "screen side" column to the [shot list](/templates/shot-list-template.md): who is screen-left, who looks screen-right.
- Put the side in the prompt: "she looks toward screen-right".
- Check reverse shots side by side before animating them.

# Related

- [Dialogue Coverage](/cinematography/dialogue-coverage.md)
- [Character Consistency](/characters/character-consistency.md)

[^storyblocks-continuity]: Continuity editing in video
[^hackernoon-direction]: AI Video Generation Forgets Where the Camera Was
