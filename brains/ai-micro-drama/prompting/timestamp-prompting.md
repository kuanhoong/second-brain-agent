---
type: Concept
title: Timestamp Prompting
description: "Directing several shots inside one generation with time ranges, and the multi-shot modes that do the same."
tags: [prompting, multi-shot, veo, kling]
status: draft
generated: { by: research-agent, at: 2026-11-10T09:00:00Z }
stale_after: 2027-03-10T09:00:00Z
sources:
  - id: google-veo31
    resource: /references/google-veo31.md
    title: The ultimate prompting guide for Veo 3.1
  - id: invideo-kling-vs-seedance
    resource: /references/invideo-kling-vs-seedance.md
    title: "Seedance 2.0 vs Kling 3.0: which AI video model is better for multi-shot storyboard animation?"
  - id: invideo-vertical
    resource: /references/invideo-vertical.md
    title: Generating Vertical Shots for AI Micro-Drama
---

# Summary

Timestamp prompting splits one clip into timed shots, for example `[00:00-00:02] Medium shot from behind... [00:02-00:04] Reverse shot of her face...`, each with its own camera, action and sound.[^google-veo31]

# Key points

- Good for a fast exchange of reactions inside one 8-second clip.
- Kling 3.0 has a dedicated multi-shot storyboard mode that takes up to six per-shot prompts with duration control.[^invideo-kling-vs-seedance]
- For anything you need to edit precisely, generate shots separately: you get coverage and control in the edit.[^invideo-vertical]

# Related

- [Video Prompt Formula](/prompting/video-prompt-formula.md)
- [Editing and Pacing](/production/editing-and-pacing.md)

[^google-veo31]: The ultimate prompting guide for Veo 3.1
[^invideo-kling-vs-seedance]: Seedance 2.0 vs Kling 3.0: which AI video model is better for multi-shot storyboard animation?
[^invideo-vertical]: Generating Vertical Shots for AI Micro-Drama
