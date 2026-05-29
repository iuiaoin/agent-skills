# Brief Intake — Guided Planning Q&A

How to turn a sparse `--plan` prompt into a rich, structured **deck brief** before expanding it into `PLANNING.md`. Used during Planning Mode. The deck brief is a generalized version of an ideal, fully-specified prompt; its fields map directly onto the `PLANNING.md` header in [planning-template.md](planning-template.md).

**Precedence**: explicit user prompt > `resources/` materials > smart defaults. Never ask about anything you can reasonably infer — state the assumption in the brief and let the user override at confirmation.

---

## Essential Fields — Ask vs Infer

| Field | Policy | Default / how to derive |
|-------|--------|--------------------------|
| Audience + background/level | **ASK** if missing | — (drives depth + jargon; do not guess) |
| Goals / key takeaways | **ASK** if missing & no resources; else infer from `resources/` and confirm | derive candidate goals from resources |
| Language | **ASK** if missing | default = language the prompt was written in |
| Length (slide count) | **ASK** if missing | default 15 |
| Slide-count tolerance | INFER | ± 2 |
| Deck / session type | INFER | from topic + audience |
| Style & tone | INFER | from deck type + [design-system.md](design-system.md) |
| Goal emphasis / allocation | INFER | KEY goal ~50% of slides; state it |
| Content rules | INFER | one takeaway/slide; explain jargon on first use; diagrams over text; code only where load-bearing |
| Visual & layout guidelines | INFER | verbatim from [design-system.md](design-system.md) |
| Title | INFER | clean title from the topic |
| Presenter / date | INFER | `[Presenter Name]` + today's date placeholders |

**Resources feed inference**: if `resources/` is non-empty, read and summarize it, derive candidate goals/subtopics and concrete per-slide content from it (so goals shift from ASK to infer-then-confirm), and seed the Data Sources section. If empty, goals are a hard ASK.

---

## The Guided Q&A (one batched round)

When essentials are missing, ask **one** batched round — at most 3-5 questions, covering ONLY missing essentials. Each question offers a **recommended default** (listed first) plus 2-4 options, so the user can simply accept.

- Use your agent's structured multiple-choice question tool to present the batch in a single call — **Claude Code**: `AskUserQuestion`; **Copilot CLI**: `ask_user`; **Codex**: `request_user_input`. Each option = short label + one-line description; lead with the recommended option. Fallback (no such tool available): ask the same set as a short numbered list in one message; tell the user they may reply _"defaults"_ to accept all recommendations.
- Skip any question already answered by the prompt or resources. If all essentials are present, **skip the Q&A entirely**.
- Do **not** ask a second round. Synthesize the brief; the confirmation step absorbs remaining tweaks.

### Example question set — prompt: "make a deck about Transformers"

1. **Audience & background** — Software engineers, limited deep-learning background _(recommended)_ / ML practitioners comfortable with the math / Mixed technical audience / Non-technical leadership.
2. **Primary goal / main takeaway** — Build intuition for the Attention mechanism from scratch _(recommended)_ / Understand the end-to-end Transformer architecture / Survey downstream models (BERT/GPT) & impact / All of the above, balanced.
3. **Approximate length** — ~15 slides _(recommended)_ / ~10 (short talk) / ~20+ (deep dive).
4. **Language** — English _(recommended — matches your prompt)_ / Chinese / Bilingual (EN + 中文).

---

## Deck Brief Template

```
DECK BRIEF
Title: <clear deck/session title>
Session type: <technical sharing | architecture review | strategy/exec briefing | research summary | pitch | team update | workshop>
Length: <N> ± <tolerance> slides
Language: <English | Chinese | bilingual>
Audience: <who> — <background/level, what they do/don't already know>

Goals (in priority order):
1. <Goal 1> — subtopics: <a, b, c>. [emphasis: KEY focus, ~<X>% of slides]
2. <Goal 2> — subtopics: <a, b, c>. [emphasis: ~<Y>%]
3. <Goal 3> — subtopics: <a, b>. [emphasis: ~<Z>%, summary/takeaways]

Style: <tone keywords — restrained, high information density, diagram-heavy, presentation-friendly>.
Do: <prefer diagrams/formulas over text; one clear takeaway per slide; ...>.
Don't: <walls of text; excessive code — snippets only for <where>; unexplained jargon>.
Content rules: <explain each new concept in one plain sentence on first use; ...>.
Resources to use: <none | resources/ files and how each maps in>.
```

Keep it tight — roughly the length of the example below. The brief is for a quick confirmation, not the full plan.

---

## Worked Example (basic input → brief)

**User input:** "a deck about Transformers for engineers" (no resources).

**Q&A answers** (recommended defaults accepted): audience = SWEs, limited DL background; primary goal = build Attention intuition; length = ~15; language = English.

**Synthesized brief:**

```
DECK BRIEF
Title: Understanding Transformer Architecture — Attention Is All You Need
Session type: Technical sharing session
Length: 15 ± 2 slides
Language: English
Audience: Software engineers with limited deep-learning background — comfortable with code, new to attention/embeddings/softmax.

Goals (in priority order):
1. Build intuition for the Attention mechanism from scratch — subtopics: dictionary-lookup analogy, Scaled Dot-Product Attention, Self-Attention, Masked Self-Attention, Cross-Attention, Multi-Head Attention. [emphasis: KEY focus, ~50% of slides]
2. Explain the end-to-end Transformer Encoder-Decoder architecture — subtopics: Positional Encoding, FFN, LayerNorm, Residual Connections, causal mask, wiring via PyTorch nn.Transformer. [emphasis: ~35%]
3. Summarize downstream paradigms & takeaways — subtopics: Encoder-only (BERT), Decoder-only (GPT), full Encoder-Decoder, key takeaways. [emphasis: ~15%, closing summary]

Style: restrained, high information density, diagram-heavy, presentation-friendly.
Do: prefer architectural diagrams and formulas over text; one clear single-point takeaway per slide.
Don't: walls of text; heavy code — use snippets ONLY for the attention formula and multi-head core logic.
Content rules: when a DL concept (softmax, embedding, gradient, ...) first appears, give a one-sentence plain-language explanation.
Resources to use: none provided — synthesize from established Transformer fundamentals.
```

After the user confirms (or tweaks) this brief, expand it into `PLANNING.md` per [planning-template.md](planning-template.md): the brief becomes the header + Content & Tone Guidelines, and the goal emphasis percentages determine how many content slides each section receives (the KEY goal gets the most).
