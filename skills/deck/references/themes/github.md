# Theme: github

GitHub light style — white canvas, GitHub blue accent, hairline `#D0D7DE` borders, system UI font, monospace-forward. Reads like developer documentation.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #FFFFFF;
  --slide-bg-rgb: 255,255,255;
  --surface: #F6F8FA;
  --border: #D0D7DE;

  --text-primary: #1F2328;
  --text-secondary: #656D76;
  --text-strong: #1F2328;

  --accent: #0969DA;
  --accent-rgb: 9,105,218;
  --accent-2: #1A7F37;
  --accent-2-rgb: 26,127,55;
  --heading-gradient: linear-gradient(90deg, #0969DA, #0969DA);

  --ok: #1A7F37;
  --warn: #9A6700;
  --muted: #656D76;

  --font-heading: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-code: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace;

  --card-radius: 6px;
  --shadow: 0 1px 0 rgba(31,35,40,0.04);
}
```

## Font setup

GitHub's system UI stack — **no `@import` needed**.

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FFFFFF;
  --light-bg: #F6F8FA;
  --dark-bg: #24292F;
  --text-color: #1F2328;
  --secondary-text: #656D76;
  --border-color: #D0D7DE;
  --hover-color: #EAEEF2;
  --active-color: #0969DA;
  --card-radius: 6px;
  --btn-radius: 6px;
}
```

## Decorative guidance

- **Border-led, not shadow-led**: 1px `#D0D7DE` borders on cards, tables, code blocks; 6px radius; near-flat shadows.
- Code blocks use the `#F6F8FA` surface with a `#D0D7DE` border — the canonical GitHub code box. Lean into code/monospace.
- Blue `--accent` for links and primary emphasis; green `--accent-2` for "added/success". Bullet markers: small blue squares or `▸` chevrons.
- Skip soft radial shapes; keep it crisp and documentation-like.
