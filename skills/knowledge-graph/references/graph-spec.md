# Graph Spec — graph.json

The graph is the explanation rendered as data. Produce a crisp, opinionated
overview a human can absorb in one screen — **not** an inventory of every page.
`scripts/build.py` validates this schema and prints numbered errors; fix the file
and rerun until it passes.

## Schema

```json
{
  "title": "Acme Wiki — Knowledge Map",
  "groups": [
    {"id": "onboarding", "label": "Getting Started", "description": "optional"}
  ],
  "nodes": [
    {
      "id": "deploy_guide",
      "label": "Deployment Guide",
      "type": "how-to",
      "summary": "One or two sentences shown in the detail panel.",
      "groupId": "onboarding",
      "path": "5.-Deployment/Guide.md",
      "weight": 4
    }
  ],
  "edges": [
    {"from": "training", "to": "deploy_guide", "label": "then deploy", "kind": "flow"}
  ]
}
```

| Field | Rules |
|---|---|
| `id` | `^[a-z][a-z0-9_]*$`, unique |
| `label` | short human name, 1–4 words (≤60 chars) |
| `type` | freeform, shown as secondary detail: `concept`, `how-to`, `tutorial`, `reference`, `policy`, `tool`, `dataset`, `process stage`, `entry point`, `section`, `scratch space`… pick what fits |
| `summary` | 1–2 sentences; carries what the label cannot |
| `groupId` | optional; must match a group id. Ungrouped renders neutral gray |
| `path` | optional; must be a real file from survey.json (validated). Powers the "open source document" link — prefer the concept's best/hub page |
| `weight` | 1–5 importance for a newcomer (node size). Default 2; use 5 sparingly |
| edge `label` | short verb phrase ≤3 words: "step 1", "produces", "runs on", "reward signal" |
| edge `kind` | `hierarchy` (contains / part-of), `flow` (journey, pipeline, sequence — rendered with an arrow), `reference` (see-also / uses — rendered dashed) |

## Design rules

Adapted for knowledge, where repository diagrams would talk about subsystems and
data flows:

- **Nodes are concepts, not files.** One node often stands for a whole cluster of
  pages; point `path` at the cluster's hub page and let `summary` say the rest.
  Never create one node per page.
- **Prefer the reader's mental model over the folder tree.** Folders are evidence
  for groups, not a mandate. Merge folders that are one theme; split a folder that
  hides two.
- **Show at least one journey.** Chain `flow` edges so a newcomer can trace
  "start here → … → productive" (onboarding, content lifecycle, process stages).
- **Edges must earn their place.** Each edge is a relationship you can point to in
  the source (a link, an explicit "before/after/uses" statement, or containment).
  Prefer the relationships a newcomer must know; drop the rest — a hairball helps
  no one.
- **Compress dead weight.** Archives, personal scratch, meeting logs: at most one
  low-weight node each (or omit entirely), whatever their page count.
- **Decompose what is central.** If one theme dominates the knowledge base, break
  it into 2–5 internal nodes instead of one black box.
- **Budgets** (soft, warned by build.py): 18–40 nodes, 3–8 groups (hard max 8 —
  one per validated color slot), edges ≈ 1–1.5× nodes. Smaller is better if it
  still captures the territory. No unconnected nodes.
- Weight by importance to a newcomer, not by page count or word count.
- Every `weight ≥ 4` node deserves a `path` and a good `summary` — these are the
  nodes people will click.

## Validation loop

```
python3 <skill>/scripts/build.py graph.json --survey survey.json -o <name>.html
```

Errors block the build and name the exact node/edge (unknown ids, duplicate ids,
bad paths — with close-match suggestions, >8 groups, self-loops). Warnings flag
budget and quality issues (too many/few nodes, hairball edge count, orphan nodes,
overlong labels). Resolve errors, take warnings seriously, rerun. Aim for a build
with zero warnings before showing the result.
