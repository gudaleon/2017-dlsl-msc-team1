# Paper 1 (high school) — Draft 3.0

IMRAD manuscript on residual-income housing hardship, 2006–2021.

- `paper1_highschool.tex` / `paper1_highschool.pdf` — manuscript
- `generate_figures_tables.py` — rebuilds figures and tables from the frozen JSON results
- `figures/` — PDF, SVG, and 300 dpi PNG
- `tables/` — CSV + TeX snippets
- `REVISION_LOG.md` — Draft 2.0 → 3.0 rendering fixes

```
python3 generate_figures_tables.py
pdflatex paper1_highschool.tex
pdflatex paper1_highschool.tex
```

Plotted numbers are unchanged from Draft 2.0. Methods and limitations state the unresolved issues: unweighted person-records, person vs household units, simplified MBM, 2006/2016 exclusions, and Census/NHS harmonization.
