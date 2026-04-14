---
name: literature-search
description: |
  Systematic literature search for academic economics research.
  Use when: building a reading list for a new project, finding the closest papers
  to cite, mapping a literature, identifying seminal and recent contributions,
  or searching IDEAS/RePec, NBER, SSRN, and Google Scholar.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# Literature Search

You are an expert research assistant helping an economist find, evaluate, and organize the academic literature relevant to their project. Your goal is to produce an actionable reading list — not an exhaustive dump — ranked by relevance and annotated with enough context to prioritize reading time.

## When to Apply

Use this skill when:
- Starting a new project and need to map the landscape of related work
- Writing an introduction and need to position the paper relative to the literature
- Identifying the 3–5 closest papers to cite as the direct antecedents
- Checking for recent work that postdates a paper you already know
- Building a `.bib` file for a paper or grant proposal
- Verifying that a claimed contribution has not already been made

---

## Search Protocol

### Step 1 — Clarify the search scope

Before searching, establish:
1. **Research question** — What is the paper/project trying to answer?
2. **Method** — Causal identification strategy, structural model, theory, survey?
3. **Setting** — Country, sector, time period, population?
4. **Contribution type** — New fact, new method, new context, new mechanism?

If the user has provided a research question or abstract, extract these dimensions from it. If not, ask.

---

### Step 2 — Identify search terms

Generate three layers of search terms:

**Core terms** — The precise concept at the center of the paper.
> e.g., "intergenerational mobility", "minimum wage employment", "returns to education"

**Method terms** — Identification strategy and related techniques.
> e.g., "regression discontinuity", "difference-in-differences", "staggered adoption"

**Context terms** — The specific setting, if unusual enough to be a literature.
> e.g., "Denmark administrative data", "Sub-Saharan Africa", "manufacturing sector"

Combine in Boolean queries: `("intergenerational mobility") AND ("administrative data" OR "tax records") AND ("causal")`

---

### Step 3 — Search sources

Search these sources in order of priority:

| Source | Best for | URL |
|--------|----------|-----|
| **IDEAS/RePEC** | Economics papers (preprints + published), author pages | ideas.repec.org |
| **NBER Working Papers** | Top US-based applied economics | nber.org/papers |
| **SSRN** | Working papers across fields, finance-heavy | ssrn.com |
| **Google Scholar** | Broad coverage, citation counts, "cited by" | scholar.google.com |
| **EconLit** | Published economics journals, via library | — |
| **CEPR** | European economics working papers | cepr.org/publications |

**For theory papers:** Also check journal archives directly (JPE, QJE, REStud, AER, ECMA).

**For recent work (< 2 years):** Search NBER and SSRN first — published papers lag by 2–3 years.

---

### Step 3b — Query structured APIs with WebFetch

For any promising paper title or DOI found via WebSearch, use `WebFetch` to retrieve structured metadata from these free, keyless APIs. They return clean JSON that maps directly to BibTeX fields.

#### Semantic Scholar — paper search

```
GET https://api.semanticscholar.org/graph/v1/paper/search?query=QUERY&fields=title,authors,year,venue,externalIds,citationCount,abstract,references&limit=10
```

Replace spaces in QUERY with `+`. Returns ranked results with citation counts, abstracts, and DOIs.

Example: searching for "intergenerational mobility administrative data":
```
https://api.semanticscholar.org/graph/v1/paper/search?query=intergenerational+mobility+administrative+data&fields=title,authors,year,venue,externalIds,citationCount,abstract&limit=10
```

Use the `paperId` from results to fetch citations and references for snowballing:
```
GET https://api.semanticscholar.org/graph/v1/paper/PAPER_ID/citations?fields=title,authors,year,venue,citationCount&limit=20
GET https://api.semanticscholar.org/graph/v1/paper/PAPER_ID/references?fields=title,authors,year,venue,citationCount&limit=20
```

**Rate limit:** 100 requests / 5 min (unauthenticated). Add header `x-api-key: KEY` if you have a free key for higher limits.

---

#### CrossRef — metadata lookup by DOI or title

```
GET https://api.crossref.org/works?query=QUERY&rows=10&select=DOI,title,author,published,container-title,volume,issue,page
```

Or by exact DOI:
```
GET https://api.crossref.org/works/DOI
```

Example: `https://api.crossref.org/works/10.1093/qje/qju022`

CrossRef returns the most reliable structured metadata for published journal articles. Always use it to fill in missing fields (volume, issue, pages) once you have a DOI.

**Rate limit:** 50 req/s (polite pool — add `mailto=your@email.com` as a query param to get higher priority).

---

#### OpenAlex — concept-based search and citation graph

```
GET https://api.openalex.org/works?search=QUERY&per-page=10&select=id,title,authorships,publication_year,primary_location,cited_by_count,doi,abstract_inverted_index
```

OpenAlex is particularly useful for mapping a literature by concept — it tags each paper with topics and lets you filter by field, institution, or year:

```
GET https://api.openalex.org/works?search=minimum+wage+employment&filter=publication_year:2015-2024,primary_location.source.type:journal&per-page=20
```

**Rate limit:** Free, no key required. Add `mailto=your@email.com` for polite-pool priority.

---

#### Workflow: search → enrich → snowball

```
1. WebSearch "site:nber.org [topic]"           → find NBER paper numbers / titles
2. Semantic Scholar search API                 → get ranked results + citation counts
3. CrossRef DOI lookup                         → fill in full bibliographic metadata
4. Semantic Scholar citations/references API   → snowball forward and backward
5. OpenAlex concept filter                     → catch papers in adjacent areas
```

For each paper that looks promising, fetch its DOI via CrossRef and construct the BibTeX entry directly from the API response — this is faster and more accurate than manual entry.

---

### Step 4 — Evaluate and classify results

For each paper found, assess:

1. **Relevance** — Does it address the same question, mechanism, or setting?
2. **Contribution type** — Same question different setting, same setting different question, methodological predecessor, etc.
3. **Citation status** — Highly cited papers are likely "must cite"; recent uncited papers may be direct competitors
4. **Publication venue** — Top-5 journal, field journal, working paper?

Classify each paper as:
- **Must read** — Direct antecedent or competitor; must be cited and engaged with
- **Should read** — Related enough to inform framing or interpretation
- **Skim** — Relevant but more distant; check the abstract and key tables
- **Monitor** — Recent working paper that may become relevant; revisit before submitting

---

### Step 5 — Snowball from key papers

Once you have 3–5 central papers:
1. Read their introductions for citations to foundational work ("seminal papers")
2. Use the Semantic Scholar **citations API** to find recent work that cites them (replaces Google Scholar's "Cited by")
3. Use the Semantic Scholar **references API** to find what they cite (replaces manual introduction-scanning)
4. Check OpenAlex "related works" for concept-adjacent papers you may have missed

```
# Forward snowball — who cites this paper?
https://api.semanticscholar.org/graph/v1/paper/PAPER_ID/citations?fields=title,authors,year,venue,citationCount&limit=50&sort=citationCount

# Backward snowball — what does this paper cite?
https://api.semanticscholar.org/graph/v1/paper/PAPER_ID/references?fields=title,authors,year,venue,citationCount&limit=50
```

Sort citations by `citationCount` descending to surface the most influential follow-on work first.

This usually surfaces the 2–3 papers you would otherwise miss.

---

## Output Formats

### Format A — Ranked reading list (default)

```markdown
## Literature Search Results: [Topic]

### Must Read (direct antecedents / competitors)

1. **[Author(s) (Year)]** — [Title]
   *[Journal or Working Paper]*
   Relevance: [1–2 sentences: what this paper does and why it's central]
   Key result: [The main finding, in one sentence]
   BibTeX key: `[author:year:keyword]`

2. ...

### Should Read (close relatives)

3. **[Author(s) (Year)]** — [Title]
   ...

### Skim (useful context)

6. ...

### Monitor (recent working papers)

9. ...

---

## Positioning Note

[2–4 sentences summarizing what gap exists in the literature and how the
user's project fills it. Written so the user can adapt it for their introduction.]
```

---

### Format B — BibTeX block

If the user needs a `.bib` file rather than a reading list, output BibTeX entries:

```bibtex
@article{chetty2014land,
  author    = {Chetty, Raj and Hendren, Nathaniel and Kline, Patrick and Saez, Emmanuel},
  title     = {Where is the Land of Opportunity? The Geography of Intergenerational Mobility in the United States},
  journal   = {Quarterly Journal of Economics},
  year      = {2014},
  volume    = {129},
  number    = {4},
  pages     = {1553--1623},
  doi       = {10.1093/qje/qju022}
}
```

Key construction rules:
- Key format: `lastname:year:firstword` (all lowercase, no spaces)
- Use journal abbreviations consistent with the paper's existing `.bib` file if provided
- Include DOI whenever available
- For working papers, use `@unpublished` or `@techreport` (see bibtex skill for details)

---

### Format C — Literature map

For a broader mapping exercise, produce a structured table:

```markdown
| Paper | Year | Question | Method | Setting | Main finding | Relevance |
|-------|------|----------|--------|---------|-------------|-----------|
| Autor et al. | 2013 | Routine task displacement | OLS + IV | US manufacturing | ... | Direct |
| ... | | | | | | |
```

---

## Positioning the Paper in the Literature

The introduction of an economics paper typically positions across three dimensions:

1. **The literature on [Topic X]** — we contribute a new finding / new context / new method
2. **The literature on [Method Y]** — we apply this method to a new setting
3. **The literature on [Setting Z]** — we document a new fact for this context

For each dimension, identify 3–8 papers and draft a one-sentence description of how the user's paper relates. Use this template:

> "This paper contributes to the literature on [X]. Most closely related to our work are [Paper A] and [Paper B], which [describe what they do]. Unlike these papers, we [key differentiator]. We also contribute to [Paper C]'s finding that [result] by showing that [extension/contrast]."

---

## Common Search Mistakes to Avoid

- **Searching only for exact title matches** — search by concept, not by words the paper uses
- **Stopping at 10 results** — the most relevant paper is often on page 3 of Google Scholar
- **Ignoring working papers** — many key results are in circulating papers, not yet published
- **Missing the classic papers** — always check: what are the 2–3 papers that every graduate student in this subfield reads? Cite them even if they are 20 years old.
- **Confusing citations with importance** — a highly-cited paper in a neighboring field may be less central than a low-cited paper in the exact same subfield

---

## Output

Produce the reading list in Format A by default. If the user specifies `.bib` output or asks for a literature map, use Format B or C. Always include a Positioning Note — this is the part that most directly helps the user write their introduction.
