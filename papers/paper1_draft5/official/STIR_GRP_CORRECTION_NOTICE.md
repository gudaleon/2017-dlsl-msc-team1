# Statistics Canada correction notice — 2021 hierarchical PUMF `STIR_GRP`

Retrieved 17 October 2026 from:

https://www150.statcan.gc.ca/n1/pub/98m0001x/index-eng.htm

Catalogue 98M0001X. Release date 12 September 2023. Correction date 8 November 2024.

> Please be advised that a data discrepancy was detected in the Hierarchical file, 2021 Census PUMF that was originally released on March 20, 2024.
>
> A data error was discovered in the Shelter Cost to income ratio, groups (STIR_GRP) variable. The STIR_GRP variable was calculated using the in-file values of shelter cost divided by total household income; expressed as a percentage. However, STIR_GRP should have been calculated using the in-file values of Shelter Cost divided by the average monthly total household income; expressed as a percentage.

Stage 1 reconstruction on the local 2021 file agrees exactly with the corrected (monthly) definition. See `outputs/stir_grp_version_check.csv`.
