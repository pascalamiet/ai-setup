---
name: wiki-init
description: |
  Initialize an LLM-maintained wiki knowledge base in the current project.
  Creates the full folder structure (wiki/_raw_/, wiki/_schema_/, wiki/_wiki_/),
  a SCHEMA.md with page conventions and workflows, an empty index.md, and a log.md.
  Optionally patches CLAUDE.md with a ## Wiki section containing the schema read instruction.
  Use when: starting a new wiki for a research project, reading notes, or any topic deep-dive.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# wiki-init — Initialize an LLM Wiki

When invoked, scaffold a complete LLM-maintained wiki in the current project directory.

## Usage

```
/wiki-init [wiki-dir]
```

- `wiki-dir` is optional. Defaults to `wiki/` in the current working directory.
- If a `wiki/` directory already exists with content, warn the user and ask before overwriting.

---

## Step 0 — Read the reference files (run in parallel)

Before doing anything else, read both files from the skill directory:

1. `~/.claude/skills/wiki-init/llm-wiki.md` — the full philosophy and pattern behind LLM wikis.
   Use this to understand the intent and make good judgment calls when adapting the schema.
2. `~/.claude/skills/wiki-init/SCHEMA.template.md` — the canonical schema template that will
   be copied into the new wiki. Do not regenerate it from scratch; copy and adapt this file.

Also check whether a `CLAUDE.md` exists in the current working directory, and if so read the
first 30 lines to learn the project name and domain.

---

## Step 1 — Create the directory structure

Create all three subdirectories (no placeholder files inside them):

```
<wiki-dir>/
├── _raw_/       ← raw sources: PDFs, markdown clips, exported notes
├── _schema_/    ← SCHEMA.md: the LLM's operating instructions
└── _wiki_/      ← all LLM-generated content pages
```

---

## Step 2 — Write `<wiki-dir>/_schema_/SCHEMA.md`

Start from the contents of `~/.claude/skills/wiki-init/SCHEMA.template.md` and make these
targeted adaptations — nothing more:

- Replace every `[PROJECT]` placeholder with the actual project name (from CLAUDE.md, or
  the current directory name if no CLAUDE.md exists)
- If the domain strongly suggests different page types (e.g. a fiction project needs
  `character-` and `location-` pages rather than `paper-`; a competitive-analysis project
  needs `company-` pages), adjust the Page Types table accordingly — but keep changes minimal
- Leave everything else exactly as in the template

---

## Step 3 — Write `<wiki-dir>/index.md`

```markdown
# Wiki Index — [PROJECT]

Master catalog of all pages. Updated on every ingest and whenever a new page is created.
Read this first when answering a query to find relevant pages.

---

*(No pages yet. Drop sources into `_raw_/` and run an ingest to get started.)*
```

---

## Step 4 — Write `<wiki-dir>/log.md`

Run `date +%Y-%m-%d` to get today's date. Use it in the entry.

```markdown
# Wiki Log — [PROJECT]

Append-only. Most recent entry first.
Format: `## [YYYY-MM-DD] <operation> | <description>`

---

## [TODAY] init | Wiki initialized

Created wiki structure: `_raw_/`, `_schema_/`, `_wiki_/`, `index.md`, `log.md`.
No pages yet. Drop sources into `_raw_/` and run an ingest to get started.
```

---

## Step 5 — Copy README.md into the wiki root

```bash
cp ~/.claude/skills/wiki-init/README.md <wiki-dir>/README.md
```

This gives the user a quick-reference guide directly inside the wiki directory.

---

## Step 6 — Patch CLAUDE.md (if it exists)


If a `CLAUDE.md` exists in the current working directory:

1. Check if it already contains a `## Wiki` section — if so, skip this step entirely
2. If not, append the following block:

```markdown
## Wiki

This project uses an LLM-maintained wiki at `<wiki-dir>/`. **Before any wiki operation
(ingest a source, answer a wiki query, lint the wiki), read `<wiki-dir>/_schema_/SCHEMA.md` first.**

```
<wiki-dir>/
├── _raw_/      — raw sources (PDFs, web clips, exported notes)
├── _schema_/   — SCHEMA.md: page conventions and workflows
├── _wiki_/     — all LLM-generated content pages
├── index.md    — master catalog
└── log.md      — append-only session log
```

No pages yet. Ingest sources from `<wiki-dir>/_raw_/` to build the wiki.
```

---

## Step 7 — Report to the user

Confirm what was created with a brief directory tree, whether CLAUDE.md was patched,
and the three next steps:

1. Drop source files (PDFs, markdown clips) into `<wiki-dir>/_raw_/`
2. Say "ingest `<wiki-dir>/_raw_/<filename>`" to process the first source
3. Optionally open `<wiki-dir>/_schema_/SCHEMA.md` to customize page types for this domain

---

## Quality Rules

- **Always read the template file** — never regenerate the schema from memory
- **Use today's actual date** — run `date +%Y-%m-%d` to confirm
- **Do not create pages** in `_wiki_/` — it starts empty
- **Do not overwrite** existing SCHEMA.md, index.md, or log.md without asking
- **Minimal adaptations only** — resist the urge to redesign the schema for each project;
  the template is battle-tested and the user can customize it themselves afterward
