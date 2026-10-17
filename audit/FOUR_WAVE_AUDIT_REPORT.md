# Four-wave housing-hardship audit

**Question.** Can the local 2006–2021 Census/NHS PUMFs support a scientifically defensible residual-income hardship series, and can the 2001 household PUMF extend that series to five waves?

**Answer.** A five-wave *after-tax* residual-income series is **not feasible** with the files and codebooks in hand. A four-wave *all-household* series is **not comparable** because the 2006 hierarchical PUMF suppresses monthly shelter for most multi-person households. Two narrower analyses *are* defensible if their limits are stated:

1. **2011 NHS + 2016 Census + 2021 Census** household residual income (document the 2011 voluntary-survey break).
2. **2006–2021 one-person households only** (2006 shelter is released for 95% of singles and ~2%–46% of larger households).

Do not download a new 2016 hierarchical PUMF. The file labelled `census_2011_nhs.csv` is already the 2016 hierarchical file. Do not impute 2006 shelter and do not invent 2001 after-tax income.

Original four-wave numbers are untouched at `audit/original/four_wave_temporal_results.json`. Recalculated numbers are only under `audit/outputs/`.

Interactive summary: [Four-wave Census hardship audit](https://cursor.com/canvas/store-0b0e7fe1-22d1-4c96-bffc-e7af685cdd0f/d4f72950-02ac-4bb9-9ac2-54e7a435427b).

---

## 1. Why 2016 kept 9.4% and 2006 kept 23.4%

Those rates are from the old person-level cleaner in `run_four_wave_analysis.py`. They are not a mysterious missingness problem in a correctly labelled 2016 file.

Three defects stacked.

### 1.1 The year labels on disk are wrong

| Local filename | Rows × cols | Official identity | Why |
| --- | --- | --- | --- |
| `census_2006.csv` | 309,841 × 101 | **2006 Census hierarchical (95M0029X)** | Matches the 2006 user-guide totals (309,841 persons / 124,358 households). Has `GROSRT`+`OMP`, no `SHELCO`, no `CIP2011`. |
| `census_2016_pumf.csv` | 309,841 × 101 | **Same 2006 file again** | Identical 2 MB md5, columns, and row count. |
| `census_2006_pumf.csv` | 333,008 × 112 | **2011 NHS hierarchical (99M0002X)** | 333,008 is the NHS hierarchical person count. Has `CIP2011`, `EFDIMBM`, `GROSRT`+`OMP`, no `SHELCO`. |
| `census_2011_nhs.csv` | 343,330 × 116 | **2016 Census hierarchical (98M0002X)** | 343,330 persons / 140,720 households. *The Daily* (18 June 2019) reported 140,705 households / 343,330 persons. Has `SHELCO`. No `GROSRT`/`OMP`. |
| `census_2021_full.csv` | 361,915 × 122 | **2021 Census hierarchical (98M0002X)** | Has `SHELCO`, `CIP2021`, `EFCOVID_ERB`. |

The old script therefore analysed **scrambled years**: the series labelled 2006 was the 2011 NHS, 2011 was 2016, 2016 was 2006, 2021 was 2021.

### 1.2 Last-match column pick kept only renters on pre-2016 files

The old cleaner walked columns and kept the *last* match in `{TOTINC, INCTOT, TOTINC_AT}` and `{SHELCO, GROSRT, SHELTER}`. It never read `OMP`.

On 2006/2011 files the last shelter match is `GROSRT`. Owners are coded `GROSRT = 9999` (not applicable). Those rows drop. That is why the original “2006” owner hardship is `NaN` and the original “2016” owner hardship is `NaN`.

Old-pipeline retention on the *actual* files:

| File | Last income col | Last shelter col | Person rows kept | Rate |
| --- | --- | --- | --- | --- |
| True 2006 (`census_2006.csv` / `census_2016_pumf.csv`) | `TOTINC_AT` | `GROSRT` | 29,056 | **9.38%** |
| True 2011 NHS (`census_2006_pumf.csv`) | `TOTINC_AT` | `GROSRT` | 78,056 | **23.44%** |
| True 2016 (`census_2011_nhs.csv`) | `TOTINC_AT` | `SHELCO` | 341,030 | 99.33% |
| True 2021 | `TOTINC_AT` | `SHELCO` | 358,621 | 99.09% |

The 9.4% figure the manuscripts treated as “2016” is the 2006 file, renters only, person rows. The 23.4% figure treated as “2006” is the 2011 NHS file, renters only, person rows.

### 1.3 Person income was treated as household income, and NA codes were left in

Hierarchical files are **person records** with a household id. Household after-tax income is the sum of person `TOTINC_AT` after removing `8888888`/`9999999` (or 2011’s 6-digit `888888`/`999999`). The old cleaner used the person amount and only replaced `{8888, 9999, 99999}` on shelter. Income sentinels `8888888` and `9999999` stayed in the mean. That is why the original JSON has income means of $23 million (2011) and $19 million (2021).

---

## 2. Codebook verification (person vs household, weights, income, shelter)

See `audit/codebook_mappings.md` for the field-by-field table. The points that change the analysis:

- **Unit.** Residual income and STIR are household quantities. Collapse to one row per `HH_ID`. `WEIGHT` is a person weight; copy one value per household. Do not sum weights over persons. 2006 `WEIGHT` is the constant 100.02061607. 2001 `WEIGHTH` is the constant 37.
- **After-tax income.** `TOTINC_AT` is a person variable from 2006 onward. 2006 user guide: 8,888,888 = not available; 9,999,999 = not applicable (persons under 15). 2011 NHS stores `TOTINC_AT` in six digits (`888888` / `999999`).
- **Shelter, 2006 and 2011.** `GROSRT` = monthly gross rent (tenants). `OMP` = monthly owner’s major payments. 8,888 = not available; 9,999 = not applicable (the other tenure, farm, band, collective). Combine with `TENUR` (1 = owned, 2 = rented or band, 8 = not available).
- **Shelter, 2016 and 2021.** `SHELCO` replaces `GROSRT` and `OMP` (Borealis 2016 content-change note). Same 8888/9999 sentinels.
- **2011 break.** The 2011 file is the voluntary National Household Survey, not a Census long form.

The repaired pipeline implements that mapping in `audit/run_four_wave_repaired.py`. It does not invent variables.

---

## 3. Recalculated four-wave results

Original outputs were copied to `audit/original/` before any recalculation.

### 3.1 All households (do not read 2006 as a comparable wave)

CPI to 2021 CAD and the single-adult MBM line are the original pipeline’s constants (still unconfirmed against CANSIM 18-10-0005 and StatCan 75F0002M). Dollars are 2021 CAD.

| Year | File identity | HH in file | HH valid | Retention | Median HH after-tax income | Median monthly shelter | STIR > 30% | Hardship | Owner / renter hardship |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2006 | 2006 Census hierarchical | 124,358 | 52,810 | 42.5% | $38,280 | $766 | 36.7% | 22.1% | 11.6% / 36.0% |
| 2011 | 2011 NHS hierarchical | 133,192 | 130,242 | 97.8% | $64,288 | $1,033 | 29.1% | 15.0% | 8.7% / 29.6% |
| 2016 | 2016 Census hierarchical | 140,720 | 139,872 | 99.4% | $67,084 | $1,082 | 29.4% | 15.6% | 8.1% / 31.4% |
| 2021 | 2021 Census hierarchical | 149,789 | 148,091 | 98.9% | $74,000 | $1,200 | 25.9% | 14.2% | 8.1% / 26.6% |

2006 valid households have **mean size 1.46** (median 1). The other waves have mean size ≈ 2.4. The 2006 all-household medians are a one-person-heavy leftover after confidentiality suppression, not a 2006 household population.

Drop log: 2006 loses 71,372 households to missing shelter and 396 to missing/non-positive after-tax income. 2011–2021 each lose well under 3,000 households.

### 3.2 Why 2006 shelter collapses after the repair

This is a codebook/confidentiality fact, not a remaining column-pick bug. `PRIHM == 1` is present for every household (124,358). Tenure at household level matches the 2006 guide exactly: 77,520 owned, 37,485 rented or band, 9,353 not available. Shelter amounts are still missing.

Share of households with a usable `GROSRT` or `OMP` (not 8888/9999, in (0, 10000)):

| Household size | 2006 | 2011 | 2016 | 2021 |
| --- | --- | --- | --- | --- |
| 1 | 95.4% | 99.1% | 99.4% | 99.1% |
| 2 | 46.2% | 98.4% | 99.7% | ~99% |
| 3 | 6.5% | 98.4% | 99.8% | ~99% |
| 4 | 2.6% | 98.2% | 99.9% | ~99% |
| 5 | 0.5% | 97.0% | 99.9% | ~99% |
| 6+ | 3.4% | 95.9% | 99.6% | ~99% |

2006 person-level `OMP = 8888` on 188,623 of 309,841 rows; `GROSRT = 8888` on 87,030. The 2006 guide describes 8888 as confidentiality “not available” and says this affects “a few records.” On this file it affects most multi-person households. Restricting to the primary maintainer does not recover the amounts — they are not on the maintainer row either.

**No undocumented proxy is used.** Suppressed 2006 shelter stays missing.

### 3.3 One-person households (the comparable 2006–2021 cut)

| Year | 1-person HH in file | Valid | Retention | Median after-tax income | Median monthly shelter | Hardship |
| --- | --- | --- | --- | --- | --- | --- |
| 2006 | 33,290 | 31,618 | 95.0% | $30,624 | $766 | 31.2% |
| 2011 | 34,996 | 34,567 | 98.8% | $32,144 | $804 | 34.3% |
| 2016 | 39,678 | 39,248 | 98.9% | $33,542 | $866 | 37.1% |
| 2021 | 43,953 | 43,074 | 98.0% | $38,000 | $900 | 36.4% |

On this cut, leftover-income hardship among one-person households **rises** from 31.2% (2006) to 37.1% (2016) and is 36.4% in 2021. That is the opposite of the original manuscript’s “stable ~38% then 38%” story, which mixed renter-only person rows, scrambled years, and unstripped income NA codes.

2011 remains a voluntary NHS wave.

### 3.4 What the original JSON actually measured

| Label in original JSON | Sample size | What it really was | Hardship printed |
| --- | --- | --- | --- |
| 2006 | 78,056 | 2011 NHS **renters**, person `TOTINC_AT`, `GROSRT` only | 38.0% |
| 2011 | 341,030 | 2016 Census persons, `SHELCO`, NA income left in the mean | 33.9% |
| 2016 | 29,056 | 2006 Census **renters**, person `TOTINC_AT`, `GROSRT` only | 59.3% |
| 2021 | 358,621 | 2021 Census persons, `SHELCO`, NA income left in the mean | 37.9% |

Those figures must not be reused in a manuscript. They remain on disk only so the audit is reconstructable.

---

## 4. Comparability across 2006 / 2011 / 2016 / 2021

| Issue | 2006 | 2011 | 2016 | 2021 |
| --- | --- | --- | --- | --- |
| Instrument | Census long form (2B) | Voluntary NHS | Census 2A-L | Census 2A-L |
| Shelter concept | `GROSRT`+`OMP` | `GROSRT`+`OMP` | `SHELCO` | `SHELCO` |
| Shelter released for multi-person HH | No (confidentiality 8888) | Yes | Yes | Yes |
| After-tax person income | Yes (`TOTINC_AT`, 7-digit NA) | Yes (6-digit NA on `TOTINC_AT`) | Yes | Yes |
| Income year | 2005 | 2010 | 2015 | 2020 (COVID transfers on file) |
| Geography on PUMF | Province + selected CMA | Province + selected CMA | Province + 5 CMA + North | Province + selected CMA |

`SHELCO` is the documented successor of `GROSRT`+`OMP`, so 2011 (composite) vs 2016/2021 (`SHELCO`) is a concept match, not a manufactured proxy. 2006 uses the same composite but the release pattern is not usable for all households. 2011 vs Census is a survey-design break, not a variable-mapping break.

Further limits that apply to every repaired number: PUMF top-coding and rounding; MBM is a single-adult national leftover line, not the official region- and size-specific MBM; CPI factors are inherited and still need Table 18-10-0005.

---

## 5. Can 2001 extend the series to 20 years?

**Not for after-tax residual-income hardship.** The 2001 Census Households and Housing PUMF (catalogue **95M0020X**; DLI codebook `hh2001gid.pdf`) is the right *unit* (one household row, `HHSORT`, `WEIGHTH` = 37, `HHSIZE`) and has compatible shelter (`TENURH`, `OMPH`, `GROSRTH`) and before-tax household income (`TOTINCH`, calendar 2000). It does **not** have after-tax household income. After-tax income enters the PUMF family in 2006 (`TOTINC_AT` / `HHINC_AT`).

A 2001 before-tax STIR, or leftover income against a before-tax LICO, would be a documented proxy series. It is not the same estimand as 2006–2021 after-tax income minus shelter versus MBM. Tax imputation from 2000 tax parameters would be a new, undocumented proxy; this audit does not build one.

The 2001 individuals file (95M0016X) and families file (95M0018X) do not fix the after-tax gap for household shelter analysis. The household file is the one to download if a before-tax 2001 wave is wanted later. It is **not** in `data/raw` now.

---

## 6. Feasibility table

Statuses: **AVAILABLE** / **PROXY ONLY** / **NOT AVAILABLE** / **UNCERTAIN**.

Full machine-readable copy: `audit/outputs/feasibility_table.csv`.

| Required item | 2001 | 2006 | 2011 | 2016 | 2021 |
| --- | --- | --- | --- | --- | --- |
| Local microdata | NOT AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE |
| Official catalogue / codebook | AVAILABLE (95M0020X) | AVAILABLE (95M0029X) | AVAILABLE (99M0002X) | AVAILABLE (98M0002X) | AVAILABLE (98M0002X) |
| Household unit / identifier | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE |
| Tenure | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE |
| Monthly shelter cost | AVAILABLE | PROXY ONLY | AVAILABLE | AVAILABLE | AVAILABLE |
| After-tax household income | NOT AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE |
| Before-tax household income | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE |
| Sampling weight | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE |
| Household size | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE |
| Official MBM line (size/region) | NOT AVAILABLE | UNCERTAIN | UNCERTAIN | UNCERTAIN | UNCERTAIN |
| After-tax STIR | PROXY ONLY | PROXY ONLY | AVAILABLE | AVAILABLE | AVAILABLE |
| After-tax residual hardship vs MBM | PROXY ONLY | PROXY ONLY | AVAILABLE | AVAILABLE | AVAILABLE |
| Census vs NHS comparability | AVAILABLE | AVAILABLE | UNCERTAIN | AVAILABLE | AVAILABLE |

Notes tied to those cells:

- 2006 shelter is on the file (`GROSRT`, `OMP`) but confidentiality 8888 makes an all-household series a selected one-person-heavy sample. One-person 2006 shelter is AVAILABLE.
- 2001 after-tax residual hardship is PROXY ONLY only in the weak sense that a *different* before-tax leftover/LICO series could be built. The after-tax MBM estimand itself is NOT AVAILABLE.
- MBM is UNCERTAIN for 2006–2021 because the current line is a single-adult national leftover copied from the old script, not Table 11-10-0066 / 75F0002M. 2011’s `EFDIMBM` is an economic-family flag and is not a substitute for household residual income.

---

## 7. Is a scientifically defensible five-wave analysis feasible?

**No**, not for the estimand the manuscripts use (household after-tax income − 12 × monthly shelter ≶ single-adult MBM, 2001–2021).

| Proposed series | Verdict | Why |
| --- | --- | --- |
| 2001–2021 after-tax residual hardship | **Not feasible** | 2001 has no after-tax income. Manufacturing tax or substituting `TOTINCH` without a documented before-tax redesign is not allowed. |
| 2006–2021 all-household after-tax residual hardship | **Not feasible as a comparable series** | 2006 shelter is suppressed for most 2+ person households. |
| 2006–2021 one-person after-tax residual hardship | **Feasible with caveats** | 95%+ retention each wave. State the single-adult MBM, inherited CPI, and 2011 NHS break. |
| 2011–2021 all-household after-tax residual hardship | **Feasible with caveats** | High retention, `GROSRT`+`OMP` / `SHELCO` mapping is official. State the NHS break and MBM/CPI limits. |
| 2016–2021 all-household after-tax residual hardship | **Feasible** | Same instrument family, `SHELCO`, ~99% household retention. Still needs official MBM and CPI confirmation before publication. |
| 2001–2021 before-tax STIR | **Feasible as a separate proxy series** | Requires downloading 95M0020X and writing a before-tax design. Not interchangeable with the after-tax residual-income papers. |

Recommended next analytic step, in order, without new Census downloads: (1) treat 2016+2021 as the core household series; (2) add 2011 only with an NHS-break paragraph; (3) publish 2006 only as a one-person robustness cut; (4) do not add 2001 until after-tax is abandoned or a documented before-tax estimand is specified.

---

## 8. Complete list of data, documentation, and code

### Already on disk (do not re-download)

- `data/raw/census_2006.csv` — 2006 hierarchical PUMF (also duplicated as `data/raw/census_2016_pumf.csv`).
- `data/raw/census_2006_pumf.csv` — 2011 NHS hierarchical PUMF.
- `data/raw/census_2011_nhs.csv` — 2016 hierarchical PUMF.
- `data/raw/census_2021_full.csv` — 2021 hierarchical PUMF.
- `audit/diagnose_four_wave_files.py` — fingerprints, pairwise identity, old-pipeline retention.
- `audit/run_four_wave_repaired.py` — remapped household pipeline.
- `audit/original/four_wave_temporal_results.json` — frozen original results.
- `audit/outputs/file_fingerprints.json`
- `audit/outputs/four_wave_repaired_results.json`
- `audit/outputs/four_wave_repaired_summary.csv`
- `audit/outputs/feasibility_table.csv`
- `audit/codebook_mappings.md`
- Old pipeline (preserved, not used): `run_four_wave_analysis.py`, `results/four_wave_temporal_results.json`.

### Official documentation already consulted (URLs / catalogues)

- 2006 hierarchical user guide 95M0029XVB — [datalib.usask.ca … pumf_user_guide.pdf](https://datalib.usask.ca/dli/census2006/pumf-hierarchical/doc-english/documentation-user-guide/pumf_user_guide.pdf)
- 2006 hierarchical README (8888 = not available for confidentiality) — [datalib.usask.ca … README.txt](https://datalib.usask.ca/dli/census2006/pumf-hierarchical/README.txt)
- 2016 hierarchical *The Daily* 18 June 2019 — catalogue 98M0002X, 140,705 HH / 343,330 persons
- 2016 hierarchical Abacus record — 140,720 HH / 343,330 persons
- Borealis 2016 individuals PUMF note — `SHELCO` replaces `GROSRT`/`OMP`
- 2001 household codebook — [datalib.usask.ca … hh2001gid.pdf](https://datalib.usask.ca/dli/census2001/households/phase1/doc/hh2001gid.pdf)
- Catalogues: 95M0020X (2001 household), 95M0016X (2001 individuals), 95M0018X (2001 families), 95M0029X (2006 hierarchical), 99M0002X (2011 NHS hierarchical), 98M0002X (2016 and 2021 hierarchical), 98M0001X (PUMF family page)

### Needed before a publishable household series (no new Census year required)

- Statistics Canada Table **18-10-0005** (annual CPI, all-items) to replace the inherited factors 2006×1.276, 2011×1.148, 2016×1.082, 2021×1.000.
- Official **MBM** thresholds by year, region, and family size (75F0002M / Table 11-10-0066), 2008-base and 2018-base crosswalk if both appear.
- 2011 NHS user guide PDF retained with the project (99M0002X) for the 6-digit `TOTINC_AT` NA codes and the voluntary-survey note.
- 2016 and 2021 hierarchical user guides (98M0002X) retained with the project for `SHELCO` universe and top-codes.
- Decision memo: all-household series starts at 2011 (or 2016), and 2006 is one-person only.

### Needed only if a 2001 wave is added (proxy series)

- 2001 Households and Housing PUMF, catalogue **95M0020X**, plus the household user guide.
- A written estimand change: before-tax `TOTINCH` and a before-tax low-income line (LICO), **or** a reviewed tax-imputation method. Until that document exists, do not download 2001 for the after-tax papers.
- Confirm 2001 `OMPH`/`GROSRTH` top-codes ($1,650 / $1,500 regional averages in the codebook) and the `99` under-$100 collapse.

### Not needed

- Another copy of the 2016 hierarchical PUMF.
- A 2006 household-only PUMF (2006 was released as Individuals + Hierarchical; the hierarchical file is the household file).
- Imputed 2006 `OMP`/`GROSRT` for suppressed multi-person households.
- Silent substitution of 2011 `EFDIMBM` for household residual-income hardship.
