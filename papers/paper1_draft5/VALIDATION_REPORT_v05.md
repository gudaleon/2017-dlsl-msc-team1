# Validation report v05

Draft 5.0 Stage 1. Research reconstructions are not official CMHC housing-hardship rates. Core need, STIR unaffordability, and residual-income hardship are different indicators.

## 1. Gate A

Draft 4.0 primary rates, sample sizes, and estimated household totals reproduce exactly (see `REPRODUCTION_REPORT.md`). Status: PASS.

## 2. Independent 2021 housing benchmarks

| Check | PUMF reconstruction | Published | Difference | Verdict |
| --- | ---: | ---: | ---: | --- |
| Homeownership (TENUR 1 among 1/2) | 66.68% | 66.5% | +0.18 pp | Consistent |
| Core need, all (`HCORENEED_IND==100`) | 10.12% | 10.1% | +0.02 pp | Consistent |
| Core need, owners | 5.28% | 5.3% | −0.02 pp | Consistent |
| Core need, renters | 20.23% | 20.0% | +0.23 pp | Consistent |
| Unaffordable housing STIR≥30% & <100%, owners | 13.91% | 14.8% | −0.89 pp | Same direction; universe incomplete |
| Unaffordable housing STIR≥30% & <100%, renters | 30.98% | 33.2% | −2.22 pp | Same direction; universe incomplete |
| Official CMHC 2021 Census hardship | not computed as official | not recovered | — | Cannot validate |

Sources: 2021 Census / The Daily 21 September 2022 for unaffordable housing and core need; Census housing indicators for the 66.5% ownership figure; CMHC/StatCan core-need publications for 5.3% / 20.0% / 10.1%. Official unaffordable-housing universe is non-farm non-reserve private households with positive income and STIR < 100%. These PUMFs cannot fully implement farm and reserve exclusions (`REGIND` is not a reserve-housing flag). That gap is a sufficient reason for the STIR shortfall and is not evidence that household residual income was computed incorrectly.

Residual hardship (owners 8.8%, renters 27.6%) is **not** expected to equal core need or STIR. Ranking is the same: renters far above owners.

## 3. `STIR_GRP` and the November 2024 correction

Statistics Canada correction notice (98M0001X, 8 November 2024): the March 20 2024 hierarchical file computed `STIR_GRP` as shelter cost divided by total household income. The corrected variable uses shelter cost divided by average monthly household income.

On the local 2021 file, among analytic households with `STIR_GRP` ∈ {0,1}:

- `STIR_GRP==1` weighted share = 21.80%
- Reconstructed before-tax monthly STIR ≥ 30% = 21.80%
- Unweighted agreement = **1.000**
- Uncorrected monthly/annual formula ≥ 30% = 0.65% (agreement 0.79)

The local 2021 PUMF matches the **corrected** definition. Draft 4.0’s reading of `STIR_GRP==1` as 30%+ is confirmed. The 21.8% flag rate is close to the published 20.9% unaffordable-housing rate; remaining difference is universe and rounding.

## 4. Codebook items previously marked UNCERTAIN

| Item | Stage 1 |
| --- | --- |
| 2006 `REGION` 1–6 | CONFIRMED (95M0029XVB). Draft 4.0 inferred labels were correct. |
| 2011/2016 `LOMBM` | CONFIRMED. Code 2 = low-income economic family. Draft 4.0 was correct. |
| 2021 `STIR_GRP` | CONFIRMED; local file is the corrected version. |
| 2006/2011 replicate-weight formula | CONFIRMED (divisor 56). Draft 4.0 SE formula was not the user-guide formula. |
| 2016/2021 replicate-weight formula | Still not recovered. No design-based CIs. |
| Official 2021 CMHC hardship | Still not recovered. |

2011 `LOMBM==2` person-weighted share in Draft 4.0 (14.7%) is a person/EF low-income flag, not household residual hardship. It remains a useful but different benchmark.

## 5. Distance-to-CMHC and headline review

M6 differs from M0 by more than 2 pp in both 2016 (−3.71) and 2021 (−5.29). That is a material methodological sensitivity and a headline **review trigger**.

M6 is not promoted:

- It drops negative-residual households from the universe (2016: 3.4% of weighted analytic households; 2021: 2.4%). Those cases may be genuine severe hardship.
- Geography is still a CMA/PR proxy, not the official 50-region assignment.
- Income is still `TOTINC_AT`, not MBM disposable income.
- Investment / capital-gain / farm restrictions are not implemented.
- No official 2021 CMHC number exists here against which to validate M6.

High-income provincial-median recode (M2) changes rates by only about −0.04 to −0.05 pp. Almost no household above the provincial equivalized median was in residual hardship under M0.

## 6. 2011 NHS

2011 is a voluntary National Household Survey. Official documentation records a global non-response rate of about 26%. No correction factor is applied. 2011 is not interchangeable with a Census long form.

## 7. What can responsibly be used in a later manuscript

- Gate A household rates and sample flow.
- Owner / renter ranking and the 2021 independent housing-flag checks.
- The distance-to-CMHC table, labelled as research approximations.
- The MBM-base and ERB strata, labelled as sensitivities.
- One-person 2006–2021 as a historical extension only.

Do not publish M6 or the ERB-subtraction residual as official or as the uncontested headline.
