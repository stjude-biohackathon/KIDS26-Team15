# P1 · ROI Analysis: SNAP Legacy vs Daedalus

Resource utilization and cost comparison between the legacy SNAP workflow (`launch_full_pipeline.sh`) and the new Daedalus orchestrator.

## Folder Structure

```
roi-analysis/
├── input/                                  # Raw data files
│   ├── Job-run-upstream-analysis-Done.pdf          # Legacy upstream LSF job (PDF)
│   ├── Job-run-integrative-analysis-Done.pdf       # Legacy integrative LSF job (PDF)
│   ├── resource_usage_2026-09-12_*.json            # Daedalus prototype resource usage (JSON)
│   ├── AugJobs_WithRunDashInName.xlsx              # August HPC jobs (all SNAP users)
│   └── daedalus-v2/                                # Daedalus v2 experiment outputs
│       ├── upstream-analysis/job.323196561.stdout
│       ├── integrative-analysis/job.323198973.stdout
│       └── outputs.json
├── output/                                 # Generated visualizations
│   ├── memory_utilization_comparison.png
│   ├── cpu_utilization_comparison.png
│   ├── memory_requested_vs_used.png
│   ├── analyst_savings_by_scenario.png
│   ├── hpc_cost_comparison.png
│   └── cost_improvement_pct.png
├── reports/                                # Analysis reports (markdown)
│   ├── P1-ROI-Combined-Run-Data.md         # Combined run data tables
│   ├── P1-ROI-Cost-Analysis.md             # Cost analysis
│   ├── P1-ROI-Cost-Scenarios.md            # Low/expected/high scenarios
│   └── P1-ROI-Job-Output-Details.md        # job.out/job.err details
├── scripts/                                # Analysis scripts
│   ├── roi_calculator.py                   # Legacy flow calculator
│   └── roi_calculator_daedalus.py          # Daedalus flow calculator
├── notebooks/                              # Jupyter notebooks
│   ├── roi_analysis_legacy_vs_daedalus_v2.ipynb    # Main analysis notebook
│   └── archive/                            # Older notebooks
│       ├── aug_data_exp.ipynb              # August jobs exploration
│       └── roi_analysis_legacy_vs_daedalus_prototype.ipynb
├── docs/                                   # Reference documents
│   ├── roi_scenarios.csv                   # Low/expected/high scenario parameters
│   ├── roi-analysis-Lindsey-questions.md   # HPC cost model and analyst rate
│   └── data-analyst-time.md                # Analyst time estimation methodology
├── .gitignore
├── .python-version
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
cd ../notebooks
jupyter notebook roi_analysis_legacy_vs_daedalus_v2.ipynb
```

## Data Sources

| Source | File | Description |
|--------|------|-------------|
| Legacy upstream | `input/Job-run-upstream-analysis-Done.pdf` | LSF job completion email (PDF) |
| Legacy integrative | `input/Job-run-integrative-analysis-Done.pdf` | LSF job completion email (PDF) |
| Daedalus v1 | `input/resource_usage_*.json` | Sprocket resource usage output |
| Daedalus v2 | `input/daedalus-v2/*.stdout` | LSF stdout files from Sprocket run |
| August jobs | `input/AugJobs_WithRunDashInName.xlsx` | All SNAP HPC jobs (Aug 2026) |
| Scenarios | `docs/roi_scenarios.csv` | Low/expected/high cost parameters |

## Key Metrics

All utilization calculations use **average memory** (not peak) for fair comparison:

- **Memory Utilization** = `avg_memory_used / total_requested_memory`
- **CPU Utilization** = `actual_cpu_time / (wall_time × cores)`

## Key Findings

### Resource Utilization

**Upstream:**

| Metric | Legacy | Daedalus Prototype | Daedalus v2 |
|--------|--------|--------------------|-------------|
| Memory Utilization | 9.6% | 3.0% | 3.1% |
| CPU Utilization | 7.1% | 11.5% | 13.4% |
| Peak Memory | 96 GB | 22 GB | 24 GB |
| Avg Memory Used | 46 GB | 8.5 GB | 8.8 GB |
| Requested Memory | 480 GB | 36 GB | 34 GB |
| Wall-clock | 1h 47m | 1h 8m | 1h 2m |
| Cores | 16 | 8 | 8 |

**Integrative:**

| Metric | Legacy | Daedalus Prototype | Daedalus v2 |
|--------|--------|--------------------|-------------|
| Memory Utilization | 1.5% | 0.5% | 0.6% |
| CPU Utilization | 6.7% | 5.8% | 10.1% |
| Peak Memory | 24 GB | 10 GB | 10.4 GB |
| Avg Memory Used | 14.1 GB | 6.3 GB | 7.4 GB |
| Requested Memory | 960 GB | 116 GB | 108 GB |
| Wall-clock | 16m | 17m | 10m |
| Cores | 10 | 10 | 10 |

### Cost Analysis

**Compute savings** (St. Jude pricing $0.024/core-hour):
- Legacy: 31.29 core-hrs = $0.75/run → Daedalus Prototype: 11.99 core-hrs = $0.29/run (62% reduction) → Daedalus v2: 9.95 core-hrs = $0.24/run (68% reduction)

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
