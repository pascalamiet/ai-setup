---
name: claude
description: Use when you want Claude CLI to handle a reasoning-heavy or coding-heavy task such as algorithm design, difficult debugging, code review, architecture analysis, mathematical derivation, or a carefully structured technical explanation.
---

# Claude

Use this skill when the task benefits from Claude's depth on reasoning, coding, derivations, or long-form technical explanation.

## Core role

- Use `claude -p "..."` for hard reasoning or coding tasks.
- Provide the relevant code, errors, constraints, and desired output format directly in the prompt.
- Keep each call focused on one hard problem.
- Review and synthesize Claude's output before presenting it.
- Attribute substantive reasoning or proposed solutions to Claude.

## Workflow

1. Confirm the task is reasoning-heavy or coding-heavy.
2. Build a precise prompt with all necessary local context.
3. Run `claude -p "..."`.
4. Check the response for completeness and plausibility.
5. If needed, make a targeted follow-up call.
6. Present a cleaned-up synthesis to the user.

## Prompting guidance

- Specify whether you want code, debugging help, derivation, critique, or explanation.
- Paste only the relevant code or error output.
- Ask for numbered steps or annotated code when structure matters.
- Split multi-part work into separate Claude calls.
- For tricky reasoning, explicitly ask for a step-by-step explanation.

## Example prompts

- `claude -p "Design a memory-efficient streaming k-means algorithm for data that does not fit in RAM. Give pseudocode and analyze time and space complexity."`
- `claude -p "Review this async Python code for race conditions and deadlock risks: [paste code]"`.
- `claude -p "Derive the gradient of cross-entropy loss with respect to the logits, step by step."`
- `claude -p "Explain this Rust borrow-checker error and propose the minimal safe fix: [paste code and error]"`.

## Quality bar

- Do not use Claude for tasks that depend on live internet access or current events.
- Sanity-check proposed code before relaying it.
- Flag skipped steps in a derivation if the explanation is too compressed.
- If the answer is truncated or vague, retry with a narrower prompt.
