"""FunctionTools the ADK agents use to query and maintain the OKF vault.

ADK turns each function into a tool and uses its *docstring* as the tool
description the model reads, so the docstrings here are written for the model.
Everything operates on plain files under VAULT_DIR — deterministic, offline.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

from . import okf


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_index(folder: str = "") -> str:
    """Read an index map for progressive disclosure (ALWAYS call this before opening notes).

    Args:
        folder: "" for the root index, or a folder name like "concepts" or "playbooks".
    Returns:
        The Markdown of the index file, which lists the notes available and what each covers.
    """
    path = okf.VAULT_DIR / (folder or "") / "index.md"
    if not path.exists():
        return f"No index found at {folder or '(root)'}."
    return path.read_text(encoding="utf-8")


def read_note(path: str) -> str:
    """Open one note by its vault-relative path (e.g. 'playbooks/project-success-v2.md').

    Returns the note's status/title plus its body. Do NOT answer from a note whose
    status is 'deprecated'; prefer 'stable' notes.
    """
    p = okf.VAULT_DIR / path
    if not p.exists():
        return f"Note not found: {path}"
    fm, body = okf.parse(p)
    head = f"[status={fm.get('status','?')} | type={fm.get('type','?')} | title={fm.get('title','?')}]"
    return f"{head}\n\n{body}"


def search_notes(query: str) -> list[dict]:
    """Keyword search over every note's title, tags, and body.

    Returns a list of {path, title, status, snippet}. This is a simple substring
    search — for the demo it stands in for a semantic (embedding) search.
    """
    q = query.lower()
    hits = []
    for p in okf.all_notes():
        fm, body = okf.parse(p)
        hay = f"{fm.get('title','')} {' '.join(map(str, fm.get('tags', [])))} {body}".lower()
        if q in hay:
            idx = hay.find(q)
            hits.append({
                "path": okf.rel(p),
                "title": fm.get("title", p.stem),
                "status": fm.get("status", "stable"),
                "snippet": body[max(0, idx - 40): idx + 80].strip(),
            })
    return hits[:8]


def write_note(path: str, title: str, body: str, type: str = "Concept", tags: list[str] = []) -> str:
    """Compile raw content into a new OKF note and file it.

    Writes valid frontmatter with status:draft and generated:{by,at} so it is clearly
    machine-made and awaits human verification. Use a sensible vault-relative path such
    as 'concepts/my-topic.md'. Returns the path written.
    """
    p = okf.VAULT_DIR / path
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = {
        "type": type,
        "title": title,
        "status": "draft",
        "generated": {"by": "archivist/gemini", "at": _now()},
        "tags": tags or [],
    }
    p.write_text(okf.dump(fm, body), encoding="utf-8")
    _log(f"write_note {path} (status:draft)")
    return okf.rel(p)


def verify_note(path: str, by: str = "human:me") -> str:
    """Promote a draft note to status:stable and stamp a human verification.

    Call ONLY when a human has approved the note. Returns a confirmation string.
    """
    p = okf.VAULT_DIR / path
    if not p.exists():
        return f"Note not found: {path}"
    fm, body = okf.parse(p)
    fm["status"] = "stable"
    fm.setdefault("verified", []).append({"by": by, "at": _now()})
    p.write_text(okf.dump(fm, body), encoding="utf-8")
    _log(f"verify_note {path} (now status:stable)")
    return f"{path} verified by {by} -> status:stable"


def lint_vault() -> dict:
    """Health-check the vault: find stale, deprecated, and orphan notes.

    Returns {stale: [...], deprecated: [...], orphans: [...]} of vault-relative paths.
    'stale' = past its stale_after date; 'orphans' = not linked from any index.
    """
    g = okf.graph()
    linked = {l["target"] for l in g["links"]} | {n["id"] for n in g["nodes"] if n["id"].endswith("index.md")}
    stale, deprecated, orphans = [], [], []
    for n in g["nodes"]:
        if n["stale"]:
            stale.append(n["id"])
        if n["status"] == "deprecated":
            deprecated.append(n["id"])
        if n["id"] not in linked and not n["id"].endswith("index.md"):
            orphans.append(n["id"])
    return {"stale": stale, "deprecated": deprecated, "orphans": orphans}


def append_index(folder: str, path: str, title: str, summary: str) -> str:
    """Add a bullet linking a new note into a folder's index.md (keeps the graph connected)."""
    idx = okf.VAULT_DIR / (folder or "") / "index.md"
    if not idx.exists():
        return f"No index at {folder}"
    name = Path(path).name
    line = f"- [{title}]({name}) - {summary}\n"
    with idx.open("a", encoding="utf-8") as f:
        f.write(line)
    _log(f"append_index {folder} -> {name}")
    return f"Linked {name} into {folder}/index.md"


def _log(msg: str) -> None:
    log = okf.VAULT_DIR / "log.md"
    try:
        with log.open("a", encoding="utf-8") as f:
            f.write(f"- {_now()} - archivist - {msg}\n")
    except OSError:
        pass
