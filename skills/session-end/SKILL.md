---
name: session-end
description: |
  Close a Claude Code session by documenting what was accomplished, updating CLAUDE.md with
  the current project structure, a session log entry, and a forward-looking todo list.
  Use at the end of any working session to maintain continuity across conversations.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# Session End

You are a session scribe. Your job is to close this working session cleanly by writing a structured record into CLAUDE.md so that the next session can pick up exactly where this one left off.

## When to Apply

Use this skill at the end of a working session to:
- Document what was accomplished and how problems were solved
- Update the project structure in CLAUDE.md to reflect current state
- Carry forward any unfinished todos and add new ones
- Leave a useful briefing for the next session

---

## Execution

### Step 1: Gather context

Run the following in parallel to understand the current state:
- `git log --oneline -15` — recent commits to summarize what changed
- `git status` — any uncommitted work to note
- Read the existing `CLAUDE.md` if it exists (to preserve prior sessions and todos)
- Read `README.md` if it exists (for project overview)

### Step 2: Ask the user

Ask the user one focused question:

> "Before I close the session — anything specific you want noted? Issues we hit, decisions we made, or todos for next time?"

Wait for their response. Merge it with what you've inferred from the git log.

### Step 3: Generate the project structure

Run a directory listing to produce an up-to-date file tree. Focus on:
- Top-level directories and their purpose
- Key files (entry points, config, main outputs)
- Skip: build artifacts, node_modules, .git, __pycache__, and other generated files

Format as an annotated tree:
```
project/
├── src/           — main source code
├── data/
│   ├── raw/       — never modified
│   └── final/     — analysis-ready
├── output/        — tables and figures
├── CLAUDE.md      — session log and project state
└── README.md      — project overview
```

### Step 4: Write CLAUDE.md

Write or update `CLAUDE.md` in the project root. Preserve all prior session entries. The file should follow this structure:

---

```markdown
# CLAUDE.md — [Project Name]

*Auto-maintained by /session-end. Read by /session-start.*

## Project Overview

[One paragraph: what this project is, its goal, the main stack/tools used.]

## Project Structure

[Annotated file tree from Step 3]

## Active Todos

- [ ] [todo item]
- [ ] [todo item]
<!-- Carry forward unchecked items from the previous version. Add new ones from this session. -->
<!-- Mark completed items with [x] and keep them for one session before removing. -->

## Session Log

### [YYYY-MM-DD] — Session N

**Summary:** [1–2 sentences: what was the main thrust of this session]

**Accomplished:**
- [specific thing done]
- [specific thing done]

**Issues solved:**
- [problem] → [how it was solved]

**Todos added:**
- [new todo items that came up this session]

---

[prior session entries below, oldest at bottom]
```

---

### Step 5: Confirm

Tell the user:
- Where CLAUDE.md was written
- The session number and date
- How many todos are active
- One sentence: what the next session should start with

---

## CLAUDE.md Maintenance Rules

- **Project structure**: always regenerated fresh from the actual directory — never stale
- **Todos**: carry all unchecked `[ ]` items forward; mark completed items `[x]` for one session, then drop them
- **Session log**: prepend new entries (newest first); keep all prior entries intact
- **Project overview**: update only if the project's scope or stack has changed
- **Do not truncate**: never delete prior session entries — they are the project memory
