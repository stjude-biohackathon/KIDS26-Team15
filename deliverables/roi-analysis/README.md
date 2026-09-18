# P1 · ROI Analysis: SNAP Legacy vs Daedalus

Resource utilization and cost comparison between the legacy SNAP workflow (`launch_full_pipeline.sh`) and the new Daedalus orchestrator.

## Folder Structure

```
roi-analysis/
├── input/                              # Raw data files
│   ├── Job-run-upstream-analysis-Done.pdf
│   ├── Job-run-integrative-analysis-Done.pdf
│   ├── resource_usage_2026-09-12_143900834470824.json
│   ├── upstream_output.txt              # Extracted text from PDF
│   └── integrative_output.txt           # Extracted text from PDF
├── output/                             # Generated visualizations
│   ├── cpu_utilization_comparison.png
│   ├── memory_utilization_comparison.png
│   ├── memory_requested_vs_used.png
│   ├── analyst_savings_by_scenario.png
│   ├── hpc_cost_comparison.png
│   └── cost_improvement_pct.png
├── reports/                            # Analysis markdown files
│   ├── P1-ROI-Combined-Run-Data.md
│   ├── P1-ROI-Cost-Analysis.md
│   ├── P1-ROI-Job-Output-Details.md
│   └── P1-ROI-Cost-Scenarios.md
├── scripts/                                # Analysis scripts
│   ├── roi_calculator.py                   # Legacy flow calculator
│   └── roi_calculator_daedalus.py          # Daedalus flow calculator
├── notebooks /                             # Jupyter notebooks for analysis and display
│   ├── roi_analysis_notebook.ipynb         # Legacy vs Deadalus comparision and display
│   └── aug_data_exp.ipynb                  # August Jobs data exploration
├── docs/                                   # Reference documents
│   ├── roi_scenarios.csv                   # Low/expected/high scenario parameters
│   ├── roi-analysis-Lindsey-questions.md   # HPC cost model and analyst rate
│   └── data-analyst-time.md                # Analyst time estimation methodology
├── pyproject.toml                          # Python dependencies
├── uv.lock                                 # Dependency lock file
└── README.md                               # This file
```

## Quick Start

```bash
# Run legacy calculator
cd scripts
uv run python3 roi_calculator.py ../input/Job-run-upstream-analysis-Done.pdf ../input/Job-run-integrative-analysis-Done.pdf

# Run Daedalus calculator
uv run python3 roi_calculator_daedalus.py ../input/resource_usage_2026-09-12_143900834470824.json

# Launch notebook (from roi-analysis/ root)
cd ..
jupyter notebook roi_analysis_notebook.ipynb
```

## Data Sources

| Source | File | Description |
|--------|------|-------------|
| Legacy upstream | `input/Job-run-upstream-analysis-Done.pdf` | LSF job completion email (PDF) |
| Legacy integrative | `input/Job-run-integrative-analysis-Done.pdf` | LSF job completion email (PDF) |
| Daedalus | `input/resource_usage_*.json` | Sprocket resource usage output |
| Scenarios | `docs/roi_scenarios.csv` | Low/expected/high cost parameters |

## Key Metrics

All utilization calculations use **average memory** (not peak) for fair comparison:

- **Memory Utilization** = `avg_memory_used / total_requested_memory`
- **CPU Utilization** = `actual_cpu_time / (wall_time × cores)`

## Key Findings

### Resource Utilization

| Metric | Legacy Up | Daedalus Up | Legacy Int | Daedalus Int |
|--------|-----------|-------------|------------|--------------|
| Memory Utilization | 9.6% | 23.6% | 1.5% | 5.4% |
| CPU Utilization | 7.1% | 11.5% | 6.7% | 5.8% |
| Peak Memory | 96 GB | 22 GB | 24 GB | 10 GB |
| Wall-clock | 1h 47m | 1h 8m | 16m | 17m |

### Cost Analysis

**Compute savings** (St. Jude pricing $0.024/core-hour):
- Legacy: $0.75/run → Daedalus: $0.42/run (44% reduction)

**Analyst time savings** (dominant factor):
| Scenario | Legacy Hrs/Run | Daedalus Hrs/Run | Savings/Run | Annual Savings | ROI | Payback |
|----------|----------------|------------------|-------------|----------------|-----|---------|
| Low | 4 | 1 | $144 | $1,748 | -32.6% | 14 runs |
| Expected | 6 | 1.5 | $216 | $5,244 | 48.1% | 14 runs |
| High | 8 | 2 | $288 | $13,993 | 136.1% | 18 runs |

**Analyst savings are 99% of total ROI** — HPC compute savings are negligible at St. Jude pricing.

## Outputs

The notebook generates 6 charts in `output/`:
1. `memory_utilization_comparison.png` — Memory utilization side by side
2. `cpu_utilization_comparison.png` — CPU utilization side by side
3. `memory_requested_vs_used.png` — Requested vs actual memory
4. `analyst_savings_by_scenario.png` — Analyst hours and cost by scenario
5. `hpc_cost_comparison.png` — HPC cost comparison
6. `cost_improvement_pct.png` — % improvement HPC vs analyst

## Requirements

- Python 3.10+
- pymupdf (for PDF parsing)
- pandas, matplotlib, seaborn (for notebook)

```bash
uv sync
```
