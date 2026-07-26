# Research Wiki & Knowledge Base — Schema

Personal knowledge base for ML / DL / DS / LLM / RL research and mathematics notes.
**Claude/Antigravity writes and maintains `wiki/`. The human curates `raw/` and maintains personal note topics.**

## Directory layout

```text
raw/                     # Source documents — immutable, human-curated
  assets/                # Downloaded images (set as Obsidian attachment folder path)
wiki/                    # Topic: LLM & ML Research Wiki
  _index.md              # Notegen topic entry for Wiki
  index.md               # Content catalog — updated on every ingest
  log.md                 # Append-only chronological log
  concepts/              # Concept and idea pages (_index.md included)
  papers/                # Paper / book / lecture summaries (_index.md included)
  models/                # Model cards (_index.md included)
  ddm_unified_framework/ # Domain decomposition framework notes
  agents_context_representation/ # Agents context research
artificial_intelligence/ # Personal topic notes (_index.md)
dev/                     # Developer notes (_index.md)
homology_theory/         # Topology & Homology notes (_index.md)
mathematic_statistics/   # Math Stats notes (_index.md)
optimization_methods/    # Optimization notes (_index.md)
physics/                 # Physics notes (_index.md)
reinforcement_learning/ # RL notes (_index.md)
AGENTS.md                # Agent schema and operational rules
CLAUDE.md                # Quick references
```

---

## Page Types & Human-Friendly Formatting

Notes created by models must be both machine-parsable and readable by human readers on the `notegen` site.

### Formatting Guidelines
- **Callouts**: Use GitHub-style callouts (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`) for key takeaways, intuition, and highlights.
- **LaTeX Math**: Use KaTeX-compatible inline `$math$` and block `$$math$$` expressions.
- **Lead Excerpt**: The first paragraph under the title/frontmatter should be a clean, scannable summary used by `notegen` for page previews.
- **Structure**: Use clear H2 (`##`) and H3 (`###`) headers, bullet points, and code blocks with language identifiers.

---

### Frontmatter Schema

Every note file in `wiki/` (and updated topic notes) must include valid `notegen`-compatible frontmatter:

```yaml
---
title: "Human-readable Title"
description: "One sentence summary — used in previews and index.md"
type: paper-summary | concept | model-card | note
tags: ["dl", "llm", "rl"]
status: draft | in-progress | done
date: YYYY-MM-DD
sources: []   # list of raw/ paths synthesized into this page
---
```

**`status` values:**
- `draft` — placeholder or early outline, fewer than 3 sections filled
- `in-progress` — core content present, may have gaps or missing links
- `done` — comprehensive, all cross-references checked

**Tag vocabulary** (extend as needed):
`dl`, `llm`, `rl`, `cv`, `nlp`, `attention`, `transformers`, `fine-tuning`, `alignment`, `inference`, `efficiency`, `theory`, `benchmark`, `math`, `stats`, `optimization`

---

## File Naming

`snake_case`, all lowercase. No spaces. Replace special characters with underscores.

```text
wiki/papers/attention_is_all_you_need.md
wiki/concepts/reinforcement_learning_from_human_feedback.md
wiki/models/llama_3.md
```

---

## Operations

### Ingest

Triggered by: "ingest X" / "добавь X" / "обработай X"

```text
1. If PDF/PPTX/DOCX → convert:
     markitdown raw/<file> > raw/<name>.md
   Then read raw/<name>.md.

2. Read the source. Discuss key takeaways if requested.

3. Search existing wiki first:
     qmd search "<paper title or concept>"
   If a matching page exists → edit it. If not → create.

4. Write/update wiki pages:
   - 1 paper-summary (always, for each ingested source)
   - concept pages for key ideas introduced or used
   - model-card pages for any models described
   Ensure valid frontmatter (title, description, tags, status, date).

5. Update wiki/index.md — add new entries under the correct section.

6. Append to wiki/log.md:
     ## [YYYY-MM-DD] ingest | <Title>
     Added: <list of new files>
     Updated: <list of edited files>

7. Append entry to changelog.jsonl:
     {"timestamp":"YYYY-MM-DDTHH:MM:SSZ","action":"created","kind":"note","path":"wiki/papers/<name>.md","title":"<Title>","topic":"Research Wiki"}

8. If source files were in raw/papers/inbox/ and moved to raw/papers/processed/,
   update `sources:` frontmatter field in created pages to reflect new path.
```

### Query

Triggered by any research question.

```text
1. qmd search "<query>" to find relevant pages across wiki and personal notes.
2. Read the relevant pages.
3. Synthesize answer with citations: [[page_name]].
4. If non-trivial and reusable → file back:
   - As a new concept or comparison page, or
   - Appended to an existing page under "My notes".
5. Append to wiki/log.md:
     ## [YYYY-MM-DD] query | <Question summary>
     Filed: <page if answer was saved>
```

### Lint

**Run weekly** — check the date of the last `lint` entry in `wiki/log.md`.
Also runs on demand: "lint the wiki" / "проверь вики".

Checklist:
- [ ] Orphan pages (no inbound wikilinks) → add links or merge into parent
- [ ] Stubs with enough source material → promote to `in-progress` or `done`
- [ ] Contradictions between pages → reconcile
- [ ] Frontmatter validation for `notegen` (`status`, `description`, `tags`)
- [ ] Missing cross-references between closely related pages → add wikilinks

---

## New Page vs Edit Existing — Decision Rule

1. Run `qmd search "<entity name>"` first.
2. If a matching page is found → **always edit it**, never create a duplicate.
3. If no match → create a new page.

---

## Cross-Referencing

Use Obsidian wikilinks: `[[filename_without_extension]]`.
Do not include the subdirectory prefix in the link.

```markdown
The [[transformer_architecture]] introduced by [[attention_is_all_you_need]]...
```

Wikilinks work globally across all topic folders in `notegen`.
