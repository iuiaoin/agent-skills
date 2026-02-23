# Agent Skills

A collection of reusable skills for AI coding agents (Claude Code, etc.). Each skill is a self-contained package that extends an agent's capabilities with specialized workflows, domain knowledge, and bundled resources.

## Skills

### [deck](https://github.com/iuiaoin/agent-skills/tree/main/skills/deck)

HTML presentation deck generator with a strict two-stage workflow:

- **`/deck --plan`** — Analyze user prompt and reference materials in `resources/`, produce a slide-by-slide outline saved to `PLANNING.md`
- **`/deck --generate`** — Generate standalone HTML slides (1280x720, 16:9) from the approved plan, with a built-in presentation viewer

Supports technical sharing talks, architecture reviews, strategy decks, research summaries, pitch decks, and team updates. Outputs pure HTML/CSS/JS with no build tools required.

📎 [Sample repo](https://github.com/iuiaoin/deck-sample) · [Live demo](https://iuiaoin.github.io/deck-sample/)

## Skill Structure

Each skill follows a standard layout:

```
skill-name/
├── SKILL.md              # Instructions and metadata (required)
├── scripts/              # Executable code for deterministic tasks
├── references/           # Documentation loaded into context as needed
└── assets/               # Files used in output (templates, images, etc.)
```

## Installation

To use a skill, copy the skill directory into your `skills/`:

**Claude Code**

```bash
cp -r skills/deck ~/.claude/skills/deck
```

**Codex Cli and others**

```bash
cp -r skills/deck ~/.agents/skills/deck
```
