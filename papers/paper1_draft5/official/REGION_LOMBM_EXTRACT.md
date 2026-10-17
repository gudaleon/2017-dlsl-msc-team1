# Official codebook extracts used to retire UNCERTAIN labels

Retrieved 17 October 2026 from university DLI user-guide PDFs. Full PDFs are not stored in git.

## 2006 `REGION` — 95M0029XVB

Hierarchical File, 2006 Census PUMF, Documentation and User Guide.

REGION — Region. Refers to the region of Canada where the current residence is located (on May 16, 2006).

| Code | Description | Unweighted frequency (persons) | Includes |
| ---: | --- | ---: | --- |
| 1 | Eastern Canada | 22,422 | Newfoundland and Labrador, Prince Edward Island, Nova Scotia, New Brunswick |
| 2 | Quebec | 73,860 | Quebec |
| 3 | Ontario | 119,484 | Ontario |
| 4 | Prairies | 52,699 | Manitoba, Saskatchewan, Alberta |
| 5 | British Columbia | 40,383 | British Columbia |
| 6 | Northern Canada | 993 | Yukon Territory, Northwest Territories, Nunavut |
| Total | | 309,841 | |

Draft 4.0 inferred Atlantic / Quebec / Ontario / Prairies / BC / Territories. That mapping matches this page (Northern Canada = territories).

## 2011 `LOMBM` — 99M0002X hierarchical user guide

LOMBM — Income: Low income status based on MBM.

The code values indicate the position of each member of an economic family and each person not in an economic family in relation to HRSDC's market basket measure low-income line.

| Code | Description | Unweighted | Weighted |
| ---: | --- | ---: | ---: |
| 1 | Member of a non-low income economic family or non-low income person aged 15+ not in an economic family | 285,632 | 28,027,302 |
| 2 | Member of a low income economic family or low income person aged 15+ not in an economic family | 43,352 | 4,342,273 |
| 8 | Not available | 2,901 | 274,290 |
| 9 | Concept not applicable | 1,123 | 104,115 |
| Total | | 333,008 | 32,852,323 |

Code 9 applies to persons living in Yukon, Northwest Territories and Nunavut. Draft 4.0's treatment of code 2 as below-MBM is correct.

## 2006 / 2011 replicate weights

Both user guides: eight random groups; SE = square root of (sum of squared deviations from the replicate mean, divided by 56).
