"""Check the vault against OKF v0.2 conformance. Exit code 1 on errors.

    python scripts/validate.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from second_brain import okf  # noqa: E402

report = okf.validate()
print(json.dumps(report, indent=2))
sys.exit(0 if report["conformant"] else 1)
