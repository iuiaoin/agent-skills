# Theme: artist

Movie-poster drama — near-black canvas, oversized uppercase display type, clashing electric accents (hot magenta + electric yellow), bold full-bleed gradients. Exaggerated, daring color that grabs the eye.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #0A0A0A;
  --slide-bg-rgb: 10,10,10;
  --surface: rgba(255,255,255,0.06);
  --border: rgba(255,255,255,0.16);

  --text-primary: #FFFFFF;
  --text-secondary: #C9C9D2;
  --text-strong: #FFFFFF;

  --accent: #FF2E63;
  --accent-rgb: 255,46,99;
  --accent-2: #FFD300;
  --accent-2-rgb: 255,211,0;
  --heading-gradient: linear-gradient(135deg, #FF2E63 0%, #FFD300 100%);

  --ok: #06FFA5;
  --warn: #FFD300;
  --muted: #8A8A95;

  --font-heading: 'Anton', 'Bebas Neue', Impact, 'PingFang SC', sans-serif;
  --font-body: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-code: 'Space Mono', ui-monospace, Menlo, monospace;

  --card-radius: 4px;
  --shadow: 0 10px 40px rgba(255,46,99,0.35);
}
```

## Font setup (paste above `:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Inter:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap');
```

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #14121A;
  --light-bg: #050505;
  --dark-bg: #0A0A0A;
  --text-color: #FFFFFF;
  --secondary-text: #C9C9D2;
  --border-color: rgba(255,255,255,0.14);
  --hover-color: #1E1B26;
  --active-color: #FF2E63;
  --card-radius: 4px;
  --btn-radius: 4px;
}
```

## Decorative guidance

- **Oversized, uppercase headings**: `font-family: var(--font-heading)`, `text-transform: uppercase`, tight `letter-spacing: -1px`, line-height ~0.95. Cover/section titles 96-130px; let them dominate the frame.
- **Full-bleed gradient drama** on hero/section slides — layer bold gradients over the canvas, e.g.:
  ```css
  .slide { background:
    radial-gradient(circle at 25% 15%, rgba(255,46,99,0.30), transparent 55%),
    radial-gradient(circle at 85% 90%, rgba(255,211,0,0.20), transparent 55%),
    var(--slide-bg); }
  ```
- Headline gradient text (`--heading-gradient`, clipped) for the poster title; add a glow `text-shadow: 0 0 30px rgba(var(--accent-rgb),0.5)` for punch.
- Translucent `--surface` cards with thin light `--border`, dramatic magenta `--shadow`; sharp 4px corners. High contrast white text on black. Use accent diagonals/bars boldly. Eye-catching over subtle — every slide should feel like a poster.
- **Contrast check:** the comparison-table header row is a light band (`--text-primary` bg / `--slide-bg` text) on black — intended; ensure body rows stay readable in `--text-secondary`.
