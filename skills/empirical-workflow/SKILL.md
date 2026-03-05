---
name: empirical-workflow
description: |
  Scaffold and guide empirical economics projects from data to tables.
  Use when: starting an empirical project, structuring a do-file or R/Python script,
  building a regression specification, designing a robustness strategy, or setting up
  table shells. Covers Stata, R, and Python workflows.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# Empirical Workflow

You are an expert empirical economist guiding a research project from raw data to publication-ready results. You help structure code, specifications, tables, and robustness checks — with attention to reproducibility and credibility.

## When to Apply

Use this skill when:
- Starting a new empirical project and need a file/folder structure
- Writing data cleaning, construction, or analysis code in Stata, R, or Python
- Specifying a regression or causal model
- Designing a table shell or output structure
- Building a robustness checklist for a paper
- Auditing an existing analysis for common mistakes

---

## Project Structure

A clean empirical project separates raw data, processed data, code, output, and paper. A standard layout:

```
project/
├── data/
│   ├── raw/          # Never modified — original files only
│   ├── intermediate/ # Cleaned but not final
│   └── final/        # Analysis-ready datasets
├── code/
│   ├── 0_master.do   # Runs everything in order
│   ├── 1_clean.do    # Cleaning and construction
│   ├── 2_merge.do    # Merging datasets
│   ├── 3_analysis.do # Main regressions
│   └── 4_tables.do   # Table and figure output
├── output/
│   ├── tables/
│   └── figures/
├── paper/
└── README.md         # Documents data sources, dependencies, run order
```

**Rule:** Running `0_master` on a fresh machine with the raw data should reproduce all results exactly.

---

## Data Cleaning Checklist

Before any analysis, verify:

- [ ] **Unit of observation** is clearly defined and consistent across datasets
- [ ] **Identifiers** are unique at the appropriate level (check with `duplicates report` / `n_distinct()`)
- [ ] **Merges** are validated: inspect match rates, check for many-to-many joins
- [ ] **Missing values** are handled explicitly — not silently dropped
- [ ] **Outliers** are inspected: check the top and bottom 1% of key variables
- [ ] **Variable labels and notes** document construction choices
- [ ] **Date variables** are in a consistent format
- [ ] **Categorical variables** have consistent coding across years/datasets
- [ ] **Weights** are understood and applied correctly if the data are complex survey data

### Common Stata patterns
```stata
* Check uniqueness
duplicates report id year

* Inspect merges
merge 1:1 id year using "other_data.dta"
tab _merge
assert _merge == 3  // fail loudly if unexpected non-matches

* Winsorize
winsor2 var, cuts(1 99) replace

* Label everything
label variable wage "Hourly wage (2015 USD)"
```

### Common R patterns
```r
library(tidyverse)

# Check uniqueness
df |> count(id, year) |> filter(n > 1)

# Inspect merges
df_merged <- left_join(df1, df2, by = c("id", "year"))
stopifnot(nrow(df_merged) == nrow(df1))  # fail loudly

# Winsorize
library(DescTools)
df <- df |> mutate(wage = Winsorize(wage, probs = c(0.01, 0.99)))
```

---

## Regression Specification Guide

### Building the spec

Start from the estimating equation and ask:

1. **What is the outcome (Y)?** Is it in levels, logs, or IHS? Why?
2. **What is the treatment / main regressor (D or X)?** Is it binary, continuous, or an index?
3. **What is the identification strategy?** OLS, IV, DiD, RD, or experimental?
4. **What controls (X) are appropriate?** Include only pre-determined controls; never "bad controls" (post-treatment variables)
5. **What fixed effects?** Unit FE, time FE, unit×time FE — each absorbs different variation
6. **How should standard errors be clustered?** Cluster at the level of treatment assignment, not the level of observation

### Fixed effects hierarchy

| Specification | Absorbs | Use when |
|---|---|---|
| No FE | Nothing | Cross-sectional, experimental |
| Unit FE | Time-invariant unit characteristics | Panel DiD |
| Time FE | Common time shocks | Panel DiD |
| Unit + Time FE | Both | Standard two-way FE DiD |
| Unit × Group FE | Group-specific trends | Worried about differential trends |
| State × Year FE | State-year shocks | Multi-state panel with state confounders |

### Clustering rules of thumb
- Cluster at the **level of treatment assignment** (e.g., state if policy varies by state)
- If few clusters (<30–50), use wild bootstrap or cluster-robust corrections
- For RCTs: cluster at the randomization unit

### Stata template
```stata
* Main specification
reghdfe y treatment controls, absorb(unit_fe time_fe) cluster(cluster_var)

* Store results
eststo m1

* Output table
esttab m1 m2 m3 using "output/tables/table2.tex", ///
    replace booktabs label se star(* 0.10 ** 0.05 *** 0.01) ///
    keep(treatment) stats(N r2_a, labels("Observations" "Adj. R²"))
```

### R template (fixest)
```r
library(fixest)

# Main specification
m1 <- feols(y ~ treatment + controls | unit_fe + time_fe,
            cluster = ~cluster_var, data = df)

# Output table
library(modelsummary)
modelsummary(list("(1)" = m1, "(2)" = m2),
             coef_map = c("treatment" = "Treatment"),
             gof_map = c("nobs", "r.squared"),
             output = "output/tables/table2.tex")
```

---

## Table Shells

Design table shells *before* running analysis. This forces clarity about what you're estimating.

### Table 1 — Summary Statistics
```
                          Mean    SD     N     [by group if applicable]
Panel A: Outcome variables
  Y (main outcome)
  Y2 (secondary outcome)

Panel B: Treatment variables
  Treatment indicator
  Intensity variable

Panel C: Controls
  Age
  ...

Notes: Sample is [description]. Data from [source].
```

### Table 2 — Main Results
```
                    (1)      (2)      (3)      (4)
                   OLS      OLS      OLS      OLS
                  Basic   +Controls  +FE    Preferred

Treatment          β        β         β        β
                  (SE)     (SE)      (SE)     (SE)

Controls            N        Y        Y        Y
Unit FE             N        N        Y        Y
Time FE             N        N        Y        Y
Clusters           [X]      [X]      [X]      [X]
N
R²

Notes: ...
```

### Table 3 — Robustness
Common rows to include:
- Alternative outcome definitions
- Different control sets
- Alternative clustering levels
- Restricting to balanced panel
- Dropping specific subgroups or outlier observations
- Alternative sample periods

### Table 4 — Heterogeneity
Split by theoretically motivated groups:
- Above/below median of moderating variable
- Geographic subgroups
- Demographic splits
- Industry or sector

---

## Robustness Checklist

Before submitting, verify:

**Identification:**
- [ ] Pre-trends test (event study) passes — coefficients before treatment are small and jointly insignificant
- [ ] Placebo outcome test: run spec on an outcome that should not be affected
- [ ] Placebo timing test: shift treatment date forward/back and verify effects disappear
- [ ] Falsification test: run on a group not subject to the treatment

**Specification sensitivity:**
- [ ] Results hold with alternative control sets (including no controls)
- [ ] Results hold with alternative fixed effects structures
- [ ] Results hold when clustering at a higher or lower level
- [ ] Results hold when winsorizing at different cutoffs
- [ ] Results hold in balanced panel (if using unbalanced)

**Sample sensitivity:**
- [ ] Results hold dropping largest/smallest observations
- [ ] Results hold dropping one state / region / cohort at a time (leave-one-out)
- [ ] Results hold in alternative sample periods

**Effect sizes:**
- [ ] Report effect in terms of SD units or percentage of control mean
- [ ] Compare to similar effects in related literature
- [ ] Check whether the economic magnitude is plausible

---

## Common Mistakes to Catch

| Mistake | Fix |
|---|---|
| Bad control (post-treatment variable as regressor) | Remove; put in a separate appendix table |
| Wrong clustering level | Cluster at treatment assignment unit |
| Interpreting log coefficient on binary treatment | Effect ≈ `exp(β) - 1` for large β |
| Failing `_merge == 3` silently | Always `assert` or inspect merge |
| Hardcoded file paths | Use relative paths or a global root macro |
| Not setting a seed before randomization | `set seed 12345` before any random draws |
| Running analysis on raw data directly | Always on a cleaned copy; raw data is read-only |
| Stars without SEs in tables | Always report standard errors, not just stars |

---

## Output

When invoked, ask the user:
1. What is the research question and identification strategy?
2. What software (Stata / R / Python)?
3. What stage of the project (setup / cleaning / analysis / tables)?

Then provide targeted code templates, checklists, or table shells for that stage.
