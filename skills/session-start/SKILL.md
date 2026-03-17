---
name: session-start
description: |
  Open a Claude Code session by reading all relevant .md files and reconstructing project context
  from CLAUDE.md, README.md, memory files, and recent git history. Use at the start of any
  working session to resume exactly where the last session left off.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# Session Start

You are a session loader. Your job is to rapidly reconstruct the full project context from persisted files so you can resume work immediately — without the user having to re-explain anything.

## When to Apply

Use this skill at the start of a working session to:
- Load the project state from CLAUDE.md and other .md files
- Review recent git history to understand what changed
- Surface active todos and the last session's open threads
- Present a concise briefing so work can resume without preamble

---

## Execution

### Step 1: Load all context files in parallel

Read the following simultaneously:
- `CLAUDE.md` in the current directory — primary source of truth for project state
- `README.md` in the current directory — project overview and setup
- Any `.md` files in the project root (e.g., `NOTES.md`, `DESIGN.md`, `TODO.md`)
- Memory files at `~/.claude/projects/[project-path]/memory/` if they exist

If `CLAUDE.md` does not exist, note this and proceed with what's available.

### Step 2: Check recent git history

Run:
```bash
git log --oneline -10
git status
```

Note any uncommitted changes or recent commits not yet reflected in CLAUDE.md.

### Step 3: Present the briefing

Output a structured briefing — concise, no padding. Format:

---

**Project:** [name]
**Last session:** [date from CLAUDE.md, or "no prior session found"]

**Where we left off:**
[1–3 sentences synthesizing the last session's summary and any open threads]

**Active todos:**
- [ ] [item]
- [ ] [item]
[List all unchecked todos from CLAUDE.md]

**Recent commits** *(since last session or last 5):*
- `abc1234` — commit message
- `def5678` — commit message

**Uncommitted changes:** [none / list of modified files]

**Ready.** What would you like to work on?

---

### Step 4: Await instruction

Do not start any work until the user responds. The briefing is the output — not the beginning of a task.

---

## Fallback: No CLAUDE.md Found

If there is no `CLAUDE.md`:

1. Read `README.md` and any other `.md` files present
2. Run `git log --oneline -10` and `git status`
3. Run a quick directory scan to understand the project structure
4. Present what you found and note:

> "No CLAUDE.md found — this may be a new session or the file hasn't been created yet. Run `/session-end` at the end of this session to start tracking."

Then proceed normally.

---

## Notes

- Be brief. The briefing should fit in a single screenful.
- Don't summarize files verbatim — synthesize.
- If todos are ambiguous, list them as-is and let the user clarify.
- If memory files contain relevant context (user preferences, prior decisions), surface anything directly relevant to the current project.
