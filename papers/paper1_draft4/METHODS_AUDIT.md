# Draft 4.0 methods audit

**Verification status.** The reconstructed **2011–2021 household** series passes the checks that can be run with the files and official tables in hand. The **2006 all-household** series does **not**. Reconstructed hardship rates are a research estimand. They are **not** official CMHC housing-hardship rates.

Draft 3.0 (`papers/paper1_highschool/`) is frozen. Original person-level JSON remains at `results/four_wave_temporal_results.json` and `audit/original/`.

## Priority 1 — Unit of analysis

Each 2006–2021 file is a **hierarchical person-in-household PUMF** (`HH_ID`, `EF_ID`, `CF_ID`, `PP_ID`). Exactly one `PRIHM==1` primary maintainer exists in every household. `WEIGHT` is constant within household.

| Rule | Implementation |
| --- | --- |
| Household income | Sum of person `TOTINC_AT` after removing `888888` / `999999` / `8888888` / `9999999` |
| Household shelter | Primary-maintainer `OMP` (owner) or `GROSRT` (renter) in 2006/2011; `SHELCO` in 2016/2021. Not summed across persons. |
| Tenure | Maintainer `TENUR` (1 owned, 2 rented) |
| Weight | One maintainer `WEIGHT` per `HH_ID`. Never the sum of person weights. |

Draft 3.0 used unweighted person rows and person `TOTINC_AT` as if it were household income. That double-counts large households in the rate and treats a child’s missing income code, or one adult’s pay, as the household budget.

## Priority 2 — Four-wave harmonization and the 23.4% / 9.4% puzzle

Those retention rates are from the old person-level cleaner. They are not a missingness mystery in a correctly labelled 2016 file.

| Local filename | Official file | Old cleaner kept | Why |
| --- | --- | --- | --- |
| `census_2006.csv` | **2006** Census hierarchical | 9.4% | Last-match `GROSRT` kept renters only; 2006 also suppresses multi-person shelter |
| `census_2006_pumf.csv` | **2011 NHS** hierarchical | 23.4% | Same `GROSRT`-only rule on a file that still has owners coded 9999 |
| `census_2011_nhs.csv` | **2016** Census hierarchical | 99.3% | `SHELCO` covers owners and renters |
| `census_2016_pumf.csv` | Duplicate of **2006** | — | Identical to `census_2006.csv` |
| `census_2021_full.csv` | **2021** Census hierarchical | 99.1% | `SHELCO` |

Household reconstruction retention:

| Year | Households in file | Analytic households | Retention |
| --- | --- | --- | --- |
| 2006 | 124,358 | 52,785 | **42.4%** (shelter 8888 on most 2+ person households) |
| 2011 | 133,192 | 130,242 | 97.8% |
| 2016 | 140,720 | 139,869 | **99.4%** |
| 2021 | 149,789 | 148,085 | 98.9% |

2016 is restored once the file is identified and collapsed to households. 2006 all-household results remain a one-person-heavy leftover (mean size 1.45 versus ≈2.4 in later waves). One-person 2006 shelter coverage is 95.4%.

## Priority 3 — MBM / CMHC definition

Official CMHC housing hardship (Research Insight, January 2020):

> Residual income (disposable income after housing costs) compared with the **non-shelter** Market Basket Measure, scaled by `sqrt(n)/2`, using regional MBM thresholds.

Draft 3.0 compared leftover income with a single-adult national leftover line ($13,500 / $15,000 / $19,728). That line is close to a **full** 2005 MBM single-adult threshold ($13,836) and is not the official non-shelter, size-adjusted, regional rule.

Primary Draft 4.0 threshold (Table 11-10-0066, current dollars, unweighted mean of regions):

| Census | Income year | Official base | Reference-family non-shelter | Single-adult non-shelter |
| --- | --- | --- | --- | --- |
| 2006 | 2005 | 2000-base | $19,855 | $9,927 |
| 2011 | 2010 | 2008-base | $24,482 | $12,241 |
| 2016 | 2015 | 2008-base | $27,925 | $13,962 |
| 2021 | 2020 | 2018-base | $34,691 | $17,345 |

Household threshold = reference-family non-shelter × `sqrt(n_persons)/2`.

What is still **not** official CMHC: MBM disposable income; 50-region geography; exclusion of negative residual from the universe; high-income / investment / farm restrictions. Those are sensitivity variants only.

## Priority 4 — Survey estimation

- Point estimates use household `WEIGHT`.
- Sample sizes and estimated population counts are reported separately.
- Replicate weights `WT1`–`WT8`/`WT16` give an approximate bootstrap SE. The year-specific PUMF variance formula is not on disk (unresolved).
- 2006 is self-weighting (`WEIGHT` = 100.02061607), so weighted and unweighted 2006 rates match.

Primary reconstructed hardship (weighted, national non-shelter size-adjusted MBM):

| Year | Sample HH | Estimated HH | Rate | Approx. SE |
| --- | --- | --- | --- | --- |
| 2006 (not comparable) | 52,785 | 5.28 million | 22.5% | 0.47 pp |
| 2011 NHS | 130,242 | 13.02 million | **18.2%** | 0.28 pp |
| 2016 | 139,869 | 14.04 million | **17.3%** | 0.42 pp |
| 2021 | 148,085 | 14.86 million | **14.9%** | 0.11 pp |

## Priority 5 — Independent validation (passed where the series is comparable)

| Check | 2011 | 2016 | 2021 |
| --- | --- | --- | --- |
| Weighted HH in file vs published private households | −0.02% | +0.36% | +0.37% |
| Median after-tax income, 2020-constant, vs Census | $63,502 vs $63,600 (−0.2%) | $67,093 vs $66,500 (+0.9%) | $74,000 vs $73,000 (+1.4%) |
| Before-tax STIR ≥30% and <100% vs official unaffordable housing | — | 21.5% vs 24.1% | 19.5% vs 20.9% |
| PUMF `HCORENEED_IND` vs official core housing need | — | — | **10.12% vs 10.1%** |

2006 analytic median income fails validation (−36% versus published $59,600) because suppressed multi-person shelter drops most families. That is a diagnosis, not a rounding issue.

CMHC CIS 2017 hardship ≈9% versus reconstructed 2016 17.3%: expected. CIS uses MBM disposable income and a tighter universe. The gap is explained in `VALIDATION_REPORT.md`, not dismissed.

## Priority 6 — Sensitivity (2011–2021 hardship, percentage points versus primary)

| Variant | 2011 | 2016 | 2021 |
| --- | --- | --- | --- |
| Primary (non-shelter, size, national, weighted) | 18.2 | 17.3 | 14.9 |
| CMA/PR geography approximation | −0.9 | −0.7 | −3.1 |
| Full MBM (incorrect: double-counts shelter) | +8.3 | +8.2 | +11.7 |
| Single-adult non-shelter (no size scale) | −3.6 | −3.8 | −3.1 |
| Draft 3.0 leftover line | −3.6 | −2.4 | −1.3 |
| Unweighted | −0.5 | 0.0 | 0.0 |
| Drop negative residual (CMHC universe) | −4.0 | −2.9 | −2.1 |
| High-income exclusion | −0.0 | −0.0 | −0.1 |
| One-person only | +14.2 | +14.8 | +15.4 |
| Owners | −7.3 | −7.9 | −6.2 |
| Renters | +16.2 | +16.8 | +12.6 |

Using the full MBM as the leftover threshold is the largest conceptual error and raises the rate by about 8–12 points. Weighting barely moves 2016/2021 (near self-weighting 1% samples). Tenure composition moves the rate more than weighting.

## Series that may be published

| Series | Verdict |
| --- | --- |
| 2011–2021 all-household reconstructed hardship | **Pass**, with NHS break and “not official CMHC” label |
| 2016–2021 all-household | **Pass** (same instrument family, `SHELCO`) |
| 2006–2021 one-person robustness | **Pass**, with NHS break |
| 2006–2021 all-household | **Fail** (shelter suppression) |
| 2001–2021 after-tax residual | **Fail** (no after-tax income on 95M0020X) |
| Draft 3.0 person-level 38% / 34% / 38% | **Do not reuse** (scrambled years, person income, `GROSRT` only) |
