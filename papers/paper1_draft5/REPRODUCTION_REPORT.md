# Gate A — Draft 4.0 baseline reproduction

Date: 17 October 2026  
Code: `papers/paper1_draft5/stage1_verification.py` imports the frozen Draft 4.0 functions in `papers/paper1_draft4/reconstruct_four_wave.py` and does not modify that file or its outputs.  
Parent commit: `b298af382523b5a14ba2e515ccdefc23326883bd`

## Environment

- Python 3.12.3
- pandas 3.0.6, numpy 2.5.4
- Command: `python3 papers/paper1_draft5/stage1_verification.py`
- Run log: `papers/paper1_draft5/logs/stage1_run_environment.json`

## Input SHA-256

| Local path | Official identity | SHA-256 |
| --- | --- | --- |
| `data/raw/census_2006.csv` | 2006 Census hierarchical PUMF (95M0029X) | `e7c3e8cb2f6229f175c13f0db5f584922dc364996ab501846094b31e005ed9ef` |
| `data/raw/census_2006_pumf.csv` | 2011 NHS hierarchical PUMF (99M0002X) | `2823a68ae4103cb46df0d3d1a75125dce0382ba3a9c7c45431273f5a4c8a8bf0` |
| `data/raw/census_2011_nhs.csv` | 2016 Census hierarchical PUMF (98M0002X) | `a4ef58aadf3ff955594672e35900f519c949c99484ce3d710b18ba147ec52ceb` |
| `data/raw/census_2021_full.csv` | 2021 Census hierarchical PUMF (98M0002X) | `bd7260a59d98e2db1058dee8023b598c86ff9f6c6d3aa70cdb1df0bfc2fd1c67` |
| `data/raw/census_2016_pumf.csv` | Duplicate of the 2006 file (not used) | `e7c3e8cb2f6229f175c13f0db5f584922dc364996ab501846094b31e005ed9ef` |

The 2006 file and `census_2016_pumf.csv` have identical hashes, confirming the locked file-identity finding.

## Reproduction against the locked Draft 4.0 numbers

| Year | Survey | n | Locked n | N̂ | Locked N̂ | Hardship | Locked | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2011 | NHS | 130,242 | 130,242 | 13,019,080 | 13,019,080 | 18.1694% → 18.2% | 18.2% | PASS |
| 2016 | Census 2A-L | 139,869 | 139,869 | 14,037,793 | 14,037,793 | 17.3308% → 17.3% | 17.3% | PASS |
| 2021 | Census 2A-L | 148,085 | 148,085 | 14,863,013 | 14,863,013 | 14.9450% → 14.9% | 14.9% | PASS |

Sample-flow counts (tenure, income, and shelter drops) match `papers/paper1_draft4/outputs/sample_flow.csv` exactly. Owner / renter / one-person rates also match the frozen one-decimal Draft 4.0 table:

- 2011: owners 10.8%, renters 34.4%, one-person 32.4%
- 2016: owners 9.4%, renters 34.2%, one-person 32.2%
- 2021: owners 8.8%, renters 27.6%, one-person 30.3%

2006 all-household reconstruction was recomputed only as a diagnostic (n = 52,785, N̂ = 5,279,588, hardship 22.5%). It is **not** a comparable all-household series.

## What was verified

1. Input identity and SHA-256 hashes.
2. One `PRIHM==1` row per household; household income = sum of person `TOTINC_AT` after official NA codes.
3. Shelter = TENUR-conditioned `GROSRT`/`OMP` (2006, 2011) or `SHELCO` (2016, 2021).
4. Analytic rule: owner or renter, after-tax income > 0, valid shelter.
5. One `WEIGHT` copy per household.
6. Primary estimand: residual = income − 12 × monthly shelter; hardship if residual < national non-shelter MBM × √n / 2.

No silent recalibration was required. Gate A passed.

These remain research estimates, not official CMHC housing-hardship rates.
