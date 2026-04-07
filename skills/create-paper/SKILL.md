---
name: create-paper
description: |
  Scaffold a new LaTeX economics paper from a standard template.
  Use when: starting a new research paper and wanting a ready-to-compile
  LaTeX project with pre-loaded math macros, theorem environments,
  bibliography style, and a skeleton structure.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# create-paper — LaTeX Paper Scaffold

When invoked, gather a few inputs from the user and create a ready-to-compile
LaTeX paper project.

## Usage

```
/create-paper [path]
```

`path` is the directory where the paper folder should be created.
If omitted, use `documents/paper/` relative to the current working directory.
If the target directory already exists and contains files, ask the user before overwriting.

---

## Step 1 — Gather inputs

Ask the user for the following. Accept anything they provide and use sensible
defaults for anything left blank.

| Field | Prompt | Default |
|-------|--------|---------|
| `TITLE` | Paper title | `Untitled` |
| `AUTHORS` | Author name(s), comma-separated | `Author` |
| `ABSTRACT` | One-paragraph abstract or research idea description | *(leave placeholder)* |
| `KEYWORDS` | 3–5 keywords, comma-separated | `keyword one, keyword two, keyword three` |
| `ACKNOWLEDGEMENTS` | Acknowledgements text | `I thank ...` |
| `MACROS` | Project-specific LaTeX macros (optional) | *(none)* |
| `SECTIONS` | Extra top-level sections beyond the defaults (optional) | *(none)* |

If the user invokes the skill with a short research description (e.g.
`/create-paper "DML and negative weights in DiD"`), treat that string as the
title and infer a draft abstract from it — tell the user what you assumed.

---

## Step 2 — Create the directory

```bash
mkdir -p <path>
```

---

## Step 3 — Copy and fill `main.tex`

The canonical template lives at `~/.claude/skills/create-paper/template.tex`.
Copy it to `<path>/main.tex`:

```bash
cp ~/.claude/skills/create-paper/template.tex <path>/main.tex
```

Then edit the file in place, substituting all `ALLCAPS` placeholders with the
user's inputs. Format AUTHORS using `\and` between names
(e.g. `Pascal Amiet \and Co-Author`).
Format KEYWORDS as a comma-separated list.
If the user supplied project-specific macros, insert them after the comment
`% PROJECT-SPECIFIC MACROS -- add here`.
If the user requested extra sections, insert them before `\section{Conclusion}`.

The template content for reference:

````latex
% ============================================================
%  PAPER TEMPLATE
%  Replace all ALLCAPS placeholders with project-specific content.
%  Sections marked [OPTIONAL] can be deleted if not needed.
% ============================================================

\documentclass[english, 12pt, a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{natbib}
\usepackage[english]{babel}
\usepackage{lmodern}
%\usepackage{subfigure}
\usepackage[top=1.25in, bottom=1.25in, left=1.25in, right=1.25in]{geometry}
\usepackage[pdftex]{graphicx}
\usepackage{verbatim}
%\usepackage[width=0.8\textwidth]{caption}
\usepackage{amsmath,amssymb,amsopn,amsthm,dsfont,mathrsfs,bm}
\usepackage{float,placeins,flafter,longtable,array,booktabs}
\usepackage{color}
\usepackage{booktabs}
\usepackage{threeparttable}
\usepackage{blindtext}
\usepackage[hidelinks]{hyperref}

\usepackage{xr}
\makeatletter

% ----------------------------------------------------------------
% THEOREM ENVIRONMENTS
% ----------------------------------------------------------------
\newtheorem{thm}{Theorem}
\newtheorem{cor}{Corollary}
\newtheorem{prop}{Proposition}
\newtheorem{lem}{Lemma}
\newtheorem{hyp}{Assumption}
\newtheorem{mydef}{Definition}
\newtheorem{remark}{Remark}[section]

% ----------------------------------------------------------------
% MATH MACROS  (add project-specific macros below the line)
% ----------------------------------------------------------------
\vfuzz2pt
\hfuzz2pt

\newcommand{\norm}[1]{\left\Vert#1\right\Vert}
\newcommand{\abs}[1]{\left\vert#1\right\vert}
\newcommand{\set}[1]{\left\{#1\right\}}
\newcommand{\interieur}[1]{\stackrel{\circ}{#1}}
\newcommand{\ind}[1]{\mathds{1}\left\{#1\right\}}
\renewcommand{\S}{\mathcal{S}}
\newcommand{\B}{\mathcal{B}}
\newcommand{\C}{\mathcal{C}}
\newcommand{\E}{E}
\newcommand{\V}{V}
\newcommand{\R}{\mathbb R}
\newcommand{\N}{\mathbb N}
\newcommand{\Z}{\mathbb Z}
\newcommand{\eps}{\varepsilon}
\newcommand{\deriv}[2]{\partial #1/\partial #2}
\newcommand{\Deriv}[2]{\frac{\partial #1}{\partial #2}}
\newcommand{\convL}{\stackrel{d}{\longrightarrow}}
\newcommand{\M}{\mathcal{M}}
\newcommand{\cl}{\text{cl}}
\newcommand{\sgn}{\text{sgn}}
\newcommand{\tr}{\text{tr}}
\newcommand{\Cov}{\text{Cov}}
\newcommand{\Corr}{\text{Corr}}
\newcommand{\Supp}{\text{Supp}}
\newcommand{\indep}{\perp \!\!\! \perp}
\def\CI{\text{CI}_{1-\alpha}}
\def\CR{\text{CR}_{1-\alpha}}
\newcommand{\bleu}[1]{\textcolor{blue}{#1}}
\newcommand{\convP}{\stackrel{P}{\longrightarrow}}
\newcommand{\convAS}{\stackrel{a.s.}{\longrightarrow}}
\newcommand{\convD}{\stackrel{d}{\longrightarrow}}
\newcommand{\convNor}[1]{\stackrel{d}{\longrightarrow} \mathcal{N}\left(0,#1\right)}
\allowdisplaybreaks

% PROJECT-SPECIFIC MACROS -- add here
% MACROS_PLACEHOLDER

% ----------------------------------------------------------------

\setlength{\parindent}{0pt}
\linespread{1.3}
\bibliographystyle{chicago}
\date{\today}

\begin{document}

% ----------------------------------------------------------------
% TITLE PAGE
% ----------------------------------------------------------------

\title{TITLE\thanks{ACKNOWLEDGEMENTS}}

\author{AUTHORS}

\maketitle
%~\vspace{-1cm}
%\hspace{5cm} \large{\textit{Preliminary and Incomplete}}

%\vspace{2cm}
\begin{abstract}
ABSTRACT
\smallskip

\textbf{Keywords:} KEYWORDS

\end{abstract}

\newpage

% ----------------------------------------------------------------
% INTRODUCTION
% ----------------------------------------------------------------
\section{Introduction}

% ----------------------------------------------------------------
% SETUP / MODEL
% ----------------------------------------------------------------
\section{Setup}

\subsection{Setting}

\subsection{Estimand}

% ----------------------------------------------------------------
% MAIN RESULTS
% ----------------------------------------------------------------
\section{Main Results}

\subsection{Main Result}

\begin{thm}[Main Theorem]
    \label{thm:main}
    % theorem statement
\end{thm}

\begin{proof}
    See Appendix~\ref{proof:main}.
\end{proof}

% ----------------------------------------------------------------
% SIMULATIONS  [OPTIONAL]
% ----------------------------------------------------------------
\section{Simulations}   % [OPTIONAL]

% ----------------------------------------------------------------
% EMPIRICAL APPLICATION  [OPTIONAL]
% ----------------------------------------------------------------
\section{Empirical Application}   % [OPTIONAL]

% ----------------------------------------------------------------
% CONCLUSION
% ----------------------------------------------------------------
\section{Conclusion}

% ----------------------------------------------------------------
% REFERENCES
% ----------------------------------------------------------------
\newpage
\bibliography{references}

% ----------------------------------------------------------------
% APPENDIX
% ----------------------------------------------------------------
\appendix

\newpage
\setcounter{page}{1}
\begin{center}
    {\huge Online Appendix}
\end{center}

\section{Proofs}
\label{proof:main}

% Proof of Theorem~\ref{thm:main}.

\section{Additional Results}   % [OPTIONAL]

% Additional tables, figures, or robustness checks.

\end{document}
````

---

## Step 4 — Copy and clean `references.bib`

The canonical template lives at `~/.claude/skills/create-paper/template.bib`.
Copy it to `<path>/references.bib`:

```bash
cp ~/.claude/skills/create-paper/template.bib <path>/references.bib
```

Then open the file and remove all existing entries (they are from an unrelated
project). Leave only the header comment:

```bibtex
% ============================================================
%  BIBLIOGRAPHY
%  Add BibTeX entries here.
% ============================================================
```

If the user mentioned any specific papers or cited works in their inputs,
add those as BibTeX stubs (with `% TODO: fill in` comments on each field).

---

## Step 5 — Try to compile (optional)

If `latexmk` is available on the system, offer to do a test compile:

```bash
cd <path> && latexmk -pdf -interaction=nonstopmode main.tex
```

Report whether it succeeded. If it fails, show the first error from the log.
Do not run this step without asking first.

---

## Step 6 — Report to the user

Confirm what was created and print the full file path to `main.tex`.
Remind the user to:
- Fill any remaining `% TODO` stubs in `references.bib`
- Add project-specific macros near the `% PROJECT-SPECIFIC MACROS` comment
- Delete `[OPTIONAL]` sections they don't need
- Run `latexmk -pdf main.tex` (or open in their LaTeX editor) to compile

---

## Conventions

- The bibliography style is `chicago` (natbib). Use `\cite{}`, `\citet{}`, `\citep{}`.
- Theorem-like environments available: `thm`, `cor`, `prop`, `lem`, `hyp`, `mydef`, `remark`.
- Commonly used math shorthands already defined: `\E`, `\R`, `\eps`, `\ind{}`, `\Cov`,
  `\indep`, `\convP`, `\convD`, `\norm{}`, `\abs{}`, `\set{}`.
- Line spacing is 1.3; paragraph indent is off — use `\medskip` / `\bigskip` between paragraphs if needed.
- Color helper: `\bleu{text}` renders in blue — useful for draft comments.
