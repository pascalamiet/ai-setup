# initialize

The `initialize` skill sets up shared project context for multiple coding agents
from one canonical file.

## What it creates

When run in a project, the skill can create:

- `.ai/AI.md` as the shared project context
- `.ai/config.toml` as the project-local configuration
- root-level symlinks such as `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` pointing to `.ai/AI.md`

This keeps one editable context file while still matching the filenames
expected by different tools.

## Configuration

Bundled defaults live in [`config.toml`](./config.toml). After initialization,
the project gets its own `.ai/config.toml`, which becomes the local source of
truth.

The config currently supports:

- `[agents]` to enable or disable agent-specific symlinks
- `[paths]` to set the shared context path
- `[behavior]` to control creation, cleanup, overwrite, and safety behavior
- `[sections]` to control optional content blocks in the generated context
- `[limits]` for soft limits such as todo count and target file length

## Default flow

1. Read bundled defaults from `skills/initialize/config.toml`
2. Create `.ai/config.toml` in the target project if needed
3. Inspect the project and write shared context to `.ai/AI.md`
4. Create or remove symlinks according to `.ai/config.toml`

## Why this exists

Without this pattern, users often end up maintaining duplicate context in
multiple files such as `CLAUDE.md` and `AGENTS.md`. This skill avoids that by
keeping the real content in one place and exposing the expected filenames as
symlinks.
