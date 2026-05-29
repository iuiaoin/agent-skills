# Theme: microsoft

Modern Microsoft **Fluent** — clean white, Segoe UI, communication blue `#0078D4`, subtle depth. Crisp, professional, contemporary Microsoft 365 look.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #FFFFFF;
  --slide-bg-rgb: 255,255,255;
  --surface: #F3F2F1;
  --border: #EDEBE9;

  --text-primary: #201F1E;
  --text-secondary: #605E5C;
  --text-strong: #000000;

  --accent: #0078D4;
  --accent-rgb: 0,120,212;
  --accent-2: #2B88D8;
  --accent-2-rgb: 43,136,216;
  --heading-gradient: linear-gradient(90deg, #0078D4, #2B88D8);

  --ok: #107C10;
  --warn: #D83B01;
  --muted: #A19F9D;

  --font-heading: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-body: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-code: 'Cascadia Code', 'Cascadia Mono', Consolas, ui-monospace, monospace;

  --card-radius: 4px;
  --shadow: 0 1.6px 3.6px rgba(0,0,0,0.13), 0 0.3px 0.9px rgba(0,0,0,0.11);
}
```

## Font setup

Segoe UI system stack — **no `@import` needed** (native on Windows; graceful fallback elsewhere).

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FFFFFF;
  --light-bg: #FAF9F8;
  --dark-bg: #0078D4;
  --text-color: #201F1E;
  --secondary-text: #605E5C;
  --border-color: #EDEBE9;
  --hover-color: #F3F2F1;
  --active-color: #0078D4;
  --card-radius: 4px;
  --btn-radius: 4px;
}
```

## Decorative guidance

- **Fluent depth**: layered neutral surfaces (`#F3F2F1`) with the soft two-part depth `--shadow`; small 4px radius (Fluent uses 2-4px).
- Communication blue `#0078D4` for primary actions, links, key data, bullet bars; the cover heading uses the blue `--heading-gradient`.
- Clean and rectilinear — minimal radial shapes; favor crisp cards and a tidy grid. Optional thin top accent bar in `--accent` on content slides.
