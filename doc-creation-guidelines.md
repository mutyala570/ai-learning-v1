# Doc Creation Guidelines

**Purpose:** rules I must follow every time the user asks me to create a markdown note file (course notes, revision notes, explanation docs, etc.). Keeps all learning notes consistent and navigable.

**Read this file first whenever the user says "create a doc", "create md file", "make a note", or asks for learning notes.**

---

## 1. Decide where the file goes

| User context | Folder |
|--------------|--------|
| Weekday AI course notes | `week-one/`, `week-two/`, `week-three/`, … |
| Weekend Python self-study | `learn-python/` (main files) or `python-practice/YYYY-MM-DD/` (small scripts) |
| Project-wide reference / status / dashboards | `goal/` |

If unsure, check `goal/04-learning-status.md` → "Learning schedule" table. Weekday = course track → `week-N/`. Weekend = Python track.

---

## 2. Decide the filename

Format: `day-<N>-<topic>.md`

- `<N>` is the spelled-out day number: `day-one`, `day-two`, `day-three`, etc.
- `<topic>` is a short kebab-case description of the subject: `rag-architecture`, `agent-patterns`, `vector-databases`.
- Example: `day-two-rag-architecture.md`

If the file is covering a single topic across many sessions (not day-bound), drop the day prefix and just use the topic: `rag-notes.md`, `agent-architecture.md`.

Always ask/confirm the name if the topic is ambiguous. Never invent a name without proposing it first.

---

## 3. Top-of-file structure

Every learning note starts with three things, in this order:

### 3.1 Title heading

Format: `# Week <N> — Day <M>: <Topic Title> (Video <V>)`

Example: `# Week 2 — Day 2: RAG Architecture (Video 2)`

If the file is not tied to a specific video (e.g. general notes), drop the `(Video V)` suffix.

### 3.2 "Slides Covered" / "Topics Covered" index

A clickable table of contents that jumps to each section in the body.

- Heading: `## Slides Covered in This Document` (for video-based notes) or `## Topics Covered in This Document` (for general notes).
- If content comes from a video with multiple slides, group the index by slide:

```markdown
### Slide 1 — <Slide Title>
1. [**<Subtopic 1>**](#subtopic-1-anchor)
2. [**<Subtopic 2>**](#subtopic-2-anchor)

### Slide 2 — <Slide Title>
1. [**<Subtopic 1>**](#subtopic-1-anchor)
```

- If the doc has no slide structure, just list the sections directly:

```markdown
1. [**<Section 1>**](#section-1-anchor)
2. [**<Section 2>**](#section-2-anchor)
```

### 3.3 Horizontal rule

Always put a `---` between the index and the first body section.

---

## 4. Anchor link rules (for the TOC)

Markdown anchors are auto-generated from heading text. The rule is:

- Lowercase everything.
- Replace spaces with `-`.
- Strip punctuation (parentheses, colons, commas, apostrophes, periods).
- Em-dash (`—`) becomes a single `-` but often produces a double `--` in practice — test both and pick whichever renders.

Example heading: `## The Four Main Components` → anchor: `#the-four-main-components`.

Example heading: `# Slide 1 — Retrieval Augmented Generation (Overview)` → anchor: `#slide-1--retrieval-augmented-generation-overview`.

---

## 5. Body structure

### 5.1 If the note covers slides

Each slide gets its own `# Slide <N> — <Title>` top-level heading, followed by its subtopics as `##` headings. Between slides, use a `---` horizontal rule.

### 5.2 If the note covers one topic

Use `#` for the main sections and `##` for subtopics within them. Use `---` between major sections sparingly.

### 5.3 Heading depth

- `#` → slide titles or major top-level sections
- `##` → main subtopics (these are the ones linked in the TOC)
- `###` → deeper subtopics inside a `##` section
- Rarely go below `###`. If you feel the need, the section is probably too long — break it up.

---

## 6. Writing style

- **Use full sentences and paragraphs.** Do not produce bullet dumps. A reader should be able to read the doc straight through and understand it.
- **Explain the "why", not just the "what".** Notes are for revision. Describe the motivation and the intuition behind each concept, not just its definition.
- **Use sub-headings generously.** Makes it easy to scan and to link to.
- **Use bullet lists for enumerations only** — things that are genuinely a list (e.g. "The three properties are: grounding, traceability, freshness"). Do not turn every paragraph into bullets.
- **Use code fences for prompts, commands, examples, and pseudo-templates.**
- **Use blockquotes (`>`) for the one-line takeaway of a section** when there is one.
- **Use bold (`**text**`)** to highlight key terms the first time they appear.
- **No emojis** unless the user explicitly asks for them.
- **No trailing section summaries** ("In summary, we saw…"). End a section with its last substantive paragraph.

---

## 7. Incremental updates

When the user adds more slides / topics to an existing note:

- **Append**, never rewrite. Existing sections stay intact.
- Add the new `### Slide N — <title>` group to the TOC and its sub-links.
- Add the new `# Slide N — <title>` body section at the bottom, separated by `---`.
- Update the `Slides Covered` section so the index stays accurate.

If the user says "this is slide 1 only, more coming" — confirm, leave space for more, and explicitly scope the current content under Slide 1 even if it is the only slide so far.

---

## 8. When to ask before writing

Ask the user before writing if any of these are unclear:

- Filename or location (ambiguous topic, or between folders).
- Whether content should be appended to an existing file or start a new one.
- The slide number / video number / week number if not stated.

Do not invent. A 10-second clarification question is cheaper than a rewrite.

---

## 9. After writing

End the response with one short sentence stating what was created (file path) and what the next expected input is (e.g. "share slide 2 when ready"). No long summary of what is inside the file — the user can read it.

---

## 10. Summary files — special shape

When the user asks to **write a summary** (recap, condensed version, "summarise X", "give me a summary of week N", "summary of these notes"), use this hierarchical shape — **not** flowing paragraphs that mention several items inline, and **not** a flat one-line glossary.

### 10.1 Core rule

Every concept, sub-concept, and leaf item gets its own numbered heading with its own short explanation. The reader should be able to scan the heading tree and pick the exact node they want to read, without wading through a paragraph that mixes several ideas.

### 10.2 Heading depth

Use numbered hierarchical headings up to four levels deep when the structure calls for it:

- `# 1. Main Section` — top-level area (e.g. "The Agent Frame")
- `## 1.1 Sub-area` — a grouping inside the main section (e.g. "Memory — Two Categories, Four Types")
- `### 1.1.1 Item` — a member of the grouping (e.g. "Short-Term Memory")
- `#### 1.1.1.1 Sub-item` — a sub-type of an item (e.g. "Semantic Memory" inside "Long-Term Memory")

Go to four levels only when there is genuine sub-grouping (e.g. "long-term memory has three types" — long-term gets level 3, each type gets level 4). Do not pad with empty levels.

### 10.3 Per-item explanation

Each **leaf** heading is followed by a short prose explanation — typically two to four sentences. Long enough to actually explain the idea, short enough that one heading equals one bite-sized concept. No bullet dumps inside the explanation; use full sentences.

### 10.4 Repeated structure for compared items

When the section compares N options that share the same shape (e.g. three chunking strategies, three vector DBs, four prompting styles), give every option **the same set of sub-headings** so the comparison is easy to scan. Common patterns:

- **For strategies / techniques:** `How it works`, `Advantage`, `Disadvantage`.
- **For tools / vendors:** `What it is`, `Best for`, `Trade-off`.
- **For pipeline stages / steps:** numbered list of steps, each as its own sub-heading.

### 10.5 Tables

Use a small table only when it genuinely beats prose at conveying the comparison (e.g. a decision matrix like vector-DB picker, or a metrics-by-use-case grid). One or two tables per file is plenty. Do not table-dump every list.

### 10.6 Top of the summary file

Standard top-of-file structure from sections 3.1–3.3 still applies: `# Title`, then `## Topics Covered in This Document` index linking to each main section, then `---`, then the body.

### 10.7 What the summary is *not*

- **Not a glossary** — flat one-line entries per topic belong in a recap/cheatsheet, not in a summary. If the user wants that shape they will say "recap" or "cheatsheet".
- **Not flowing paragraphs** — paragraphs that mention three or four sub-items inline force the reader to scan prose to find one idea. Break the items out into their own headings instead.
- **Not bullet dumps** — within an explanation, write full sentences. Bullets are only for genuine enumerations the source itself enumerates.

### 10.8 Reference example

`week-three/week-two-summary.md` is the canonical example of this shape — read it before writing a new summary if the structure is unclear.
