# SERIES_LOCK — Draft 5.0 Stage 1

Status vocabulary: `LOCKED` / `PROVISIONAL` / `REJECTED` / `NOT AVAILABLE`

Headline rule applied: a >2 pp move of M6 versus M0 in 2016 or 2021 is a **review trigger**, not an automatic replacement. M6 moved 2016 by −3.71 pp and 2021 by −5.29 pp. M6 is not independently validated as a CMHC-equivalent estimand (MBM disposable income, 50-region geography, and several universe rules remain unavailable; dropping negative residual changes the population). **Headline selection remains PROVISIONAL.** M0 is retained as the provisional primary specification. M6 and the two-factor variant are documented sensitivities. Neither is an official CMHC calculation.

Code: `papers/paper1_draft5/stage1_verification.py`  
Equation: residual = Σ TOTINC_AT − 12 × monthly shelter; hardship if residual < non-shelter MBM × √n / 2.

---

## Series A — 2011–2021 all-household residual hardship

**Status: PROVISIONAL**

| Year | Survey | n | N̂ | Hardship | Owners | Renters | One-person |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2011 | NHS (voluntary) | 130,242 | 13,019,080 | 18.2% | 10.8% | 34.4% | 32.4% |
| 2016 | Census 2A-L | 139,869 | 14,037,793 | 17.3% | 9.4% | 34.2% | 32.2% |
| 2021 | Census 2A-L | 148,085 | 14,863,013 | 14.9% | 8.8% | 27.6% | 30.3% |

Estimand: household residual-income hardship using national non-shelter MBM, contemporaneous official base, after-tax Census income. Research estimate only.

Gate B:

1. Unit and denominator coherent — yes (household, one WEIGHT).
2. Variable definitions reproducible — yes (Gate A PASS).
3. Survey weights handled — yes.
4. Major exclusions explained — yes (tenure / income / shelter; 2011 NHS non-response not corrected).
5. Time and price references consistent within year — yes; 2018-base break at 2020 is explicit.
6. Independent benchmarks reviewed — ownership, core need, and STIR directionally consistent; official 2021 CMHC hardship not recovered.
7. Limitations documented — yes, but they include a material M6 sensitivity and a COVID-income threat to the 2016–2021 reading.

Why not LOCKED: headline specification remains unresolved after the >2 pp review trigger; 2021 income year includes emergency benefits; official CMHC 2021 rate is missing.

Do not describe this as a 15-year all-household series.

---

## Series B — 2006–2021 one-person households

**Status: PROVISIONAL**

| Year | n | N̂ | Hardship |
| --- | ---: | ---: | ---: |
| 2006 | 31,618 | 3,162,452 | 28.8% |
| 2011 | 34,567 | 3,617,928 | 32.4% |
| 2016 | 39,248 | 3,938,664 | 32.2% |
| 2021 | 43,074 | 4,322,451 | 30.3% |

Same household residual equation and same contemporaneous non-shelter MBM as Series A. 2006 one-person shelter is usable; 2006 all-household is not. One-person results do not represent all Canadian households. 2011 remains a voluntary NHS.

---

## Series C — Owner versus renter hardship

**Status: PROVISIONAL** (same specification as Series A)

Weighted owner share among TENUR ∈ {1,2} on the full household file: 2011 68.9%; 2016 67.8%; 2021 66.7% (published 2021 homeownership ≈ 66.5%). Tenure coding is consistent enough for a split, with the locked 2011 caveat that `TENUR==2` is “rented or band.”

Rates are the Series A owner / renter columns. The 2016–2021 decline is concentrated among renters (34.2% → 27.6%).

---

## Series D — Distance-to-CMHC specifications

**Status: LOCKED as a methods table** (not as a headline rate)

Implemented or ruled:

| Scenario | 2011 | 2016 | 2021 | Status |
| --- | ---: | ---: | ---: | --- |
| M0 Draft 4.0 primary | 18.17% | 17.33% | 14.95% | IMPLEMENTED |
| M1 drop negative residual | 14.20% | 14.39% | 12.83% | IMPLEMENTED; changes universe |
| M2 provincial-median high-income recode | 18.13% | 17.29% | 14.89% | IMPLEMENTED from CMHC 2020; investment/farm/capital-gain rules NOT IMPLEMENTED — INSUFFICIENT EVIDENCE |
| M3 CMA/PR geography | 17.28% | 16.62% | 11.88% | APPROXIMATED |
| M4 2008-base same income year | 18.17% | 17.33% | 11.63% | IMPLEMENTED |
| M5 EF_ID residual | — | — | — | NOT IMPLEMENTABLE |
| TWO_FACTOR (M1+M3) | 13.27% | 13.65% | 9.69% | IMPLEMENTED separately from M6 |
| M6 closest feasible | 13.25% | 13.62% | 9.66% | APPROXIMATED; not official CMHC |
| MBM disposable | — | — | — | NOT AVAILABLE |
| Official 50-region MBM | — | — | — | NOT AVAILABLE |

Incremental 2016 (pp vs M0): M1 −2.94; M3 −0.71; TWO_FACTOR −3.68; M6 −3.71.  
Incremental 2021 (pp vs M0): M1 −2.12; M3 −3.07; TWO_FACTOR −5.26; M6 −5.29.

Universe change for M1 / TWO_FACTOR / M6: 2016 drops 4,804 households (N̂ 482,251); 2021 drops 3,595 (N̂ 360,923). Negative residual may be genuine severe hardship.

---

## Series E — COVID / MBM-base / composition

**Status: LOCKED as a sensitivity and decomposition package** (not as a headline)

See `COVID_MBM_DECOMPOSITION.md`. Preserve both consistent-base rates and ERB strata. Do not publish the ERB-subtraction residual (20.1%) as a primary 2021 hardship rate.

---

## Rejected / not available

| Series | Status | Reason |
| --- | --- | --- |
| 2006 all-household residual | REJECTED | 8888 shelter suppression; 42.4% retention; mean size 1.45 |
| 2001 after-tax residual | NOT AVAILABLE | No after-tax income on 95M0020X in `data/raw` |
| Draft 3.0 person-level ~38% rates | REJECTED | Scrambled-year person `GROSRT`-only estimates |
| Full-MBM leftover as headline | REJECTED | Double-counts shelter |
| Official CMHC 2021 Census hardship | NOT AVAILABLE | NH18-33/85-2024E-PDF withdrawn; rate not recovered |
