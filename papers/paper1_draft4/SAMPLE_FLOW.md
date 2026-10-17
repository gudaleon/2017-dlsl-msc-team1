# Sample-flow table

Unit after the first row is the **household**. Person rows are the file structure, not the analytic unit.

| Step | 2006 Census | 2011 NHS | 2016 Census | 2021 Census |
| --- | --- | --- | --- | --- |
| Person records in file | 309,841 | 333,008 | 343,330 | 361,915 |
| Households in file (`HH_ID`) | 124,358 | 133,192 | 140,720 | 149,789 |
| Weighted households in file | 12,438,364 | 13,317,308 | 14,123,218 | 15,034,101 |
| Drop tenure not owner/renter (`TENUR`≠1,2) | 9,353 | 501 | 3 | 8 |
| Drop missing or non-positive after-tax income | 396 | 948 | 390 | 833 |
| Drop missing / suppressed shelter | 71,397 | 2,129 | 466 | 879 |
| **Analytic households (sample n)** | **52,785** | **130,242** | **139,869** | **148,085** |
| Analytic households (weighted N) | 5,279,588 | 13,019,080 | 14,037,793 | 14,863,013 |
| Retention of file households | 42.4% | 97.8% | 99.4% | 98.9% |
| Analytic owners (n) | 30,177 | 90,851 | 95,108 | 99,428 |
| Analytic renters (n) | 22,608 | 39,391 | 44,761 | 48,657 |
| Analytic one-person (n) | 31,618 | 34,567 | 39,248 | 43,074 |
| Mean persons per analytic household | 1.45 | 2.44 | 2.44 | 2.42 |

Drops are not mutually exclusive; a household can fail more than one rule. Analytic n is the intersection (tenure owner/renter **and** income > 0 **and** valid shelter).

Machine-readable copy: `outputs/sample_flow.csv`.

## Why 2006 loses most households

Shelter coverage by household size (`GROSRT`/`OMP` not 8888/9999):

| Size | 2006 | 2011 | 2016 | 2021 |
| --- | --- | --- | --- | --- |
| 1 | 95.4% | 99.1% | 99.4% | 99.1% |
| 2 | 46.2% | 98.4% | 99.7% | 99.6% |
| 3 | 6.5% | 98.4% | 99.8% | 99.5% |
| 4 | 2.6% | 98.2% | 99.9% | 99.6% |
| 5 | 0.5% | 97.0% | 99.9% | 99.4% |
| 6+ | 2.7% | 95.9% | 99.6% | 98.9% |

The 2006 user guide describes 8888 as confidentiality “not available” affecting “a few records.” On this hierarchical file it removes most multi-person households. Primary-maintainer rows are suppressed too. No undocumented proxy is used.
