---
type: Concept
title: Reference Image Prompting
description: "Using character, location and style images as ingredients so every shot shares the same cast and set."
tags: [prompting, reference-images, consistency, veo]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-03-10T09:00:00Z
sources:
  - id: google-veo31
    resource: /references/google-veo31.md
    title: The ultimate prompting guide for Veo 3.1
  - id: gemini-api-veo31
    resource: /references/gemini-api-veo31.md
    title: Introducing Veo 3.1 and new creative capabilities in the Gemini API
  - id: fal-kling-seedance
    resource: /references/fal-kling-seedance.md
    title: "Seedance 2.0 vs. Kling 3.0: What's The Difference?"
  - id: seedance-microexpression
    resource: /references/seedance-microexpression.md
    title: "MiniMax H3 Microexpression Prompts: Direct Subtle, Natural Emotion"
---

# Summary

Reference-to-video modes take images of characters, objects, settings or styles and keep them consistent across shots. Google calls this Ingredients to Video.[^google-veo31] In the Gemini API, Veo 3.1 accepts up to three reference images per request.[^gemini-api-veo31]

# Example (from Google's guide)

Create reference images of the detective, the woman and the office. Then: "Using the provided images for the detective, the woman, and the office setting, create a medium shot of the detective behind his desk..." Generate the reverse shot with the same three images.[^google-veo31]

# Key points

- Other models take more references: Seedance 2.0 accepts up to 9 images, 3 videos and 3 audio clips in one call.[^fal-kling-seedance]
- Give each reference one job (face, wardrobe, location) and say so in the prompt.[^seedance-microexpression]

# Related

- [Character Consistency](/characters/character-consistency.md)
- [Shot Routing](/production/shot-routing.md)

[^google-veo31]: The ultimate prompting guide for Veo 3.1
[^gemini-api-veo31]: Introducing Veo 3.1 and new creative capabilities in the Gemini API
[^fal-kling-seedance]: Seedance 2.0 vs. Kling 3.0: What's The Difference?
[^seedance-microexpression]: MiniMax H3 Microexpression Prompts: Direct Subtle, Natural Emotion
