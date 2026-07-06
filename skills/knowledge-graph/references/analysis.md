# Analyzing a Knowledge Base

Goal: understand the knowledge base well enough to write a short **explanation** — a
prose map of the territory. Write the explanation BEFORE designing any graph. The
explanation is the thinking; the graph (see [graph-spec.md](graph-spec.md)) is only
its rendering.

Act as a knowledge cartographer, not a software engineer: the map is about
**concepts, domains, and reader journeys** — not subsystems and data flows. (This is
the key difference from repository-architecture diagrams: a wiki's "architecture" is
how understanding is organized, and its explicit cross-page links are real evidence.)

## Stage A — Read the survey digest

Run the survey first (see SKILL.md workflow). Interpret its signals:

- **Entry points** — where the authors expect readers to start. Read all of them.
- **Root `.order`** — the author-curated table of contents. Its ordering IS the
  intended narrative (e.g. numbered sections = the canonical journey). Weight it
  heavily when choosing groups.
- **Hub pages** (high `in:`) — pages many others link to; usually core concepts or
  must-do setup steps. High `out:` with low `in:` is usually an index page.
- **Sections by volume** — where the mass of content lives. Big ≠ important:
  scratch/log/archive sections are often the largest. Judge by role, not size.
- **Orphans / unresolved links** — a high orphan share means the link graph alone
  understates structure; lean more on directories, `.order`, and reading.

## Stage B — Read a sample of pages (targeted, not exhaustive)

Read roughly 10–20 pages, chosen deliberately:

1. Every entry point, and the top ~10 hub pages.
2. One representative page per major section (use `survey.py <src> --dir <section>`
   to pick — prefer the section's most-inbound page).
3. Anything the digest makes look load-bearing but you cannot yet describe in one
   sentence.

While reading, collect exactly what the map needs:

- **Purpose & audience** — who reads this knowledge base and to do what?
- **Domains** — the 3–8 big themes a newcomer would recognize.
- **Core concepts** — the entities everything else talks about (systems, processes,
  datasets, policies, tools). Note the best single page for each.
- **Relationships stated in prose** — "before X do Y", "X produces Y", "X runs on
  Y", "see also" — these become edges, with the sentence as evidence.
- **Reader journeys** — ordered paths (onboarding sequence, lifecycle stages,
  numbered guides). Every good knowledge map shows at least one journey.
- **Dead weight** — archives, personal scratch notes, meeting logs, drafts. Note
  them so the graph can compress them to at most one low-weight node each.

## Stage C — Write the explanation

Write 8–16 short sections of prose (not JSON, not diagram syntax). Requirements:

- Be concrete and source-specific; name actual pages, sections, and systems.
- Identify the main domains, the core concepts inside each, and the boundaries
  between them.
- Describe the relationships and at least one reader journey end to end.
- Say where a newcomer should start and which pages are the load-bearing hubs.
- Call out what you are deliberately leaving off the map (scratch, archive,
  per-person notes) in one line.
- Keep it high-signal; do not describe the same theme twice under different names.

Show the explanation to the user when they asked for review, or proceed directly to
graph design (graph-spec.md) otherwise — the explanation stays in the conversation
as the source of truth for every node and edge you draw.
