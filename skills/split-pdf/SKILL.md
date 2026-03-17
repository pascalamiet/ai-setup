---
name: split-pdf
description: |
  Deep-read an academic paper by splitting it into 4-page chunks and extracting structured
  notes across 8 dimensions. Use when: the user provides a PDF path or a paper search query
  and wants a thorough structured extraction (research question, method, data, findings, etc.).
  Also use for any paper too long to read in one pass.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# split-pdf — Deep-Read Academic Papers

You split a PDF into small chunks, read them in batches, and write structured reading notes incrementally. This prevents session crashes from token-heavy PDFs and produces richer notes than one-shot summarization.

## When Invoked

The user will provide either:
- A local file path: `/split-pdf path/to/paper.pdf`
- A search query: `/split-pdf "Gentzkow Shapiro 2014 competition newspapers"`

If invoked with no argument, ask the user what paper they want to read.

## Step 1 — Acquire the PDF

**Local file:** Use it directly. Do not copy or move it.

**Search query:** Use WebSearch to find the paper. Look for a direct PDF link (author website, NBER, SSRN, AER, journal page). Download it with:

```bash
curl -L -o "articles/<author_year_keyword>.pdf" "<url>"
```

Save to an `articles/` subdirectory relative to the current working directory. The original PDF must never be deleted.

## Step 2 — Split into 4-page chunks

```python
import os
from pypdf import PdfReader, PdfWriter

input_path = "articles/<filename>.pdf"
output_dir = "articles/split_<filename>/"
os.makedirs(output_dir, exist_ok=True)

reader = PdfReader(input_path)
total = len(reader.pages)
chunk = 4

for start in range(0, total, chunk):
    end = min(start + chunk, total)
    writer = PdfWriter()
    for i in range(start, end):
        writer.add_page(reader.pages[i])
    out = f"{output_dir}<stem>_pp{start+1}-{end}.pdf"
    with open(out, "wb") as f:
        writer.write(f)

print(f"Split {total} pages into chunks of {chunk}.")
```

Name chunks as `<stem>_pp1-4.pdf`, `<stem>_pp5-8.pdf`, etc. Install `pypdf` if missing (`pip install pypdf`).

## Step 3 — Create notes.md

Create `<output_dir>/notes.md` with this skeleton:

```markdown
# Reading Notes: "<Title>" (<Authors>, <Journal> <Year>)

## Status: In progress — pages X of Y read

---

## 1. Research question and importance

## 2. Intended audience

## 3. How they answer the question

## 4. Data sources and where they came from

## 5. Statistical methods

## 6. Findings

## 7. What is learned

## 8. Data availability and replication access
```

## Step 4 — Read in batches of 3 chunks (~12 pages)

Read exactly 3 split files at a time using the Read tool. After each batch:

1. **Update notes.md** — fill in or extend all 8 sections based on what was just read. Be specific: include equation numbers, coefficient estimates with standard errors, exact data source names, sample sizes, and page references. Do not compress — accumulate detail.
2. **Report to the user** — briefly state what pages were just read and what was found.
3. **Pause and ask** — "Continue to pages X–Y?" Wait for confirmation before proceeding.

If the user says to skip a section (e.g., "skip the appendix"), skip those splits and note the skip in notes.md.

## Step 5 — Finalize

After all chunks are read (or the user stops early):

1. Update the status line in notes.md to `Complete — all N pages read` (or note how far you got).
2. Report the output directory and notes.md path to the user.

## What to Extract (8 Dimensions)

Fill every section with specific, replicable detail — not summaries:

1. **Research question** — exact question, why it matters, what gap it fills
2. **Intended audience** — which sub-community, what literature it engages
3. **How they answer the question** — identification strategy, model structure, key assumptions
4. **Data** — every dataset by name, source, how it was obtained, unit of observation, sample size, time period
5. **Statistical methods** — estimators, key specifications, equation numbers, software
6. **Findings** — main results with specific numbers (coefficients, SEs, p-values, effect sizes)
7. **What is learned** — what is new relative to prior work; implications for the user's project if apparent
8. **Data availability and replication** — public data? replication archive? DOI? URLs? what would need to be re-collected?

## Directory Layout After Completion

```
articles/
├── smith_2024.pdf                    # original — never deleted
└── split_smith_2024/
    ├── smith_2024_pp1-4.pdf
    ├── smith_2024_pp5-8.pdf
    ├── ...
    └── notes.md
```

## Notes on Behavior

- **Papers under ~15 pages**: read directly without splitting; skip to structured extraction.
- **If the paper is not found online**: tell the user and ask them to provide a local file.
- **If a split file is corrupted or unreadable**: note it in notes.md and skip to the next batch.
- **Do not rush**: careful reading over fast reading. If a section is dense (structural model, identification), slow down and extract more detail.
