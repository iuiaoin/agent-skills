/* Knowledge-graph document reader.
 * Renders the page's embedded markdown (script#kg-md) to HTML and rewrites
 * internal links to their rendered counterparts using the KG_* globals from
 * _kg/index.js (KG_INDEX, KG_BASE, KG_ROOT, KG_ROOT_NAME, KG_MAP).
 * Zero dependencies; GFM subset: headings, emphasis, code, lists (nested,
 * tasks), tables, blockquotes, images (incl. ADO "=WxH" sizing), wikilinks,
 * [[_TOC_]], safe inline-HTML passthrough. */
(function () {
"use strict";

/* ---------------- context ---------------- */
const body = document.body;
const DOC_PATH = body.dataset.path || "";
const IS_PLAIN = body.dataset.plain === "1";
const DEPTH = (DOC_PATH.match(/\//g) || []).length;
const PREFIX = "../".repeat(DEPTH);
const CUR_DIR = DOC_PATH.includes("/") ? DOC_PATH.slice(0, DOC_PATH.lastIndexOf("/")) : "";

const encodeSegs = p => p.split("/").map(encodeURIComponent).join("/");
const escapeHtml = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/* ---------------- link resolution (mirrors survey.py) ---------------- */
function normKey(s) {
  try { s = decodeURIComponent(s); } catch (_) {}
  return s.replace(/\\/g, "/").replace(/^\/+|\/+$/g, "").replace(/ /g, "-").toLowerCase();
}
const stripExt = s => s.replace(/\.(md|markdown|mdx|txt|rst|adoc|html|htm)$/i, "");
function normPath(p) {
  const out = [];
  for (const seg of p.split("/")) {
    if (!seg || seg === ".") continue;
    if (seg === "..") out.pop(); else out.push(seg);
  }
  return out.join("/");
}
/* returns {doc, frag} | {raw, frag} | {ext} */
function resolveTarget(target) {
  target = target.trim();
  if (!target) return { ext: "#" };
  const hashAt = target.indexOf("#");
  let frag = "";
  if (hashAt >= 0) { frag = target.slice(hashAt); target = target.slice(0, hashAt); }
  target = target.split("?")[0];
  if (!target) return { doc: DOC_PATH, frag };            // same-page anchor

  if (/^[a-z][a-z0-9+.-]*:/i.test(target)) {
    if (/^https?:/i.test(target) && /\/_wiki\/|\/wikis\//i.test(target)) {
      const last = target.replace(/\/+$/, "").split("/").pop();
      const hit = KG_BASE[normKey(stripExt(last))];
      if (hit) return { doc: hit, frag };
    }
    return { ext: target + frag };
  }

  let candidates = [];
  let rawPath;
  if (target.startsWith("/")) {
    const p = target.replace(/^\/+/, "");
    const key = normKey(stripExt(p));
    candidates.push(key);
    const cut = key.indexOf("/");
    if (cut > 0 && key.slice(0, cut) === KG_ROOT_NAME) candidates.push(key.slice(cut + 1));
    rawPath = p;
  } else {
    const joined = normPath((CUR_DIR ? CUR_DIR + "/" : "") + target);
    candidates.push(normKey(stripExt(joined)), normKey(stripExt(target)));
    rawPath = joined;
  }
  for (const c of candidates) if (KG_INDEX[c]) return { doc: KG_INDEX[c], frag };
  const base = candidates[0].split("/").pop();
  if (KG_BASE[base]) return { doc: KG_BASE[base], frag };
  return { raw: rawPath, frag };
}
/* attachments may live at the wiki repo root rather than inside the surveyed
 * folder (ADO layout) — KG_ATTACH points wherever /.attachments was found */
const rawBase = p => (/^\.attachments\//i.test(p) ? KG_ATTACH : KG_ROOT);
function hrefFor(target) {
  const r = resolveTarget(target);
  if (r.ext) return { href: r.ext, ext: true };
  if (r.doc) return { href: PREFIX + encodeSegs(r.doc) + ".html" + (r.frag || "") };
  return { href: rawBase(r.raw) + "/" + encodeSegs(r.raw) + (r.frag || ""), raw: true };
}
function assetSrc(src) {
  if (/^[a-z][a-z0-9+.-]*:/i.test(src)) return src;
  const p = src.startsWith("/") ? src.replace(/^\/+/, "")
                                : normPath((CUR_DIR ? CUR_DIR + "/" : "") + src);
  return rawBase(p) + "/" + encodeSegs(p);
}

/* ---------------- inline rendering ---------------- */
function inline(text) {
  const store = [];
  const put = html => "\x00" + (store.push(html) - 1) + "\x00";

  // code spans first — protect their content from everything else
  text = text.replace(/(`+)([^`]|[\s\S]*?[^`])\1(?!`)/g,
    (_, t, code) => put("<code>" + escapeHtml(code.trim()) + "</code>"));
  // autolinks
  text = text.replace(/<(https?:\/\/[^\s<>]+)>/gi,
    (_, url) => put(`<a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(url)}</a>`));

  text = escapeHtml(text);

  // let a whitelist of inline HTML tags back through (wikis rely on them)
  text = text.replace(/&lt;(\/?)(br|b|i|u|em|strong|sub|sup|kbd|mark|span|small|ins|del|details|summary|center|font|img|a)((?:\s(?:[^&<>]|&quot;)*)?)\s*(\/?)&gt;/gi,
    (_, close, tag, attrs, self) => "<" + close + tag.toLowerCase() + attrs.replace(/&quot;/g, '"') + (self ? " /" : "") + ">");

  // images (with optional ADO "=WxH" size hint), before links
  text = text.replace(/!\[([^\]]*)\]\(\s*([^)\s]+)(?:\s+=(\d*)x?(\d*))?(?:\s+&quot;[^&]*&quot;)?\s*\)/g,
    (_, alt, src, w, h) => {
      let dims = "";
      if (w) dims += ` width="${w}"`;
      if (h) dims += ` height="${h}"`;
      return put(`<img src="${assetSrc(src)}" alt="${alt}" loading="lazy"${dims}>`);
    });
  // wikilinks [[Page]] / [[Page|label]]
  text = text.replace(/\[\[([^\]|#]+)(#[^\]|]*)?(?:\|([^\]]+))?\]\]/g, (_, page, frag, label) => {
    if (/^_TOC_$/i.test(page.trim())) return put('<div class="toc-inline" data-toc></div>');
    const r = hrefFor(page.trim() + (frag || ""));
    return put(`<a href="${r.href}"${r.ext ? ' target="_blank" rel="noopener"' : ""}>${label || page}</a>`);
  });
  // standard links
  text = text.replace(/\[([^\]]+)\]\(\s*([^)\s]+)(?:\s+&quot;[^&]*&quot;)?\s*\)/g, (_, label, href) => {
    const r = hrefFor(href);
    return put(`<a href="${r.href}"${r.ext ? ' target="_blank" rel="noopener"' : ""}>` + inlineLight(label) + "</a>");
  });
  // bare URLs
  text = text.replace(/(^|[\s(])((?:https?:\/\/)[^\s<>()]+[^\s<>().,;:!?'"])/g,
    (_, pre, url) => pre + put(`<a href="${url}" target="_blank" rel="noopener">${url}</a>`));

  text = emphasis(text);
  text = text.replace(/ {2,}\n|\\\n/g, "<br>\n");
  while (/\x00\d+\x00/.test(text)) text = text.replace(/\x00(\d+)\x00/g, (_, i) => store[+i]);
  return text;
}
function emphasis(text) {
  return text
    .replace(/~~(?=\S)([\s\S]*?\S)~~/g, "<del>$1</del>")
    .replace(/\*\*(?=\S)([\s\S]*?\S)\*\*/g, "<strong>$1</strong>")
    .replace(/__(?=\S)([\s\S]*?\S)__/g, "<strong>$1</strong>")
    .replace(/(^|[^\w*])\*(?=\S)([^*]*?\S)\*(?=[^\w*]|$)/g, "$1<em>$2</em>")
    .replace(/(^|[^\w_])_(?=\S)([^_]*?\S)_(?=[^\w_]|$)/g, "$1<em>$2</em>");
}
function inlineLight(text) { return emphasis(text); }

/* ---------------- block rendering ---------------- */
const headings = [];
const usedIds = new Set();
function slugify(text) {
  let id = text.toLowerCase().replace(/<[^>]*>/g, "").replace(/[`*_~[\]()!]/g, "")
    .trim().replace(/[^\p{L}\p{N}\s-]/gu, "").replace(/\s+/g, "-").replace(/-+/g, "-") || "section";
  let unique = id, n = 2;
  while (usedIds.has(unique)) unique = id + "-" + n++;
  usedIds.add(unique);
  return unique;
}

function renderBlocks(src) {
  const lines = src.split("\n");
  let html = "", i = 0;

  const isBlank = l => /^\s*$/.test(l);
  const fenceRe = /^(\s*)(```+|~~~+)\s*([\w+-]*)/;
  const headRe = /^(#{1,6})\s+(.*?)\s*#*\s*$/;
  const hrRe = /^\s{0,3}([-*_])(\s*\1){2,}\s*$/;
  const listRe = /^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$/;
  const tableSepRe = /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/;
  const htmlBlockRe = /^\s*<\/?(div|details|summary|table|thead|tbody|tr|td|th|p|center|video|img|br|hr|ul|ol|li|blockquote|h[1-6]|pre|iframe|!--)[\s>/!-]/i;

  while (i < lines.length) {
    const line = lines[i];
    if (isBlank(line)) { i++; continue; }

    const fence = line.match(fenceRe);
    if (fence) {
      const close = new RegExp("^\\s*" + fence[2].slice(0, 3) + "+\\s*$");
      let j = i + 1; const buf = [];
      while (j < lines.length && !close.test(lines[j])) buf.push(lines[j++]);
      const lang = fence[3] ? `<span class="lang">${escapeHtml(fence[3])}</span>` : "";
      html += `<pre>${lang}<code>${escapeHtml(buf.join("\n"))}</code></pre>\n`;
      i = j + 1; continue;
    }

    const head = line.match(headRe);
    if (head) {
      const level = head[1].length, text = inline(head[2]);
      const id = slugify(head[2]);
      if (level <= 3) headings.push({ level, text: head[2], id });
      html += `<h${level} id="${id}">${text}</h${level}>\n`;
      i++; continue;
    }

    if (/^\s*\[\[_TOC_\]\]\s*$/i.test(line)) { html += '<div class="toc-inline" data-toc></div>\n'; i++; continue; }
    if (hrRe.test(line)) { html += "<hr>\n"; i++; continue; }

    if (/^\s*>/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) buf.push(lines[i++].replace(/^\s*> ?/, ""));
      html += `<blockquote>${renderBlocks(buf.join("\n"))}</blockquote>\n`;
      continue;
    }

    if (line.includes("|") && i + 1 < lines.length && tableSepRe.test(lines[i + 1]) && lines[i + 1].includes("|")) {
      const cells = l => {
        l = l.replace(/\\\|/g, "\x01").trim().replace(/^\||\|$/g, "");
        return l.split("|").map(c => c.replace(/\x01/g, "|").trim());
      };
      const headCells = cells(line);
      const aligns = cells(lines[i + 1]).map(s =>
        /^:-+:$/.test(s) ? "center" : /^-+:$/.test(s) ? "right" : /^:/.test(s) ? "left" : "");
      let t = "<table><thead><tr>" + headCells.map((c, k) =>
        `<th${aligns[k] ? ` style="text-align:${aligns[k]}"` : ""}>${inline(c)}</th>`).join("") + "</tr></thead><tbody>";
      i += 2;
      while (i < lines.length && lines[i].includes("|") && !isBlank(lines[i])) {
        t += "<tr>" + cells(lines[i]).map((c, k) =>
          `<td${aligns[k] ? ` style="text-align:${aligns[k]}"` : ""}>${inline(c)}</td>`).join("") + "</tr>";
        i++;
      }
      html += t + "</tbody></table>\n"; continue;
    }

    const list = line.match(listRe);
    if (list) { const r = renderList(lines, i, list[1].length); html += r.html; i = r.next; continue; }

    if (htmlBlockRe.test(line) && !/<script/i.test(line)) {
      const buf = [];
      while (i < lines.length && !isBlank(lines[i])) buf.push(lines[i++]);
      html += buf.join("\n").replace(/<script/gi, "&lt;script") + "\n";
      continue;
    }

    const buf = [];
    while (i < lines.length && !isBlank(lines[i]) && !lines[i].match(headRe) && !lines[i].match(fenceRe)
           && !hrRe.test(lines[i]) && !/^\s*>/.test(lines[i]) && !lines[i].match(listRe)) {
      buf.push(lines[i++]);
    }
    html += `<p>${inline(buf.join("\n"))}</p>\n`;
  }
  return html;

  function renderList(lines, start, indent) {
    const itemRe = /^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$/;
    const first = lines[start].match(itemRe);
    const ordered = /\d/.test(first[2]);
    const startNum = ordered ? parseInt(first[2], 10) : 1;
    let html = ordered ? `<ol${startNum !== 1 ? ` start="${startNum}"` : ""}>` : "<ul>";
    let i = start;
    while (i < lines.length) {
      const m = lines[i].match(itemRe);
      if (!m || m[1].length > indent + 2) break;      // deeper = handled as content
      if (m[1].length < indent - 1) break;             // shallower = parent's problem
      const contentCol = m[1].length + m[2].length + 1;
      const buf = [m[3]];
      i++;
      while (i < lines.length) {
        const l = lines[i];
        if (isBlank(l)) {
          if (i + 1 < lines.length && /^\s+/.test(lines[i + 1]) &&
              (lines[i + 1].match(/^\s*/)[0].length >= contentCol || lines[i + 1].match(itemRe))) {
            buf.push(""); i++; continue;
          }
          break;
        }
        const ind = l.match(/^\s*/)[0].length;
        const im = l.match(itemRe);
        if (im && ind <= indent + 1) break;            // sibling or parent item
        if (ind >= contentCol || im) { buf.push(l.slice(Math.min(contentCol, ind))); i++; continue; }
        buf.push(l.trim()); i++;                        // lazy continuation
      }
      let inner = renderBlocks(buf.join("\n")).trim();
      const single = inner.match(/^<p>([\s\S]*)<\/p>$/);
      if (single && !single[1].includes("<p>")) inner = single[1];
      const task = inner.match(/^\[([ xX])\]\s+([\s\S]*)$/);
      if (task) {
        html += `<li class="task"><input type="checkbox" disabled${task[1] !== " " ? " checked" : ""}>${task[2]}</li>`;
      } else {
        html += `<li>${inner}</li>`;
      }
      while (i < lines.length && isBlank(lines[i]) &&
             i + 1 < lines.length && lines[i + 1].match(itemRe)) i++;
    }
    return { html: html + (ordered ? "</ol>" : "</ul>") + "\n", next: i };
  }
}

/* ---------------- boot ---------------- */
let md = document.getElementById("kg-md").textContent;
md = md.replace(/<\\\//g, "</");                        // undo build-time escaping
if (md.startsWith("---")) {                             // strip YAML front matter
  const end = md.indexOf("\n---", 3);
  if (end > 0 && end < 2500) md = md.slice(md.indexOf("\n", end + 1) + 1);
}

const mount = document.getElementById("kg-content");
if (IS_PLAIN) {
  mount.innerHTML = `<pre class="plain">${escapeHtml(md)}</pre>`;
} else {
  mount.innerHTML = renderBlocks(md);
}

// inline + floating TOC
const tocEntries = headings.filter(h => h.level >= 1 && h.level <= 3);
const tocHtml = tocEntries.map(h =>
  `<a class="h${h.level}" href="#${h.id}">${escapeHtml(h.text.replace(/[`*_~]/g, ""))}</a>`).join("");
document.querySelectorAll("[data-toc]").forEach(el => {
  el.innerHTML = '<div class="toc-title">Contents</div>' +
    "<ul>" + tocEntries.map(h => `<li class="h${h.level}"><a href="#${h.id}">${escapeHtml(h.text.replace(/[`*_~]/g, ""))}</a></li>`).join("") + "</ul>";
});
const sideToc = document.querySelector("nav.toc");
if (sideToc && tocEntries.length >= 4) {
  sideToc.innerHTML = '<div class="toc-title">On this page</div>' + tocHtml;
  sideToc.hidden = false;
}

// theme toggle (shared key with the map viewer)
const btnTheme = document.getElementById("btn-theme");
if (btnTheme) {
  const THEMES = ["auto", "light", "dark"], ICONS = { auto: "◐", light: "☀", dark: "☾" };
  let idx = Math.max(0, THEMES.indexOf(localStorage.getItem("kg-theme") || "auto"));
  const apply = () => {
    const t = THEMES[idx];
    if (t === "auto") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", t);
    btnTheme.textContent = ICONS[t];
    localStorage.setItem("kg-theme", t);
  };
  btnTheme.addEventListener("click", () => { idx = (idx + 1) % 3; apply(); });
  apply();
}
})();
