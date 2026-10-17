# Paper 1 Draft 4.0 revision log

Date: 17 October 2026

Draft 3.0 is the graphics-corrected reference. This draft does not overwrite it.

## What changed

- Unit of analysis: household (`HH_ID`), not person rows.
- Income: sum of person `TOTINC_AT` after official NA codes.
- Shelter: `TENUR`-conditioned `OMP`/`GROSRT` or `SHELCO`; one value per household.
- Weights: one `WEIGHT` per household; sample n and estimated N reported separately.
- File identity: 2006 / 2011 NHS / 2016 / 2021 mapped from catalogues, not filenames.
- 2016 restored (99.4% household retention). The old 9.4% figure was the 2006 file under a renter-only cleaner.
- 2006 all-household series removed from the primary charts (8888 shelter suppression).
- Threshold: official CMHC concept reconstructed as non-shelter MBM × √n / 2 from Table 11-10-0066. Not presented as official CMHC rates.
- CPI: Table 18-10-0005 income-year factors, used only for dollar medians.
- Validation against published household counts, Census medians, unaffordable housing, and 2021 core need.
- Sensitivity for full MBM, single-adult line, Draft 3 leftover, geography, negative residual, tenure.

## What did not change

- Draft 3.0 manuscript, figures and tables stay in `papers/paper1_highschool/`.
- Original JSON stays at `results/four_wave_temporal_results.json`.
