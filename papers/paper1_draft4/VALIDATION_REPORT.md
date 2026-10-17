# Independent validation report

Comparisons use published Statistics Canada and CMHC figures for the corresponding year, definition and population. Discrepancies are explained. Reconstructed residual-income hardship is **not** expected to equal official CMHC housing hardship.

## 1. Survey weights recover the private-household universe

| Year | Weighted households in the PUMF | Published private households | Difference |
| --- | --- | --- | --- |
| 2006 | 12,438,364 | 12,437,500 | +0.007% |
| 2011 | 13,317,308 | 13,320,615 | −0.02% |
| 2016 | 14,123,218 | 14,072,079 | +0.36% |
| 2021 | 15,034,101 | 14,978,941 | +0.37% |

The household weight copy rule is correct. Small 2016/2021 differences are consistent with a 1% hierarchical PUMF versus the full 2A-L count (*The Daily*, 18 June 2019, reported 140,705 PUMF households versus 140,720 on this file).

## 2. Median after-tax household income

Published Census medians are in **2020 constant dollars**. PUMF medians are converted with Table 18-10-0005 (Canada All-items).

| Year (income year) | PUMF weighted median, 2020-constant | Published Census | Difference |
| --- | --- | --- | --- |
| 2006 (2005) | $38,411 | $59,600 | **−35.6%** |
| 2011 (2010) | $63,502 | $63,600 | −0.2% |
| 2016 (2015) | $67,093 | $66,500 | +0.9% |
| 2021 (2020) | $74,000 | $73,000 | +1.4% |

**2011–2021 pass.** Remaining gaps are PUMF rounding, top-coding, and the analytic owner/renter restriction.

**2006 fails for a documented reason.** The analytic 2006 sample has mean household size 1.45 because `OMP`/`GROSRT` are 8888-suppressed for most 2+ person households. A one-person-heavy income distribution cannot match the all-household Census median. This is why 2006 all-household hardship is not in the primary series.

Current-dollar PUMF medians used in the paper (income year): $54,000 (2010), $62,000 (2015), $74,000 (2020).

## 3. Shelter-cost-to-income ratio versus official unaffordable housing

Official unaffordable housing: share of owner/renter non-farm non-reserve households with income > 0 and **before-tax** STIR ≥ 30% and < 100% (*The Daily*, 21 September 2022).

| Year | PUMF before-tax STIR ≥30% & <100% | Published | Difference |
| --- | --- | --- | --- |
| 2016 | 21.5% | 24.1% | −2.6 pp |
| 2021 | 19.5% | 20.9% | −1.4 pp |

Direction and 2016→2021 decline match. The remaining gap is expected: the PUMF cannot fully drop farm, reserve and band dwellings; top-codes compress high shelter and high income; 2011 `TENUR==2` mixes band with renters. After-tax STIR > 30% is higher (28.9% in 2016, 25.9% in 2021) because the denominator is smaller. That after-tax figure must not be labelled as the official unaffordable-housing rate.

2021 PUMF `STIR_GRP==1` is 21.8% — close to the official 20.9% before-tax rate. Codebook confirmation of `STIR_GRP` remains UNCERTAIN.

## 4. Core housing need (different concept, same files)

| Year | PUMF `HCORENEED_IND==100` (analytic, weighted) | Published core housing need |
| --- | --- | --- |
| 2021 | **10.12%** | **10.1%** |

The 2021 flag reproduces the published rate to one decimal. Core housing need is **not** residual-income hardship. The match is evidence that household construction, weights and the 2021 file identity are right.

Published core need for context: 12.7% (2006), 12.5% (2011), 12.7% (2016), 10.1% (2021). Owners 5.3% and renters 20.0% in 2021. Reconstructed hardship is higher than core need (14.9% versus 10.1% in 2021) because hardship does not require a local-market alternative-rent test.

## 5. Official low-income / MBM flags (economic family, not household residual)

| Year | PUMF flag (household, weighted) | Published person MBM low income |
| --- | --- | --- |
| 2011 `LOMBM==2` | 14.7% | (person concept; NHS) |
| 2016 `LOMBM==2` | 14.3% | 14.4% of persons (2015) |
| 2021 `LOMBM_2018==1` | 9.3% | 11.1% of persons (2020) |

Units differ (household versus person; economic family versus household). 2011/2016 code 2 is treated as below-MBM **UNCERTAIN** without the codebook page. These flags are complements, not substitutes for residual-income hardship.

## 6. CMHC housing hardship

CMHC Research Insight (2020), Canadian Income Survey 2012–2017: Canada hardship hovered near **10%** and was **about 9% in 2017**. The same publication’s restricted before-tax STIR > 30% was about 11%.

Reconstructed 2016 Census household hardship is **17.3%**. The gap is not a file error. Official CMHC also:

1. uses **MBM disposable income**, not Census `TOTINC_AT`;
2. assigns **50 MBM regions**, not a national mean;
3. **drops negative residual** from the universe (our sensitivity: 17.3% → 14.4%);
4. forbids hardship for households with equivalized income above the provincial median, and for some investment / farm cases;
5. uses CIS, not the Census hierarchical PUMF.

A 2024 CMHC Census update (NH18-33/85-2024) exists in library catalogues but was not recovered (retrieval timed out; the PDF was later reported removed). No official 2021 Census hardship percentage is cited in this draft.

**Do not present 14.9% / 17.3% / 18.2% as CMHC rates.**

## 7. What Draft 3.0 actually measured

| Draft 3.0 label | n | What it was | Printed hardship |
| --- | --- | --- | --- |
| 2006 | 78,056 | 2011 NHS **renters**, person income, `GROSRT` only | 38.0% |
| 2011 | 341,030 | **2016** persons, `SHELCO` | 33.9% |
| 2016 (dropped) | 29,056 | **2006** renters | 59.3% |
| 2021 | 358,621 | 2021 persons | 37.9% |

Those figures stay on disk for the audit. They are not in Draft 4.0 tables or figures.
