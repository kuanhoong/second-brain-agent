#!/usr/bin/env bash
# Restore the vault to its committed state between demo runs (agents write to it).
set -e
git checkout -- my-second-brain 2>/dev/null || echo "No git checkout (not a repo yet?)"
git clean -fdq my-second-brain 2>/dev/null || true
python build_viz.py
echo "Vault reset. viz.html rebuilt."
