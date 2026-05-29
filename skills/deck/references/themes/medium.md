# Theme: medium

Medium.com reading style — serif typography (bundled **Source Serif Pro**), white canvas, signature green, generous whitespace. Calm, literary, long-form feel.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #FFFFFF;
  --slide-bg-rgb: 255,255,255;
  --surface: #FAFAFA;
  --border: #E6E6E6;

  --text-primary: #242424;
  --text-secondary: #6B6B6B;
  --text-strong: #000000;

  --accent: #1A8917;
  --accent-rgb: 26,137,23;
  --accent-2: #0F730C;
  --accent-2-rgb: 15,115,12;
  --heading-gradient: linear-gradient(90deg, #1A8917, #1A8917);

  --ok: #1A8917;
  --warn: #C9700A;
  --muted: #B3B3B3;

  --font-heading: 'Source Serif Pro', Georgia, 'Times New Roman', 'Songti SC', serif;
  --font-body: 'Source Serif Pro', Georgia, 'Times New Roman', 'Songti SC', serif;
  --font-code: 'SFMono-Regular', Menlo, Consolas, monospace;

  --card-radius: 4px;
  --shadow: 0 1px 4px rgba(0,0,0,0.06);
}
```

## Font setup (paste above `:root`) — uses the **bundled** Source Serif Pro

```css
@font-face { font-family: 'Source Serif Pro'; font-weight: 400; font-style: normal;
  src: url('../assets/fonts/source-serif-pro-400-normal.woff') format('woff'); font-display: swap; }
@font-face { font-family: 'Source Serif Pro'; font-weight: 400; font-style: italic;
  src: url('../assets/fonts/source-serif-pro-400-italic.woff') format('woff'); font-display: swap; }
@font-face { font-family: 'Source Serif Pro'; font-weight: 700; font-style: normal;
  src: url('../assets/fonts/source-serif-pro-700-normal.woff') format('woff'); font-display: swap; }
@font-face { font-family: 'Source Serif Pro'; font-weight: 700; font-style: italic;
  src: url('../assets/fonts/source-serif-pro-700-italic.woff') format('woff'); font-display: swap; }
```

## Special setup (required)

Copy the four font files from the skill into the deck before/while generating slides, so the relative `../assets/fonts/...` URLs resolve (works in the browser **and** under the Puppeteer `file://` render):

```
<skill>/assets/fonts/source-serif-pro-400-normal.woff  →  presentation/assets/fonts/source-serif-pro-400-normal.woff
<skill>/assets/fonts/source-serif-pro-400-italic.woff  →  presentation/assets/fonts/source-serif-pro-400-italic.woff
<skill>/assets/fonts/source-serif-pro-700-normal.woff  →  presentation/assets/fonts/source-serif-pro-700-normal.woff
<skill>/assets/fonts/source-serif-pro-700-italic.woff  →  presentation/assets/fonts/source-serif-pro-700-italic.woff
```

(`slides/slideN.html` → `../assets/fonts/` resolves to `presentation/assets/fonts/`.)

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FFFFFF;
  --light-bg: #FFFFFF;
  --dark-bg: #242424;
  --text-color: #242424;
  --secondary-text: #6B6B6B;
  --border-color: #E6E6E6;
  --hover-color: #F2F2F2;
  --active-color: #1A8917;
  --card-radius: 4px;
  --btn-radius: 4px;
}
```

## Decorative guidance

- **Serif everything** — headings and body in Source Serif Pro. Larger, comfortable line-height (1.6-1.8); plenty of whitespace.
- Restrained color: green `--accent` for links, key numbers, and bullet markers only. Links: green, underlined.
- Minimal shadows, hairline `#E6E6E6` dividers, 4px radius. No flashy shapes — it should read like a well-typeset article.
