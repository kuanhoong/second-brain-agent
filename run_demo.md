# Demo runsheet — the multi-agent second brain

Split your screen: **left** = the `adk web` chat (shows the live tool-call / agent-transfer trace), **right** = `viz.html` (the knowledge graph, color-coded by trust signal). Every prompt below changes the graph on the right.

> Reliability: agents are non-deterministic. Run `./reset.sh` before every rehearsal and before you go on stage, keep a spare API key, and have the backup recording queued. Decide your abort-to-video trigger in advance (e.g. no answer in ~20s).

## Setup (once)
```bash
pip install -r requirements.txt
cp .env.example .env          # paste your Google AI Studio key
python build_viz.py           # generate viz.html, open it in a browser
adk web                       # opens the dev UI; pick the "archivist" agent
```

## The 4-beat storyline (~6–7 min)

**Act 1 — CAPTURE → COMPILE** *(orchestrator → writer → linker)*
> Prompt: **"Process the raw note in my inbox and file it properly."**
Watch: the writer compiles `00_inbox/dump.md` into a clean `concepts/…md` (status: **draft**), the linker adds it to the concepts index. Refresh `viz.html` → a new **amber** node appears, wired into the graph.
Say: *"Messy in, structured knowledge out — it filed and linked itself. That's the compiler."*

**Act 2 — QUERY → the Contradiction-Killer** *(the moment to protect)*
> Prompt: **"What are our criteria for a successful project?"**
Watch (in the trace): reads root index → playbooks index → opens BOTH playbooks → **rejects `project-success-legacy` because status: deprecated** → answers from `project-success-v2`, citing it.
Say: *"It didn't average two contradictory notes. It reasoned about which to trust."*

**Act 3 — RESEARCH → ADD** *(researcher → writer → linker → reviewer — the full multi-agent chain)*
> Prompt: **"Research the current impact of AI Overviews on click-through, and add it to my brain."**
Watch: researcher runs `google_search`; writer drafts a new OKF note (status: **draft**); linker indexes it; reviewer runs `lint_vault` and asks you to verify. New amber node on the graph.
Say: *"Four specialist agents — research, write, link, review — and a human still signs off."*

**Act 4 — MAINTAIN + VERIFY → node goes green** *(reviewer, then a human verify)*
> Prompt: **"Anything in my brain rotting or contradictory?"**
Watch: reviewer flags `agentic-search` (past `stale_after`) and the deprecated legacy playbook.
> Prompt: **"Verify concepts/<the draft you just wrote>."**
Watch: `verify_note` stamps it stable → refresh `viz.html` → the node flips **amber → green**.
Say: *"Your second brain does its own upkeep — and you stay the human in the loop."*

**Close:** zoom out on the tidier, mostly-green graph. *"RAG reads your notes. This agent keeps them."*

## Between runs
```bash
./reset.sh     # restores the vault, rebuilds viz.html
```

## Fallbacks
- Act 1/3 write misbehaves → `git checkout -- my-second-brain`, use a pre-written note, or cut to recording.
- Act 3 network/`google_search` flaky → skip to Act 4, or use the canned draft in `demo_backup/`.
- Anything red → play the full screen recording; the acts are independent, so you can also drop Act 3 or 4 for time.
