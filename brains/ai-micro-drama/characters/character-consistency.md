---
type: Concept
title: Character Consistency
description: "Keeping the same face, build and wardrobe across hundreds of AI shots: a workflow, not a prompt."
tags: [characters, consistency, ai-video, reference-images]
status: draft
generated: { by: research-agent, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: figma-consistency
    resource: /references/figma-consistency.md
    title: AI character consistency across scenes
  - id: invideo-lock
    resource: /references/invideo-lock.md
    title: Using character sheet grid panels to keep AI characters consistent
  - id: gemini-api-veo31
    resource: /references/gemini-api-veo31.md
    title: Introducing Veo 3.1 and new creative capabilities in the Gemini API
  - id: google-veo31
    resource: /references/google-veo31.md
    title: The ultimate prompting guide for Veo 3.1
  - id: invideo-expression
    resource: /references/invideo-expression.md
    title: "How do you improve facial expression quality in AI-generated video?"
  - id: seedance-microexpression
    resource: /references/seedance-microexpression.md
    title: "MiniMax H3 Microexpression Prompts: Direct Subtle, Natural Emotion"
---

# Summary

Video models generate each clip with no memory of the last one, so faces, clothes and props drift unless every generation is anchored to the same references.[^figma-consistency] Consistency comes from the workflow around each generation, not from a sharper description.[^figma-consistency]

# The workflow

1. Lock a [character sheet](/characters/character-sheet.md) before generating any video.[^invideo-lock]
2. Approve keyframes as stills first, then animate them in short shots.[^figma-consistency]
3. Attach the same references to every generation of that character. Veo 3.1 takes up to three reference images per request.[^gemini-api-veo31]
4. Reuse the same reference images across prompts and break scenes into sequential shots rather than one long prompt.[^google-veo31]

# Key points

- Starting each shot from an approved still keeps the face and the expression under control.[^invideo-expression]
- When identity slips as an emotion peaks, reduce camera travel and simplify the expression.[^seedance-microexpression]

# Related

- [Reference Image Prompting](/prompting/reference-image-prompting.md)
- [Costume and Per-Beat Sheets](/characters/costume-and-per-beat-sheets.md)

[^figma-consistency]: AI character consistency across scenes
[^invideo-lock]: Using character sheet grid panels to keep AI characters consistent
[^gemini-api-veo31]: Introducing Veo 3.1 and new creative capabilities in the Gemini API
[^google-veo31]: The ultimate prompting guide for Veo 3.1
[^invideo-expression]: How do you improve facial expression quality in AI-generated video?
[^seedance-microexpression]: MiniMax H3 Microexpression Prompts: Direct Subtle, Natural Emotion
