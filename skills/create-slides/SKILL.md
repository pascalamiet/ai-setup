---
name: create-slides
description: |
  Scaffold a new LaTeX Beamer slide deck from a standard template.
  Use when: starting a new presentation and wanting a ready-to-compile
  Beamer project with pre-loaded math macros, color theming, section
  cards, appendix with frame-number reset, and a skeleton structure.
  Also covers rhetoric design, iterative compile-review-fix workflow,
  and multi-agent quality review for finished or in-progress decks.
license: MIT
metadata:
  author: custom
  version: "2.0.0"
---

# create-slides — LaTeX Beamer Scaffold & Design Guide

This skill does two things:
1. **Scaffold** a new slide deck from the standard template (Steps 1–5).
2. **Guide** the design, rhetoric, compile workflow, and quality review of any
   Beamer deck — whether freshly scaffolded or brought in from existing content.

## Usage

```
/create-slides [path]
```

`path` is the directory where the slides folder should be created.
If omitted, use `documents/slides/` relative to the current working directory.
If the target directory already exists and contains files, ask the user before overwriting.

If the user brings **existing content** (a paper, notes, a prior deck, or a
short research description), treat this as a redesign/generation task: scaffold
the template, then populate it with restructured content following the rhetoric
and design principles in this skill.

---

## Step 1 — Gather inputs

Ask the user for the following. Accept anything they provide and use sensible
defaults for anything left blank.

| Field | Prompt | Default |
|-------|--------|---------|
| `TITLE` | Full presentation title | `Untitled` |
| `SHORT_TITLE` | Short title for footer | *(first 4 words of title)* |
| `SUBTITLE` | Subtitle (optional) | *(omit subtitle line)* |
| `AUTHORS` | Author name(s), comma-separated | `Author` |
| `SHORT_AUTHORS` | Short author(s) for footer | *(last name(s) of authors)* |
| `INSTITUTIONS` | Institution per author (optional) | *(omit \inst{} lines)* |
| `VENUE` | Conference or seminar name | `[Venue]` |
| `DATE` | Presentation date | `\today` |
| `PRIMARY_COLOR` | Primary brand color as RGB hex (e.g. `#405C7E`) | `#405C7E` (steel blue) |
| `SECTIONS` | Top-level section names beyond the defaults (optional) | *(none)* |
| `MACROS` | Project-specific LaTeX macros (optional) | *(none)* |
| `AUDIENCE` | Who is this for? (e.g., "PhD seminar", "conference", "undergrads") | *(general academic)* |
| `SOURCE` | Existing content to restructure: paper, notes, prior deck (optional) | *(none)* |
| `CODE_LANG` | Code language for figures: R, Python, Stata (optional) | *(none)* |

If the user invokes the skill with a short description (e.g.
`/create-slides "DML and negative weights in DiD"`), treat that string as the
title and infer a draft subtitle and audience from it — tell the user what you assumed.

---

## Step 2 — Create the directory

```bash
mkdir -p <path>/figures
mkdir -p <path>/scripts
mkdir -p <path>/tables
```

Copy the Makefile template:

```bash
cp ~/.claude/skills/create-slides/Makefile <path>/Makefile
```

Standard output structure:

```
<path>/
├── slides.tex        # Main Beamer file
├── slides.pdf        # Compiled deck (after Step 4)
├── Makefile          # Build automation (make / make watch / make open / make clean)
├── figures/          # PNG/PDF figures — referenced as figures/FILENAME
├── scripts/          # Standalone R/Python/Stata scripts that generate figures
└── tables/           # .tex table fragments
```

---

## Step 3 — Copy and fill `slides.tex`

The canonical template lives at `~/.claude/skills/create-slides/template.tex`.
Copy it to `<path>/slides.tex`:

```bash
cp ~/.claude/skills/create-slides/template.tex <path>/slides.tex
```

Then edit the file in place:

**Placeholders** — every `\ph{NAME}` call renders as bold `[NAME]` in the PDF
(easy to spot during drafting). Replace them using the user's inputs:

| Placeholder | Replace with |
|-------------|-------------|
| `\ph{Full title}` | `TITLE` |
| `\ph{Short title}` | `SHORT_TITLE` |
| `\ph{Subtitle}` | `SUBTITLE` (or remove the `\subtitle{…}` line if omitted) |
| `\ph{Author One}`, `\ph{Author Two}`, … | Author names; add/remove `\and` blocks to match |
| `\ph{Short author(s)}` | `SHORT_AUTHORS` |
| `\ph{Institution One}`, `\ph{Institution Two}` | `INSTITUTIONS`; add/remove `\inst{}` lines to match, or remove all `\inst{}` markup if only one institution |
| `\ph{Venue}` | `VENUE` |
| `\ph{Full date, e.g. April 8, 2026}` | `DATE` |
| `\ph{Short date}` | short form of `DATE` (e.g. `April 2026`) |

**Colors** — convert the user's `PRIMARY_COLOR` hex to two RGB-in-[0,1] triples
and substitute them on the two `\definecolor` lines marked `% COLOR`:

```latex
\definecolor{PRIMARY}{rgb}{R, G, B}          % primary brand color
\definecolor{PRIMARY-light}{rgb}{R, G, B}    % lighter accent (~30% tint)
```

For the light accent, blend the primary color with white at roughly 35 %
(i.e. `light = primary × 0.65 + 1 × 0.35` per channel).

**Extra sections** — if the user requested additional sections, insert them
before `\section{Next Steps}`, each with a section-title card frame and at
least one content frame stub.

**Project-specific macros** — if supplied, insert them after
`% PROJECT-SPECIFIC MACROS -- add here` in the preamble.

**Populating from existing content** — if the user provided source material,
apply the rhetoric framework (see [Rhetoric Design](#rhetoric-design)) to
restructure it into slides before filling placeholders.

---

## Step 4 — Compile and review

### 4a — Code-first workflow (if figures are needed)

Always generate figures **before** inserting them. Never insert a placeholder
`\includegraphics` path that does not yet exist in `figures/`.

```
run script → verify PNG/PDF output → insert into slides.tex → compile
```

Save each figure script as a standalone file in `scripts/` so the user can
rerun it independently.

### 4b — Initial compile

```bash
cd <path> && latexmk -pdf -interaction=nonstopmode slides.tex
```

Report whether it succeeded. If it fails, show the first error from the log.

### 4c — Fix ALL compilation warnings

Check the log for and eliminate **every** instance of:
- Overfull hbox / underfull hbox
- Overfull vbox / underfull vbox

No matter how small or inconsequential they appear. These warnings mean LaTeX
is making layout compromises you did not authorize.

Recompile after fixing.

### 4d — Check for silent visual errors

**Compilation success does not mean visual success.** These problems do NOT
produce errors or warnings but ruin the deck:

**Tikz:**
- Shape size constraints forcing label misplacement
- Arrows pointing to wrong locations
- Coordinate systems misaligned

**Software-generated graphics (ggplot2, matplotlib, Stata):**
- Axis labels cut off or overlapping
- Legend placement obscuring data
- Text sizing inconsistent with slide aesthetic
- Coordinate / position constraints wrong

To check, explicitly ask: "Do the coordinate values match the intended visual
placement?" — do not assume the figure looks correct without verifying.

### 4e — Multi-agent review (for substantive decks)

For a full deck going to a seminar or conference, run two review passes after
the initial compile:

**Reviewer 1 (Rhetoric & Flow):** Evaluates narrative arc, MB/MC balance across
slides, technical rigor, and whether the argument structure follows the audience
type guidelines below.

**Reviewer 2 (Graphics Specialist):** Checks ONLY graphics — Tikz positioning
vs. intended positioning, ggplot/matplotlib label placement, numerical accuracy
in figures, coordinate/position constraint conflicts.

Incorporate feedback from both reviewers and recompile a final time.

---

## Step 5 — Report to the user

Confirm what was created and print the full file path to `slides.tex`.
Remind the user to:
- Replace remaining `\ph{…}` placeholders with real content
- Add figures to `figures/` and uncomment the `\includegraphics` lines
- Remove or repurpose stub frames they don't need
- Link appendix frames to main-deck frames via `\hypertarget` / `\hyperlink` pairs
- Run `latexmk -pdf slides.tex` (or open in their LaTeX editor) to compile

---

## Rhetoric Design

> Read `rhetoric.md` — it sits in the same directory as this SKILL.md file.
> It contains the full framework: Aristotelian modes, MB/MC optimization,
> visual grammar, common failures, and context-specific applications.
> Load it whenever you are populating slide content or reviewing a deck's
> argument structure. The summary below covers the most frequently needed rules.

### Narrative arc

Every presentation follows one of two patterns depending on audience:

**Academic research (seminars, conferences):**
```
Hook / motivation (10%)  →  Setup & literature (20%)  →  Method (30%)  →  Results (30%)  →  Conclusion & next steps (10%)
```

**General / applied audience:**
```
WHAT — hook, problem statement (10%)
WHY  — stakes, context, why now (30%)
HOW  — solution, method, evidence (50%)
CLOSE — takeaways, next steps (10%)
```

The hook comes first. Never open with definitions, background, or an agenda
slide before the audience knows why they should care.

### Slide-level rules

1. **One idea per slide.** If you need "and" in the title, split the slide.
2. **Titles as assertions,** not labels. "Estimates are robust to clustering"
   beats "Robustness checks."
3. **5–7 words per bullet.** Slides are speaking cues, not scripts.
4. **Visual over text.** A well-labeled figure beats three bullet points.
5. **Readable from the back.** Body text minimum 18pt; Beamer's defaults satisfy
   this — do not shrink fonts to fit more content.

### Cognitive load balance (MB/MC equivalence)

The goal is NOT to maximize information density. The goal is **smoothness**: a
consistent cognitive load throughout, so the audience isn't overwhelmed on
slide 8 and bored on slide 14.

**Allowed exception — "jump scares":** a deliberate, brief spike in density for
rhetorical effect (a striking statistic, a surprising result). These must be
*intentional*, not accidents of poor layout.

### Presentation types and timing

**Research seminar / conference (20–30 min):**
| Segment | Content | Time |
|---------|---------|------|
| Introduction | Motivation, question, contribution, lit | 5 min |
| Methodology | Setup, estimand, method | 7–8 min |
| Results | Main findings, robustness | 8–10 min |
| Conclusion | Summary, next steps | 2–3 min |
| Q&A | — | 5–10 min |

**PhD workshop / work-in-progress (45–60 min):**
Allocate more time to methodology and open questions; plan for longer discussion.

**Short talk / lightning (10 min):**
Lead with the result. One slide per: motivation, method, main finding, implication.

### Audience calibration

**PhD seminar:**
Assume strong technical background but varying exposure to your specific method.
Emphasize intuition alongside formal results. State the identification assumption
clearly and early.

**Conference (specialists):**
State identification strategy in slide 2. Key results need one clear figure each.
Skip derivations; cite the paper.

**Conference (mixed field):**
More context, less jargon. Lead with economic significance, not statistical.

**Undergraduate course:**
One concept per slide. Worked examples over proofs. Return to the motivating
question at the end of every section.

---

## Anti-patterns to avoid

- Opening with "Today I'm going to talk about…"
- Reading slides verbatim
- Agenda slide before the hook
- Shrinking font to fit more text
- More than one figure per slide (unless explicitly comparing two)
- Overfull/underfull warnings left in the log
- Appendix frames that advance the main slide counter
- Apologizing for preliminary results

---

## LaTeX & Beamer Conventions

- **Theme**: `Madrid` with a two-color palette (`PRIMARY` and `PRIMARY-light`).
- **Aspect ratio**: 16:9 (`aspectratio=169`).
- **Placeholder macro**: `\ph{NAME}` → bold `[NAME]` in the PDF. Delete the
  `\newcommand{\ph}` line once all placeholders are filled.
- **Appendix frame counter**: wrapped between `\backupbegin` / `\backupend` so
  appendix frames do not advance the main slide count.
- **Section title cards**: each `\section{}` is preceded by a centered section-title
  frame using `\color{PRIMARY}{\huge{Section Name}}`.
- **Figures**: always placed in `figures/` and referenced as
  `\includegraphics[width=…]{figures/FILENAME}` (no extension needed for PDF/PNG).
- **Math helpers pre-defined**: `\indep`, `\ind{}` (indicator).
- **Theorem environments**: `thm`, `pf`, `dfn`; block colors auto-switch to
  `PRIMARY` background inside `theorem` and `definition` environments.
- **Navigation buttons**: use `\hypertarget{label}{}` on target frames and
  `\hyperlink{label}{\beamergotobutton{Text}}` to link back from appendix slides.
- **Two-column layout**: use the `columns` environment with `[t]` alignment and
  `0.48\textwidth` columns for side-by-side content.
- **Bibliography**: cite inline as `\cite{}` or `\citet{}`; bibliography slide
  is optional — place in the appendix if included.
- **Build commands**: `make` (compile), `make watch` (auto-recompile on save),
  `make open` (compile + open PDF), `make clean` (remove aux files including
  Beamer's `.nav`, `.snm`, `.vrb`).
- **TikZ diagrams**: ready-to-paste snippets for DAGs, event study timelines,
  DiD 2×2 tables, methodology pipelines, and RD cutoff diagrams live in
  `tikz-snippets.tex` in the same directory as this SKILL.md. Read that file
  and copy the relevant snippet into the frame. Each snippet needs
  `\usetikzlibrary{...}` calls noted in its header comment — add them to the
  preamble if not already present.
