# SNAP Legacy — Combined Run Data (3 Runs)

**Source:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/`  
**Cohort:** Victoria Knockout (4 samples, ~27k cells)

---

## Run 1: FastQC Analysis

### Configuration (from `lsf-script.txt`)

| Parameter | Value |
|-----------|-------|
| CPUs (`-n`) | 2 |
| RAM (`rusage[mem]`) | 16 GB |
| Queue | standard |
| Job name | fastqc-analysis |


### Runtime

| Metric | Value |
|--------|-------|
| **Wall-clock** | Not available (no Job-*-Done.pdf) |
| Samples processed | 4 |
| Output | `results/01-fastqc-reports/` + `results/multiqc_report.html` |

---

## Run 2: Upstream Analysis

### Configuration (from `lsf-script.txt`)

| Parameter | Value |
|-----------|-------|
| CPUs (`-n`) | 16 |
| RAM (`rusage[mem]`) | 30 GB |
| Queue | standard |
| Job name | run-upstream-analysis |

### Runtime (from `Job-run-upstream-analysis-Done.pdf`)

| Metric | Value |
|--------|-------|
| **LSF Job ID** | 320244720 |
| **Start** | Sat Sep 12 09:56:01 2026 |
| **Finish** | Sat Sep 12 11:43:29 2026 |
| **Wall-clock** | **1h 47m 28s** (6,445 sec) |
| **Turnaround time** | 6,454 sec |

### Resource Utilization (from `Job-run-upstream-analysis-Done.pdf`)

| Metric | Value |
|--------|-------|
| CPU time | 7,304 sec |
| Max Memory | 98,523 MB (~96 GB) |
| Average Memory | 47,118 MB (~46 GB) |
| Total Requested Memory | 491,520 MB (~480 GB) |
| Delta Memory | 392,997 MB (~384 GB) |
| Max Processes | 33 |
| Max Threads | 343 |

### Resource Request vs Actual

| Metric | Total Requested | Avg Used | Max Used | Avg Utilization |
|--------|-----------------|----------|----------|-----------------|
| Memory | 491,520 MB (~480 GB) | 47,118 MB (~47 GB) | 98,523 MB (~96 GB) | **~10%** |

**Note:** Total Requested Memory (480 GB) = per-slot request (30 GB) × 16 cores. This is LSF's accounting figure, not a physical allocation. Average Memory (47 GB) is the sustained usage across the job's 1h 47m runtime. Max Memory (96 GB) is a brief peak spike. The 433 GB delta between total requested and average used represents significant over-provisioning waste.

---

## Run 3: Integrative Analysis

### Configuration (from `lsf-script.txt`)

| Parameter | Value |
|-----------|-------|
| CPUs (`-n`) | 10 |
| RAM (`rusage[mem]`) | 96 GB |
| Queue | standard |
| Job name | run-integrative-analysis |

### Runtime (from `Job-run-integrative-analysis-Done.pdf`)

| Metric | Value |
|--------|-------|
| **LSF Job ID** | 320244722 |
| **Start** | Sat Sep 12 11:43:31 2026 |
| **Finish** | Sat Sep 12 11:59:25 2026 |
| **Wall-clock** | **15m 54s** (954 sec) |
| **Turnaround time** | 7,410 sec |

### Resource Utilization (from `Job-run-integrative-analysis-Done.pdf`)

| Metric | Value |
|--------|-------|
| CPU time | 642 sec |
| Max Memory | 24,416 MB (~24 GB) |
| Average Memory | 14,434 MB (~14 GB) |
| Total Requested Memory | 983,040 MB (~960 GB) |
| Delta Memory | 958,624 MB (~936 GB) |
| Max Processes | 17 |
| Max Threads | 136 |

### Resource Request vs Actual

| Metric | Total Requested | Avg Used | Max Used | Avg Utilization |
|--------|-----------------|----------|----------|-----------------|
| Memory | 983,040 MB (~960 GB) | 14,434 MB (~14 GB) | 24,416 MB (~24 GB) | **~1.5%** |

**Note:** Total Requested Memory (960 GB) = per-slot request (96 GB) × 10 cores. Average Memory (14 GB) is the sustained usage across the job's 16m runtime. The 946 GB delta between total requested and average used represents significant over-provisioning waste.

---

## Combined Summary

### Runtime Comparison

| Run | Wall-clock | CPUs | Total Requested Memory | Avg Memory | Memory Efficiency |
|-----|-----------|------|------------------------|------------|-------------------|
| FastQC | N/A | 2 | 16 GB | N/A | N/A |
| Upstream | 1h 47m | 16 | 480 GB | 47 GB | **~10%** |
| Integrative | 16m | 10 | 960 GB | 14 GB | **~1.5%** |
| **Total** | **~2h 4m** | — | — | — | — |


### Resource Utilization Summary

| Metric | Upstream | Integrative | Combined |
|--------|----------|-------------|----------|
| CPU time | 7,304 sec | 642 sec | 7,946 sec (~2.2 CPU-hr) |
| Max Memory | 96 GB | 24 GB | 96 GB (peak) |
| Avg Memory | 47 GB | 14 GB | — |
| Max Processes | 33 | 17 | 33 |
| Max Threads | 343 | 136 | 343 |


### Cell Ranger Summary (from `QC_Summary_CellRanger_Report.tsv`)

| Sample | Est. Cells | Mean Reads/Cell | Median Genes/Cell | Fraction Reads in Cells |
|--------|-----------|-----------------|-------------------|-------------------------|
| DYE_2519 | 4,865 | 18,098 | 913 | 67.9% |
| DYE_2520 | 7,477 | 13,306 | 940 | 68.5% |
| DYE_2521 | 6,351 | 14,855 | 772 | 70.5% |
| DYE_2522 | 8,208 | 11,711 | 803 | 67.9% |
| **Total** | **26,901** | — | — | — |


### Cell Ranger Configuration (from `j1.sh`)

| Parameter | Value |
|-----------|-------|
| Version | CellRanger v8.0.1 |
| CPUs per sample | 6 |
| RAM per sample | 48 GB |
| Samples | 4 |

---

## Key Observations

1. **Memory utilization is abysmal** — upstream used only 10% of total requested memory (47 GB avg / 480 GB requested); integrative used only 1.5% (14 GB avg / 960 GB requested)
2. **CPU utilization is equally poor** — see table below

### CPU Utilization

| Run | Wall-clock | Cores | Allocated Core-time | Actual CPU Time | Avg CPU Utilization |
|-----|-----------|-------|---------------------|-----------------|---------------------|
| Upstream | 6,445s (1h 47m) | 16 | 103,120s | 7,304s | **7.1%** |
| Integrative | 954s (16m) | 10 | 9,540s | 642s | **6.7%** |

**93% of allocated CPU goes unused across both jobs.**



---

## Source Files

| Data | Path |
|------|------|
| FastQC job output | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/fastqc-analysis/job.out` |
| FastQC LSF script | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/fastqc-analysis/lsf-script.txt` |
| Upstream Job Done PDF | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/Job-run-upstream-analysis-Done.pdf` |
| Upstream job output | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/job.out` |
| Upstream job error | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/job.err` |
| Upstream LSF script | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/lsf-script.txt` |
| Integrative Job Done PDF | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/Job-run-integrative-analysis-Done.pdf` |
| Integrative job output | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/job.out` |
| Integrative job error | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/job.err` |
| Integrative LSF script | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/lsf-script.txt` |
| CellRanger QC summary | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/cellranger-analysis/results/03_cellranger_count_summary/DefaultParameters/QC_Summary_CellRanger_Report.tsv` |
| CellRanger j1.sh | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/cellranger-analysis/j1.sh` |
| Legacy launcher | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/launch_full_pipeline.sh` |
| Project config | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/project_parameters.Config.yaml` |

---

