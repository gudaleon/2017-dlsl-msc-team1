#!/usr/bin/env python3
"""Repaired four-wave household analysis after file-identity and codebook audit.

Does not invent 2016 microdata. The file labeled census_2011_nhs.csv is the
2016 hierarchical PUMF (SHELCO present; household count matches the 2016 1%
sample). The file labeled census_2016_pumf.csv is a duplicate of 2006.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path("audit/outputs")
OUT.mkdir(parents=True, exist_ok=True)

# Bank of Canada / CPI all-items factors used in the original pipeline.
# Flagged in the report as needing CANSIM 18-10-0005 confirmation.
CPI_TO_2021 = {2006: 1.276, 2011: 1.148, 2016: 1.082, 2021: 1.000}

# Single-adult national-average MBM leftover-income lines used previously.
# Not household-size adjusted. Official MBM tables still need a citation pass.
MBM_SINGLE_ADULT = {2006: 13500, 2011: 15000, 2016: 17000, 2021: 19728}

INCOME_NA = {888888, 999999, 8888888, 9999999, 88888888, 99999999}
SHELTER_NA = {8888, 9999, 88888, 99999}

# Identity from official hierarchical sample sizes + codebook markers.
WAVES = {
    2006: {
        "path": "data/raw/census_2006.csv",
        "identity": "2006 Census hierarchical PUMF (95M0029X); 309,841 persons / 124,358 HH",
        "shelter_mode": "grosrt_omp",
    },
    2011: {
        "path": "data/raw/census_2006_pumf.csv",
        "identity": "2011 NHS hierarchical PUMF (99M0002X); 333,008 persons / 133,192 HH; codebook total matches",
        "shelter_mode": "grosrt_omp",
    },
    2016: {
        "path": "data/raw/census_2011_nhs.csv",
        "identity": "2016 Census hierarchical PUMF (98M0002X); 343,330 persons / 140,720 HH ≈ 1% of 14,072,079 private households",
        "shelter_mode": "shelco",
    },
    2021: {
        "path": "data/raw/census_2021_full.csv",
        "identity": "2021 Census hierarchical PUMF (98M0002X); 361,915 persons / 149,789 HH",
        "shelter_mode": "shelco",
    },
}


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def valid_income(s: pd.Series) -> pd.Series:
    x = _num(s)
    return x.where(~x.isin(INCOME_NA))


def valid_shelter(s: pd.Series) -> pd.Series:
    x = _num(s)
    return x.where(~x.isin(SHELTER_NA) & (x > 0) & (x < 10000))


def person_shelter(df: pd.DataFrame, mode: str) -> pd.Series:
    if mode == "shelco":
        if "SHELCO" not in df.columns:
            raise KeyError("SHELCO missing on a wave that should have it")
        return valid_shelter(df["SHELCO"])
    grosrt = valid_shelter(df["GROSRT"]) if "GROSRT" in df.columns else pd.Series(np.nan, index=df.index)
    omp = valid_shelter(df["OMP"]) if "OMP" in df.columns else pd.Series(np.nan, index=df.index)
    tenur = _num(df["TENUR"]) if "TENUR" in df.columns else pd.Series(np.nan, index=df.index)
    # Official 2006/2011: 1 = owned, 2 = rented (2011: rented or band).
    out = pd.Series(np.nan, index=df.index)
    out = out.mask(tenur == 1, omp)
    out = out.mask(tenur == 2, grosrt)
    # If tenure is missing but exactly one of GROSRT/OMP is valid, use that.
    only_g = grosrt.notna() & omp.isna()
    only_o = omp.notna() & grosrt.isna()
    out = out.fillna(grosrt.where(only_g))
    out = out.fillna(omp.where(only_o))
    return out


def householdize(df: pd.DataFrame, year: int, mode: str) -> pd.DataFrame:
    df = df.copy()
    df["inc_at"] = valid_income(df["TOTINC_AT"] if "TOTINC_AT" in df.columns else df["TOTINC"])
    df["inc_bt"] = valid_income(df["TOTINC"]) if "TOTINC" in df.columns else np.nan
    df["shelter_m"] = person_shelter(df, mode)
    df["weight"] = _num(df["WEIGHT"]) if "WEIGHT" in df.columns else 1.0
    df["tenur"] = _num(df["TENUR"]) if "TENUR" in df.columns else np.nan

    g = df.groupby("HH_ID", sort=False)
    hh = pd.DataFrame(
        {
            "n_persons": g.size(),
            "hh_income_at": g["inc_at"].sum(min_count=1),
            "n_income_at": g["inc_at"].count(),
            "hh_income_bt": g["inc_bt"].sum(min_count=1),
            "shelter_m": g["shelter_m"].median(),
            "tenur": g["tenur"].median(),
            "weight": g["weight"].first(),
        }
    )
    hh["year"] = year
    hh["cpi"] = CPI_TO_2021[year]
    hh["income_at_2021"] = hh["hh_income_at"] * hh["cpi"]
    hh["shelter_m_2021"] = hh["shelter_m"] * hh["cpi"]
    hh["annual_shelter_2021"] = hh["shelter_m_2021"] * 12
    hh["residual_at"] = hh["income_at_2021"] - hh["annual_shelter_2021"]
    hh["stir"] = hh["annual_shelter_2021"] / hh["income_at_2021"].clip(lower=1)
    hh["hardship"] = (hh["residual_at"] < MBM_SINGLE_ADULT[year]).astype("float")
    hh["is_owner"] = hh["tenur"] == 1
    hh["is_renter"] = hh["tenur"] == 2
    keep = (
        hh["hh_income_at"].notna()
        & (hh["hh_income_at"] > 0)
        & hh["shelter_m"].notna()
        & (hh["n_income_at"] > 0)
    )
    return hh, keep


def wmean(s: pd.Series, w: pd.Series) -> float:
    w = w.fillna(0)
    if w.sum() <= 0:
        return float(s.mean())
    return float(np.average(s, weights=w))


def wmedian(s: pd.Series, w: pd.Series) -> float:
    d = pd.DataFrame({"s": s, "w": w.fillna(0)}).dropna()
    d = d[d["w"] > 0].sort_values("s")
    if d.empty:
        return float("nan")
    cdf = d["w"].cumsum()
    cutoff = d["w"].sum() / 2.0
    return float(d.loc[cdf >= cutoff, "s"].iloc[0])


def summarize(hh: pd.DataFrame, keep: pd.Series, year: int, identity: str, n_person: int) -> dict:
    d = hh.loc[keep].copy()
    w = d["weight"]
    out = {
        "year": year,
        "file_identity": identity,
        "unit": "household (one row per HH_ID)",
        "income_definition": "sum of person TOTINC_AT excluding not-available/not-applicable codes",
        "shelter_definition": "SHELCO if present, else TENUR-conditioned GROSRT (rent) + OMP (own)",
        "person_records_in_file": n_person,
        "households_in_file": int(len(hh)),
        "households_valid": int(keep.sum()),
        "retention_pct_of_households": float(keep.mean() * 100),
        "income_at_2021": {
            "median_unweighted": float(d["income_at_2021"].median()),
            "median_weighted": wmedian(d["income_at_2021"], w),
            "p25_unweighted": float(d["income_at_2021"].quantile(0.25)),
            "p75_unweighted": float(d["income_at_2021"].quantile(0.75)),
        },
        "shelter_m_2021": {
            "median_unweighted": float(d["shelter_m_2021"].median()),
            "median_weighted": wmedian(d["shelter_m_2021"], w),
            "p25_unweighted": float(d["shelter_m_2021"].quantile(0.25)),
            "p75_unweighted": float(d["shelter_m_2021"].quantile(0.75)),
        },
        "stir": {
            "median_unweighted": float(d["stir"].median()),
            "pct_above_30_unweighted": float((d["stir"] > 0.30).mean() * 100),
            "pct_above_30_weighted": wmean((d["stir"] > 0.30).astype(float), w) * 100,
            "pct_above_50_unweighted": float((d["stir"] > 0.50).mean() * 100),
        },
        "hardship": {
            "mbm_single_adult": MBM_SINGLE_ADULT[year],
            "rate_unweighted_pct": float(d["hardship"].mean() * 100),
            "rate_weighted_pct": wmean(d["hardship"], w) * 100,
            "count": int(d["hardship"].sum()),
        },
        "tenure": {
            "owner_hardship_unweighted_pct": float(d.loc[d["is_owner"], "hardship"].mean() * 100)
            if d["is_owner"].any()
            else None,
            "renter_hardship_unweighted_pct": float(d.loc[d["is_renter"], "hardship"].mean() * 100)
            if d["is_renter"].any()
            else None,
            "n_owner": int(d["is_owner"].sum()),
            "n_renter": int(d["is_renter"].sum()),
        },
        "diagnostics": {
            "mean_persons_per_valid_hh": float(d["n_persons"].mean()),
            "median_persons_per_valid_hh": float(d["n_persons"].median()),
        },
    }
    return out


def main() -> None:
    results = []
    drop_logs = []
    for year, spec in WAVES.items():
        path = Path(spec["path"])
        print(f"\n=== {year} ← {path} ===")
        print(spec["identity"])
        df = pd.read_csv(path, low_memory=False)
        hh, keep = householdize(df, year, spec["shelter_mode"])
        rec = summarize(hh, keep, year, spec["identity"], len(df))
        results.append(rec)
        drop_logs.append(
            {
                "year": year,
                "person_rows": len(df),
                "households": int(len(hh)),
                "dropped_no_income": int((hh["hh_income_at"].isna() | (hh["hh_income_at"] <= 0)).sum()),
                "dropped_no_shelter": int(hh["shelter_m"].isna().sum()),
                "valid_households": int(keep.sum()),
            }
        )
        one = keep & (hh["n_persons"] == 1)
        rec_one = summarize(hh, one, year, spec["identity"], len(df))
        rec_one["restriction"] = "one-person households only"
        rec["one_person_households"] = {
            "households_in_file": int((hh["n_persons"] == 1).sum()),
            "households_valid": rec_one["households_valid"],
            "retention_pct_of_one_person_hh": float(
                rec_one["households_valid"] / max(int((hh["n_persons"] == 1).sum()), 1) * 100
            ),
            "median_income_2021": rec_one["income_at_2021"]["median_unweighted"],
            "median_shelter_2021": rec_one["shelter_m_2021"]["median_unweighted"],
            "stir_gt30_unweighted_pct": rec_one["stir"]["pct_above_30_unweighted"],
            "hardship_unweighted_pct": rec_one["hardship"]["rate_unweighted_pct"],
            "owner_hardship_unweighted_pct": rec_one["tenure"]["owner_hardship_unweighted_pct"],
            "renter_hardship_unweighted_pct": rec_one["tenure"]["renter_hardship_unweighted_pct"],
        }
        size_tab = (
            hh.assign(
                size=hh["n_persons"].clip(upper=6).astype(int),
                has_shelter=hh["shelter_m"].notna(),
            )
            .groupby("size")
            .agg(n_hh=("size", "size"), n_with_shelter=("has_shelter", "sum"))
        )
        size_tab["pct_with_shelter"] = 100 * size_tab["n_with_shelter"] / size_tab["n_hh"]
        rec["shelter_coverage_by_hh_size"] = {
            str(int(i)): {
                "households": int(r.n_hh),
                "with_shelter": int(r.n_with_shelter),
                "pct": float(r.pct_with_shelter),
            }
            for i, r in size_tab.iterrows()
        }
        print(
            f"  HH {rec['households_in_file']:,} valid {rec['households_valid']:,} "
            f"({rec['retention_pct_of_households']:.1f}%) "
            f"med inc ${rec['income_at_2021']['median_unweighted']:,.0f} "
            f"med shel ${rec['shelter_m_2021']['median_unweighted']:,.0f} "
            f"hardship {rec['hardship']['rate_unweighted_pct']:.1f}% "
            f"| 1-person valid {rec['one_person_households']['households_valid']:,} "
            f"({rec['one_person_households']['retention_pct_of_one_person_hh']:.1f}%) "
            f"hardship {rec['one_person_households']['hardship_unweighted_pct']:.1f}%"
        )

    years = [r["year"] for r in results]
    idx = {r["year"]: r for r in results}
    findings = {}
    if 2006 in idx and 2021 in idx:
        findings["income_growth_2006_2021_pct"] = (
            idx[2021]["income_at_2021"]["median_unweighted"]
            / idx[2006]["income_at_2021"]["median_unweighted"]
            - 1
        ) * 100
        findings["shelter_growth_2006_2021_pct"] = (
            idx[2021]["shelter_m_2021"]["median_unweighted"]
            / idx[2006]["shelter_m_2021"]["median_unweighted"]
            - 1
        ) * 100
        findings["hardship_change_2006_2021_pp"] = (
            idx[2021]["hardship"]["rate_unweighted_pct"]
            - idx[2006]["hardship"]["rate_unweighted_pct"]
        )
        findings["one_person_income_growth_2006_2021_pct"] = (
            idx[2021]["one_person_households"]["median_income_2021"]
            / idx[2006]["one_person_households"]["median_income_2021"]
            - 1
        ) * 100
        findings["one_person_shelter_growth_2006_2021_pct"] = (
            idx[2021]["one_person_households"]["median_shelter_2021"]
            / idx[2006]["one_person_households"]["median_shelter_2021"]
            - 1
        ) * 100
        findings["one_person_hardship_change_2006_2021_pp"] = (
            idx[2021]["one_person_households"]["hardship_unweighted_pct"]
            - idx[2006]["one_person_households"]["hardship_unweighted_pct"]
        )
        findings["all_hh_2006_not_comparable"] = (
            "2006 all-household medians are not comparable to later waves: "
            "GROSRT/OMP are confidentiality-suppressed (8888) for most multi-person households."
        )

    payload = {
        "analysis_date": datetime.now(timezone.utc).isoformat(),
        "pipeline": "audit/run_four_wave_repaired.py",
        "original_results_preserved_at": "audit/original/four_wave_temporal_results.json",
        "years_analyzed": years,
        "total_valid_households": sum(r["households_valid"] for r in results),
        "results_by_year": results,
        "drop_log": drop_logs,
        "key_findings_repaired": findings,
        "limitations": [
            "Household after-tax income is the sum of person TOTINC_AT; PUMF top-coding and rounding remain.",
            "MBM line is a single-adult national average, not household-size or region specific.",
            "2011 is the voluntary NHS, not a Census long-form; comparability is a documented break.",
            "WEIGHT is the person weight; household estimates use the first person weight in the household.",
            "CPI factors and MBM lines are those used in the original pipeline and still need official-table confirmation.",
            "2006 hierarchical PUMF suppresses GROSRT/OMP (code 8888) for most households with 2+ persons; the all-household 2006 series is composition-biased toward one-person households.",
            "A one-person-household restricted series is reported separately and is the only 2006–2021 comparison that does not mix suppressed and unsuppressed shelter.",
        ],
    }
    dest = OUT / "four_wave_repaired_results.json"
    dest.write_text(json.dumps(payload, indent=2))
    rows = []
    for r in results:
        rows.append(
            {
                "year": r["year"],
                "households_valid": r["households_valid"],
                "retention_pct_hh": round(r["retention_pct_of_households"], 1),
                "median_income_2021": round(r["income_at_2021"]["median_unweighted"]),
                "median_shelter_2021": round(r["shelter_m_2021"]["median_unweighted"]),
                "stir_gt30_pct": round(r["stir"]["pct_above_30_unweighted"], 1),
                "hardship_pct": round(r["hardship"]["rate_unweighted_pct"], 1),
                "owner_hardship_pct": None
                if r["tenure"]["owner_hardship_unweighted_pct"] is None
                else round(r["tenure"]["owner_hardship_unweighted_pct"], 1),
                "renter_hardship_pct": None
                if r["tenure"]["renter_hardship_unweighted_pct"] is None
                else round(r["tenure"]["renter_hardship_unweighted_pct"], 1),
                "one_person_valid": r["one_person_households"]["households_valid"],
                "one_person_retention_pct": round(
                    r["one_person_households"]["retention_pct_of_one_person_hh"], 1
                ),
                "one_person_median_income_2021": round(
                    r["one_person_households"]["median_income_2021"]
                ),
                "one_person_median_shelter_2021": round(
                    r["one_person_households"]["median_shelter_2021"]
                ),
                "one_person_hardship_pct": round(
                    r["one_person_households"]["hardship_unweighted_pct"], 1
                ),
            }
        )
    pd.DataFrame(rows).to_csv(OUT / "four_wave_repaired_summary.csv", index=False)
    print(f"\nWrote {dest}")
    print(f"Wrote {OUT / 'four_wave_repaired_summary.csv'}")


if __name__ == "__main__":
    main()
