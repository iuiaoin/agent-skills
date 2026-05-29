# PLANNING.md Template

Use this structure when generating `PLANNING.md` during `--plan` mode. Adapt sections to match the user's prompt — not all sections are required for every deck.

---

## Template

```markdown
**Task**: [One-sentence description of the deck to generate]
**Slide count**: [N] ± [tolerance]
**Language**: [e.g., Chinese / English / bilingual]
**Audience**: [Target audience description]
**Goals**:
- [Goal 1]
- [Goal 2]
- [Goal 3]
**Style**: [Tone and style keywords, e.g., restrained, high information density, presentation-friendly]

---

## Visual & Layout Guidelines

- **Color theme**: chosen at `/deck --generate` (see the Themes catalog) — do not fix a palette here.
- **Brand override** (optional): [only if the brief specified brand colors — hex values to layer on the chosen theme's accent]
- **Canvas**: 1280×720 (16:9); keep content within safe margins (≥60px from edges)
- **Typography**: type scale from design-system.md (headings 48-72px, body 18-30px); the font family comes from the selected theme
- **Per-slide rule**: 1 key point + up to 4 supporting bullets; avoid large blocks of text
- **Footer**: page number + brief section name

---

## Slide-by-Slide Outline

**Slide 1 | Cover**
- Title: [title]
- Subtitle: [subtitle]
- Footer: presenter name, date

**Slide 2 | Agenda**
- [Topic 1]
- [Topic 2]
- [Topic 3]
- ...

**Slide 3 | [Section Title]**
- Key point: [one sentence]
- Supporting: [2-3 bullets]
- Visual element: [chart type / icon / diagram description]

[...continue for each slide...]

**Slide N | Closing / Q&A**
- Summary statement
- Call to action or discussion prompt

---

## Content & Tone Guidelines

- [Writing style notes]
- [What to emphasize / avoid]
- [How to handle controversial points]

---

## Data Sources & References

- [List materials from resources/ that should be synthesized]
- [Note how to use them: summarize, quote, compare, etc.]

---

## Deliverables

- Output: [N] HTML slides in `presentation/slides/`
- Viewer: `presentation/index.html` (from viewer template)
- Each slide: standalone HTML, 1280x720, 16:9 aspect ratio
- Optional: `PRESENTATION_SUMMARY.md`, `PRESENTATION_SCRIPT.md`
```

## Guidelines for Writing the Plan

1. **Be specific about content** — For each slide, write the actual key point and supporting bullets, not just "content about X". The plan is the source of truth for generation.
2. **Synthesize from resources/** — Reference specific files and describe how their content maps to slides.
3. **Specify visual elements** — For each slide, note what visual element it should have (chart, grid, diagram, image, icon set, etc.).
4. **Match audience expectations** — Technical audience = more data, less fluff. Executive audience = more impact, less detail.
5. **Include speaker notes guidance** — Note what the presenter should emphasize on each slide.
