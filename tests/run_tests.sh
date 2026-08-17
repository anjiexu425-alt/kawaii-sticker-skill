#!/usr/bin/env bash
# Kawaii Sticker Skill — test entry point (SPEC M8, CI: .github/workflows/ci.yml)
#
# Runs both validators from the repo root, prints a summary, and exits
# non-zero when any validator fails.
set -euo pipefail

# Repo root = parent directory of this script.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Kawaii Sticker Skill — test suite =="
echo "repo root: $ROOT"

fail=0

echo
echo "--- [1/2] validate_structure.py (SPEC M1-M4) ---"
if python3 tests/validate_structure.py; then
  echo ">> structure: OK"
else
  echo ">> structure: FAILED"
  fail=1
fi

echo
echo "--- [2/2] validate_examples.py (SPEC M5-M6) ---"
if python3 tests/validate_examples.py; then
  echo ">> examples: OK"
else
  echo ">> examples: FAILED"
  fail=1
fi

echo
echo "=================================================="
if [ "$fail" -eq 0 ]; then
  echo "ALL TESTS PASSED"
else
  echo "SOME TESTS FAILED"
fi
echo "=================================================="

exit "$fail"
