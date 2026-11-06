#!/usr/bin/env python3
"""Generate ROI plots from KIDS26 legacy vs post-hackathon Daedalus resource_usage CSVs."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.load_resource_usage_csv import (  # noqa: E402
    COMPARE_MODULES,
    load_daedalus_csv,
    load_legacy_csv,
)
from scripts.roi_scope import (  # noqa: E402
    POSTHACKATHON_DAEDALUS_ONLY_MODULES,
    POSTHACKATHON_QC_ALIGN_MODULES,
)

# Requested vs used memory: paired downstream modules only (exclude QC/align and Daedalus-only extras).
MEMORY_REQUESTED_VS_USED_MODULES = tuple(COMPARE_MODULES)

LEGACY_CSV = ROOT / "input/resource_usage_KIDS26-Victoria-Knockout_2026-11-05.csv"
_TEAM15_ROOT = ROOT.parent.parent  # roi-analysis → deliverables → KIDS26-Team15
DAEDALUS_CSV = (
    _TEAM15_ROOT
    / "analyses"
    / "sc-rna-seq-snap-daedalus-Victoria-Knockout"
    / "daedalus-post-hackathon"
    / "resource_usage_2026-11-05_220340654817588.csv"
)
ROI_SCENARIOS = ROOT / "docs/roi_scenarios.csv"
OUT = ROOT / "output/results-posthackathon"

CB_LEGACY = "#DC267F"
CB_DAEDALUS = "#648FFF"
CB_REQUEST = "#785EF0"
CB_USED = "#FE6100"


def _polish(ax, title: str) -> None:
    ax.set_title(title, fontsize=13, fontweight="bold", pad=14)
    for spine in ax.spines.values():
        spine.set_color("black")
        spine.set_linewidth(1.0)
        spine.set_visible(True)
    ax.grid(False)
    leg = ax.get_legend()
    if leg:
        leg.set_framealpha(0.9)
        for t in leg.get_texts():
            t.set_fontsize(10)


def _annotate_bar_heights(ax, bars, *, fmt: str) -> None:
    for bar in bars:
        h = bar.get_height()
        if h <= 0:
            continue
        ax.annotate(
            fmt.format(h),
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )


def _plot_memory_requested_vs_used_panel(
    ax,
    mod: str,
    legacy: dict,
    daedalus: dict,
    *,
    show_legend: bool,
) -> None:
    """Legacy (left) then Daedalus; requested vs avg used grouped like biohackathon v2 notebook."""
    labels = ["Legacy", "Daedalus"]
    xs = range(len(labels))
    w = 0.35
    req = [
        legacy[mod]["total_req_mem_gb"] if mod in legacy else 0.0,
        daedalus[mod]["total_req_mem_gb"] if mod in daedalus else 0.0,
    ]
    avg = [
        legacy[mod]["avg_mem_gb"] if mod in legacy else 0.0,
        daedalus[mod]["avg_mem_gb"] if mod in daedalus else 0.0,
    ]
    bars_req = ax.bar(
        [i - w / 2 for i in xs],
        req,
        w,
        label="Requested",
        color=CB_REQUEST,
        alpha=0.88,
        zorder=3,
    )
    bars_avg = ax.bar(
        [i + w / 2 for i in xs],
        avg,
        w,
        label="Avg used",
        color=CB_USED,
        alpha=0.88,
        zorder=3,
    )
    ax.set_xticks(list(xs))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Memory (GB)")
    title = mod.replace("_", " ").title()
    _polish(ax, f"{title}: requested vs avg used")
    ymax = max(max(req, default=0), max(avg, default=0))
    ax.set_ylim(0, ymax * 1.32 if ymax else 1)
    _annotate_bar_heights(ax, bars_req, fmt="{:.0f} GB")
    _annotate_bar_heights(ax, bars_avg, fmt="{:.1f} GB")
    if show_legend:
        ax.legend(loc="upper right", framealpha=0.9, fontsize=10)


def _plot_utilization_panel(
    ax,
    modules: list[str],
    legacy_vals: list[float],
    daedalus_vals: list[float],
    *,
    ylabel: str,
    title: str,
    show_legend: bool,
    width: float = 0.38,
) -> None:
    x = range(len(modules))
    ax.bar(
        [i - width / 2 for i in x],
        legacy_vals,
        width,
        label="Legacy",
        color=CB_LEGACY,
        alpha=0.88,
    )
    ax.bar(
        [i + width / 2 for i in x],
        daedalus_vals,
        width,
        label="Daedalus",
        color=CB_DAEDALUS,
        alpha=0.88,
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(modules, rotation=25, ha="right")
    ax.set_ylabel(ylabel)
    _polish(ax, title)
    if show_legend:
        ax.legend(loc="upper right", framealpha=0.9, fontsize=10)
    ymax = max(max(legacy_vals, default=0), max(daedalus_vals, default=0))
    ax.set_ylim(0, ymax * 1.25 if ymax else 1)


def _plot_legacy_vs_daedalus_cost_panel(
    ax,
    x_s: range,
    legacy_cost,
    daedalus_cost,
    pct_reduction,
    *,
    ylabel: str,
    title: str,
    value_fmt: str,
    show_legend: bool,
) -> None:
    """Side-by-side Legacy (left) vs Daedalus (right) $/run; annotate % lower on Daedalus bars."""
    width = 0.38
    bars_l = ax.bar(
        [i - width / 2 for i in x_s],
        legacy_cost,
        width,
        label="Legacy",
        color=CB_LEGACY,
        alpha=0.88,
        zorder=3,
    )
    bars_d = ax.bar(
        [i + width / 2 for i in x_s],
        daedalus_cost,
        width,
        label="Daedalus",
        color=CB_DAEDALUS,
        alpha=0.88,
        zorder=3,
    )
    ax.set_ylabel(ylabel)
    _polish(ax, title)
    if show_legend:
        ax.legend(loc="upper right", framealpha=0.9, fontsize=10)
    ymax = max(float(legacy_cost.max()), float(daedalus_cost.max()), 0.01)
    ax.set_ylim(0, ymax * 1.35)
    _annotate_bar_heights(ax, bars_l, fmt=value_fmt)
    _annotate_bar_heights(ax, bars_d, fmt=value_fmt)
    for i, bar in enumerate(bars_d):
        pct = float(pct_reduction.iloc[i])
        ax.annotate(
            f"−{pct:.1f}% vs Legacy",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 22),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#333333",
        )


def main() -> None:
    plt.style.use("ggplot")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["font.size"] = 12
    OUT.mkdir(parents=True, exist_ok=True)

    legacy = load_legacy_csv(LEGACY_CSV)
    daedalus = load_daedalus_csv(DAEDALUS_CSV)
    modules = [m for m in COMPARE_MODULES if m in legacy or m in daedalus]

    legacy_mem = [legacy[m]["memory_util_pct"] if m in legacy else 0 for m in modules]
    daed_mem = [daedalus[m]["memory_util_pct"] if m in daedalus else 0 for m in modules]
    legacy_cpu = [legacy[m]["cpu_util_pct"] if m in legacy else 0 for m in modules]
    daed_cpu = [daedalus[m]["cpu_util_pct"] if m in daedalus else 0 for m in modules]

    width = 0.38
    util_fig_w = max(10, len(modules) * 1.2)

    # 1 — Memory + CPU utilization (one row, two panels)
    fig, axes = plt.subplots(1, 2, figsize=(util_fig_w * 1.55, 5.5))
    _plot_utilization_panel(
        axes[0],
        modules,
        legacy_mem,
        daed_mem,
        ylabel="Memory utilization (%)\n(avg used / total requested)",
        title="Memory utilization",
        show_legend=True,
        width=width,
    )
    _plot_utilization_panel(
        axes[1],
        modules,
        legacy_cpu,
        daed_cpu,
        ylabel="CPU utilization (%)",
        title="CPU utilization",
        show_legend=False,
        width=width,
    )
    fig.suptitle(
        "Post-hackathon scope (5 modules, Victoria Knockout) — Legacy vs Daedalus",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96), pad=1.2)
    fig.savefig(OUT / "resource_utilization_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # 2 — Requested vs avg memory (paired downstream modules only)
    memory_modules = [
        m for m in MEMORY_REQUESTED_VS_USED_MODULES if m in legacy or m in daedalus
    ]
    ncols = 3
    nrows = math.ceil(len(memory_modules) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4.8 * nrows))
    axes_flat = axes.flatten() if len(memory_modules) > 1 else [axes]
    for idx, mod in enumerate(memory_modules):
        _plot_memory_requested_vs_used_panel(
            axes_flat[idx],
            mod,
            legacy,
            daedalus,
            show_legend=(idx == 0),
        )
    for ax in axes_flat[len(memory_modules) :]:
        ax.set_visible(False)
    fig.suptitle(
        "Memory requested vs avg used — paired downstream modules (Victoria Knockout)",
        fontsize=14,
        fontweight="bold",
        y=1.01,
    )
    fig.tight_layout(pad=1.5)
    fig.savefig(OUT / "memory_requested_vs_used.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    scenarios_df = pd.read_csv(ROI_SCENARIOS)
    scenarios_df["legacy_analyst_cost"] = (
        scenarios_df["legacy_analyst_hours_per_run"] * scenarios_df["analyst_hourly_rate_usd"]
    )
    scenarios_df["daedalus_analyst_cost"] = (
        scenarios_df["daedalus_analyst_hours_per_run"] * scenarios_df["analyst_hourly_rate_usd"]
    )

    x_s = range(len(scenarios_df))

    def _sum(mods: tuple[str, ...], data: dict) -> float:
        return sum(data[m]["core_hours"] for m in mods if m in data)

    legacy_core_h = _sum(POSTHACKATHON_QC_ALIGN_MODULES, legacy) + _sum(
        tuple(COMPARE_MODULES), legacy
    )
    daedalus_only = tuple(m for m in POSTHACKATHON_DAEDALUS_ONLY_MODULES if m != "biological_validation")
    daedalus_core_h = _sum(tuple(COMPARE_MODULES), daedalus) + _sum(daedalus_only, daedalus)

    legacy_hpc = legacy_core_h * scenarios_df["hpc_cpu_hour_rate_usd"]
    daed_hpc = daedalus_core_h * scenarios_df["hpc_cpu_hour_rate_usd"]

    # 5 — Legacy vs Daedalus: HPC $, analyst hours, analyst $ (single scenario summary figure)
    scenarios_df["legacy_hpc_cost"] = legacy_hpc
    scenarios_df["daedalus_hpc_cost"] = daed_hpc
    scenarios_df["analyst_hours_pct_reduction"] = (
        (
            scenarios_df["legacy_analyst_hours_per_run"]
            - scenarios_df["daedalus_analyst_hours_per_run"]
        )
        / scenarios_df["legacy_analyst_hours_per_run"]
        * 100
    )
    scenarios_df["analyst_pct_reduction"] = (
        (scenarios_df["legacy_analyst_cost"] - scenarios_df["daedalus_analyst_cost"])
        / scenarios_df["legacy_analyst_cost"]
        * 100
    )
    scenarios_df["hpc_pct_reduction"] = (
        (scenarios_df["legacy_hpc_cost"] - scenarios_df["daedalus_hpc_cost"])
        / scenarios_df["legacy_hpc_cost"]
        * 100
    )

    scenario_labels = scenarios_df["scenario"].str.title()
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    _plot_legacy_vs_daedalus_cost_panel(
        axes[0],
        x_s,
        scenarios_df["legacy_hpc_cost"],
        scenarios_df["daedalus_hpc_cost"],
        scenarios_df["hpc_pct_reduction"],
        ylabel="HPC cost ($) / run",
        title=(
            f"HPC $/run ({legacy_core_h:.0f} vs {daedalus_core_h:.0f} core-hrs)"
        ),
        value_fmt="${:.2f}",
        show_legend=True,
    )
    _plot_legacy_vs_daedalus_cost_panel(
        axes[1],
        x_s,
        scenarios_df["legacy_analyst_hours_per_run"],
        scenarios_df["daedalus_analyst_hours_per_run"],
        scenarios_df["analyst_hours_pct_reduction"],
        ylabel="Analyst hours / run",
        title="Analyst hours / run",
        value_fmt="{:.1f} h",
        show_legend=False,
    )
    _plot_legacy_vs_daedalus_cost_panel(
        axes[2],
        x_s,
        scenarios_df["legacy_analyst_cost"],
        scenarios_df["daedalus_analyst_cost"],
        scenarios_df["analyst_pct_reduction"],
        ylabel="Analyst cost ($) / run",
        title="Analyst cost $/run (@ $48.08/hr)",
        value_fmt="${:.0f}",
        show_legend=False,
    )
    for ax in axes:
        ax.set_xticks(list(x_s))
        ax.set_xticklabels(scenario_labels)
    fig.suptitle(
        "Legacy vs Daedalus — cost per run (low / expected / high scenarios)",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96), pad=1.2)
    fig.savefig(OUT / "cost_improvement_pct.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    summary = OUT / "comparison_summary.csv"
    rows = []
    for mod in modules:
        rows.append(
            {
                "module": mod,
                "legacy_memory_util_pct": legacy.get(mod, {}).get("memory_util_pct"),
                "daedalus_memory_util_pct": daedalus.get(mod, {}).get("memory_util_pct"),
                "legacy_cpu_util_pct": legacy.get(mod, {}).get("cpu_util_pct"),
                "daedalus_cpu_util_pct": daedalus.get(mod, {}).get("cpu_util_pct"),
                "legacy_core_hours": legacy.get(mod, {}).get("core_hours"),
                "daedalus_core_hours": daedalus.get(mod, {}).get("core_hours"),
            }
        )
    pd.DataFrame(rows).to_csv(summary, index=False)
    print(f"Wrote plots to {OUT}")
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main()
