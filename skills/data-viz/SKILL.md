---
name: data-viz
description: |
  Guide for creating publication-quality figures for academic papers and presentations.
  Use when: making charts, plots, or figures in R (ggplot2), Python (matplotlib/seaborn),
  or Stata; asking about figure design principles; preparing output for journals or slides.
license: MIT
metadata:
  author: custom
  version: "1.0.0"
---

# Data Visualization for Academic Work

You are an expert in data visualization for academic economics and social science. Your goal is to produce publication-quality figures: honest, clear, and precise. You know the conventions of top journals, the design principles behind good charts, and the code to implement them in R, Python, and Stata.

## When to Apply

Use this skill when:
- Making a figure for a paper, thesis chapter, or presentation
- Choosing the right chart type for a given data structure
- Applying journal-specific formatting requirements
- Debugging or improving an existing plot
- Building event study plots, coefficient plots, maps, or distribution figures
- Asking how to make a figure look more professional

---

## Core Design Principles

### 1. Every element must earn its place
Remove anything that does not convey information: unnecessary gridlines, 3D effects, chartjunk, redundant legends, decorative borders. Tufte's data-ink ratio: maximize the share of ink devoted to data.

### 2. Choose the right chart type
| Data structure | Chart type |
|---|---|
| Distribution of one variable | Histogram, density, CDF, violin |
| Two continuous variables | Scatter, binscatter, regression fit |
| Time series | Line chart |
| Coefficients + CIs | Coefficient plot (dot + whisker) |
| Event study / DiD | Event study plot with CIs |
| Categorical comparison | Bar chart (horizontal preferred), dot plot |
| Heterogeneity across subgroups | Faceted panels or grouped dot plot |
| Maps / geographic data | Choropleth (with careful color scale) |
| Joint distribution | Binscatter, hexbin, contour |

**Avoid:** pie charts (use bar), 3D plots (use 2D), dual y-axes (use facets or normalize), stacked bars when the message is about individual components.

### 3. Axes and scales
- **Always label axes** with variable name and units
- **Start y-axis at zero** for bar charts showing totals; not required for line charts showing change
- **Log scales** when data spans orders of magnitude or when proportional change is the story
- **Avoid truncated axes** that exaggerate small differences
- **Tick marks** should be round numbers; 4–6 ticks is usually right

### 4. Color
- Use color purposefully: to encode a dimension, not for decoration
- **Sequential palettes** (low → high): `viridis`, `Blues`, `YlOrRd` — for continuous variables
- **Diverging palettes**: `RdBu`, `PRGn` — for data with a meaningful midpoint (e.g., positive/negative)
- **Qualitative palettes**: `Set1`, `Okabe-Ito`, `ColorBrewer` — for categorical groups
- **Colorblind-safe**: always use Okabe-Ito or viridis for multi-group figures
- **Grayscale check**: does the figure still work if printed in black and white?
- Max 4–5 colors in a single figure; use shape or linetype as a second channel

### 5. Text and typography
- **Font size**: axis labels ≥ 11pt, tick labels ≥ 9pt; ensure readability at print size
- **Figure title**: informative, not generic ("Effect of X on Y by subgroup" not "Figure 3")
- **Notes**: include data source, sample definition, and what error bars represent
- **Annotations** > legends: when possible, label lines/groups directly on the figure

### 6. Error bars and uncertainty
- Always show uncertainty for estimates: 95% CI standard; add 90% CI for significance reading
- For coefficient plots: show both 90% and 95% CI (different line widths or colors)
- State in the note what the bars represent: "Bars represent 95% confidence intervals"
- **Never** show error bars without explaining them

---

## Journal-Specific Requirements

### General economics journals (AER, QJE, JPE, RES, Econometrica)
- Figures in black and white or grayscale (color often allowed online, but check)
- EPS or PDF format preferred; TIFF at 300+ DPI accepted
- Figure dimensions: usually max width ~6 inches (single column) or 6.5 inches (full page)
- No figure title in the figure itself — caption goes in the paper
- Caption ends with period

### Health/applied journals (JAMA, NEJM, AEJ series)
- Color often allowed but must be colorblind-safe
- Specific font requirements (check journal style guide)

### For presentations / slides
- Increase all font sizes by ~4pt relative to paper figures
- Use color more freely
- Simpler is better — one message per slide figure
- Wider aspect ratio (16:9 widescreen)

---

## Code Templates

### R — ggplot2

#### Base theme for papers
```r
library(ggplot2)
library(scales)

theme_paper <- function(base_size = 12) {
  theme_bw(base_size = base_size) +
    theme(
      panel.grid.minor   = element_blank(),
      panel.grid.major   = element_line(color = "grey90", linewidth = 0.3),
      panel.border       = element_rect(color = "grey40"),
      axis.ticks         = element_line(color = "grey40"),
      legend.position    = "bottom",
      legend.title       = element_text(size = base_size - 1),
      legend.key.size    = unit(0.8, "lines"),
      strip.background   = element_rect(fill = "grey95", color = "grey40"),
      plot.caption       = element_text(size = base_size - 2, hjust = 0, color = "grey40")
    )
}
```

#### Coefficient / dot-whisker plot
```r
library(dplyr)

# df should have: term, estimate, conf.low95, conf.high95, conf.low90, conf.high90
ggplot(df, aes(x = estimate, y = reorder(term, estimate))) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "grey50") +
  geom_linerange(aes(xmin = conf.low95, xmax = conf.high95), linewidth = 0.6) +
  geom_linerange(aes(xmin = conf.low90, xmax = conf.high90), linewidth = 1.2) +
  geom_point(size = 2.5, shape = 21, fill = "white", color = "black") +
  labs(x = "Coefficient estimate", y = NULL,
       caption = "Thick lines: 90% CI. Thin lines: 95% CI.") +
  theme_paper()
```

#### Event study plot
```r
# df: relative_time (integer), estimate, conf.low, conf.high
# Normalize: estimate at t = -1 is 0 by convention

ggplot(df, aes(x = relative_time, y = estimate)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey50") +
  geom_vline(xintercept = -0.5, linetype = "dotted", color = "grey60") +
  geom_ribbon(aes(ymin = conf.low, ymax = conf.high), alpha = 0.15) +
  geom_line(linewidth = 0.8) +
  geom_point(size = 2) +
  scale_x_continuous(breaks = seq(min(df$relative_time), max(df$relative_time), 2)) +
  labs(x = "Years relative to treatment", y = "Estimate (95% CI)",
       caption = "Note: ...") +
  theme_paper()
```

#### Binscatter
```r
library(binsreg)

# Using binsreg package (Cattaneo, Crump, Farrell, Feng)
bs <- binsreg(y = df$y, x = df$x, w = df[, controls], data = df,
              ci = c(3, 3), cb = c(3, 3))
# Access bs$bins_plot for ggplot layer or use bs$figure directly
```

#### Save for paper
```r
ggsave("output/figures/fig1_main.pdf",
       plot = p, width = 6.5, height = 4, units = "in", device = cairo_pdf)

# Also save PNG at high DPI for sharing
ggsave("output/figures/fig1_main.png",
       plot = p, width = 6.5, height = 4, units = "in", dpi = 300)
```

---

### Python — matplotlib / seaborn

#### Paper style setup
```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Style
plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'grid.color': '#e0e0e0',
    'grid.linewidth': 0.6,
})
```

#### Coefficient plot
```python
fig, ax = plt.subplots(figsize=(5, len(coefs) * 0.5 + 1))

for i, (label, est, lo90, hi90, lo95, hi95) in enumerate(coefs):
    ax.plot([lo95, hi95], [i, i], color='black', linewidth=1.0)
    ax.plot([lo90, hi90], [i, i], color='black', linewidth=2.5)
    ax.plot(est, i, 'o', color='white', markeredgecolor='black',
            markersize=6, markeredgewidth=1.2)

ax.axvline(0, linestyle='--', color='grey', linewidth=0.8)
ax.set_yticks(range(len(coefs)))
ax.set_yticklabels([c[0] for c in coefs])
ax.set_xlabel('Coefficient estimate')
ax.text(0, -0.12, 'Thick lines: 90% CI. Thin lines: 95% CI.',
        transform=ax.transAxes, fontsize=8, color='grey')

plt.tight_layout()
plt.savefig('output/figures/fig1.pdf')
```

#### Colorblind-safe palette
```python
# Okabe-Ito palette
OKABE_ITO = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
```

---

### Stata

#### Scheme setup
```stata
* Install scheme-burd or lean2 for publication-quality output
* ssc install schemepack, replace
set scheme white_tableau  // or: lean2, plotplain, s1color

* Or use built-in
set scheme s2mono  // grayscale, good for journals
```

#### Coefficient plot
```stata
* After regression:
coefplot, drop(_cons) xline(0, lpattern(dash) lcolor(gray)) ///
    xlabel(, format(%5.2f)) ///
    msize(small) msymbol(circle_hollow) ///
    ciopts(recast(rcap) lwidth(thin)) ///
    levels(95 90) ///
    legend(order(1 "95% CI" 2 "90% CI")) ///
    graphregion(color(white)) plotregion(color(white))
```

#### Event study
```stata
* After estimating relative-time dummies:
coefplot, keep(rel_*) baselevels ///
    vertical xline(-.5, lpattern(dot) lcolor(gray)) ///
    yline(0, lpattern(dash) lcolor(gray)) ///
    xlabel(, angle(45)) ///
    xtitle("Years relative to treatment") ///
    ytitle("Coefficient estimate") ///
    graphregion(color(white))
```

#### Export
```stata
graph export "output/figures/fig1.pdf", replace
graph export "output/figures/fig1.png", replace width(1950)  // 300 DPI at 6.5 in
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Error bars with no explanation | Add note: "Bars are 95% CI, clustered at [level]" |
| Axis labels missing units | Add units: "Log earnings (2015 USD)" |
| Too many groups in one plot | Facet or split into two figures |
| Line chart with too many lines | Highlight the key one; grey out others |
| Bar chart with y-axis not at zero | Start at zero for bars; it's misleading otherwise |
| Font too small for journal page | Check at actual print size (6.5in wide) |
| Color that fails grayscale | Use shape + linetype as backup encoding |
| Figures not reproducible | Script must generate figure from data; no manual edits in GUI |

---

## Checklist Before Submitting a Figure

- [ ] Axes labeled with variable name and units
- [ ] Error bars present (if showing estimates) and explained in note
- [ ] Data source stated in caption or note
- [ ] Sample definition clear (what sample, what years)
- [ ] Colorblind-safe palette (or grayscale-compatible)
- [ ] All text readable at print size
- [ ] Exported at correct resolution and format for journal
- [ ] Figure is generated by code (reproducible), not manually edited

---

## Output

When invoked, ask the user:
1. What is the data structure and what message should the figure convey?
2. What software (R / Python / Stata)?
3. Is this for a paper, slides, or a presentation?

Then provide code, design guidance, and a checklist tailored to their specific figure.
