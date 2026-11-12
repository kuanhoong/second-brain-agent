---
type: Concept
title: Audio and Dialogue Prompting
description: "How to write dialogue, sound effects and ambience into a native-audio video prompt."
tags: [prompting, audio, dialogue, veo]
status: draft
generated: { by: research-agent, at: 2026-11-10T09:00:00Z }
stale_after: 2027-05-09T09:00:00Z
sources:
  - id: google-veo31
    resource: /references/google-veo31.md
    title: The ultimate prompting guide for Veo 3.1
---

# Summary

Veo 3.1 generates synchronised sound, including dialogue between several people and timed sound effects.[^google-veo31] Google's syntax has three forms:[^google-veo31]

- **Dialogue** in quotation marks: `A woman says, "We have to leave now."`
- **Sound effects** prefixed with `SFX:`
- **Ambience** prefixed with `Ambient noise:`

# Key points

- Say who speaks and how: the character, the tone and the emotion, then the line.
- Keep each line short enough to fit the clip. Veo clips are 4, 6 or 8 seconds.[^google-veo31]
- For a two-person exchange, generate the line and the reply as separate shots with the same references, then cut between them.[^google-veo31]
- Plan for sound-off viewing anyway; every line also becomes a caption ([captions](/production/captions-and-sound-off.md)).

# Related

- [Dialogue for Vertical](/writing/dialogue-for-vertical.md)
- [Voice Casting](/characters/voice-casting.md)

[^google-veo31]: The ultimate prompting guide for Veo 3.1
