# Theme: classic

Clean, elegant white-on-black editorial. Monochrome, generous whitespace, thin rules, no decorative noise. Lets the content speak.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #FFFFFF;
  --slide-bg-rgb: 255,255,255;
  --surface: #F5F5F5;
  --border: #E0E0E0;

  --text-primary: #111111;
  --text-secondary: #555555;
  --text-strong: #000000;

  --accent: #111111;
  --accent-rgb: 17,17,17;
  --accent-2: #888888;
  --accent-2-rgb: 136,136,136;
  --heading-gradient: linear-gradient(90deg, #111111, #111111);

  --ok: #2E7D32;
  --warn: #B26A00;
  --muted: #9E9E9E;

  --font-heading: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-body: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-code: 'SF Mono', SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;

  --card-radius: 4px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08);
}
```

## Font setup

System font stack — **no `@import` needed**. (Helvetica/Arial on every platform.)

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FFFFFF;
  --light-bg: #FFFFFF;
  --dark-bg: #111111;
  --text-color: #111111;
  --secondary-text: #555555;
  --border-color: #E0E0E0;
  --hover-color: #F0F0F0;
  --active-color: #111111;
  --card-radius: 4px;
  --btn-radius: 4px;
}
```

## Decorative guidance

- **No decorative background shapes.** Omit the cover's `.accent-shape` elements (or set them transparent). The aesthetic is restraint.
- Monochrome: accent is near-black `#111`. Bullet bars/dots are black; headings solid black (gradient resolves to flat black).
- Thin 1px `#E0E0E0` rules to separate sections; 4px radius; whisper-soft shadows.
- Lean on **whitespace and typographic hierarchy** (size/weight) rather than color for emphasis.
