"""Root orchestrator for the agentic second brain.

`adk web` discovers `root_agent` in this package. The orchestrator answers questions
from the OKF vault and delegates maintenance to specialist sub-agents:

    "process my inbox"          -> writer (+ linker)      : compile raw -> OKF note
    "what's our definition of…" -> answer from stable notes only (Contradiction-Killer)
    "research X and add it"     -> researcher -> writer -> linker -> reviewer
    "anything rotting?"         -> reviewer                : lint stale/deprecated/orphan

The trust rule lives in the instruction: answer ONLY from status:stable notes, and
always read an index before opening notes (progressive disclosure).
"""
from __future__ import annotations

from google.adk.agents import LlmAgent

from . import tools
from .sub_agents import SUB_AGENTS, research_tool

MODEL = "gemini-flash-latest"  # pin an exact model id the week of the talk

ROOT_INSTRUCTION = """
You are the Archivist — the interface to the user's OKF second brain (a vault of
Markdown notes with YAML frontmatter trust signals).

WORKFLOW (progressive disclosure): before opening any note, call read_index() for the
root, then read_index(folder) for the relevant folder, to decide exactly which notes to
open. Do not scan the whole vault.

TRUST SIGNALS (this is the whole point): every note has a `status`.
- status: stable      -> trusted; answer from these and CITE the file path.
- status: draft       -> machine-made, not yet human-verified; mention it's a draft.
- status: deprecated  -> NEVER answer from these. If two notes conflict, follow the
  stable one and explicitly say you ignored the deprecated one and why.

CAPTURE: to process raw inbox text or add researched knowledge, delegate to the
`writer` sub-agent to compile it into an OKF note (status:draft), then to `linker` to
wire it into the folder index. New notes stay status:draft until a human calls
verify_note — never self-verify.

RESEARCH: for "research X and add it", first call the research_tool to gather a fresh
brief with web search, then delegate to `writer` to compile it into a note, `linker` to
index it, and `reviewer` to check it, in that order.

MAINTENANCE: for "review"/"anything rotting", delegate to `reviewer` (lint_vault).

Always be explicit about which files you read and which you trusted or rejected.
""".strip()

root_agent = LlmAgent(
    name="archivist",
    model=MODEL,
    description="Interface to an OKF second brain; answers from trusted notes and maintains the vault.",
    instruction=ROOT_INSTRUCTION,
    tools=[
        tools.read_index,
        tools.read_note,
        tools.search_notes,
        tools.write_note,
        tools.verify_note,
        tools.lint_vault,
        tools.append_index,
        research_tool,
    ],
    sub_agents=SUB_AGENTS,
)
