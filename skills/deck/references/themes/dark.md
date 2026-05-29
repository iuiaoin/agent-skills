# Theme: dark

Mysterious, elegant dark mode — near-black canvas, off-white text, violet→cyan accents with soft glow.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #0E0E10;
  --slide-bg-rgb: 14,14,16;
  --surface: #1A1A1F;
  --border: #2A2A30;

  --text-primary: #F5F5F7;
  --text-secondary: #A9A9B2;
  --text-strong: #FFFFFF;

  --accent: #8B5CF6;
  --accent-rgb: 139,92,246;
  --accent-2: #22D3EE;
  --accent-2-rgb: 34,211,238;
  --heading-gradient: linear-gradient(90deg, #8B5CF6, #22D3EE);

  --ok: #34D399;
  --warn: #FBBF24;
  --muted: #6B7280;

  --font-heading: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-body: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-code: 'JetBrains Mono', 'Source Code Pro', ui-monospace, Menlo, monospace;

  --card-radius: 12px;
  --shadow: 0 0 40px rgba(139,92,246,0.25);
}
```

## Font setup (paste above `:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
```

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #1A1A1F;
  --light-bg: #08080A;
  --dark-bg: #0E0E10;
  --text-color: #F5F5F7;
  --secondary-text: #A9A9B2;
  --border-color: #2A2A30;
  --hover-color: #232329;
  --active-color: #8B5CF6;
  --card-radius: 12px;
  --btn-radius: 8px;
}
```

## Decorative guidance

- Glow, not drop-shadow: cards/code use the violet glow `--shadow`. Cover shapes are low-opacity violet & cyan radials (`rgba(var(--accent-rgb),0.18)`, `rgba(var(--accent-2-rgb),0.12)`).
- Headings can use the violet→cyan `--heading-gradient` (clipped text) for a luminous look; keep body text off-white `--text-secondary` for comfort.
- Surfaces `#1A1A1F` sit subtly above the `#0E0E10` canvas; 1px `#2A2A30` borders.
- **Contrast check:** the comparison-table header row renders as a light band (`--text-primary` bg, `--slide-bg` text) on the dark slide — that's intended and legible. Keep accents bright enough against the dark canvas.
