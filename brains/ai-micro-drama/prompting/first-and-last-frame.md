---
type: Concept
title: First and Last Frame
description: "Generating the motion between two approved stills: transitions, reveals and transformations."
tags: [prompting, keyframes, veo]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: google-veo31
    resource: /references/google-veo31.md
    title: The ultimate prompting guide for Veo 3.1
---

# Summary

First-and-last-frame generation takes a start image and an end image and fills in the motion between them, with audio.[^google-veo31] Google's example moves from a front view of a singer to a POV shot behind her with a 180-degree arc.[^google-veo31]

# Uses in micro drama

- The makeover reveal: start on the "before" still, end on the "after".
- The slow push from a full figure to a close-up for the cliffhanger frame.
- Hiding a cut: two shots joined by a camera move.

# Key points

- Make both frames in an image model first, so you approve the start and the end.[^google-veo31]
- Keep the camera position consistent between the two stills when only the subject changes.

# Related

- [Image-to-Video Prompting](/prompting/image-to-video-prompting.md)

[^google-veo31]: The ultimate prompting guide for Veo 3.1
