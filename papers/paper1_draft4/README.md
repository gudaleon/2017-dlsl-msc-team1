# Paper 1 Draft 4.0 — Methodological reconstruction

Draft 3.0 (`papers/paper1_highschool/`) is frozen. This folder is the Draft 4.0 reconstruction. It does **not** overwrite Draft 3.0 figures, tables, or the original `results/four_wave_temporal_results.json`.

The task is computational, not formatting. The pipeline rebuilds household income, shelter, tenure and weights from the original Statistics Canada hierarchical PUMFs and official MBM / CPI tables.

## Do not treat these as official CMHC rates

The reconstructed hardship rate uses Census after-tax income (`TOTINC_AT`) and a national-average non-shelter MBM. Official CMHC housing hardship uses MBM disposable income, 50-region MBM geography, and additional universe restrictions. Gaps versus the published CIS ~9% rate are expected and are explained in the validation report.

## How to reproduce

```bash
python3 papers/paper1_draft4/reconstruct_four_wave.py
```

Requires the five local CSVs under `data/raw/` (gitignored). Identity mapping is in `audit/codebook_mappings.md` and `VARIABLE_CROSSWALK.md`.

Interactive summary: [Draft 4.0 methods reconstruction](https://cursor.com/canvas/store-0b0e7fe1-22d1-4c96-bffc-e7af685cdd0f/714d76a1-3970-48eb-b34d-42709ae77d08).

Google Drive (new folder; Draft 3.0 not overwritten): https://drive.google.com/drive/folders/13Md3OCtWXfxYq16IU7JVzo4caYykb3a0

## Outputs

| Path | Contents |
| --- | --- |
| `outputs/draft4_reconstruction.json` | Full machine-readable results |
| `outputs/sample_flow.csv` | Person → household → analytic sample |
| `outputs/primary_estimates.csv` | Weighted household estimates |
| `outputs/validation.csv` | Comparisons with published StatCan / CMHC figures |
| `outputs/sensitivity.csv` | Alternative thresholds, weights, exclusions |
| `outputs/shelter_coverage_by_size.csv` | Why 2006 all-household results are not comparable |

## Documents

- `METHODS_AUDIT.md` — unit of analysis, file identity, 2006/2016 retention
- `VARIABLE_CROSSWALK.md` — year-specific variables and missing codes
- `SAMPLE_FLOW.md` — narrative sample-flow table
- `VALIDATION_REPORT.md` — independent checks
- `UNRESOLVED_ISSUES.md` — what still cannot be implemented
- `REVISED_METHODS.md` — replacement Methods section
- `official/` — CPI, MBM and published-benchmark extracts
