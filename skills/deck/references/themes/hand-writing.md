# Theme: hand-writing

Hand-drawn sketchnote style — cream paper, handwriting fonts, **sketchy borders via [rough.js](https://github.com/rough-stuff/rough)** and **highlight/underline/circle annotations via [rough-notation](https://github.com/rough-stuff/rough-notation)**. Highly distinctive, playful, human.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #FFFEF8;
  --slide-bg-rgb: 255,254,248;
  --surface: #FFFDF5;
  --border: #2B2B2B;

  --text-primary: #2B2B2B;
  --text-secondary: #555555;
  --text-strong: #000000;

  --accent: #E63946;
  --accent-rgb: 230,57,70;
  --accent-2: #F4A261;
  --accent-2-rgb: 244,162,97;
  --heading-gradient: linear-gradient(90deg, #E63946, #E63946);

  --ok: #2A9D8F;
  --warn: #E63946;
  --muted: #9E9E9E;

  --font-heading: 'Caveat', 'Kalam', cursive;
  --font-body: 'Kalam', 'Caveat', cursive;
  --font-code: 'Cascadia Code', Consolas, monospace;

  --card-radius: 6px;
  --shadow: none;
}
```

## Font setup (paste above `:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Kalam:wght@300;400;700&display=swap');
```

## Special setup (required) — rough.js + rough-notation

Add these two scripts at the **end of `<body>`** of every slide, followed by the init script. The init runs on `load`, draws a sketchy border behind every `.sketch` element, and applies rough-notation annotations to every `[data-annotate]` element.

```html
<script src="https://unpkg.com/roughjs@4.6.6/bundled/rough.js"></script>
<script src="https://unpkg.com/rough-notation@0.5.1/lib/rough-notation.iife.js"></script>
<script>
  window.addEventListener('load', () => {
    // 1) Sketchy hand-drawn borders behind any .sketch box (cards, code blocks, the slide frame…)
    document.querySelectorAll('.sketch').forEach(el => {
      const r = el.getBoundingClientRect();
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('width', r.width);
      svg.setAttribute('height', r.height);
      svg.style.cssText = 'position:absolute;top:0;left:0;pointer-events:none;z-index:0;overflow:visible;';
      const rc = rough.svg(svg);
      svg.appendChild(rc.rectangle(3, 3, r.width - 6, r.height - 6, {
        roughness: 1.8, bowing: 1.5, stroke: '#2B2B2B', strokeWidth: 2.5, fill: 'none'
      }));
      if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
      el.insertBefore(svg, el.firstChild);
      [...el.children].forEach(c => { if (c !== svg) c.style.position = c.style.position || 'relative'; });
    });
    // 2) Annotations: mark text with data-annotate="underline|circle|highlight|box|strike-through"
    //    optional data-color="#E63946". animate:false is REQUIRED so the QA screenshot captures it.
    document.querySelectorAll('[data-annotate]').forEach(el => {
      RoughNotation.annotate(el, {
        type: el.dataset.annotate,
        color: el.dataset.color || '#E63946',
        animate: false, strokeWidth: 2.5, padding: 5, multiline: true
      }).show();
    });
  });
</script>
```

Usage in slide markup:
- Add `class="sketch"` to any card / code block / callout (and optionally the `.slide` itself) for a wobbly hand-drawn border.
- Wrap key words in `<span data-annotate="underline">…</span>` (or `circle`, `highlight`, `box`). Use `data-color="#F4A261"` for the highlighter look.

**CDN note:** these load from unpkg (consistent with the deck's CDN web-fonts). They run during the Puppeteer QA/export render and complete well within the 2.5s wait because `animate:false`.

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FFFEF8;
  --light-bg: #FBF7EC;
  --dark-bg: #2B2B2B;
  --text-color: #2B2B2B;
  --secondary-text: #555555;
  --border-color: #2B2B2B;
  --hover-color: #F3EEDF;
  --active-color: #E63946;
  --card-radius: 6px;
  --btn-radius: 6px;
}
```

## Decorative guidance

- Cream paper canvas; ink `#2B2B2B` text. **Bump font sizes ~15-20%** — Caveat/Kalam render smaller than sans fonts (headings 64-84px, body 22-28px).
- Borders are drawn by rough.js (`.sketch`), not CSS — leave CSS borders off on sketched boxes. Don't over-annotate: 1-2 rough-notation marks per slide for emphasis.
- Bullets: use `circle`/`underline` annotations or hand-drawn `✓`/`→` glyphs. Red `--accent` for emphasis, orange `--accent-2` as highlighter. Keep it loose and friendly.
