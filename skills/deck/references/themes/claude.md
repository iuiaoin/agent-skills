# Theme: claude

Warm, restrained Claude.com style — beige canvas, coral accent, mint secondary. The default theme; calm and editorial.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #F7F4EF;
  --slide-bg-rgb: 247,244,239;
  --surface: #FBF8F5;
  --border: #EAE0D9;

  --text-primary: #2B2A27;
  --text-secondary: #5D4E42;
  --text-strong: #4A3F35;

  --accent: #E07A59;
  --accent-rgb: 224,122,89;
  --accent-2: #9FD3B8;
  --accent-2-rgb: 159,211,184;
  --heading-gradient: linear-gradient(90deg, #E07A59, #A0816A);

  --ok: #4CAF50;
  --warn: #E07A59;
  --muted: #9E9086;

  --font-heading: 'Inter', 'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', sans-serif;
  --font-body: 'Inter', 'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', sans-serif;
  --font-code: 'Source Code Pro', ui-monospace, Menlo, Consolas, monospace;

  --card-radius: 12px;
  --shadow: 0 4px 12px rgba(0,0,0,0.05);
}
```

## Font setup (paste above `:root`)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Code+Pro:wght@400;500&display=swap');
```

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FBF8F5;
  --light-bg: #F7F4EF;
  --dark-bg: #2B2A27;
  --text-color: #2B2A27;
  --secondary-text: #5D4E42;
  --border-color: #EAE0D9;
  --hover-color: #EFEAE3;
  --active-color: #E07A59;
  --card-radius: 12px;
  --btn-radius: 8px;
}
```

## Decorative guidance

- Warm and restrained — **no high-saturation neon**. Coral `--accent` for bars/icons/key data; mint `--accent-2` for secondary highlights.
- Cover: two soft radial accent shapes (`rgba(var(--accent-rgb),0.15)`, `rgba(var(--accent-2-rgb),0.1)`).
- Cards: 12px radius, subtle shadow. Bullet markers: 12×28px coral bars or coral dots.
- This is the baseline look — keep it calm and editorial.
