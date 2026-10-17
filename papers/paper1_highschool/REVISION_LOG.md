# Paper 1 Draft 3.0 revision log

Date: 17 October 2026  
Source of plotted numbers: `results/four_wave_temporal_results.json` (unchanged)

## What was wrong in Draft 2.0

The Drive folder `Paper1_HighSchool_LaTeX` held ~10–13 KB JPEG previews, not the 300 dpi PNG files. Those JPEGs are what failed visual review:

| Figure | Draft 2.0 failure | Cause |
| --- | --- | --- |
| Fig 1 | Lower half grey / missing | JPEG crushing of the percentile `fill_between` bands; `suptitle` + `tight_layout` left little pad |
| Fig 2 | Bright green fill, poor contrast, overlapping period labels | Neon `#1E8449` bars and two-line x labels (`crisis + recovery` / `expansion + COVID`) |
| Fig 3 | 2021 tick looked misplaced | Linear time axis: 2006–2011 is 5 years, 2011–2021 is 10 years, so 2021 sat on the far right |
| Fig 4 | Acceptable | Kept the same numbers; restyled only |
| Fig 5 | Bottom grey / clipped | Dashboard saved without `constrained_layout`; JPEG preview dropped the lower panels |

`includegraphics` pointed at `.png` while the shared folder only had `.jpg`.

## What Draft 3.0 changes (rendering only)

- Regenerated all five figures from `generate_figures_tables.py`.
- White figure and axes backgrounds. Muted Okabe–Ito colours. No neon green.
- Equal-spaced year positions for 2006, 2011, 2021 (labels in that order).
- Each figure exported as vector PDF, SVG, and 300 dpi PNG.
- Saved files were inspected with PIL (size, lower-panel ink, washed-out grey bands), then opened as rasters, then checked again inside the compiled 17-page PDF.
- LaTeX now includes `figures/fig0X_….pdf`.
- Draft label is 3.0 (17 October 2026).

Analytical medians, STIR shares, hardship rates, and tenure gaps are the same values as Draft 2.0.

## Methodological issues left visible

Draft 3.0 does not paper over the analysis limits. Methods and §4.5 now state:

1. Estimates are **unweighted** person-records (`WEIGHT` is not applied).
2. Hierarchical files are **person rows**; income is person `TOTINC_AT`, not a household sum.
3. The MBM line is a **single-adult national leftover**, not official 75F0002M region/family-size thresholds.
4. **2016 is excluded** (9.4% retention). **2006 kept 23.4%**, largely because cleaning used `GROSRT` and dropped owners.
5. **2011 is the voluntary NHS.** Shelter names change from `GROSRT`/`OMP` to `SHELCO`. The series is not fully harmonized.

## Caption / table check

| Object | Plotted / tabled values |
| --- | --- |
| Hardship | 38.0% (2006), 33.9% (2011), 37.9% (2021) |
| Median income | $34,452; $45,920; $46,000 |
| Median shelter | $1,021; $1,378; $1,400 |
| STIR > 30% | 57.0%; 52.2%; 50.8% |
| Income index | 100.0; 133.3; 133.5 |
| Shelter index | 100.0; 135.0; 137.1 |
| Tenure 2011 / 2021 | owners 31.4% / 35.6%; renters 40.4% / 43.6% |
| Period changes | income +33.3% then +0.2%; shelter +35.0% then +1.6%; hardship −4.1 pp then +4.0 pp (Figure 2 uses the same one-decimal labels as Table 5) |

Those match Figure 1–5, Tables 1–5, and the results text.

## Compile

```
cd papers/paper1_highschool
python3 generate_figures_tables.py
pdflatex paper1_highschool.tex
pdflatex paper1_highschool.tex
```

Output: 17 pages, `paper1_highschool.pdf`.
