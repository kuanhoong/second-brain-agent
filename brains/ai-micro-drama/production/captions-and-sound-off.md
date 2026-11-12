---
type: Concept
title: Captions and Sound-Off
description: "Designing for viewers who watch muted: captions on every line, placed clear of the app UI."
tags: [production, captions, accessibility]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: morphic-make
    resource: /references/morphic-make.md
    title: How to make a microdrama
  - id: genra-short-drama
    resource: /references/genra-short-drama.md
    title: How to create AI short dramas solo
  - id: invideo-vertical
    resource: /references/invideo-vertical.md
    title: Generating Vertical Shots for AI Micro-Drama
---

# Summary

Captions are not optional: a large share of viewers watch muted.[^morphic-make] One vendor puts it at about 80% of viewers; treat that as a rough claim, not a measurement.[^genra-short-drama]

# Key points

- Keep the bottom third of the frame quiet so captions do not cover faces or action, and stay out of the app's UI zones.[^invideo-vertical]
- Caption every line and make key sound cues visible too: a phone buzzing, a door slamming.[^genra-short-drama]
- Ask the video model for a frame with no text, and add captions in the edit ([describing absence](/prompting/negative-prompting.md)).

# Related

- [Vertical Composition](/cinematography/vertical-composition.md)

[^morphic-make]: How to make a microdrama
[^genra-short-drama]: How to create AI short dramas solo
[^invideo-vertical]: Generating Vertical Shots for AI Micro-Drama
