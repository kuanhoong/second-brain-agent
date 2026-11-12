---
type: Concept
title: Video Prompt Formula
description: "The five-part structure for a video prompt: cinematography, subject, action, context, style and ambiance."
tags: [prompting, veo, ai-video]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: google-veo31
    resource: /references/google-veo31.md
    title: The ultimate prompting guide for Veo 3.1
  - id: ltx-veo
    resource: /references/ltx-veo.md
    title: Veo 3.1 Prompt Guide
  - id: veo3gen-i2v
    resource: /references/veo3gen-i2v.md
    title: Google's Official Veo 3.1 Prompting Guide vs. Community Templates
---

# Summary

Google's guide for Veo 3.1 structures a prompt as **cinematography + subject + action + context + style and ambiance**, and calls the cinematography part the most powerful lever for tone and emotion.[^google-veo31]

> Medium shot, a tired office worker rubbing his temples, at a cluttered desk late at night, lit by harsh fluorescent light and a green monitor glow. Retro look, grainy film.

# Key points

- Put the camera instruction first, as its own sentence, then describe the subject.[^ltx-veo]
- One action and one camera move per shot. Conflicting directives (a wide shot and an extreme close-up in one prompt) confuse the model.[^veo3gen-i2v]
- Add audio explicitly; see [audio and dialogue prompting](/prompting/audio-and-dialogue-prompting.md).
- For micro drama, also state the vertical frame and where things sit in it ([vertical prompting](/prompting/vertical-prompting.md)).

# Related

- [Video Prompt Template](/templates/video-prompt-template.md)
- [Shot Sizes](/cinematography/shot-sizes.md)

[^google-veo31]: The ultimate prompting guide for Veo 3.1
[^ltx-veo]: Veo 3.1 Prompt Guide
[^veo3gen-i2v]: Google's Official Veo 3.1 Prompting Guide vs. Community Templates
