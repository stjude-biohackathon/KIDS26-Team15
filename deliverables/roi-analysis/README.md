# P1 · ROI Analysis: SNAP Legacy vs Daedalus

Resource utilization and cost comparison between the legacy SNAP workflow (`launch_full_pipeline.sh`) and the new Daedalus orchestrator.

## Folder Structure

```
roi-analysis/
├── docs/                                   # Reference documents
│   ├── data-analyst-time.md                # Analyst time estimation methodology
│   ├── roi-analysis-Lindsey-questions.md   # HPC cost model and analyst rate
│   └── roi_scenarios.csv                   # Low/expected/high scenario parameters
├── input/                                  # Raw data files
│   ├── AugJobs_WithRunDashInName.xlsx              # August HPC jobs (all SNAP users)
│   ├── daedalus-v2/                                # Daedalus v2 experiment outputs
│   │   ├── integrative-analysis/job.323198973.stdout
│   │   ├── outputs.json
│   │   └── upstream-analysis/job.323196561.stdout
│   ├── Job-run-integrative-analysis-Done.pdf       # Legacy integrative LSF job (PDF)
│   ├── Job-run-upstream-analysis-Done.pdf          # Legacy upstream LSF job (PDF)
│   └── resource_usage_2026-09-12_*.json            # Daedalus prototype resource usage (JSON)
├── notebooks/                              # Jupyter notebooks
│   ├── roi_analysis_legacy_vs_daedalus_v2.ipynb    # Original (PDF + Daedalus v2) — writes `output/`
│   └── roi_analysis_posthackathon_resource_usage.ipynb  # September 2026 CSV comparison — writes `output/results-posthackathon/`
├── output/                                 # Generated visualizations (original run)
│   ├── cost_improvement_pct.png
│   ├── cpu_utilization_comparison.png
│   ├── memory_requested_vs_used.png
│   └── memory_utilization_comparison.png
├── output/results-posthackathon/           # Post-hackathon CSV comparison plots (preserves output/ above)
│   ├── resource_utilization_comparison.png   # Memory + CPU % (two panels)
│   ├── memory_requested_vs_used.png
│   ├── cost_improvement_pct.png
│   └── comparison_summary.csv
├── pyproject.toml                          # Python dependencies
├── README.md                               # This file
├── reports/                                # Analysis reports (markdown)
│   ├── P1-ROI-Combined-Run-Data.md         # Combined run data tables
│   ├── P1-ROI-Biohackathon-vs-Post-Hackathon-Comparison.md  # KIDS26 legacy CSV vs Daedalus post-hackathon CSV
│   ├── P1-ROI-Cost-Scenarios.md            # Low/expected/high scenarios
│   └── P1-ROI-Job-Output-Details.md        # job.out/job.err details
├── scripts/                                # Analysis scripts
│   ├── roi_calculator.py                   # Legacy flow calculator
│   ├── roi_calculator_daedalus.py          # Daedalus flow calculator
│   ├── roi_scope.py                        # Biohackathon (2) vs post-hackathon module scopes
│   ├── compare_biohackathon_posthackathon.py  # Scoped ROI markdown report
│   ├── load_resource_usage_csv.py
│   └── generate_posthackathon_plots.py
└── uv.lock                                 # Dependency lock file
```

## Quick Start

```bash
# Run legacy calculator
cd scripts
uv run python3 roi_calculator.py ../input/Job-run-upstream-analysis-Done.pdf ../input/Job-run-integrative-analysis-Done.pdf

# Run Daedalus calculator
uv run python3 roi_calculator_daedalus.py ../input/resource_usage_2026-09-12_143900834470824.json

# Regenerate biohackathon vs post-hackathon comparison (September 2026 legacy vs November 2026 Daedalus CSV)
uv run python3 compare_biohackathon_posthackathon.py

# Regenerate post-hackathon plots (requires matplotlib + pandas; e.g. module load matplotlib/3.9.2-gfbf-2024a)
python3 scripts/generate_posthackathon_plots.py

# Launch notebook (from roi-analysis/ root)
cd ../notebooks
jupyter notebook roi_analysis_legacy_vs_daedalus_v2.ipynb

# Post-hackathon resource_usage CSVs → output/results-posthackathon/
jupyter notebook roi_analysis_posthackathon_resource_usage.ipynb
```

## Data Sources

| Source | File | Description |
|--------|------|-------------|
| Legacy upstream | `input/Job-run-upstream-analysis-Done.pdf` | LSF job completion email (PDF) |
| Legacy integrative | `input/Job-run-integrative-analysis-Done.pdf` | LSF job completion email (PDF) |
| Daedalus v1 | `input/resource_usage_*.json` | Sprocket resource usage output |
| KIDS26 legacy (September 2026) | `input/resource_usage_KIDS26-Victoria-Knockout_2026-11-05.csv` | Full legacy module LSF export |
| Daedalus post-hackathon | `../analyses/sc-rna-seq-snap-daedalus-Victoria-Knockout/daedalus-post-hackathon/resource_usage_2026-11-05_220340654817588.csv` | Victoria Knockout Daedalus downstream run (single copy; SMB: `smb://jude.stjude.org/developmentalneurobiology/core_operations/Bioinformatics/achroni/GitHub/stjude-biohackathon/stjude-biohackathon-KIDS26/KIDS26-Team15/analyses/sc-rna-seq-snap-daedalus-Victoria-Knockout/daedalus-post-hackathon/resource_usage_2026-11-05_220340654817588.csv`) |
| Daedalus v2 | `input/daedalus-v2/*.stdout` | LSF stdout files from Sprocket run |
| August jobs | `input/AugJobs_WithRunDashInName.xlsx` | All SNAP HPC jobs (Aug 2026) |
| Scenarios | `docs/roi_scenarios.csv` | Low/expected/high cost parameters |

## Key Metrics

All utilization calculations use **average memory** (not peak) for fair comparison:

- **Memory Utilization** = `avg_memory_used / total_requested_memory`
- **CPU Utilization** = `actual_cpu_time / (wall_time × cores)`

## Key Findings

**Victoria Knockout ROI scopes** ([`P1-ROI-Biohackathon-vs-Post-Hackathon-Comparison.md`](reports/P1-ROI-Biohackathon-vs-Post-Hackathon-Comparison.md)):

| Phase | Compared modules | Notes |
|-------|------------------|-------|
| **Biohackathon** | 2 — `upstream`, `integrative` | Legacy vs Daedalus head-to-head |
| **Post-hackathon** | 5 — `upstream`, `integrative`, `cluster`, `cell_types`, `rshiny` | Plus **FastQC & Cell Ranger** on shared project data (legacy HPC in CSV); **biological validation** (Daedalus only); `de_go` / `project_updates` in Daedalus export |

HPC totals in that report are **summed per scope** (not the full CSV overlap). Post-hackathon plots: `resource_utilization_comparison.png` (memory + CPU, 5 modules), `memory_requested_vs_used.png`, `cost_improvement_pct.png` (HPC/analyst $ uses legacy 5 + fastqc + cellranger vs Daedalus 5 + de_go + project_updates core-hours).

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
4. `cost_improvement_pct.png` — Legacy vs Daedalus per scenario: **HPC $/run**, **analyst hours/run**, and **analyst $/run**, with % savings on Daedalus bars

## Requirements

- Python 3.10+
- pymupdf (for PDF parsing)
- pandas, matplotlib, seaborn (for notebook)

```bash
uv sync
```
