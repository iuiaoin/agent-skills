---
name: deck
description: Generate high-quality HTML presentation decks with a strict two-stage workflow; manually invoked only when the user runs `/deck --plan` (create PLANNING.md) or `/deck --generate` (produce final slides from approved PLANNING.md), supporting technical sharing, architecture reviews, strategy decks, research summaries, pitch decks, and team updates as standalone 1280x720 (16:9) HTML slides.
---

# Deck — Presentation Deck Generator

## Command Modes

Parse the invocation to determine mode:

- **`/deck --plan [prompt]`** — Planning mode. Create deck outline, save to `PLANNING.md`, present for review. **Do NOT generate HTML.**
- **`/deck --generate [optional instructions]`** — Generation mode. Produce final HTML slides from approved `PLANNING.md`. **Refuse if `PLANNING.md` is missing.**

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

5. **Generate the viewer**
   - Copy `assets/viewer-template.html` to `presentation/index.html`.
   - Replace `{{DECK_TITLE}}` with the deck title from PLANNING.md.
   - Replace `{{SLIDES_ARRAY}}` with the actual slide paths: `"slides/slide1.html", "slides/slide2.html", ...`

6. **Optional deliverables** (generate if the plan requests them or the deck has 8+ slides)
   - `presentation/slides/PRESENTATION_SUMMARY.md` — deck overview, structure, design specs.
   - `presentation/slides/PRESENTATION_SCRIPT.md` — speaker notes per slide (2-4 sentences each).

7. **Summary** — Report what was generated: file count, total slides, output location, and how to view (open `presentation/index.html` in a browser).

---

## Slide Quality Rules

- **One key point per slide** + up to 4 supporting bullets.
- **No text walls.** If a slide has more than ~60 words of body text, split it.
- **Every slide has a visual element** — icon set, grid layout, chart placeholder, diagram, color-blocked card, or image.
- **Consistent styling** — all slides share the same color palette, font stack, and animation approach.
- **Scannable** — use bold labels, short phrases, and structured layouts (grids, lists, cards).
- **Footer** — include page number on content slides.

---

## Output Structure

```
working-directory/
├── PLANNING.md                  # Created in --plan mode
├── resources/                   # User-provided reference materials
└── presentation/                # Created in --generate mode
    ├── index.html               # Viewer (from viewer-template.html)
    └── slides/
        ├── slide1.html          # Individual slides
        ├── slide2.html
        ├── ...
        ├── slideN.html
        ├── images/              # If slides reference images
        ├── PRESENTATION_SUMMARY.md   # Optional
        └── PRESENTATION_SCRIPT.md    # Optional
```
