# ROI — Biohackathon vs Post-Hackathon (Victoria Knockout)

**Cohort:** Victoria Knockout (4 samples, ~27k cells)

| Phase | Legacy vs Daedalus test scope |
|-------|----------------------------------|
| **Biohackathon** | **2 modules:** `upstream`, `integrative` |
| **Post-hackathon** | **5 modules** (`upstream`, `integrative`, `cluster`, `cell_types`, `rshiny`) + **FastQC & Cell Ranger** (both workflow types on shared project data) + **Daedalus-only:** `de_go`, `project_updates`, **`biological_validation`** |

| Data file | Role |
|-----------|------|
| `resource_usage_KIDS26-Victoria-Knockout_2026-11-05.csv` | Legacy SNAP LSF export (KIDS26) |
| `resource_usage_2026-10-28_232725179937495.csv` | Daedalus/Sprocket post-hackathon downstream run |

## 1. Biohackathon ROI (2 modules: legacy vs Daedalus)

| Module | Legacy CPUs | Daedalus CPUs | Legacy req mem (GB/slot) | Daedalus req mem | Legacy avg mem (GB) | Daedalus avg mem | Legacy wall | Daedalus wall | Legacy core-hrs | Daedalus core-hrs |
|--------|-------------|---------------|---------------------------|------------------|--------------------|------------------|-------------|---------------|---------------|-------------------|
| upstream | 16 | 8 | 30.00 | 36.00 | 45.98 | 8.90 | 1h 54m | 0h 59m | 30.51 | 7.87 |
| integrative | 10 | 10 | 96.00 | 116.00 | 18.05 | 7.30 | 2h 2m | 0h 11m | 20.46 | 1.93 |

### Biohackathon totals (upstream + integrative only)

| Metric | Legacy | Daedalus |
|--------|--------|----------|
| Allocated core-hours | 50.97 | 9.80 |
| Est. HPC cost (@ $0.024/core-hr) | $1.22 | $0.24 |
| Core-hour change (Daedalus vs legacy) | — | **80.8%** vs legacy |

## 2. Post-hackathon ROI

### 2a. Five modules — legacy vs Daedalus

| Module | Legacy CPUs | Daedalus CPUs | Legacy req mem (GB/slot) | Daedalus req mem | Legacy avg mem (GB) | Daedalus avg mem | Legacy wall | Daedalus wall | Legacy core-hrs | Daedalus core-hrs |
|--------|-------------|---------------|---------------------------|------------------|--------------------|------------------|-------------|---------------|---------------|-------------------|
| upstream | 16 | 8 | 30.00 | 36.00 | 45.98 | 8.90 | 1h 54m | 0h 59m | 30.51 | 7.87 |
| integrative | 10 | 10 | 96.00 | 116.00 | 18.05 | 7.30 | 2h 2m | 0h 11m | 20.46 | 1.93 |
| cluster | 4 | 4 | 48.00 | 58.00 | 17.51 | 9.10 | 2h 51m | 1h 4m | 11.45 | 4.29 |
| cell_types | 4 | 4 | 64.00 | 77.00 | 6.21 | 6.40 | 3h 4m | 0h 13m | 12.31 | 0.92 |
| rshiny | 4 | 4 | 30.00 | 30.00 | 3.63 | 3.30 | 3h 5m | 0h 1m | 12.38 | 0.07 |

### Post-hackathon paired-module totals (5 modules)

| Metric | Legacy | Daedalus |
|--------|--------|----------|
| Allocated core-hours | 87.11 | 15.08 |
| Est. HPC cost (@ $0.024/core-hr) | $2.09 | $0.36 |
| Core-hour change (Daedalus vs legacy) | — | **82.7%** vs legacy |

### 2b. FastQC & Cell Ranger (both pipelines)

Both legacy and Daedalus Victoria Knockout projects use the same **FastQC** and **Cell Ranger** outputs under `analyses/fastqc-analysis` and `analyses/cellranger-analysis`. HPC is captured in the **legacy** export; Daedalus downstream consumes these results without a separate row in the Daedalus CSV.

| Module | Legacy CPUs | Daedalus CPUs | Legacy req mem (GB/slot) | Daedalus req mem | Legacy avg mem (GB) | Daedalus avg mem | Legacy wall | Daedalus wall | Legacy core-hrs | Daedalus core-hrs |
|--------|-------------|---------------|---------------------------|------------------|--------------------|------------------|-------------|---------------|---------------|-------------------|
| fastqc | 6 | NA | 2.00 | NA | 1.04 | NA | 0h 8m | NA | 0.86 | NA |
| cellranger | 6 | NA | 48.00 | NA | 0.03 | NA | 0h 21m | NA | 2.19 | NA |

*Legacy QC/align core-hours (included in post-hackathon legacy HPC footprint):* **3.05** (~$0.07)

### 2c. Daedalus-only downstream (post-hackathon)

| Module | Legacy CPUs | Daedalus CPUs | Legacy req mem (GB/slot) | Daedalus req mem | Legacy avg mem (GB) | Daedalus avg mem | Legacy wall | Daedalus wall | Legacy core-hrs | Daedalus core-hrs |
|--------|-------------|---------------|---------------------------|------------------|--------------------|------------------|-------------|---------------|---------------|-------------------|
| de_go | NA | 4 | NA | 39.00 | NA | 9.90 | NA | 2h 42m | 0.00 | 10.80 |
| project_updates | NA | 1 | NA | 5.00 | NA | 0.12 | NA | 0h 0m | 0.00 | 0.00 |

| Module | Legacy | Daedalus | Notes |
|--------|--------|----------|-------|
| biological_validation | Not run | **Enabled** | Automated checks in Daedalus/Sprocket; no LSF module row in resource_usage CSV |

### Post-hackathon combined HPC footprint (legacy: 5 paired + fastqc + cellranger; Daedalus: 5 paired + de_go + project_updates)

| Metric | Legacy | Daedalus |
|--------|--------|----------|
| Allocated core-hours | 90.16 | 25.88 |
| Est. HPC cost (@ $0.024/core-hr) | $2.16 | $0.62 |
| Core-hour change (Daedalus vs legacy) | — | **71.3%** vs legacy |

## 3. Findings (scoped)

1. **Biohackathon (2 modules):** Daedalus used **9.8** vs legacy **51.0** allocated core-hours on upstream + integrative (~$0.24 vs ~$1.22 HPC).
2. **Post-hackathon (5 paired modules):** Daedalus **15.1** vs legacy **87.1** core-hours on the expanded module set (cluster, cell_types, rshiny added to the comparison).
3. **Shared QC/align:** Add **3.0** legacy core-hours for FastQC + Cell Ranger when costing the full legacy SNAP path.
4. **Biological validation:** Post-hackathon Daedalus adds automated validation (no legacy equivalent in this ROI export).
5. **Analyst time dominates ROI** — see `docs/data-analyst-time.md` and scenario charts in `output/results-posthackathon/`.

## Plots

Charts use the **post-hackathon five-module** scope unless labeled otherwise: `output/results-posthackathon/` (regenerate with `scripts/generate_posthackathon_plots.py`).
