# 2016–2021 decline: MBM base, COVID benefits, and composition

Draft 4.0 / Gate A primary rates (research estimates, not official CMHC):

- 2016 (income year 2015, 2008-base MBM): **17.3%**
- 2021 (income year 2020, 2018-base MBM): **14.9%**
- Change: **−2.4 percentage points**

This note separates (1) findings supported by the reconstructed PUMF estimates, (2) possible explanations, and (3) factors that remain unidentifiable. It does not attribute the decline to a causal effect of COVID benefits or to a structural improvement in housing markets.

---

## A. MBM base-year sensitivity

Table 11-10-0066 supplies both bases for the relevant income years.

| Comparison | 2016 | 2021 | Change |
| --- | ---: | ---: | ---: |
| Primary / mixed bases (2008 then 2018) | 17.33% | 14.95% | −2.39 pp |
| Consistent 2008-base | 17.33% | 11.63% | −5.70 pp |
| Consistent 2018-base | 18.07% | 14.95% | −3.13 pp |

Reference-family non-shelter means used:

- 2015, 2008-base: $27,925
- 2015, 2018-base: $28,699
- 2020, 2008-base: $29,668
- 2020, 2018-base: $34,691

**Finding supported by the data.** The direction of the 2016–2021 decline survives both consistent-base comparisons. The 2018-base revision raises the 2020 non-shelter threshold and therefore *raises* 2021 hardship relative to a 2008-base 2020 threshold (14.95% vs 11.63%). The mixed-base primary decline (−2.4 pp) is smaller than the consistent 2008-base decline (−5.7 pp). The decline is not an artefact of a lower 2021 basket.

**Not identified.** How much of the remaining decline is a living-standard change versus other 2020 income-composition changes.

---

## B. COVID-19 emergency and recovery benefits

`EFCOVID_ERB` is a **dollar amount** at the economic-family level (CERB, CRB, CRCB, CRSB, CESB; calendar 2020; Census dictionary pop254). Sentinels `88888888` / `99999999` were removed. The household amount is the sum of one copy per `EF_ID`. `TOTINC_AT` already includes these benefits.

| Stratum | Sample n | Weighted N̂ | Share of analytic | Hardship |
| --- | ---: | ---: | ---: | ---: |
| All analytic 2021 | 148,085 | 14,863,013 | 100% | 14.95% |
| Recorded ERB > 0 | 59,713 | 5,993,395 | 40.3% | 13.23% |
| No recorded ERB | 88,372 | 8,869,618 | 59.7% | 16.10% |
| $1–$5,000 | 12,790 | 1,283,522 | 8.6% | 12.06% |
| $5,001–$10,000 | 16,396 | 1,645,470 | 11.1% | 12.24% |
| $10,001–$20,000 | 22,111 | 2,219,456 | 14.9% | 15.55% |
| Over $20,000 | 8,416 | 844,947 | 5.7% | 10.87% |

Among recipients the weighted median household ERB is $10,100.

**Sensitivity using recorded dollars, not invented amounts.** Subtracting the recorded household ERB total from `TOTINC_AT` and re-scoring the 2021 primary threshold raises hardship from 14.95% to **20.09%**. That mechanical residual is *above* the 2016 primary rate of 17.33%. This is not a non-pandemic counterfactual: it does not restore lost earnings, other transfers, or 2020 prices, and ERB receipt is selected.

**Finding supported by the data.** About two in five analytic households have a positive recorded ERB amount. Their reconstructed hardship is 2.9 pp lower than households with no recorded ERB. A mechanical subtraction of recorded ERB dollars is large enough to reverse the 2016–2021 sign.

**Possible explanation, not a causal claim.** 2020 emergency benefits are in the 2021 Census income year and are associated with lower reconstructed hardship. The data do not identify how much of the −2.4 pp primary decline is *caused* by those benefits.

**Unidentifiable here.** Other 2020 transfers (for example CESB is in ERB; wage subsidies and provincial benefits are not separately recovered), labour-market composition, and the fact that shelter is a census-month amount while income is calendar 2020.

---

## C. Population composition (descriptive Kitagawa)

2016 shares and rates are the base. This is a descriptive decomposition, not a causal explanation.

| Grouping | Composition effect | Within-group rate effect | Total reconstructed change |
| --- | ---: | ---: | ---: |
| Tenure (owner / renter) | +0.21 pp | −2.60 pp | −2.39 pp |
| Household size (1 / 2 / 3 / 4+) | +0.21 pp | −2.59 pp | −2.39 pp |
| Tenure × size | +0.33 pp | −2.71 pp | −2.39 pp |
| Within-year income quartile | −0.18 pp | −2.20 pp | −2.39 pp |

Tenure shares in the analytic sample:

- Owners: 68.0% (2016) → 67.1% (2021)
- Renters: 32.0% → 32.9%

Renter hardship: 34.2% → 27.6%. Owner hardship: 9.4% → 8.8%. The renter within-group change accounts for most of the tenure-standardized decline. The small shift toward renters would, by itself, have *raised* the national rate.

One-person share rose (28.1% → 29.1%). One-person hardship remained high (32.2% → 30.3%). Size composition does not explain the decline.

Almost all hardship remains in the bottom income quartile (2016: 59.9%; 2021: 52.1%). Upper-quartile hardship is essentially zero under this residual definition.

**Finding supported by the data.** The reconstructed decline is a within-group rate change, concentrated among renters and the lowest income quartile. Composition of tenure and household size does not account for it.

---

## D. Timing

Income reference years are calendar 2005 / 2010 / 2015 / 2020. Shelter is the census-month amount. The 2021 Census therefore compares 2020 income, including emergency benefits, with May 2021 shelter costs. Official Census STIR uses the same mix. This timing is a limitation of every 2021 income-and-shelter indicator, not a coding error.

---

## E. What can and cannot be said

Supported:

- The −2.4 pp primary decline reproduces.
- It is larger, not smaller, on a consistent 2008-base.
- It is not explained by owner/renter or household-size composition.
- 2020 ERB amounts are on the file, cover about 40% of analytic households, and are large enough, if subtracted, to reverse the sign of the 2016–2021 change.

Possible, not demonstrated:

- That emergency benefits caused the observed decline.
- That housing became structurally more affordable.

Unidentifiable on these PUMFs:

- Official CMHC 2021 hardship.
- A full MBM-disposable-income residual.
- A design-based confidence interval for the 2016–2021 change (2016/2021 PUMF variance formula not recovered).
