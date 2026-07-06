#!/usr/bin/env python3
"""Validate a knowledge-graph JSON file and build the interactive HTML viewer.

Validates graph.json (schema, referential integrity, budgets), then injects it
into assets/viewer-template.html. On validation errors it prints numbered,
actionable issues and exits 1 — fix graph.json and rerun. Warnings don't block.

Stdlib only. Usage:
  build.py graph.json [--survey survey.json] [-o knowledge-graph.html]
           [--title "..."] [--subtitle "..."] [--link-base URL-or-path prefix]

  --survey     survey.json from survey.py; enables node.path validation against
               the real file list and defaults --link-base to the source folder.
  --link-base  Prefix for "Open source document" links. Node paths are URL-
               encoded per segment and appended. Pass "" to keep links relative.
"""

import argparse
import difflib
import json
import os
import re
import sys
from datetime import date

ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
EDGE_KINDS = {"hierarchy", "flow", "reference"}
MAX_GROUPS = 8          # matches the 8 validated categorical color slots
NODE_BUDGET = (8, 45)   # soft budget, warning only
LABEL_MAX = 60


def load_json(path, what):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"{what} not found: {path}"
    except json.JSONDecodeError as e:
        return None, f"{what} is not valid JSON: {e}"


def validate(graph, known_paths):
    errors, warnings = [], []

    def err(msg): errors.append(msg)
    def warn(msg): warnings.append(msg)

    if not isinstance(graph, dict):
        return ["graph.json must be a JSON object with groups/nodes/edges"], []

    groups = graph.get("groups", [])
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if not isinstance(nodes, list) or not nodes:
        return ["graph.nodes must be a non-empty list"], []
    if not isinstance(groups, list) or not isinstance(edges, list):
        return ["graph.groups and graph.edges must be lists"], []

    if len(groups) > MAX_GROUPS:
        err(f"{len(groups)} groups, max is {MAX_GROUPS} (one per validated color slot). "
            f"Fold the smallest or most peripheral groups into a broader theme.")

    group_ids = set()
    for i, g in enumerate(groups):
        gid = g.get("id", "")
        if not ID_RE.match(str(gid)):
            err(f"groups[{i}].id \"{gid}\": ids must match ^[a-z][a-z0-9_]*$")
        if gid in group_ids:
            err(f"groups[{i}].id \"{gid}\" is a duplicate")
        group_ids.add(gid)
        if not str(g.get("label", "")).strip():
            err(f"groups[{i}] (\"{gid}\") is missing a label")

    node_ids = set()
    for i, n in enumerate(nodes):
        nid = n.get("id", "")
        label = str(n.get("label", "")).strip()
        if not ID_RE.match(str(nid)):
            err(f"nodes[{i}].id \"{nid}\": ids must match ^[a-z][a-z0-9_]*$")
        if nid in node_ids:
            err(f"nodes[{i}].id \"{nid}\" is a duplicate")
        node_ids.add(nid)
        if not label:
            err(f"nodes[{i}] (\"{nid}\") is missing a label")
        elif len(label) > LABEL_MAX:
            warn(f"node \"{nid}\" label is {len(label)} chars; keep labels short "
                 f"(the full story belongs in summary)")
        gid = n.get("groupId")
        if gid is not None and gid not in group_ids:
            err(f"nodes[{i}] (\"{nid}\") references unknown groupId \"{gid}\"")
        w = n.get("weight")
        if w is not None and (not isinstance(w, int) or not 1 <= w <= 5):
            err(f"nodes[{i}] (\"{nid}\") weight must be an integer 1-5")
        path = n.get("path")
        if path and known_paths is not None and path not in known_paths:
            close = difflib.get_close_matches(path, known_paths, n=3, cutoff=0.55)
            hint = f" Close matches: {close}" if close else ""
            err(f"nodes[{i}] (\"{nid}\") path \"{path}\" is not in the survey "
                f"file list.{hint}")

    seen_edges = set()
    degree = {nid: 0 for nid in node_ids}
    for i, e in enumerate(edges):
        f, t = e.get("from"), e.get("to")
        if f not in node_ids:
            err(f"edges[{i}].from \"{f}\" is not a node id")
        if t not in node_ids:
            err(f"edges[{i}].to \"{t}\" is not a node id")
        if f == t:
            err(f"edges[{i}] is a self-loop on \"{f}\"")
        kind = e.get("kind")
        if kind is not None and kind not in EDGE_KINDS:
            err(f"edges[{i}].kind \"{kind}\" must be one of {sorted(EDGE_KINDS)}")
        key = (f, t)
        if key in seen_edges:
            warn(f"duplicate edge {f} -> {t}; merge them (labels can be combined)")
        seen_edges.add(key)
        if f in degree:
            degree[f] += 1
        if t in degree:
            degree[t] += 1

    lo, hi = NODE_BUDGET
    if len(nodes) > hi:
        warn(f"{len(nodes)} nodes — over the ~{hi} budget; a knowledge map should "
             f"be an opinionated overview, not an inventory. Merge leaf pages "
             f"into their parent concept.")
    if len(nodes) < lo:
        warn(f"only {len(nodes)} nodes — likely too sparse to be a useful map")
    if edges and len(edges) > 2.5 * len(nodes):
        warn(f"{len(edges)} edges for {len(nodes)} nodes — likely a hairball; "
             f"keep only the relationships a newcomer must know")
    orphans = [nid for nid, d in degree.items() if d == 0]
    if orphans:
        warn(f"unconnected nodes (no edges): {orphans} — connect or remove them")

    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("graph", help="graph.json produced by the analysis stage")
    ap.add_argument("--survey", help="survey.json from survey.py (enables path checks)")
    ap.add_argument("-o", "--out", default="knowledge-graph.html")
    ap.add_argument("--title", help="Override the graph title")
    ap.add_argument("--subtitle", help="Override the auto subtitle")
    ap.add_argument("--link-base", dest="link_base", default=None,
                    help="Prefix for source-document links (default: file:// path "
                         "of the surveyed folder, if --survey is given)")
    ap.add_argument("--template",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "assets", "viewer-template.html"))
    args = ap.parse_args()

    graph, e = load_json(args.graph, "graph file")
    if e:
        sys.exit(f"error: {e}")

    survey = None
    known_paths = None
    if args.survey:
        survey, e = load_json(args.survey, "survey file")
        if e:
            sys.exit(f"error: {e}")
        known_paths = [p["path"] for p in survey.get("pages", [])]

    errors, warnings = validate(graph, known_paths)
    for i, w in enumerate(warnings, 1):
        print(f"warning {i}: {w}", file=sys.stderr)
    if errors:
        print(f"\ngraph.json failed validation with {len(errors)} error(s):",
              file=sys.stderr)
        for i, msg in enumerate(errors, 1):
            print(f"  {i}. {msg}", file=sys.stderr)
        print("\nFix graph.json and rerun.", file=sys.stderr)
        sys.exit(1)

    title = args.title or graph.get("title") or "Knowledge graph"
    source_dir = survey.get("source") if survey else None
    source_name = os.path.basename(source_dir.rstrip("/")) if source_dir else graph.get("source", "")
    if args.subtitle:
        subtitle = args.subtitle
    elif survey:
        subtitle = (f"{survey['stats']['pages']:,} pages distilled to "
                    f"{len(graph.get('nodes', []))} concepts")
    else:
        subtitle = (f"{len(graph.get('nodes', []))} nodes · "
                    f"{len(graph.get('edges', []))} edges")

    link_base = args.link_base
    if link_base is None and source_dir:
        link_base = "file://" + source_dir.rstrip("/") + "/"
    if link_base and not (link_base.endswith("/") or link_base.endswith("=")):
        link_base += "/"

    payload = {
        "title": title,
        "subtitle": subtitle,
        "source": source_name,
        "generated": date.today().isoformat(),
        "linkBase": link_base or "",
        "graph": {
            "groups": graph.get("groups", []),
            "nodes": graph.get("nodes", []),
            "edges": graph.get("edges", []),
        },
    }

    with open(args.template, encoding="utf-8") as f:
        html = f.read()
    # '</' must not appear inside the inline <script> JSON payload
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__KG_DATA__", data).replace("__KG_TITLE__", title)
    if "__KG_" in html:
        sys.exit("error: template still contains an unreplaced __KG_ placeholder")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Built {args.out}: {len(payload['graph']['nodes'])} nodes, "
          f"{len(payload['graph']['edges'])} edges, "
          f"{len(payload['graph']['groups'])} groups"
          + (f" ({len(warnings)} warning(s) above)" if warnings else ""))


if __name__ == "__main__":
    main()
