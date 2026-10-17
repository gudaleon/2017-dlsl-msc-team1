#!/usr/bin/env python3
"""Draft 5.0 Stage 1 — scientific verification.

Reproduces the frozen Draft 4.0 household pipeline without modifying it,
then measures distance-to-CMHC variants, codebook checks, 2016–2021
MBM/COVID/composition analyses, and independent validation.

This script does not write official CMHC housing-hardship rates.
It does not overwrite papers/paper1_draft4/ or papers/paper1_highschool/.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D4 = HERE.parent / "paper1_draft4"
OUT = HERE / "outputs"
LOG = HERE / "logs"
OFF = HERE / "official"
OUT.mkdir(parents=True, exist_ok=True)
LOG.mkdir(parents=True, exist_ok=True)
OFF.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(D4))
import reconstruct_four_wave as d4  # noqa: E402
from official_thresholds import (  # noqa: E402
    CMA_LABEL,
    INCOME_YEAR,
    PR_NAME,
    PRIMARY_BASE,
    benchmarks,
    series_row,
)

EXTRA_COLS = ["EF_ID", "EFCOVID_ERB", "EFDIMBM", "EFDIMBM_2018", "EF_RP"]
ERB_NA = {88888888, 99999999, 8888888, 9999999, 888888, 999999}
LOCKED_D4 = {
    2011: {"n": 130242, "N": 13019080, "hardship": 18.2},
    2016: {"n": 139869, "N": 14037793, "hardship": 17.3},
    2021: {"n": 148085, "N": 14863013, "hardship": 14.9},
}
PUMF_PATHS = {
    2006: ROOT / "data/raw/census_2006.csv",
    2011: ROOT / "data/raw/census_2006_pumf.csv",
    2016: ROOT / "data/raw/census_2011_nhs.csv",
    2021: ROOT / "data/raw/census_2021_full.csv",
    "dup_2006": ROOT / "data/raw/census_2016_pumf.csv",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def wmean(s: pd.Series, w: pd.Series) -> float:
    return d4.wmean(s, w)


def wmedian(s: pd.Series, w: pd.Series) -> float:
    return d4.wmedian(s, w)


def load_wave_extended(year: int) -> pd.DataFrame:
    spec = d4.WAVES[year]
    hdr = pd.read_csv(spec["path"], nrows=0).columns.tolist()
    usecols = [c for c in d4.COMMON_COLS if c in hdr]
    usecols += [c for c in EXTRA_COLS if c in hdr]
    usecols += [c for c in hdr if c.startswith("WT") and c[2:].isdigit()]
    usecols = list(dict.fromkeys(usecols))
    df = pd.read_csv(spec["path"], usecols=usecols, low_memory=False)
    if len(df) != spec["official_persons"]:
        raise RuntimeError(f"{year}: expected {spec['official_persons']} person rows, got {len(df)}")
    return df


def attach_family_fields(persons: pd.DataFrame, hh: pd.DataFrame) -> pd.DataFrame:
    hh = hh.copy()
    g = persons.groupby("HH_ID", sort=False)
    if "EF_ID" in persons.columns:
        hh["n_ef"] = g["EF_ID"].nunique()
    else:
        hh["n_ef"] = np.nan

    if "EFCOVID_ERB" in persons.columns:
        erb = pd.to_numeric(persons["EFCOVID_ERB"], errors="coerce")
        erb = erb.where(~erb.isin(ERB_NA))
        tmp = persons.assign(_erb=erb)
        ef = (
            tmp.groupby(["HH_ID", "EF_ID"], sort=False)["_erb"]
            .first()
            .reset_index()
        )
        hh["hh_erb"] = ef.groupby("HH_ID")["_erb"].sum(min_count=1)
    else:
        hh["hh_erb"] = np.nan

    for src, dest in (("EFDIMBM", "efdimbm_any"), ("EFDIMBM_2018", "efdimbm_2018_any")):
        if src in persons.columns:
            x = pd.to_numeric(persons[src], errors="coerce")
            x = x.where(~x.isin(ERB_NA))
            hh[dest] = persons.assign(_x=x).groupby("HH_ID")["_x"].first()
        else:
            hh[dest] = np.nan
    return hh


def geo_threshold_from_row(hh: pd.DataFrame, row: dict) -> np.ndarray:
    ns_nat = row["national_unweighted_mean"]["nonshelter"]
    cma_map = {k: v["nonshelter"] for k, v in row["selected_cma_nonshelter"].items()}
    prov_map = row["by_province_mean_nonshelter"]
    n = hh["n_persons"].clip(lower=1)
    equiv = np.sqrt(n) / 2.0
    geo = np.full(len(hh), ns_nat, dtype=float)
    cma_int = pd.to_numeric(hh["cma"], errors="coerce").round().astype("Int64")
    pr_int = pd.to_numeric(hh["pr"], errors="coerce").round().astype("Int64")
    if cma_int.notna().any():
        labels = cma_int.map(CMA_LABEL)
        for lab, val in cma_map.items():
            geo = np.where(labels == lab, val, geo)
    if pr_int.notna().any():
        names = pr_int.map(PR_NAME)
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
    return geo * equiv.to_numpy()


def provincial_median_equiv(d: pd.DataFrame) -> pd.Series:
    pr = pd.to_numeric(d["pr"], errors="coerce").round().astype("Int64")
    medians: dict[int, float] = {}
    for code, sub in d.groupby(pr, dropna=True):
        medians[int(code)] = wmedian(sub["equiv_inc"], sub["weight"])
    national = wmedian(d["equiv_inc"], d["weight"])
    mapped = pr.map(medians).astype(float)
    return mapped.fillna(national)


def apply_high_income_recode(hard: pd.Series, d: pd.DataFrame) -> pd.Series:
    cap = provincial_median_equiv(d)
    out = hard.astype(float).copy()
    out = out.mask(d["equiv_inc"] > cap, 0.0)
    return out


def random_group_se(d: pd.DataFrame, col: str) -> dict | None:
    """2006/2011 PUMF user-guide random-groups SE: sqrt(sum((r-rbar)^2)/56)."""
    wt = [c for c in d.columns if c.startswith("WT") and c[2:].isdigit()]
    if len(wt) != 8:
        return None
    reps = []
    for c in wt:
        reps.append(wmean(d[col], d[c]))
    reps = np.array(reps, dtype=float)
    reps = reps[np.isfinite(reps)]
    if len(reps) < 2:
        return None
    rbar = float(np.mean(reps))
    se = math.sqrt(float(np.sum((reps - rbar) ** 2)) / 56.0)
    return {
        "point": wmean(d[col], d["weight"]),
        "se": se,
        "n_replicates": int(len(reps)),
        "divisor": 56,
        "method": "2006/2011 hierarchical PUMF random-groups formula: sqrt(sum((r_i-rbar)^2)/56)",
        "source": "95M0029XVB / 99M0002X user guides",
    }


def rate_block(d: pd.DataFrame, hard: pd.Series) -> dict:
    w = d["weight"]
    return {
        "n": int(len(d)),
        "N": float(w.sum()) if len(d) else 0.0,
        "n_flagged": int(pd.Series(hard, index=d.index).sum()),
        "weighted_flagged": float((pd.Series(hard, index=d.index) * w).sum()) if len(d) else 0.0,
        "weighted_pct": wmean(pd.Series(hard, index=d.index), w) * 100 if len(d) else float("nan"),
        "unweighted_pct": float(pd.Series(hard, index=d.index).mean() * 100) if len(d) else float("nan"),
    }


def kitagawa(base: pd.DataFrame, end: pd.DataFrame, group: str) -> list[dict]:
    """Descriptive Kitagawa decomposition using 2016 shares/rates as the base."""
    rows = []
    b = base.copy()
    e = end.copy()
    b["_g"] = b[group]
    e["_g"] = e[group]
    b_tot = float(b["weight"].sum())
    e_tot = float(e["weight"].sum())
    groups = sorted(set(b["_g"].dropna().unique()) | set(e["_g"].dropna().unique()), key=str)
    r0 = {}
    s0 = {}
    r1 = {}
    s1 = {}
    for g in groups:
        db = b[b["_g"] == g]
        de = e[e["_g"] == g]
        s0[g] = float(db["weight"].sum()) / b_tot if b_tot else 0.0
        s1[g] = float(de["weight"].sum()) / e_tot if e_tot else 0.0
        r0[g] = wmean(db["hard_ns_size"], db["weight"]) if len(db) else float("nan")
        r1[g] = wmean(de["hard_ns_size"], de["weight"]) if len(de) else float("nan")
    comp = 0.0
    rate = 0.0
    for g in groups:
        if not (math.isfinite(r0[g]) and math.isfinite(r1[g])):
            continue
        comp += (s1[g] - s0[g]) * r0[g]
        rate += s1[g] * (r1[g] - r0[g])
        rows.append(
            {
                "grouping": group,
                "group": str(g),
                "share_2016": s0[g],
                "share_2021": s1[g],
                "rate_2016": r0[g] * 100,
                "rate_2021": r1[g] * 100,
                "composition_pp": (s1[g] - s0[g]) * r0[g] * 100,
                "rate_pp": s1[g] * (r1[g] - r0[g]) * 100,
            }
        )
    rows.append(
        {
            "grouping": group,
            "group": "TOTAL",
            "share_2016": 1.0,
            "share_2021": 1.0,
            "rate_2016": wmean(b["hard_ns_size"], b["weight"]) * 100,
            "rate_2021": wmean(e["hard_ns_size"], e["weight"]) * 100,
            "composition_pp": comp * 100,
            "rate_pp": rate * 100,
        }
    )
    return rows


def main() -> None:
    started = datetime.now(timezone.utc)
    print("Draft 5.0 Stage 1 verification")
    print(f"parent reconstruct: {D4 / 'reconstruct_four_wave.py'}")

    hashes = []
    for label, path in PUMF_PATHS.items():
        digest = sha256_file(path)
        hashes.append(
            {
                "label": str(label),
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": digest,
            }
        )
        print(f"  SHA-256 {path.name} {digest}")
    pd.DataFrame(hashes).to_csv(OUT / "input_sha256.csv", index=False)

    frozen = pd.read_csv(D4 / "outputs" / "primary_estimates.csv")
    frozen_flow = pd.read_csv(D4 / "outputs" / "sample_flow.csv")

    waves: dict[int, dict] = {}
    reproduction_rows = []
    distance_rows = []
    covid_rows = []
    mbm_rows = []
    composition_rows = []
    validation_rows = []
    ef_diag_rows = []
    stir_rows = []
    codebook_notes = []

    for year in (2006, 2011, 2016, 2021):
        spec = d4.WAVES[year]
        print(f"\n=== {year} {spec['identity']} ===")
        persons = load_wave_extended(year)
        hh = d4.householdize(persons, year)
        hh, th = d4.attach_thresholds(hh, year)
        hh = attach_family_fields(persons, hh)
        analytic = hh.loc[hh["analytic"]].copy()
        flow = d4.sample_flow(hh, len(persons))

        h = rate_block(analytic, analytic["hard_ns_size"])
        print(
            f"  analytic n={h['n']:,} N={h['N']:,.0f} hardship={h['weighted_pct']:.2f}%"
        )

        waves[year] = {
            "persons": persons,
            "hh": hh,
            "analytic": analytic,
            "th": th,
            "flow": flow,
            "spec": spec,
        }

        if year in LOCKED_D4:
            lock = LOCKED_D4[year]
            fr = frozen[frozen["year"] == year].iloc[0]
            ff = frozen_flow[frozen_flow["year"] == year].iloc[0]
            n_ok = h["n"] == lock["n"] == int(fr["sample_households"])
            n_hat_ok = abs(h["N"] - lock["N"]) < 1.5
            rate_ok = abs(round(h["weighted_pct"], 1) - lock["hardship"]) < 1e-9
            flow_ok = (
                int(flow["analytic_households"]["sample"]) == int(ff["analytic_n"])
                and int(flow["households_in_file"]) == int(ff["households_in_file"])
            )
            reproduction_rows.append(
                {
                    "year": year,
                    "survey": spec["instrument"],
                    "file_identity": spec["identity"],
                    "local_path": str(spec["path"].relative_to(ROOT)),
                    "sha256": next(x["sha256"] for x in hashes if x["label"] == str(year)),
                    "person_records": int(len(persons)),
                    "households_in_file": int(flow["households_in_file"]),
                    "drop_tenure": flow["drop_tenure_not_owner_renter"]["sample"],
                    "drop_income": flow["drop_missing_or_nonpositive_aftertax_income"]["sample"],
                    "drop_shelter": flow["drop_missing_shelter"]["sample"],
                    "analytic_n": h["n"],
                    "locked_n": lock["n"],
                    "frozen_n": int(fr["sample_households"]),
                    "analytic_N": round(h["N"]),
                    "locked_N": lock["N"],
                    "frozen_N": int(fr["estimated_households"]),
                    "hardship_pct": round(h["weighted_pct"], 4),
                    "locked_hardship_pct": lock["hardship"],
                    "frozen_hardship_pct": float(fr["hardship_ns_size_w"]),
                    "owner_hardship_pct": round(
                        wmean(analytic.loc[analytic["is_owner"], "hard_ns_size"], analytic.loc[analytic["is_owner"], "weight"])
                        * 100,
                        4,
                    ),
                    "renter_hardship_pct": round(
                        wmean(analytic.loc[analytic["is_renter"], "hard_ns_size"], analytic.loc[analytic["is_renter"], "weight"])
                        * 100,
                        4,
                    ),
                    "one_person_hardship_pct": round(
                        wmean(
                            analytic.loc[analytic["n_persons"] == 1, "hard_ns_size"],
                            analytic.loc[analytic["n_persons"] == 1, "weight"],
                        )
                        * 100,
                        4,
                    ),
                    "n_match": n_ok,
                    "N_match": n_hat_ok,
                    "rate_match_1dp": rate_ok,
                    "flow_match": flow_ok,
                    "reproduction_status": "PASS" if (n_ok and n_hat_ok and rate_ok and flow_ok) else "FAIL",
                }
            )

        # EF diagnosis for every wave
        if "n_ef" in hh.columns and hh["n_ef"].notna().any():
            multi = hh["n_ef"] > 1
            analytic_multi = analytic["n_ef"] > 1
            shelter_nunique = persons.groupby("HH_ID")["SHELCO" if "SHELCO" in persons.columns else "GROSRT"].nunique(dropna=False)
            ef_diag_rows.append(
                {
                    "year": year,
                    "households_in_file": int(len(hh)),
                    "hh_with_2plus_ef": int(multi.sum()),
                    "pct_hh_2plus_ef": float(multi.mean() * 100),
                    "analytic_hh_2plus_ef": int(analytic_multi.sum()),
                    "weighted_pct_analytic_2plus_ef": wmean(analytic_multi.astype(float), analytic["weight"]) * 100,
                    "max_ef_per_hh": int(hh["n_ef"].max()),
                    "single_ef_analytic_n": int((analytic["n_ef"] == 1).sum()),
                    "reason_if_not_implementable": (
                        "SHELCO/GROSRT/OMP are household dwelling costs. "
                        f"{int(multi.sum())} households contain 2+ economic families. "
                        "Assigning the full household shelter cost to each EF would double-count "
                        "the same dwelling cost. No EF-level shelter allocation exists on these PUMFs."
                    ),
                }
            )

        if year not in (2011, 2016, 2021):
            continue

        d = analytic
        m0 = rate_block(d, d["hard_ns_size"])
        se0 = random_group_se(d, "hard_ns_size")

        # M1 drop negative residual from universe
        pos = d[d["residual"] >= 0].copy()
        m1 = rate_block(pos, pos["hard_ns_size"])
        neg = d[d["residual"] < 0]
        neg_share = wmean((d["residual"] < 0).astype(float), d["weight"]) * 100

        # M2 documented provincial-median high-income recode (remain in universe)
        hard_m2 = apply_high_income_recode(d["hard_ns_size"], d)
        m2 = rate_block(d, hard_m2)
        above = d["equiv_inc"] > provincial_median_equiv(d)
        above_share = wmean(above.astype(float), d["weight"]) * 100
        recoded = above & (d["hard_ns_size"] == 1)
        recoded_share = wmean(recoded.astype(float), d["weight"]) * 100

        # M3 geo CMA/PR proxy
        m3 = rate_block(d, d["hard_ns_geo"])

        # M4 2008-base (and 2018-base counterpart)
        iy = INCOME_YEAR[year]
        row_2008 = None
        row_2018 = None
        try:
            row_2008 = series_row(iy, "2008 base")
        except KeyError:
            pass
        try:
            row_2018 = series_row(iy, "2018 base")
        except KeyError:
            pass
        hard_2008 = None
        hard_2018 = None
        if row_2008 is not None:
            thr = row_2008["national_unweighted_mean"]["nonshelter"] * (np.sqrt(d["n_persons"].clip(lower=1)) / 2.0)
            hard_2008 = (d["residual"] < thr).astype(float)
            m4 = rate_block(d, hard_2008)
        else:
            m4 = {"n": d.shape[0], "N": float(d["weight"].sum()), "weighted_pct": float("nan"), "n_flagged": None, "weighted_flagged": None, "unweighted_pct": float("nan")}
        if row_2018 is not None:
            thr18 = row_2018["national_unweighted_mean"]["nonshelter"] * (np.sqrt(d["n_persons"].clip(lower=1)) / 2.0)
            hard_2018 = (d["residual"] < thr18).astype(float)

        # Two-factor: drop_neg + geo
        hard_tf = (pos["residual"] < pos["mbm_ns_geo_size"]).astype(float)
        two_factor = rate_block(pos, hard_tf)

        # M6: drop_neg + geo + documented high-income recode
        pos6 = pos.copy()
        hard_geo = (pos6["residual"] < pos6["mbm_ns_geo_size"]).astype(float)
        hard_m6 = apply_high_income_recode(hard_geo, pos6)
        m6 = rate_block(pos6, hard_m6)

        def add_distance(code, name, block, status, notes, universe="analytic_households", extra=None):
            row = {
                "year": year,
                "survey": spec["instrument"],
                "scenario": code,
                "scenario_name": name,
                "status": status,
                "analytical_unit": "household",
                "income_concept": "sum of person TOTINC_AT after official NA codes (not MBM disposable income)",
                "shelter_concept": spec["shelter_mode"],
                "mbm_base": th["mbm_base"] if code not in {"M4"} else (row_2008["base"] if row_2008 else "unavailable"),
                "threshold": "non-shelter MBM x sqrt(n)/2",
                "geography": "national unweighted mean of Table 11-10-0066" if code in {"M0", "M1", "M2", "M4"} else "CMA/PR proxy (not official 50-region MBM)",
                "universe": universe,
                "eligibility": notes,
                "sample_n": block.get("n"),
                "weighted_N": None if block.get("N") is None else round(block["N"]),
                "excluded_from_m0_n": m0["n"] - (block.get("n") or 0) if block.get("n") is not None else None,
                "excluded_from_m0_N": None if block.get("N") is None else round(m0["N"] - block["N"]),
                "hardship_pct": None if block.get("weighted_pct") is None or not math.isfinite(block["weighted_pct"]) else round(block["weighted_pct"], 4),
                "pp_vs_m0": None
                if block.get("weighted_pct") is None or not math.isfinite(block["weighted_pct"])
                else round(block["weighted_pct"] - m0["weighted_pct"], 4),
                "se_pp_random_groups": None if se0 is None or code != "M0" else round(se0["se"] * 100, 3),
                "official_cmhc": False,
            }
            if extra:
                row.update(extra)
            distance_rows.append(row)

        add_distance(
            "M0",
            "Draft 4.0 primary",
            m0,
            "IMPLEMENTED",
            "owner/renter, income>0, valid shelter; national non-shelter MBM x sqrt(n)/2; negative residual retained as hardship",
        )
        add_distance(
            "M1",
            "drop_neg_residual",
            m1,
            "IMPLEMENTED",
            f"M0 universe minus residual<0. Weighted share excluded={neg_share:.3f}%. Negative residual may be genuine severe hardship; exclusion changes the population.",
            universe="analytic_households with residual>=0",
            extra={"negative_residual_weighted_pct_of_m0": round(neg_share, 4)},
        )
        add_distance(
            "M2",
            "high_income_cap_provincial_median",
            m2,
            "IMPLEMENTED — documented CMHC 2020 provincial-median rule only",
            (
                "CMHC 2020 Research Insight: equivalized income above the provincial median cannot be hardship. "
                f"Weighted share above provincial median={above_share:.3f}%; recoded out of hardship={recoded_share:.3f}%. "
                "Investment/capital-gain/farm restrictions NOT IMPLEMENTED — INSUFFICIENT EVIDENCE on these PUMFs. "
                "Households remain in the denominator."
            ),
            extra={
                "above_provincial_median_weighted_pct": round(above_share, 4),
                "recoded_from_hardship_weighted_pct": round(recoded_share, 4),
            },
        )
        add_distance(
            "M3",
            "geo_cma_pr",
            m3,
            "APPROXIMATED — not official 50-region MBM",
            "Selected-CMA non-shelter MBM if CMA in {462,535,825,835,933}; else provincial mean of Table 11-10-0066; else national mean.",
        )
        add_distance(
            "M4",
            "mbm_2008base_same_income_year",
            m4,
            "IMPLEMENTED" if row_2008 is not None else "NOT AVAILABLE",
            "Score this wave with 2008-base non-shelter MBM for the same income year. 2011/2016 primary already uses 2008-base; 2021 primary uses 2018-base.",
        )
        add_distance(
            "M5",
            "ef_unit",
            {"n": None, "N": None, "weighted_pct": float("nan")},
            "NOT IMPLEMENTABLE",
            (
                "Economic-family residual-income test is not implementable. Shelter costs are household dwelling "
                "costs (SHELCO or TENUR-conditioned GROSRT/OMP). Multiple EF_ID values share one dwelling. "
                "No supported rule allocates that shelter cost across economic families. "
                "Assigning the full household shelter cost to each EF would double-count. "
                "EFDIMBM / EFDIMBM_2018 are economic-family MBM disposable income, but they cannot be paired "
                "with household shelter for multi-EF households."
            ),
            universe="not constructed",
        )
        add_distance(
            "TWO_FACTOR",
            "drop_neg_residual + geo_cma_pr",
            two_factor,
            "IMPLEMENTED — research approximation, not official CMHC",
            "Original two-factor variant requested separately from M6. Universe = residual>=0; threshold = CMA/PR proxy.",
            universe="analytic_households with residual>=0",
        )
        add_distance(
            "M6",
            "closest_feasible_cmhc_like",
            m6,
            "APPROXIMATED — closest feasible documented subset, not official CMHC",
            (
                "Combined documented/feasible components only: drop residual<0 + CMA/PR proxy + provincial-median "
                "high-income recode. Unavailable: MBM disposable income, official 50-region geography, "
                "investment/capital-gain/farm restrictions, farm/band/reserve universe."
            ),
            universe="analytic_households with residual>=0",
        )
        add_distance(
            "MBM_DISPOSABLE",
            "official_mbm_disposable_income",
            {"n": None, "N": None, "weighted_pct": float("nan")},
            "NOT AVAILABLE",
            "Census TOTINC_AT is after-tax income, not ESDC MBM disposable income. EFDIMBM(_2018) is an economic-family field and cannot be used as household MBM disposable income without an unsupported allocation.",
            universe="not constructed",
        )
        add_distance(
            "MBM_50_REGION",
            "official_50_region_mbm",
            {"n": None, "N": None, "weighted_pct": float("nan")},
            "NOT AVAILABLE",
            "PUMF geography is 5 named CMAs + residual 999 + PR. Official MBM has ~50 community/size cells.",
            universe="not constructed",
        )

        mbm_rows.append(
            {
                "year": year,
                "income_year": iy,
                "primary_base": PRIMARY_BASE[iy],
                "primary_hardship_pct": round(m0["weighted_pct"], 4),
                "base_2008_hardship_pct": None if hard_2008 is None else round(wmean(hard_2008, d["weight"]) * 100, 4),
                "base_2018_hardship_pct": None if hard_2018 is None else round(wmean(hard_2018, d["weight"]) * 100, 4),
                "ref_family_nonshelter_primary": th["ref_family_nonshelter"],
                "ref_family_nonshelter_2008": None if row_2008 is None else row_2008["national_unweighted_mean"]["nonshelter"],
                "ref_family_nonshelter_2018": None if row_2018 is None else row_2018["national_unweighted_mean"]["nonshelter"],
            }
        )

        # COVID / ERB — 2021 only
        if year == 2021 and d["hh_erb"].notna().any():
            rec = d["hh_erb"].fillna(0) > 0
            bands = pd.cut(
                d["hh_erb"].fillna(0),
                bins=[-0.1, 0, 5000, 10000, 20000, 1e12],
                labels=["0", "1_to_5000", "5001_to_10000", "10001_to_20000", "over_20000"],
            )
            for label, mask in (
                ("all_analytic", pd.Series(True, index=d.index)),
                ("erb_receipt_gt0", rec),
                ("no_recorded_erb", ~rec),
            ):
                sub = d[mask]
                covid_rows.append(
                    {
                        "stratum": label,
                        "sample_n": int(len(sub)),
                        "weighted_N": round(float(sub["weight"].sum())),
                        "weighted_share_of_analytic": wmean(mask.astype(float), d["weight"]) * 100,
                        "median_hh_erb": None if label == "no_recorded_erb" else wmedian(sub["hh_erb"].fillna(0), sub["weight"]),
                        "hardship_pct": round(wmean(sub["hard_ns_size"], sub["weight"]) * 100, 4),
                        "note": "EFCOVID_ERB is a dollar amount at the economic-family level. Household amount = sum of one copy per EF_ID. Sentinels 88888888/99999999 removed. TOTINC_AT already includes these benefits. No invented dollar amounts.",
                    }
                )
            for lab in bands.cat.categories:
                sub = d[bands == lab]
                covid_rows.append(
                    {
                        "stratum": f"erb_band_{lab}",
                        "sample_n": int(len(sub)),
                        "weighted_N": round(float(sub["weight"].sum())),
                        "weighted_share_of_analytic": wmean((bands == lab).astype(float), d["weight"]) * 100,
                        "median_hh_erb": wmedian(sub["hh_erb"].fillna(0), sub["weight"]) if len(sub) else None,
                        "hardship_pct": round(wmean(sub["hard_ns_size"], sub["weight"]) * 100, 4) if len(sub) else None,
                        "note": "Documented amount bands only. Not a causal estimate of ERB effects.",
                    }
                )
            # Documented-amount subtraction sensitivity (uses recorded dollars, not invented amounts)
            inc_wo = d["hh_income_at"] - d["hh_erb"].fillna(0)
            resid_wo = inc_wo - d["annual_shelter"]
            hard_wo = (resid_wo < d["mbm_ns_national_size"]).astype(float)
            covid_rows.append(
                {
                    "stratum": "sensitivity_subtract_recorded_erb_from_totinc_at",
                    "sample_n": int(len(d)),
                    "weighted_N": round(float(d["weight"].sum())),
                    "weighted_share_of_analytic": 100.0,
                    "median_hh_erb": wmedian(d["hh_erb"].fillna(0), d["weight"]),
                    "hardship_pct": round(wmean(hard_wo, d["weight"]) * 100, 4),
                    "note": "Sensitivity only: subtract the recorded household EFCOVID_ERB total from TOTINC_AT. This is not an official counterfactual and does not restore a non-pandemic income distribution.",
                }
            )

        # STIR_GRP version check
        if year == 2021 and d["stir_grp"].notna().any():
            univ = d[d["stir_grp"].isin([0, 1])].copy()
            correct_bt = univ["annual_shelter"] / univ["hh_income_bt"].clip(lower=1)
            wrong_bt = univ["shelter_m"] / univ["hh_income_bt"].clip(lower=1)
            flag = univ["stir_grp"] == 1
            for name, pred in (
                ("corrected_monthly_over_monthly_bt_ge30", correct_bt >= 0.30),
                ("uncorrected_monthly_over_annual_bt_ge30", wrong_bt >= 0.30),
                ("corrected_at_ge30", (univ["annual_shelter"] / univ["hh_income_at"].clip(lower=1)) >= 0.30),
            ):
                agree = float((flag.astype(int) == pred.astype(int)).mean())
                stir_rows.append(
                    {
                        "comparison": name,
                        "universe_n": int(len(univ)),
                        "stir_grp1_weighted_pct": wmean(flag.astype(float), univ["weight"]) * 100,
                        "reconstructed_weighted_pct": wmean(pred.astype(float), univ["weight"]) * 100,
                        "unweighted_agreement": agree,
                        "note": "November 8, 2024 StatCan correction: STIR_GRP should be SHELCO / (household income / 12). Uncorrected used SHELCO / annual income.",
                    }
                )

        # Independent validation pieces per year
        all_hh = hh
        tenure_univ = all_hh[all_hh["tenure_ok"]]
        validation_rows.append(
            {
                "year": year,
                "check": "weighted_homeownership_tenure_ok_file",
                "estimate": wmean(tenure_univ["is_owner"].astype(float), tenure_univ["weight"]) * 100,
                "published": 66.5 if year == 2021 else None,
                "source": "2021 Census housing / The Daily homeownership rate ~66.5% of private households",
                "note": "PUMF owner share among TENUR in {1,2}. Not restricted to the residual-income analytic subset.",
            }
        )
        flags = d4.published_flags(analytic)
        if "hcoreneed_ind" in flags:
            validation_rows.append(
                {
                    "year": year,
                    "check": "hcoreneed_ind_all",
                    "estimate": flags["hcoreneed_ind"]["weighted_pct"],
                    "published": benchmarks()["core_housing_need"]["values"].get(str(year), {}).get("all"),
                    "source": "Statistics Canada / CMHC core housing need",
                    "note": flags["hcoreneed_ind"]["codes"],
                }
            )
        for ten, key in (("is_owner", "owner"), ("is_renter", "renter")):
            sub = analytic[analytic[ten]]
            if sub["hcoreneed"].notna().any():
                univ = sub[sub["hcoreneed"].isin([0, 100, 0.0, 100.0])]
                if len(univ):
                    validation_rows.append(
                        {
                            "year": year,
                            "check": f"hcoreneed_ind_{key}",
                            "estimate": wmean((univ["hcoreneed"] == 100).astype(float), univ["weight"]) * 100,
                            "published": benchmarks()["core_housing_need"]["values"].get(str(year), {}).get(key),
                            "source": "Statistics Canada / CMHC core housing need",
                            "note": "Different indicator from residual-income hardship.",
                        }
                    )
            una = ((sub["stir_bt"] >= 0.30) & (sub["stir_bt"] < 1.0)).astype(float)
            pub = benchmarks()["unaffordable_housing_stir_ge_30_percent"]["values"].get(str(year), {})
            validation_rows.append(
                {
                    "year": year,
                    "check": f"stir_bt_ge30_lt100_{key}",
                    "estimate": wmean(una, sub["weight"]) * 100,
                    "published": pub.get(key) if isinstance(pub, dict) else None,
                    "source": "The Daily 21 September 2022; Census unaffordable housing",
                    "note": "Official unaffordable-housing universe is non-farm non-reserve STIR<100%. PUMF cannot fully implement farm/reserve exclusions.",
                }
            )
        validation_rows.append(
            {
                "year": year,
                "check": "residual_hardship_primary",
                "estimate": m0["weighted_pct"],
                "published": None,
                "source": "Draft 4.0 / Draft 5.0 reconstructed estimand",
                "note": "Not comparable numerically to core need or STIR. Not an official CMHC hardship rate.",
            }
        )
        if se0 is not None:
            validation_rows.append(
                {
                    "year": year,
                    "check": "m0_random_groups_se_pp",
                    "estimate": se0["se"] * 100,
                    "published": None,
                    "source": se0["source"],
                    "note": se0["method"],
                }
            )

    # Composition / Kitagawa 2016 vs 2021
    a16 = waves[2016]["analytic"].copy()
    a21 = waves[2021]["analytic"].copy()
    a16["tenure"] = np.where(a16["is_owner"], "owner", "renter")
    a21["tenure"] = np.where(a21["is_owner"], "owner", "renter")
    a16["size_cat"] = np.where(a16["n_persons"] == 1, "1", np.where(a16["n_persons"] == 2, "2", np.where(a16["n_persons"] == 3, "3", "4plus")))
    a21["size_cat"] = np.where(a21["n_persons"] == 1, "1", np.where(a21["n_persons"] == 2, "2", np.where(a21["n_persons"] == 3, "3", "4plus")))
    a16["tenure_size"] = a16["tenure"] + "_" + a16["size_cat"]
    a21["tenure_size"] = a21["tenure"] + "_" + a21["size_cat"]

    def income_quartile(frame: pd.DataFrame) -> pd.Series:
        # Weighted quartiles of current-dollar after-tax income within year.
        x = frame[["hh_income_at", "weight"]].dropna().sort_values("hh_income_at")
        cdf = x["weight"].cumsum() / x["weight"].sum()
        cuts = []
        for p in (0.25, 0.50, 0.75):
            cuts.append(float(x.loc[cdf >= p, "hh_income_at"].iloc[0]))
        return pd.cut(frame["hh_income_at"], bins=[-np.inf, *cuts, np.inf], labels=["Q1", "Q2", "Q3", "Q4"])

    a16["inc_q"] = income_quartile(a16)
    a21["inc_q"] = income_quartile(a21)
    for grouping in ("tenure", "size_cat", "tenure_size", "inc_q"):
        composition_rows.extend(kitagawa(a16, a21, grouping))

    # One-person series B snapshot
    one_rows = []
    for year in (2006, 2011, 2016, 2021):
        a = waves[year]["analytic"]
        one = a[a["n_persons"] == 1]
        one_rows.append(
            {
                "year": year,
                "survey": waves[year]["spec"]["instrument"],
                "sample_n": int(len(one)),
                "weighted_N": round(float(one["weight"].sum())),
                "hardship_pct": round(wmean(one["hard_ns_size"], one["weight"]) * 100, 4),
                "retention_note": "2006 one-person shelter is usable; 2006 all-household is not comparable.",
            }
        )

    # Codebook ledger rows
    codebook_notes.extend(
        [
            {
                "item": "REGION_2006",
                "status": "CONFIRMED",
                "source": "2006 Census hierarchical PUMF user guide 95M0029XVB, REGION field",
                "finding": "1 Eastern Canada (NL/PE/NS/NB); 2 Quebec; 3 Ontario; 4 Prairies (MB/SK/AB); 5 British Columbia; 6 Northern Canada (YT/NT/NU). Draft 4.0 inferred labels match the official page. UNCERTAIN label retired.",
            },
            {
                "item": "LOMBM_2011",
                "status": "CONFIRMED",
                "source": "2011 NHS hierarchical PUMF user guide 99M0002X, LOMBM field",
                "finding": "1 = member of a non-low-income economic family; 2 = member of a low-income economic family; 8 not available; 9 not applicable (territories). Draft 4.0 treatment of code 2 as below-MBM is correct. UNCERTAIN label retired.",
            },
            {
                "item": "STIR_GRP_2021_correction",
                "status": "NOTICE_VERIFIED",
                "source": "https://www150.statcan.gc.ca/n1/pub/98m0001x/index-eng.htm correction date 8 November 2024",
                "finding": "Original March 20 2024 hierarchical file calculated STIR_GRP as shelter cost / total household income. Corrected file uses shelter cost / average monthly household income. Local file version is inferred by reconstructing both formulas against STIR_GRP (see stir_grp_version_check.csv).",
            },
            {
                "item": "EFCOVID_ERB",
                "status": "CONFIRMED",
                "source": "2021 Census dictionary pop254; 2021 hierarchical PUMF variable list (Borealis/Abacus)",
                "finding": "Dollar amount: COVID-19 emergency and recovery benefits of the economic family (CERB, CRB, CRCB, CRSB, CESB). Calendar 2020. Sentinels 88888888 / 99999999. Not a receipt flag only.",
            },
            {
                "item": "replicate_weights_2006_2011",
                "status": "FORMULA_CONFIRMED",
                "source": "95M0029XVB and 99M0002X user guides, random-groups method",
                "finding": "Eight replicates. SE = sqrt(sum((r_i - rbar)^2) / 56). Draft 4.0 used mean((r_i - point)^2), which is not the user-guide formula. Stage 1 reports the documented formula for 2006/2011 only.",
            },
            {
                "item": "replicate_weights_2016_2021",
                "status": "WEIGHTS_PRESENT_FORMULA_NOT_RECOVERED",
                "source": "2016/2021 hierarchical PUMF contain WT1–WT16; Census 98-306 describes Fay BRR for the long form, not the PUMF-specific divisor",
                "finding": "Do not present 2016/2021 replicate intervals as design-based confidence intervals in this pass.",
            },
            {
                "item": "CMHC_2024_census_hardship",
                "status": "NOT_RECOVERED",
                "source": "publications.gc.ca 9.949944; withdrawn 25 November 2025 at CMHC request",
                "finding": "Catalogue NH18-33/85-2024E-PDF identified. PDF collection URL now serves an archived-removal page. Internet Archive CDX empty. LAC weekly-acquisitions URL 404. Official 2021 Census hardship rate not quoted.",
            },
        ]
    )

    pd.DataFrame(reproduction_rows).to_csv(OUT / "baseline_reproduction.csv", index=False)
    pd.DataFrame(distance_rows).to_csv(OUT / "distance_to_official_cmhc.csv", index=False)
    pd.DataFrame(covid_rows).to_csv(OUT / "covid_erb_stratification.csv", index=False)
    pd.DataFrame(mbm_rows).to_csv(OUT / "mbm_base_sensitivity.csv", index=False)
    pd.DataFrame(composition_rows).to_csv(OUT / "composition_decomposition.csv", index=False)
    pd.DataFrame(validation_rows).to_csv(OUT / "INDEPENDENT_VALIDATION_v05.csv", index=False)
    pd.DataFrame(ef_diag_rows).to_csv(OUT / "ef_unit_diagnosis.csv", index=False)
    pd.DataFrame(stir_rows).to_csv(OUT / "stir_grp_version_check.csv", index=False)
    pd.DataFrame(codebook_notes).to_csv(OUT / "SOURCE_VERIFICATION_LEDGER.csv", index=False)
    pd.DataFrame(one_rows).to_csv(OUT / "one_person_series_b.csv", index=False)

    env = {
        "started_utc": started.isoformat(),
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "parent_commit_intended": "b298af382523b5a14ba2e515ccdefc23326883bd",
        "draft4_code": str((D4 / "reconstruct_four_wave.py").relative_to(ROOT)),
        "command": "python3 papers/paper1_draft5/stage1_verification.py",
        "hashes": hashes,
        "gate_a": reproduction_rows,
    }
    (LOG / "stage1_run_environment.json").write_text(json.dumps(env, indent=2, default=str))
    print(f"\nWrote outputs to {OUT}")
    print("Gate A rows:")
    for r in reproduction_rows:
        print(f"  {r['year']} {r['reproduction_status']} {r['hardship_pct']}% n={r['analytic_n']} N={r['analytic_N']}")


if __name__ == "__main__":
    main()
