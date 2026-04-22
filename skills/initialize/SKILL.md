---
name: initialize
description: |
  Create a shared .ai/AI.md context file in the current working directory by
  inspecting the project, then create only the agent-specific symlinks the user
  needs (for example CLAUDE.md, AGENTS.md, GEMINI.md) based on a TOML config
  that also controls paths, behavior, content sections, and limits. Use when:
  starting an AI-assisted project, when the user says /initialize, or when they
  ask to set up persistent agent context files.
license: MIT
metadata:
  author: custom
  version: "1.2.0"
---

# initialize — Create Shared AI Context for This Project

When invoked, inspect the current project and produce a shared `.ai/AI.md` that gives future agent sessions an accurate, immediately useful briefing. Then create only the root-level symlinks needed for the enabled agents, pointing each of them at the configured shared context path.

## When to Apply

- `/initialize` is typed explicitly
- The user says "initialize this project", "set up AGENTS/CLAUDE/GEMINI files", "create a session file", etc.
- An agent-start workflow finds no usable project context file

---

## Execution

### Step 1: Resolve enabled agents

1. Read `skills/initialize/config.toml` and use it as the default source of truth for this skill.
2. Ensure the project has a `.ai/` directory.
3. If `.ai/config.toml` does not exist in the project and `behavior.create_if_missing = true`, create it by copying `skills/initialize/config.toml`.
4. Read `.ai/config.toml` and use it as the project-local source of truth for which symlinks to create, where to point them, what sections to include, and what limits to respect.
5. Do not ask the user which agents they use. The config file controls this behavior.

Only these agents are currently supported by this skill:

| Agent | Root symlink |
|------|--------------|
| Claude | `CLAUDE.md` |
| Codex | `AGENTS.md` |
| Gemini | `GEMINI.md` |

Config sections currently supported:

| Section | Purpose |
|------|---------|
| `[agents]` | Which root-level symlinks should exist |
| `[paths]` | Where the shared context file lives |
| `[behavior]` | Creation, overwrite, cleanup, and file-protection rules |
| `[sections]` | Which optional content blocks to include in `.ai/AI.md` |
| `[limits]` | Soft limits for todo count and target file length |

### Step 2: Gather project context (run all in parallel)

1. **Directory tree** — list top-level structure and key subdirectories (exclude `.git`, `node_modules`, `__pycache__`, build artifacts)
2. **README.md** — read if present
3. **Git history** — `git log --oneline -10` and `git status` (skip gracefully if not a git repo)
4. **Key config / manifest files** — read the first relevant one found: `pyproject.toml`, `setup.py`, `package.json`, `Makefile`, `*.Rproj`, `environment.yml` — just enough to infer stack and purpose
5. **Memory files** — read any relevant agent memory directories that exist (for example `~/.claude/projects/[project-path]/memory/`) to surface user preferences or prior decisions

### Step 3: Infer project type

Classify the project into one of:

| Type | Signals |
|------|---------|
| **Empirical research** | `data/`, `code/R/`, `code/stata/`, `scripts/`, `*.do`, `*.Rmd`, `*.ipynb` |
| **Theory paper** | `notes.md`, `literature/`, LaTeX files, no data scripts |
| **Software / package** | `src/`, `tests/`, `package.json`, `pyproject.toml`, CI config |
| **Mixed / other** | Combination of above |

The project type determines which optional sections to include (see Step 4).

### Step 4: Ask the user one focused question

If the project purpose is unclear from inspection alone, ask:

> "Quick question before I write `.ai/AI.md` — what is this project about in one sentence? (I can infer the structure but want to get the goal right.)"

If the purpose is obvious from README or files, skip this and proceed.

### Step 5: Write the shared context file

Use `paths.shared_context` as the output path for the shared context file. The default is `.ai/AI.md`. This file should contain the content that would normally go into the main project agent file. Fill every section from what you gathered — never leave placeholder text if real content is available.

Honor the config when deciding what to include:

- If `sections.include_stack = false`, omit `## Stack & Tools`
- If `sections.include_conventions = false`, omit `## Conventions`
- If `sections.include_core_ideas = false`, omit `## Core Ideas / Framework`
- If `sections.include_gemini_cli = false`, omit `## Using Gemini CLI for Large Context Analysis`
- If `sections.include_session_log = false`, omit `## Session Log`
- Cap inferred todos to roughly `limits.max_todos`
- Aim to keep the file near `limits.target_max_lines`

---

```markdown
# AI.md

*Shared project context for Claude, Codex, Gemini, and other coding agents.*

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

**Summary:** Initialized shared AI context from project inspection.

**Accomplished:**
- Created `.ai/AI.md`

**Issues solved:**
- (none)

**Todos added:**
- [same as Active Todos above]
```

---

### Step 6: Create or remove symlinks from `.ai/config.toml`

If `.ai/config.toml` did not exist, initialize it from `skills/initialize/config.toml`. The default bundled config is:

```toml
[agents]
claude = true
codex = true
gemini = false

[paths]
shared_context = ".ai/AI.md"

[behavior]
create_if_missing = true
remove_disabled_symlinks = true
overwrite_existing_symlinks = true
protect_regular_files = true

[sections]
include_stack = true
include_conventions = true
include_core_ideas = true
include_session_log = true
include_gemini_cli = true

[limits]
max_todos = 8
target_max_lines = 180
```

Interpret `.ai/config.toml` as follows:

- `paths.shared_context` is the symlink target path for enabled agents
- If `agents.claude = true`, ensure `CLAUDE.md` exists as a symlink to `paths.shared_context`
- If `agents.codex = true`, ensure `AGENTS.md` exists as a symlink to `paths.shared_context`
- If `agents.gemini = true`, ensure `GEMINI.md` exists as a symlink to `paths.shared_context`
- If any value is `false` and `behavior.remove_disabled_symlinks = true`, remove the corresponding root symlink if it exists and points to `paths.shared_context`

Use symlinks, not file copies. Prefer commands equivalent to:

```bash
mkdir -p .ai
ln -sfn .ai/AI.md CLAUDE.md
ln -sfn .ai/AI.md AGENTS.md
ln -sfn .ai/AI.md GEMINI.md
```

Honor the behavior flags:

- If `behavior.protect_regular_files = true`, do not overwrite a non-symlink context file that already contains user content
- If `behavior.overwrite_existing_symlinks = true`, you may repoint existing symlinks to `paths.shared_context`
- If `behavior.create_if_missing = false`, do not create `.ai/config.toml`; use the bundled config only for this run

If `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md` already exists as a regular file and `behavior.protect_regular_files = true`, stop and ask the user before replacing it.

### Step 7: Report to the user

Tell the user:
- That the shared context file was written, and where
- Which symlinks were created or removed
- How many todos are listed
- That the agent toggle file was read from or initialized into `.ai/config.toml`
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
- Keep the shared context file near `limits.target_max_lines`. Long context files are harder to maintain and slower to load.
- `skills/initialize/config.toml` defines the bundled defaults. `.ai/config.toml` is the per-project switchboard after initialization. Respect `.ai/config.toml` on every initialize run.
- The shared content in `.ai/AI.md` must remain agent-neutral. Do not add agent-specific instructions unless the user explicitly asks for them.
