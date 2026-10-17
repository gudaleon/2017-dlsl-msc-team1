# Uncertainty methods — Draft 5.0 Stage 1

## What is on the files

| Wave | Replicate weights | User-guide formula recovered? |
| --- | --- | --- |
| 2006 hierarchical PUMF | `WT1`–`WT8` | Yes. Random-groups method, 95M0029XVB. |
| 2011 NHS hierarchical PUMF | `WT1`–`WT8` | Yes. Same method, 99M0002X. |
| 2016 hierarchical PUMF | `WT1`–`WT16` | Weights present. PUMF-specific divisor not recovered. |
| 2021 hierarchical PUMF | `WT1`–`WT16` | Weights present. PUMF-specific divisor not recovered. |

## Documented 2006 / 2011 formula

The hierarchical PUMF user guides describe a random-groups estimator (Wolter 1985), not ordinary i.i.d. bootstrap.

1. Compute the full-sample estimate with `WEIGHT`.
2. Recompute the estimate with each of the eight replicate weights. Empty groups contribute 0.
3. Let \(\bar r\) be the mean of the eight replicate estimates.
4. Standard error \(= \sqrt{\sum_{i=1}^{8}(r_i-\bar r)^2 / 56}\).
5. A 19-in-20 interval uses ±1.96 SE (2011 guide) or ±2 SE (2006 guide wording).

The factor 56 is \(R(R-1)\) for \(R=8\). Each positive replicate weight is described as \(8 \times\) `WEIGHT`.

**2011 Series A (M0) result using that formula:** SE = 0.107 percentage points. An approximate 95% interval around 18.17% is about 18.0% to 18.4%. This interval is for the reconstructed research estimand, not for an official CMHC rate, and it does not cover 2011 NHS non-response bias.

## What Draft 4.0 did

Draft 4.0 reported `sqrt(mean((r_i - point)^2))`, using the full-weight point as the centre and dividing by 8 rather than 56. That is not the user-guide formula. Stage 1 does not reuse those SEs as design-based intervals.

## 2016 and 2021

The Census long-form sampling report (98-306) describes Fay / modified BRR for the confidential long form, with a multiplicative factor and 32 or 100 replicates. That is **not** a recovered write-up of the 16 PUMF replicate weights.

Stage 1 therefore does **not** present 2016 or 2021 ordinary bootstrap intervals, and does not present 16-weight intervals, as survey-design confidence intervals.

Consequence: the −2.4 pp 2016–2021 change is a point-estimate comparison. Sampling variability of that change is not quantified here.

## Other uncertainty that is not sampling error

- 2011 NHS global non-response (about 26%; do not apply an invented correction).
- PUMF rounding and top-coding.
- Threshold approximation (national or CMA/PR mean versus official 50-region MBM).
- Income concept (Census after-tax versus MBM disposable).
- 2020 emergency benefits inside 2021 Census income.
- 2018-base MBM revision at income year 2020.
