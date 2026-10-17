"""Load official CPI / MBM extracts used by the Draft 4.0 reconstruction.

Numbers are derived from Statistics Canada tables downloaded 17 October 2026.
They are not invented. See official/SOURCES.md.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OFFICIAL = HERE / "official"

# Census wave -> income year (Statistics Canada PUMF convention)
INCOME_YEAR = {2006: 2005, 2011: 2010, 2016: 2015, 2021: 2020}

# Primary MBM base for each income year: the contemporaneous official base.
PRIMARY_BASE = {
    2005: "2000 base",
    2010: "2008 base",
    2015: "2008 base",
    2020: "2018 base",
}

# Standard SGC CMA codes released on these hierarchical PUMFs.
CMA_LABEL = {
    462: "Montreal",
    535: "Toronto",
    825: "Calgary",
    835: "Edmonton",
    933: "Vancouver",
}

PR_NAME = {
    10: "Newfoundland and Labrador",
    11: "Prince Edward Island",
    12: "Nova Scotia",
    13: "New Brunswick",
    24: "Quebec",
    35: "Ontario",
    46: "Manitoba",
    47: "Saskatchewan",
    48: "Alberta",
    59: "British Columbia",
    60: "Yukon",
    61: "Northwest Territories",
    62: "Nunavut",
    63: "Northwest Territories",
    70: "Territories",
}

# 2006 PUMF REGION codes inferred from household shares (UNCERTAIN without the codebook page).
REGION2006_NAME = {
    1: "Atlantic",
    2: "Quebec",
    3: "Ontario",
    4: "Prairies",
    5: "British Columbia",
    6: "Territories",
}


def _load(name: str) -> dict:
    return json.loads((OFFICIAL / name).read_text())


def cpi_extract() -> dict:
    return _load("cpi_18-10-0005_extract.json")


def mbm_extract() -> dict:
    return _load("mbm_11-10-0066_national.json")


def benchmarks() -> dict:
    return _load("published_benchmarks.json")


def series_row(income_year: int, base: str | None = None) -> dict:
    base = base or PRIMARY_BASE[income_year]
    for row in mbm_extract()["series"]:
        if row["year"] == income_year and row["base"] == base:
            return row
    raise KeyError(f"No MBM series for {income_year} {base}")


def cpi_to_2021(income_year: int) -> float:
    return float(cpi_extract()["factors_income_year_to_2021"][str(income_year)])


def primary_thresholds(census_year: int) -> dict:
    iy = INCOME_YEAR[census_year]
    row = series_row(iy)
    mean = row["national_unweighted_mean"]
    return {
        "income_year": iy,
        "mbm_base": row["base"],
        "n_regions": row["n_regions"],
        "ref_family_total": mean["total"],
        "ref_family_shelter": mean["shelter"],
        "ref_family_nonshelter": mean["nonshelter"],
        "single_adult_full_mbm": mean["single_adult_full_mbm"],
        "single_adult_nonshelter": mean["single_adult_nonshelter"],
        "cpi_income_year_to_2021": cpi_to_2021(iy),
        "by_province_nonshelter": row["by_province_mean_nonshelter"],
        "selected_cma_nonshelter": {
            k: v["nonshelter"] for k, v in row["selected_cma_nonshelter"].items()
        },
        "note": row["note"],
    }
