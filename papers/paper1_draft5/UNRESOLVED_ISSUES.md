# Unresolved issues — Draft 5.0 Stage 1

Issues retired in this pass are listed at the end.

## Still unresolved

1. **Official CMHC 2021 Census hardship rate.** `NH18-33/85-2024E-PDF` is bibliographically identified and was withdrawn on 25 November 2025. No archived PDF or verified national rate was recovered.

2. **Headline specification.** M6 moves 2016 and 2021 by more than 2 pp versus M0, which triggers review. M6 is not independently validated. Series A remains PROVISIONAL.

3. **MBM disposable income.** `TOTINC_AT` is after-tax income. `EFDIMBM` / `EFDIMBM_2018` are economic-family fields and cannot be used as household MBM disposable income without an unsupported allocation.

4. **Official 50-region MBM geography.** PUMF geography is five named CMAs, residual 999, and province. CMA/PR assignment is a proxy.

5. **CMHC investment / capital-gain / farm restrictions.** Documented in the 2020 Research Insight; not implementable from these PUMF fields. Status: NOT IMPLEMENTED — INSUFFICIENT EVIDENCE.

6. **Economic-family residual test.** NOT IMPLEMENTABLE. Household shelter cannot be allocated across multiple `EF_ID` values in one dwelling (2011: 5.2% of households; 2016/2021: about 1.9%).

7. **Farm, band, and reserve universe.** `TENUR==8` is dropped. `REGIND` is not a reserve-housing flag. 2011 `TENUR==2` includes band housing.

8. **2016/2021 PUMF replicate-weight formula.** Sixteen weights are on the files. The year-specific PUMF divisor was not recovered. No design-based interval is reported for 2016, 2021, or the −2.4 pp change.

9. **How much of the 2016–2021 decline is COVID income.** ERB amounts are on the file and a mechanical subtraction reverses the sign. That is not a causal identification.

10. **2011 NHS non-response.** Official global non-response is about 26%. No invented correction is applied. Comparability with 2016/2021 remains qualified.

11. **2001 after-tax residual series.** Still infeasible.

12. **One-person 2006–2021 as a statement about all households.** Forbidden. Series B remains a restricted historical extension.

13. **PUMF disclosure.** Incomes and shelter are rounded and top-coded.

## Retired or reduced

- **2006 `REGION` labels UNCERTAIN.** Retired. Official 95M0029XVB page confirms Eastern Canada / Quebec / Ontario / Prairies / BC / Northern Canada.
- **`LOMBM==2` as low income UNCERTAIN.** Retired. Official 99M0002X page confirms code 2 = low-income economic family.
- **`STIR_GRP==1` as 30%+ UNCERTAIN.** Retired. Local 2021 file matches the November 2024 corrected monthly formula with 100% agreement.
- **Whether 2006 and `census_2016_pumf.csv` are the same file.** Confirmed again by identical SHA-256.
- **Whether Draft 4.0 primary rates reproduce.** Gate A PASS.

## What the researcher may still need to provide

- A legitimate copy of `NH18-33/85-2024E-PDF`, or written confirmation that the 2021 official hardship rate will remain unpublished.
- The 2016 and 2021 hierarchical PUMF user-guide pages that state the 16-replicate variance formula, if those PDFs can be obtained through DLI.
- If an economic-family headline is desired, an authoritative shelter-allocation rule. None is invented here.
