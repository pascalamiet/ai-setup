---
name: writing-setup
description: |
  Build a writing-style workflow from prior `.tex` files so the AI can draft in a consistent tone,
  structure sections similarly across papers, and optionally generate markdown evaluation reports.
  Use when: setting up AI-assisted academic writing from existing drafts/published examples.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# writing-setup — Learn Style from `.tex` and Assist Drafting

Use this skill to set up a reusable writing workflow where the AI learns from your previous papers and then helps draft new text in the same style.

## Goal

1. Learn your writing style from prior `.tex` files
2. Keep tone and structure consistent across new drafts
3. Optionally produce feedback as `.md` evaluation files

## Recommended Project Layout

Create and use this structure in your project:

```text
writing/
├── corpus/
│   ├── own/          # your old drafts/papers (.tex)
│   └── reference/    # high-quality published papers (.tex or extracted text)
├── drafts/           # new sections generated with AI
├── evaluations/      # optional AI feedback reports (.md)
└── STYLE_GUIDE.md    # synthesized style profile
```

If files are currently scattered, first collect all relevant `.tex` files into `writing/corpus/own/`.

## Setup Workflow

### Step 1 — Ingest style corpus

- Read all `.tex` files in `writing/corpus/own/`
- Read selected high-quality examples in `writing/corpus/reference/`
- Prioritize well-written, final or near-final versions over rough notes

### Step 2 — Build a style profile

Create `writing/STYLE_GUIDE.md` with:

- preferred tone (direct, formal, assertive, cautious)
- section structure patterns (intro flow, results narrative, conclusion style)
- paragraph rhythm (sentence length, transitions, signposting)
- citation and LaTeX conventions
- recurring phrases to prefer/avoid
- a short “Do / Don’t” checklist

### Step 3 — Draft with style constraints

When drafting a new section:

1. State target section and purpose
2. Reuse the structure conventions from `STYLE_GUIDE.md`
3. Produce draft text in `writing/drafts/<section>.md`
4. Run a quick self-check against the Do/Don’t checklist

## Optional Feedback Mode (Evaluation Files)

If feedback is requested, generate:

`writing/evaluations/YYYY-MM-DD_<section>-evaluation.md`

Template:

```markdown
# Writing Evaluation — <section>

## Overall fit to style guide
- Score: X/10
- One-paragraph diagnosis

## Dimension scores
- Tone consistency: X/10
- Structure consistency: X/10
- Clarity and flow: X/10
- Concision: X/10

## Most important edits
1. ...
2. ...
3. ...

## Revised sample paragraph
...

## Next-pass checklist
- [ ] ...
- [ ] ...
```

## Guardrails

- Preserve the author’s argument and technical content
- Do not copy phrasing from reference papers verbatim
- Flag uncertainty instead of inventing claims or citations
- Prefer concrete edits over generic writing advice

## References

- Paul G. P. — Writing & Thinking with AI Assistance: https://paulgp.substack.com/p/writing-and-thinking-with-ai-assistance
- Han Lu Long — econ-writing-skill: https://github.com/hanlulong/econ-writing-skill
