# Stage runsheet

Screen: `adk web` chat on the left half, `http://localhost:8765` graph on the right half. Browser zoom 125% on both.

## Before you walk on

```bash
./reset.sh                      # vault back to the seed state
python scripts/validate.py      # expect "conformant": true
python graph_server.py          # terminal 1
adk web                         # terminal 2, pick second_brain, start a NEW session
```

Load the extension once (`chrome://extensions`, Developer mode, Load unpacked, `extension/`), pin it to the toolbar, and keep the embeddings docs page open in a tab.

Check the graph shows 9 concepts, 2 gaps, 1 stale. Send one throwaway prompt ("hello") so the first real call is not a cold start. Have a second API key in `.env.backup`.

## Beats (about 9 minutes)

**0. Read the graph (45 s).** No prompt. Point at: green = I reviewed it, blue = a machine checked it, grey = deprecated, red ring = stale, dashed = linked but not written. Click *Open Knowledge Format* to show the frontmatter panel.

**1. Capture from the web (2.5 min).**
> Research Model Context Protocol and add it to my brain.

Watch the trace: `brain_overview` → `web_scout` → `save_source` (x2 or x3) → `save_concept`. On the graph the dashed MCP node turns solid amber and pulses, with new source diamonds and tag dots. Click it: summary, key points, tags, `status: draft`, `generated.by`, footnoted sources. Say: nobody typed a tag or a link.

**2. Highlight and save (1.5 min).** Open https://ai.google.dev/gemini-api/docs/embeddings in a tab. Highlight the opening paragraph, click the extension button, click **Save highlight**.

The popup shows the passage, then the path, tags and link count. On the graph a source diamond appears first (the highlight, saved by code), then an amber concept (written by Gemini). Click the diamond to show the passage quoted word for word.

Typed fallback if the extension misbehaves:
> Read https://ai.google.dev/gemini-api/docs/embeddings and add a note called Vector Embeddings.

**3. Ask, and the contradiction (1.5 min).**
> Which OKF field records when a concept last changed?

Two notes disagree. The agent should answer `generated.at`, cite `concepts/okf-trust-signals.md`, and say it ignored the deprecated v0.1 note. This beat needs no network beyond Gemini itself. Protect it.

**4. What next? (1.5 min).**
> What should I learn next, and is anything going stale?

`review_brain` returns the stale *Gemini Models* note, any new gaps the captures created, and thinly covered tags. Then:
> Refresh the Gemini Models note.

The red-ringed green node becomes amber: new content, and trust resets because a different actor wrote it.

**5. Trust ladder (2 min).**
> Fact-check the Model Context Protocol note.

`fact_checker` re-reads the sources, `record_check` adds a machine `verified` entry. Amber turns blue.
> I have read it. Verify it.

ADK shows a confirmation prompt. Click confirm. Blue turns green, status becomes stable. Open the file in an editor and show the two `verified` entries.

**Close.** Open `vault/` in a file browser or Obsidian. It is a folder of markdown. `git diff` shows exactly what the agent changed.

## If something breaks

| Problem | Do this |
|---|---|
| Search or URL read hangs past 25 s | Stop the run. In a third terminal: `python scripts/offline_capture.py model-context-protocol`. The graph updates the same way. Say so openly. |
| Beat 4 refresh fails | `python scripts/offline_capture.py gemini-models` |
| Extension popup says it cannot reach the second brain | `graph_server.py` is not running or is on another port. Use the typed fallback for beat 2. |
| Quota or key error | Swap in the backup key, restart `adk web`. |
| Agent skips a step or rambles | Start a new session and repeat the prompt. Sessions are independent. |
| Everything is down | `python graph_server.py --export viz.html` beforehand and walk through the exported file, or play the screen recording. |

Beats 2 and 4b are optional. Cut them first if you are short on time. Beats 1, 3 and 5 carry the talk.
