#!/usr/bin/env python3
"""Validate a knowledge-graph JSON file and build the interactive HTML viewer.

Validates graph.json (schema, referential integrity, budgets), then injects it
into assets/viewer-template.html. On validation errors it prints numbered,
actionable issues and exits 1 — fix graph.json and rerun. Warnings don't block.

By default it also renders every surveyed source page into a styled HTML reader
under <out-dir>/docs/, and the map links there (relative links — the whole
output folder stays self-contained and movable). Pass --docs none to keep raw
file:// links instead.

Stdlib only. Usage:
  build.py graph.json [--survey survey.json] [-o knowledge-graph/knowledge-map.html]
           [--title "..."] [--subtitle "..."] [--docs all|linked|none]
           [--link-base URL-or-path prefix]

  --survey     survey.json from survey.py; enables node.path validation against
               the real file list, powers the docs reader, and supplies titles.
  --docs       all (default): render every surveyed page; linked: only pages
               referenced by nodes; none: no reader, links point at the source
               files directly.
  --link-base  Only used with --docs none: prefix for source links (e.g. a
               published wiki base URL). Defaults to file:// into the surveyed
               folder.
"""

import argparse
import difflib
import json
import os
import re
import shutil
import sys
from datetime import date
from urllib.parse import quote

sys.dont_write_bytecode = True          # keep the skill folder free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from survey import normalize_key, pretty_name, strip_ext  # noqa: E402

RENDER_MD = {".md", ".markdown", ".mdx", ".rst", ".adoc"}
RENDER_PLAIN = {".txt", ".log"}
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

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


def escape_script(text):
    """Make arbitrary text safe inside a <script type="text/plain"> element."""
    return re.sub(r"(?i)</script", lambda m: "<\\/" + m.group(0)[2:], text)


def render_docs(survey, out_path, mode, node_paths):
    """Render source pages into <out-dir>/docs/ and return (count, docs_dir)."""
    source_dir = survey["source"]
    out_dir = os.path.dirname(os.path.abspath(out_path))
    docs_dir = os.path.join(out_dir, "docs")
    kg_dir = os.path.join(docs_dir, "_kg")
    os.makedirs(kg_dir, exist_ok=True)

    shutil.copyfile(os.path.join(ASSETS_DIR, "doc.css"), os.path.join(kg_dir, "doc.css"))
    shutil.copyfile(os.path.join(ASSETS_DIR, "doc.js"), os.path.join(kg_dir, "doc.js"))
    with open(os.path.join(ASSETS_DIR, "doc-template.html"), encoding="utf-8") as f:
        template = f.read()

    pages = survey.get("pages", [])
    if mode == "linked":
        pages = [p for p in pages if p["path"] in node_paths]

    # link index shared by every reader page (see doc.js resolveTarget)
    index, base = {}, {}
    for p in survey.get("pages", []):
        key = normalize_key(strip_ext(p["path"]))
        index[key] = p["path"]
        b = key.rsplit("/", 1)[-1]
        base[b] = "" if b in base and base[b] != p["path"] else p["path"]
    base = {k: v for k, v in base.items() if v}
    if mode == "linked":
        rendered = {p["path"] for p in pages}
        index = {k: v for k, v in index.items() if v in rendered}
        base = {k: v for k, v in base.items() if v in rendered}

    root_url = "file://" + quote(source_dir.rstrip("/"), safe="/:")
    # ADO wikis keep /.attachments at the wiki REPO root, which may be a parent
    # of the surveyed folder — find the directory that actually contains it.
    attach_url = root_url
    probe = source_dir.rstrip("/")
    for _ in range(3):
        if os.path.isdir(os.path.join(probe, ".attachments")):
            attach_url = "file://" + quote(probe, safe="/:")
            break
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    index_js = (
        f"const KG_INDEX={json.dumps(index, ensure_ascii=False)};"
        f"const KG_BASE={json.dumps(base, ensure_ascii=False)};"
        f"const KG_ROOT={json.dumps(root_url)};"
        f"const KG_ATTACH={json.dumps(attach_url)};"
        f"const KG_ROOT_NAME={json.dumps(normalize_key(os.path.basename(source_dir.rstrip('/'))))};"
        f"const KG_MAP={json.dumps(os.path.basename(out_path))};"
    ).replace("</", "<\\/")
    with open(os.path.join(kg_dir, "index.js"), "w", encoding="utf-8") as f:
        f.write(index_js)

    count = 0
    for page in pages:
        rel = page["path"]
        src_file = os.path.join(source_dir, rel)
        try:
            with open(src_file, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        dst = os.path.join(docs_dir, rel + ".html")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        ext = os.path.splitext(rel)[1].lower()
        if ext in (".html", ".htm"):
            with open(dst, "w", encoding="utf-8") as f:
                f.write(text)                       # already HTML: mirror as-is
            count += 1
            continue

        depth = rel.count("/")
        prefix = "../" * depth
        segs = rel.split("/")
        crumbs = "".join(
            f"{pretty_name(s)}<span class=\"sep\">/</span>" for s in segs[:-1]
        ) + f"<b>{page['title']}</b>"
        html = (template
                .replace("__KG_PREFIX__", prefix)
                .replace("__KG_DOC_TITLE__", page["title"])
                .replace("__KG_DOC_PATH__", rel)
                .replace("__KG_DOC_PLAIN__", "1" if ext in RENDER_PLAIN else "")
                .replace("__KG_DOC_CRUMBS__", crumbs)
                .replace("__KG_MAP_HREF__", prefix + "../" + os.path.basename(out_path))
                .replace("__KG_RAW_HREF__", root_url + "/" + quote(rel, safe="/"))
                .replace("__KG_DOC_META__",
                         f"{page['words']:,} words · {os.path.basename(source_dir.rstrip('/'))}")
                .replace("__KG_DOC_MD__", escape_script(text)))
        with open(dst, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
    return count, docs_dir


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("graph", help="graph.json produced by the analysis stage")
    ap.add_argument("--survey", help="survey.json from survey.py (enables path checks)")
    ap.add_argument("-o", "--out", default="knowledge-graph/knowledge-map.html")
    ap.add_argument("--title", help="Override the graph title")
    ap.add_argument("--subtitle", help="Override the auto subtitle")
    ap.add_argument("--docs", choices=["all", "linked", "none"], default=None,
                    help="Render source pages into <out-dir>/docs/ (default: all "
                         "when a local survey is given, none otherwise)")
    ap.add_argument("--link-base", dest="link_base", default=None,
                    help="With --docs none: prefix for source-document links "
                         "(default: file:// path of the surveyed folder)")
    ap.add_argument("--template",
                    default=os.path.join(ASSETS_DIR, "viewer-template.html"))
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

    out_parent = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_parent, exist_ok=True)

    docs_mode = args.docs
    if docs_mode is None:
        remote = bool(args.link_base and re.match(r"https?://", args.link_base))
        docs_mode = "none" if (remote or not survey) else "all"
    if docs_mode != "none" and not survey:
        sys.exit("error: --docs all/linked requires --survey (it supplies the "
                 "page list and titles)")

    docs_count = 0
    if docs_mode != "none":
        node_paths = {n.get("path") for n in graph.get("nodes", []) if n.get("path")}
        docs_count, docs_dir = render_docs(survey, args.out, docs_mode, node_paths)
        link_base = "docs/"
        doc_suffix = ".html"
    else:
        link_base = args.link_base
        if link_base is None and source_dir:
            link_base = "file://" + source_dir.rstrip("/") + "/"
        if link_base and not (link_base.endswith("/") or link_base.endswith("=")):
            link_base += "/"
        doc_suffix = ""

    payload = {
        "title": title,
        "subtitle": subtitle,
        "source": source_name,
        "generated": date.today().isoformat(),
        "linkBase": link_base or "",
        "docSuffix": doc_suffix,
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
    if docs_count:
        print(f"Rendered {docs_count} source page(s) into {docs_dir} "
              f"(map links open the styled reader)")


if __name__ == "__main__":
    main()
