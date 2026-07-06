# Agent Skills

A collection of reusable skills for AI coding agents (Claude Code, Codex, Copilot, etc.). Each skill is a self-contained package that extends an agent's capabilities with specialized workflows, domain knowledge, and bundled resources.

## Skills

### [deck](https://github.com/iuiaoin/agent-skills/tree/main/skills/deck)

HTML presentation deck generator with a strict two-stage workflow:

- **`/deck --plan <prompt>`** — From a basic prompt, run a quick guided Q&A and synthesize a structured deck brief (using your prompt and any materials in `resources/`), confirm it, then expand it into a slide-by-slide outline saved to `PLANNING.md`
- **`/deck --generate`** — Pick a visual theme (10 built-in), then generate standalone HTML slides (1280x720, 16:9) from the approved plan, with a built-in presentation viewer that adopts the same theme — then automatically screenshot every slide and fix any overflow or broken-layout issues before opening

Themes — at the start of generation you choose one of 10 built-in themes; every slide and the viewer adopt its palette, fonts, and decoration. The same deck rendered in each (cover slide):

| | |
|:---:|:---:|
| <img src="docs/themes/claude.png" width="400" alt="claude theme"><br>**`claude`** | <img src="docs/themes/classic.png" width="400" alt="classic theme"><br>**`classic`** |
| <img src="docs/themes/medium.png" width="400" alt="medium theme"><br>**`medium`** | <img src="docs/themes/github.png" width="400" alt="github theme"><br>**`github`** |
| <img src="docs/themes/dark.png" width="400" alt="dark theme"><br>**`dark`** | <img src="docs/themes/google.png" width="400" alt="google theme"><br>**`google`** |
| <img src="docs/themes/microsoft.png" width="400" alt="microsoft theme"><br>**`microsoft`** | <img src="docs/themes/twitter.png" width="400" alt="twitter theme"><br>**`twitter`** |
| <img src="docs/themes/hand-writing.png" width="400" alt="hand-writing theme"><br>**`hand-writing`** · [rough.js](https://github.com/rough-stuff/rough) | <img src="docs/themes/artist.png" width="400" alt="artist theme"><br>**`artist`** |

Bonus:

- **`/deck --qa [--scale N]`** — Re-run the visual QA loop on already-generated slides (screenshot each slide via headless Chromium, detect overflow/layout problems, fix the HTML, re-check until clean) — useful after manual edits
- **`/deck --export pptx [--scale N]`** — Export generated slides to a PPTX file (renders each slide as a high-quality image via headless Chromium, default 3x resolution)

Supports technical sharing talks, architecture reviews, strategy decks, research summaries, pitch decks, and team updates. Outputs pure HTML/CSS/JS with no build tools required.

📎 [Sample repo](https://github.com/iuiaoin/deck-transformer) · [Live demo](https://iuiaoin.github.io/deck-transformer/)

### [knowledge-graph](https://github.com/iuiaoin/agent-skills/tree/main/skills/knowledge-graph)

Turn any docs folder, wiki, or knowledge base into an interactive knowledge map:

- **`/knowledge-graph <path-to-docs> [focus]`** — survey the folder with a script (titles, sections, cross-page links, `.order` files), distill it into concepts, domains, and reader journeys, then build a **self-contained HTML map**: a force-directed concept graph with no server, CDN, or network dependency
- Viewer features — search (`/`), group show/hide via legend, hover to highlight neighborhoods, click a node for a detail panel with summary + link back to the source document, edge-label toggle, accessible table view, light/dark theme
- **Built-in markdown reader** — every surveyed page is also rendered into `knowledge-graph/docs/` as an elegant, theme-aware HTML document (breadcrumbs, contents sidebar, tables/code/task-lists, images), with internal wiki links rewritten to other reader pages — clicking a node's source document never dumps raw markdown in the browser
- Works on plain markdown folders and Azure DevOps-style wikis (URL-encoded filenames, `.order` navigation, full-URL self-links); survey scales to thousands of pages, and generated node links are validated against the real file list before the map builds
- Everything lands in `./knowledge-graph/` in your working directory, with relative links throughout — the folder is portable as a unit; refinements only edit `graph.json` and rebuild, no re-survey

## Skill Structure

Each skill follows a standard layout:

```
skill-name/
├── SKILL.md              # Instructions and metadata (required)
├── scripts/              # Executable code for deterministic tasks
├── references/           # Documentation loaded into context as needed
└── assets/               # Files used in output (templates, images, etc.)
```

## Installation

Install any skill straight from this repo with [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx skills add iuiaoin/agent-skills --skill deck -g
```

`-g` installs globally (drop it for the current project); swap `--skill deck` for another skill, or use `--all` for every skill. Update later with `npx skills update deck`.