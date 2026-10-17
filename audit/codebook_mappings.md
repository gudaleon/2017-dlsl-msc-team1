# Official PUMF mappings used in the audit

Statuses are taken from year-specific Statistics Canada user guides, not from filename labels.

## File identity (local path → official file)

| Local path | Official identity | Catalogue | Official totals used as fingerprint |
| --- | --- | --- | --- |
| `data/raw/census_2006.csv` | 2006 Census hierarchical PUMF | 95M0029X | 309,841 persons / 124,358 households |
| `data/raw/census_2016_pumf.csv` | Duplicate of the 2006 file (identical md5 head, columns, row count) | 95M0029X | same |
| `data/raw/census_2006_pumf.csv` | 2011 NHS hierarchical PUMF | 99M0002X | 333,008 persons / 133,192 households; `CIP2011` present; no `SHELCO` |
| `data/raw/census_2011_nhs.csv` | 2016 Census hierarchical PUMF | 98M0002X | 343,330 persons / 140,720 households; `SHELCO` present; The Daily reported 140,705 households |
| `data/raw/census_2021_full.csv` | 2021 Census hierarchical PUMF | 98M0002X | 361,915 persons / 149,789 households; `SHELCO`, `CIP2021`, `EFCOVID_ERB` |
| *(not downloaded)* | 2001 Census Households and Housing PUMF | 95M0020X | Household file; `WEIGHTH` = 37. Individuals file is 95M0016X; families file is 95M0018X. |

## Record type and unit

| Year | Record type | How to get household income | How to get household shelter |
| --- | --- | --- | --- |
| 2001 | Household (one row per household; `HHSORT`) | `TOTINCH` (before tax) | `TENURH`-conditioned `OMPH` / `GROSRTH` |
| 2006 | Person rows in households (`HH_ID`, `EF_ID`, `CF_ID`, `PP_ID`) | Sum `TOTINC_AT` over persons in `HH_ID`, excluding NA codes | `TENUR`-conditioned `OMP` / `GROSRT` |
| 2011 | Same hierarchical person rows | Same | Same (`GROSRT` + `OMP`) |
| 2016 | Same hierarchical person rows | Same | `SHELCO` (replaces `GROSRT`/`OMP`) |
| 2021 | Same hierarchical person rows | Same | `SHELCO` |

`PRIHM == 1` identifies the primary household maintainer (exactly one per 2006 household). Housing variables are household-level concepts even when stored on every person row.

## Missing-value codes (official)

| Concept | 2001 household file | 2006 hierarchical | 2011 NHS hierarchical | 2016 / 2021 hierarchical |
| --- | --- | --- | --- | --- |
| Income not available | not documented as a separate 8888888 series on `TOTINCH`; exclude documented not-applicable sentinels before use | `8888888` | `TOTINC` 7-digit `8888888`; `TOTINC_AT` 6-digit `888888` | `8888888` |
| Income not applicable (age < 15 on person files) | `9999999` on person-level income fields; `TOTINCH` is household | `9999999` | `TOTINC_AT` `999999` | `9999999` |
| Shelter not available (confidentiality) | not the dominant 2001 household-file pattern; 2001 codebook uses `9999` for not applicable | `8888` on `GROSRT`/`OMP` | `8888` | `8888` on `SHELCO` |
| Shelter not applicable (other tenure / farm / band / collective) | `9999` on `OMPH`/`GROSRTH` | `9999` | `9999` | `9999` |
| Tenure not available | combined rented + band on `TENURH` | `TENUR == 8` (9,353 households) | `TENUR == 8` (rare) | `TENUR == 8` (rare) |

2006 user guide (95M0029XVB): “The value 8,888 stands for not available. The value 9,999 stands for not applicable.” Same guide: “For a few records, the codes for certain variables were changed to indicate Not available, so as to guarantee data confidentiality. Users must make sure to exclude them from their calculations.” Empirically the 8888 suppression on `OMP`/`GROSRT` is not a few records — it removes most multi-person households (see report).

## Weights

| Year | Variable | Official note |
| --- | --- | --- |
| 2001 | `WEIGHTH` | Constant 37 on every household record |
| 2006 | `WEIGHT` | Constant 100.02061607; person weight; use one copy per household, do not sum over persons |
| 2011–2021 | `WEIGHT` | Person weight; household estimates use one weight per `HH_ID` (first / primary maintainer). Replicate weights `WT1`… are for variance only |

## Shelter definitions (do not mix without a mapping)

- **GROSRT / GROSRTH** — monthly gross rent of tenant-occupied non-farm dwellings (rent + utilities). Not applicable to owners.
- **OMP / OMPH** — monthly owner’s major payments (mortgage, property tax, utilities, condominium fees). Not applicable to renters, farm, or band dwellings.
- **SHELCO** — 2016/2021 unified monthly shelter cost. Borealis 2016 individuals-file note: “The replacement of Owner’s major payment (OMP) and Gross rent (GROSRT) by Shelter Cost (SHELCO).”

Composite for 2001/2006/2011: `TENUR==1 → OMP`; `TENUR==2 → GROSRT`. Do not pick the last matching column name (`GROSRT` after `SHELCO`) — that was the old-pipeline bug.

## Income definitions

- **TOTINC** — person total income before tax.
- **TOTINC_AT** — person total income after tax. Present from 2006. 2006 is calendar 2005; 2011 NHS is 2010; 2016 is 2015; 2021 is 2020.
- **TOTINCH** — 2001 household total income before tax, calendar 2000. No after-tax counterpart on 95M0020X.
- Household after-tax income on hierarchical files is the sum of valid person `TOTINC_AT`. Official 2006 guide example aggregates income by `EF_ID` / `HH_ID` after excluding `8888888` and `9999999`.

## Sources consulted

- Statistics Canada, *2006 Census PUMF Hierarchical File: Documentation and User Guide*, 95M0029XVB (record layout; `GROSRT`, `OMP`, `TOTINC_AT`, `WEIGHT`; NA codes; sample 124,358 / 309,841).
- Statistics Canada, *2011 NHS PUMF Hierarchical File* 99M0002X (sample 333,008 persons).
- Statistics Canada, *The Daily*, 18 June 2019, 2016 Census PUMF Hierarchical File (140,705 households / 343,330 persons; 98M0002X).
- UBC Abacus, 2016 hierarchical PUMF (140,720 households / 343,330 persons).
- Borealis 2016 individuals PUMF note: `SHELCO` replaces `GROSRT`/`OMP`.
- University of Saskatchewan DLI, *2001 PUMF Households and Housing File* codebook (`TENURH`, `OMPH`, `GROSRTH`, `TOTINCH`, `HHSIZE`, `WEIGHTH` = 37).
- Statistics Canada catalogue 95M0020X (2001 households and housing), 95M0016X (2001 individuals), 95M0018X (2001 families).
- Statistics Canada 98M0001X PUMF product family page.
