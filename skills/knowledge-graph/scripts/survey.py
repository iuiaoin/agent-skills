#!/usr/bin/env python3
"""Survey a docs/wiki folder: inventory pages, titles, headings, and internal links.

Produces two things:
  1. A human-readable digest on stdout (sections, entry points, link hubs) sized
     for an agent to read directly, even for wikis with thousands of pages.
  2. A survey.json file with the full per-page inventory, used by build.py to
     validate node paths and by the agent for targeted lookups.

Stdlib only. Usage:
  survey.py <source-dir> [--out survey.json] [--dir <subdir>] [--top N]

  --dir <subdir>   Drill into one section: list its pages with titles and links
                   (prints to stdout; does not rewrite survey.json).
  --top N          How many hub/large pages to show in the digest (default 30).
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from urllib.parse import unquote, urlparse

DOC_EXTENSIONS = {".md", ".markdown", ".mdx", ".txt", ".rst", ".adoc", ".html", ".htm"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", ".attachments", "attachments",
             "images", "img", "assets", ".vscode", "__pycache__"}
ENTRY_NAMES = {"welcome", "home", "index", "readme", "overview", "start-here",
               "getting-started", "introduction", "intro"}

MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
HREF_RE = re.compile(r"href=[\"']([^\"'#]+)[\"']", re.IGNORECASE)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)


def normalize_key(s: str) -> str:
    """Normalize a path-ish string for matching links to files on disk.

    Handles URL-encoded wiki filenames (ADO style: space→'-', literal '-'→'%2D')
    and case differences. 'Q%2A-training' and 'Q*-training' both normalize to
    'q*-training'.
    """
    s = unquote(s)
    s = s.replace("\\", "/").strip("/")
    s = s.replace(" ", "-")
    return s.lower()


def strip_ext(path: str) -> str:
    root, ext = os.path.splitext(path)
    return root if ext.lower() in DOC_EXTENSIONS else path


def pretty_name(filename: str) -> str:
    """Fallback title from a wiki filename: 'SWE-Agent%3A-Notes' → 'SWE Agent: Notes'."""
    name = strip_ext(filename)
    name = name.replace("-", " ")
    return unquote(name).strip()


def read_text(path: str) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def extract_title(text: str, filename: str, filename_is_canonical: bool) -> str:
    # In ADO-style wikis the filename IS the page title and the first H1 is
    # usually just the first section — prefer the filename there.
    if filename_is_canonical:
        return pretty_name(filename)
    head = text[:4000]
    m = H1_RE.search(head)
    if m:
        h1 = m.group(1).strip().lstrip("#").strip()
        if 0 < len(h1) <= 80:
            return h1
    if head.startswith("---"):
        m = FRONTMATTER_TITLE_RE.search(head[:1500])
        if m:
            return m.group(1).strip()
    return pretty_name(filename)


def extract_links(text: str, ext: str):
    targets = []
    if ext in (".html", ".htm"):
        targets.extend(HREF_RE.findall(text))
    else:
        targets.extend(t for _, t in MD_LINK_RE.findall(text))
        targets.extend(WIKILINK_RE.findall(text))
    return targets


class Resolver:
    """Resolve link targets to relative file paths within the surveyed set."""

    def __init__(self, rel_paths, source_name: str):
        self.by_relpath = {}
        self.by_basename = {}
        self.source_name = normalize_key(source_name)
        for rel in rel_paths:
            key = normalize_key(strip_ext(rel))
            self.by_relpath[key] = rel
            base = normalize_key(strip_ext(os.path.basename(rel)))
            # Basename lookup only stays valid while unambiguous.
            self.by_basename[base] = None if base in self.by_basename else rel

    def resolve(self, target: str, from_rel: str):
        target = target.strip()
        if not target or target.startswith(("mailto:", "tel:", "data:")):
            return None
        parsed = urlparse(target)
        if parsed.scheme in ("http", "https", "ftp"):
            # Wiki pages often self-link via full host URLs
            # (e.g. dev.azure.com/.../_wiki/wikis/<wiki>/<id>/<Page-Name>).
            # Best-effort: match the final path segment against known pages.
            if "/_wiki/" in parsed.path or "/wikis/" in parsed.path:
                last = parsed.path.rstrip("/").rsplit("/", 1)[-1]
                hit = self.by_basename.get(normalize_key(strip_ext(last)))
                if hit:
                    return hit
            return "EXTERNAL"
        path = unquote(parsed.path) if parsed.scheme else target.split("#")[0].split("?")[0]
        path = path.strip()
        if not path:
            return None

        candidates = []
        norm = normalize_key(strip_ext(path))
        if path.startswith("/"):
            # Absolute wiki path, possibly prefixed with the wiki root name
            # (ADO style: '/Orange-wiki/Section/Page').
            candidates.append(norm)
            first, _, rest = norm.partition("/")
            if rest and first == self.source_name:
                candidates.append(rest)
        else:
            # Relative to the linking file's directory, then repo-root relative.
            from_dir = os.path.dirname(from_rel)
            joined = os.path.normpath(os.path.join(from_dir, path))
            candidates.append(normalize_key(strip_ext(joined)))
            candidates.append(norm)

        for cand in candidates:
            if cand in self.by_relpath:
                return self.by_relpath[cand]
        base = norm.rsplit("/", 1)[-1]
        hit = self.by_basename.get(base)
        return hit  # may be None (ambiguous or unknown)


def load_order(dirpath: str):
    order_file = os.path.join(dirpath, ".order")
    if not os.path.isfile(order_file):
        return []
    return [line.strip() for line in read_text(order_file).splitlines() if line.strip()]


def collect(source: str):
    rel_paths = []
    orders = {}
    for dirpath, dirnames, filenames in os.walk(source):
        dirnames[:] = sorted(d for d in dirnames
                             if d.lower() not in SKIP_DIRS and not d.startswith("."))
        rel_dir = os.path.relpath(dirpath, source)
        order = load_order(dirpath)
        if order:
            orders["." if rel_dir == "." else rel_dir] = order
        for fn in sorted(filenames):
            if fn.startswith("."):
                continue
            if os.path.splitext(fn)[1].lower() in DOC_EXTENSIONS:
                rel = fn if rel_dir == "." else f"{rel_dir}/{fn}"
                rel_paths.append(rel.replace(os.sep, "/"))
    return rel_paths, orders


def survey(source: str):
    source = os.path.abspath(source)
    source_name = os.path.basename(source.rstrip("/"))
    rel_paths, orders = collect(source)
    resolver = Resolver(rel_paths, source_name)

    pages = []
    inbound = {rel: 0 for rel in rel_paths}
    unresolved = 0
    external = 0
    ado_style = bool(orders)
    for rel in rel_paths:
        text = read_text(os.path.join(source, rel))
        ext = os.path.splitext(rel)[1].lower()
        title = extract_title(text, os.path.basename(rel), ado_style)
        headings = [h.strip() for _, h in HEADING_RE.findall(text)][:12]
        words = len(text.split())
        out_links = []
        for target in extract_links(text, ext):
            hit = resolver.resolve(target, rel)
            if hit == "EXTERNAL":
                external += 1
            elif hit is None:
                unresolved += 1
            elif hit != rel and hit not in out_links:
                out_links.append(hit)
        for hit in out_links:
            inbound[hit] += 1
        pages.append({"path": rel, "title": title, "words": words,
                      "headings": headings, "links_out": out_links})

    for page in pages:
        page["links_in"] = inbound[page["path"]]

    sections = {}
    for page in pages:
        sec = page["path"].split("/")[0] if "/" in page["path"] else "."
        entry = sections.setdefault(sec, {"dir": sec, "files": 0, "words": 0})
        entry["files"] += 1
        entry["words"] += page["words"]

    entry_points = []
    root_order = orders.get(".", [])
    if root_order:
        first = resolver.resolve(root_order[0], "")
        if first:
            entry_points.append(first)
    for page in pages:
        base = normalize_key(strip_ext(os.path.basename(page["path"])))
        if base in ENTRY_NAMES and page["path"] not in entry_points:
            entry_points.append(page["path"])

    return {
        "source": source,
        "generated": date.today().isoformat(),
        "stats": {
            "pages": len(pages),
            "words": sum(p["words"] for p in pages),
            "internal_links": sum(len(p["links_out"]) for p in pages),
            "external_links": external,
            "unresolved_links": unresolved,
            "orphan_pages": sum(1 for p in pages if p["links_in"] == 0),
        },
        "entry_points": entry_points,
        "root_order": root_order,
        "sections": sorted(sections.values(), key=lambda s: -s["words"]),
        "pages": pages,
    }


def fmt_page(page, source=""):
    title = page["title"]
    if len(title) > 70:
        title = title[:67] + "..."
    return (f"  {page['path']}  —  \"{title}\""
            f"  ({page['words']}w, in:{page['links_in']}, out:{len(page['links_out'])})")


def print_digest(data, top: int):
    stats = data["stats"]
    print(f"SOURCE: {data['source']}")
    print(f"PAGES: {stats['pages']}   WORDS: {stats['words']:,}   "
          f"INTERNAL LINKS: {stats['internal_links']}   "
          f"UNRESOLVED: {stats['unresolved_links']}   ORPHANS: {stats['orphan_pages']}")
    print()

    if data["entry_points"]:
        print("ENTRY POINTS (read these first):")
        for rel in data["entry_points"]:
            print(f"  {rel}")
        print()

    if data["root_order"]:
        print("ROOT .order (author-curated top-level ordering):")
        for name in data["root_order"]:
            print(f"  {pretty_name(name)}")
        print()

    print("SECTIONS (top-level dirs by volume):")
    for sec in data["sections"][:25]:
        label = "(root)" if sec["dir"] == "." else sec["dir"]
        print(f"  {label:<44} {sec['files']:>4} pages  {sec['words']:>8,} words")
    print()

    pages = data["pages"]
    # Inbound links weigh double: being linked TO signals a core concept,
    # while many outbound links usually just mark an index page.
    hubs = sorted(pages, key=lambda p: -(2 * p["links_in"] + len(p["links_out"])))[:top]
    hubs = [p for p in hubs if p["links_in"] + len(p["links_out"]) > 0]
    print(f"TOP {len(hubs)} HUB PAGES (most connected — likely core concepts):")
    for page in hubs:
        print(fmt_page(page))
    print()

    largest = sorted(pages, key=lambda p: -p["words"])[:top]
    print(f"TOP {len(largest)} LARGEST PAGES:")
    for page in largest:
        print(fmt_page(page))


def print_dir(data, subdir: str):
    norm = subdir.strip("/")
    matches = [p for p in data["pages"]
               if p["path"].startswith(norm + "/") or
               (norm == "." and "/" not in p["path"])]
    if not matches:
        print(f"No pages under '{subdir}'.", file=sys.stderr)
        return
    print(f"SECTION {subdir}: {len(matches)} pages")
    for page in sorted(matches, key=lambda p: -(p["links_in"] + p["words"] / 1000)):
        print(fmt_page(page))
        for h in page["headings"][:6]:
            print(f"      · {h}")
        if page["links_out"]:
            shown = ", ".join(page["links_out"][:8])
            print(f"      → links to: {shown}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="Docs/wiki folder to survey")
    ap.add_argument("--out", default="survey.json", help="Where to write the JSON inventory")
    ap.add_argument("--dir", dest="subdir", help="Drill into one section instead of the digest")
    ap.add_argument("--top", type=int, default=30, help="Rows in digest hub/largest tables")
    args = ap.parse_args()

    if not os.path.isdir(args.source):
        sys.exit(f"error: not a directory: {args.source}")

    data = survey(args.source)

    if args.subdir:
        print_dir(data, args.subdir)
        return

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print_digest(data, args.top)
    print(f"\nFull inventory written to {args.out}")


if __name__ == "__main__":
    main()
