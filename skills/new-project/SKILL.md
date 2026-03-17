---
name: new-project
description: |
  Scaffold a new empirical research project with a standard directory structure.
  Use when: the user starts a new research project and wants consistent folder layout,
  a CLAUDE.md copied from the permanent template, and a generated README.md.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# new-project — Standard Project Scaffold

When invoked, create a new research project directory with a consistent structure.

## Usage

```
/new-project <project-name>
```

If no name is given, ask the user for one.

## Step 1 — Create the directory structure

```bash
mkdir -p <project-name>/{code/{R,python,stata},data/{raw,clean},output/{tables,figures},documents,decks,notes,progress_logs}
```

## Step 2 — Copy CLAUDE.md from the permanent template

```bash
cp ~/mixtapetools/claude/CLAUDE.md <project-name>/CLAUDE.md
```

If the template does not exist at that path, tell the user and skip this step. Do not create a placeholder.

## Step 3 — Generate README.md

Create `<project-name>/README.md` with the following content, filling in the project name:

```markdown
# <project-name>

## Research question

_To be filled in._

## Status

_In progress._

## Collaborators

_To be filled in._

## Directory structure

```
<project-name>/
├── CLAUDE.md              # Research rules & estimation philosophy (permanent template)
├── README.md              # This file — project-specific notes
├── code/
│   ├── R/                 # R scripts
│   ├── python/            # Python scripts
│   └── stata/             # Stata do-files
├── data/
│   ├── raw/               # Original source data — never modify
│   └── clean/             # Cleaned and merged datasets
├── output/
│   ├── tables/            # Generated tables (LaTeX, CSV)
│   └── figures/           # Generated figures (PDF, PNG)
├── documents/             # Outside papers and PDFs
├── decks/                 # Beamer presentations
├── notes/                 # Scratch notes and ideas
└── progress_logs/         # Session logs for continuity across Claude conversations
```
```

## Step 4 — Report to the user

Confirm the directory was created and list the top-level structure. Remind the user to:
- Fill in the research question and collaborators in `README.md`
- Start a progress log in `progress_logs/` at the end of each session

## Conventions to enforce

- `data/raw/` is **read-only**. Scripts read from it; nothing writes to it.
- `data/clean/` holds everything transformed, merged, or constructed.
- `progress_logs/` files are named `YYYY-MM-DD_description.md`. They exist so a new Claude session can pick up exactly where the last one left off.
- `documents/` holds outside PDFs (papers, referee reports, data documentation). Use `/split-pdf` to read long ones.
- `decks/` holds Beamer presentations built with the rhetoric-of-decks philosophy: assertion titles, one idea per slide.
