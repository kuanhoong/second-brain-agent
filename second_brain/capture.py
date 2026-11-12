"""Capture a highlighted passage sent by the Chrome extension.

Two steps, in this order:

1. Code files the highlight verbatim as a Reference. No model involved, so the
   passage is never lost, even with no API key or no network.
2. The `highlight_filer` agent (Gemini) writes one draft concept from it.
"""
from __future__ import annotations

import asyncio
import threading
import uuid

from . import okf, tools

MAX_CHARS = 12000
JOBS: dict[str, dict] = {}


def allowed_origin(origin: str | None) -> bool:
    """Only the extension may post. A web page calling localhost is refused."""
    return bool(origin) and origin.startswith("chrome-extension://")


def file_highlight(url: str, title: str, text: str) -> dict:
    """Step 1: deterministic. Returns {source_id, path, already_filed}."""
    text = (text or "").strip()
    if not text:
        raise ValueError("Nothing highlighted.")
    if not str(url).startswith(("http://", "https://")):
        raise ValueError("Only http and https pages can be captured.")
    title = (title or url).strip()[:150]
    # Written by code, not by a model, so the actor is a process (OKF spec section 7).
    return tools._file_source(
        url, title, "Passage highlighted in the browser and captured with the Chrome extension.",
        "", "", text[:MAX_CHARS], "process:chrome-extension",
    )


async def _summarise(url: str, title: str, text: str, source_id: str) -> dict:
    """Step 2: run the restricted agent once and return save_concept's result."""
    from google.adk.runners import InMemoryRunner
    from google.genai import types

    from .agent import highlight_filer

    runner = InMemoryRunner(agent=highlight_filer, app_name="second_brain_capture")
    session = await runner.session_service.create_session(app_name="second_brain_capture", user_id="extension")
    prompt = (f"source_id: {source_id}\npage title: {title}\npage url: {url}\n\n"
              f"<highlighted_passage>\n{text[:MAX_CHARS]}\n</highlighted_passage>")
    result: dict = {}
    async for event in runner.run_async(user_id="extension", session_id=session.id,
                                        new_message=types.Content(role="user", parts=[types.Part(text=prompt)])):
        for part in (event.content.parts if event.content else None) or []:
            response = part.function_response
            if response and response.name == "save_concept":
                result = dict(response.response or {})
    if not result:
        raise RuntimeError("The model did not write a concept.")
    if "error" in result:
        raise RuntimeError(result["error"])
    return result


def start(url: str, title: str, text: str, summarise=_summarise) -> dict:
    """File the highlight now, summarise in the background. Returns the job record."""
    source = file_highlight(url, title, text)
    job = {"id": uuid.uuid4().hex[:12], "state": "summarising", "source": source["path"],
           "concept": None, "tags": [], "linked_to": [], "error": None}
    JOBS[job["id"]] = job

    def work() -> None:
        try:
            out = asyncio.run(summarise(url, title, text.strip(), source["source_id"]))
            job.update(state="done", concept=out.get("path"), tags=out.get("tags", []),
                       linked_to=out.get("linked_to", []))
        except Exception as exc:  # the highlight itself is already safely on disk
            job.update(state="saved_only", error=str(exc)[:300])
            okf.log("Capture", f"Highlight kept in /{source['path']} but not summarised: {str(exc)[:120]}")

    threading.Thread(target=work, daemon=True).start()
    return job
