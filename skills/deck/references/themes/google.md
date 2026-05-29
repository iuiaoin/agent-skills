# Theme: google

Google rainbow — white canvas, Roboto, the four Google colors (blue/red/yellow/green), Material elevation. Bright, friendly, playful.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #FFFFFF;
  --slide-bg-rgb: 255,255,255;
  --surface: #F8F9FA;
  --border: #DADCE0;

  --text-primary: #202124;
  --text-secondary: #5F6368;
  --text-strong: #202124;

  --accent: #4285F4;
  --accent-rgb: 66,133,244;
  --accent-2: #EA4335;
  --accent-2-rgb: 234,67,53;
  --heading-gradient: linear-gradient(90deg, #4285F4, #EA4335, #FBBC05, #34A853);

  --ok: #34A853;
  --warn: #FBBC05;
  --muted: #5F6368;

  /* extra Google palette for rainbow accents */
  --g-blue: #4285F4;
  --g-red: #EA4335;
  --g-yellow: #FBBC05;
  --g-green: #34A853;

  --font-heading: 'Roboto', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-body: 'Roboto', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-code: 'Roboto Mono', ui-monospace, Menlo, Consolas, monospace;

  --card-radius: 8px;
  --shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
}
```

## Font setup (paste above `:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap');
```

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FFFFFF;
  --light-bg: #F8F9FA;
  --dark-bg: #202124;
  --text-color: #202124;
  --secondary-text: #5F6368;
  --border-color: #DADCE0;
  --hover-color: #F1F3F4;
  --active-color: #4285F4;
  --card-radius: 8px;
  --btn-radius: 8px;
}
```

## Decorative guidance

- **Rainbow heading**: the cover `h2` (clipped-text `--heading-gradient`) sweeps blue→red→yellow→green. Use it sparingly for hero headings; section titles can be solid `#202124`.
- **Multi-color accents**: cycle bullet markers / agenda bars / icon chips through `--g-blue`, `--g-red`, `--g-yellow`, `--g-green` (e.g. `li:nth-child(1)::before{background:var(--g-blue)} (2){--g-red} (3){--g-yellow} (4){--g-green}`).
- Material elevation shadows (`--shadow`), 8px radius, `#F8F9FA` surfaces. Clean white, lots of light. Friendly and rounded.
