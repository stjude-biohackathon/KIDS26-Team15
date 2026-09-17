# P1 · ROI Analysis: SNAP Legacy vs Daedalus

Resource utilization comparison between the legacy SNAP workflow (`launch_full_pipeline.sh`) and the new Daedalus orchestrator.

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
│   └── memory_requested_vs_used.png
├── reports/                            # Analysis markdown files
│   ├── P1-ROI-Combined-Run-Data.md
│   ├── P1-ROI-Cost-Analysis.md
│   └── P1-ROI-Job-Output-Details.md
├── scripts/                            # Analysis scripts
│   ├── roi_calculator.py               # Legacy flow calculator
│   └── roi_calculator_daedalus.py      # Daedalus flow calculator
├── roi_analysis_notebook.ipynb         # Jupyter notebook for display
├── roi-analysis-Lindsey-questions.md   # HPC cost model and analyst rate
└── README.md                           # This file
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

## Key Metrics

All utilization calculations use **average memory** (not peak) for fair comparison:

- **Memory Utilization** = `avg_memory_used / total_requested_memory`
- **CPU Utilization** = `actual_cpu_time / (wall_time × cores)`

## Key Findings

| Metric | Legacy Up | Daedalus Up | Legacy Int | Daedalus Int |
|--------|-----------|-------------|------------|--------------|
| Memory Utilization | 9.6% | 23.6% | 1.5% | 5.4% |
| CPU Utilization | 7.1% | 11.5% | 6.7% | 5.8% |
| Peak Memory | 96 GB | 22 GB | 24 GB | 10 GB |
| Wall-clock | 1h 47m | 1h 8m | 16m | 17m |

**Conclusion:** Daedalus shows directional improvement but the auto-scaler is still conservative. Real wins are fewer cores (16→8), lower peak memory, faster runtime, and YAML-driven configuration — not utilization %.

## Cost Analysis

Using St. Jude HPC pricing ($0.024/core-hour):
- Legacy compute: $0.75 per run
- Daedalus compute: $0.42 per run
- **Savings: 44%**

## Requirements

- Python 3.10+
- pymupdf (for PDF parsing)
- pandas, matplotlib, seaborn (for notebook)

```bash
uv add pymupdf pandas matplotlib seaborn
```
