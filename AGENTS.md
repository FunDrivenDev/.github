# FunDrivenDev/.github for agents

## Layout

| Path | Holds |
| --- | --- |
| `profile/README.md` | the README shown on <https://github.com/FunDrivenDev> |
| `assets/` | the images it references (SVG, dark and light variants) |
| `logos/` | the org avatar: `fdd.svg`, and `fdd.png` uploaded by hand |
| `design/images.py` | draws every SVG above; `just images` reruns it and the PNG |
| `.github/workflows/bot-dod.yml` | the reusable workflow that posts `dod` on bot pull requests (Renovate, Dependabot, the tap's casks), called from each repo |

## Writing here

- The profile README renders on github.com: Markdown and GitHub's allowed HTML
  only, no CSS or scripts. Images are local SVGs referenced by relative path,
  with `<picture>` dark and light variants where colors matter.
- An SVG holds no script, external font or external image; its animations
  respect `prefers-reduced-motion`.
- Nothing private: no server names, IPs, personal paths or clients.
- A change to `bot-dod.yml` reaches a repo once its caller's pinned SHA is bumped
  to a commit of `main`.

Checks: just check
