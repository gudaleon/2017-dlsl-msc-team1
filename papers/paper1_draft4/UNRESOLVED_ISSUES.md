# Unresolved issues

These limits are not hidden in a footnote. They are why Draft 4.0 rates are a reconstructed research estimand and not official CMHC statistics.

1. **PUMF geography ≠ 50 MBM regions.** Hierarchical files release province (`PR`, 2011+) and six CMA codes (Montreal, Toronto, Calgary, Edmonton, Vancouver, residual 999). The official MBM has about 50 community / population-size cells. Primary thresholds are the unweighted mean of Table 11-10-0066 regions. A CMA/PR approximation is a sensitivity only.

2. **`TOTINC_AT` ≠ MBM disposable income.** Official MBM disposable income also deducts EI, CPP/QPP, registered pension, union dues, work-related childcare, support payments and health premiums, and applies a mortgage-free homeowner advantage. Those fields are not on these PUMFs.

3. **Farm, band and reserve universe.** CMHC and official unaffordable-housing / core-need universes drop farm, band and reserve households. `TENUR==8` is dropped. `REGIND` is not a reserve-housing flag. 2011 `TENUR==2` is “rented or band.”

4. **2006 multi-person shelter is suppressed.** Code 8888 on `GROSRT`/`OMP` removes most households of size 3+. The 2006 guide calls this a confidentiality “few records” rule; empirically it is most multi-person households. No imputation is used.

5. **2006 has no `PR`.** `REGION` 1–6 is inferred from household shares as Atlantic / Quebec / Ontario / Prairies / BC / Territories. Status: **UNCERTAIN** without the 95M0029X codebook page.

6. **Replicate-weight variance.** `WT1`–`WT8`/`WT16` are used with a generic bootstrap formula. The year-specific PUMF user-guide constant (Fay, successive difference, or `(R−1)/R`) is not on disk. Standard errors are approximate.

7. **CMHC universe extras** (negative residual dropped; high-income and investment-income households cannot be in hardship) are sensitivity variants, not the primary rate.

8. **MBM base-year breaks.** 2005 = 2000-base; 2010 and 2015 = 2008-base; 2020 = 2018-base. The 2018-base revision raises the basket, especially shelter. Part of the 2016–2021 hardship decline may be a basket change rather than a living-standard change. A 2008-base 2020 sensitivity exists in the extract (`single_adult_nonshelter` $14,834 versus 2018-base $17,345).

9. **Income year versus shelter month.** Income is the previous calendar year. Shelter is the census-month amount. Official Census STIR uses the same mix. CPI conversion uses income-year All-items (18-10-0005).

10. **2024 CMHC Census hardship update not recovered.** NH18-33/85-2024E-PDF timed out and was later reported removed from publications.gc.ca. No official 2021 Census hardship percentage is quoted.

11. **2001 after-tax series is not feasible.** 95M0020X has `TOTINCH` (before-tax) only. It is not in `data/raw`. Do not invent tax.

12. **`LOMBM` / `STIR_GRP` codebook pages** for 2011/2016/2021 were not stored locally. Flag interpretations used for validation are labelled UNCERTAIN except 2021 `HCORENEED_IND`, which matches the published 10.1% rate.

13. **PUMF disclosure.** Incomes and shelter are rounded and top-coded. Medians are more robust than means. Draft 3.0 means of $19–23 million were unstripped `8888888`/`9999999` codes.

14. **2011 is a voluntary NHS.** Non-response is a survey-design break, not a variable-mapping break.
