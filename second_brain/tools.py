"""Function tools the agents use to read and maintain the OKF bundle.

ADK turns each function into a tool and shows the model its docstring, so the
docstrings are written for the model. Every tool is deterministic file work:
the model decides WHAT to save, these functions decide HOW it lands on disk,
so the frontmatter is always valid OKF v0.2 no matter what the model does.
"""
from __future__ import annotations

import datetime as dt
import re
from collections import Counter
from pathlib import Path

from . import okf
from .config import MODEL, OWNER

AGENT_ACTOR = f"second-brain/{MODEL}"
CHECKER_ACTOR = f"fact-checker/{MODEL}"
HUMAN_ACTOR = f"human:{OWNER}"

_STOP = set("a an and are as at be by for from how in is it of on or that the this to what when "
            "which who why with you your my me do does about into".split())


# ----------------------------------------------------------------------- helpers
def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9][a-z0-9.+-]*", str(text).lower()) if t not in _STOP and len(t) > 1]


def _all() -> list[tuple[str, dict, str]]:
    return [(okf.rel(p), *okf.parse(p)) for p in okf.concept_files()]


def _vocabulary() -> Counter:
    counts: Counter = Counter()
    for _, fm, _ in _all():
        counts.update(str(t) for t in (fm.get("tags") or []))
    return counts


def _normalise_tags(tags: list[str]) -> list[str]:
    """Lowercase, hyphenate, and snap to tags that already exist (llms -> llm)."""
    known = set(_vocabulary())
    out: list[str] = []
    for raw in tags or []:
        tag = okf.slugify(raw)
        if not tag or tag == "untitled":
            continue
        for variant in (tag, tag.rstrip("s"), tag + "s", tag.replace("-", "")):
            if variant in known:
                tag = variant
                break
        if tag not in out:
            out.append(tag)
    return out[:6]


def _card(rid: str, fm: dict) -> dict:
    return {
        "path": rid,
        "title": fm.get("title") or Path(rid).stem,
        "type": fm.get("type") or "Unknown",
        "description": fm.get("description") or "",
        "status": okf.status(fm),
        "trust": okf.trust_tier(fm),
        "stale": okf.is_stale(fm),
        "tags": [str(t) for t in (fm.get("tags") or [])],
    }


def _find(ref: str) -> str | None:
    """Resolve a path, a slug or a title to an existing bundle-relative path."""
    ref = str(ref).strip()
    if not ref:
        return None
    try:
        target = okf.resolve(ref)
        if target.exists():
            return okf.rel(target)
    except ValueError:
        return None
    wanted = okf.slugify(Path(ref).stem if ref.endswith(".md") else ref)
    for rid, fm, _ in _all():
        if Path(rid).stem == wanted or okf.slugify(fm.get("title", "")) == wanted:
            return rid
    return None


# ------------------------------------------------------------------------- read
def brain_overview() -> dict:
    """Get the map of the second brain. ALWAYS call this first (progressive disclosure).

    Returns the folders, every concept as a one-line card (path, title, description,
    status, trust tier, stale flag, tags), and the existing tag vocabulary with counts.
    Reuse existing tags when you save something new.
    """
    cards = [_card(rid, fm) for rid, fm, _ in _all()]
    return {
        "okf_version": okf.OKF_VERSION,
        "folders": sorted({Path(c["path"]).parent.as_posix() for c in cards}),
        "concepts": cards,
        "tag_vocabulary": dict(_vocabulary().most_common()),
        "trust_tiers": dict(Counter(c["trust"] for c in cards)),
    }


def search_brain(query: str) -> list[dict]:
    """Search the second brain by keywords. Matches titles, tags, descriptions and bodies.

    Args:
        query: A few keywords, for example "okf trust signals".
    Returns:
        Up to 8 concept cards, best match first, each with a short snippet.
    """
    terms = _tokens(query)
    hits = []
    for rid, fm, body in _all():
        title = str(fm.get("title", "")).lower()
        tags = " ".join(str(t) for t in (fm.get("tags") or [])).lower()
        desc = str(fm.get("description", "")).lower()
        text = body.lower()
        score = sum(6 * (t in title) + 4 * (t in tags) + 3 * (t in desc) + min(text.count(t), 3) for t in terms)
        if score:
            pos = min([text.find(t) for t in terms if t in text] or [0])
            card = _card(rid, fm)
            card["snippet"] = re.sub(r"\s+", " ", body[max(0, pos - 60): pos + 200]).strip()
            hits.append((score, card))
    return [card for _, card in sorted(hits, key=lambda h: -h[0])[:8]]


def read_concept(path: str) -> dict:
    """Open one concept. Use the path from brain_overview or search_brain.

    Returns the frontmatter trust fields and the full markdown body. Check `status`,
    `trust` and `stale` before you rely on the content: never answer from a
    `deprecated` concept, and say so when a concept is a draft, unverified or stale.
    """
    rid = _find(path)
    if not rid:
        return {"error": f"No concept found for '{path}'. It may not be written yet."}
    fm, body = okf.parse(okf.resolve(rid))
    card = _card(rid, fm)
    card.update({
        "generated": {k: okf.iso(v) if k == "at" else v for k, v in (fm.get("generated") or {}).items()},
        "verified": [{"by": v.get("by"), "at": okf.iso(v.get("at"))} for v in okf.verifications(fm)],
        "stale_after": okf.iso(fm.get("stale_after")),
        "sources": fm.get("sources") or [],
        "resource": fm.get("resource") or "",
        "superseded_by": fm.get("superseded_by") or "",
        "body": body,
    })
    return card


# ------------------------------------------------------------------------ write
def save_source(url: str, title: str, summary: str, author: str = "", last_modified: str = "", highlight: str = "") -> dict:
    """File one web page as a Reference concept, so later claims can cite it.

    Call this once per web source BEFORE save_concept, then pass the returned
    `source_id` values to save_concept.

    Args:
        url: The page's full URL.
        title: The page title.
        summary: Two to four sentences, in your own words, on what the page says.
        author: Publisher or author if known, for example "Google Cloud".
        last_modified: The page's publication or update date if known (YYYY-MM-DD).
        highlight: Exact text the user highlighted on the page, if any. Kept verbatim.
    Returns:
        {source_id, path}. If the URL was already filed, returns the existing one.
    """
    return _file_source(url, title, summary, author, last_modified, highlight, AGENT_ACTOR)


def _file_source(url: str, title: str, summary: str, author: str, last_modified: str, highlight: str, actor: str) -> dict:
    """Shared by save_source (the agent) and the Chrome extension capture (plain code)."""
    url = url.strip()
    quote = "\n".join(f"> {line}" for line in highlight.strip().splitlines() if line.strip())
    for rid, fm, body in _all():
        if fm.get("type") == "Reference" and str(fm.get("resource", "")).rstrip("/") == url.rstrip("/"):
            if quote and quote not in body:
                head, sep, notes = body.partition("\n[^")
                if "# Highlights" not in head:
                    head = head.rstrip() + "\n\n# Highlights"
                okf.write(okf.resolve(rid), fm, head.rstrip() + "\n\n" + quote + "\n" + (sep + notes if sep else ""))
                okf.log("Update", f"Added a highlight to [{fm.get('title', rid)}](/{rid}).")
            return {"source_id": Path(rid).stem, "path": rid, "already_filed": True}
    slug = okf.slugify(title)
    target = okf.resolve(f"references/{slug}")
    if target.exists():
        slug = f"{slug}-{okf.now().strftime('%H%M%S')}"
        target = okf.resolve(f"references/{slug}")
    source = {"id": slug, "resource": url, "title": title}
    if author:
        source["author"] = author
    stamp = okf.parse_time(last_modified)
    if stamp:
        source["last_modified"] = okf.iso(stamp)
    fm = {
        "type": "Reference",
        "title": title,
        "description": re.sub(r"\s+", " ", summary).strip().split(". ")[0].rstrip(".") + ".",
        "resource": url,
        "tags": ["source"],
        "status": "stable",
        "generated": {"by": actor, "at": okf.iso(okf.now())},
        "sources": [source],
    }
    body = f"# Summary\n\n{summary.strip()}[^{slug}]\n\n"
    if quote:
        body += f"# Highlights\n\n{quote}\n\n"
    body += f"[^{slug}]: {title}"
    okf.write(target, fm, body)
    okf.rebuild_indexes()
    okf.log("Creation", f"Filed source [{title}](/references/{slug}.md).")
    return {"source_id": slug, "path": okf.rel(target), "already_filed": False}


def save_concept(
    title: str,
    description: str,
    summary: str,
    key_points: list[str],
    tags: list[str],
    source_ids: list[str],
    related: list[str] = [],
    shelf_life_days: int = 90,
) -> dict:
    """Write one atomic concept into the second brain as valid OKF v0.2.

    The tool, not you, sets the trust fields: status is `draft`, `generated` records
    this agent, and there is no `verified` entry until a check or a human adds one.
    It also links the concept into the graph automatically.

    Args:
        title: Short noun phrase, for example "Model Context Protocol".
        description: ONE sentence. Shown in indexes and search results.
        summary: Three to five sentences in your own words.
        key_points: Three to six short factual bullets. No markdown bullets, plain text.
        tags: Two to five lowercase tags. Prefer tags from brain_overview's vocabulary.
        source_ids: The `source_id` values returned by save_source for the pages used.
        related: Paths or titles of existing concepts this one relates to. Titles of
            concepts that do not exist yet are fine: they show up as gaps in the graph.
        shelf_life_days: Days until the content should be re-checked. Use 30 for
            fast-moving topics (model versions, prices), 180 for stable ideas.
    Returns:
        {path, tags, linked_to, gaps, replaced}
    """
    slug = okf.slugify(title)
    target = okf.resolve(f"concepts/{slug}")
    rid = f"concepts/{slug}.md"
    tags = _normalise_tags(tags)
    replaced = None
    if target.exists():
        old_fm, _ = okf.parse(target)
        if okf.trust_tier(old_fm) == "human-reviewed" and not okf.is_stale(old_fm) and okf.status(old_fm) == "stable":
            return {"error": f"{rid} is human-reviewed and still fresh. I will not overwrite it. "
                             "Pick a more specific title, or ask the human to deprecate it first."}
        replaced = okf.trust_tier(old_fm)

    sources = []
    for sid in source_ids or []:
        ref = _find(f"references/{okf.slugify(sid)}") or _find(sid)
        if not ref:
            continue
        ref_fm, _ = okf.parse(okf.resolve(ref))
        entry = {"id": Path(ref).stem, "resource": f"/{ref}", "title": ref_fm.get("title", Path(ref).stem)}
        if entry not in sources:
            sources.append(entry)

    # Automatic linking: what the model asked for, plus concepts that share two or
    # more tags or are mentioned by name in the text.
    text = f"{summary} {' '.join(key_points or [])}".lower()
    linked, gaps = [], []
    for ref in related or []:
        found = _find(ref)
        if found and found != rid and found not in linked:
            linked.append(found)
        elif not found:
            gap = f"concepts/{okf.slugify(Path(str(ref)).stem)}.md"
            if gap != rid and gap not in gaps:
                gaps.append(gap)
    for other, fm, _ in _all():
        if other == rid or other in linked or fm.get("type") == "Reference":
            continue
        if okf.status(fm) == "deprecated":
            continue
        shared = set(tags) & {str(t) for t in (fm.get("tags") or [])}
        name = str(fm.get("title", "")).lower()
        if len(shared) >= 2 or (len(name) > 3 and re.search(rf"\b{re.escape(name)}\b", text)):
            linked.append(other)

    cite = "".join(f"[^{s['id']}]" for s in sources)
    lines = ["# Summary", "", summary.strip() + cite, "", "# Key points", ""]
    for point in key_points or []:
        point = re.sub(r"^[-*•]\s*", "", str(point).strip())
        if point:
            lines.append(f"- {point}{cite}")
    if linked or gaps:
        lines += ["", "# Related", ""]
        for other in linked:
            fm, _ = okf.parse(okf.resolve(other))
            lines.append(f"- [{fm.get('title', Path(other).stem)}](/{other})")
        for gap in gaps:
            lines.append(f"- [{Path(gap).stem.replace('-', ' ').title()}](/{gap})")
    if sources:
        lines.append("")
        lines += [f"[^{s['id']}]: {s['title']}" for s in sources]

    stamp = okf.now()
    fm = {
        "type": "Concept",
        "title": title.strip(),
        "description": re.sub(r"\s+", " ", description).strip(),
        "tags": tags,
        "status": "draft",
        "generated": {"by": AGENT_ACTOR, "at": okf.iso(stamp)},
        "stale_after": okf.iso(stamp + dt.timedelta(days=max(1, int(shelf_life_days)))),
        "sources": sources,
    }
    okf.write(target, fm, "\n".join(lines))
    okf.rebuild_indexes()
    okf.log("Update" if replaced else "Creation",
            f"{'Rewrote' if replaced else 'Added'} [{title.strip()}](/{rid}) as a draft from {len(sources)} source(s).")
    return {"path": rid, "tags": tags, "linked_to": linked, "gaps": gaps, "replaced": replaced,
            "status": "draft", "trust": "unverified"}


# ------------------------------------------------------------------------ trust
def record_check(path: str, passed: bool, notes: str) -> dict:
    """Record the result of a machine fact-check against a concept's sources.

    Call this ONLY after the fact_checker tool has re-read the sources. When
    `passed` is true the concept gains a machine `verified` entry and its trust tier
    becomes machine-confirmed. It stays a draft: only a human can make it stable.

    Args:
        path: The concept's path.
        passed: True only if every key point is supported by the sources.
        notes: One or two sentences on what was checked or what failed.
    """
    rid = _find(path)
    if not rid:
        return {"error": f"No concept found for '{path}'."}
    fm, body = okf.parse(okf.resolve(rid))
    if not passed:
        okf.log("Check failed", f"[{fm.get('title', rid)}](/{rid}): {notes.strip()}")
        return {"path": rid, "trust": okf.trust_tier(fm), "passed": False, "notes": notes}
    events = okf.verifications(fm) + [{"by": CHECKER_ACTOR, "at": okf.iso(okf.now())}]
    fm["verified"] = events
    okf.write(okf.resolve(rid), fm, body)
    okf.rebuild_indexes()
    okf.log("Verification", f"Machine check passed for [{fm.get('title', rid)}](/{rid}). {notes.strip()}")
    return {"path": rid, "trust": okf.trust_tier(fm), "passed": True, "status": okf.status(fm)}


def verify_concept(path: str) -> dict:
    """Record that the HUMAN owner has reviewed a concept and promote it to stable.

    This asks the human for confirmation. Call it only when the human says they
    have read and approved the concept. Never call it on your own initiative.
    """
    rid = _find(path)
    if not rid:
        return {"error": f"No concept found for '{path}'."}
    fm, body = okf.parse(okf.resolve(rid))
    fm["status"] = "stable"
    fm["verified"] = okf.verifications(fm) + [{"by": HUMAN_ACTOR, "at": okf.iso(okf.now())}]
    okf.write(okf.resolve(rid), fm, body)
    okf.rebuild_indexes()
    okf.log("Verification", f"{HUMAN_ACTOR} reviewed [{fm.get('title', rid)}](/{rid}). Now stable.")
    return {"path": rid, "status": "stable", "trust": okf.trust_tier(fm), "verified_by": HUMAN_ACTOR}


def deprecate_concept(path: str, superseded_by: str = "") -> dict:
    """Mark a concept as deprecated (kept for links and history, never answered from).

    This asks the human for confirmation.

    Args:
        path: The concept to deprecate.
        superseded_by: Optional path of the concept that replaces it.
    """
    rid = _find(path)
    if not rid:
        return {"error": f"No concept found for '{path}'."}
    fm, body = okf.parse(okf.resolve(rid))
    fm["status"] = "deprecated"
    newer = _find(superseded_by) if superseded_by else None
    if newer:
        fm["superseded_by"] = f"/{newer}"
    okf.write(okf.resolve(rid), fm, body)
    okf.rebuild_indexes()
    okf.log("Deprecation", f"Deprecated [{fm.get('title', rid)}](/{rid})" + (f" in favour of /{newer}." if newer else "."))
    return {"path": rid, "status": "deprecated", "superseded_by": newer or ""}


# ----------------------------------------------------------------------- review
def review_brain() -> dict:
    """Health-check the second brain and find what to learn or fix next.

    Returns:
        conformance: OKF v0.2 conformance result.
        gaps: concepts that are linked to but not written yet. Good research topics.
        stale: concepts past their `stale_after` instant. They need a refresh.
        unverified: drafts no machine or human has confirmed.
        awaiting_human: machine-confirmed concepts waiting for a human review.
        deprecated: superseded concepts.
        thin_tags: tags used by only one concept. Areas the brain barely covers.
        orphans: concepts nothing links to.
    """
    g = okf.graph()
    by_id = {n["id"]: n for n in g["nodes"]}
    inbound: Counter = Counter(e["target"] for e in g["edges"] if e["kind"] != "tag")
    wanted_by: dict[str, list[str]] = {}
    for e in g["edges"]:
        if by_id[e["target"]]["kind"] == "gap":
            wanted_by.setdefault(e["target"], []).append(e["source"])
    concepts = [n for n in g["nodes"] if n["kind"] == "concept"]
    notes = [n for n in concepts if n["type"] != "Reference"]
    tag_use = Counter(t for n in notes for t in n["tags"])
    return {
        "conformance": okf.validate(),
        "gaps": [{"path": k, "title": by_id[k]["title"], "wanted_by": v} for k, v in wanted_by.items()],
        "stale": [n["id"] for n in notes if n["stale"] and n["status"] != "deprecated"],
        "unverified": [n["id"] for n in notes if n["trust"] == "unverified" and n["status"] != "deprecated"],
        "awaiting_human": [n["id"] for n in notes if n["trust"] == "machine-confirmed"],
        "deprecated": [n["id"] for n in notes if n["status"] == "deprecated"],
        "thin_tags": sorted(t for t, c in tag_use.items() if c == 1),
        "orphans": [n["id"] for n in notes if not inbound[n["id"]]],
    }
