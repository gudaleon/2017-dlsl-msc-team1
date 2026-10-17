# Four-wave variable crosswalk

Statuses follow year-specific Statistics Canada PUMF user guides, not local filenames. Local files are mislabeled; the identity column is the official file.

| Concept | 2006 Census hierarchical `census_2006.csv` (95M0029X) | 2011 NHS hierarchical `census_2006_pumf.csv` (99M0002X) | 2016 Census hierarchical `census_2011_nhs.csv` (98M0002X) | 2021 Census hierarchical `census_2021_full.csv` (98M0002X) |
| --- | --- | --- | --- | --- |
| Record type | Person rows nested in households | Same | Same | Same |
| Household id | `HH_ID` | `HH_ID` | `HH_ID` | `HH_ID` |
| Person id | `PP_ID` | `PP_ID` | `PP_ID` | `PP_ID` |
| Economic / census family | `EF_ID`, `CF_ID` | `EF_ID`, `CF_ID` | `EF_ID`, `CF_ID` | `EF_ID`, `CF_ID` |
| Primary maintainer | `PRIHM==1` (exactly one per household) | `PRIHM==1` | `PRIHM==1` | `PRIHM==1` |
| Tenure | `TENUR` 1=owned, 2=rented or band, 8=not available | `TENUR` 1=owned, 2=rented or band, 8=not available | `TENUR` 1=owned, 2=rented, 8=not available | `TENUR` 1=owned, 2=rented, 8=not available |
| Monthly shelter, owners | `OMP` | `OMP` | `SHELCO` | `SHELCO` |
| Monthly shelter, renters | `GROSRT` | `GROSRT` | `SHELCO` | `SHELCO` |
| Shelter NA / not applicable | 8888 / 9999 | 8888 / 9999 | 8888 / 9999 | 8888 / 9999 |
| Person after-tax income | `TOTINC_AT` (calendar 2005) | `TOTINC_AT` (calendar 2010, 6-digit field) | `TOTINC_AT` (calendar 2015) | `TOTINC_AT` (calendar 2020) |
| Person before-tax income | `TOTINC` | `TOTINC` | `TOTINC` | `TOTINC` |
| Income not available | `8888888` | `TOTINC_AT` `888888`; `TOTINC` `8888888` | `8888888` | `8888888` |
| Income not applicable (age &lt; 15) | `9999999` | `TOTINC_AT` `999999` | `9999999` | `9999999` |
| Household after-tax income | **Constructed:** sum of valid person `TOTINC_AT` in `HH_ID` | Same | Same | Same |
| Household before-tax income | **Constructed:** sum of valid person `TOTINC` | Same | Same | Same |
| Survey weight | `WEIGHT` = 100.02061607 (self-weighting). Use one copy per household. | `WEIGHT` varies by household; constant within household | `WEIGHT` ≈ 100, 12 distinct values, constant within household | `WEIGHT` ≈ 100, 11 distinct values, constant within household |
| Replicate weights | `WT1`–`WT8` | `WT1`–`WT8` | `WT1`–`WT16` | `WT1`–`WT16` |
| Province | Not on file. `REGION` 1–6 only (inferred Atlantic/QC/ON/Prairies/BC/Territories; UNCERTAIN) | `PR` standard SGC | `PR` | `PR` |
| Selected CMA | `CMA` in {462,535,825,835,933,999} | Same codes | Same codes | Same codes |
| Official MBM poverty flag | Not on file | `LOMBM`, `EFDIMBM` (economic family) | `LOMBM`, `EFDIMBM` | `LOMBM_2018`, `EFDIMBM_2018` |
| Core housing need flag | Not on file | Not on file | Not on file | `HCORENEED_IND` (100 / 0 / 888) |
| Published STIR group | Not on file | Not on file | Not on file | `STIR_GRP` (0 / 1 / 9) |
| Instrument | Mandatory Census long form | Voluntary NHS | Mandatory Census 2A-L | Mandatory Census 2A-L |

## Construction rules (do not invent variables)

1. **Unit.** Collapse to one row per `HH_ID`. Residual income and STIR are household quantities.
2. **Income.** Sum person `TOTINC_AT` after removing official not-available / not-applicable codes. Do not treat a person amount as household income. Do not sum `8888888` or `9999999`.
3. **Shelter.** Take the primary-maintainer (`PRIHM==1`) value. Housing variables are household concepts stored on every person row. Do not sum shelter across persons.
4. **2006/2011 composite.** `TENUR==1 → OMP`; `TENUR==2 → GROSRT`. `SHELCO` replaces both from 2016 (Borealis 2016 content-change note).
5. **Weight.** Copy one `WEIGHT` per household. Do not sum person weights. 2006 is self-weighting at 100.02.
6. **2001** (not on disk). Household file 95M0020X has `TOTINCH` (before-tax only), `TENURH`, `OMPH`, `GROSRTH`, `WEIGHTH=37`. After-tax residual hardship is **not available**.

`census_2016_pumf.csv` is a byte-identical duplicate of `census_2006.csv` and is not a 2016 file.
