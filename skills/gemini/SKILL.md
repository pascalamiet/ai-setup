---
name: gemini
description: Use when you want Gemini CLI to gather external information, research a topic, fact-check a claim, find recent papers or developments, or clarify concepts that may require knowledge beyond the current local context.
---

# Gemini

Use this skill when the task is primarily research: current developments, background explanation, fact-checking, paper discovery, or idea exploration.

## Core role

- Use `gemini -p "..."` as an external research tool.
- Prefer focused prompts over one overloaded prompt.
- Ask for structured output, sources, paper titles, authors, or dates when useful.
- Synthesize Gemini's output instead of forwarding it raw.
- Attribute substantive findings to Gemini.

## Workflow

1. Identify the exact information gap.
2. Write one or more precise Gemini prompts.
3. Run `gemini -p "..."`.
4. If the first response is weak, narrow or reformulate the prompt and try again.
5. Present a concise synthesis with caveats where needed.

## Prompting guidance

- State the topic and the user's actual goal.
- Ask for lists, comparisons, timelines, or summaries explicitly.
- For academic searches, request years, authors, and key contributions.
- For ambiguous questions, clarify before querying.
- For multi-part requests, split the work into multiple calls.

## Example prompts

- `gemini -p "Explain the difference between Sinkhorn divergence and entropic optimal transport. Give mathematical intuition and practical implications."`
- `gemini -p "List recent papers from 2022 onward on LLM embeddings for statistical testing. Include authors and one-line contributions."`
- `gemini -p "What are the latest algorithmic advances in entropic optimal transport? Focus on methods rather than applications."`

## Quality bar

- Do not pretend Gemini is authoritative if the answer looks uncertain or dated.
- Surface uncertainty when queries return conflicting or incomplete results.
- Keep terminology precise, especially for academic or technical topics.
- If the task requires live web verification and Gemini output alone is insufficient, say so.
