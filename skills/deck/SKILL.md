---
name: deck
description: Generate high-quality HTML presentation decks with a strict two-stage workflow; manually invoked only when the user runs `/deck --plan` (guided brief, then create PLANNING.md), `/deck --generate` (produce final slides from approved PLANNING.md), and optionally `/deck --export pptx` (export generated slides to PPTX format), supporting technical sharing, architecture reviews, strategy decks, research summaries, pitch decks, and team updates as standalone 1280x720 (16:9) HTML slides.
---

# Deck — Presentation Deck Generator

## Command Modes

Parse the invocation to determine mode:

- **`/deck --plan [prompt]`** — Planning mode. From a basic prompt, run a quick guided Q&A, synthesize a structured deck brief, confirm it, then expand it into `PLANNING.md` and present for review. **Do NOT generate HTML.**
- **`/deck --generate [optional instructions]`** — Generation mode. Produce final HTML slides from approved `PLANNING.md`, then automatically run visual QA to catch and fix overflow/layout issues. **Refuse if `PLANNING.md` is missing.**
- **`/deck --qa [--scale N]`** — Visual QA mode. Re-run the screenshot-inspect-fix loop against already-generated slides (the same loop that runs automatically at the end of `--generate`). Useful after manual edits. **Refuse if `presentation/slides/` is missing or contains no slide HTML files.**
- **`/deck --export pptx [--scale N]`** — Export mode. Convert generated HTML slides into a PPTX file. Optional `--scale N` controls image resolution multiplier (default 3). **Refuse if `presentation/slides/` is missing or contains no slide HTML files.**

If neither flag is provided, ask the user which mode they want.

---

## Planning Mode (`--plan`)

Goal: turn whatever the user gives — often just a topic — into a rich, structured **deck brief**, confirm it, then expand the confirmed brief into a polished `PLANNING.md`. Brief first, plan second.

1. **Check `resources/` folder**
   - If missing or empty, remind the user: _"Place relevant source materials (articles, reports, notes, images) into `resources/` before planning for best results."_
   - If present, read and analyze all files. Summarize what was found, and use them to derive candidate goals/subtopics and concrete per-slide content.

2. **Parse the prompt; detect present vs missing essentials**
   - Extract whatever is given: topic/title, audience + level, goals/takeaways, language, slide count, style.
   - Classify the essentials (see [references/brief-intake.md](references/brief-intake.md)) as PRESENT or MISSING. Essentials: **audience + background**, **goals** (unless derivable from `resources/`), **language**, **rough slide count**.
   - Precedence for everything: explicit prompt > `resources/` > smart defaults.
   - **Already well-specified?** If the prompt already supplies the essentials (e.g. it resembles a full brief), skip step 3 and go straight to step 4.

3. **Guided Q&A** (one batched round, only if essentials are missing)
   - Ask **one** round of at most 3-5 questions, covering ONLY the missing essentials. Each question must offer a **recommended default** (listed first) plus 2-4 options so the user can simply accept. See [references/brief-intake.md](references/brief-intake.md) for the field policy and an example question set.
   - Present the batch with your agent's structured multiple-choice question tool — `AskUserQuestion` (Claude Code), `ask_user` (Copilot CLI), or `request_user_input` (Codex); one option per choice with a short label + one-line description, recommended first. Fallback: ask the same set as a short numbered list in one message and let the user reply _"defaults"_ to accept all.
   - Do **not** ask a second round, and never ask about fields you can infer — state those as assumptions in the brief for the user to override.

4. **Synthesize the deck brief**
   - Fill the **Deck Brief Template** in [references/brief-intake.md](references/brief-intake.md): title, session type, length ± tolerance, language, audience + level, goals (priority order, each with subtopics and an emphasis/allocation — mark the KEY goal and give it ~50% of slides), style with Do/Don't rules, content rules (one takeaway/slide, explain jargon on first use, diagrams over text, code only where load-bearing), and resources to use.
   - Infer everything not asked from topic + audience + [references/design-system.md](references/design-system.md). State assumptions explicitly. Keep the brief tight (about the length of the worked example).

5. **Confirm the brief**
   - Show the brief to the user and ask for a quick **OK or tweak**. Apply any edits and re-show. Do **not** expand into `PLANNING.md` until the brief is approved.

6. **Expand the confirmed brief into `PLANNING.md`**
   - Follow [references/planning-template.md](references/planning-template.md). The confirmed brief becomes the **header** (Task / Slide count ± tolerance / Language / Audience / Goals / Style) plus the **Content & Tone Guidelines** section.
   - **Visual & Layout Guidelines**: fill from the theme-neutral rules in [references/design-system.md](references/design-system.md) (1280x720 canvas, type scale, footer, density rules). **Do not bake in a color palette** — the color **theme is chosen at `/deck --generate`** (see [Themes](#themes)). If the brief specified brand colors, record them as an override to layer on the chosen theme's accent.
   - **Slide-by-Slide Outline**: let the goal **emphasis/allocation drive how many content slides each section gets** (the KEY goal gets the most — e.g. ~50%). Reserve cover + agenda + closing. For each slide write the actual key point (single takeaway), 2-4 supporting bullets, and a visual element, choosing a pattern from [references/slide-patterns.md](references/slide-patterns.md). Place code only on the slides the brief authorizes.
   - **Data Sources & References**: map each `resources/` file to slides; if none, note the content is synthesized.
   - **Deliverables**: standard block; offer `PRESENTATION_SUMMARY.md` / `PRESENTATION_SCRIPT.md` for 8+ slides.
   - Save to `PLANNING.md` in the working directory.

7. **Present & stop.** Summarize slide count, section allocation, and key decisions; ask for approval or revisions. **Do NOT proceed to generation.**

---

## Generation Mode (`--generate`)

1. **Check for `PLANNING.md`**
   - If missing: stop and tell the user to run `/deck --plan` first.
   - If present: read it as the source of truth.

2. **Confirm approval**
   - If the user has not clearly approved the plan in this conversation, ask: _"The plan in PLANNING.md is ready. Proceed with generation?"_

3. **Select a theme**
   - The deck's visual style comes from a **theme** (see [Themes](#themes) and `references/themes/`). Pick the default: a theme or brand named in `PLANNING.md` if present, otherwise `claude`.
   - Ask the user to choose one, using your agent's structured multiple-choice question tool — `AskUserQuestion` (Claude Code) / `ask_user` (Copilot CLI) / `request_user_input` (Codex). One question; the 10 themes are the options (label = theme name + the one-line description from the Themes table), the default listed first. Fallback (no such tool): present the 10 themes as a numbered list and let the user reply with a name or _"default"_.
   - Read the chosen `references/themes/<name>.md` — it supplies the `:root{}` token block, font setup, viewer overrides, decorative guidance, and any special setup.

4. **Read design references**
   - Load [references/design-system.md](references/design-system.md) for the [token contract](references/design-system.md#theme-token-contract), dimensions, type scale, animations, and density rules.
   - Load [references/slide-patterns.md](references/slide-patterns.md) for HTML patterns (written against the theme tokens) matching each slide type.

5. **Generate slides**
   - Create `presentation/slides/` directory.
   - Generate each slide as `slide{N}.html` — standalone HTML, 1280x720 canvas.
   - Follow the slide-by-slide outline from `PLANNING.md` exactly.
   - Apply the appropriate pattern from slide-patterns.md for each slide type (cover, agenda, content grid, comparison table, code, closing, etc.).
   - **Apply the theme to every slide:** paste the chosen theme's font setup + `:root{}` block at the top of each slide's `<style>` so the token-based patterns render in that theme, and follow the theme's decorative guidance.
   - **Theme-specific setup:**
     - `medium`: copy the four `assets/fonts/source-serif-pro-*.woff` files from the skill into `presentation/assets/fonts/` so the `@font-face` URLs resolve.
     - `hand-writing`: add the rough.js + rough-notation `<script>` tags and init snippet (from `themes/hand-writing.md`) at the end of each slide's `<body>`; mark boxes with `class="sketch"` and emphasis text with `data-annotate="…"`.
   - Incorporate content synthesized from `resources/` as specified in the plan.
   - **Animate every slide, consistently.** Apply the design system's fade-in / staggered-reveal approach to every slide's primary content — heading first, then cards / list items / table rows / columns via `animation-delay` increments — on **all** slide types (content, two-column, table, closing), not just the cover and agenda. Each pattern in slide-patterns.md already bakes this in; keep it (and the `@keyframes` it references, e.g. `fadeInContent` / `slideInUp`) when you adapt the pattern. Animations must finish within ~1.5s so the visual-QA screenshots capture the settled slide.

6. **Generate the viewer**
   - Copy `assets/viewer-template.html` to `presentation/index.html`.
   - Replace `{{DECK_TITLE}}` with the deck title from PLANNING.md.
   - Replace `{{SLIDES_ARRAY}}` with the actual slide paths: `"slides/slide1.html", "slides/slide2.html", ...`
   - Replace `{{VIEWER_THEME}}` with the chosen theme's **Viewer overrides** `:root{}` block (from `themes/<name>.md`) so the viewer frame matches the deck.
   - Verify `presentation/index.html` contains no unresolved template placeholders (`{{...}}`) after substitution. If any remain, fix them before visual QA or opening the browser.
   - **Per-slide URLs:** while playing, the viewer reflects the current slide in the URL hash (`index.html#3` = slide 3), so a slide can be refreshed, deep-linked, and navigated with browser Back/Forward; preview mode stays at the bare `index.html`. This ships inside the template — no substitution needed.

7. **Optional deliverables** (generate if the plan requests them or the deck has 8+ slides)
   - `presentation/slides/PRESENTATION_SUMMARY.md` — deck overview, structure, design specs.
   - `presentation/slides/PRESENTATION_SCRIPT.md` — speaker notes per slide (2-4 sentences each).

8. **Visual QA & autofix** (run before opening the browser, so the deck the user sees is already clean)

   1. **Ensure dependencies** — if `node_modules/` is missing in the skill's `scripts/` directory, run `cd <skill-path>/scripts && npm install` (same as Export mode). The QA step is often the first thing to need Node modules.
   2. **Screenshot all slides** — run `node <skill-path>/scripts/screenshot.mjs <presentation-dir> --report`. This writes `presentation/.screenshots/slideN.png` (one per slide, numbered to match `slides/slideN.html`) and `presentation/.screenshots/overflow-report.json`.
   3. **Inspect** — read `overflow-report.json` first: any slide in its `flagged` list (non-empty `overflowY` / `overflowX` / `offendingSelectors`) has clipped or escaping content and must be fixed. Then **read each `slideN.png`** image and judge it visually for issues the report cannot see:
      - Content clipped at the 1280×720 edge (text cut mid-line, missing footer).
      - Overlapping elements, collisions, text running under/over other boxes.
      - Misalignment, broken grids, uneven columns.
      - Awkward or excessive whitespace, content crammed into a corner, unbalanced composition.
   4. **Fix offending `slides/slideN.html`** with good design taste, applying the density rules in [references/design-system.md](references/design-system.md):
      - **Overflow (too much content):** reduce font size toward the documented minimums (body 16-18px, code 13-14px, never below 12px); tighten padding to 50-60px; condense or trim wording; cap bullets at 6 and table rows at 8-10.
      - **Overlap / collision:** increase gaps, fix `position` / `flex` / `grid` so elements no longer stack.
      - **Misalignment / broken grid:** equalize column widths, align baselines, fix `grid-template-columns` / `gap`.
      - **Awkward whitespace:** rebalance padding, recenter, or redistribute content across the canvas.

      Keep the theme's palette tokens, font stack, footer, and animation approach identical to the other slides. **Do not split a slide into multiple slides** — that changes the approved slide count; if content genuinely cannot fit, leave it as-is and report it instead (sub-step 6).
   5. **Re-check only what changed** — re-screenshot just the slides you edited: `node <skill-path>/scripts/screenshot.mjs <presentation-dir> --slides <comma-list> --report`. Read the updated PNGs and report. Repeat sub-steps 3-5.
   6. **Iteration cap** — run at most **3 QA rounds**. If any slide is still flagged after the third round, stop fixing and **report the remaining issues to the user**: name the slide, the specific problem (e.g. _"slide 6: code block still overflows ~40px past the bottom edge"_), and a recommendation (e.g. _"split into two slides, or shorten the example"_). Never loop indefinitely.
   7. `presentation/.screenshots/` is a scratch directory — leave it for the user to inspect or delete it; exclude it from the reported file count.

9. **Open & summarize**
   - Open the presentation in the default browser:
     - macOS: `open presentation/index.html`
     - Linux: `xdg-open presentation/index.html`
     - Windows: `start presentation/index.html`
   - Then report what was generated: file count, total slides, and output location. Note how many slides were auto-fixed during visual QA, and any issues you could not resolve.

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
   - The renderer is the shared `scripts/lib/render.mjs` module also used by the visual-QA step, so PPTX rendering and QA screenshots stay consistent.

4. **Report results**
   - Tell the user the PPTX file path and slide count.
   - If the export fails, show the error message and suggest troubleshooting steps:
     - Ensure Node.js >= 18 is installed
     - Ensure `presentation/slides/` contains valid slide HTML files
     - Try running `cd <skill-path>/scripts && npm install` manually if dependency installation failed

---

## QA Mode (`--qa`)

Re-run the visual QA loop against the already-generated slides — the same loop performed automatically at the end of Generation mode. Useful after the user has manually edited slides.

1. **Check for `presentation/slides/`** — if missing or empty, stop and tell the user to run `/deck --generate` first.
2. **Install dependencies** (first time only) — same as Export mode: if `node_modules/` is missing in the skill's `scripts/` directory, run `cd <skill-path>/scripts && npm install`.
3. **Run the QA loop** — perform Generation mode step 8 (Visual QA & autofix), sub-steps 2-7, against the existing slides. Honor an optional `--scale N` (default 1).
4. **Report** — tell the user which slides were fixed and list any issues you could not resolve within 3 rounds.

---

## Themes

Generated decks are styled by a **theme** chosen at the start of `--generate` (see that mode's "Select a theme" step). Each theme is defined in `references/themes/<name>.md` as a CSS-variable palette + font setup + viewer overrides + decorative guidance; slides reference the shared [token contract](references/design-system.md#theme-token-contract), so a deck adopts a theme simply by pasting that theme's `:root{}` block (and font setup) into each slide.

| Theme | Look |
|-------|------|
| `claude` *(default)* | Warm beige canvas, coral accent — calm, editorial (the original style). |
| `classic` | Clean white-on-black, monochrome, generous whitespace — simple and elegant. |
| `medium` | Medium.com serif (bundled Source Serif Pro), white canvas, green accent. |
| `github` | GitHub light — white, blue accent, hairline borders, code-forward. |
| `dark` | Near-black canvas, off-white text, violet→cyan glow — mysterious and elegant. |
| `google` | White + Google rainbow (blue/red/yellow/green), Roboto, Material elevation. |
| `microsoft` | Modern Fluent — Segoe UI, `#0078D4` blue, subtle depth. |
| `twitter` | Classic blue-bird — `#1DA1F2`, Helvetica Neue, rounded tweet cards. |
| `hand-writing` | Sketchnote — handwriting fonts + rough.js sketchy borders & rough-notation marks. |
| `artist` | Movie-poster drama — oversized type, bold clashing gradients. |

The token contract and shared (theme-independent) rules live in [references/design-system.md](references/design-system.md).

---

## Slide Quality Rules

- **One key point per slide** + up to 4 supporting bullets.
- **No text walls.** If a slide has more than ~60 words of body text, split it.
- **No overflow.** All content must fit within 1280×720 without clipping. For dense content (code blocks, file trees, tables), reduce font size or split across multiple slides. See content density guidelines in [references/design-system.md](references/design-system.md).
- **Every slide has a visual element** — icon set, grid layout, chart placeholder, diagram, color-blocked card, or image.
- **Consistent styling** — all slides share the **selected theme's** palette tokens, font stack, and animation approach.
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
    ├── assets/fonts/            # Theme-bundled fonts (when a theme needs them, e.g. medium)
    ├── <deck-title>.pptx        # Created in --export pptx mode
    ├── .screenshots/            # QA scratch: slideN.png + overflow-report.json
    └── slides/
        ├── slide1.html          # Individual slides
        ├── slide2.html
        ├── ...
        ├── slideN.html
        ├── images/              # If slides reference images
        ├── PRESENTATION_SUMMARY.md   # Optional
        └── PRESENTATION_SCRIPT.md    # Optional
```
