# Next instruction set — Draft 5.0 (close remaining gaps)

**For the next Cursor agent.** Draft 4.0 is the frozen methods-reconstructed reference. Do not overwrite it. Do not overwrite Draft 3.0. Do not restart the file-identity audit. The household pipeline in `papers/paper1_draft4/reconstruct_four_wave.py` is the computational base.

This is **not** a formatting job. It is the next computational increment: close every remaining gap that the supplied PUMFs and official tables can support, quantify every gap that they cannot, and only then lock a publication series.

Interactive Draft 4.0 summary: https://cursor.com/canvas/store-0b0e7fe1-22d1-4c96-bffc-e7af685cdd0f/714d76a1-3970-48eb-b34d-42709ae77d08

---

## Locked facts (do not reopen)

1. Local filenames are wrong. True identity: `census_2006.csv` = 2006; `census_2006_pumf.csv` = 2011 NHS; `census_2011_nhs.csv` = 2016; `census_2016_pumf.csv` = duplicate 2006; `census_2021_full.csv` = 2021.
2. Unit is the household (`HH_ID`). Income = sum of person `TOTINC_AT` after official NA codes. Shelter = one maintainer (`PRIHM==1`) value. Weight = one `WEIGHT` per household.
3. Official CMHC hardship = residual income vs **non-shelter** MBM × `sqrt(n)/2`. Full MBM as the leftover line double-counts shelter.
4. Draft 3.0’s 38.0 / 33.9 / 37.9% figures are scrambled-year person-level `GROSRT`-only results. Do not reuse them as estimates.
5. 2016 is usable (99.4% household retention). 2006 all-household is **not** comparable (8888 shelter suppression; mean size 1.45). One-person 2006–2021 is the only four-wave shelter cut.
6. 2001 after-tax residual hardship is **not feasible**. Do not invent tax.
7. Reconstructed Draft 4.0 rates (weighted, national non-shelter size-adjusted MBM): **2011 18.2%; 2016 17.3%; 2021 14.9%**. These are research estimates, not official CMHC rates.

Preserve: `papers/paper1_highschool/` (Draft 3.0), `results/four_wave_temporal_results.json`, `audit/original/`, `papers/paper1_draft4/` outputs as the Draft 4.0 archive. Write Draft 5.0 under `papers/paper1_draft5/`.

Branch: `cursor/paper1-draft5-<short-name>-0ace` off `cursor/paper1-draft4-methods-0ace`. PR base: `cursor/paper1-draft4-methods-0ace`. Do not commit `data/raw/*.csv`, parquet, or LaTeX aux/log/toc.

---

## Priority 1 — Distance to official CMHC (must finish)

Draft 4.0 named the gaps. Draft 5.0 must **measure** them.

Produce one table, `distance_to_official_cmhc.csv`, with a row per closable rule and the 2011 / 2016 / 2021 weighted hardship rate after that rule is added, plus percentage-point change vs the Draft 4.0 primary rate.

Implement, in this order, as named variants (do not silently replace the primary series until the table exists):

| Variant | What to do | Status if impossible |
| --- | --- | --- |
| `D4_primary` | Copy Draft 4.0 primary (national non-shelter MBM × √n/2, `TOTINC_AT`, owner/renter, income>0, valid shelter) | Already computed |
| `drop_neg_residual` | Drop households with residual < 0 from the **universe** (CMHC 2020 Research Insight) | Must implement |
| `high_income_cap` | Equivalized after-tax income above the provincial (or national if no `PR`) median cannot be hardship | Must implement |
| `geo_cma_pr` | Use selected-CMA non-shelter MBM where `CMA` ∈ {462,535,825,835,933}; else provincial mean of Table 11-10-0066; else national mean | Must implement; label PROXY |
| `mbm_2008base_2020` | Score 2021 with 2008-base 2020 non-shelter MBM (already in `official/mbm_11-10-0066_national.json`) so the 2016–2021 change is not mixed with the 2018-base revision | Must implement |
| `ef_unit` | Repeat the residual test on **economic families** (`EF_ID`) using family-size of the EF, not HH. Report whether household vs EF moves the national rate by more than 1 pp | Must implement |
| `mbm_disposable` | Reconstruct ESDC/MBM disposable income | **NOT AVAILABLE** on these PUMFs — do not manufacture EI/CPP/childcare/mortgage-free adjustments. One paragraph, no proxy. |
| `mbm_50_region` | Assign official 50 MBM regions | **NOT AVAILABLE** — PUMF has 6 CMA codes + PR. Stop after the CMA/PR proxy. |

**Decision rule after the table.** If `drop_neg_residual` + `geo_cma_pr` together move 2016/2021 by more than 2 pp, the Draft 5.0 **headline** series becomes that closer-to-CMHC variant and Draft 4.0 primary is the robustness column. If they move it by ≤2 pp, keep Draft 4.0 primary as headline and put the closer-to-CMHC variant in Table 5. Either way, the manuscript must show both.

Do not present any Draft 5.0 rate as an official CMHC number.

---

## Priority 2 — Recover missing official documents

Download and **retain** (small extracts in `papers/paper1_draft5/official/`, not 20 MB dumps unless needed):

1. **CMHC 2024 Census hardship update** — *New insights on affordability* (NH18-33/85-2024E-PDF). Try CMHC, publications.gc.ca, Internet Archive, university caches. If a Canada-wide 2021 Census hardship rate is found, add it to `published_benchmarks.json` and the validation table. If not found, keep UNRESOLVED and stop searching after the listed sources.
2. **Year-specific PUMF user-guide pages** for: 2006 `REGION` 1–6; 2011/2016 `LOMBM` codes; 2021 `STIR_GRP` and `LOMBM_2018`; replicate-weight formula (`WT1`–`WT16`). Sources already cited in `audit/FOUR_WAVE_AUDIT_REPORT.md` (DLI 95M0029XVB, 99M0002X, 98M0002X). Confirm or retire the UNCERTAIN labels.
3. **2011 NHS non-response** — one official citation for the voluntary-survey break (do not invent a correction factor).

If a codebook page contradicts Draft 4.0 (`LOMBM==2` as poor; `STIR_GRP==1` as 30%+; 2006 REGION = Atlantic/QC/ON/Prairies/BC/Territories), fix the validation report and say so. Do not “smooth over” a contradiction.

---

## Priority 3 — 2020 COVID income and the 2016–2021 decline

2021 income is calendar **2020** and includes emergency benefits. The 2021 file has `EFCOVID_ERB`.

- Build a household (or EF) COVID-transfer indicator from `EFCOVID_ERB` using the codebook, not guesswork.
- Report reconstructed hardship **with and without** households that received ERB, or a residual that subtracts documented ERB if the variable is a dollar amount.
- If `EFCOVID_ERB` is only a flag, report hardship rates split by flag. Do not invent dollar amounts.
- State how much of the −2.4 pp (2016→2021) decline is associated with ERB households versus the 2018-base MBM revision (`mbm_2008base_2020` from Priority 1).

This is the main threat to reading 14.9% as a structural improvement.

---

## Priority 4 — Publication series lock

After Priorities 1–3, lock **exactly these** series and no others:

| Series | Waves | Status required before lock |
| --- | --- | --- |
| A. Headline all-household | 2011, 2016, 2021 | Chosen by Priority 1 decision rule; NHS break stated |
| B. One-person robustness | 2006, 2011, 2016, 2021 | Same threshold family as A |
| C. Tenure split | 2011, 2016, 2021 owners / renters | Same as A |
| D. Distance-to-CMHC | 2011, 2016, 2021 | Priority 1 table |
| E. COVID / MBM-base decomposition | 2021 vs 2016 | Priority 3 |

Do **not** lock: 2006 all-household; 2001; Draft 3.0 person-level rates; full-MBM leftover as a headline.

Write `papers/paper1_draft5/SERIES_LOCK.md` with the locked numbers, sample n, estimated N, and a one-sentence estimand for each series.

---

## Priority 5 — Independent validation add-ons

Keep Draft 4.0 checks (household counts, median income, 2021 core need). Add:

1. Owner / renter reconstructed hardship vs published core need (2021: 5.3% / 20.0%) and unaffordable housing (2021: 14.8% / 33.2%) — explain the expected gap (hardship ≠ core need ≠ STIR).
2. Weighted tenure shares vs published ownership rate (2021: 66.5%).
3. If the 2024 CMHC Census rate is recovered, a direct comparison with Series A and D.
4. One-person median income vs published one-person household medians if a StatCan table is found; otherwise mark UNCERTAIN.

Explain discrepancies. Do not dismiss them.

---

## Priority 6 — Draft 5.0 manuscript and package (only after Series A is locked)

Only after `SERIES_LOCK.md` exists and validation is updated:

1. Copy Draft 4.0 figure/table style (Okabe–Ito, equal-spaced 2011/2016/2021, white background). Do not edit `papers/paper1_highschool/`.
2. Regenerate five figures and five tables from locked Series A–E. Figure 5 must include the one-person 2006–2021 panel and a “not official CMHC” caption.
3. Manuscript `paper1_draft5.tex`: high-school IMRAD; Methods = `REVISED_METHODS.md` plus Priority 1–3 decisions; Results use locked numbers; Discussion states the COVID and MBM-base threats; Limitations copy unresolved items that remain after this pass.
4. New Drive folder `Draft_5.0` under `Paper1_HighSchool_LaTeX` (`1DrIvYHuCTvQOEqzp1IfHwCw5RcEhxf2m`). Do **not** write into Draft 3.0 (`1bhoL_OB66mXfrkGX_ZPMl4EHJg2vS9Me`) or Draft 4.0 (`13Md3OCtWXfxYq16IU7JVzo4caYykb3a0`).
5. Commit, push, open/update the Draft 5.0 PR via `ManagePullRequest` (base `cursor/paper1-draft4-methods-0ace`).

---

## Explicitly forbidden

- Overwriting Draft 3.0 or Draft 4.0 outputs.
- Imputing 2006 suppressed `OMP`/`GROSRT`.
- Inventing 2001 after-tax income or MBM disposable income.
- Calling any PUMF residual rate an official CMHC housing-hardship rate.
- Using `results/four_wave_temporal_results.json` as analytic input.
- Treating 2011 as interchangeable with a Census long form.
- Replacing the headline series before the distance-to-CMHC table exists.
- Downloading another 2016 hierarchical PUMF.

---

## Done when

- [ ] `distance_to_official_cmhc.csv` exists with all implementable variants.
- [ ] Headline series chosen by the written decision rule.
- [ ] Codebook UNCERTAIN labels confirmed or retired (REGION, LOMBM, STIR_GRP, replicate weights).
- [ ] 2024 CMHC Census rate recovered **or** logged as still missing after the listed sources.
- [ ] COVID/ERB and 2008-base 2020 decomposition of the 2016–2021 decline is in the validation report.
- [ ] `SERIES_LOCK.md` written.
- [ ] Five figures, five tables, manuscript, and a new Drive `Draft_5.0` folder exist.
- [ ] Unresolved issues that remain are listed, not hidden.

Reproduce Draft 4.0 first (`python3 papers/paper1_draft4/reconstruct_four_wave.py`) before changing any estimand, so the distance table is against a verified baseline.
