---
name: initialize
description: |
  Create a CLAUDE.md file in the current working directory by inspecting the
  project and generating a populated, accurate project context file.
  Use when: starting Claude Code in a directory that has no CLAUDE.md, or when
  the user says /initialize or asks to initialize / set up the session file.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# initialize — Create CLAUDE.md for This Project

When invoked, inspect the current project and produce a `CLAUDE.md` that gives future Claude sessions an accurate, immediately useful briefing.

## When to Apply

- `/initialize` is typed explicitly
- The user says "initialize this project", "set up CLAUDE.md", "create a session file", etc.
- `session-start` is run and finds no `CLAUDE.md`

---

## Execution

### Step 1: Gather project context (run all in parallel)

1. **Directory tree** — list top-level structure and key subdirectories (exclude `.git`, `node_modules`, `__pycache__`, build artifacts)
2. **README.md** — read if present
3. **Git history** — `git log --oneline -10` and `git status` (skip gracefully if not a git repo)
4. **Key config / manifest files** — read the first relevant one found: `pyproject.toml`, `setup.py`, `package.json`, `Makefile`, `*.Rproj`, `environment.yml` — just enough to infer stack and purpose
5. **Memory files** — read `~/.claude/projects/[project-path]/memory/` if they exist, to surface any user preferences or prior decisions

### Step 2: Infer project type

Classify the project into one of:

| Type | Signals |
|------|---------|
| **Empirical research** | `data/`, `code/R/`, `code/stata/`, `scripts/`, `*.do`, `*.Rmd`, `*.ipynb` |
| **Theory paper** | `notes.md`, `literature/`, LaTeX files, no data scripts |
| **Software / package** | `src/`, `tests/`, `package.json`, `pyproject.toml`, CI config |
| **Mixed / other** | Combination of above |

The project type determines which optional sections to include (see Step 4).

### Step 3: Ask the user one focused question

If the project purpose is unclear from inspection alone, ask:

> "Quick question before I write CLAUDE.md — what is this project about in one sentence? (I can infer the structure but want to get the goal right.)"

If the purpose is obvious from README or files, skip this and proceed.

### Step 4: Write CLAUDE.md

Write `CLAUDE.md` in the current directory using the template below. Fill every section from what you gathered — never leave placeholder text if real content is available.

---

```markdown
# CLAUDE.md

*Auto-maintained by /session-end. Read by /session-start.*

## Project Overview

[One paragraph: research question or software goal, current status, main tools / language stack. Be specific — bad: "a research project about welfare". Good: "Theory paper deriving regret bounds for distributional EWM estimators (S-Gini objective). Ideas stage, no code yet. Will use R for simulations."]

## Project Structure

[Annotated directory tree. Include all top-level dirs/files. Add a short comment after each entry explaining its role.]

## Stack & Tools

[List languages, frameworks, key packages, and any unusual tooling. Skip if obvious from structure. Examples: "R (fixest, ggplot2), LaTeX, GitHub Actions CI" or "Python 3.12, PyTorch 2, uv for deps".]

<!-- OPTIONAL — include for empirical/software projects: -->
## Conventions

[Any project-specific rules: naming conventions, where to write outputs, code style, data immutability rules, etc. Start with the most important ones. 3–6 bullet points max.]

<!-- OPTIONAL — include for research projects: -->
## Core Ideas / Framework

[For theory or empirical research: the central model, estimand, or approach in 3–8 bullet points. This is the intellectual core that future sessions need to understand quickly. Include key equations only if they fit on one line.]

## Active Todos

- [ ] [todo inferred from README, notes, git history, or user input]
<!-- Add as many as you can infer. Better to have too many than none. -->

## Using Gemini CLI for Large Context Analysis

When analyzing large codebases or multiple files that might exceed context limits, use the Gemini CLI with its massive context window via `gemini -p`.

**File/directory inclusion syntax** (paths relative to where you run the command):
```bash
gemini -p "@src/main.py Explain this file"                        # single file
gemini -p "@src/ @tests/ Analyze test coverage"                   # multiple dirs
gemini -p "@./ Give me an overview of this entire project"        # full project
gemini --all_files -p "Analyze the project structure"             # alternative flag
```

**Use `gemini -p` when:**
- Analyzing entire codebases or large directories
- Comparing multiple large files
- Understanding project-wide patterns or architecture
- Files total more than ~100 KB
- Verifying whether specific features, patterns, or security measures are implemented across the codebase

## Session Log

### [YYYY-MM-DD] — Session 1 (init)

**Summary:** Initialized CLAUDE.md from project inspection.

**Accomplished:**
- Created CLAUDE.md

**Issues solved:**
- (none)

**Todos added:**
- [same as Active Todos above]
```

---

### Step 5: Report to the user

Tell the user:
- That CLAUDE.md was written
- How many todos are listed
- One sentence on what's missing or what they should fill in manually (e.g., "The core framework section is a placeholder — fill in your model once you've settled on it.")

---

## Quality Rules

- **Never leave `[placeholder]` text** if real content can be inferred. Inspect files to fill sections.
- **Project Structure must be accurate** — regenerate from the actual directory, not from memory.
- **Todos must be actionable** — "Set up data pipeline" is good. "Do research" is not.
- **Session Log entry date** — use today's actual date (check `date` if unsure).
- **Stack section** — omit entirely if the project has no code yet (pure ideas stage).
- **Conventions section** — omit for pure theory/ideas projects; include for any project with code or data.
- **Core Ideas section** — include for research projects; omit for pure software projects.
- Keep the file under ~180 lines. Long CLAUDE.md files are harder to maintain and slower to load.
