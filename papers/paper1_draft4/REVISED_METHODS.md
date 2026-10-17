# Revised Methods section (Draft 4.0)

This text replaces the Draft 3.0 Methods. It is written so that a high-school reader can follow it, but it does not simplify away official definitions.

## Data sources

We use four Statistics Canada hierarchical Public Use Microdata Files. Hierarchical files are **person records nested in households**. Local filenames on disk do not match calendar years. Identity is taken from official sample sizes and codebook markers:

| Census / survey | Catalogue | Local file | Persons | Households |
| --- | --- | --- | --- | --- |
| 2006 Census long form | 95M0029X | `census_2006.csv` | 309,841 | 124,358 |
| 2011 National Household Survey (voluntary) | 99M0002X | `census_2006_pumf.csv` | 333,008 | 133,192 |
| 2016 Census 2A-L | 98M0002X | `census_2011_nhs.csv` | 343,330 | 140,720 |
| 2021 Census 2A-L | 98M0002X | `census_2021_full.csv` | 361,915 | 149,789 |

`census_2016_pumf.csv` is a duplicate of the 2006 file and is not used.

Income on each file is for the **previous calendar year** (2005, 2010, 2015, 2020).

## Unit of analysis

The analytic unit is the **household**, one row per `HH_ID`.

- **After-tax household income** is the sum of person `TOTINC_AT` after official not-available and not-applicable codes are removed (`8888888` / `9999999`, or 2011’s 6-digit `888888` / `999999`). Children under 15 have not-applicable income and do not enter the sum.
- **Monthly shelter** is taken from the primary household maintainer (`PRIHM==1`). It is not summed across persons. For 2006 and 2011, owners use `OMP` and renters use `GROSRT`. For 2016 and 2021, both tenures use `SHELCO`.
- **Tenure** is the maintainer’s `TENUR` (1 = owned, 2 = rented). `TENUR==8` is dropped.
- **Weight** is one copy of `WEIGHT` per household. Person weights are not added up.

The 2006 file suppresses monthly shelter (code 8888) for most households with two or more people. The 2006 **all-household** sample is therefore one-person-heavy (mean size 1.45) and is **not** in the primary series. A 2006–2021 **one-person** cut is reported as robustness (95%+ of singles have usable shelter in every wave).

## Housing hardship (reconstructed CMHC concept)

Canada Mortgage and Housing Corporation defines housing hardship as: after housing is paid, the household cannot afford the **non-shelter** part of the Market Basket Measure (food, clothing, transportation, other necessities). The official MBM is built for a family of four and scaled by the square root of household size.

\[
\text{Annual shelter} = 12 \times \text{monthly shelter}
\]
\[
\text{Residual income} = \text{after-tax household income} - \text{annual shelter}
\]
\[
\text{Threshold} = \text{non-shelter MBM}_{n=4} \times \frac{\sqrt{n}}{2}
\]
\[
\text{Hardship} = 1 \text{ if residual income} < \text{threshold}
\]

Non-shelter MBM is Food + Clothing + Transportation + Other expenses from Statistics Canada Table 11-10-0066-01, current dollars, unweighted mean of published MBM regions, using the official base in force for that income year (2000-base in 2005, 2008-base in 2010 and 2015, 2018-base in 2020).

This is **not** an official CMHC rate. Official CMHC also uses MBM disposable income (after several non-discretionary deductions), about 50 geographic cells, and extra sample rules we can apply only as sensitivity tests.

Comparing residual income with the **full** MBM double-counts shelter and is reported only as a warning sensitivity (+8 to +12 percentage points).

## Inflation

Hardship **rates** use income-year dollars against same-year MBM dollars. No CPI is applied to the rate.

Dollar **medians** in figures are converted to 2021 CAD with Table 18-10-0005, Canada All-items annual average (2002=100): 2005 = 107.0, 2010 = 116.5, 2015 = 126.6, 2020 = 137.0, 2021 = 141.6.

## Survey estimation

Estimates are household-weighted. Sample *n* and estimated population *N* are reported separately. Approximate standard errors use the PUMF replicate weights with a generic bootstrap formula; the exact user-guide constant was not on disk.

## Comparison measures

- After-tax STIR = annual shelter / after-tax household income.
- Before-tax STIR ≥ 30% and < 100% is compared with Statistics Canada’s official unaffordable-housing rate (a different, before-tax concept).
- 2021 `HCORENEED_IND` is compared with published core housing need (a different concept).

## What this draft does not claim

It does not claim official CMHC housing-hardship percentages. It does not treat 2011 as interchangeable with a Census long form. It does not extend the after-tax series to 2001. It does not reuse Draft 3.0’s person-level 38% / 34% / 38% figures.
