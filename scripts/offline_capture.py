"""Replay a canned capture through the real tools. The stage fallback for dead Wi-Fi.

    python scripts/offline_capture.py model-context-protocol
    python scripts/offline_capture.py gemini-models
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from second_brain import tools  # noqa: E402

name = sys.argv[1] if len(sys.argv) > 1 else "model-context-protocol"
payload = json.loads((ROOT / "demo_backup" / f"{name}.json").read_text(encoding="utf-8"))
ids = [tools.save_source(**src)["source_id"] for src in payload["sources"]]
print(json.dumps(tools.save_concept(source_ids=ids, **payload["concept"]), indent=2))
