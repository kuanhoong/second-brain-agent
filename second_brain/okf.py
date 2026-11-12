"""Open Knowledge Format (OKF) v0.2 helpers.

Everything here is plain filesystem work: parse, write, index, log, validate and
graph a bundle of Markdown files with YAML frontmatter. No network, no LLM.

Spec: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
"""
from __future__ import annotations

import datetime as dt
import os
import re
from pathlib import Path

import yaml

OKF_VERSION = "0.2"
RESERVED = {"index.md", "log.md"}

VAULT_DIR = Path(
    os.environ.get("VAULT_DIR", Path(__file__).resolve().parent.parent / "vault")
).resolve()

FOLDER_BLURBS = {
    "concepts": "Ideas, definitions and summaries. Mostly written by the agent, reviewed by a human.",
    "references": "External sources mirrored as first-class concepts (OKF spec section 6.3).",
    "industry": "Market, platforms, money and the tropes that sell.",
    "writing": "Episode and season structure, hooks, cliffhangers and dialogue.",
    "characters": "Bibles, character sheets, consistency and voices.",
    "prompting": "How to write prompts for video models: formula, audio, references, emotion.",
    "cinematography": "Shot sizes, angles, movement, light, vertical framing and continuity.",
    "production": "The pipeline, models, editing, captions, sound and dubbing.",
    "distribution": "Labels, regulation, rights and consent.",
    "templates": "Fill-in templates for sheets, bibles, scripts, shot lists and prompts.",
}

_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)
_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")


# --------------------------------------------------------------------------- time
def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def iso(value: dt.datetime | dt.date | str | None) -> str:
    """Render any timestamp as ISO 8601 with an explicit UTC offset (spec section 5)."""
    if value is None:
        return ""
    if isinstance(value, str):
        parsed = parse_time(value)
        return iso(parsed) if parsed else value
    if isinstance(value, dt.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt.datetime(value.year, value.month, value.day, tzinfo=dt.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def parse_time(value) -> dt.datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, dt.datetime):
        return value if value.tzinfo else value.replace(tzinfo=dt.timezone.utc)
    if isinstance(value, dt.date):
        return dt.datetime(value.year, value.month, value.day, tzinfo=dt.timezone.utc)
    try:
        parsed = dt.datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


# ---------------------------------------------------------------- parse and write
def parse_text(text: str) -> tuple[dict, str]:
    match = _FM_RE.match(text)
    if not match:
        return {}, text
    try:
        fm = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}, text
    return (fm if isinstance(fm, dict) else {}), match.group(2).strip()


def parse(path: Path) -> tuple[dict, str]:
    """Return (frontmatter, body). A file without frontmatter gives ({}, text)."""
    return parse_text(Path(path).read_text(encoding="utf-8"))


_PLAIN = re.compile(r"^[A-Za-z0-9_./@+-][A-Za-z0-9 _./@+()'-]*$")


def _scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (dt.datetime, dt.date)):
        return iso(value)
    text = str(value)
    if parse_time(text) and re.match(r"^\d{4}-\d{2}-\d{2}T", text):
        return iso(text)
    if _PLAIN.match(text) and text.lower() not in {"true", "false", "null", "yes", "no", "on", "off", "~"}:
        try:
            float(text)
        except ValueError:
            return text
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _inline_map(mapping: dict) -> str:
    return "{ " + ", ".join(f"{k}: {_scalar(v)}" for k, v in mapping.items()) + " }"


def dump(frontmatter: dict, body: str) -> str:
    """Serialise frontmatter and body in the compact style the spec's examples use."""
    lines = ["---"]
    for key, value in frontmatter.items():
        if value is None or value == [] or value == {}:
            continue
        if isinstance(value, dict):
            lines.append(f"{key}: {_inline_map(value)}")
        elif isinstance(value, list) and all(isinstance(v, dict) for v in value):
            lines.append(f"{key}:")
            for item in value:
                if key == "sources":
                    first = True
                    for k, v in item.items():
                        lines.append(f"  {'- ' if first else '  '}{k}: {_scalar(v)}")
                        first = False
                else:
                    lines.append(f"  - {_inline_map(item)}")
        elif isinstance(value, list):
            lines.append(f"{key}: [{', '.join(_scalar(v) for v in value)}]")
        else:
            lines.append(f"{key}: {_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def write(path: Path, frontmatter: dict, body: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump(frontmatter, body), encoding="utf-8")


# -------------------------------------------------------------------------- paths
def rel(path: Path) -> str:
    """Bundle-relative path with forward slashes, for example 'concepts/rag.md'."""
    return Path(path).resolve().relative_to(VAULT_DIR).as_posix()


def resolve(ref: str) -> Path:
    """Accept 'concepts/rag', 'concepts/rag.md' or '/concepts/rag.md'. Stays inside the vault."""
    clean = str(ref).strip().lstrip("/")
    if not clean.endswith(".md"):
        clean += ".md"
    target = (VAULT_DIR / clean).resolve()
    if VAULT_DIR not in target.parents:
        raise ValueError(f"path escapes the vault: {ref}")
    return target


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return slug[:60].strip("-") or "untitled"


def concept_files() -> list[Path]:
    return sorted(p for p in VAULT_DIR.rglob("*.md") if p.name not in RESERVED)


# -------------------------------------------------------------- trust and lifecycle
def verifications(fm: dict) -> list[dict]:
    """`verified` may be a list or one bare mapping; consumers MUST accept both (5.2)."""
    raw = fm.get("verified")
    if not raw:
        return []
    if isinstance(raw, dict):
        return [raw]
    return [v for v in raw if isinstance(v, dict)]


def trust_tier(fm: dict) -> str:
    """Derive the trust tier from `verified` (spec section 5.3)."""
    events = verifications(fm)
    if not events:
        return "unverified"
    if any(str(v.get("by", "")).startswith("human:") for v in events):
        return "human-reviewed"
    return "machine-confirmed"


def status(fm: dict) -> str:
    return str(fm.get("status") or "stable")


def is_stale(fm: dict, at: dt.datetime | None = None) -> bool:
    limit = parse_time(fm.get("stale_after"))
    return bool(limit) and (at or now()) >= limit


# -------------------------------------------------------------------------- links
def links_in(body: str, source_rel: str) -> list[str]:
    """Bundle-relative targets of every markdown link to a .md file in a body."""
    base = Path(source_rel).parent
    found = []
    for _, target in _LINK_RE.findall(body):
        if re.match(r"^[a-z]+://", target):
            continue
        if target.startswith("/"):
            resolved = target.lstrip("/")
        else:
            resolved = os.path.normpath((base / target).as_posix()).replace(os.sep, "/")
        if resolved not in found:
            found.append(resolved)
    return found


def graph() -> dict:
    """Build the knowledge graph: concepts, sources, tags, and not-yet-written gaps."""
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    parsed = {}
    for path in concept_files():
        fm, body = parse(path)
        rid = rel(path)
        parsed[rid] = (fm, body)
        nodes[rid] = {
            "id": rid,
            "kind": "concept",
            "title": fm.get("title") or path.stem.replace("-", " ").title(),
            "type": fm.get("type") or "Unknown",
            "description": fm.get("description") or "",
            "status": status(fm),
            "trust": trust_tier(fm),
            "stale": is_stale(fm),
            "tags": [str(t) for t in (fm.get("tags") or [])],
            "generated_by": (fm.get("generated") or {}).get("by", "") if isinstance(fm.get("generated"), dict) else "",
        }

    def ensure(target: str) -> None:
        if target not in nodes:
            nodes[target] = {
                "id": target, "kind": "gap", "type": "Not yet written",
                "title": Path(target).stem.replace("-", " ").title(),
                "description": "Linked from the bundle but not written yet.",
                "status": "missing", "trust": "none", "stale": False, "tags": [],
            }

    seen = set()
    for rid, (fm, body) in parsed.items():
        for target in links_in(body, rid):
            if target == rid or Path(target).name in RESERVED:
                continue
            ensure(target)
            if (rid, target) not in seen:
                seen.add((rid, target))
                edges.append({"source": rid, "target": target, "kind": "link"})
        for src in fm.get("sources") or []:
            res = str((src or {}).get("resource", ""))
            if res.endswith(".md") and not re.match(r"^[a-z]+://", res):
                target = res.lstrip("/") if res.startswith("/") else os.path.normpath(
                    (Path(rid).parent / res).as_posix()).replace(os.sep, "/")
                ensure(target)
                if (rid, target) not in seen:
                    seen.add((rid, target))
                    edges.append({"source": rid, "target": target, "kind": "source"})
        for tag in nodes[rid]["tags"]:
            tid = f"tag:{tag}"
            nodes.setdefault(tid, {"id": tid, "kind": "tag", "title": f"#{tag}", "type": "Tag",
                                   "description": "", "status": "", "trust": "none",
                                   "stale": False, "tags": []})
            edges.append({"source": rid, "target": tid, "kind": "tag"})
    return {"nodes": list(nodes.values()), "edges": edges, "generated_at": iso(now())}


# ------------------------------------------------------------------ index and log
def rebuild_indexes() -> None:
    """Regenerate every index.md from frontmatter (spec section 8). Deterministic."""
    folders = sorted({p.parent for p in concept_files()} | {VAULT_DIR})
    for folder in folders:
        lines: list[str] = []
        if folder == VAULT_DIR:
            lines += ["---", f'okf_version: "{OKF_VERSION}"', "---", ""]
        files = sorted(p for p in folder.glob("*.md") if p.name not in RESERVED)
        subdirs = sorted(d for d in folder.iterdir() if d.is_dir() and any(d.rglob("*.md")))
        if subdirs:
            lines.append("# Subdirectories\n")
            for sub in subdirs:
                blurb = FOLDER_BLURBS.get(sub.name, f"Concepts filed under {sub.name}.")
                lines.append(f"* [{sub.name}]({sub.name}/index.md) - {blurb}")
            lines.append("")
        if files:
            lines.append(f"# {folder.name.replace('-', ' ').title() if folder != VAULT_DIR else 'Concepts'}\n")
            for path in files:
                fm, _ = parse(path)
                title = fm.get("title") or path.stem
                desc = fm.get("description") or ""
                flags = []
                if status(fm) != "stable":
                    flags.append(status(fm))
                if is_stale(fm):
                    flags.append("stale")
                suffix = f" ({', '.join(flags)})" if flags else ""
                lines.append(f"* [{title}]({path.name}) - {desc}{suffix}")
            lines.append("")
        (folder / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def log(kind: str, message: str) -> None:
    """Prepend an entry to the bundle-root log.md, grouped by date, newest first (section 9)."""
    path = VAULT_DIR / "log.md"
    today = now().strftime("%Y-%m-%d")
    entry = f"* **{kind}**: {message}"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Second Brain Update Log\n"
    head, _, rest = text.partition("\n## ")
    if rest.startswith(today):
        day, sep, older = rest.partition("\n## ")
        day_lines = day.split("\n")
        day_lines.insert(1, entry)
        rest = "\n".join(day_lines) + (sep + older if sep else "")
        text = head.rstrip() + "\n\n## " + rest
    else:
        text = head.rstrip() + f"\n\n## {today}\n{entry}\n" + (f"\n## {rest}" if rest else "")
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


# --------------------------------------------------------------------- conformance
def validate() -> dict:
    """Check the bundle against OKF v0.2 conformance (spec section 11)."""
    errors, warnings = [], []
    for path in concept_files():
        rid = rel(path)
        text = path.read_text(encoding="utf-8")
        if not _FM_RE.match(text):
            errors.append(f"{rid}: no parseable YAML frontmatter block")
            continue
        fm, _ = parse_text(text)
        if not str(fm.get("type") or "").strip():
            errors.append(f"{rid}: missing required `type`")
        gen = fm.get("generated")
        if gen is not None and not (isinstance(gen, dict) and gen.get("by")):
            warnings.append(f"{rid}: `generated` should be {{ by, at }} with a `by` actor")
        stamps = [fm.get("stale_after")]
        if isinstance(gen, dict):
            stamps.append(gen.get("at"))
        stamps += [v.get("at") for v in verifications(fm)]
        for stamp in stamps:
            if stamp not in (None, "") and not (isinstance(stamp, dt.datetime) and stamp.tzinfo):
                warnings.append(f"{rid}: timestamp `{stamp}` is not an ISO 8601 datetime with an offset")
        if fm.get("status") not in (None, "draft", "stable", "deprecated"):
            warnings.append(f"{rid}: unknown status `{fm.get('status')}`")
        for src in fm.get("sources") or []:
            if not (isinstance(src, dict) and src.get("resource")):
                warnings.append(f"{rid}: a `sources` entry is missing `resource`")
    for path in VAULT_DIR.rglob("index.md"):
        fm, _ = parse(path)
        if fm and not (path.parent == VAULT_DIR and set(fm) == {"okf_version"}):
            errors.append(f"{rel(path)}: index files carry no frontmatter (only okf_version at the root)")
    for path in VAULT_DIR.rglob("log.md"):
        for heading in re.findall(r"^## (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE):
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", heading.strip()):
                errors.append(f"{rel(path)}: log date heading `{heading}` is not YYYY-MM-DD")
    return {"conformant": not errors, "okf_version": OKF_VERSION, "concepts": len(concept_files()),
            "errors": errors, "warnings": warnings}
