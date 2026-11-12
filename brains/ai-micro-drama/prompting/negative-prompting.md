---
type: Concept
title: Describing Absence
description: "How to keep things out of a shot: describe the empty scene instead of writing 'no X'."
tags: [prompting, veo]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: google-veo31
    resource: /references/google-veo31.md
    title: The ultimate prompting guide for Veo 3.1
  - id: veo3gen-i2v
    resource: /references/veo3gen-i2v.md
    title: Google's Official Veo 3.1 Prompting Guide vs. Community Templates
---

# Summary

Google's guide recommends describing what the scene looks like without the unwanted thing, rather than using negation: "a desolate landscape with no buildings or roads" instead of "no man-made structures".[^google-veo31]

# Key points

- For image-to-video, name what must stay stable instead of listing what must not happen.[^veo3gen-i2v]
- Common micro-drama uses: no extra people entering frame, no on-screen text, no logos.
- If a model keeps adding burned-in subtitles to dialogue shots, say the frame has no text and add captions in the edit ([captions](/production/captions-and-sound-off.md)).

# Related

- [Video Prompt Formula](/prompting/video-prompt-formula.md)

[^google-veo31]: The ultimate prompting guide for Veo 3.1
[^veo3gen-i2v]: Google's Official Veo 3.1 Prompting Guide vs. Community Templates
