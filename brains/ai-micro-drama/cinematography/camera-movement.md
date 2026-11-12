---
type: Concept
title: Camera Movement
description: "Static, push-in, pull-back, tracking, pan, crane, orbit and handheld, and how to prompt them."
tags: [cinematography, camera-movement, vocabulary]
status: draft
generated: { by: claude/claude-opus-5-5, at: 2026-11-10T09:00:00Z }
stale_after: 2027-11-10T09:00:00Z
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

Google's guide lists dolly, tracking, crane, aerial, slow pan and POV shots as camera movements Veo understands.[^google-veo31] If you want the camera to move, say so in its own sentence.[^ltx-veo]

| Move | Effect | Micro-drama use |
| --- | --- | --- |
| Static (locked off) | Calm, observational | Dialogue, most shots |
| Push-in (dolly in) | Rising tension, realisation | The cliffhanger close-up |
| Pull-back (dolly out) | Isolation, reveal of context | Revealing who else is in the room |
| Tracking | Following action | Walking into the gala |
| Pan / tilt | Scanning, revealing | Tilting up from shoes to face |
| Crane / arc | Grandeur, transition | Season openers, transitions |
| Handheld | Urgency, chaos | Fights, chases |

# Key points

- One move per shot. Conflicting camera directives in one prompt confuse the model.[^veo3gen-i2v]
- Lock the camera first, and add a slow push-in on a later attempt once the action works.
- In a vertical frame a forward push feels stronger than a sideways move, because the frame fills the viewer's whole field of view.

# Related

- [Camera Angles](/cinematography/camera-angles.md)

[^google-veo31]: The ultimate prompting guide for Veo 3.1
[^ltx-veo]: Veo 3.1 Prompt Guide
[^veo3gen-i2v]: Google's Official Veo 3.1 Prompting Guide vs. Community Templates
