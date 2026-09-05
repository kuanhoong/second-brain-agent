"""OKF (Open Knowledge Format) helpers: parse, write, and graph a vault of
Markdown-with-YAML-frontmatter notes. Pure filesystem — no network, no SDK.

A note is a Markdown file whose body is preceded by a YAML frontmatter block:

    ---
    type: Concept
    title: "..."
    status: stable            # draft | stable | deprecated
    stale_after: 2027-01-01T00:00:00Z
    ---
    # body markdown...
"""
from __future__ import annotations

import datetime as _dt
import os
import re
from pathlib import Path

import yaml

# Vault location: env override, else the sibling `my-second-brain/` folder.
VAULT_DIR = Path(os.environ.get("VAULT_DIR", Path(__file__).resolve().parent.parent / "my-second-brain"))

_FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


def parse(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_markdown) for a note. Missing frontmatter -> ({}, text)."""
    text = Path(path).read_text(encoding="utf-8")
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2).strip()


def dump(frontmatter: dict, body: str) -> str:
    """Serialise frontmatter + body back into an OKF Markdown string."""
    fm = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{fm}\n---\n\n{body.strip()}\n"


def rel(path: Path) -> str:
    """Vault-relative path string (the OKF concept identity)."""
    return str(Path(path).resolve().relative_to(VAULT_DIR.resolve()))


def all_notes() -> list[Path]:
    return sorted(p for p in VAULT_DIR.rglob("*.md"))


def is_stale(frontmatter: dict, now: _dt.datetime | None = None) -> bool:
    """True if the note's stale_after date has passed."""
    raw = frontmatter.get("stale_after")
    if not raw:
        return False
    now = now or _dt.datetime.now(_dt.timezone.utc)
    try:
        when = _dt.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        if when.tzinfo is None:
            when = when.replace(tzinfo=_dt.timezone.utc)
        return when < now
    except ValueError:
        return False


_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")


def links_in(body: str) -> list[str]:
    """Markdown links to other .md notes found in a body."""
    return [m.group(1) for m in _LINK_RE.finditer(body)]


def graph() -> dict:
    """Build a {nodes, links} graph of the whole vault for the visualizer."""
    nodes, links, index = [], [], {}
    notes = all_notes()
    for i, p in enumerate(notes):
        fm, _ = parse(p)
        index[rel(p)] = i
        nodes.append({
            "id": rel(p),
            "title": fm.get("title", p.stem),
            "type": fm.get("type", "Note"),
            "status": fm.get("status", "stable"),
            "stale": is_stale(fm),
        })
    for p in notes:
        fm, body = parse(p)
        src = rel(p)
        base = Path(src).parent
        for tgt in links_in(body):
            resolved = os.path.normpath(str(base / tgt))
            if resolved in index:
                links.append({"source": src, "target": resolved})
    return {"nodes": nodes, "links": links}
