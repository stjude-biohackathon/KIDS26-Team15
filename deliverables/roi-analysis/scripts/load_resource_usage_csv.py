"""Load legacy (KIDS26) and Daedalus resource_usage CSV exports into comparable metric rows."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from scripts.roi_scope import (
    BIOHACKATHON_PAIRED_MODULES,
    POSTHACKATHON_PAIRED_MODULES,
)

# Post-hackathon bar charts: five legacy vs Daedalus modules.
COMPARE_MODULES = list(POSTHACKATHON_PAIRED_MODULES)


def _f(value: Any) -> float | None:
    if value is None:
        return None
    s = str(value).strip()
    if s in ("", "NA"):
        return None
    return float(s)


def _metrics_from_row(row: dict[str, str]) -> dict[str, float] | None:
    cpu = _f(row.get("requested_cpu"))
    mem_slot = _f(row.get("requested_memory_gb"))
    wall = _f(row.get("wall_time_sec"))
    cpu_time = _f(row.get("cpu_time_sec"))
    avg_mem = _f(row.get("actual_avg_memory_gb"))
    max_mem = _f(row.get("actual_max_memory_gb"))
    if cpu is None or mem_slot is None or wall is None:
        return None
    total_req = cpu * mem_slot
    mem_util = (avg_mem / total_req * 100) if avg_mem is not None and total_req > 0 else None
    cpu_util = (
        (cpu_time / (wall * cpu) * 100) if cpu_time is not None and wall > 0 and cpu > 0 else None
    )
    cpu_util_csv = _f(row.get("cpu_avg_efficiency_pct"))
    if cpu_util is None and cpu_util_csv is not None:
        cpu_util = cpu_util_csv
    mem_util_csv = _f(row.get("memory_utilization_pct"))
    return {
        "cores": cpu,
        "mem_slot_gb": mem_slot,
        "wall_h": wall / 3600,
        "cpu_time_s": cpu_time or 0.0,
        "avg_mem_gb": avg_mem or 0.0,
        "max_mem_gb": max_mem or 0.0,
        "total_req_mem_gb": total_req,
        "memory_util_pct": mem_util if mem_util is not None else (mem_util_csv or 0.0),
        "cpu_util_pct": cpu_util if cpu_util is not None else 0.0,
        "core_hours": wall * cpu / 3600,
    }


def load_legacy_csv(path: Path) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("legacy_run_status") != "DONE":
                continue
            mod = row["module"]
            m = _metrics_from_row(row)
            if m:
                out[mod] = m
    return out


def load_daedalus_csv(path: Path) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            mod = row["module"]
            m = _metrics_from_row(row)
            if m:
                out[mod] = m
    return out
