# Paper 1 figures and tables (Draft 3.0)

Publication figures are vector PDF + SVG + 300 dpi PNG. Tables are CSV plus `\input`-able `.tex`.

## Figures

| Stem | Content |
|---|---|
| `figures/fig01_national_trends.{pdf,svg,png}` | Income, shelter, STIR, residual-income hardship, 2006–2021 |
| `figures/fig02_period_comparison.{pdf,svg,png}` | 2006–2011 vs 2011–2021 income, shelter, hardship |
| `figures/fig03_tenure_divergence.{pdf,svg,png}` | Owner vs renter hardship |
| `figures/fig04_income_shelter_squeeze.{pdf,svg,png}` | Indexed squeeze, 2006 = 100 |
| `figures/fig05_summary_dashboard.{pdf,svg,png}` | Four-panel summary |

LaTeX includes the PDF files. Rebuild with `python3 generate_figures_tables.py`.

## Tables

| Stem | Content |
|---|---|
| `tables/table01_sample_characteristics` | Sample size, medians, STIR, hardship |
| `tables/table02_tenure_hardship` | Owner vs renter |
| `tables/table03_indexed_squeeze` | 2006 = 100 indexes |
| `tables/table04_summary_2006_2021` | 15-year summary |
| `tables/table05_period_changes` | Period-over-period changes |

## Drive

- Package folder: https://drive.google.com/drive/folders/1DrIvYHuCTvQOEqzp1IfHwCw5RcEhxf2m
- Draft 3.0 (current): https://drive.google.com/drive/folders/1bhoL_OB66mXfrkGX_ZPMl4EHJg2vS9Me
- Draft 2.0 archive: https://drive.google.com/drive/folders/1O5JEzOkNVJnS2aA2oYiPEbGtmIxFE_Jg
- Readable cover: https://docs.google.com/document/d/1lUiSVj6VeA7NUENlWntn7kSGc1OHp5gqLnXt9ie_Io8/edit

### Draft 3.0 figures folder (`1l5zei4CKY_3-W3opV0OFhrQI3Jz6R4qA`)

| File | Drive id | Notes |
|---|---|---|
| `fig01_national_trends.pdf` | `1AUhEzuNPo1B6Cnn78zpUlrpjnr_OH63S` | vector |
| `fig01_national_trends.svg` | `1Aon-tyT0qIQ7dqh571RWMI7HY5jts9fo` | vector |
| `fig01_national_trends_preview.png` | `1T6vqMgii3tI497uOyVRVhid9FEa9k3EI` | 1100 px viewing copy |
| `fig02_period_comparison.pdf` | `1WijIYCDPeEa3W51S7TxpbTo7CtLXcLRt` | vector |
| `fig02_period_comparison.svg` | `1OpG72AwT9-g3v6iju5ucHm66C0hUtqHR` | vector |
| `fig02_period_comparison_preview.png` | `1_4UPEmpCEQ7mbOcjkSXoIpwdusPL8DXU` | 1100 px viewing copy |
| `fig03_tenure_divergence.pdf` | `154BMTJxIqIOh0yptEuF8qkcSOh0Flkx2` | vector |
| `fig03_tenure_divergence.svg` | `1fSuI2yWwOuTLt8SKchYO1mJaw96LygGW` | vector |
| `fig03_tenure_divergence_preview.png` | `1FTO5exmGBizTnGpipRjlFBlTZrp-Yehj` | 1100 px viewing copy |
| `fig04_income_shelter_squeeze.svg` | `19aCYMiGWhrzvSNxKt_7SibiC8gH25U1G` | vector |
| `fig04_income_shelter_squeeze_preview.png` | `1s47INm4LGoWg0mBgLdpy_YNoQuGi9a8T` | 1100 px viewing copy |
| `fig05_summary_dashboard.svg` | `1UQxIOUhsBxeguGQ7wHYf1Tz8gt-Ynsox` | vector |
| `fig05_summary_dashboard_preview.png` | `1IwThGDm_hCMg2WzcBsWFSpt6IDL2tJJ8` | 1100 px viewing copy |

The compiled `paper1_highschool.pdf` (258 KB) and the five 300 dpi PNGs (168–410 KB) are in this git package. The Drive `create_file` tool rejects a single ~30–340 KB base64 payload, so those binaries stay in the repository rather than as truncated Drive files. Use the vector PDFs/SVGs on Drive, or compile locally:

```
cd papers/paper1_highschool
python3 generate_figures_tables.py
pdflatex paper1_highschool.tex
pdflatex paper1_highschool.tex
```
