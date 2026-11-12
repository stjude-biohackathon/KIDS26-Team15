#!/usr/bin/env python3
"""Compare legacy vs Daedalus resource usage with biohackathon vs post-hackathon ROI scopes."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.roi_scope import (  # noqa: E402
    BIOHACKATHON_PAIRED_MODULES,
    POSTHACKATHON_DAEDALUS_ONLY_MODULES,
    POSTHACKATHON_PAIRED_MODULES,
    POSTHACKATHON_QC_ALIGN_MODULES,
)

CORE_HOUR_USD = 0.024


def fnum(value: str | None) -> float | None:
    if value is None or str(value).strip() in ("", "NA"):
        return None
    return float(value)


def fmt_num(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}f}"


def fmt_hours(seconds: float | None) -> str:
    if seconds is None:
        return "NA"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    return f"{h}h {m}m"


def load_legacy(path: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("legacy_run_status") != "DONE":
                continue
            out[row["module"]] = row
    return out


def load_daedalus(path: Path) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[row["module"]] = row
    return out


def core_hours(row: dict[str, str] | None) -> float:
    if not row:
        return 0.0
    wall = fnum(row.get("wall_time_sec"))
    cpu = fnum(row.get("requested_cpu"))
    if wall is None or cpu is None:
        return 0.0
    return wall * cpu / 3600


def sum_core(modules: tuple[str, ...], data: dict[str, dict[str, str]]) -> float:
    return sum(core_hours(data.get(m)) for m in modules)


def module_row_table(
    lines: list[str],
    modules: tuple[str, ...],
    legacy: dict[str, dict[str, str]],
    daedalus: dict[str, dict[str, str]],
    *,
    legacy_only_ok: bool = False,
    daedalus_only_ok: bool = False,
) -> tuple[float, float]:
    lines.append(
        "| Module | Legacy CPUs | Daedalus CPUs | Legacy req mem (GB/slot) | Daedalus req mem | "
        "Legacy avg mem (GB) | Daedalus avg mem | Legacy wall | Daedalus wall | "
        "Legacy core-hrs | Daedalus core-hrs |"
    )
    lines.append(
        "|--------|-------------|---------------|---------------------------|------------------|"
        "--------------------|------------------|-------------|---------------|"
        "---------------|-------------------|"
    )
    sum_l = 0.0
    sum_d = 0.0
    for mod in modules:
        lr = legacy.get(mod) if not daedalus_only_ok or mod in legacy else None
        dr = daedalus.get(mod) if not legacy_only_ok or mod in daedalus else None
        if mod == "biological_validation":
            lines.append(
                f"| {mod} | NA | NA | NA | NA | NA | NA | NA | NA | "
                f"0 (not run) | 0 (automated; no LSF row in CSV) |"
            )
            continue
        l_ch = core_hours(lr) if lr else 0.0
        d_ch = core_hours(dr) if dr else 0.0
        sum_l += l_ch
        sum_d += d_ch
        def dval(key: str, digits: int = 2) -> str:
            if dr and key in dr:
                return fmt_num(fnum(dr[key]), digits)
            return "NA"

        def dwall() -> str:
            return fmt_hours(fnum(dr["wall_time_sec"])) if dr else "NA"

        lines.append(
            f"| {mod} | "
            f"{fmt_num(fnum(lr['requested_cpu']) if lr else None, 0)} | "
            f"{dval('requested_cpu', 0)} | "
            f"{fmt_num(fnum(lr['requested_memory_gb']) if lr else None)} | "
            f"{dval('requested_memory_gb')} | "
            f"{fmt_num(fnum(lr['actual_avg_memory_gb']) if lr else None)} | "
            f"{dval('actual_avg_memory_gb')} | "
            f"{fmt_hours(fnum(lr['wall_time_sec']) if lr else None)} | "
            f"{dwall()} | "
            f"{fmt_num(l_ch)} | {fmt_num(d_ch) if d_ch else 'NA'} |"
        )
    lines.append("")
    return sum_l, sum_d


def totals_block(lines: list[str], title: str, sum_l: float, sum_d: float) -> None:
    lines.append(f"### {title}")
    lines.append("")
    lines.append("| Metric | Legacy | Daedalus |")
    lines.append("|--------|--------|----------|")
    lines.append(f"| Allocated core-hours | {sum_l:.2f} | {sum_d:.2f} |")
    lines.append(f"| Est. HPC cost (@ ${CORE_HOUR_USD}/core-hr) | ${sum_l * CORE_HOUR_USD:.2f} | ${sum_d * CORE_HOUR_USD:.2f} |")
    if sum_l > 0 and sum_d > 0:
        pct = 100 * (1 - sum_d / sum_l)
        lines.append(f"| Core-hour change (Daedalus vs legacy) | — | **{pct:.1f}%** vs legacy |")
    lines.append("")


def build_report(legacy_path: Path, daedalus_path: Path) -> str:
    legacy = load_legacy(legacy_path)
    daedalus = load_daedalus(daedalus_path)
    lines: list[str] = []

    lines.append("# ROI — Biohackathon vs Post-Hackathon (Victoria Knockout)")
    lines.append("")
    lines.append("**Cohort:** Victoria Knockout (4 samples, ~27k cells)")
    lines.append("")
    lines.append("| Phase | Legacy vs Daedalus test scope |")
    lines.append("|-------|----------------------------------|")
    lines.append(
        "| **Biohackathon** | **2 modules:** `upstream`, `integrative` |"
    )
    lines.append(
        "| **Post-hackathon** | **5 modules** (`upstream`, `integrative`, `cluster`, `cell_types`, `rshiny`) "
        "+ **FastQC & Cell Ranger** (both workflow types on shared project data) "
        "+ **Daedalus-only:** `de_go`, `project_updates`, **`biological_validation`** |"
    )
    lines.append("")
    lines.append("| Data file | Role |")
    lines.append("|-----------|------|")
    lines.append(f"| `{legacy_path.name}` | Legacy SNAP LSF export (KIDS26) |")
    lines.append(f"| `{daedalus_path.name}` | Daedalus/Sprocket post-hackathon downstream run |")
    lines.append("")
    missing_daedalus_only = [
        m
        for m in POSTHACKATHON_DAEDALUS_ONLY_MODULES
        if m != "biological_validation" and m not in daedalus
    ]
    if missing_daedalus_only:
        lines.append(
            "> **Note:** This Daedalus `resource_usage` export has no rows for "
            + ", ".join(f"`{m}`" for m in missing_daedalus_only)
            + " (those modules were not in this Sprocket run). Daedalus combined HPC in §2 therefore "
            "matches the five paired modules only — not five paired + `de_go` + `project_updates`."
        )
        lines.append("")

    # --- Biohackathon ---
    lines.append("## 1. Biohackathon ROI (2 modules: legacy vs Daedalus)")
    lines.append("")
    bh_l, bh_d = module_row_table(
        lines, BIOHACKATHON_PAIRED_MODULES, legacy, daedalus
    )
    totals_block(lines, "Biohackathon totals (upstream + integrative only)", bh_l, bh_d)

    # --- Post-hackathon paired ---
    lines.append("## 2. Post-hackathon ROI")
    lines.append("")
    lines.append("### 2a. Five modules — legacy vs Daedalus")
    lines.append("")
    ph_l, ph_d = module_row_table(
        lines, POSTHACKATHON_PAIRED_MODULES, legacy, daedalus
    )
    totals_block(lines, "Post-hackathon paired-module totals (5 modules)", ph_l, ph_d)

    lines.append("### 2b. FastQC & Cell Ranger (both pipelines)")
    lines.append("")
    lines.append(
        "Both legacy and Daedalus Victoria Knockout projects use the same **FastQC** and **Cell Ranger** "
        "outputs under `analyses/fastqc-analysis` and `analyses/cellranger-analysis`. "
        "HPC is captured in the **legacy** export; Daedalus downstream consumes these results without a separate row in the Daedalus CSV."
    )
    lines.append("")
    qc_l, _ = module_row_table(
        lines,
        POSTHACKATHON_QC_ALIGN_MODULES,
        legacy,
        daedalus,
        daedalus_only_ok=True,
    )
    lines.append(
        f"*Legacy QC/align core-hours (included in post-hackathon legacy HPC footprint):* **{qc_l:.2f}** "
        f"(~${qc_l * CORE_HOUR_USD:.2f})"
    )
    lines.append("")

    lines.append("### 2c. Daedalus-only downstream (post-hackathon)")
    lines.append("")
    daedalus_extra = tuple(m for m in POSTHACKATHON_DAEDALUS_ONLY_MODULES if m != "biological_validation")
    _, extra_d = module_row_table(
        lines,
        daedalus_extra,
        legacy,
        daedalus,
        legacy_only_ok=True,
    )
    lines.append("| Module | Legacy | Daedalus | Notes |")
    lines.append("|--------|--------|----------|-------|")
    lines.append(
        "| biological_validation | Not run | **Enabled** | Automated checks in Daedalus/Sprocket; no LSF module row in resource_usage CSV |"
    )
    lines.append("")

    post_legacy_total = ph_l + qc_l
    post_daedalus_total = ph_d + extra_d
    totals_block(
        lines,
        "Post-hackathon combined HPC footprint (legacy: 5 paired + fastqc + cellranger; "
        "Daedalus: 5 paired + de_go + project_updates)",
        post_legacy_total,
        post_daedalus_total,
    )

    lines.append("## 3. Findings (scoped)")
    lines.append("")
    lines.append(
        f"1. **Biohackathon (2 modules):** Daedalus used **{bh_d:.1f}** vs legacy **{bh_l:.1f}** allocated core-hours "
        f"on upstream + integrative (~${bh_d * CORE_HOUR_USD:.2f} vs ~${bh_l * CORE_HOUR_USD:.2f} HPC)."
    )
    lines.append(
        f"2. **Post-hackathon (5 paired modules):** Daedalus **{ph_d:.1f}** vs legacy **{ph_l:.1f}** core-hours "
        "on the expanded module set (cluster, cell_types, rshiny added to the comparison)."
    )
    lines.append(
        f"3. **Shared QC/align:** Add **{qc_l:.1f}** legacy core-hours for FastQC + Cell Ranger when costing the full legacy SNAP path."
    )
    lines.append(
        "4. **Biological validation:** Post-hackathon Daedalus adds automated validation (no legacy equivalent in this ROI export)."
    )
    lines.append(
        "5. **Analyst time dominates ROI** — see `docs/data-analyst-time.md` and scenario charts in `output/results-posthackathon/`."
    )
    lines.append("")
    lines.append("## Plots")
    lines.append("")
    lines.append(
        "Charts use the **post-hackathon five-module** scope unless labeled otherwise: "
        "`output/results-posthackathon/` — `combined_utilization_time_comparison.png` (2×2 summary), "
        "or `resource_utilization_comparison.png` + `computational_time_comparison.png`; "
        "`memory_requested_vs_used.png`, `cost_improvement_pct.png` "
        "(regenerate with `scripts/generate_posthackathon_plots.py`)."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--legacy",
        type=Path,
        default=Path("../input/resource_usage_KIDS26-Victoria-Knockout_2026-11-05.csv"),
    )
    parser.add_argument(
        "--daedalus",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent.parent
        / "analyses"
        / "sc-rna-seq-snap-daedalus-Victoria-Knockout"
        / "daedalus-post-hackathon"
        / "resource_usage_2026-11-05_220340654817588.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("../reports/P1-ROI-Biohackathon-vs-Post-Hackathon-Comparison.md"),
    )
    args = parser.parse_args()
    args.legacy = args.legacy.resolve()
    args.daedalus = args.daedalus.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_report(args.legacy, args.daedalus), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
