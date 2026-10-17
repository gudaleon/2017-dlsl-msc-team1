#!/usr/bin/env python3
"""Generate publication figures and standalone tables for Paper 1 (high school).

Uses 2006, 2011, and 2021 Census waves only. Census 2016 is excluded because
valid-record retention was 9.4% and special codes distorted medians.
All dollar values are already inflation-adjusted to 2021 CAD.

Analytical numbers are taken from results/four_wave_temporal_results.json and
are not recalculated here. This script only controls rendering and export.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
TAB_DIR = ROOT / "tables"
FIG_DIR.mkdir(exist_ok=True)
TAB_DIR.mkdir(exist_ok=True)

# Okabe–Ito / journal muted palette (colorblind-safe, no neon fills)
NAVY = "#0072B2"
TEAL = "#009E73"
ORANGE = "#E69F00"
SLATE = "#3D3D3D"
RED = "#D55E00"
INK = "#111111"
GRID = "#D0D0D0"

# Equal-spaced census-year positions so 2021 is not pushed to the far right
# of a linear time axis (2006–2011 is 5 years; 2011–2021 is 10 years).
YEAR_POS = {2006: 0, 2011: 1, 2021: 2}
YEAR_TICKS = [0, 1, 2]
YEAR_LABELS = ["2006", "2011", "2021"]

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

# --- Source statistics (from results/four_wave_temporal_results.json) ---
years = [2006, 2011, 2021]
n = [78056, 341030, 358621]
inc_med = [34452, 45920, 46000]
inc_p25 = [17864, 22960, 25000]
inc_p75 = [70180, 101024, 93000]
shel_med = [1020.8, 1377.6, 1400.0]
shel_p25 = [765.6, 803.6, 800.0]
shel_p75 = [1531.2, 2181.2, 2129.0]
shel_mean = [1181.65, 1572.84, 1597.77]
stir30 = [56.98, 52.19, 50.77]
stir50 = [35.84, 33.63, 31.49]
hardship = [38.03, 33.86, 37.85]
hardship_n = [29681, 115459, 135740]
owner = [None, 31.41, 35.60]
renter = [38.03, 40.38, 43.64]


def xpos(year_list: list[int]) -> list[int]:
    return [YEAR_POS[y] for y in year_list]


def style_year_axis(ax: plt.Axes) -> None:
    ax.set_xticks(YEAR_TICKS)
    ax.set_xticklabels(YEAR_LABELS)
    ax.set_xlim(-0.35, 2.35)


def savefig(fig: plt.Figure, stem: str) -> None:
    fig.patch.set_facecolor("white")
    for ax in fig.axes:
        ax.set_facecolor("white")
        ax.tick_params(colors=INK)
    kwargs = dict(
        facecolor="white",
        edgecolor="none",
        bbox_inches="tight",
        pad_inches=0.28,
    )
    png = FIG_DIR / f"{stem}.png"
    pdf = FIG_DIR / f"{stem}.pdf"
    svg = FIG_DIR / f"{stem}.svg"
    fig.savefig(png, dpi=300, **kwargs)
    fig.savefig(pdf, **kwargs)
    fig.savefig(svg, **kwargs)
    plt.close(fig)
    inspect_png(png)


def inspect_png(path: Path) -> None:
    """Inspect the saved raster, not only the Matplotlib window."""
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im)
    h, w, _ = arr.shape
    if h < 800 or w < 1200:
        raise RuntimeError(f"{path.name}: export too small ({w}x{h})")

    def band_stats(band: np.ndarray) -> tuple[float, float]:
        # Mean luminance and share of near-uniform grey pixels.
        lum = band.mean(axis=2)
        grey = np.abs(band[:, :, 0].astype(int) - band[:, :, 1].astype(int)) < 8
        grey &= np.abs(band[:, :, 1].astype(int) - band[:, :, 2].astype(int)) < 8
        mid = (lum > 160) & (lum < 210)
        return float(lum.mean()), float((grey & mid).mean())

    top = arr[: max(h // 6, 1)]
    bot = arr[-max(h // 6, 1) :]
    left = arr[:, : max(w // 8, 1)]
    right = arr[:, -max(w // 8, 1) :]
    for name, band in (("top", top), ("bottom", bot), ("left", left), ("right", right)):
        lum, grey_share = band_stats(band)
        if grey_share > 0.55 and 165 < lum < 205:
            raise RuntimeError(
                f"{path.name}: {name} band looks washed-out grey "
                f"(lum={lum:.1f}, grey_share={grey_share:.2f})"
            )
    # Ink should exist in the lower third (axes / labels), not a blank slab.
    lower = arr[int(h * 0.62) :]
    if lower.std() < 8:
        raise RuntimeError(f"{path.name}: lower panel has almost no ink (clipped?)")
    print(f"  wrote {path.name}  {w}x{h}  ok")


def fig01_national_trends() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), constrained_layout=True)
    fig.suptitle(
        "Fifteen-year national trends in Canadian housing affordability, 2006–2021",
        fontsize=13,
        fontweight="bold",
        color=INK,
    )
    x = xpos(years)

    ax = axes[0, 0]
    ax.plot(x, [v / 1000 for v in inc_med], "o-", color=TEAL, lw=2.2, ms=7, label="Median")
    ax.fill_between(
        x,
        [v / 1000 for v in inc_p25],
        [v / 1000 for v in inc_p75],
        color=TEAL,
        alpha=0.15,
        label="25th–75th percentile",
    )
    ax.set_title("A. Median household income")
    ax.set_ylabel("Thousands of 2021 CAD")
    style_year_axis(ax)
    ax.set_ylim(0, 115)
    ax.annotate(
        "+33.5%",
        xy=(2, 46),
        xytext=(1.15, 72),
        arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1),
        color=TEAL,
        fontweight="bold",
        fontsize=10,
    )
    ax.legend(loc="upper left")

    ax = axes[0, 1]
    ax.plot(x, shel_med, "s-", color=ORANGE, lw=2.2, ms=7, label="Median")
    ax.fill_between(x, shel_p25, shel_p75, color=ORANGE, alpha=0.15, label="25th–75th percentile")
    ax.set_title("B. Median monthly shelter cost")
    ax.set_ylabel("2021 CAD per month")
    style_year_axis(ax)
    ax.set_ylim(0, 2500)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax.annotate(
        "+37.1%",
        xy=(2, 1400),
        xytext=(1.05, 2050),
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1),
        color=ORANGE,
        fontweight="bold",
        fontsize=10,
    )
    ax.legend(loc="upper left")

    ax = axes[1, 0]
    ax.plot(x, stir30, "o-", color=ORANGE, lw=2.2, ms=7, label="STIR > 30%")
    ax.plot(x, stir50, "s--", color=SLATE, lw=1.8, ms=6, label="STIR > 50%")
    ax.axhline(30, color="#888888", ls=":", lw=0.9)
    ax.set_title("C. Traditional affordability (STIR)")
    ax.set_ylabel("Share of records (%)")
    ax.set_xlabel("Census year")
    style_year_axis(ax)
    ax.set_ylim(0, 75)
    ax.legend(loc="upper right")

    ax = axes[1, 1]
    ax.plot(x, hardship, "D-", color=RED, lw=2.2, ms=7)
    ax.set_title("D. Housing hardship (residual income < MBM)")
    ax.set_ylabel("Share of records (%)")
    ax.set_xlabel("Census year")
    style_year_axis(ax)
    ax.set_ylim(0, 55)
    for xi, y in zip(x, hardship):
        ax.annotate(
            f"{y:.1f}%",
            (xi, y),
            textcoords="offset points",
            xytext=(0, 9),
            ha="center",
            fontsize=9,
            fontweight="bold",
            color=INK,
        )
    ax.text(
        0.03,
        0.07,
        "15-year change: −0.2 pp",
        transform=ax.transAxes,
        fontsize=9,
        color=SLATE,
    )

    savefig(fig, "fig01_national_trends")


def fig02_period_comparison() -> None:
    periods = ["2006–2011", "2011–2021"]
    inc_chg = [33.29, 0.17]
    shel_chg = [34.95, 1.63]
    # Published one-decimal values (Table 5 / results text). Bar heights use
    # the same rounded figures so the figure and tables do not disagree.
    hard_chg = [-4.1, 4.0]
    up = "#4C72B0"
    down = "#C44E52"

    fig, axes = plt.subplots(1, 3, figsize=(11.2, 4.8), constrained_layout=True)
    fig.suptitle(
        "Period changes in income, shelter cost, and housing hardship",
        fontsize=13,
        fontweight="bold",
        color=INK,
    )

    specs = [
        (inc_chg, "A. Median income", "Percent change", "{:+.1f}%", True),
        (shel_chg, "B. Median shelter cost", "Percent change", "{:+.1f}%", False),
        (hard_chg, "C. Housing hardship", "Percentage points", "{:+.1f} pp", False),
    ]
    for ax, (vals, title, ylab, fmt, higher_is_gain) in zip(axes, specs):
        colors = []
        for v in vals:
            if higher_is_gain:
                colors.append(up if v >= 0 else down)
            else:
                colors.append(down if v > 0 else up)
        bars = ax.bar(periods, vals, color=colors, edgecolor=INK, linewidth=0.4, width=0.58)
        ax.axhline(0, color=INK, lw=0.8)
        ax.set_title(title)
        ax.set_ylabel(ylab)
        ymax = max(abs(min(vals)), abs(max(vals))) * 1.55
        ax.set_ylim(-ymax, ymax)
        ax.set_xlabel("")
        for bar, v in zip(bars, vals):
            va = "bottom" if v >= 0 else "top"
            yoff = 0.04 * ymax if v >= 0 else -0.04 * ymax
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                v + yoff,
                fmt.format(v),
                ha="center",
                va=va,
                fontweight="bold",
                fontsize=10,
                color=INK,
            )

    fig.text(
        0.5,
        -0.02,
        "2006–2011 = crisis and recovery.  2011–2021 = expansion and COVID-19.  "
        "Blue = income up or hardship down.  Red = shelter up or hardship up.",
        ha="center",
        fontsize=8.5,
        color=SLATE,
    )
    savefig(fig, "fig02_period_comparison")


def fig03_tenure_divergence() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 5.2), constrained_layout=True)
    own_y = [2011, 2021]
    own_v = [31.41, 35.60]
    rent_y = [2006, 2011, 2021]
    rent_v = [38.03, 40.38, 43.64]

    ax.plot(xpos(own_y), own_v, "o-", color=TEAL, lw=2.3, ms=8, label="Owners")
    ax.plot(xpos(rent_y), rent_v, "s-", color=ORANGE, lw=2.3, ms=8, label="Renters")
    ax.plot([1, 1], [31.41, 40.38], color="#888888", ls=":", lw=1.0)
    ax.plot([2, 2], [35.60, 43.64], color="#888888", ls=":", lw=1.0)
    ax.annotate("9.0 pp gap", xy=(1.04, 35.9), ha="left", va="center", fontsize=9, color=SLATE)
    ax.annotate("8.0 pp gap", xy=(1.96, 39.6), ha="right", va="center", fontsize=9, color=SLATE)
    ax.set_title("Owner versus renter housing hardship, 2006–2021")
    ax.set_xlabel("Census year")
    ax.set_ylabel("Housing hardship rate (%)")
    style_year_axis(ax)
    ax.set_ylim(18, 52)
    ax.legend(loc="upper left")
    ax.text(
        0.02,
        0.045,
        "Owner hardship is unavailable for 2006 after tenure cleaning. Both groups worsened 2011–2021.",
        transform=ax.transAxes,
        fontsize=8.5,
        color=SLATE,
    )
    savefig(fig, "fig03_tenure_divergence")


def fig04_income_shelter_squeeze() -> None:
    inc_idx = [100.0, 133.29, 133.52]
    shel_idx = [100.0, 134.95, 137.15]
    x = xpos(years)

    fig, ax = plt.subplots(figsize=(8.8, 5.3), constrained_layout=True)
    ax.plot(x, inc_idx, "o-", color=TEAL, lw=2.3, ms=8, label="Median income (2021 CAD)")
    ax.plot(x, shel_idx, "s-", color=ORANGE, lw=2.3, ms=8, label="Median shelter cost (2021 CAD)")
    ax.axhline(100, color="#888888", ls="--", lw=1, label="2006 baseline = 100")
    ax.fill_between(x, inc_idx, shel_idx, color=RED, alpha=0.12, label="Affordability squeeze")
    ax.annotate(
        "133.5",
        (2, 133.52),
        textcoords="offset points",
        xytext=(-36, -16),
        color=TEAL,
        fontweight="bold",
    )
    ax.annotate(
        "137.1",
        (2, 137.15),
        textcoords="offset points",
        xytext=(8, 6),
        color=ORANGE,
        fontweight="bold",
    )
    ax.set_title("The income–shelter squeeze (indexed, 2006 = 100)")
    ax.set_xlabel("Census year")
    ax.set_ylabel("Index (2006 = 100)")
    style_year_axis(ax)
    ax.set_ylim(88, 158)
    ax.legend(loc="upper left")
    savefig(fig, "fig04_income_shelter_squeeze")


def fig05_summary_dashboard() -> None:
    fig = plt.figure(figsize=(11.2, 7.6), constrained_layout=True)
    fig.suptitle(
        "Summary dashboard: Canada’s housing squeeze, 2006–2021",
        fontsize=13,
        fontweight="bold",
        color=INK,
    )
    gs = fig.add_gridspec(2, 3, height_ratios=[1.15, 1.0])

    ax = fig.add_subplot(gs[0, :])
    colors = [ORANGE, TEAL, RED]
    bars = ax.bar(
        YEAR_LABELS,
        hardship,
        color=colors,
        edgecolor=INK,
        linewidth=0.4,
        width=0.52,
    )
    ax.set_title("Housing hardship rate (residual income below MBM)")
    ax.set_ylabel("Percent of records")
    ax.set_ylim(0, 52)
    ax.set_xlim(-0.55, 2.55)
    for bar, v, c in zip(bars, hardship, hardship_n):
        ax.annotate(
            f"{v:.1f}%\n(n={c:,})",
            (bar.get_x() + bar.get_width() / 2, v),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
            color=INK,
        )

    ax = fig.add_subplot(gs[1, 0])
    ax.plot(xpos(years), [v / 1000 for v in inc_med], "o-", color=TEAL, lw=2.2, ms=7)
    ax.set_title("Median income")
    ax.set_ylabel("Thousands of 2021 CAD")
    style_year_axis(ax)
    ax.set_ylim(0, 62)
    ax.annotate(
        "$46,000\n(+33.5%)",
        (2, 46),
        textcoords="offset points",
        xytext=(-8, 12),
        ha="right",
        fontsize=8,
        color=TEAL,
    )

    ax = fig.add_subplot(gs[1, 1])
    ax.plot(xpos(years), shel_med, "s-", color=ORANGE, lw=2.2, ms=7)
    ax.set_title("Median monthly shelter")
    ax.set_ylabel("2021 CAD")
    style_year_axis(ax)
    ax.set_ylim(0, 1900)
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax.annotate(
        "$1,400\n(+37.1%)",
        (2, 1400),
        textcoords="offset points",
        xytext=(-8, 12),
        ha="right",
        fontsize=8,
        color=ORANGE,
    )

    ax = fig.add_subplot(gs[1, 2])
    ax.plot([1, 2], [31.41, 35.60], "o-", color=TEAL, lw=2.2, ms=7, label="Owners")
    ax.plot([1, 2], [40.38, 43.64], "s-", color=ORANGE, lw=2.2, ms=7, label="Renters")
    ax.set_title("Hardship by tenure")
    ax.set_ylabel("Percent")
    style_year_axis(ax)
    ax.set_ylim(18, 55)
    ax.legend(loc="upper left", fontsize=8)

    savefig(fig, "fig05_summary_dashboard")


def write_csv(name: str, df: pd.DataFrame) -> None:
    path = TAB_DIR / name
    df.to_csv(path, index=False)
    print(f"  wrote {path}")


def write_tex_table(name: str, caption: str, label: str, header: list[str], rows: list[list[str]], notes: str) -> None:
    colspec = "l" + "r" * (len(header) - 1)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        rf"\caption{{{caption}}}",
        rf"\label{{{label}}}",
        r"\small",
        rf"\begin{{tabular}}{{{colspec}}}",
        r"\toprule",
        " & ".join(header) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(row) + r" \\")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            rf"\par\smallskip{{\footnotesize {notes}}}",
            r"\end{table}",
            "",
        ]
    )
    path = TAB_DIR / name
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {path}")


def write_tables() -> None:
    t1 = pd.DataFrame(
        {
            "characteristic": [
                "Valid sample size (n)",
                "Median income (2021 CAD)",
                "Income 25th percentile (2021 CAD)",
                "Income 75th percentile (2021 CAD)",
                "Median monthly shelter (2021 CAD)",
                "Shelter 25th percentile (2021 CAD)",
                "Shelter 75th percentile (2021 CAD)",
                "Mean monthly shelter (2021 CAD)",
                "STIR > 30% (%)",
                "STIR > 50% (%)",
                "Housing hardship rate (%)",
                "Households in hardship (n)",
            ],
            "year_2006": [78056, 34452, 17864, 70180, 1021, 766, 1531, 1182, 57.0, 35.8, 38.0, 29681],
            "year_2011": [341030, 45920, 22960, 101024, 1378, 804, 2181, 1573, 52.2, 33.6, 33.9, 115459],
            "year_2021": [358621, 46000, 25000, 93000, 1400, 800, 2129, 1598, 50.8, 31.5, 37.9, 135740],
        }
    )
    write_csv("table01_sample_characteristics.csv", t1)
    write_tex_table(
        "table01_sample_characteristics.tex",
        "Sample characteristics by Census year (inflation-adjusted to 2021 CAD)",
        "tab:sample",
        ["Characteristic", "2006", "2011", "2021"],
        [
            ["Valid sample size ($n$)", "78,056", "341,030", "358,621"],
            ["Median income (2021 CAD)", "\\$34,452", "\\$45,920", "\\$46,000"],
            ["Income 25th percentile", "\\$17,864", "\\$22,960", "\\$25,000"],
            ["Income 75th percentile", "\\$70,180", "\\$101,024", "\\$93,000"],
            ["Median monthly shelter", "\\$1,021", "\\$1,378", "\\$1,400"],
            ["Shelter 25th percentile", "\\$766", "\\$804", "\\$800"],
            ["Shelter 75th percentile", "\\$1,531", "\\$2,181", "\\$2,129"],
            ["STIR $>$ 30\\%", "57.0\\%", "52.2\\%", "50.8\\%"],
            ["STIR $>$ 50\\%", "35.8\\%", "33.6\\%", "31.5\\%"],
            ["Housing hardship rate", "38.0\\%", "33.9\\%", "37.9\\%"],
            ["Households in hardship ($n$)", "29,681", "115,459", "135,740"],
        ],
        r"Notes: All dollar values converted to 2021 constant dollars using CPI multipliers "
        r"(2006 $\times$ 1.276; 2011 $\times$ 1.148). Census 2016 is excluded because valid-record "
        r"retention was 9.4\%. Estimates are unweighted person-records from hierarchical PUMF files. "
        r"Median income is reported instead of the mean because hierarchical PUMF files produce "
        r"inflated household-level means.",
    )

    t2 = pd.DataFrame(
        {
            "year": [2011, 2021],
            "owner_hardship_pct": [31.4, 35.6],
            "renter_hardship_pct": [40.4, 43.6],
            "gap_pp": [9.0, 8.0],
        }
    )
    write_csv("table02_tenure_hardship.csv", t2)
    write_tex_table(
        "table02_tenure_hardship.tex",
        "Housing hardship by tenure, 2011 and 2021",
        "tab:tenure",
        ["Year", "Owner hardship", "Renter hardship", "Gap"],
        [
            ["2011", "31.4\\%", "40.4\\%", "9.0 pp"],
            ["2021", "35.6\\%", "43.6\\%", "8.0 pp"],
            ["Change", "+4.2 pp", "+3.2 pp", "$-$1.0 pp"],
        ],
        r"Notes: Owner hardship is unavailable for 2006 because tenure coding in that PUMF file "
        r"did not support a clean owner/renter split after cleaning. The gap narrowed because "
        r"owners deteriorated toward renter rates, not because renters improved.",
    )

    t3 = pd.DataFrame(
        {
            "year": [2006, 2011, 2021],
            "income_index_2006eq100": [100.0, 133.3, 133.5],
            "shelter_index_2006eq100": [100.0, 135.0, 137.1],
            "index_gap": [0.0, 1.7, 3.6],
        }
    )
    write_csv("table03_indexed_squeeze.csv", t3)
    write_tex_table(
        "table03_indexed_squeeze.tex",
        "Income versus shelter cost, indexed to 2006 = 100",
        "tab:squeeze",
        ["Year", "Income index", "Shelter index", "Gap"],
        [
            ["2006", "100.0", "100.0", "0.0"],
            ["2011", "133.3", "135.0", "1.7"],
            ["2021", "133.5", "137.1", "3.6"],
        ],
        "Notes: Index = (year median / 2006 median) $\\times$ 100. Both series are in 2021 CAD. "
        "The 3.6-point 2021 gap equals about \\$38 per month (\\$456 per year) at the 2021 median.",
    )

    t4 = pd.DataFrame(
        {
            "metric": [
                "Median income (2021 CAD)",
                "Median monthly shelter (2021 CAD)",
                "STIR > 30% (%)",
                "Housing hardship (%)",
                "Renter hardship (%)",
                "Owner hardship (%)",
            ],
            "year_2006": ["34452", "1021", "57.0", "38.0", "38.0", "n/a"],
            "year_2021": ["46000", "1400", "50.8", "37.9", "43.6", "35.6"],
            "change": ["+33.5%", "+37.1%", "-6.2 pp", "-0.1 pp", "+5.6 pp", "n/a"],
        }
    )
    write_csv("table04_summary_2006_2021.csv", t4)
    write_tex_table(
        "table04_summary_2006_2021.tex",
        "Summary statistics, 2006 versus 2021",
        "tab:summary",
        ["Metric", "2006", "2021", "15-year change"],
        [
            ["Median income (2021 CAD)", "\\$34,452", "\\$46,000", "+33.5\\%"],
            ["Median monthly shelter", "\\$1,021", "\\$1,400", "+37.1\\%"],
            ["STIR $>$ 30\\%", "57.0\\%", "50.8\\%", "$-$6.2 pp"],
            ["Housing hardship", "38.0\\%", "37.9\\%", "$-$0.1 pp"],
            ["Renter hardship", "38.0\\%", "43.6\\%", "+5.6 pp"],
            ["Owner hardship", "n/a", "35.6\\%", "n/a"],
        ],
        r"Notes: Owner hardship is not available for 2006. STIR improved while residual-income "
        r"hardship did not, which is the central measurement result of this paper.",
    )

    t5 = pd.DataFrame(
        {
            "period": ["2006–2011", "2011–2021"],
            "income_pct_change": [33.3, 0.2],
            "shelter_pct_change": [35.0, 1.6],
            "hardship_pp_change": [-4.1, 4.0],
        }
    )
    write_csv("table05_period_changes.csv", t5)
    write_tex_table(
        "table05_period_changes.tex",
        "Period-over-period changes in income, shelter costs, and hardship",
        "tab:periods",
        ["Period", "Income change", "Shelter change", "Hardship change"],
        [
            ["2006--2011 (crisis + recovery)", "+33.3\\%", "+35.0\\%", "$-$4.1 pp"],
            ["2011--2021 (expansion + COVID)", "+0.2\\%", "+1.6\\%", "+4.0 pp"],
        ],
        r"Notes: Income and shelter changes are percent changes in inflation-adjusted medians. "
        r"Hardship change is in percentage points. The later period erased the earlier improvement.",
    )


def main() -> None:
    print("Generating figures...")
    fig01_national_trends()
    fig02_period_comparison()
    fig03_tenure_divergence()
    fig04_income_shelter_squeeze()
    fig05_summary_dashboard()
    print("Generating tables...")
    write_tables()
    print("Done.")


if __name__ == "__main__":
    main()
