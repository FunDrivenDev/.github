# The only entry point for checking this repo.
#
# A scope picks the files a recipe looks at:
#   all      every tracked and untracked file (the default)
#   changed  files that differ from origin/main, committed or not
#   staged   files in the git index

set shell := ["bash", "-euo", "pipefail", "-c"]

# List the recipes.
default:
    @just --list --unsorted

# Once per clone: install the pinned tools and the git hooks.
init:
    mise install
    hk install

# Format the Markdown files in scope.
fmt scope="all":
    @files=$(just _files {{ quote(scope) }} '\.md$'); [ -z "$files" ] || rumdl fmt $files

# Lint the files in scope: Markdown, spelling, and every SVG must parse.
lint scope="all":
    #!/usr/bin/env bash
    set -euo pipefail
    md=$(just _files {{ quote(scope) }} '\.md$')
    svg=$(just _files {{ quote(scope) }} '\.svg$')
    all=$(just _files {{ quote(scope) }} '.')
    [ -z "$md" ] || rumdl check $md
    [ -z "$all" ] || typos $all
    [ -z "$svg" ] || xmllint --noout $svg

# Lint everything that differs from main, or the whole repo.
check scope="all": (lint scope)

# Audit for secrets and personal data in the whole history.
audit:
    gitleaks git --config .gitleaks.toml --redact --no-banner --log-level warn .

# The existing files of a scope matching a pattern, one per line.
_files scope pattern:
    #!/usr/bin/env bash
    set -euo pipefail
    case {{ quote(scope) }} in
      all) git ls-files --cached --others --exclude-standard ;;
      changed) { git diff --name-only origin/main...HEAD 2>/dev/null || true; git diff --name-only HEAD; git ls-files --others --exclude-standard; } ;;
      staged) git diff --cached --name-only --diff-filter=ACMR ;;
      *) echo "unknown scope: {{ scope }}" >&2; exit 2 ;;
    esac | sort -u | grep -E {{ quote(pattern) }} | while read -r f; do [ -f "$f" ] && echo "$f"; done || true
