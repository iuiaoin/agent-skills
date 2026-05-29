# Theme: twitter

Classic blue-bird Twitter — white canvas, the iconic `#1DA1F2` blue, Helvetica Neue, rounded "tweet card" shapes, light-blue surfaces. Friendly and social.

## :root (paste into every slide's `<style>`)

```css
:root {
  --slide-bg: #FFFFFF;
  --slide-bg-rgb: 255,255,255;
  --surface: #F5F8FA;
  --border: #E1E8ED;

  --text-primary: #14171A;
  --text-secondary: #657786;
  --text-strong: #14171A;

  --accent: #1DA1F2;
  --accent-rgb: 29,161,242;
  --accent-2: #17BF63;
  --accent-2-rgb: 23,191,99;
  --heading-gradient: linear-gradient(90deg, #1DA1F2, #1DA1F2);

  --ok: #17BF63;
  --warn: #E0245E;
  --muted: #AAB8C2;

  --font-heading: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-body: 'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  --font-code: Menlo, Consolas, 'Liberation Mono', monospace;

  --card-radius: 14px;
  --shadow: 0 1px 3px rgba(20,23,26,0.1);
}
```

## Font setup

Helvetica Neue system stack — **no `@import` needed**.

## Viewer overrides (for `{{VIEWER_THEME}}` in index.html)

```css
:root {
  --bg-color: #FFFFFF;
  --light-bg: #E8F5FE;
  --dark-bg: #1DA1F2;
  --text-color: #14171A;
  --secondary-text: #657786;
  --border-color: #E1E8ED;
  --hover-color: #F5F8FA;
  --active-color: #1DA1F2;
  --card-radius: 14px;
  --btn-radius: 9999px;
}
```

## Decorative guidance

- **Rounded everything** — `--card-radius` is a generous 14px (tweet-card feel); pill-shaped buttons/badges (`border-radius: 9999px`).
- Bird-blue `#1DA1F2` dominates: accent bars/dots, links, key data, icon circles. Light-blue `#F5F8FA` / `#E8F5FE` surfaces for cards and callouts.
- Soft, low shadows; friendly and airy. Green `--accent-2` for positive metrics, `#E0245E` (`--warn`) for alerts. Round avatar-style chips work well for people/quotes.
