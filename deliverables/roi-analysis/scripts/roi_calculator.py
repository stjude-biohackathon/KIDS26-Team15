#!/usr/bin/env python3
"""
ROI Analysis - Resource Utilization Calculator

Reads LSF Job Done PDFs (or extracted text) and calculates:
- Memory utilization (avg used / total requested)
- CPU utilization (actual CPU time / allocated core-time)

Usage:
    python roi_calculator.py <pdf_or_text_file> [pdf_or_text_file2 ...]
    uv run roi_calculator.py <pdf_or_text_file> [pdf_or_text_file2 ...]

Input: PDF file (LSF Job Done email) or pre-extracted text file
Output: utilization metrics table (markdown)

Examples:
    uv run roi_calculator.py Job-run-upstream-analysis-Done.pdf
    uv run roi_calculator.py upstream.txt integrative.txt
    uv run roi_calculator.py upstream.pdf integrative.pdf
"""

import re
import sys
from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pymupdf."""
    try:
        import fitz  # pymupdf 
    except ImportError:
        print("Error: pymupdf is required for PDF processing.")
        print("Install with: uv add pymupdf")
        sys.exit(1)

    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += str(page.get_text())
    return text


def read_input_file(file_path: Path) -> str:
    """Read input file, handling both PDF and text formats."""
    if file_path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        return file_path.read_text()


def parse_job_output(text: str) -> dict:
    """Parse LSF job output text and extract resource metrics."""
    metrics = {}

    # Extract CPU time
    cpu_match = re.search(r"CPU time\s*:\s*([\d.]+)\s*sec", text)
    if cpu_match:
        metrics["cpu_time_sec"] = float(cpu_match.group(1))

    # Extract Max Memory
    max_mem_match = re.search(r"Max Memory\s*:\s*([\d.]+)\s*MB", text)
    if max_mem_match:
        metrics["max_memory_mb"] = float(max_mem_match.group(1))

    # Extract Average Memory
    avg_mem_match = re.search(r"Average Memory\s*:\s*([\d.]+)\s*MB", text)
    if avg_mem_match:
        metrics["avg_memory_mb"] = float(avg_mem_match.group(1))

    # Extract Total Requested Memory
    total_req_match = re.search(r"Total Requested Memory\s*:\s*([\d.]+)\s*MB", text)
    if total_req_match:
        metrics["total_requested_memory_mb"] = float(total_req_match.group(1))

    # Extract Delta Memory
    delta_match = re.search(r"Delta Memory\s*:\s*([\d.]+)\s*MB", text)
    if delta_match:
        metrics["delta_memory_mb"] = float(delta_match.group(1))

    # Extract Run time
    run_time_match = re.search(r"Run time\s*:\s*(\d+)\s*sec", text)
    if run_time_match:
        metrics["run_time_sec"] = float(run_time_match.group(1))

    # Extract Max Processes
    proc_match = re.search(r"Max Processes\s*:\s*(\d+)", text)
    if proc_match:
        metrics["max_processes"] = int(proc_match.group(1))

    # Extract Max Threads
    thread_match = re.search(r"Max Threads\s*:\s*(\d+)", text)
    if thread_match:
        metrics["max_threads"] = int(thread_match.group(1))

    # Extract cores from bsub -n
    cores_match = re.search(r"#BSUB\s+-n\s+(\d+)", text)
    if cores_match:
        metrics["cores"] = int(cores_match.group(1))

    # Extract rusage memory from bsub -R
    rusage_match = re.search(r"rusage\[mem=(\d+)GB\]", text)
    if rusage_match:
        metrics["rusage_mem_gb"] = int(rusage_match.group(1))

    # Extract job name
    job_match = re.search(r"#BSUB\s+-J\s+(\S+)", text)
    if job_match:
        metrics["job_name"] = job_match.group(1)

    return metrics


def calculate_utilization(metrics: dict) -> dict:
    """Calculate memory and CPU utilization percentages."""
    results = {}

    # Memory utilization
    if "total_requested_memory_mb" in metrics and "avg_memory_mb" in metrics:
        total_req = metrics["total_requested_memory_mb"]
        avg_used = metrics["avg_memory_mb"]
        if total_req > 0:
            results["memory_utilization_pct"] = (avg_used / total_req) * 100
            results["memory_waste_gb"] = (total_req - avg_used) / 1024

    # CPU utilization (actual CPU time / allocated core-time)
    if "cpu_time_sec" in metrics and "run_time_sec" in metrics and "cores" in metrics:
        allocated_core_time = metrics["run_time_sec"] * metrics["cores"]
        actual_cpu_time = metrics["cpu_time_sec"]
        if allocated_core_time > 0:
            results["cpu_utilization_pct"] = (
                actual_cpu_time / allocated_core_time
            ) * 100
            results["allocated_core_time_sec"] = allocated_core_time
            results["cpu_waste_pct"] = 100 - results["cpu_utilization_pct"]

    return results


def format_table(metrics: dict, results: dict) -> str:
    """Format results as a markdown table."""
    lines = []

    # Input metrics
    lines.append("## Input Metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")

    if "job_name" in metrics:
        lines.append(f"| Job Name | {metrics['job_name']} |")
    if "cores" in metrics:
        lines.append(f"| Cores Allocated | {metrics['cores']} |")
    if "rusage_mem_gb" in metrics:
        lines.append(f"| Per-Slot Memory Request | {metrics['rusage_mem_gb']} GB |")
    if "run_time_sec" in metrics:
        lines.append(
            f"| Wall-clock | {metrics['run_time_sec']:.0f}s ({metrics['run_time_sec']/3600:.2f}h) |"
        )
    if "cpu_time_sec" in metrics:
        lines.append(f"| Actual CPU Time | {metrics['cpu_time_sec']:.0f}s |")
    if "allocated_core_time_sec" in results:
        lines.append(
            f"| Allocated Core-time | {results['allocated_core_time_sec']:.0f}s |"
        )
    if "total_requested_memory_mb" in metrics:
        lines.append(
            f"| Total Requested Memory | {metrics['total_requested_memory_mb']:.0f} MB ({metrics['total_requested_memory_mb']/1024:.0f} GB) |"
        )
    if "avg_memory_mb" in metrics:
        lines.append(
            f"| Average Memory Used | {metrics['avg_memory_mb']:.0f} MB ({metrics['avg_memory_mb']/1024:.1f} GB) |"
        )
    if "max_memory_mb" in metrics:
        lines.append(
            f"| Max Memory Used | {metrics['max_memory_mb']:.0f} MB ({metrics['max_memory_mb']/1024:.1f} GB) |"
        )

    lines.append("")

    # Utilization results
    lines.append("## Utilization Results")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")

    if "memory_utilization_pct" in results:
        lines.append(
            f"| Memory Utilization (avg/req) | **{results['memory_utilization_pct']:.1f}%** |"
        )
    if "cpu_utilization_pct" in results:
        lines.append(
            f"| CPU Utilization (actual/allocated) | **{results['cpu_utilization_pct']:.1f}%** |"
        )
    if "memory_waste_gb" in results:
        lines.append(f"| Memory Waste | {results['memory_waste_gb']:.1f} GB |")
    if "cpu_waste_pct" in results:
        lines.append(f"| CPU Waste | {results['cpu_waste_pct']:.1f}% |")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python roi_calculator.py <pdf_or_text_file> [pdf_or_text_file2 ...]"
        )
        print(
            "       uv run roi_calculator.py <pdf_or_text_file> [pdf_or_text_file2 ...]"
        )
        print("")
        print("Input: PDF file (LSF Job Done email) or pre-extracted text file")
        sys.exit(1)

    for input_path in sys.argv[1:]:
        input_file = Path(input_path)

        if not input_file.exists():
            print(f"Error: File not found: {input_file}")
            continue

        # Read input (PDF or text)
        text = read_input_file(input_file)

        # Parse metrics
        metrics = parse_job_output(text)

        if not metrics:
            print(f"Error: No metrics found in {input_file}")
            continue

        # Calculate utilization
        results = calculate_utilization(metrics)

        # Output results
        print("# Resource Utilization Analysis")
        print("")
        print(f"**Source:** `{input_file}`")
        print("")
        print(format_table(metrics, results))
        print("")
        print("---")
        print("")


if __name__ == "__main__":
    main()
