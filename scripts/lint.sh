#!/usr/bin/env bash
# Usage: lint.sh <scope>. Lints the files in scope without changing them:
# Markdown (rumdl), spelling (typos), and every SVG must parse (xmllint).
set -euo pipefail

scope=$1
mapfile -t md < <(scripts/files.sh "$scope" '\.md$')
mapfile -t svg < <(scripts/files.sh "$scope" '\.svg$')
mapfile -t all < <(scripts/files.sh "$scope" '.')

if (( ${#md[@]} )); then rumdl check "${md[@]}"; fi
if (( ${#all[@]} )); then typos --force-exclude "${all[@]}"; fi
if (( ${#svg[@]} )); then xmllint --noout "${svg[@]}"; fi
