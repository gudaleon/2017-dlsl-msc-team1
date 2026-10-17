#!/usr/bin/env python3
"""Draft 4.0 figures and tables from the reconstructed household estimates.

Draft 3.0 figures in papers/paper1_highschool/ are not overwritten.
Analytical numbers come from outputs/primary_estimates.csv and the reconstruction JSON.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from PIL import Image

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
TAB = HERE / "tables"
FIG.mkdir(exist_ok=True)
TAB.mkdir(exist_ok=True)

NAVY = "#0072B2"
TEAL = "#009E73"
ORANGE = "#E69F00"
SLATE = "#3D3D3D"
RED = "#D55E00"
INK = "#111111"
GRID = "#D0D0D0"

# Comparable all-household waves (2006 all-HH is not comparable).
YEAR_POS = {2011: 0, 2016: 1, 2021: 2}
YEAR_TICKS = [0, 1, 2]
YEAR_LABELS = ["2011", "2016", "2021"]
years = [2011, 2016, 2021]

# Weighted household estimates, 2021 CAD for dollars (Table 18-10-0005).
n = [130242, 139869, 148085]
N_mill = [13.02, 14.04, 14.86]
inc_med = [65634, 69346, 76485]
shel_med = [1094, 1118, 1240]
stir30 = [29.6, 28.9, 25.9]
stir50 = [12.3, 11.1, 8.9]
hardship = [18.2, 17.3, 14.9]
owner = [10.8, 9.4, 8.8]
renter = [34.4, 34.2, 27.6]
one_person_years = [2006, 2011, 2016, 2021]
one_person = [28.8, 32.4, 32.2, 30.3]

plt.rcParams.update(
    {
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.edgecolor": "none",
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelcolor": INK,
        "axes.edgecolor": INK,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.alpha": 1.0,
        "grid.linestyle": ":",
        "grid.linewidth": 0.6,
        "xtick.color": INK,
        "ytick.color": INK,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)


def xpos(year_list: list[int]) -> list[int]:
    return [YEAR_POS[y] for y in year_list]


def style_year_axis(ax: plt.Axes) -> None:
    ax.set_xticks(YEAR_TICKS)
    ax.set_xticklabels(YEAR_LABELS)
    ax.set_xlim(-0.35, 2.35)


def inspect_png(path: Path) -> None:
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im)
    h, w, _ = arr.shape
    if h < 800 or w < 1200:
        raise RuntimeError(f"{path.name}: export too small ({w}x{h})")
    lower = arr[int(h * 0.62) :]
    if lower.std() < 8:
        raise RuntimeError(f"{path.name}: lower panel has almost no ink")
    print(f"  wrote {path.name}  {w}x{h}  ok")


def savefig(fig: plt.Figure, stem: str) -> None:
    kwargs = dict(facecolor="white", edgecolor="none", bbox_inches="tight", pad_inches=0.28)
    png = FIG / f"{stem}.png"
    fig.savefig(png, dpi=300, **kwargs)
    fig.savefig(FIG / f"{stem}.pdf", **kwargs)
    fig.savefig(FIG / f"{stem}.svg", **kwargs)
    plt.close(fig)
    inspect_png(png)


def fig01() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
    fig.suptitle(
        "Household housing affordability in Canada, 2011–2021 (reconstructed)",
        fontsize=13,
        fontweight="bold",
        color=INK,
    )
    x = xpos(years)
    ax = axes[0, 0]
    ax.plot(x, [v / 1000 for v in inc_med], "o-", color=TEAL, lw=2.2, ms=7)
    ax.set_title("A. Median household after-tax income")
    ax.set_ylabel("Thousands of 2021 CAD")
    style_year_axis(ax)
    ax.set_ylim(0, 100)
    for xi, v in zip(x, inc_med):
        ax.annotate(f"${v/1000:.1f}k", (xi, v / 1000), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
    ax = axes[0, 1]
    ax.plot(x, shel_med, "s-", color=ORANGE, lw=2.2, ms=7)
    ax.set_title("B. Median monthly shelter cost")
    ax.set_ylabel("2021 CAD per month")
    style_year_axis(ax)
    ax.set_ylim(0, 2000)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax = axes[1, 0]
    ax.plot(x, stir30, "o-", color=ORANGE, lw=2.2, ms=7, label="After-tax STIR > 30%")
    ax.plot(x, stir50, "s--", color=SLATE, lw=1.8, ms=6, label="After-tax STIR > 50%")
    ax.set_title("C. Shelter-to-income ratio (after tax)")
    ax.set_ylabel("Share of households (%)")
    ax.set_xlabel("Year")
    style_year_axis(ax)
    ax.set_ylim(0, 50)
    ax.legend(loc="upper right")
    ax = axes[1, 1]
    ax.plot(x, hardship, "D-", color=RED, lw=2.2, ms=7)
    ax.set_title("D. Reconstructed housing hardship")
    ax.set_ylabel("Share of households (%)")
    ax.set_xlabel("Year")
    style_year_axis(ax)
    ax.set_ylim(0, 40)
    for xi, y in zip(x, hardship):
        ax.annotate(f"{y:.1f}%", (xi, y), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9, fontweight="bold")
    ax.text(0.03, 0.07, "Not an official CMHC rate. 2011 is the voluntary NHS.", transform=ax.transAxes, fontsize=8, color=SLATE)
    savefig(fig, "fig01_national_trends")


def fig02() -> None:
    periods = ["2011–2016", "2016–2021"]
    inc_chg = [5.7, 10.3]
    shel_chg = [2.2, 10.9]
    hard_chg = [-0.9, -2.4]
    up, down = "#4C72B0", "#C44E52"
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.8), constrained_layout=True)
    fig.suptitle("Period changes in income, shelter cost, and reconstructed hardship", fontsize=13, fontweight="bold", color=INK)
    specs = [
        (inc_chg, "A. Median income", "Percent change", "{:+.1f}%", True),
        (shel_chg, "B. Median shelter cost", "Percent change", "{:+.1f}%", False),
        (hard_chg, "C. Housing hardship", "Percentage points", "{:+.1f} pp", False),
    ]
    for ax, (vals, title, ylab, fmt, higher_is_gain) in zip(axes, specs):
        colors = [(up if v >= 0 else down) if higher_is_gain else (down if v > 0 else up) for v in vals]
        bars = ax.bar(periods, vals, color=colors, edgecolor=INK, linewidth=0.4, width=0.58)
        ax.axhline(0, color=INK, lw=0.8)
        ax.set_title(title)
        ax.set_ylabel(ylab)
        ymax = max(abs(min(vals)), abs(max(vals))) * 1.7
        ax.set_ylim(-ymax, ymax)
        for bar, v in zip(bars, vals):
            yoff = 0.06 * ymax if v >= 0 else -0.06 * ymax
            ax.text(bar.get_x() + bar.get_width() / 2, v + yoff, fmt.format(v), ha="center", va="bottom" if v >= 0 else "top", fontweight="bold", fontsize=10)
    fig.text(0.5, -0.02, "Weighted households. 2011 is the NHS. Blue = income up or hardship down. Red = shelter up or hardship up.", ha="center", fontsize=8.5, color=SLATE)
    savefig(fig, "fig02_period_comparison")


def fig03() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 5.2), constrained_layout=True)
    x = xpos(years)
    ax.plot(x, owner, "o-", color=TEAL, lw=2.3, ms=8, label="Owners")
    ax.plot(x, renter, "s-", color=ORANGE, lw=2.3, ms=8, label="Renters")
    for xi, o, r in zip(x, owner, renter):
        ax.plot([xi, xi], [o, r], color="#888888", ls=":", lw=1.0)
        ax.annotate(f"{r-o:.1f} pp", xy=(xi + 0.06, (o + r) / 2), fontsize=8, color=SLATE)
    ax.set_title("Owner versus renter reconstructed housing hardship")
    ax.set_xlabel("Year")
    ax.set_ylabel("Hardship rate (%)")
    style_year_axis(ax)
    ax.set_ylim(0, 50)
    ax.legend(loc="upper right")
    ax.text(0.02, 0.045, "Household-weighted. Renters remain about three times as likely to be in reconstructed hardship as owners.", transform=ax.transAxes, fontsize=8.5, color=SLATE)
    savefig(fig, "fig03_tenure_divergence")


def fig04() -> None:
    inc_idx = [100.0, 105.7, 116.5]
    shel_idx = [100.0, 102.2, 113.4]
    x = xpos(years)
    fig, ax = plt.subplots(figsize=(8.8, 5.3), constrained_layout=True)
    ax.plot(x, inc_idx, "o-", color=TEAL, lw=2.3, ms=8, label="Median after-tax income")
    ax.plot(x, shel_idx, "s-", color=ORANGE, lw=2.3, ms=8, label="Median shelter cost")
    ax.axhline(100, color="#888888", ls="--", lw=1, label="2011 = 100")
    ax.fill_between(x, inc_idx, shel_idx, color=TEAL, alpha=0.12, label="Income grew faster than shelter")
    ax.set_title("Income and shelter, indexed (2011 = 100, 2021 CAD)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Index")
    style_year_axis(ax)
    ax.set_ylim(88, 140)
    ax.legend(loc="upper left")
    savefig(fig, "fig04_income_shelter_index")


def fig05() -> None:
    fig = plt.figure(figsize=(11.2, 7.6), constrained_layout=True)
    fig.suptitle("Draft 4.0 dashboard: reconstructed household hardship", fontsize=13, fontweight="bold", color=INK)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 1.0])
    ax = fig.add_subplot(gs[0, :])
    bars = ax.bar(YEAR_LABELS, hardship, color=[ORANGE, TEAL, NAVY], edgecolor=INK, linewidth=0.4, width=0.5)
    ax.set_ylabel("Hardship rate (%)")
    ax.set_title("A. Primary series (2011 NHS, 2016 and 2021 Census)")
    ax.set_ylim(0, 30)
    for bar, y, ni in zip(bars, hardship, n):
        ax.text(bar.get_x() + bar.get_width() / 2, y + 0.6, f"{y:.1f}%\nn={ni:,}", ha="center", va="bottom", fontsize=8)
    ax = fig.add_subplot(gs[1, 0])
    ax.plot([0, 1, 2, 3], one_person, "D-", color=RED, lw=2.0, ms=7)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["2006", "2011", "2016", "2021"])
    ax.set_title("B. One-person robustness")
    ax.set_ylabel("Hardship (%)")
    ax.set_ylim(20, 40)
    ax = fig.add_subplot(gs[1, 1])
    w = 0.36
    xs = np.arange(3)
    ax.bar(xs - w / 2, owner, width=w, color=TEAL, edgecolor=INK, linewidth=0.3, label="Owners")
    ax.bar(xs + w / 2, renter, width=w, color=ORANGE, edgecolor=INK, linewidth=0.3, label="Renters")
    ax.set_xticks(xs)
    ax.set_xticklabels(YEAR_LABELS)
    ax.set_title("C. Tenure")
    ax.set_ylabel("Hardship (%)")
    ax.set_ylim(0, 50)
    ax.legend(loc="upper right")
    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    ax.text(0.0, 0.92, "What changed vs Draft 3.0", fontsize=10, fontweight="bold", color=INK, transform=ax.transAxes)
    ax.text(
        0.0,
        0.05,
        "Household unit, not person rows.\n"
        "Survey weights applied.\n"
        "2016 restored (99.4% of HH).\n"
        "2006 all-HH dropped (shelter 8888).\n"
        "Non-shelter MBM × √n / 2.\n"
        "Not an official CMHC rate.\n"
        "2011 is the voluntary NHS.",
        fontsize=9,
        color=SLATE,
        transform=ax.transAxes,
        va="bottom",
        linespacing=1.45,
    )
    savefig(fig, "fig05_summary_dashboard")


def write_tables() -> None:
    t1 = pd.DataFrame(
        {
            "Year": [2006, 2011, 2016, 2021],
            "Person records": [309841, 333008, 343330, 361915],
            "Households in file": [124358, 133192, 140720, 149789],
            "Analytic n": [52785, 130242, 139869, 148085],
            "Estimated N": [5279588, 13019080, 14037793, 14863013],
            "Retention %": [42.4, 97.8, 99.4, 98.9],
            "In primary series": ["No — shelter suppression", "Yes (NHS break)", "Yes", "Yes"],
        }
    )
    t2 = pd.DataFrame(
        {
            "Year": years,
            "Sample n": n,
            "Estimated N (millions)": N_mill,
            "Median after-tax income (2021 CAD)": inc_med,
            "Median monthly shelter (2021 CAD)": shel_med,
            "After-tax STIR > 30%": stir30,
            "After-tax STIR > 50%": stir50,
        }
    )
    t3 = pd.DataFrame(
        {
            "Year": years,
            "All households %": hardship,
            "Owners %": owner,
            "Renters %": renter,
            "One-person %": [32.4, 32.2, 30.3],
        }
    )
    t4 = pd.DataFrame(
        {
            "Check": [
                "Weighted HH vs published private HH",
                "Median after-tax income (2020-constant)",
                "Before-tax STIR 30–99% vs unaffordable housing",
                "2021 HCORENEED_IND vs core housing need",
                "CMHC CIS 2017 hardship (different source/definition)",
            ],
            "2011": ["−0.02%", "$63,502 vs $63,600", "—", "—", "—"],
            "2016": ["+0.36%", "$67,093 vs $66,500", "21.5% vs 24.1%", "—", "17.3% vs ~9%"],
            "2021": ["+0.37%", "$74,000 vs $73,000", "19.5% vs 20.9%", "10.12% vs 10.1%", "—"],
        }
    )
    t5 = pd.DataFrame(
        {
            "Variant": [
                "Primary (non-shelter, size, national, weighted)",
                "CMA/PR geography approximation",
                "Full MBM (double-counts shelter)",
                "Single-adult non-shelter",
                "Draft 3.0 leftover line",
                "Drop negative residual",
                "Owners",
                "Renters",
            ],
            "2011 %": [18.2, 17.3, 26.5, 14.6, 14.6, 14.2, 10.8, 34.4],
            "2016 %": [17.3, 16.6, 25.5, 13.6, 14.9, 14.4, 9.4, 34.2],
            "2021 %": [14.9, 11.9, 26.6, 11.9, 13.6, 12.8, 8.8, 27.6],
        }
    )
    for name, df in [
        ("table1_sample_flow", t1),
        ("table2_income_shelter", t2),
        ("table3_hardship", t3),
        ("table4_validation", t4),
        ("table5_sensitivity", t5),
    ]:
        df.to_csv(TAB / f"{name}.csv", index=False)
        print(f"  wrote {name}.csv")


def main() -> None:
    fig01()
    fig02()
    fig03()
    fig04()
    fig05()
    write_tables()


if __name__ == "__main__":
    main()
