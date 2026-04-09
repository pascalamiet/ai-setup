# promptify

`promptify` is a small utility skill for turning rough voice-typed English into a clean, paste-ready prompt.

It is useful when you want to speak or quickly dump an idea first, then hand the cleaned prompt to Claude Code, Codex, or another AI assistant.

## What it does

- preserves the original intent
- removes filler, repetition, and speech artifacts
- fixes grammar and awkward phrasing
- returns only the final prompt as plain text

## Intended use

Use this skill when the input is messy natural language and the output should be a polished prompt.

Typical cases:

- voice dictation
- rushed brainstorming notes
- half-formed task descriptions
- prompt cleanup before handing work to another agent

## Codex workflow

If you are using Codex, a simple workflow is:

1. write `promptify:` and paste or dictate your rough text
2. let the skill return one cleaned prompt as plain text
3. run `/copy`
4. paste the copied result into Claude Code, Codex, or another AI tool

Example:

```text
promptify:
[your rough voice-typed English]
```

Then:

```text
/copy
```

The canonical behavior lives in `SKILL.md`.
