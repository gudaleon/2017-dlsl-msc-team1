#!/usr/bin/env python3
"""Draft 4.0 — household reconstruction of Canadian housing hardship.

Uses original Statistics Canada hierarchical PUMFs and official MBM/CPI tables.
Does not overwrite Draft 3.0 outputs or the frozen original four-wave JSON.

This script does NOT produce official CMHC housing-hardship rates. It reconstructs
the CMHC residual-income concept as far as the supplied PUMFs allow and documents
every official step that cannot be implemented.

Primary estimand
----------------
Household residual income = sum of person TOTINC_AT (NA codes removed)
                            − 12 × monthly shelter.
Hardship if residual < non-shelter MBM of a reference family of four
                       × sqrt(household size) / 2.
Shelter is TENUR-conditioned GROSRT/OMP (2006, 2011) or SHELCO (2016, 2021).
One WEIGHT copy per household (primary maintainer). Dollars for the *rate*
are income-year current dollars against same-year MBM current dollars.
CPI (Table 18-10-0005) is used only to put medians in 2021 CAD.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from official_thresholds import (
    CMA_LABEL,
    INCOME_YEAR,
    PR_NAME,
    REGION2006_NAME,
    benchmarks,
    primary_thresholds,
    series_row,
)

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

INCOME_NA = {888888, 999999, 8888888, 9999999, 88888888, 99999999}
SHELTER_NA = {8888, 9999, 88888, 99999}

# Draft 3.0 leftover lines, retained only as a sensitivity / audit contrast.
DRAFT3_SINGLE_ADULT = {2006: 13500, 2011: 15000, 2016: 17000, 2021: 19728}
DRAFT3_CPI = {2006: 1.276, 2011: 1.148, 2016: 1.082, 2021: 1.000}

WAVES = {
    2006: {
        "path": ROOT / "data/raw/census_2006.csv",
        "identity": "2006 Census hierarchical PUMF (95M0029X)",
        "catalogue": "95M0029X",
        "instrument": "Census long form 2B",
        "shelter_mode": "grosrt_omp",
        "official_persons": 309841,
        "official_households": 124358,
    },
    2011: {
        "path": ROOT / "data/raw/census_2006_pumf.csv",
        "identity": "2011 NHS hierarchical PUMF (99M0002X)",
        "catalogue": "99M0002X",
        "instrument": "National Household Survey (voluntary)",
        "shelter_mode": "grosrt_omp",
        "official_persons": 333008,
        "official_households": 133192,
    },
    2016: {
        "path": ROOT / "data/raw/census_2011_nhs.csv",
        "identity": "2016 Census hierarchical PUMF (98M0002X)",
        "catalogue": "98M0002X",
        "instrument": "Census 2A-L",
        "shelter_mode": "shelco",
        "official_persons": 343330,
        "official_households": 140720,
    },
    2021: {
        "path": ROOT / "data/raw/census_2021_full.csv",
        "identity": "2021 Census hierarchical PUMF (98M0002X)",
        "catalogue": "98M0002X",
        "instrument": "Census 2A-L",
        "shelter_mode": "shelco",
        "official_persons": 361915,
        "official_households": 149789,
    },
}

COMMON_COLS = [
    "HH_ID",
    "PP_ID",
    "TOTINC",
    "TOTINC_AT",
    "TENUR",
    "WEIGHT",
    "PRIHM",
    "HHMAINP",
    "GROSRT",
    "OMP",
    "SHELCO",
    "PR",
    "CMA",
    "REGION",
    "REGIND",
    "HCORENEED_IND",
    "STIR_GRP",
    "LOMBM",
    "LOMBM_2018",
    "EFDIMBM",
    "EFDIMBM_2018",
]


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
        return valid_shelter(df["SHELCO"])
    grosrt = valid_shelter(df["GROSRT"]) if "GROSRT" in df.columns else pd.Series(np.nan, index=df.index)
    omp = valid_shelter(df["OMP"]) if "OMP" in df.columns else pd.Series(np.nan, index=df.index)
    tenur = _num(df["TENUR"]) if "TENUR" in df.columns else pd.Series(np.nan, index=df.index)
    out = pd.Series(np.nan, index=df.index)
    out = out.mask(tenur == 1, omp)
    out = out.mask(tenur == 2, grosrt)
    only_g = grosrt.notna() & omp.isna()
    only_o = omp.notna() & grosrt.isna()
    out = out.fillna(grosrt.where(only_g))
    out = out.fillna(omp.where(only_o))
    return out


def load_wave(year: int) -> pd.DataFrame:
    spec = WAVES[year]
    hdr = pd.read_csv(spec["path"], nrows=0).columns.tolist()
    usecols = [c for c in COMMON_COLS if c in hdr]
    usecols += [c for c in hdr if c.startswith("WT") and c[2:].isdigit()]
    df = pd.read_csv(spec["path"], usecols=usecols, low_memory=False)
    if len(df) != spec["official_persons"]:
        raise RuntimeError(f"{year}: expected {spec['official_persons']} person rows, got {len(df)}")
    return df


def householdize(df: pd.DataFrame, year: int) -> pd.DataFrame:
    spec = WAVES[year]
    d = df.copy()
    d["inc_at"] = valid_income(d["TOTINC_AT"])
    d["inc_bt"] = valid_income(d["TOTINC"]) if "TOTINC" in d.columns else np.nan
    d["shelter_m"] = person_shelter(d, spec["shelter_mode"])
    d["weight"] = _num(d["WEIGHT"])
    d["tenur"] = _num(d["TENUR"])
    d["prihm"] = _num(d["PRIHM"]) if "PRIHM" in d.columns else np.nan
    d["pr"] = _num(d["PR"]) if "PR" in d.columns else np.nan
    d["cma"] = _num(d["CMA"]) if "CMA" in d.columns else np.nan
    d["region"] = _num(d["REGION"]) if "REGION" in d.columns else np.nan
    d["regind"] = _num(d["REGIND"]) if "REGIND" in d.columns else np.nan
    for flag, dest in (
        ("HCORENEED_IND", "hcoreneed"),
        ("STIR_GRP", "stir_grp"),
        ("LOMBM", "lombm"),
        ("LOMBM_2018", "lombm_2018"),
    ):
        d[dest] = _num(d[flag]) if flag in d.columns else np.nan

    wt_cols = [c for c in d.columns if c.startswith("WT") and c[2:].isdigit()]
    pri = d[d["prihm"] == 1].copy()
    if pri["HH_ID"].nunique() != d["HH_ID"].nunique():
        raise RuntimeError(f"{year}: PRIHM==1 is not one-per-household")

    g = d.groupby("HH_ID", sort=False)
    hh = pd.DataFrame(
        {
            "n_persons": g.size(),
            "hh_income_at": g["inc_at"].sum(min_count=1),
            "n_income_at": g["inc_at"].count(),
            "hh_income_bt": g["inc_bt"].sum(min_count=1),
            "n_income_bt": g["inc_bt"].count(),
        }
    )
    pri = pri.set_index("HH_ID")
    hh["shelter_m"] = pri["shelter_m"]
    hh["tenur"] = pri["tenur"]
    hh["weight"] = pri["weight"]
    hh["pr"] = pri["pr"]
    hh["cma"] = pri["cma"]
    hh["region"] = pri["region"]
    hh["regind"] = pri["regind"]
    hh["hcoreneed"] = pri["hcoreneed"]
    hh["stir_grp"] = pri["stir_grp"]
    hh["lombm"] = pri["lombm"]
    hh["lombm_2018"] = pri["lombm_2018"]
    for c in wt_cols:
        hh[c] = _num(pri[c])

    # Housing variables are household concepts copied onto every person row.
    # If the maintainer row is suppressed, no other person recovers the amount.
    hh["shelter_any"] = g["shelter_m"].median()
    hh["year"] = year
    hh["is_owner"] = hh["tenur"] == 1
    hh["is_renter"] = hh["tenur"] == 2
    hh["tenure_ok"] = hh["is_owner"] | hh["is_renter"]
    hh["income_ok"] = hh["hh_income_at"].notna() & (hh["hh_income_at"] > 0) & (hh["n_income_at"] > 0)
    hh["shelter_ok"] = hh["shelter_m"].notna()
    hh["analytic"] = hh["tenure_ok"] & hh["income_ok"] & hh["shelter_ok"]
    return hh


def attach_thresholds(hh: pd.DataFrame, year: int) -> pd.DataFrame:
    th = primary_thresholds(year)
    hh = hh.copy()
    n = hh["n_persons"].clip(lower=1)
    equiv = np.sqrt(n) / 2.0
    ns_nat = th["ref_family_nonshelter"]
    full_nat = th["ref_family_total"]
    hh["mbm_ns_national_size"] = ns_nat * equiv
    hh["mbm_full_national_size"] = full_nat * equiv
    hh["mbm_ns_single_adult"] = th["single_adult_nonshelter"]
    hh["mbm_full_single_adult"] = th["single_adult_full_mbm"]
    hh["mbm_draft3_single"] = DRAFT3_SINGLE_ADULT[year]

    # Geography-sensitive non-shelter MBM (still not the official 50-region assignment).
    cma_map = th["selected_cma_nonshelter"]
    prov_map = th["by_province_nonshelter"]
    geo = np.full(len(hh), ns_nat, dtype=float)
    cma_int = pd.to_numeric(hh["cma"], errors="coerce").round().astype("Int64")
    pr_int = pd.to_numeric(hh["pr"], errors="coerce").round().astype("Int64")
    if cma_int.notna().any():
        labels = cma_int.map(CMA_LABEL)
        for lab, val in cma_map.items():
            geo = np.where(labels == lab, val, geo)
    if pr_int.notna().any():
        names = pr_int.map(PR_NAME)
        # Use provincial mean only when CMA is the residual 999 / unmapped.
        use_pr = cma_int.fillna(999).isin([999]) | cma_int.isna()
        for name, val in prov_map.items():
            geo = np.where(use_pr.to_numpy() & (names == name).to_numpy(), val, geo)
        terr = [prov_map[k] for k in ("Yukon", "Northwest Territories", "Nunavut") if k in prov_map]
        if terr:
            geo = np.where(
                use_pr.to_numpy() & names.eq("Territories").to_numpy(),
                float(np.mean(terr)),
                geo,
            )
    hh["mbm_ns_geo_size"] = geo * equiv

    cpi = th["cpi_income_year_to_2021"]
    hh["cpi_official"] = cpi
    hh["income_at_2021"] = hh["hh_income_at"] * cpi
    hh["income_bt_2021"] = hh["hh_income_bt"] * cpi
    hh["shelter_m_2021"] = hh["shelter_m"] * cpi
    hh["annual_shelter"] = hh["shelter_m"] * 12
    hh["annual_shelter_2021"] = hh["shelter_m_2021"] * 12
    hh["residual"] = hh["hh_income_at"] - hh["annual_shelter"]
    hh["residual_2021"] = hh["income_at_2021"] - hh["annual_shelter_2021"]
    hh["stir_at"] = hh["annual_shelter"] / hh["hh_income_at"].clip(lower=1)
    hh["stir_bt"] = hh["annual_shelter"] / hh["hh_income_bt"].clip(lower=1)

    hh["hard_ns_size"] = (hh["residual"] < hh["mbm_ns_national_size"]).astype(float)
    hh["hard_ns_geo"] = (hh["residual"] < hh["mbm_ns_geo_size"]).astype(float)
    hh["hard_full_size"] = (hh["residual"] < hh["mbm_full_national_size"]).astype(float)
    hh["hard_ns_single"] = (hh["residual"] < hh["mbm_ns_single_adult"]).astype(float)
    hh["hard_draft3"] = (hh["residual_2021"] < hh["mbm_draft3_single"]).astype(float)
    # CMHC-style extra restriction: equivalized income above median cannot be hardship.
    hh["equiv_inc"] = hh["hh_income_at"] / np.sqrt(n)
    return hh, th


def wmean(s: pd.Series, w: pd.Series) -> float:
    d = pd.DataFrame({"s": s, "w": w}).dropna()
    d = d[d["w"] > 0]
    if d.empty or d["w"].sum() <= 0:
        return float("nan")
    return float(np.average(d["s"], weights=d["w"]))


def wmedian(s: pd.Series, w: pd.Series) -> float:
    d = pd.DataFrame({"s": s, "w": w}).dropna()
    d = d[d["w"] > 0].sort_values("s")
    if d.empty:
        return float("nan")
    cdf = d["w"].cumsum()
    return float(d.loc[cdf >= d["w"].sum() / 2.0, "s"].iloc[0])


def replicate_se(d: pd.DataFrame, col: str) -> dict | None:
    wt = [c for c in d.columns if c.startswith("WT") and c[2:].isdigit()]
    if not wt:
        return None
    point = wmean(d[col], d["weight"])
    reps = []
    for c in wt:
        reps.append(wmean(d[col], d[c]))
    reps = np.array(reps, dtype=float)
    reps = reps[np.isfinite(reps)]
    if len(reps) < 2 or not math.isfinite(point):
        return None
    # Bootstrap-style variance used as an approximation; PUMF user-guide constant not on disk.
    var = float(np.mean((reps - point) ** 2))
    return {
        "point": point,
        "se": math.sqrt(var),
        "n_replicates": int(len(reps)),
        "method": "bootstrap mean of squared deviations from the full-weight estimate; formula not confirmed against a year-specific PUMF user guide",
    }


def _rate_block(d: pd.DataFrame, col: str) -> dict:
    w = d["weight"]
    return {
        "n": int(len(d)),
        "n_flagged": int(d[col].sum()),
        "unweighted_pct": float(d[col].mean() * 100) if len(d) else float("nan"),
        "weighted_pct": wmean(d[col], w) * 100 if len(d) else float("nan"),
        "weighted_population": float(w.sum()) if len(d) else 0.0,
        "weighted_flagged": float((d[col] * w).sum()) if len(d) else 0.0,
        "replicate": replicate_se(d, col),
    }


def summarize_subset(d: pd.DataFrame, label: str) -> dict:
    if d.empty:
        return {"label": label, "n": 0}
    w = d["weight"]
    out = {
        "label": label,
        "sample_households": int(len(d)),
        "estimated_households": float(w.sum()),
        "mean_hh_size": float(d["n_persons"].mean()),
        "weighted_mean_hh_size": wmean(d["n_persons"], w),
        "median_income_at_current": wmedian(d["hh_income_at"], w),
        "median_income_at_2021": wmedian(d["income_at_2021"], w),
        "median_income_at_unweighted_current": float(d["hh_income_at"].median()),
        "median_shelter_current": wmedian(d["shelter_m"], w),
        "median_shelter_2021": wmedian(d["shelter_m_2021"], w),
        "median_residual_current": wmedian(d["residual"], w),
        "stir_at_gt30": {
            "unweighted_pct": float((d["stir_at"] > 0.30).mean() * 100),
            "weighted_pct": wmean((d["stir_at"] > 0.30).astype(float), w) * 100,
        },
        "stir_bt_gt30_lt100": {
            "unweighted_pct": float(((d["stir_bt"] >= 0.30) & (d["stir_bt"] < 1.0)).mean() * 100),
            "weighted_pct": wmean(((d["stir_bt"] >= 0.30) & (d["stir_bt"] < 1.0)).astype(float), w) * 100,
        },
        "stir_at_gt50": {
            "weighted_pct": wmean((d["stir_at"] > 0.50).astype(float), w) * 100,
        },
        "hardship_nonshelter_size_national": _rate_block(d, "hard_ns_size"),
        "hardship_nonshelter_size_geo": _rate_block(d, "hard_ns_geo"),
        "hardship_full_mbm_size_national": _rate_block(d, "hard_full_size"),
        "hardship_nonshelter_single_adult": _rate_block(d, "hard_ns_single"),
        "hardship_draft3_leftover": _rate_block(d, "hard_draft3"),
    }
    return out


def sample_flow(hh: pd.DataFrame, n_persons: int) -> dict:
    def n_w(mask: pd.Series) -> dict:
        return {"sample": int(mask.sum()), "weighted": float(hh.loc[mask, "weight"].sum())}

    return {
        "person_records_in_file": n_persons,
        "households_in_file": int(len(hh)),
        "weighted_households_in_file": float(hh["weight"].sum()),
        "drop_tenure_not_owner_renter": n_w(~hh["tenure_ok"]),
        "drop_missing_or_nonpositive_aftertax_income": n_w(~hh["income_ok"]),
        "drop_missing_shelter": n_w(~hh["shelter_ok"]),
        "analytic_households": n_w(hh["analytic"]),
        "analytic_owners": n_w(hh["analytic"] & hh["is_owner"]),
        "analytic_renters": n_w(hh["analytic"] & hh["is_renter"]),
        "analytic_one_person": n_w(hh["analytic"] & (hh["n_persons"] == 1)),
        "analytic_two_plus": n_w(hh["analytic"] & (hh["n_persons"] >= 2)),
        "negative_residual_inside_analytic": n_w(hh["analytic"] & (hh["residual"] < 0)),
        "retention_pct_of_households": float(hh["analytic"].mean() * 100),
    }


def published_flags(d: pd.DataFrame) -> dict:
    out = {}
    if d["hcoreneed"].notna().any():
        # 2021: 100 = in core need, 0 = not, 888 = not applicable
        univ = d[d["hcoreneed"].isin([0, 100, 0.0, 100.0])]
        if len(univ):
            flag = (univ["hcoreneed"] == 100).astype(float)
            out["hcoreneed_ind"] = {
                "universe_sample": int(len(univ)),
                "weighted_pct": wmean(flag, univ["weight"]) * 100,
                "unweighted_pct": float(flag.mean() * 100),
                "codes": "100 = in core housing need; 0 = not; 888 excluded as not applicable",
            }
    if d["stir_grp"].notna().any():
        univ = d[d["stir_grp"].isin([0, 1])]
        if len(univ):
            flag = (univ["stir_grp"] == 1).astype(float)
            out["stir_grp"] = {
                "universe_sample": int(len(univ)),
                "weighted_pct": wmean(flag, univ["weight"]) * 100,
                "unweighted_pct": float(flag.mean() * 100),
                "codes": "interpreted as 1 = STIR group indicating 30%+; 9 excluded; confirm against 2021 codebook",
            }
    if d["lombm"].notna().any():
        univ = d[d["lombm"].isin([1, 2])]
        if len(univ):
            # 2011/2016: 2 is the smaller class and matches a low-income prevalence.
            flag = (univ["lombm"] == 2).astype(float)
            out["lombm"] = {
                "universe_sample": int(len(univ)),
                "weighted_pct_code2": wmean(flag, univ["weight"]) * 100,
                "codes": "1/2/8/9 present; code 2 treated as below-MBM on the economic-family flag — UNCERTAIN without the NHS/2016 codebook page",
            }
    if d["lombm_2018"].notna().any():
        univ = d[d["lombm_2018"].isin([0, 1])]
        if len(univ):
            flag = (univ["lombm_2018"] == 1).astype(float)
            out["lombm_2018"] = {
                "universe_sample": int(len(univ)),
                "weighted_pct": wmean(flag, univ["weight"]) * 100,
                "codes": "1 = below 2018-base MBM (economic family); 0 = not; 8 excluded",
            }
    return out


def validate_wave(year: int, analytic: pd.DataFrame, flow: dict, summary: dict) -> list[dict]:
    b = benchmarks()
    rows = []
    iy = str(INCOME_YEAR[year])
    cpi = analytic["cpi_official"].iloc[0] if len(analytic) else float("nan")
    cpi2020 = 137.0
    # 1. Weighted household count vs published private households (file total, not analytic).
    pub_hh = b["private_households"]["values"].get(str(year))
    if pub_hh:
        est = flow["weighted_households_in_file"]
        rows.append(
            {
                "check": "weighted_private_households_in_file",
                "year": year,
                "estimate": est,
                "published": pub_hh,
                "abs_diff": est - pub_hh,
                "pct_diff": 100 * (est / pub_hh - 1) if pub_hh else None,
                "note": "PUMF WEIGHT × household count should recover the private-household universe of the parent file, not the analytic residual-income subset.",
            }
        )
    # 2. Median after-tax income in 2020 constant dollars.
    pub_med = b["median_after_tax_household_income_2020_constant_cad"]["values"].get(iy)
    if pub_med and len(analytic):
        # hh_income_at is current income-year dollars. 2020-constant = current × (137 / CPI_income_year).
        cpi_iy = 141.6 / cpi
        est_2020 = wmedian(analytic["hh_income_at"] * (cpi2020 / cpi_iy), analytic["weight"])
        rows.append(
            {
                "check": "median_after_tax_income_2020_constant",
                "year": year,
                "estimate": est_2020,
                "published": pub_med,
                "abs_diff": est_2020 - pub_med,
                "pct_diff": 100 * (est_2020 / pub_med - 1),
                "note": "PUMF is a 1% hierarchical sample with top-coding. 2006 analytic sample is one-person-heavy because of shelter suppression.",
            }
        )
    # 3. Before-tax STIR >= 30% and < 100%.
    una = b["unaffordable_housing_stir_ge_30_percent"]["values"].get(str(year))
    if una:
        rows.append(
            {
                "check": "stir_bt_ge30_lt100",
                "year": year,
                "estimate": summary["all_analytic"]["stir_bt_gt30_lt100"]["weighted_pct"],
                "published": una["all"],
                "abs_diff": summary["all_analytic"]["stir_bt_gt30_lt100"]["weighted_pct"] - una["all"],
                "note": "Official unaffordable-housing rate uses a non-farm non-reserve STIR<100% universe. PUMF cannot fully implement farm/reserve exclusions.",
            }
        )
    # 4. Published core housing need vs PUMF HCORENEED_IND (2021).
    chn = b["core_housing_need"]["values"].get(str(year), {})
    flags = summary.get("published_flags", {})
    if "hcoreneed_ind" in flags and "all" in chn:
        rows.append(
            {
                "check": "hcoreneed_ind_vs_published_core_need",
                "year": year,
                "estimate": flags["hcoreneed_ind"]["weighted_pct"],
                "published": chn["all"],
                "abs_diff": flags["hcoreneed_ind"]["weighted_pct"] - chn["all"],
                "note": "Same concept family, but PUMF flag universe and rounding differ from the official 2A-L tabulation.",
            }
        )
    # 5. CMHC CIS housing hardship ~9% in 2017 — not a same-year, same-source benchmark.
    if year == 2016:
        rows.append(
            {
                "check": "cmhc_cis_housing_hardship_2017_context",
                "year": year,
                "estimate": summary["all_analytic"]["hardship_nonshelter_size_national"]["weighted_pct"],
                "published": 9.0,
                "note": "CMHC 9% is CIS 2017 with MBM disposable income, high-income exclusion, and negative-residual drop. A large gap is expected and is not evidence that the PUMF files are wrong.",
            }
        )
    return rows


def sensitivity_table(analytic: pd.DataFrame, year: int) -> list[dict]:
    rows = []
    d = analytic
    w = d["weight"]
    base = wmean(d["hard_ns_size"], w) * 100
    variants = [
        ("primary_nonshelter_size_national_weighted", d["hard_ns_size"], d),
        ("nonshelter_size_geo_weighted", d["hard_ns_geo"], d),
        ("full_mbm_size_national_weighted", d["hard_full_size"], d),
        ("nonshelter_single_adult_weighted", d["hard_ns_single"], d),
        ("draft3_leftover_weighted", d["hard_draft3"], d),
        ("primary_unweighted", d["hard_ns_size"], d),
    ]
    # Exclude negative residual from the universe (CMHC).
    pos = d[d["residual"] >= 0]
    variants.append(("primary_drop_negative_residual", pos["hard_ns_size"], pos))
    # High-income exclusion: equivalized income above median cannot be hardship.
    med = wmedian(d["equiv_inc"], w)
    capped = d.copy()
    capped["hard_cap"] = np.where(capped["equiv_inc"] > med, 0.0, capped["hard_ns_size"])
    variants.append(("primary_plus_high_income_exclusion", capped["hard_cap"], capped))
    # One-person only.
    one = d[d["n_persons"] == 1]
    variants.append(("one_person_primary", one["hard_ns_size"], one))
    # Owners / renters
    variants.append(("owners_primary", d.loc[d["is_owner"], "hard_ns_size"], d[d["is_owner"]]))
    variants.append(("renters_primary", d.loc[d["is_renter"], "hard_ns_size"], d[d["is_renter"]]))

    for name, series, frame in variants:
        if frame.empty:
            continue
        ww = pd.Series(1.0, index=frame.index) if name == "primary_unweighted" else frame["weight"]
        rate = wmean(series, ww) * 100
        rows.append(
            {
                "year": year,
                "variant": name,
                "sample_households": int(len(frame)),
                "estimated_households": float(frame["weight"].sum()),
                "hardship_pct": rate,
                "pp_vs_primary": rate - base,
            }
        )
    return rows


def main() -> None:
    results = []
    flows = []
    validations = []
    sensitivities = []
    coverage_rows = []
    print("Draft 4.0 household reconstruction")
    for year, spec in WAVES.items():
        print(f"\n=== {year} ← {spec['path'].name} :: {spec['identity']} ===")
        persons = load_wave(year)
        hh = householdize(persons, year)
        hh, th = attach_thresholds(hh, year)
        analytic = hh.loc[hh["analytic"]].copy()
        flow = sample_flow(hh, len(persons))
        flow["year"] = year
        flow["file_identity"] = spec["identity"]
        flow["local_path"] = str(spec["path"].relative_to(ROOT))
        flows.append(flow)

        size_tab = (
            hh.assign(size=hh["n_persons"].clip(upper=6).astype(int))
            .groupby("size")
            .agg(n_hh=("size", "size"), n_shelter=("shelter_ok", "sum"), n_analytic=("analytic", "sum"))
        )
        size_tab["pct_shelter"] = 100 * size_tab["n_shelter"] / size_tab["n_hh"]
        coverage = {
            str(int(i)): {
                "households": int(r.n_hh),
                "with_shelter": int(r.n_shelter),
                "analytic": int(r.n_analytic),
                "pct_with_shelter": float(r.pct_shelter),
            }
            for i, r in size_tab.iterrows()
        }
        for size, rec in coverage.items():
            coverage_rows.append({"year": year, "hh_size": size, **rec})

        summary = {
            "year": year,
            "file_identity": spec["identity"],
            "catalogue": spec["catalogue"],
            "instrument": spec["instrument"],
            "income_year": INCOME_YEAR[year],
            "shelter_mode": spec["shelter_mode"],
            "thresholds": {
                k: th[k]
                for k in (
                    "mbm_base",
                    "n_regions",
                    "ref_family_total",
                    "ref_family_shelter",
                    "ref_family_nonshelter",
                    "single_adult_full_mbm",
                    "single_adult_nonshelter",
                    "cpi_income_year_to_2021",
                    "note",
                )
            },
            "all_analytic": summarize_subset(analytic, "all_analytic"),
            "owners": summarize_subset(analytic[analytic["is_owner"]], "owners"),
            "renters": summarize_subset(analytic[analytic["is_renter"]], "renters"),
            "one_person": summarize_subset(analytic[analytic["n_persons"] == 1], "one_person"),
            "two_plus": summarize_subset(analytic[analytic["n_persons"] >= 2], "two_plus"),
            "cmhc_universe_drop_neg_residual": summarize_subset(
                analytic[analytic["residual"] >= 0], "drop_neg_residual"
            ),
            "published_flags": published_flags(analytic),
            "shelter_coverage_by_hh_size": coverage,
        }
        results.append(summary)
        validations.extend(validate_wave(year, analytic, flow, summary))
        sensitivities.extend(sensitivity_table(analytic, year))

        h = summary["all_analytic"]["hardship_nonshelter_size_national"]
        print(
            f"  HH file {flow['households_in_file']:,}  analytic {flow['analytic_households']['sample']:,} "
            f"({flow['retention_pct_of_households']:.1f}%)  "
            f"N̂={flow['analytic_households']['weighted']:,.0f}  "
            f"med inc ${summary['all_analytic']['median_income_at_current']:,.0f}  "
            f"med shel ${summary['all_analytic']['median_shelter_current']:,.0f}  "
            f"hardship {h['weighted_pct']:.1f}% (unw {h['unweighted_pct']:.1f}%)  "
            f"1-person {summary['one_person']['hardship_nonshelter_size_national']['weighted_pct']:.1f}%"
        )

    payload = {
        "analysis_date": datetime.now(timezone.utc).isoformat(),
        "draft": "4.0",
        "pipeline": "papers/paper1_draft4/reconstruct_four_wave.py",
        "original_results_preserved_at": [
            "results/four_wave_temporal_results.json",
            "audit/original/four_wave_temporal_results.json",
            "papers/paper1_highschool/ (Draft 3.0 frozen)",
        ],
        "primary_estimand": (
            "Household residual income (sum of person TOTINC_AT − 12×monthly shelter) "
            "compared with the non-shelter MBM of a four-person reference family "
            "scaled by sqrt(n)/2, national unweighted mean of Table 11-10-0066 regions, "
            "contemporaneous official MBM base, income-year current dollars. "
            "NOT an official CMHC housing-hardship rate."
        ),
        "results_by_year": results,
        "sample_flow": flows,
        "validation": validations,
        "sensitivity": sensitivities,
        "unresolved": [
            "PUMF geography is not the official 50-region MBM geography. National means are used as the primary threshold; CMA/PR assignment is a documented approximation.",
            "Census TOTINC_AT is after-tax income, not MBM disposable income (which also deducts EI/CPP/union/childcare/support/health premiums and applies a mortgage-free homeowner adjustment).",
            "Farm, band and reserve households cannot be fully excluded with the variables retained on these PUMFs (TENUR==8 is dropped; REGIND is not a reserve-housing flag).",
            "2011 TENUR==2 combines renters and band housing.",
            "2006 GROSRT/OMP code 8888 suppresses shelter for most multi-person households; the 2006 all-household series is not comparable.",
            "2006 has no PR; REGION 1–6 provincial grouping is inferred from household shares (UNCERTAIN).",
            "Replicate-weight variance uses a generic bootstrap formula; year-specific PUMF user-guide constants were not on disk.",
            "CMHC high-income, investment-income and negative-residual universe rules are implemented only as sensitivity variants.",
            "2018-base MBM is the official poverty line from 2018; 2005 uses 2000-base and 2010/2015 use 2008-base. Base-year changes are a real series break.",
            "The 2024 CMHC Census housing-hardship update (NH18-33/85-2024) was not recovered; CIS 2017 ~9% is the available official hardship benchmark.",
            "2001 after-tax residual series remains not feasible (TOTINCH is before-tax only).",
        ],
    }
    dest = OUT / "draft4_reconstruction.json"
    dest.write_text(json.dumps(payload, indent=2, default=str))

    flow_rows = []
    for f in flows:
        flow_rows.append(
            {
                "year": f["year"],
                "file_identity": f["file_identity"],
                "person_records": f["person_records_in_file"],
                "households_in_file": f["households_in_file"],
                "drop_tenure": f["drop_tenure_not_owner_renter"]["sample"],
                "drop_income": f["drop_missing_or_nonpositive_aftertax_income"]["sample"],
                "drop_shelter": f["drop_missing_shelter"]["sample"],
                "analytic_n": f["analytic_households"]["sample"],
                "analytic_N": round(f["analytic_households"]["weighted"]),
                "retention_pct": round(f["retention_pct_of_households"], 1),
                "owners_n": f["analytic_owners"]["sample"],
                "renters_n": f["analytic_renters"]["sample"],
                "one_person_n": f["analytic_one_person"]["sample"],
            }
        )
    pd.DataFrame(flow_rows).to_csv(OUT / "sample_flow.csv", index=False)
    pd.DataFrame(coverage_rows).to_csv(OUT / "shelter_coverage_by_size.csv", index=False)
    pd.DataFrame(validations).to_csv(OUT / "validation.csv", index=False)
    pd.DataFrame(sensitivities).to_csv(OUT / "sensitivity.csv", index=False)

    summary_rows = []
    for r in results:
        a = r["all_analytic"]
        h = a["hardship_nonshelter_size_national"]
        summary_rows.append(
            {
                "year": r["year"],
                "instrument": r["instrument"],
                "income_year": r["income_year"],
                "mbm_base": r["thresholds"]["mbm_base"],
                "sample_households": a["sample_households"],
                "estimated_households": round(a["estimated_households"]),
                "median_income_current": round(a["median_income_at_current"]),
                "median_income_2021": round(a["median_income_at_2021"]),
                "median_shelter_current": round(a["median_shelter_current"]),
                "median_shelter_2021": round(a["median_shelter_2021"]),
                "stir_at_gt30_w": round(a["stir_at_gt30"]["weighted_pct"], 1),
                "stir_bt_gt30_lt100_w": round(a["stir_bt_gt30_lt100"]["weighted_pct"], 1),
                "hardship_ns_size_w": round(h["weighted_pct"], 1),
                "hardship_ns_size_uw": round(h["unweighted_pct"], 1),
                "hardship_ns_size_se": (
                    None if h["replicate"] is None else round(h["replicate"]["se"] * 100, 2)
                ),
                "owner_hardship_w": round(
                    r["owners"]["hardship_nonshelter_size_national"]["weighted_pct"], 1
                ),
                "renter_hardship_w": round(
                    r["renters"]["hardship_nonshelter_size_national"]["weighted_pct"], 1
                ),
                "one_person_hardship_w": round(
                    r["one_person"]["hardship_nonshelter_size_national"]["weighted_pct"], 1
                ),
                "full_mbm_hardship_w": round(
                    a["hardship_full_mbm_size_national"]["weighted_pct"], 1
                ),
            }
        )
    pd.DataFrame(summary_rows).to_csv(OUT / "primary_estimates.csv", index=False)
    print(f"\nWrote {dest}")
    print(f"Wrote {OUT / 'sample_flow.csv'}")
    print(f"Wrote {OUT / 'primary_estimates.csv'}")
    print(f"Wrote {OUT / 'validation.csv'}")
    print(f"Wrote {OUT / 'sensitivity.csv'}")


if __name__ == "__main__":
    main()
