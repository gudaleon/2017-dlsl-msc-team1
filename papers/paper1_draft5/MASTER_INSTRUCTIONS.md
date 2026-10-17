# CURSOR MASTER INSTRUCTIONS
## Jason Wu Housing Research — Draft 5.0
### Methodological Convergence, Independent Validation, and Manuscript Preparation

**Objective:** Complete the remaining scientific analysis needed to produce a defensible, reproducible high-school research paper on Canadian housing affordability and residual-income hardship.

The immediate goal is to determine which findings can be supported by the available Statistics Canada microdata, quantify departures from official CMHC methodology, and explain the apparent decline in housing hardship from 2016 to 2021.

Do not prioritize manuscript formatting or attractive figures until the statistical results are sufficiently validated.

---

## 0. Repository and version-control requirements

Start from:

`cursor/paper1-draft4-methods-0ace`

Create a new branch:

`cursor/paper1-draft5-validation-0ace`

Write all new analysis and documentation into:

`papers/paper1_draft5/`

**Do not overwrite:**

- `papers/paper1_highschool/`
- `papers/paper1_draft4/`
- Draft 3.0 Google Drive folder: `1bhoL_OB66mXfrkGX_ZPMl4EHJg2vS9Me`
- Draft 4.0 Google Drive folder: `13Md3OCtWXfxYq16IU7JVzo4caYykb3a0`

Before execution, read:

`papers/paper1_draft4/NEXT_AGENT_INSTRUCTIONS.md`

Treat that document and the frozen Draft 4.0 record as controlling project context. If any instruction here conflicts with the repository's existing research contract, record the conflict and request a decision rather than silently overriding a methodological requirement.

Record the parent commit hash, dependency versions, dataset checksums, execution commands, and run environment.

Do not change frozen results.

---

## 1. Locked Draft 4.0 baseline

Treat the following as the existing reconstruction, which must first be reproduced:

| Year | Analytic households | Estimated population households | Hardship |
|---|---:|---:|---:|
| 2011 NHS | 130,242 | 13,019,080 | 18.2% |
| 2016 Census | 139,869 | 14,037,793 | 17.3% |
| 2021 Census | 148,085 | 14,863,013 | 14.9% |

These are **research estimates, not official CMHC housing-hardship rates**.

Other locked conclusions:

- Analytical unit: household, not person.
- 2016 Census successfully restored, with 99.4% retention.
- 2006 all-household series fails comparability and income-validation checks.
- 2001 after-tax residual-income series is currently infeasible.
- Draft 3.0's approximately 38% hardship estimates must not be reused as valid population estimates.
- No invented MBM disposable income, geographic identifiers, shelter values, or COVID benefit amounts.
- Current baseline uses a non-shelter MBM threshold scaled for family size.

For the scaling formula, explicitly verify the intended expression:

\[
T(n)=T(4)\frac{\sqrt{n}}{2}
\]

Here `n` must be the documented relevant household or economic-family size. Never assume those concepts are interchangeable.

### Gate A — Baseline reproducibility

Run the frozen Draft 4.0 analytical code without altering its methodology.

Verify:

1. Input dataset identity and SHA-256 hashes.
2. Household-record extraction and record linkage.
3. Household income and shelter-cost definitions.
4. Sample inclusion and exclusion counts.
5. Survey weighting and estimated household totals.
6. Reproduction of the published Draft 4.0 results.

Generate `baseline_reproduction.csv` and `REPRODUCTION_REPORT.md`.

If results do not reproduce, diagnose and record the discrepancy before proceeding. Do not silently recalibrate the code to force agreement.

---

## 2. Priority 1 — Distance to official CMHC methodology

This is the most important analytical extension.

Create an explicit comparison between the reconstructed Draft 4.0 methodology and the best documented implementation of CMHC's housing-hardship methodology supported by the available PUMFs.

### Required scenarios

For 2011, 2016 and 2021, evaluate:

- **M0:** Exact Draft 4.0 baseline.
- **M1:** Exclude observations with negative residual income.
- **M2:** Apply any documented high-income restriction consistent with the relevant CMHC methodology.
- **M3:** Replace the national MBM approximation with the most defensible geography-sensitive threshold supported by the PUMF.
- **M4:** Evaluate a consistently constructed 2008-base MBM sensitivity for the applicable reference year, including 2020.
- **M5:** Evaluate economic-family (`EF_ID`) definitions where the variables genuinely support them.
- **M6:** Combined closest-feasible CMHC-like specification, using only validated and documented components.

For each scenario, record:

- Year and survey.
- Exact eligibility criteria.
- Analytical unit.
- Income concept.
- Shelter-cost concept.
- MBM base and threshold components.
- Household or economic-family scaling.
- Geography approximation.
- Inclusion/exclusion counts.
- Weighted population denominator.
- Weighted hardship percentage.
- Difference from Draft 4.0 in percentage points.
- Uncertainty estimates, where defensible.
- Whether the specification is fully implemented, approximated, or unavailable.

**Important safeguards:**

Negative residual income may represent genuine severe hardship. Excluding those observations changes the population being analyzed. Quantify the exclusion rate and describe the resulting selection effect; do not imply that exclusion is inherently more correct.

Do not introduce an arbitrary high-income cap. Implement it only when supported by a documented methodological rule.

Do not treat household and economic-family units as interchangeable. If shelter costs cannot be attributed to economic families without an unsupported allocation rule, mark that scenario NOT IMPLEMENTABLE rather than inventing an allocation.

Mark the following explicitly where they remain unavailable:

- Official MBM disposable income.
- Exact official 50-region MBM geographic classification.
- Other variables or exclusions required for CMHC equivalence.

**Output:** `distance_to_official_cmhc.csv`

### Headline selection rule

Retain the proposed 2-percentage-point threshold as a prespecified **review trigger**.

If the combined, properly validated M6 specification differs from M0 by more than 2 percentage points in either 2016 or 2021:

1. Flag this as a material methodological sensitivity.
2. Determine whether M6 is conceptually and empirically more defensible than M0.
3. Promote M6 to the candidate headline only if its assumptions, analytical population, and cross-year implementation are consistent and independently validated.
4. Otherwise, preserve M0 as provisional and explicitly report that headline selection remains unresolved.

If the difference is 2 percentage points or less, retain M0 as the provisional primary specification and M6 as sensitivity analysis, provided M0 passes validation.

Do not choose a specification because its results are closer to a desirable conclusion or a published numerical estimate.

Never label either specification an official CMHC calculation.

---

## 3. Priority 2 — Recover and verify official documentation

### CMHC publication

Investigate:

*New Insights on Affordability: Update on Housing Hardship from the 2021 Census*

Catalogue: `NH18-33/85-2024E-PDF`

Government catalogue:

https://publications.gc.ca/site/eng/9.949944/publication.html

The catalogue reports that the PDF was withdrawn on November 25, 2025, at CMHC's request.

Search legitimate available copies or technical summaries through:

- CMHC publications and research archives.
- Government of Canada Publications.
- Library and Archives Canada.
- Internet Archive.
- University library holdings.
- Indexed research references citing the report.

If the complete document is unavailable, record its bibliographic identity, documented withdrawal, retrieval attempts, and exactly which findings remain unverified.

Do not invent the 2021 CMHC hardship rate.

### Statistics Canada PUMF documentation

Check year-specific dictionaries for:

- `REGION`
- `LOMBM`
- `STIR_GRP`
- `EF_ID`
- `EFCOVID_ERB`
- Household and economic-family identifiers.
- Sampling and replicate weights.
- Housing tenure and shelter-cost variables.
- Household income and relevant after-tax income definitions.

For the 2021 hierarchical PUMF, specifically investigate the corrected `STIR_GRP` definition and November 2024 correction notice:

https://www150.statcan.gc.ca/n1/pub/98m0001x/index-eng.htm

Verify whether the project's local 2021 PUMF is the corrected version. Independently calculate STIR from compatible income and shelter fields wherever feasible.

Review Statistics Canada MBM table 11-10-0066-01 for component-specific thresholds and base years:

https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1110006601

### Deliverables

- `SOURCE_VERIFICATION_LEDGER.csv`
- `PUMF_VARIABLE_CROSSWALK_v05.csv`
- `CMHC_DOCUMENT_RECOVERY.md`
- Revised validation report if the official documentation contradicts any existing assumptions.

Each reported method must have a traceable documentation source.

---

## 4. Priority 3 — Investigate the 2016–2021 decline

The Draft 4.0 baseline shows:

- 2016: 17.3%.
- 2021: 14.9%.
- Change: −2.4 percentage points.

The central question is:

**How much confidence can we place in this decline, and what methodological or socioeconomic factors might contribute to it?**

### A. MBM base-year sensitivity

Recalculate compatible measures using consistently defined 2008-base and 2018-base MBM components, where available.

Do not mix reference-year thresholds or monetary units.

Report whether the direction and magnitude of the 2016–2021 change survive these methodological alternatives.

### B. COVID emergency and recovery benefits

Inspect `EFCOVID_ERB` in the 2021 codebook.

Determine whether it records:

- Benefit receipt status.
- Benefit amounts.
- Categories or bands.
- Other information.

Use only what is actually present.

Estimate 2021 hardship separately by available ERB categories, reporting weighted sample sizes and rates.

Do not subtract hypothetical benefits or create counterfactual income amounts if the data only provide receipt indicators.

### C. Population composition

Investigate changes in the shares and rates of:

- Owner-occupied and renter households.
- One-person and multi-person households.
- Available household-size categories.
- Available income strata.

Use an appropriate descriptive standardization or decomposition to distinguish changes in group composition from changes in group-specific hardship rates.

Clearly distinguish descriptive decomposition from causal explanation.

### D. Timing

Check the income reference periods for all Census waves, especially that 2021 Census income variables typically reference 2020.

Discuss pandemic income supports and their potential implications without attributing observed changes to them causally unless the data support that inference.

### Deliverables

- `covid_erb_stratification.csv`
- `mbm_base_sensitivity.csv`
- `composition_decomposition.csv`
- `COVID_MBM_DECOMPOSITION.md`

The final report must clearly separate findings supported by the data, possible explanations, and factors that remain unidentifiable.

---

## 5. Priority 4 — Lock defensible analytical series

Create `SERIES_LOCK.md`.

Evaluate the following candidates individually:

**Series A — 2011–2021 all-household analysis**

Primary candidate for the high-school manuscript, subject to validation and sensitivity tests.

**Series B — 2006–2021 one-person households**

Separate historical extension. Lock only if comparable income, shelter costs, record selection and threshold construction are verified for all required years.

Do not infer that one-person results represent all Canadian households.

**Series C — Owner versus renter hardship**

Check weighted tenure classifications and their consistency across years.

**Series D — Distance-to-CMHC specifications**

Document all implemented variants, approximations, and unavailable official methodology elements.

**Series E — COVID/MBM-base sensitivity and decomposition**

Preserve both alternative-threshold results and descriptive subgroup analyses.

For each series, assign:

`LOCKED / PROVISIONAL / REJECTED / NOT AVAILABLE`

Document the supporting data, analytical unit, year coverage, equations, code location, methodological qualifications, sample sizes and uncertainty.

Do not lock the 2006 all-household series or Draft 3.0 person-based rates.

### Gate B — Series acceptance

A primary series should not be locked until:

1. Analytical unit and denominator are coherent.
2. Variable definitions are reproducible.
3. Survey weights are correctly handled.
4. Major sample exclusions are explained.
5. Time and price references are consistent.
6. Independent benchmarks and sensitivity results have been reviewed.
7. Important unresolved limitations are prominently documented.

If these conditions fail, leave the series provisional and explain what additional evidence is necessary.

---

## 6. Priority 5 — Independent statistical validation

Reproduce or compare relevant 2021 external benchmarks, including:

- Homeownership: approximately 66.5%.
- Core housing need: owners approximately 5.3%, renters approximately 20.0%.
- Unaffordable housing: owners approximately 14.8%, renters approximately 33.2%.
- Overall core housing need: approximately 10.1%.
- Official CMHC 2021 hardship rate, only if independently recovered and verified.

Before making comparisons, verify each benchmark's exact publication, reference year, definition, geographic scope, and denominator.

Do not compare household-level hardship with economic-family-level statistics as if they measured the same population.

Core housing need, STIR-based unaffordability, and residual-income hardship are **different indicators**. Agreement in direction or ranking can be informative, but their numerical values need not coincide.

### Uncertainty analysis

Investigate the documented replicate-weight methodology for each Census wave.

If applicable replicate weights and valid variance formulas are available, calculate design-appropriate confidence intervals.

If they are not available, do not present ordinary independent-observation bootstrap intervals as survey-design confidence intervals.

Document the resulting limitations on statistical inference.

### Deliverables

- `INDEPENDENT_VALIDATION_v05.csv`
- `UNCERTAINTY_METHODS.md`
- `VALIDATION_REPORT_v05.md`

---

## 7. Priority 6 — Reconstruct the publication only after verification

Once an acceptable primary series has been established, create:

`papers/paper1_draft5/paper1_draft5.tex`

### Main text

Prepare a conventional scientific manuscript suitable for peer review at a high-school research journal:

1. Abstract
2. Introduction and research questions
3. Data and Methods
4. Results
5. Discussion
6. Limitations
7. Conclusions
8. References

Methods must explain the exact implemented calculations, not intended calculations.

The central research question should remain neutral:

*How do conventional shelter-cost burden and residual-income-based hardship indicators characterize changes in Canadian housing affordability?*

Do not assert that the analysis proves a structural crisis, successful government policies, or the causal effects of COVID benefits.

### Title and study period

If the primary series covers only 2011–2021, revise the title accordingly. A separate validated 2006 one-person analysis may be presented as a historical extension, but it does not justify describing the all-household analysis as a 15-year series.

### Tables and figures

Produce five high-quality main-text figures and five main-text tables, prioritizing:

- Sample flow and data validation.
- Verified hardship trends.
- Owner-renter comparisons.
- Methodological sensitivity and distance to CMHC.
- MBM-base and COVID-related analyses.

Do not force precisely five if a different number better serves the scientific argument. Archive all intermediate diagnostics and provide relevant additional analyses as Supplementary Information.

All figures should use validated source tables, readable labels, vector outputs, and full-page rendering checks.

### Supplementary Information

Include:

- Dataset provenance and record-level processing.
- Variable definitions and crosswalk.
- Threshold and weighting equations.
- Sample exclusion tables.
- Sensitivity and variance-estimation methods.
- Validation comparisons.
- Full computational reproducibility instructions.

---

## 8. Drive organization and preservation

Create:

`Draft_5.0`

under Google Drive folder:

`1DrIvYHuCTvQOEqzp1IfHwCw5RcEhxf2m`

Preserve Drafts 3.0 and 4.0 unchanged.

Within Draft 5.0, organize the outputs into:

- `01_Methods_and_Data_Audit`
- `02_Validation_and_Sensitivity`
- `03_Figures_and_Tables`
- `04_Manuscript_and_SI`
- `05_Code_and_Run_Logs`

Upload verified completed outputs to Drive and preserve full binary outputs in the version-controlled research package.

If a Drive upload fails, record the error and provide a verified alternative. Never upload a truncated or corrupted publication file.

Write `CURRENT.md` identifying the most recent validated outputs and unresolved questions.

---

## 9. Mandatory completion criteria

The analytical phase is complete only when the following exist and have been checked:

- [ ] Draft 4.0 baseline reproduction report.
- [ ] `distance_to_official_cmhc.csv`.
- [ ] CMHC publication recovery result or documented unavailability.
- [ ] Corrected PUMF codebook and variable validation.
- [ ] `COVID_MBM_DECOMPOSITION.md`.
- [ ] `SERIES_LOCK.md`.
- [ ] Updated independent validation and uncertainty reports.
- [ ] Updated `UNRESOLVED_ISSUES.md`.

**Do not proceed to manuscript finalization while essential primary-series validation remains unresolved.**

At completion, return a concise research handover describing:

1. Which findings changed from Draft 4.0 and why.
2. Which analytical series passed validation.
3. What results can responsibly be published.
4. What remains unresolved.
5. What further data or documentation, if any, the researcher must provide.
6. The exact Git branch, commit and Google Drive location.

The objective is a scientifically defensible paper, not a predetermined conclusion or a polished manuscript built on unverified assumptions.
