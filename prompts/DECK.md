I want to create a skill called "deck" (short for presentation deck generator).

1. What it should do

This skill should generate a high-quality HTML presentation deck from:

- a user prompt (topic, audience, tone, slide count, etc.)
- reference materials placed in a local `resources/` folder (default behavior; the user should not need to mention this explicitly)
- optional project/code context

This skill should support a strict two-stage workflow with explicit command modes:

- `/deck --plan` → planning only
- `/deck --generate` → generate the final deck HTML only if `PLANNING.md` already exists and the user has reviewed/approved the plan

Important workflow requirements:

- The skill MUST create a deck plan/outline first
- It must save that plan to `PLANNING.md`
- The skill must not generate the final deck during `--plan`
- The skill must not generate the final deck during `--generate` if `PLANNING.md` is missing
- The skill must treat `PLANNING.md` as the source of truth for deck generation
- The skill should ask for confirmation/approval before generation if approval is not clearly established in the conversation

The skill should help Claude:

- parse the command mode (`--plan` vs `--generate`)
- analyze the user prompt
- automatically inspect `resources/` for relevant materials (articles, reports, quotes, notes, images, etc.)
- create a clear deck outline / plan
- save the plan into `PLANNING.md`
- present the plan to the user for review (for `--plan`)
- generate the final presentation deck as HTML (for `--generate`, after approval)
- follow a consistent style and formatting standard
- optionally reuse existing templates/examples

The output should be:

- `PLANNING.md` (required in planning stage)
- final deck HTML in `presentation/` (generation stage)
- optionally an intermediate `deck_spec.json` if useful

I want this skill to be used manually (explicit invocation like `/deck --plan` or `/deck --generate`), not auto-triggered.

Also, the skill should proactively remind the user to place relevant source materials into the `resources/` folder before generating the plan, if the folder is missing or empty.

2. Example prompts / scenarios

The example prompts should be specific, structured, and realistic (not generic). Here are examples of the kinds of requests this skill should support:

Example A (technical tool comparison / sharing talk, planning stage):

- "/deck --plan Create a Chinese presentation deck for a technical sharing session titled 'Horizontal Comparison and Practical Experience with AI Coding Agent Tools'. Target length: 15 ± 2 slides. Audience: engineers and technical managers with software development experience. Goals: compare and evaluate Claude Code CLI, Codex CLI, Cursor, Windsurf, GitHub Copilot (VS Code), Augment Code, Cline, Devin, and V0; explain suitable use cases and tool-selection advice; summarize with practical hands-on experience and opinions. Style: restrained, high information density, presentation-friendly."

Example B (technical tool comparison / generation stage):

- "/deck --generate Use the approved plan in PLANNING.md to generate the final HTML deck. Keep the tone restrained, high-density, and suitable for a live technical sharing talk."

Example C (architecture review, planning stage):

- "/deck --plan Create an 8-slide English deck for an architecture review of our monolith-to-microservices migration plan. Audience: backend engineers and engineering managers. Goal: explain current pain points, target architecture, migration phases, risks, and rollout strategy. Style: concise, technical, and decision-oriented."

Example D (executive strategy update, planning stage):

- "/deck --plan Create a 10-slide executive-facing strategy deck in English on our AI-assisted developer productivity initiative. Audience: CTO, VP Engineering, and product leadership. Goal: summarize current experiments, key findings, ROI assumptions, risks, and next-quarter recommendations. Style: clean, high signal, minimal jargon."

Example E (research synthesis, planning stage):

- "/deck --plan Create a 12-slide research summary deck in Chinese based on the source materials in `resources/`. Topic: trends and constraints of AI coding agents in enterprise environments. Audience: engineering leads and platform teams. Goal: synthesize key insights, compare viewpoints, identify risks, and provide actionable recommendations."

Example F (generation blocked because plan missing):

- "/deck --generate Generate the final deck for a startup pitch about an AI workflow product."
  (Expected behavior: the skill should detect that `PLANNING.md` is missing and ask the user to run `/deck --plan` first.)

Typical scenarios:

- Technical design review
- Product roadmap / strategy review
- Research summary / analysis presentation
- Pitch / proposal deck
- Internal team update deck

Note: The skill should automatically use materials from `resources/` by default, rather than requiring the user to mention them in the prompt.

3. Specific tools, file formats, and domains

Primary domain:

- Presentation deck generation (HTML slides)
- Research / technical / product / strategy communication

Important file formats and folders:

- HTML (final deck output)
- Markdown (.md) for planning and instructions
- JSON (optional `deck_spec.json` intermediate format)
- Reference materials in text/markdown/pdf/image form (if present)
- Images from user-provided resources

I already have a practice project that the skill should learn from / reference:

- /Users/lixiaoli/Projects/presentation-deck-builder

In that project:

- `examples/` contains template examples (sample generated deck HTML)
- `resources/` contains user-provided references and materials (articles, reports, quotes, user opinions/notes, possibly images)
- `presentation/` contains final generated outputs
- `PLANNING.md` contains the generated deck outline, requirements, and theme based on the prompt + resources
- `CLAUDE.md` contains rules/instructions for Claude when generating the deck HTML code

The skill should ideally:

- inspect these files/folders when relevant
- use `PLANNING.md` and `CLAUDE.md` as guidance if available
- use `examples/` as style/template references
- generate output into a `presentation/` folder
- keep slides scannable (clear headings, concise bullets, not too much text)

Preferred workflow behavior:

1. Parse command mode (`--plan` or `--generate`)
2. For `--plan`:
   - Read user prompt
   - Inspect `resources/` automatically
   - Draft plan and save to `PLANNING.md`
   - Present the plan for user review/approval
   - Do NOT generate deck HTML
3. For `--generate`:
   - Check whether `PLANNING.md` exists
   - Check whether the user has approved the plan
   - If missing/unapproved, stop and ask user to review or run `/deck --plan`
   - If approved, generate deck HTML in `presentation/`
4. Save final output and summarize what was generated

It should work well for Claude Code, but I also want the structure to be reusable for other agent/code CLIs later (e.g. Codex CLI), so a clean skill structure + scripts/templates approach is preferred.
