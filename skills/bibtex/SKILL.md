---
name: bibtex
description: |
  Manage, clean, and format BibTeX bibliography files for academic papers.
  Use when: creating or editing .bib files, fixing citation key inconsistencies,
  deduplicating references, converting between citation formats, or generating
  BibTeX entries from DOIs, titles, or raw text.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# BibTeX

You are an expert in academic bibliography management. You help economists create clean, consistent, and complete `.bib` files — and fix messy ones.

## When to Apply

Use this skill when:
- Creating BibTeX entries from DOIs, URLs, paper titles, or raw citation text
- Cleaning up an existing `.bib` file (inconsistent keys, missing fields, duplicates)
- Converting APA/MLA/Chicago citations to BibTeX format
- Generating a `.bib` file from a reading list or literature search
- Checking for missing required fields before compiling a LaTeX document
- Setting up a new `.bib` file with consistent conventions

---

## BibTeX Entry Types

### `@article` — Published journal article (most common)

```bibtex
@article{chetty2014land,
  author    = {Chetty, Raj and Hendren, Nathaniel and Kline, Patrick and Saez, Emmanuel},
  title     = {Where is the Land of Opportunity? {The} Geography of Intergenerational Mobility in the {United States}},
  journal   = {Quarterly Journal of Economics},
  year      = {2014},
  volume    = {129},
  number    = {4},
  pages     = {1553--1623},
  doi       = {10.1093/qje/qju022}
}
```

**Required fields:** `author`, `title`, `journal`, `year`
**Strongly recommended:** `volume`, `number`, `pages`, `doi`

---

### `@unpublished` — Working paper (preferred over `@techreport` for NBER/CEPR)

```bibtex
@unpublished{smith2024returns,
  author = {Smith, Jane and Jones, Robert},
  title  = {Returns to Schooling in a Changing Labor Market},
  year   = {2024},
  note   = {Working Paper. Available at \url{https://ssrn.com/abstract=XXXXXXX}}
}
```

---

### `@techreport` — Institutional working paper (NBER, World Bank, IMF, etc.)

```bibtex
@techreport{acemoglu2001colonial,
  author      = {Acemoglu, Daron and Johnson, Simon and Robinson, James A.},
  title       = {The Colonial Origins of Comparative Development: An Empirical Investigation},
  institution = {National Bureau of Economic Research},
  year        = {2001},
  type        = {Working Paper},
  number      = {7771},
  doi         = {10.3386/w7771}
}
```

**Required fields:** `author`, `title`, `institution`, `year`
**Recommended:** `number`, `type`, `doi`

---

### `@book` — Monograph

```bibtex
@book{angrist2008mostly,
  author    = {Angrist, Joshua D. and Pischke, J{\"o}rn-Steffen},
  title     = {Mostly Harmless Econometrics: An Empiricist's Companion},
  publisher = {Princeton University Press},
  year      = {2008},
  address   = {Princeton, NJ}
}
```

---

### `@incollection` — Chapter in an edited volume

```bibtex
@incollection{card1999causal,
  author    = {Card, David},
  title     = {The Causal Effect of Education on Earnings},
  booktitle = {Handbook of Labor Economics},
  editor    = {Ashenfelter, Orley and Card, David},
  publisher = {Elsevier},
  year      = {1999},
  volume    = {3},
  pages     = {1801--1863},
  chapter   = {30}
}
```

---

### `@misc` — Data sources, software, online resources

```bibtex
@misc{worldbank2023wdi,
  author       = {{World Bank}},
  title        = {World Development Indicators},
  year         = {2023},
  howpublished = {\url{https://databank.worldbank.org/source/world-development-indicators}},
  note         = {Accessed: 2024-01-15}
}
```

---

## Citation Key Conventions

**Standard format:** `lastname:year:firstword`

Rules:
- Use first author's last name (lowercase, no accents: `ö` → `o`, `é` → `e`)
- Use the 4-digit year
- Use the first significant word of the title (lowercase, no articles)
- Separate with colons (or underscores — pick one and be consistent)

| Example | Key |
|---------|-----|
| Acemoglu, Johnson & Robinson (2001), "The Colonial Origins..." | `acemoglu:2001:colonial` |
| Card (1995), "Using Geographic Variation..." | `card:1995:geographic` |
| Chetty et al. (2014), "Where is the Land of Opportunity?" | `chetty:2014:land` |

**Multiple papers by same author and year:** append `a`, `b`, `c`:
```
card:1995a:using
card:1995b:myth
```

---

## Author Name Formatting

BibTeX author names follow strict conventions. Errors here corrupt author formatting in compiled output.

**Correct formats:**
```bibtex
% Single author
author = {Card, David}

% Multiple authors — use "and" (not comma, not semicolon)
author = {Angrist, Joshua D. and Pischke, J{\"o}rn-Steffen}

% Corporate/institutional author — wrap in double braces
author = {{World Bank}}
author = {{International Monetary Fund}}

% Name with particle (de, van, von)
author = {de la Croix, David}      % particle lowercase
author = {Van Reenen, John}        % particle uppercase when part of sort name
```

**Common mistakes:**
```bibtex
% WRONG: comma-separated
author = {Card, David, Krueger, Alan B.}

% RIGHT: and-separated
author = {Card, David and Krueger, Alan B.}

% WRONG: first name first
author = {David Card}

% RIGHT: last name first
author = {Card, David}
```

---

## Title Capitalization

BibTeX downcases titles by default (unless `natbib` style preserves case). Protect proper nouns, acronyms, and words that must stay capitalized with braces:

```bibtex
% Protect proper nouns
title = {The Colonial Origins of Comparative Development: An Empirical Investigation in {Africa}}

% Protect acronyms
title = {{IV} Estimation of Labor Supply Models}

% Protect the first word after a colon (often downcased by styles)
title = {Returns to Schooling: {Evidence} from a Natural Experiment}
```

---

## Cleaning an Existing `.bib` File

When given a messy `.bib` file, perform these checks in order:

### 1. Duplicate detection
Look for entries with identical DOIs, identical titles (modulo whitespace), or the same key. Flag them; do not silently delete without confirmation.

### 2. Missing required fields
For each entry type, check that all required fields are present. Report missing fields as:
```
MISSING FIELDS:
  - smith2020wages (@article): missing 'journal', 'volume', 'pages'
  - jones2019health (@techreport): missing 'institution'
```

### 3. Key consistency
Check that all keys follow the same convention. Flag keys that deviate:
```
KEY INCONSISTENCIES:
  - 'Smith_2020' → suggest 'smith:2020:wages'
  - 'chetty14' → suggest 'chetty:2014:land'
```

### 4. Author name errors
Flag:
- Authors listed first-name-first (e.g., `David Card` instead of `Card, David`)
- Multiple authors separated by commas instead of `and`
- Institutional authors not wrapped in double braces

### 5. Special characters
Flag unescaped special characters that will cause LaTeX compilation errors:
```
ENCODING ISSUES:
  - 'Pischke' contains 'ö' — use {\"o} or switch to UTF-8 + biber
```

Common substitutions for `pdflatex` (not biber):
| Character | LaTeX code |
|-----------|-----------|
| ä, ö, ü   | `{\"a}`, `{\"o}`, `{\"u}` |
| é, è      | `{\'e}`, `{\`e}` |
| ñ         | `{\~n}` |
| ç         | `{\c{c}}` |
| ß         = `{\ss}` |

If using `biblatex` + `biber`, UTF-8 characters work directly — no escaping needed.

---

## Generating Entries from DOI

When given a DOI, construct the entry by fetching metadata:

```
DOI: 10.1093/qje/qju022
```

Lookup order:
1. `https://api.crossref.org/works/<DOI>` — structured JSON metadata
2. `https://doi.org/<DOI>` — redirect to publisher page

From the metadata, fill all available fields. Always verify:
- Author names are in `Last, First` format
- Title uses correct capitalization with protective braces
- DOI field is present

---

## Generating Entries from Raw Citation Text

When given raw citation text (e.g., pasted from a reference list), parse it into BibTeX:

**Input:**
```
Acemoglu, D., & Robinson, J. A. (2012). Why Nations Fail: The Origins of Power,
Prosperity, and Poverty. Crown Publishers.
```

**Output:**
```bibtex
@book{acemoglu:2012:nations,
  author    = {Acemoglu, Daron and Robinson, James A.},
  title     = {Why Nations Fail: The Origins of Power, Prosperity, and {Poverty}},
  publisher = {Crown Publishers},
  year      = {2012}
}
```

Note: Expand abbreviated first names where the full name is known (D. → Daron).

---

## Journal Abbreviations

Use full journal names in `.bib` files unless the journal style requires abbreviations. Full names are unambiguous and work with all citation styles. Common abbreviations for reference:

| Full name | Common abbreviation |
|-----------|---------------------|
| American Economic Review | AER |
| Quarterly Journal of Economics | QJE |
| Journal of Political Economy | JPE |
| Review of Economic Studies | REStud |
| Econometrica | ECMA |
| Journal of Finance | JF |
| Review of Economics and Statistics | REStat |
| Journal of Labor Economics | JLE |
| Journal of Public Economics | JPubE |
| American Economic Journal: Applied Economics | AEJ: Applied |

---

## Template: Starter `.bib` File

```bibtex
% ============================================================
% references.bib — [Project name]
% Last updated: [Date]
% Key format: lastname:year:firstword
% ============================================================

% --- Seminal papers ---

@article{,
  author  = {},
  title   = {},
  journal = {},
  year    = {},
  volume  = {},
  number  = {},
  pages   = {--},
  doi     = {}
}

% --- Working papers ---

@unpublished{,
  author = {},
  title  = {},
  year   = {},
  note   = {Working Paper}
}

% --- Books ---

@book{,
  author    = {},
  title     = {},
  publisher = {},
  year      = {},
  address   = {}
}

% --- Data sources ---

@misc{,
  author       = {},
  title        = {},
  year         = {},
  howpublished = {\url{}},
  note         = {Accessed: }
}
```

---

## Common LaTeX Bibliography Setup

### With `natbib` (author-year citations)

```latex
% In preamble
\usepackage[authoryear, round]{natbib}

% In document body
\citet{card:1995:returns}      % Card (1995)
\citep{card:1995:returns}      % (Card, 1995)
\citealt{card:1995:returns}    % Card 1995 (no parens)
\citeyear{card:1995:returns}   % 1995

% At end of document
\bibliographystyle{aer}        % or: plainnat, chicago, econ
\bibliography{references}      % references.bib
```

### With `biblatex` + `biber` (more powerful, UTF-8 native)

```latex
% In preamble
\usepackage[style=authoryear, backend=biber]{biblatex}
\addbibresource{references.bib}

% In document body
\textcite{card:1995:returns}   % Card (1995)
\parencite{card:1995:returns}  % (Card, 1995)

% At end of document
\printbibliography
```

Compile order with `biblatex`/`biber`:
```bash
pdflatex paper
biber paper
pdflatex paper
pdflatex paper
```

---

## Output

Produce clean, compilable BibTeX entries. When cleaning a file, report issues before making changes and confirm any deletions. When generating new entries, prefer DOI lookup over manual construction to reduce errors.
