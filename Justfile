# The only entry point for checking this repo.
#
# A scope picks the files a recipe looks at:
#   all      every tracked and untracked file (the default)
#   changed  files that differ from origin/main, committed or not
#   staged   files in the git index

set shell := ["mise", "exec", "--", "bash", "-euo", "pipefail", "-c"]

# List the recipes.
default:
    @just --list --unsorted

# Once per clone: install the pinned tools and the git hooks.
init:
    mise install --locked
    hk install

# Format the Markdown files in scope.
fmt scope="all":
    @files=$(scripts/files.sh {{ quote(scope) }} '\.md$'); [ -z "$files" ] || rumdl fmt $files

# Redraw the banner, start button and avatar from design/images.py, then the avatar PNG.
images:
    python3 design/images.py
    resvg --width 1024 --height 1024 logos/fdd.svg logos/fdd.png

# Lint the files in scope: Markdown, spelling, and every SVG must parse.
lint scope="all":
    scripts/lint.sh {{ quote(scope) }}

# Lint everything that differs from main, or the whole repo.
check scope="all": (lint scope)

# Audit for secrets and personal data in the whole history.
audit:
    gitleaks git --config .gitleaks.toml --redact --no-banner --log-level warn .
