# Paper 1 — High School Version (LaTeX)

This folder is the revised high-school manuscript. It uses a full journal skeleton (Abstract, Introduction, Methods, Results, Discussion, Conclusion). Figures and tables are **separate files**, then included in LaTeX.

## Compile

```bash
cd papers/paper1_highschool
python3 generate_figures_tables.py   # rebuild PNG + CSV + table .tex
pdflatex paper1_highschool.tex
pdflatex paper1_highschool.tex
```

## Layout

| Path | What it is |
|---|---|
| `paper1_highschool.tex` | Manuscript (includes figures and tables) |
| `paper1_highschool.pdf` | Compiled PDF |
| `figures/*.png` | Five 300 dpi figures (2016 wave excluded) |
| `tables/*.csv` | Five tables for spreadsheets |
| `tables/*.tex` | Same tables as `\input{...}` snippets |
| `generate_figures_tables.py` | Rebuild script |

Census 2016 is excluded on purpose: after cleaning, only 9.4% of records remained and medians were not comparable.
