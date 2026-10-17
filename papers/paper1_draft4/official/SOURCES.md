# Official sources used in Draft 4.0

Downloaded or consulted on 17 October 2026. Full StatCan cubes are not stored in git (they are large). Derived extracts used by the reconstruction are in this folder.

| Extract | Official source | DOI / URL |
| --- | --- | --- |
| `cpi_18-10-0005_extract.json` | Table 18-10-0005-01, Consumer Price Index, annual average, not seasonally adjusted, Canada, All-items, 2002=100 | https://doi.org/10.25318/1810000501-eng |
| `mbm_11-10-0066_national.json` | Table 11-10-0066-01, MBM thresholds for the reference family by region, component and base year, current dollars | https://doi.org/10.25318/1110006601-eng |
| `published_benchmarks.json` | Census / CMHC published statistics used only for validation | see JSON `source` / `url` fields |

## PUMF catalogues and user guides

| File on disk | Official identity | Catalogue |
| --- | --- | --- |
| `data/raw/census_2006.csv` | 2006 Census hierarchical PUMF | 95M0029X |
| `data/raw/census_2006_pumf.csv` | 2011 NHS hierarchical PUMF | 99M0002X |
| `data/raw/census_2011_nhs.csv` | 2016 Census hierarchical PUMF | 98M0002X |
| `data/raw/census_2016_pumf.csv` | Duplicate of the 2006 file (do not use) | 95M0029X |
| `data/raw/census_2021_full.csv` | 2021 Census hierarchical PUMF | 98M0002X |

Year-specific user guides were consulted via DLI / *The Daily* records (see `audit/FOUR_WAVE_AUDIT_REPORT.md`). The PDF user guides themselves are not stored in this repository.

## CMHC housing-hardship definition

CMHC Research Insight, *Introducing the Housing Hardship Concept* (January 2020):

https://assets.cmhc-schl.gc.ca/sites/cmhc/data-research/publications-reports/research-insight/2020/research-insight-introducing-housing-hardship-concept-69619-en.pdf

A household is in housing hardship if residual income after housing costs is below the **non-shelter** portion of the Market Basket Measure, scaled by the square root of family size, using regional MBM thresholds and MBM disposable income.

The 2024 Census update (*New insights on affordability*, NH18-33/85-2024E-PDF) was listed at publications.gc.ca but was not recovered in this reconstruction (retrieval timed out; the file was later reported removed on 25 November 2025).
