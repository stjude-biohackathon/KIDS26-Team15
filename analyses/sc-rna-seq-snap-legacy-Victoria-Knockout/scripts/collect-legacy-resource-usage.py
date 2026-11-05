#!/usr/bin/env python3
"""Build Daedalus-style resource_usage CSV/JSON from legacy SNAP module job.out / LSF Done PDFs."""

from __future__ import annotations

import csv
import glob
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from typing import Any

LEGACY_ROOT = os.environ.get(
    "LEGACY_ROOT",
    "/research/dept/dnb/core_operations/Bioinformatics/achroni/GitHub/"
    "stjude-biohackathon/stjude-biohackathon-KIDS26/sc-rna-seq-snap-legacy-Victoria-Knockout",
)
TEAM15_ROOT = os.environ.get(
    "TEAM15_ROOT",
    "/research/dept/dnb/core_operations/Bioinformatics/achroni/GitHub/"
    "stjude-biohackathon/stjude-biohackathon-KIDS26/KIDS26-Team15/analyses/"
    "sc-rna-seq-snap-legacy-Victoria-Knockout",
)

MODULES: list[tuple[str, str, str]] = [
    ("fastqc-analysis", "fastqc", "fastqc-analysis"),
    ("cellranger-analysis", "cellranger", "cellranger-analysis"),
    ("upstream-analysis", "upstream", "run-upstream-analysis"),
    ("integrative-analysis", "integrative", "run-integrative-analysis"),
    ("cluster-cell-calling", "cluster", "run-cluster-cell-calling"),
    (
        "cell-contamination-removal-analysis",
        "contamination_removal",
        "run-cell-contamination-removal-analysis",
    ),
    ("cell-types-annotation", "cell_types", "run-cell-types-annotation"),
    ("clone-phylogeny-analysis", "clone_phylogeny", "run-clone-phylogeny-analysis"),
    ("de-go-analysis", "de_go", "run-de-go-analysis"),
    ("rshiny-app", "rshiny", "run-rshiny-app"),
    ("project-updates", "project_updates", "run-project-updates"),
]

CSV_HEADER = [
    "run_id",
    "module",
    "call_alias",
    "analysis_dir",
    "team15_run_status",
    "legacy_run_status",
    "lsf_job_id",
    "lsf_status",
    "requested_cpu",
    "requested_memory_gb",
    "requested_lsf_queue",
    "actual_max_memory_gb",
    "actual_avg_memory_gb",
    "memory_utilization_pct",
    "lsf_mem_efficiency_pct",
    "cpu_time_sec",
    "wall_time_sec",
    "cpu_avg_efficiency_pct",
    "cpu_peak_efficiency_pct",
    "lsf_exit_code",
    "legacy_last_sample",
]


def rel_legacy_path(path: str) -> str:
    if not path:
        return ""
    try:
        return os.path.relpath(path, LEGACY_ROOT)
    except ValueError:
        return os.path.basename(path)


def parse_lsf_script(path: str) -> dict[str, Any]:
    out: dict[str, Any] = {"cpu": "", "memory_gb": "", "queue": "standard"}
    if not os.path.isfile(path):
        return out
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#BSUB -n "):
                out["cpu"] = line.split()[-1]
            elif line.startswith("#BSUB -q "):
                out["queue"] = line.split()[-1]
            elif "mem=" in line.lower():
                m = re.search(r"mem\s*=\s*([0-9.]+)\s*([GgMmKk]?[Bb]?)", line, re.I)
                if m:
                    val = float(m.group(1))
                    unit = (m.group(2) or "").upper()
                    if unit.startswith("G"):
                        out["memory_gb"] = val
                    elif unit.startswith("M") or "rusage[mem=" in line.lower():
                        out["memory_gb"] = round(val / 1024, 4)
                    else:
                        out["memory_gb"] = val
    return out


def extract_job_id_from_logs(module_dir: str) -> str:
    for name in ("job.out", "job.err"):
        path = os.path.join(module_dir, name)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        ids = sorted(set(re.findall(r"/lsf_tmp/(\d+)\.tmpdir", text)))
        if ids:
            return ids[0]
    return ""


def find_done_pdf(module_dir: str) -> str | None:
    matches = glob.glob(os.path.join(module_dir, "Job*.pdf"))
    return matches[0] if matches else None


def apply_lsf_resource_summary(stats: dict[str, Any], text: str) -> None:
    for pat in (
        r"Subject:\s*Job\s+(\d+):",
        r"Job\s+(\d+):\s*<",
        r"Job\s+(\d+):",
    ):
        m = re.search(pat, text)
        if m:
            stats["lsf_job_id"] = m.group(1)
            break
    if "Successfully completed" in text:
        stats["lsf_status"] = "DONE"
    bsub_n = re.search(r"#BSUB\s+-n\s+(\d+)", text)
    bsub_mem = re.search(r"#BSUB\s+-R\s+\"rusage\[mem=([0-9.]+)(GB|MB)?", text, re.I)
    if bsub_n:
        stats["requested_cpu"] = bsub_n.group(1)
    if bsub_mem:
        val = float(bsub_mem.group(1))
        unit = (bsub_mem.group(2) or "GB").upper()
        stats["requested_memory_gb"] = val if unit == "GB" else round(val / 1024, 4)
    localcores = re.search(r"--localcores=(\d+)", text)
    localmem = re.search(r"--localmem=(\d+)", text)
    if localcores:
        stats["requested_cpu"] = localcores.group(1)
    if localmem:
        stats["requested_memory_gb"] = float(localmem.group(1))

    block = text.split("Resource usage summary:", 1)
    if len(block) < 2:
        return
    nums = [
        ln.strip()
        for ln in block[1].splitlines()
        if re.search(r"[0-9]", ln)
        and not ln.strip().startswith("Read file")
        and "The output" not in ln
    ]

    def num_at(i: int) -> str:
        if i >= len(nums):
            return ""
        m = re.search(r"([0-9.]+)", nums[i])
        return m.group(1) if m else ""

    stats["cpu_time_sec"] = num_at(0)
    max_mb = num_at(1)
    avg_mb = num_at(2)
    total_req_mb = num_at(3)
    stats["actual_max_memory_gb"] = f"{float(max_mb) / 1024:.4f}" if max_mb else ""
    stats["actual_avg_memory_gb"] = f"{float(avg_mb) / 1024:.4f}" if avg_mb else ""
    stats["wall_time_sec"] = num_at(8) or num_at(7)
    if max_mb and total_req_mb:
        try:
            stats["lsf_mem_efficiency_pct"] = f"{(float(max_mb) / float(total_req_mb)) * 100:.2f}"
        except (ValueError, ZeroDivisionError):
            pass


def parse_cellranger_from_logs(module_dir: str) -> dict[str, Any]:
    """Use results/01_logs/*.out; pick the sample whose log was written last (last to finish)."""
    logs_dir = os.path.join(module_dir, "results", "01_logs")
    if not os.path.isdir(logs_dir):
        return {}
    candidates: list[tuple[float, str, str, str]] = []
    for name in os.listdir(logs_dir):
        if not name.endswith(".out"):
            continue
        path = os.path.join(logs_dir, name)
        if not os.path.isfile(path):
            continue
        sample = name[: -len(".out")]
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        if "Successfully completed" not in text and "Pipestance completed" not in text:
            continue
        mtime = os.path.getmtime(path)
        term = re.search(r"Terminated at (.+?)\n", text)
        sort_key = mtime
        if term:
            try:
                sort_key = datetime.strptime(
                    term.group(1).strip(), "%a %b %d %H:%M:%S %Y"
                ).timestamp()
            except ValueError:
                pass
        candidates.append((sort_key, sample, path, text))
    if not candidates:
        return {}
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, sample, path, text = candidates[0]
    stats: dict[str, Any] = {
        "last_sample": sample,
        "log_path": path,
        "lsf_status": "UNKNOWN",
    }
    apply_lsf_resource_summary(stats, text)
    # j1.sh: bsub -n 6 -M 48000 (MB total slot memory)
    j1 = os.path.join(module_dir, "j1.sh")
    if os.path.isfile(j1):
        with open(j1, encoding="utf-8", errors="replace") as fh:
            j1_text = fh.read()
        m_n = re.search(r"bsub[^\n]*-n\s+(\d+)", j1_text)
        m_m = re.search(r"-M\s+(\d+)", j1_text)
        if m_n and not stats.get("requested_cpu"):
            stats["requested_cpu"] = m_n.group(1)
        if m_m and not stats.get("requested_memory_gb"):
            stats["requested_memory_gb"] = round(float(m_m.group(1)) / 1024, 4)
    return stats


def parse_done_pdf(pdf_path: str) -> dict[str, Any]:
    proc = subprocess.run(
        ["pdftotext", pdf_path, "-"],
        check=False,
        capture_output=True,
        text=True,
    )
    text = proc.stdout or ""
    stats: dict[str, Any] = {
        "lsf_job_id": "",
        "lsf_status": "DONE",
        "lsf_exit_code": "",
        "pdf_path": pdf_path,
    }
    apply_lsf_resource_summary(stats, text)
    return stats


def memory_utilization(actual_gb: str, requested_gb: str) -> str:
    try:
        a = float(actual_gb)
        r = float(requested_gb)
        if r <= 0:
            return ""
        return f"{(a / r) * 100:.2f}"
    except (TypeError, ValueError):
        return ""


def legacy_module_ran(module_dir: str, module_key: str) -> bool:
    job_out = os.path.join(module_dir, "job.out")
    if os.path.isfile(job_out) and os.path.getsize(job_out) > 200:
        return True
    if module_key == "cellranger":
        cr = os.path.join(module_dir, "results", "02_cellranger_count")
        return os.path.isdir(cr)
    if module_key == "rshiny":
        return os.path.isdir(os.path.join(module_dir, "results", "shinyApp"))
    return False


def team15_module_ran(analysis_dir: str) -> bool:
    mod_dir = os.path.join(TEAM15_ROOT, "analyses", analysis_dir)
    if not os.path.isdir(mod_dir):
        return False
    job_out = os.path.join(mod_dir, "job.out")
    if os.path.isfile(job_out) and os.path.getsize(job_out) > 200:
        return True
    if analysis_dir == "cellranger-analysis":
        return os.path.isdir(os.path.join(mod_dir, "results", "02_cellranger_count"))
    if analysis_dir == "rshiny-app":
        return os.path.isdir(os.path.join(mod_dir, "results", "shinyApp"))
    return False


def build_row(
    run_id: str,
    analysis_dir: str,
    module: str,
    call_alias: str,
) -> dict[str, str]:
    legacy_dir = os.path.join(LEGACY_ROOT, "analyses", analysis_dir)
    req = parse_lsf_script(os.path.join(legacy_dir, "lsf-script.txt"))
    if analysis_dir == "cellranger-analysis":
        req = parse_lsf_script(os.path.join(legacy_dir, "submit-multiple-jobs.sh"))
        if not req.get("cpu"):
            req["cpu"] = "1"

    legacy_ran = legacy_module_ran(legacy_dir, module)
    team15_ran = team15_module_ran(analysis_dir)

    stats: dict[str, Any] = {}
    pdf = find_done_pdf(legacy_dir)
    if pdf:
        stats = parse_done_pdf(pdf)
    elif module == "cellranger":
        stats = parse_cellranger_from_logs(legacy_dir)
    job_id = stats.get("lsf_job_id") or extract_job_id_from_logs(legacy_dir)

    team15_status = "ran" if team15_ran else "not_run_yet"
    if stats.get("lsf_status") == "DONE":
        legacy_status = "DONE"
        lsf_status = "DONE"
    elif legacy_ran:
        legacy_status = "DONE"
        lsf_status = "DONE"
    else:
        legacy_status = "NOT_RUN"
        lsf_status = "NOT_RUN"

    requested_cpu = str(stats.get("requested_cpu") or req.get("cpu") or "")
    requested_mem = str(stats.get("requested_memory_gb") or req.get("memory_gb") or "")

    row = {
        "run_id": run_id,
        "module": module,
        "call_alias": call_alias,
        "analysis_dir": analysis_dir,
        "team15_run_status": team15_status,
        "legacy_run_status": legacy_status,
        "lsf_job_id": job_id or "",
        "lsf_status": lsf_status,
        "requested_cpu": requested_cpu,
        "requested_memory_gb": requested_mem,
        "requested_lsf_queue": str(req.get("queue") or "standard"),
        "actual_max_memory_gb": stats.get("actual_max_memory_gb", ""),
        "actual_avg_memory_gb": stats.get("actual_avg_memory_gb", ""),
        "memory_utilization_pct": "",
        "lsf_mem_efficiency_pct": stats.get("lsf_mem_efficiency_pct", ""),
        "cpu_time_sec": stats.get("cpu_time_sec", ""),
        "wall_time_sec": stats.get("wall_time_sec", ""),
        "cpu_avg_efficiency_pct": "",
        "cpu_peak_efficiency_pct": "",
        "lsf_exit_code": stats.get("lsf_exit_code", ""),
        "legacy_lsf_pdf": rel_legacy_path(stats.get("pdf_path", "")) if pdf else "",
        "legacy_last_sample": stats.get("last_sample", ""),
        "legacy_log_path": rel_legacy_path(stats.get("log_path", "")),
    }
    row["memory_utilization_pct"] = memory_utilization(
        row["actual_max_memory_gb"], row["requested_memory_gb"]
    )
    try:
        cpu_t = float(row["cpu_time_sec"])
        wall = float(row["wall_time_sec"])
        ncpu = float(requested_cpu)
        if wall > 0 and ncpu > 0:
            row["cpu_avg_efficiency_pct"] = f"{(cpu_t / (wall * ncpu)) * 100:.2f}"
    except (TypeError, ValueError):
        pass
    return row


def csv_row_with_na(row: dict[str, str]) -> dict[str, str]:
    out = {key: row.get(key, "") for key in CSV_HEADER}
    for key, value in out.items():
        if value is None or str(value).strip() == "":
            out[key] = "NA"
    return out


def main() -> None:
    run_id = os.environ.get(
        "RUN_ID",
        f"KIDS26-Victoria-Knockout_{datetime.now().strftime('%Y-%m-%d')}",
    )
    out_dir = os.path.join(TEAM15_ROOT, "out", "resource_usage")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, f"resource_usage_{run_id}.csv")
    json_path = os.path.join(out_dir, f"resource_usage_{run_id}.json")

    rows = [build_row(run_id, ad, mod, alias) for ad, mod, alias in MODULES]

    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_HEADER, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(csv_row_with_na(row) for row in rows)

    payload = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "legacy_root": LEGACY_ROOT,
        "team15_root": TEAM15_ROOT,
        "run_id": run_id,
        "modules": [],
    }
    for row in rows:
        payload["modules"].append(
            {
                "run_id": row["run_id"],
                "module": row["module"],
                "call_alias": row["call_alias"],
                "analysis_dir": row["analysis_dir"],
                "team15_run_status": row["team15_run_status"],
                "legacy_run_status": row["legacy_run_status"],
                "lsf_job_id": row["lsf_job_id"] or None,
                "lsf_status": row["lsf_status"],
                "requested": {
                    "cpu": float(row["requested_cpu"]) if row["requested_cpu"] else None,
                    "memory_gb": float(row["requested_memory_gb"])
                    if row["requested_memory_gb"]
                    else None,
                    "lsf_queue": row["requested_lsf_queue"],
                },
                "actual": {
                    "max_memory_gb": float(row["actual_max_memory_gb"])
                    if row["actual_max_memory_gb"]
                    else None,
                    "avg_memory_gb": float(row["actual_avg_memory_gb"])
                    if row["actual_avg_memory_gb"]
                    else None,
                    "cpu_time_sec": float(row["cpu_time_sec"]) if row["cpu_time_sec"] else None,
                    "wall_time_sec": float(row["wall_time_sec"])
                    if row["wall_time_sec"]
                    else None,
                },
                "efficiency": {
                    "memory_utilization_pct": float(row["memory_utilization_pct"])
                    if row["memory_utilization_pct"]
                    else None,
                    "lsf_mem_efficiency_pct": float(row["lsf_mem_efficiency_pct"])
                    if row["lsf_mem_efficiency_pct"]
                    else None,
                    "cpu_avg_efficiency_pct": float(row["cpu_avg_efficiency_pct"])
                    if row["cpu_avg_efficiency_pct"]
                    else None,
                    "cpu_peak_efficiency_pct": None,
                },
                "legacy_lsf_pdf": row["legacy_lsf_pdf"] or None,
                "legacy_last_sample": row["legacy_last_sample"] or None,
                "legacy_log_path": row["legacy_log_path"] or None,
                "lsf_exit_code": row["lsf_exit_code"] or None,
            }
        )

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    print(csv_path)
    print(json_path)


if __name__ == "__main__":
    main()
