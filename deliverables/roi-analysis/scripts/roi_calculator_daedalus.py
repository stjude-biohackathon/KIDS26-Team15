#!/usr/bin/env python3
"""
ROI Analysis - Daedalus/Sprocket Resource Utilization Calculator

Reads a single Daedalus resource_usage JSON file and calculates:
- Memory utilization (avg used / requested) — matches legacy calculation
- CPU utilization (actual CPU time / allocated core-time)

Usage:
    python roi_calculator_daedalus.py <resource_usage.json>
    uv run python3 roi_calculator_daedalus.py <resource_usage.json>

Input: JSON file from Daedalus resource_usage output
Output: utilization metrics table (markdown)

Example:
    uv run python3 roi_calculator_daedalus.py resource_usage_2026-09-12_143900834470824.json
"""

import json
import sys
from pathlib import Path


def parse_modules(data: dict) -> list:
    """Parse modules from Daedalus JSON data."""
    modules = data.get('modules', [])
    parsed = []
    
    for mod in modules:
        metrics = {}
        
        # Basic info
        metrics['run_id'] = data.get('run_id', mod.get('run_id', 'N/A'))
        metrics['module'] = mod.get('module', 'N/A')
        metrics['lsf_job_id'] = mod.get('lsf_job_id', 'N/A')
        metrics['lsf_status'] = mod.get('lsf_status', 'N/A')
        
        # Requested resources
        requested = mod.get('requested', {})
        metrics['requested_cpu'] = int(requested.get('cpu', 0))
        metrics['requested_memory_gb'] = float(requested.get('memory_gb', 0))
        
        # Actual usage
        actual = mod.get('actual', {})
        metrics['actual_max_memory_gb'] = float(actual.get('max_memory_gb', 0))
        metrics['actual_avg_memory_gb'] = float(actual.get('avg_memory_gb', 0))
        metrics['cpu_time_sec'] = float(actual.get('cpu_time_sec', 0))
        metrics['wall_time_sec'] = float(actual.get('wall_time_sec', 0))
        
        parsed.append(metrics)
    
    return parsed


def calculate_utilization(metrics: dict) -> dict:
    """Calculate memory and CPU utilization percentages."""
    results = {}
    
    # Memory utilization: avg used / requested (matches legacy calculation)
    if metrics['requested_memory_gb'] > 0 and metrics['actual_avg_memory_gb'] > 0:
        results['memory_utilization_pct'] = (metrics['actual_avg_memory_gb'] / metrics['requested_memory_gb']) * 100
        results['memory_waste_gb'] = metrics['requested_memory_gb'] - metrics['actual_avg_memory_gb']
    
    # CPU utilization: actual CPU time / allocated core-time
    if metrics['wall_time_sec'] > 0 and metrics['requested_cpu'] > 0:
        allocated_core_time = metrics['wall_time_sec'] * metrics['requested_cpu']
        if allocated_core_time > 0:
            results['cpu_utilization_pct'] = (metrics['cpu_time_sec'] / allocated_core_time) * 100
            results['allocated_core_time_sec'] = allocated_core_time
    
    return results


def format_table(metrics: dict, results: dict) -> str:
    """Format results as a markdown table."""
    lines = []
    
    lines.append("## Input Metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Module | {metrics['module']} |")
    lines.append(f"| LSF Job ID | {metrics['lsf_job_id']} |")
    lines.append(f"| LSF Status | {metrics['lsf_status']} |")
    lines.append(f"| Cores Allocated | {metrics['requested_cpu']} |")
    lines.append(f"| Memory Requested | {metrics['requested_memory_gb']} GB |")
    lines.append(f"| Wall-clock | {metrics['wall_time_sec']:.0f}s ({metrics['wall_time_sec']/3600:.2f}h) |")
    lines.append(f"| Actual CPU Time | {metrics['cpu_time_sec']:.1f}s |")
    lines.append(f"| Avg Memory Used | {metrics['actual_avg_memory_gb']:.1f} GB |")
    lines.append(f"| Max Memory Used | {metrics['actual_max_memory_gb']:.1f} GB |")
    
    lines.append("")
    
    lines.append("## Utilization Results")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    
    if 'memory_utilization_pct' in results:
        lines.append(f"| Memory Utilization (avg/req) | **{results['memory_utilization_pct']:.1f}%** |")
    if 'cpu_utilization_pct' in results:
        lines.append(f"| CPU Utilization (actual/allocated) | **{results['cpu_utilization_pct']:.1f}%** |")
    if 'memory_waste_gb' in results:
        lines.append(f"| Memory Waste | {results['memory_waste_gb']:.1f} GB |")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: python roi_calculator_daedalus.py <resource_usage.json>")
        print("       uv run python3 roi_calculator_daedalus.py <resource_usage.json>")
        print("")
        print("Input: JSON file from Daedalus resource_usage output")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    # Read JSON
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Parse modules
    modules = parse_modules(data)
    
    if not modules:
        print(f"Error: No modules found in {input_file}")
        sys.exit(1)
    
    # Process each module
    print("# Daedalus Resource Utilization Analysis")
    print("")
    print(f"**Source:** `{input_file}`")
    print(f"**Run ID:** `{data.get('run_id', 'N/A')}`")
    print("")
    
    for metrics in modules:
        results = calculate_utilization(metrics)
        print(format_table(metrics, results))
        print("")
        print("---")
        print("")


if __name__ == "__main__":
    main()
