#!/usr/bin/env bash
# Usage: files.sh <scope> <pattern>. The existing files of a scope (all, changed,
# staged) whose path matches the extended regex <pattern>, one per line.
set -euo pipefail

scope=$1
pattern=$2
case "$scope" in
  all | changed | staged) ;;
  *) echo "unknown scope: $scope" >&2; exit 2 ;;
esac

case "$scope" in
  all) git ls-files --cached --others --exclude-standard ;;
  changed) { git diff --name-only origin/main...HEAD 2>/dev/null || true; git diff --name-only HEAD; git ls-files --others --exclude-standard; } ;;
  staged) git diff --cached --name-only --diff-filter=ACMR ;;
esac | sort -u | grep -E "$pattern" | while read -r f; do [ -f "$f" ] && echo "$f"; done || true
