# Deck Design System

Theme-agnostic design rules for generated decks. **Colors and fonts come from the selected theme** (see [themes/](themes/) and the registry in `SKILL.md`); everything else here — dimensions, type scale, animations, density, layout — is shared by all themes. The color theme is chosen at `/deck --generate`, not in the plan.

## Theme Token Contract

Every theme defines the same set of CSS custom properties. Slide patterns reference these tokens (`var(--…)`) instead of hardcoded colors, so a deck is themed simply by pasting the chosen theme's `:root{}` block into the top of each slide's `<style>`. Each theme file (`themes/<name>.md`) provides concrete values for all of these:

```css
:root {
  /* Surfaces */
  --slide-bg:        /* slide background */;
  --slide-bg-rgb:    /* same color as "r,g,b" for rgba() */;
  --surface:         /* cards, code blocks, info panels */;
  --border:          /* hairline borders */;

  /* Text */
  --text-primary:    /* titles, body */;
  --text-secondary:  /* subtitles, captions */;
  --text-strong:     /* bold emphasis */;

  /* Accents */
  --accent:          /* primary accent — bars, icons, key data, links */;
  --accent-rgb:      /* same color as "r,g,b" */;
  --accent-2:        /* secondary accent */;
  --accent-2-rgb:    /* same color as "r,g,b" */;
  --heading-gradient:/* gradient for clipped headings; solid themes use two equal stops */;

  /* Status / table semantics */
  --ok:              /* check / positive */;
  --warn:            /* warning */;
  --muted:           /* dash / disabled */;

  /* Typography */
  --font-heading:    /* heading font stack */;
  --font-body:       /* body font stack */;
  --font-code:       /* monospace stack */;

  /* Shape */
  --card-radius:     /* card/border radius */;
  --shadow:          /* default card shadow */;
}
```

**Why `*-rgb` triplets:** decorative shapes use the accent with alpha, e.g. `rgba(var(--accent-rgb), 0.15)`. **Why `--heading-gradient` is always a gradient:** the cover heading uses `background-clip: text`, so even solid-color themes define it as `linear-gradient(90deg, COLOR, COLOR)`.

Themes also ship a **font setup** (a Google Fonts `@import`, a local `@font-face`, or a system stack) and a **viewer-override** snippet — see each theme file.

## Typography (scale is universal; family comes from `--font-*`)

- **Headings**: `var(--font-heading)`, weight 600-700, sizes 48-72px, letter-spacing -0.5 to -1px
- **Body**: `var(--font-body)`, weight 400-500, sizes 18-30px, line-height 1.5-1.7
- **Chinese fallback**: append `'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB'` to the body/heading stacks
- **Code**: `var(--font-code)`, monospace

Some themes intentionally break this scale for effect (e.g. `artist` uses oversized uppercase display type); follow the theme file when it overrides the default.

## Slide Dimensions

- **Canvas**: 1280px x 720px (16:9)
- **Padding**: 60-120px depending on slide type
- **Content area**: Keep text within safe margins (min 60px from edges)

## Animations

```css
/* Primary content fade-in */
@keyframes fadeInContent {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* List items staggered reveal */
@keyframes slideInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
```

- **Every slide animates** — not just the cover and agenda. Animate the heading first, then stagger its cards / list items / table rows / columns. Never leave a content, two-column, table, or closing slide static; all slides share one animation approach.
- Use `animation-delay` increments of 0.1s for staggered items
- Duration: 0.5-1.2s, easing: `ease-out` or `ease-in-out`
- Decorative shapes: `scale(0.8)` to `scale(1)` over 2s
- Keep the full reveal (max `animation-delay` + duration) under ~1.5s. The visual-QA screenshots fire ~2.5s after load, so anything slower risks being captured mid-animation or blank.

## Layout Patterns

- **Per slide**: 1 key information point + 2-4 supporting bullets maximum
- **Avoid**: Large blocks of text, walls of bullets, dense paragraphs
- **Visual elements**: At least 1 per slide (icon, chart, diagram, card, color block)
- **Footer**: Page number + section name, positioned bottom-left or bottom-right

## Content Density & Overflow Prevention

All content must fit within the 1280×720 canvas without overflow or clipping.

- **Code blocks / file trees**: Maximum ~15 lines at 15px font size, or ~18 lines at 13px. If content exceeds this, reduce font size (minimum 12px) or split across slides.
- **Dense technical slides**: Use smaller font sizes (13-14px for code, 16-18px for body) and tighter padding (50-60px) to fit more content. Always verify the content fits within 720px height minus footer space (~50px).
- **Bullet lists**: Maximum 6 items per slide. If more are needed, split into multiple slides or use a 2-column grid.
- **Tables**: Maximum 8-10 rows. Beyond that, split across slides or use a smaller font size (13-14px).
- **When in doubt, split**: It is always better to use two clear slides than one cramped slide.

## Links

- All links in slides should include `target="_blank" rel="noopener"` since slides are rendered inside iframes.
- Style links to match the accent color (`color: var(--accent)`) with `text-decoration: none`.

## Decorative Elements

- Background accent shapes: radial gradients with low opacity, e.g. `radial-gradient(circle, rgba(var(--accent-rgb), 0.15) 0%, transparent 70%)`
- Card style: rounded corners (`var(--card-radius)`), subtle shadow (`var(--shadow)`)
- Borders: 1px solid `var(--border)`
- Bullet markers: Colored bars (12x28px in `var(--accent)`) or large accent-colored dots

Themes may override these conventions (e.g. `classic` drops decorative shapes; `hand-writing` draws borders with rough.js; `artist` uses dramatic full-bleed gradients). The theme file is authoritative for its own decorative style.
