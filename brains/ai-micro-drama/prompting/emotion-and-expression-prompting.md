---
type: Concept
title: Emotion and Expression Prompting
description: "Directing a face: visible evidence and timing instead of emotion words."
tags: [prompting, performance, emotion]
status: draft
generated: { by: research-agent, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: seedance-microexpression
    resource: /references/seedance-microexpression.md
    title: "MiniMax H3 Microexpression Prompts: Direct Subtle, Natural Emotion"
  - id: kling-advanced
    resource: /references/kling-advanced.md
    title: 5 Advanced Prompting Techniques for Hyper-Realistic Videos
  - id: invideo-expression
    resource: /references/invideo-expression.md
    title: "How do you improve facial expression quality in AI-generated video?"
---

# Summary

Emotion words alone ("sad", "angry") produce stock, flat or exaggerated faces. Name the emotion, the visible facial evidence, what triggers it and the moment it settles, and use one restrained change rather than a stack of dramatic words.[^seedance-microexpression]

> Close-up. She reads the message. Her jaw tightens, her eyes stay dry, then she exhales slowly and sets the phone face down.

# Key points

- Pick one or two facial details to describe; too many confuse the model. Body language (shoulders, hands) sells the emotion as much as the face.[^kling-advanced]
- Set the expression in a start frame and animate from it.[^invideo-expression]
- For mixed emotion, define the order: eyes brighten, shoulders soften, an almost-smile, composure returns.[^seedance-microexpression]
- Judge performance in motion, not from a flattering paused frame.[^seedance-microexpression]

# Related

- [Dialogue for Vertical](/writing/dialogue-for-vertical.md)
- [Shot Routing](/production/shot-routing.md)

[^seedance-microexpression]: MiniMax H3 Microexpression Prompts: Direct Subtle, Natural Emotion
[^kling-advanced]: 5 Advanced Prompting Techniques for Hyper-Realistic Videos
[^invideo-expression]: How do you improve facial expression quality in AI-generated video?
