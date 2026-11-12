---
type: Concept
title: Shot Routing
description: Sending each shot type to the model that handles it best.
tags: [production, ai-video, models, workflow]
status: draft
generated: { by: research-agent, at: 2026-11-10T09:00:00Z }
stale_after: 2027-01-09T09:00:00Z
sources:
  - id: invideo-vertical
    resource: /references/invideo-vertical.md
    title: Generating Vertical Shots for AI Micro-Drama
  - id: invideo-expression
    resource: /references/invideo-expression.md
    title: "How do you improve facial expression quality in AI-generated video?"
  - id: invideo-kling-vs-seedance
    resource: /references/invideo-kling-vs-seedance.md
    title: "Seedance 2.0 vs Kling 3.0: which AI video model is better for multi-shot storyboard animation?"
---

# Summary

No single model is best at every shot. One documented approach routes tight vertical close-ups and facial performance to Veo, multi-shot dialogue to Kling, and continuity shots that must match a previous shot to Seedance 2.0 reference-to-video.[^invideo-vertical]

# Key points

- Inserts and two-second cutaways do not need continuity setup; prompt them straight from the script.[^invideo-vertical]
- For facial performance, one vendor currently rates Kling 3.0 highest.[^invideo-expression]
- Kling's storyboard mode suits shot-level precision across a sequence; Seedance suits feeding many references and chaining segments.[^invideo-kling-vs-seedance]
- Treat routing as a rule in the [series bible](/characters/series-bible.md), and re-test it when models update.

# Related

- [Video Model Landscape](/production/video-model-landscape.md)

[^invideo-vertical]: Generating Vertical Shots for AI Micro-Drama
[^invideo-expression]: How do you improve facial expression quality in AI-generated video?
[^invideo-kling-vs-seedance]: Seedance 2.0 vs Kling 3.0: which AI video model is better for multi-shot storyboard animation?
