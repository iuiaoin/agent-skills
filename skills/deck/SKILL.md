---
name: deck
description: Generate high-quality HTML presentation decks with a strict two-stage workflow; manually invoked only when the user runs `/deck --plan` (create PLANNING.md), `/deck --generate` (produce final slides from approved PLANNING.md), and optionally `/deck --export pptx` (export generated slides to PPTX format), supporting technical sharing, architecture reviews, strategy decks, research summaries, pitch decks, and team updates as standalone 1280x720 (16:9) HTML slides.
---

# Deck — Presentation Deck Generator

## Command Modes

Parse the invocation to determine mode:

- **`/deck --plan [prompt]`** — Planning mode. Create deck outline, save to `PLANNING.md`, present for review. **Do NOT generate HTML.**
- **`/deck --generate [optional instructions]`** — Generation mode. Produce final HTML slides from approved `PLANNING.md`. **Refuse if `PLANNING.md` is missing.**
- **`/deck --export pptx [--scale N]`** — Export mode. Convert generated HTML slides into a PPTX file. Optional `--scale N` controls image resolution multiplier (default 3). **Refuse if `presentation/slides/` is missing or contains no slide HTML files.**

If neither flag is provided, ask the user which mode they want.

---

## Planning Mode (`--plan`)

1. **Check `resources/` folder**
   - If missing or empty, remind the user: _"Place relevant source materials (articles, reports, notes, images) into `resources/` before planning for best results."_
   - If present, read and analyze all files. Summarize what was found.

2. **Analyze the user prompt**
   - Extract: topic, audience, tone, language, slide count, goals, style preferences.
   - If the user prompt is under-specified, ask clarifying questions (audience, slide count, language, goals).

3. **Draft the plan**
   - Follow the structure in [references/planning-template.md](references/planning-template.md).
   - For each slide: specify the key point, supporting bullets, and visual element type.
   - Map content from `resources/` to specific slides — cite which resource informs which slide.
   - Include visual/layout guidelines (colors, fonts) — use defaults from [references/design-system.md](references/design-system.md) unless the user specifies otherwise.

4. **Save to `PLANNING.md`** in the working directory.

5. **Present the plan** to the user for review. Summarize slide count, structure, and key decisions. Ask for approval or revision feedback.

6. **Stop.** Do NOT proceed to generation.

---

## Generation Mode (`--generate`)

1. **Check for `PLANNING.md`**
   - If missing: stop and tell the user to run `/deck --plan` first.
   - If present: read it as the source of truth.

2. **Confirm approval**
   - If the user has not clearly approved the plan in this conversation, ask: _"The plan in PLANNING.md is ready. Proceed with generation?"_

3. **Read design references**
   - Load [references/design-system.md](references/design-system.md) for color palette, typography, animations.
   - Load [references/slide-patterns.md](references/slide-patterns.md) for HTML patterns matching each slide type.

4. **Generate slides**
   - Create `presentation/slides/` directory.
   - Generate each slide as `slide{N}.html` — standalone HTML, 1280x720 canvas.
   - Follow the slide-by-slide outline from `PLANNING.md` exactly.
   - Apply appropriate pattern from slide-patterns.md for each slide type (cover, agenda, content grid, comparison table, code, closing, etc.).
   - Incorporate content synthesized from `resources/` as specified in the plan.
   - Include animations (fade-in, staggered reveals) per the design system.
   - Keep the visual center of gravity centered within the canvas. Avoid slides that feel top-heavy, left-heavy, or visually cropped in the preview/player.
   - Reserve a playback-safe bottom area on every slide. No meaningful text, diagrams, or footers may sit in the bottom ~56px of the 720px canvas.
   - If a slide cannot fit cleanly while preserving the safe area and readable sizing, reduce the content or split it into 2 slides. Never rely on clipping.
   - Reserve a bottom safe area on every slide: keep meaningful content above the footer lane and leave roughly one text line of empty space above the bottom edge so presentation chrome never overlaps the last line.
   - Balance layouts inside the live frame, not the full canvas: center single-column covers/section-breaks within the safe content area, and avoid top-heavy compositions unless the slide is intentionally diagram-led.
   - Keep geometry contract stable: do not add safe-area padding directly on `.slide` (fixed 1280x720 frame). Apply safe-area padding in `.content-frame` only.
   - If any wrapper uses `height: 100%` and padding, ensure `box-sizing: border-box` so added padding does not push content off-center or clip the bottom.
   - If a slide becomes cramped, do not shrink everything indiscriminately. First reduce copy, then simplify the visual, then split the content into two slides.

5. **Generate the viewer**
   - Copy `assets/viewer-template.html` to `presentation/index.html`.
   - Replace `{{DECK_TITLE}}` with the deck title from PLANNING.md.
   - Replace `{{SLIDES_ARRAY}}` with the actual slide paths: `"slides/slide1.html", "slides/slide2.html", ...`

6. **Optional deliverables** (generate if the plan requests them or the deck has 8+ slides)
   - `presentation/slides/PRESENTATION_SUMMARY.md` — deck overview, structure, design specs.
   - `presentation/slides/PRESENTATION_SCRIPT.md` — speaker notes per slide (2-4 sentences each).

7. **Open & summarize**
   - Open the presentation in the default browser:
     - macOS: `open presentation/index.html`
     - Linux: `xdg-open presentation/index.html`
     - Windows: `start presentation/index.html`
   - Then report what was generated: file count, total slides, and output location.

---

## Export Mode (`--export pptx`)

1. **Check for `presentation/slides/`**
   - If missing or empty: stop and tell the user to run `/deck --generate` first.
   - Verify that slide HTML files (`slide1.html`, `slide2.html`, ...) exist in the directory.

2. **Install dependencies** (first time only)
   - Check if `node_modules/` exists in the skill's `scripts/` directory.
   - If not, run: `cd <skill-path>/scripts && npm install`
   - The skill's `scripts/` directory is located relative to this SKILL.md file, under `scripts/`.

3. **Run the export script**
   - Execute: `node <skill-path>/scripts/export-pptx.mjs <presentation-dir> [deck-title] [--scale N]`
   - `<presentation-dir>` is the `presentation/` directory in the working directory.
   - `[deck-title]` is optional — extract it from `PLANNING.md` if available, otherwise default to `deck`.
   - `[--scale N]` is optional — pass through from the user's invocation if provided (default 3).
   - The script will:
     - Launch a headless browser to render each slide at 1280x720 (Nx resolution for crisp output, default 3x)
     - Capture each slide as a high-quality PNG screenshot
     - Assemble all screenshots into a PPTX file
     - Save the PPTX to `presentation/<deck-title>.pptx`
     - Clean up temporary image files automatically

4. **Report results**
   - Tell the user the PPTX file path and slide count.
   - If the export fails, show the error message and suggest troubleshooting steps:
     - Ensure Node.js >= 18 is installed
     - Ensure `presentation/slides/` contains valid slide HTML files
     - Try running `cd <skill-path>/scripts && npm install` manually if dependency installation failed

---

## Slide Quality Rules

- **One key point per slide** + up to 4 supporting bullets.
- **No text walls.** If a slide has more than ~60 words of body text, split it.
- **No overflow.** All content must fit within 1280×720 without clipping. For dense content (code blocks, file trees, tables), reduce font size or split across multiple slides. See content density guidelines in [references/design-system.md](references/design-system.md).
- **Every slide has a visual element** — icon set, grid layout, chart placeholder, diagram, color-blocked card, or image.
- **Consistent styling** — all slides share the same color palette, font stack, and animation approach.
- **Scannable** — use bold labels, short phrases, and structured layouts (grids, lists, cards).
- **Title-page alignment policy** — default to centered composition for cover/section/title pages. Use left-aligned title pages only when explicitly requested by the user/plan and keep that choice consistent across title pages in the same deck.
- **Centered composition** — titles and major content blocks should feel optically centered within the safe content frame, not pushed against the top edge.
- **Bottom safe area** — keep the last ~56px of the slide clear of critical content so playback chrome or page overlays never cover the final line.
- **Footer profile** — default content-slide footer style should stay compact and consistent (`left/right: 70px`, `bottom: 18px`, `font-size: 12px`, muted text). Cover slides may use a larger footer profile (`left/right: 60px`, `bottom: 40px`, `font-size: 16px`).
- **Dense-slide compact mode** — when a slide includes 2+ dense cards/panels or a large summary bar, increase bottom-safe padding to about `86-102px` and reduce body text one step before shipping; never let content extend into the footer lane.
- **No visual clipping** — do not depend on `overflow: hidden` to hide oversized content; condense or split the slide instead.
- **Stable frame contract** — keep `.slide` as a fixed frame (1280x720) without extra safe-area padding. Use `.content-frame` for internal spacing and footer-lane reservation.
- **Title descender safety** — for large display titles (about 56px+), use line-height >= 1.02 so letters like `g/y/p/q` are never clipped.
- **Dense stack budget** — for architecture/layer stacks, reduce per-layer sizing and spacing so the last layer remains clearly above the footer lane; split if needed.
- **Footer** — include page number on content slides.

## Validation Checklist

Before finishing generation, visually inspect the generated deck in the viewer and verify:

- List view preserves a 16:9 aspect ratio with no horizontal or vertical cropping.
- Fullscreen/player mode keeps slides centered and scaled without distortion.
- No slide has important content or footer text inside the playback-safe bottom area.
- If any slide feels cramped or cropped, revise that slide immediately by simplifying or splitting it.
- **Safe area** — reserve a bottom footer lane; no body copy, captions, or cards should sit flush against the lower edge.
- **Centered composition** — for cover, section break, and single-message slides, center content within the safe content frame rather than anchoring it too high.
- **Title-page consistency check** — cover/section/title page alignment should be consistent within the same deck unless a mixed alignment is explicitly requested.
- **Title alignment sanity check** — on cover/section slides, the title block should be centered horizontally and visually around the middle band of the live frame (roughly 45%-55% of frame height), not biased toward the top.
- **Descender sanity check** — verify the largest title renders cleanly (including `g/y/p/q/j` descenders) with no top/bottom crop in list and player mode.
- **Stack sanity check** — for layer/architecture slides, confirm the bottom card and labels remain fully visible above the footer lane.
- **Dense layout sanity check** — for slides with multiple cards/rows (for example comparison grids, two-column panel stacks, or bottom callout bars), verify the lowest card/callout clears the footer lane with visible breathing room.
- **Overflow policy** — never let content crop at the bottom. Shorten, simplify, or split the slide instead.

---

## Output Structure

```
working-directory/
├── PLANNING.md                  # Created in --plan mode
├── resources/                   # User-provided reference materials
└── presentation/                # Created in --generate mode
    ├── index.html               # Viewer (from viewer-template.html)
    ├── <deck-title>.pptx        # Created in --export pptx mode
    └── slides/
        ├── slide1.html          # Individual slides
        ├── slide2.html
        ├── ...
        ├── slideN.html
        ├── images/              # If slides reference images
        ├── PRESENTATION_SUMMARY.md   # Optional
        └── PRESENTATION_SCRIPT.md    # Optional
```
