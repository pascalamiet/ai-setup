---
name: promptify
description: Use when rough voice-typed English needs to be rewritten into a polished, paste-ready prompt for Claude Code, Codex, or similar AI workflows. Preserve intent, remove filler and repetition, improve grammar and structure, and return only the final prompt as plain text.
---

# Promptify

Use this skill for one job: turn messy voice-typed English into a clean prompt ready to paste into Claude Code, Codex, or another AI assistant workflow.

## Output contract

- Return only the final prompt.
- Return plain text only.
- Do not wrap the result in a code block.
- Do not add commentary before or after the prompt.
- Preserve the user's original intent exactly.
- Remove filler, repetition, and speech artifacts.
- Fix grammar and awkward phrasing.
- Reorder content only when it improves clarity without changing meaning.
- Keep the result concise but complete.
- Do not invent requirements.
- If an assumption is unavoidable, label it explicitly as `Assumption:`.

## Style guidance

- Optimize for a general-purpose AI assistant prompt.
- Prefer direct task language.
- Make constraints explicit.
- Separate the main task from supporting details when useful.
- Keep the final prompt visually clean and easy to paste.

## Default structure

When helpful, organize the prompt as:

1. Main task
2. Constraints
3. Relevant context
4. Expected output

Do not force structure when the source text is short.
