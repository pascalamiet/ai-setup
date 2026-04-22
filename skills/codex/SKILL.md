---
name: codex
description: Use when you want Codex CLI in headless mode via `codex exec` for non-interactive coding, repository edits, code review, automation, structured output, or one-shot task execution from the shell.
---

# Codex

Use this skill when the task should be run non-interactively through Codex CLI rather than in the interactive TUI.

## Core role

- Use `codex exec "..."` for one-shot headless runs.
- Pass the working directory with `-C` when the task is repo-specific.
- Use stdin when the prompt is long or generated dynamically.
- Use `--json` or `-o` when the output needs to be captured by another tool.
- Prefer safe sandbox settings; avoid bypass flags unless the environment is already externally sandboxed.

## Workflow

1. Identify the exact task that should run in headless mode.
2. Build a focused `codex exec` prompt with the relevant context, constraints, and output format.
3. Choose the right execution options for sandboxing, working directory, and output capture.
4. Run `codex exec`.
5. Review the result, then summarize or apply follow-up steps as needed.

## Prompting guidance

- State the concrete task first, then the constraints.
- Ask for a specific output shape when the result will be consumed by another process.
- Keep each call focused on one unit of work.
- Include file paths, errors, and expected behavior directly in the prompt when relevant.
- Split multi-step jobs into multiple calls when you need better control or validation between steps.

## Common patterns

- Direct prompt:
  `codex exec -C /path/to/repo "Find the failing test, fix the bug, and explain the change briefly."`
- Prompt from stdin:
  `cat prompt.txt | codex exec -C /path/to/repo -`
- Capture the final message:
  `codex exec -C /path/to/repo -o result.txt "Review the latest changes for regressions."`
- Stream machine-readable events:
  `codex exec -C /path/to/repo --json "Summarize the architecture of this package."`
- Run outside a git repo:
  `codex exec --skip-git-repo-check -C /tmp "Create a small Python script that prints primes under 100."`

## Quality bar

- Do not use interactive-only assumptions; `codex exec` must be fully specified up front.
- Prefer `-C`, `--sandbox`, and `--add-dir` over fragile shell setup.
- Avoid `--dangerously-bypass-approvals-and-sandbox` unless there is an explicit reason and an external sandbox.
- If the task needs structured output, ask for it explicitly and use `--output-schema`, `--json`, or `-o` where appropriate.
- Sanity-check any code or edits before relaying them as final.
