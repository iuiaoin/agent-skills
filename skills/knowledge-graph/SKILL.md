---
name: knowledge-graph
description: Turn any docs folder, wiki, or knowledge base into an interactive knowledge map — a standalone HTML force-directed graph of concepts, domains, and reader journeys, with search, group filtering, and per-node links back to the source documents. Manually invoked via the /knowledge-graph command with a path to the docs/wiki folder; also fits requests like "map this wiki", "visualize our docs as a graph", or "make a knowledge graph of this folder".
---

# Knowledge Graph — Interactive Map of a Knowledge Base

Distill a folder of documents (markdown wiki, docs site source, notes collection)
into an interactive concept map. The pipeline: **survey** the folder with a script,
**analyze** what the knowledge is about, design a **graph.json**, then **build** a
self-contained HTML viewer. The output needs no server, CDN, or network — one file.

## Workflow

### 1. Locate the source

The invocation should name one folder — the knowledge base root (e.g.
`/knowledge-graph ~/wiki` or `/knowledge-graph ./docs "focus on onboarding"`).
Extra prose in the invocation is guidance for what the map should emphasize.

If no folder was given, ask for it. If the request is ambiguous between folders,
ask with your agent's structured question tool — `AskUserQuestion` (Claude Code),
`ask_user` (Copilot CLI), `request_user_input` (Codex) — or as a plain question if
no such tool exists.

### 2. Survey (scripted)

```
python3 <skill>/scripts/survey.py <source-dir> --out survey.json
```

Prints a digest (entry points, author-curated `.order` ordering, sections by
volume, hub pages by inbound links) and writes `survey.json` — the full per-page
inventory used later for path validation. Handles markdown/wikitext/HTML,
wikilinks, URL-encoded Azure-DevOps-style filenames, and `.order` files. It reads
thousands of pages in seconds; never inventory a wiki by hand.

Drill into a section without rereading files:
`python3 <skill>/scripts/survey.py <source-dir> --dir <section>`.

### 3. Analyze

Read [references/analysis.md](references/analysis.md) and follow it: interpret the
digest, read a targeted sample of pages (entry points, hubs, one page per major
section), then write the short prose **explanation** of domains, core concepts,
relationships, and reader journeys. Do not skip the explanation — it is what keeps
the graph honest.

### 4. Design the graph

Read [references/graph-spec.md](references/graph-spec.md), then write `graph.json`
(schema, node/edge/group rules, and budgets are all there). Honor any focus the
user gave in the invocation.

### 5. Build (scripted)

```
python3 <skill>/scripts/build.py graph.json --survey survey.json -o <name>-knowledge-map.html
```

The script validates graph.json and refuses to build on errors — fix the file and
rerun until clean (aim for zero warnings too). Useful flags: `--title`,
`--subtitle`, `--link-base <url>` to make node links open a published wiki instead
of local files (default is `file://` links into the surveyed folder).

### 6. Verify, deliver, iterate

- Open the HTML in a browser (macOS `open`, Linux `xdg-open`, Windows `start`).
  If a headless browser / screenshot tool is available, capture the initial view
  and check it: no overlapping labels, groups form readable neighborhoods, the
  journey edges are traceable. Drag-test is not needed — layout is deterministic.
- Spot-check 2–3 "open source document" links from the detail panel.
- Tell the user the file path, the distillation ratio (N pages → M concepts), and
  the viewer's affordances: search (`/`), group show/hide via legend, edge-label
  toggle, list/table view, light/dark theme, click a node for details + source
  link, drag to pin, double-click to release.
- **Iterating** ("add more depth on X", "drop the archive", "rename a group"):
  edit `graph.json` and rerun step 5 — no need to re-survey unless the source
  folder itself changed. Deeper content questions may need another `--dir`
  drilldown or a few more pages read.

## Output

```
working-directory/
├── survey.json                  # full page inventory (step 2)
├── graph.json                   # the designed graph (step 4)
└── <name>-knowledge-map.html    # self-contained interactive viewer (step 5)
```

## Notes

- The viewer template lives at `assets/viewer-template.html`; build.py injects the
  graph payload into it. If a user asks for visual customization (colors, physics,
  sizing), edit a **copy** of the built HTML or pass different data — change the
  template itself only for fixes that should apply to every future map.
- Both scripts are Python 3 stdlib only; no installation step.
- For very large knowledge bases, the survey digest aggregates by section — do not
  read `survey.json` wholesale into context; grep it or use `--dir`.
