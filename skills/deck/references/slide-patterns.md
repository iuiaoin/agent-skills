# Slide HTML Patterns

Each slide is a standalone HTML file at 1280x720. Below are patterns for common slide types.

**Theming:** these patterns reference the [Theme Token Contract](design-system.md#theme-token-contract) via `var(--…)` instead of hardcoded colors. To theme a deck, paste the selected theme's `:root{}` block **and** its font setup (from `themes/<name>.md`) at the top of each slide's `<style>` — the patterns below then inherit the theme automatically. Some themes add their own decorative rules (shapes, borders, annotations) on top; follow the theme file.

## Table of Contents

1. [Base Structure](#base-structure)
2. [Cover Slide](#cover-slide)
3. [Agenda / List Slide](#agenda--list-slide)
4. [Content with Feature Grid](#content-with-feature-grid)
5. [Two-Column with Image](#two-column-with-image)
6. [Two-Column Code + Info](#two-column-code--info)
7. [Comparison Table](#comparison-table)
8. [Closing / Q&A Slide](#closing--qa-slide)

---

## Base Structure

Every slide HTML follows this skeleton. The theme's `:root{}` + font setup goes at the very top of `<style>`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide Title</title>
  <style>
    /* ── Paste selected theme :root{} block + font setup (@import / @font-face) here ── */

    body {
      margin: 0; padding: 0; width: 100vw; height: 100vh;
      display: flex; justify-content: center; align-items: center;
      background-color: var(--slide-bg);
      font-family: var(--font-body);
    }
    html, body {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
    html::-webkit-scrollbar,
    body::-webkit-scrollbar {
      display: none;
    }
    .slide {
      width: 1280px; height: 720px;
      background-color: var(--slide-bg);
      position: relative; overflow: hidden;
      box-sizing: border-box;
    }
    /* Fade-in animation */
    @keyframes fadeInContent {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <div class="slide">
    <!-- slide content here -->
  </div>
</body>
</html>
```

---

## Cover Slide

Centered title with gradient accent, decorative background shapes, footer with presenter/date.

```html
<style>
  .slide {
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; text-align: center;
  }
  .slide-content {
    z-index: 2; padding: 40px;
    animation: fadeInContent 1.2s ease-in-out forwards; opacity: 0;
  }
  h1 { font-family: var(--font-heading); font-size: 72px; font-weight: 700; color: var(--text-primary); margin: 0 0 20px; letter-spacing: -1px; }
  h2 {
    font-family: var(--font-heading); font-size: 48px; font-weight: 600; margin: 0 0 25px;
    background: var(--heading-gradient);
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  p.tagline { font-size: 24px; color: var(--text-secondary); margin: 0; max-width: 800px; line-height: 1.5; }
  .footer {
    position: absolute; bottom: 40px; left: 60px; right: 60px;
    display: flex; justify-content: space-between; align-items: center; z-index: 2;
    animation: fadeInContent 1.2s ease-in-out 0.2s forwards; opacity: 0;
  }
  .presenter { font-size: 18px; font-weight: 600; color: var(--text-primary); }
  .date { font-size: 18px; color: var(--text-secondary); }
  /* Decorative shapes */
  .accent-shape { position: absolute; border-radius: 50%; opacity: 0; animation: fadeInShape 2s ease-out forwards; }
  @keyframes fadeInShape { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
  .shape1 { width: 300px; height: 300px; background: radial-gradient(circle, rgba(var(--accent-rgb),0.15) 0%, transparent 70%); top: -100px; left: -100px; }
  .shape2 { width: 400px; height: 400px; background: radial-gradient(circle, rgba(var(--accent-2-rgb),0.1) 0%, transparent 70%); bottom: -150px; right: -150px; }
</style>
<div class="slide">
  <div class="accent-shape shape1"></div>
  <div class="accent-shape shape2"></div>
  <div class="slide-content">
    <h2>Deck Title</h2>
    <p class="tagline">Subtitle or tagline</p>
  </div>
  <div class="footer">
    <div class="presenter">Presenter Name</div>
    <div class="date">Date</div>
  </div>
</div>
```

---

## Agenda / List Slide

Large title + vertical list with accent-colored left bar markers and staggered animation.

```html
<style>
  .slide { display: flex; flex-direction: column; justify-content: center; padding: 90px 120px; }
  h1 { font-family: var(--font-heading); color: var(--text-primary); font-size: 64px; font-weight: 700; margin: 0 0 60px; animation: slideInUp 0.6s ease-out; }
  ul { list-style: none; padding: 0; margin: 0; }
  li {
    color: var(--text-secondary); font-size: 30px; line-height: 1.6; margin-bottom: 24px;
    padding-left: 55px; position: relative;
    opacity: 0; animation: slideInUp 0.5s ease-out forwards;
  }
  li:nth-child(1) { animation-delay: 0.2s; }
  li:nth-child(2) { animation-delay: 0.3s; }
  li:nth-child(3) { animation-delay: 0.4s; }
  li:nth-child(4) { animation-delay: 0.5s; }
  li:nth-child(5) { animation-delay: 0.6s; }
  li::before {
    content: ''; position: absolute; left: 0; top: 50%; transform: translateY(-50%);
    width: 12px; height: 28px; background-color: var(--accent); border-radius: 4px;
  }
</style>
<div class="slide">
  <h1>Agenda</h1>
  <ul>
    <li>Topic One</li>
    <li>Topic Two</li>
    <li>Topic Three</li>
  </ul>
</div>
```

---

## Content with Feature Grid

Title + 2-column grid of features with emoji icons and bold labels.

```html
<style>
  .slide { display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 60px 80px; }
  .slide-content { width: 100%; opacity: 0; animation: fadeInContent 0.8s 0.2s ease-out forwards; }
  .title { font-family: var(--font-heading); font-size: 50px; font-weight: 700; color: var(--text-primary); text-align: center; margin: 0 0 25px; }
  .mission { font-size: 26px; color: var(--accent); text-align: center; margin: 0 auto 60px; max-width: 85%; font-weight: 700; }
  .features-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px 60px; list-style: none; padding: 0; margin: 0; }
  .feature-item {
    display: flex; align-items: flex-start; color: var(--text-secondary); font-size: 20px; line-height: 1.6;
    opacity: 0; animation: fadeInContent 0.6s ease-out forwards;
  }
  .feature-item:nth-child(1) { animation-delay: 0.5s; }
  .feature-item:nth-child(2) { animation-delay: 0.6s; }
  .feature-item:nth-child(3) { animation-delay: 0.7s; }
  .feature-item:nth-child(4) { animation-delay: 0.8s; }
  .feature-item::before { content: '\2022'; color: var(--accent); font-size: 32px; margin-right: 15px; flex-shrink: 0; }
  .feature-item strong { color: var(--text-primary); font-weight: 700; }
</style>
```

---

## Two-Column with Image

Title + side-by-side image and text list. Good for architecture diagrams.

```html
<style>
  .slide { display: flex; flex-direction: column; padding: 60px; }
  h1 { font-family: var(--font-heading); color: var(--text-primary); font-size: 52px; font-weight: 700; margin: 0 0 35px; text-align: center; }
  .content-container { display: flex; flex: 1; gap: 40px; align-items: center; }
  .image-section { flex: 1; display: flex; justify-content: center; align-items: center; }
  .image-section img { max-width: 100%; max-height: 450px; object-fit: contain; border-radius: var(--card-radius); box-shadow: var(--shadow); }
  .text-section { flex: 1; }
  .layers-list { list-style: none; padding: 0; counter-reset: layer-counter; }
  .layers-list li { color: var(--text-secondary); font-size: 19px; line-height: 1.6; display: flex; margin-bottom: 12px; }
  .layers-list li::before { content: counter(layer-counter); counter-increment: layer-counter; color: var(--accent); font-weight: 700; font-size: 20px; margin-right: 12px; min-width: 22px; }
  .layers-list strong { color: var(--text-strong); font-weight: 600; margin-right: 8px; }
</style>
```

---

## Two-Column Code + Info

Side-by-side code example and info/config panel. Good for technical demos.

```html
<style>
  .slide { display: flex; flex-direction: column; padding: 60px 80px; }
  h1 { font-family: var(--font-heading); font-size: 52px; color: var(--text-primary); text-align: center; margin: 0 0 50px; font-weight: 700; }
  .content-wrapper { display: flex; gap: 60px; flex: 1; height: 0; }
  .column { flex: 1; display: flex; flex-direction: column; min-width: 0; }
  .column h2 { font-size: 26px; color: var(--text-secondary); margin: 0 0 20px; font-weight: 700; }
  .code-block {
    background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--card-radius);
    padding: 0 20px; font-family: var(--font-code); font-size: 14px;
    line-height: 1.5; white-space: pre; box-shadow: var(--shadow);
  }
  .info-block {
    background-color: var(--surface); border: 1px solid var(--border); border-radius: var(--card-radius);
    padding: 16px 20px; font-family: var(--font-code);
    font-size: 18px; font-weight: 500; margin-bottom: 25px;
  }
  .info-block.config { color: var(--accent); }
</style>
```

---

## Comparison Table

Full-width table with header row and data rows. Use icons/symbols for quick scanning.

```html
<style>
  .slide { padding: 50px 60px; display: flex; flex-direction: column; }
  h1 { font-family: var(--font-heading); font-size: 44px; color: var(--text-primary); margin: 0 0 30px; text-align: center; }
  table { width: 100%; border-collapse: collapse; font-size: 15px; }
  th {
    background-color: var(--text-primary); color: var(--slide-bg); padding: 12px 16px;
    text-align: left; font-weight: 600; font-size: 14px;
  }
  td { padding: 10px 16px; border-bottom: 1px solid var(--border); color: var(--text-secondary); vertical-align: top; }
  tr:nth-child(even) td { background-color: rgba(var(--slide-bg-rgb),0.5); }
  td:first-child { font-weight: 600; color: var(--text-primary); }
  .check { color: var(--ok); }   /* positive check */
  .warn { color: var(--warn); }   /* warning */
  .dash { color: var(--muted); }  /* dash / n-a */
</style>
<div class="slide">
  <h1>Feature Comparison</h1>
  <table>
    <thead><tr><th>Tool</th><th>Feature A</th><th>Feature B</th><th>Feature C</th></tr></thead>
    <tbody>
      <tr><td>Tool 1</td><td class="check">&#10003;</td><td class="warn">&#9888;</td><td class="dash">&mdash;</td></tr>
      <tr><td>Tool 2</td><td class="check">&#10003;</td><td class="check">&#10003;</td><td class="warn">&#9888;</td></tr>
    </tbody>
  </table>
</div>
```

---

## Closing / Q&A Slide

Centered, minimal. Similar to cover but simpler.

```html
<style>
  .slide {
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; text-align: center;
  }
  h1 { font-family: var(--font-heading); font-size: 72px; color: var(--text-primary); margin: 0 0 30px; font-weight: 700; }
  p { font-size: 28px; color: var(--text-secondary); max-width: 700px; line-height: 1.6; }
</style>
<div class="slide">
  <h1>Thank You</h1>
  <p>Questions & Discussion</p>
</div>
```
