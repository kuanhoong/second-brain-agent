"""The four specialist sub-agents that make the second brain *agentic*.

    researcher  -> gathers fresh facts (google_search)
    writer      -> compiles raw/looked-up content into a clean OKF note (write_note)
    linker      -> wires the new note into the index maps (append_index)
    reviewer    -> checks trust signals and flags for human verification (lint_vault)

Each is an LlmAgent. The root orchestrator (see agent.py) delegates to them via
`sub_agents`, so Gemini decides which specialist to hand control to for each step.

NOTE: illustrative — verify class/tool names against your installed `google-adk`.
Some ADK versions require `google_search` to be the ONLY tool on its agent and to
run on a Gemini 2+/flash model; isolating it in `researcher` respects that.
"""
from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools import google_search, agent_tool
from . import tools

MODEL = "gemini-flash-latest"  # pin an exact model id the week of the talk

researcher = LlmAgent(
    name="researcher",
    model=MODEL,
    description="Finds fresh, external facts about a topic using web search.",
    instruction=(
        "You research a topic and return a short, sourced brief (3-6 bullet points, "
        "each with the source URL). Be factual and current. Do not write to the vault; "
        "hand your brief back to the orchestrator."
    ),
    tools=[google_search],
)

writer = LlmAgent(
    name="writer",
    model=MODEL,
    description="Compiles raw notes or a research brief into one clean OKF concept note.",
    instruction=(
        "Turn the provided raw text into ONE atomic OKF note. Distill a 3-5 line summary "
        "plus key points. Call write_note(path, title, body, type, tags) with a sensible "
        "vault-relative path under concepts/. The tool sets status:draft automatically. "
        "Return the path you wrote."
    ),
    tools=[tools.write_note, tools.read_note],
)

linker = LlmAgent(
    name="linker",
    model=MODEL,
    description="Connects a new note into the vault's index maps so nothing is orphaned.",
    instruction=(
        "Given a newly written note's path and title, call append_index(folder, path, title, "
        "summary) to link it from the right folder index (usually 'concepts'). Keep the "
        "summary to one line. Confirm what you linked."
    ),
    tools=[tools.append_index, tools.read_index],
)

reviewer = LlmAgent(
    name="reviewer",
    model=MODEL,
    description="Audits trust signals: finds stale/deprecated/orphan notes and flags drafts for a human.",
    instruction=(
        "Call lint_vault() and report what needs attention: stale notes (past stale_after), "
        "deprecated notes still present, and orphans. For any draft note that resulted from "
        "this session, remind the human to verify it (verify_note) rather than verifying it "
        "yourself. Never mark your own work as verified."
    ),
    tools=[tools.lint_vault],
)

# Wrap the search agent as a TOOL rather than a transfer sub-agent. Gemini forbids
# combining a built-in tool (google_search) with function calling in one request,
# which is exactly what happens when researcher is a transfer sub-agent (ADK injects
# transfer_to_agent). As an AgentTool it runs in its own isolated call with only
# google_search, so real web search works.
research_tool = agent_tool.AgentTool(agent=researcher)

SUB_AGENTS = [writer, linker, reviewer]
