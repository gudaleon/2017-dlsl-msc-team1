#!/usr/bin/env python3
"""Fingerprint local Census CSVs and diagnose 2006/2016 retention collapse."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("audit/outputs")
OUT.mkdir(parents=True, exist_ok=True)

FILES = [
    RAW / "census_2006.csv",
    RAW / "census_2006_pumf.csv",
    RAW / "census_2011_nhs.csv",
    RAW / "census_2016_pumf.csv",
    RAW / "census_2021_full.csv",
]

SHELTER_CANDIDATES = ["SHELCO", "GROSRT", "OMP", "SHELTER"]
INCOME_CANDIDATES = ["TOTINC", "TOTINC_AT", "INCTOT", "TOTINCH"]
ID_CANDIDATES = ["HH_ID", "EF_ID", "CF_ID", "PP_ID"]
WEIGHT_CANDIDATES = ["WEIGHT", "WEIGHTP", "WEIGHTH"]
MARKER_COLS = [
    "CIP2011",
    "CIP2021",
    "CIP",
    "EFDIMBM",
    "EFDIMBM_2018",
    "EFCOVID_ERB",
    "HCORENEED_IND",
    "STIR_GRP",
    "GENDER",
    "SEX",
    "PRESMORTG",
    "MORGH",
    "SHELCO",
    "GROSRT",
    "OMP",
]


def file_md5_head(path: Path, nbytes: int = 2_000_000) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        h.update(f.read(nbytes))
    return h.hexdigest()


def describe_numeric(s: pd.Series) -> dict:
    s = pd.to_numeric(s, errors="coerce")
    codes = {
        "n": int(s.notna().sum()),
        "n_zero": int((s == 0).sum()),
        "n_8888": int((s == 8888).sum()),
        "n_9999": int((s == 9999).sum()),
        "n_99999": int((s == 99999).sum()),
        "n_888888": int((s == 888888).sum()),
        "n_999999": int((s == 999999).sum()),
        "n_8888888": int((s == 8888888).sum()),
        "n_9999999": int((s == 9999999).sum()),
        "n_ge_1e7": int((s >= 10_000_000).sum()),
        "min": float(s.min()) if s.notna().any() else None,
        "p50": float(s.median()) if s.notna().any() else None,
        "p99": float(s.quantile(0.99)) if s.notna().any() else None,
        "max": float(s.max()) if s.notna().any() else None,
    }
    return codes


def old_filter_retention(df: pd.DataFrame) -> dict:
    """Replicate run_four_wave_analysis.py column pick + filter."""
    income_col = None
    shelter_col = None
    for col in df.columns:
        if col in ["TOTINC", "INCTOT", "TOTINC_AT"]:
            income_col = col
        if col in ["SHELCO", "GROSRT", "SHELTER"]:
            shelter_col = col
    if not income_col or not shelter_col:
        return {"income_col": income_col, "shelter_col": shelter_col, "valid": None}
    income = pd.to_numeric(df[income_col], errors="coerce")
    shelter = pd.to_numeric(df[shelter_col], errors="coerce").replace(
        [8888, 9999, 99999], np.nan
    )
    valid = (income > 0) & shelter.notna() & (shelter > 0) & (shelter < 10000)
    return {
        "income_col_last_match": income_col,
        "shelter_col_last_match": shelter_col,
        "n_valid": int(valid.sum()),
        "pct_valid": float(valid.mean() * 100),
        "median_income_valid": float(income[valid].median()) if valid.any() else None,
        "median_shelter_valid": float(shelter[valid].median()) if valid.any() else None,
    }


def fingerprint(path: Path) -> dict:
    print(f"\n=== {path.name} ===")
    size = path.stat().st_size
    df = pd.read_csv(path, low_memory=False)
    rec = {
        "file": path.name,
        "bytes": size,
        "md5_head_2mb": file_md5_head(path),
        "n_rows": int(len(df)),
        "n_cols": int(len(df.columns)),
        "columns": list(df.columns),
        "has": {c: (c in df.columns) for c in MARKER_COLS + ID_CANDIDATES + WEIGHT_CANDIDATES},
        "old_pipeline": old_filter_retention(df),
    }
    if "HH_ID" in df.columns:
        rec["n_unique_hh"] = int(df["HH_ID"].nunique())
        rec["mean_persons_per_hh"] = float(len(df) / df["HH_ID"].nunique())
    for col in SHELTER_CANDIDATES + INCOME_CANDIDATES + WEIGHT_CANDIDATES + ["TENUR"]:
        if col in df.columns:
            rec[f"desc_{col}"] = describe_numeric(df[col])
    print(
        f"  rows={rec['n_rows']:,} cols={rec['n_cols']} "
        f"hh={rec.get('n_unique_hh')} old={rec['old_pipeline']}"
    )
    return rec


def main() -> None:
    reports = [fingerprint(p) for p in FILES if p.exists()]
    # pairwise header/md5 identity
    identity = []
    for i, a in enumerate(reports):
        for b in reports[i + 1 :]:
            identity.append(
                {
                    "a": a["file"],
                    "b": b["file"],
                    "same_md5_head": a["md5_head_2mb"] == b["md5_head_2mb"],
                    "same_columns": a["columns"] == b["columns"],
                    "same_nrows": a["n_rows"] == b["n_rows"],
                }
            )
    out = {"files": reports, "pairwise": identity}
    dest = OUT / "file_fingerprints.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {dest}")
    print("\nPAIRWISE")
    for row in identity:
        print(row)


if __name__ == "__main__":
    main()
