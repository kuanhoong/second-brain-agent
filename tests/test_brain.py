"""Offline tests: the OKF layer and the tools, no API key needed."""
import datetime as dt
import shutil
from pathlib import Path

import pytest

from second_brain import okf, tools

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def vault(tmp_path, monkeypatch):
    target = tmp_path / "vault"
    shutil.copytree(ROOT / "vault", target)
    monkeypatch.setattr(okf, "VAULT_DIR", target.resolve())
    return target


def test_seed_vault_is_conformant(vault):
    report = okf.validate()
    assert report["conformant"], report["errors"]
    assert report["warnings"] == []


def test_trust_tiers_follow_spec_5_3():
    assert okf.trust_tier({}) == "unverified"
    assert okf.trust_tier({"verified": {"by": "process:nightly", "at": "2026-01-01T00:00:00Z"}}) == "machine-confirmed"
    assert okf.trust_tier({"verified": [{"by": "fact-checker/x"}, {"by": "human:me"}]}) == "human-reviewed"


def test_absent_status_is_stable_and_staleness_is_a_plain_comparison():
    assert okf.status({}) == "stable"
    assert okf.is_stale({"stale_after": "2026-01-01T00:00:00Z"}, dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc))
    assert not okf.is_stale({"stale_after": "2026-01-01T00:00:00Z"}, dt.datetime(2025, 12, 31, tzinfo=dt.timezone.utc))
    assert not okf.is_stale({})


def test_review_finds_gaps_stale_and_deprecated(vault):
    review = tools.review_brain()
    assert {g["path"] for g in review["gaps"]} == {"concepts/model-context-protocol.md", "concepts/vector-embeddings.md"}
    assert review["stale"] == ["concepts/gemini-models.md"]
    assert review["deprecated"] == ["concepts/okf-change-tracking-v0-1.md"]
    assert review["awaiting_human"] == ["concepts/knowledge-graph.md"]


def test_capture_writes_valid_okf_and_fills_the_gap(vault):
    src = tools.save_source("https://modelcontextprotocol.io/", "Model Context Protocol documentation",
                            "MCP is an open protocol. It connects models to tools.", author="MCP project")
    again = tools.save_source("https://modelcontextprotocol.io", "Same page", "Duplicate.")
    assert again["already_filed"] and again["source_id"] == src["source_id"]

    out = tools.save_concept(
        title="Model Context Protocol", description="An open protocol for connecting models to tools.",
        summary="MCP standardises tool access. The Agent Development Kit can load MCP tools.",
        key_points=["- Uses JSON-RPC 2.0.", "Servers expose tools, resources and prompts."],
        tags=["MCP", "Agents", "Open Standard"], source_ids=[src["source_id"]],
        related=["Open Knowledge Format", "A2A Protocol"])
    assert out["path"] == "concepts/model-context-protocol.md"
    assert out["tags"] == ["mcp", "agents", "open-standard"]
    assert "concepts/open-knowledge-format.md" in out["linked_to"]
    assert "concepts/agent-development-kit.md" in out["linked_to"]      # found by name in the text
    assert out["gaps"] == ["concepts/a2a-protocol.md"]

    fm, body = okf.parse(vault / out["path"])
    assert fm["status"] == "draft" and "verified" not in fm
    assert fm["generated"]["by"].startswith("second-brain/")
    assert isinstance(fm["generated"]["at"], dt.datetime) and fm["generated"]["at"].tzinfo
    assert fm["sources"][0]["resource"] == f"/references/{src['source_id']}.md"
    assert f"[^{src['source_id']}]" in body and "- Uses JSON-RPC 2.0." in body
    assert okf.validate()["conformant"]
    assert "concepts/model-context-protocol.md" not in {g["path"] for g in tools.review_brain()["gaps"]}
    assert "Model Context Protocol" in (vault / "concepts" / "index.md").read_text()
    assert (vault / "log.md").read_text().split("\n## ")[1].startswith(okf.now().strftime("%Y-%m-%d"))


def test_trust_ladder_unverified_machine_human(vault):
    out = tools.save_concept("Vector Embeddings", "Meaning as coordinates.", "Text becomes vectors.",
                             ["Close vectors mean similar text."], ["llm", "retrieval"], [])
    path = out["path"]
    assert tools.read_concept(path)["trust"] == "unverified"
    assert tools.record_check(path, False, "One claim unsupported.")["trust"] == "unverified"
    checked = tools.record_check(path, True, "All points supported.")
    assert checked["trust"] == "machine-confirmed" and checked["status"] == "draft"
    verified = tools.verify_concept(path)
    assert verified == {"path": path, "status": "stable", "trust": "human-reviewed", "verified_by": tools.HUMAN_ACTOR}
    assert [v["by"] for v in tools.read_concept(path)["verified"]] == [tools.CHECKER_ACTOR, tools.HUMAN_ACTOR]


def test_agent_cannot_overwrite_fresh_human_reviewed_note_but_can_refresh_a_stale_one(vault):
    blocked = tools.save_concept("Open Knowledge Format", "x", "y", ["z"], ["okf"], [])
    assert "error" in blocked
    refreshed = tools.save_concept("Gemini Models", "Current model IDs.", "Use the current Flash model.",
                                   ["Pin the ID."], ["gemini", "models"], [], shelf_life_days=30)
    assert refreshed["replaced"] == "human-reviewed" and refreshed["trust"] == "unverified"
    assert tools.review_brain()["stale"] == []


def test_search_ranks_and_reports_trust(vault):
    hits = tools.search_brain("okf trust signals")
    assert hits[0]["path"] == "concepts/okf-trust-signals.md"
    assert any(h["status"] == "deprecated" for h in tools.search_brain("okf timestamp citations"))


def test_graph_has_gap_and_tag_nodes(vault):
    g = okf.graph()
    kinds = {n["id"]: n["kind"] for n in g["nodes"]}
    assert kinds["concepts/vector-embeddings.md"] == "gap" and kinds["tag:okf"] == "tag"
    assert {"source": "concepts/open-knowledge-format.md", "target": "references/okf-spec.md", "kind": "source"} in g["edges"]


def test_paths_cannot_escape_the_vault(vault):
    with pytest.raises(ValueError):
        okf.resolve("../../etc/passwd")
    assert "error" in tools.read_concept("../../etc/passwd")


# ----------------------------------------------------------- Chrome extension capture
def test_highlight_is_filed_verbatim_before_any_model_runs(vault):
    from second_brain import capture

    src = capture.file_highlight("https://example.com/post", "A post", "First line.\nSecond line.")
    fm, body = okf.parse(vault / src["path"])
    assert fm["type"] == "Reference" and fm["resource"] == "https://example.com/post"
    assert fm["generated"]["by"] == "process:chrome-extension"      # code wrote it, not a model
    assert "# Highlights" in body and "> First line.\n> Second line." in body
    again = capture.file_highlight("https://example.com/post", "A post", "Another passage.")
    assert again["already_filed"] and again["path"] == src["path"]
    _, body = okf.parse(vault / src["path"])
    assert "> First line." in body and "> Another passage." in body and body.count("# Highlights") == 1
    assert okf.validate()["conformant"]
    for bad in [("https://example.com", "t", "  "), ("file:///etc/passwd", "t", "x"), ("javascript:alert(1)", "t", "x")]:
        with pytest.raises(ValueError):
            capture.file_highlight(*bad)


def test_capture_job_summarises_or_keeps_the_highlight(vault):
    import time

    from second_brain import capture

    async def good(url, title, text, source_id):
        return tools.save_concept("Captured Idea", "An idea.", "Summary.", ["Point."], ["agents"], [source_id])

    async def broken(url, title, text, source_id):
        raise RuntimeError("no API key")

    def finish(job):
        for _ in range(100):
            if job["state"] != "summarising":
                return job
            time.sleep(0.05)
        raise AssertionError("job did not finish")

    ok = finish(capture.start("https://example.com/a", "Page A", "Some passage.", summarise=good))
    assert ok["state"] == "done" and ok["concept"] == "concepts/captured-idea.md" and ok["tags"] == ["agents"]
    fm, _ = okf.parse(vault / ok["concept"])
    assert fm["status"] == "draft" and fm["sources"][0]["resource"] == f"/{ok['source']}"

    kept = finish(capture.start("https://example.com/b", "Page B", "Another passage.", summarise=broken))
    assert kept["state"] == "saved_only" and "no API key" in kept["error"]
    assert (vault / kept["source"]).exists()


def test_only_the_extension_may_post_captures():
    from second_brain import capture

    assert capture.allowed_origin("chrome-extension://abcdefghijklmnop")
    for origin in (None, "", "https://evil.example", "http://localhost:8765", "null"):
        assert not capture.allowed_origin(origin)


def test_ai_micro_drama_bundle_is_conformant_and_fully_sourced(monkeypatch):
    bundle = ROOT / "brains" / "ai-micro-drama"
    monkeypatch.setattr(okf, "VAULT_DIR", bundle.resolve())
    report = okf.validate()
    assert report["conformant"] and report["warnings"] == [], report
    review = tools.review_brain()
    assert review["orphans"] == []
    for path in okf.concept_files():
        fm, body = okf.parse(path)
        ids = {s["id"] for s in fm.get("sources") or []}
        cited = set(__import__("re").findall(r"\[\^([a-z0-9-]+)\]", body))
        assert cited == ids, f"{okf.rel(path)}: footnotes and sources disagree"
        for s in fm.get("sources") or []:
            res = s["resource"]
            assert res.startswith("https://") or (bundle / res.lstrip("/")).exists(), f"{okf.rel(path)}: {res}"
