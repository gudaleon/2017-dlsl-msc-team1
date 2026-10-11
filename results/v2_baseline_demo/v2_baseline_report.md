# V2 Baseline: CMHC Housing Hardship Replication

**Generated:** 2026-10-11T02:24:32.694793

## Objective

Exact replication of CMHC 2024 revised Housing Hardship methodology using 2021 Census PUMF and 2018-base MBM thresholds.

## Sample

- **Persons:** 7,442
- **Total Households:** 3,000
- **Excluded:** 71
- **Analysis Sample:** 2,929

## Exclusions

- **zero_negative_total_income:** 71 households (2.4%)
- **zero_negative_disposable_income:** 0 households (0.0%)
- **negative_shelter_cost:** 0 households (0.0%)

## Results

### National Hardship Rate

**23.1%**

- CMHC reference: 7.8%
- Difference: +15.3%
- Status: ⚠ Review needed

### Rates by CMA

| CMA | Hardship Rate | Households in Hardship |
|-----|---------------|------------------------|
| 462 | 21.3% | 93 |
| 535 | 22.0% | 157 |
| 825 | 24.9% | 77 |
| 835 | 26.1% | 56 |
| 933 | 24.3% | 96 |
| 999 | 22.9% | 188 |

## Data Limitations

1. **CMA=999 ambiguous:** Requires lower/upper bound estimation
2. **PR=70 territories:** Cannot isolate Nunavut (CMHC excludes)
3. **Band housing:** TENUR=2 merges band with other subsidized housing

## Next Steps

- Implement bounded estimation for CMA=999
- Integrate full MBM geography mapping
- Document discrepancies with CMHC master file
- Prepare for V3 extension (shocks + assets)
