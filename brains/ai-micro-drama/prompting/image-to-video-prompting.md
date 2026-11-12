---
type: Concept
title: Image-to-Video Prompting
description: "When you start from an approved still, describe what moves and changes, not what is already there."
tags: [prompting, image-to-video, keyframes]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: veo3gen-i2v
    resource: /references/veo3gen-i2v.md
    title: Google's Official Veo 3.1 Prompting Guide vs. Community Templates
  - id: invideo-expression
    resource: /references/invideo-expression.md
    title: "How do you improve facial expression quality in AI-generated video?"
  - id: scenario-veo31
    resource: /references/scenario-veo31.md
    title: "Veo 3.1: The Essentials"
---

# Summary

When the input image already fixes the composition, the face, the wardrobe and the palette, spend the prompt on motion, camera movement, changes over time and what must stay stable.[^veo3gen-i2v]

# Key points

- Describe the change: the head turn, the tear, the hand reaching for the phone.
- Name what must not change: "no new people enter the frame", "she keeps holding the letter".[^veo3gen-i2v]
- Start-frame anchoring is also the most reliable way to get a specific expression: make the still with the expression already right.[^invideo-expression]
- In Veo 3.1 a first frame and a set of reference images cannot be combined in the same request; choose one mode per shot.[^scenario-veo31]

# Related

- [Storyboard First](/production/storyboard-first.md)
- [First and Last Frame](/prompting/first-and-last-frame.md)

[^veo3gen-i2v]: Google's Official Veo 3.1 Prompting Guide vs. Community Templates
[^invideo-expression]: How do you improve facial expression quality in AI-generated video?
[^scenario-veo31]: Veo 3.1: The Essentials
