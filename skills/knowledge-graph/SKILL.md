---
name: knowledge-graph
description: Turn any docs folder, wiki, or knowledge base into an interactive knowledge map — a standalone HTML force-directed graph of concepts, domains, and reader journeys, with search, group filtering, and per-node links back to the source documents. Manually invoked via the /knowledge-graph command with a path to the docs/wiki folder, optionally followed by a focus hint and "--linkbase" plus a published wiki URL to make nodes link to the online wiki; also fits requests like "map this wiki", "visualize our docs as a graph", or "make a knowledge graph of this folder".
---

# Knowledge Graph — Interactive Map of a Knowledge Base

Distill a folder of documents (markdown wiki, docs site source, notes collection)
into an interactive concept map. The pipeline: **survey** the folder with a script,
**analyze** what the knowledge is about, design a **graph.json**, then **build** a
self-contained HTML viewer. The output needs no server, CDN, or network — one file.

## Workflow

### 1. Locate the source; parse options

Invocation shape: `/knowledge-graph <path-to-docs> [focus] [--linkbase <url>]`.
It should name one folder — the knowledge base root (e.g. `/knowledge-graph
~/wiki` or `/knowledge-graph ./docs "focus on onboarding"`). Remaining prose is
guidance for what the map should emphasize.

**`--linkbase <url>`** (optional) — the knowledge base is published (e.g. an
Azure DevOps wiki:
`--linkbase "https://dev.azure.com/org/proj/_wiki/wikis/X.wiki?pagePath=Wiki/"`).
Node links then open the online wiki instead of a local reader: skip the
markdown reader entirely (no `docs/` folder) and pass the URL to build.py in
step 5, which appends each node's path with the trailing `.md` stripped
(`<url>` + `10-Inference/Inference-via-Bus`).

If no folder was given, ask for it. If the request is ambiguous between folders,
ask with your agent's structured question tool — `AskUserQuestion` (Claude Code),
`ask_user` (Copilot CLI), `request_user_input` (Codex) — or as a plain question if
no such tool exists.

**Every artifact goes into `knowledge-graph/` under the user's current working
directory** (the directory the command was invoked from) — create it if missing.
Never write outputs to the agent's session/temp/scratch directory: the user must
be able to find, keep, and open these files after the session ends. The script
defaults already target `knowledge-graph/`; run them from the user's working
directory.

### 2. Survey (scripted)

```
python3 <skill>/scripts/survey.py <source-dir> --out knowledge-graph/survey.json
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

Read [references/graph-spec.md](references/graph-spec.md), then write
`knowledge-graph/graph.json` (schema, node/edge/group rules, and budgets are all
there). Honor any focus the user gave in the invocation.

### 5. Build (scripted)

```
python3 <skill>/scripts/build.py knowledge-graph/graph.json \
        --survey knowledge-graph/survey.json -o knowledge-graph/<name>-map.html
```

The script validates graph.json and refuses to build on errors — fix the file and
rerun until clean (aim for zero warnings too).

By default it also renders **every surveyed page** into `knowledge-graph/docs/`
as a styled, theme-aware HTML reader (markdown rendered client-side; internal
wiki links rewritten to other reader pages; images loaded from the source
folder). Map links open the reader via relative URLs, so the whole
`knowledge-graph/` folder is portable.

**If the user passed `--linkbase <url>`**, add `--link-base "<url>"` to the
build.py command instead. An http(s) link-base automatically skips the reader
(no `docs/` is generated) and links each node straight to the published wiki,
dropping the source file extension (`.../Inference-via-Bus.md` →
`<url>10-Inference/Inference-via-Bus`); already-URL-encoded filenames like
`Q%2A-training` are passed through, not double-encoded. `--keep-ext` keeps the
extension if the target actually serves raw files.

Other flags: `--docs linked` renders only node-linked pages; `--docs none`
skips the reader and links to local source files.

### 6. Verify, deliver, iterate

- Open the HTML in a browser (macOS `open`, Linux `xdg-open`, Windows `start`).
  If a headless browser / screenshot tool is available, capture the initial view
  and check it: no overlapping labels, groups form readable neighborhoods, the
  journey edges are traceable. Save any QA screenshots into `knowledge-graph/`
  too (e.g. `knowledge-graph/map-check.png`) and tell the user they are safe to
  delete. Drag-test is not needed — layout is deterministic.
- Spot-check 2–3 "open source document" links from the detail panel, and one
  rendered reader page (headings, a table or code block, an internal link). In
  `--linkbase` mode check the composed URLs instead (extension stripped, path
  appended to the base as expected).
- Tell the user the file path, the distillation ratio (N pages → M concepts), and
  the viewer's affordances: search (`/`), group show/hide via legend, edge-label
  toggle, list/table view, light/dark theme, click a node for details + source
  link, drag to pin, double-click to release; reader pages have breadcrumbs,
  "◂ Map" / "Raw" links, a contents sidebar, and the same theme toggle.
- **Iterating** ("add more depth on X", "drop the archive", "rename a group"):
  edit `knowledge-graph/graph.json` and rerun step 5 — no need to re-survey
  unless the source folder itself changed. Deeper content questions may need
  another `--dir` drilldown or a few more pages read.

## Output

Everything lives in `knowledge-graph/` under the user's working directory:

```
<invocation directory>/
└── knowledge-graph/
    ├── survey.json              # full page inventory (step 2)
    ├── graph.json               # the designed graph (step 4)
    ├── <name>-map.html          # self-contained interactive map (step 5)
    ├── map-check.png            # optional QA screenshot(s); disposable
    └── docs/                    # styled reader (step 5; omitted with --linkbase)
        ├── _kg/                 # shared reader css/js + link index
        └── <page path>.html     # one per surveyed page, mirrored layout
```

## Notes

- The map template is `assets/viewer-template.html`; the reader is
  `assets/doc-template.html` + `assets/doc.css` + `assets/doc.js` (copied to
  `docs/_kg/`). build.py injects all data. If a user asks for visual
  customization (colors, physics, sizing), edit the **generated** files — change
  the templates only for fixes that should apply to every future map.
- Both scripts are Python 3 stdlib only; no installation step.
- For very large knowledge bases, the survey digest aggregates by section — do not
  read `survey.json` wholesale into context; grep it or use `--dir`.
