#!/usr/bin/env bash
# Restore the vault to its committed state between demo runs.
set -euo pipefail
cd "$(dirname "$0")"
git checkout -- vault
git clean -fdq vault
echo "Vault reset. $(find vault -name '*.md' | wc -l | tr -d ' ') markdown files."
