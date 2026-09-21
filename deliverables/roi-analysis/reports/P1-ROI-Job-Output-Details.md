# P1 · ROI Analysis: job.out & job.err Details

**Source:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/`

---

## 1. FastQC Analysis — `job.out`

**File:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/fastqc-analysis/job.out`

```
Metadata file: project_metadata.tsv
Sample column: 1, FASTQ column: 3
Processing sample: DYE_2519, replicate: 1
Analysis complete for DYE_2519_rep1_1657569_DYE_2519_S15_L004_R2_001.fastq.gz
Processing sample: DYE_2520, replicate: 1
Analysis complete for DYE_2520_rep1_1657570_DYE_2520_S16_L004_R2_001.fastq.gz
Processing sample: DYE_2521, replicate: 1
Analysis complete for DYE_2521_rep1_1657571_DYE_2521_S17_L004_R2_001.fastq.gz
Processing sample: DYE_2522, replicate: 1
Analysis complete for DYE_2522_rep1_1657572_DYE_2522_S18_L004_R2_001.fastq.gz
```

**Run Summary:**
- 4 samples processed (DYE_2519, DYE_2520, DYE_2521, DYE_2522)
- Each sample processed individually, replicate 1
- All completed successfully (no errors)

---

## 3. Upstream Analysis — `job.out`

**File:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/job.out`

**Total lines:** 495

### Per-Step Chunk Breakdown

#### Step 1: `01_run_SoupX.Rmd` — 21 chunks × 2 runs

| Chunk | Description |
|-------|-------------|
| 1 | logo-file |
| 2 | load-library |
| 3 | set-dir-and-file-names |
| 4-5 | unnamed-chunk-1, read-metadata-define-sample-name |
| 6 | run-SoupX |
| 7 | unnamed-chunk-2 |
| 8 | save-output |
| 9-10 | unnamed-chunk-3, unnamed-chunk-4 |

#### Step 2: `02A_run_seurat_qc.Rmd` — 30 chunks × 6 runs (samples/runs)

| Chunk | Description |
|-------|-------------|
| 1 | logo-file |
| 2 | load-library |
| 3 | set-dir-and-file-names |
| 4 | unnamed-chunk-1 |
| 5 | define-parameters-for-plots |
| 6 | read-process-data |
| 7 | plot-data-before-filtering |
| 8 | run-miQC |
| 9 | filter-data |
| 10-12 | plot-cells-genes, plot-genes-library, plot-data-after-filter |
| 13 | process-seurat |
| 14-15 | unnamed-chunk-2, unnamed-chunk-3 |

**Total for Step 2:** 30 chunks × 6 runs = 180 chunk executions

#### Step 3: `03_run_scDblFinder.Rmd` — 23 chunks × 2 runs

| Chunk | Description |
|-------|-------------|
| 1 | logo-file |
| 2 | load-library |
| 3 | unnamed-chunk-1 |
| 4-5 | set-dir-and-file-names, read-metadata-define-sample-name |
| 6 | run-recoverDoublets-plot-predictions |
| 7 | unnamed-chunk-2 |
| 8 | create-object |
| 9 | filter-object |
| 10-11 | unnamed-chunk-3, unnamed-chunk-4 |

#### Step 4: `04_run_filter_object.Rmd` — 30 chunks

| Chunk | Description |
|-------|-------------|
| 1 | logo-file |
| 2 | load-library |
| 3 | unnamed-chunk-1 |
| 4-5 | set-dir-and-file-names, read-metadata-define-sample-name |
| 6 | define-parameters-for-plots |
| 7 | read-merge-objects |
| 8 | filter-ambient-RNA |
| 9 | filter-doublets |
| 10-12 | unnamed-chunk-2, unnamed-chunk-3, process-seurat |
| 13 | save_seurat |
| 14-15 | unnamed-chunk-4, unnamed-chunk-5 |

#### Step 5: `05_run_summary_report.Rmd` — 53 chunks

| Chunk Range | Description |
|-------------|-------------|
| 1-3 | logo, library, unnamed-chunk-1 |
| 4-5 | set-dir-and-file-names, read-metadata-define-sample-name |
| 6-9 | read-fastqc-analysis, unnamed (×3) |
| 10-11 | read-cellranger-analysis, unnamed |
| 12-14 | read-seurat-qc-plots (file + plot), unnamed |
| 15-16 | read-SoupX, unnamed |
| 17-18 | read-SoupX-plots (file + plot) |
| 19-20 | read-scDblFinder, unnamed |
| 21-22 | read-scDblFinder-plots (file + plot) |
| 23-24 | read-Filter-object, unnamed |
| 25-26 | read-final-plots (file + plot) |
| 27-29 | unnamed-chunk-7, unnamed-chunk-8, unnamed-chunk-9 |

### Key Findings from job.out

1. **Seurat QC is the heaviest step** — 30 chunks × 6 runs = 180 chunk executions (HTML + PDF output per sample)
2. **Every Rmd produces both HTML and PDF** — PDF generation doubles output work
3. **No timestamps or per-step timing** — only chunk progress metadata
4. **Evidence of what ran** — 5 Rmd steps, 11 named chunks + unnamed chunks per step

---

**File:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/fastqc-analysis/job.err`

### Progress Log (per sample)

| Sample | Progress Entries | First | Last |
|--------|-----------------|-------|------|
| DYE_2519 | 20 (Started + 5%→95%) | Started analysis of DYE_2519... | Approx 95% complete for DYE_2519... |
| DYE_2520 | 20 | Started analysis of DYE_2520... | Approx 95% complete for DYE_2520... |
| DYE_2521 | 20 | Started analysis of DYE_2521... | Approx 95% complete for DYE_2521... |
| DYE_2522 | 20 | Started analysis of DYE_2522... | Approx 95% complete for DYE_2522... |


### MultiQC Summary

| Field | Value |
|-------|-------|
| MultiQC version | v1.25 |
| Version check | MultiQC Version v1.35 now available! |
| Reports found | 4 |
| Data output | `multiqc_data` |
| Report output | `multiqc_report.html` |
| Status | MultiQC complete |


---



## 4. Upstream Analysis — `job.err`

**File:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/job.err`

### Step-by-Step Rmd Processing

| Step | Rmd File | Processing | Output |
|------|----------|------------|--------|
| 1 | `01_run_SoupX.Rmd` | `processing file: 01_run_SoupX.Rmd` → `output file: 01_run_SoupX.knit.md` | `plots/01_SoupX/Report-SoupX-2026-09-12.html` |
| 2 | `01_run_SoupX.Rmd` | (re-run for PDF) | `plots/01_SoupX/Report-SoupX-2026-09-12.pdf` |
| 3 | `02A_run_seurat_qc.Rmd` | `processing file: 02A_run_seurat_qc.Rmd` → `output file: 02A_run_seurat_qc.knit.md` | `plots/02_Seurat_qc/DYE_2519/Report-seurat-qc-DYE_2519-2026-09-12.html` |
| 4 | `02A_run_seurat_qc.Rmd` | (re-run for PDF) | `plots/02_Seurat_qc/DYE_2519/Report-seurat-qc-DYE_2519-2026-09-12.pdf` |
| 5 | `02A_run_seurat_qc.Rmd` | (×4 more samples) | DYE_2520, DYE_2521, DYE_2522 reports |
| 6 | `03_run_scDblFinder.Rmd` | `processing file: 03_run_scDblFinder.Rmd` → `output file: 03_run_scDblFinder.knit.md` | `plots/03_scDblFinder/Report-scDblFinder-2026-09-12.html` |
| 7 | `03_run_scDblFinder.Rmd` | (re-run for PDF) | `plots/03_scDblFinder/Report-scDblFinder-2026-09-12.pdf` |
| 8 | `04_run_filter_object.Rmd` | `processing file: 04_run_filter_object.Rmd` → `output file: 04_run_filter_object.knit.md` | `plots/04_Filter_object/Report-Filter-object-2026-09-12.html` |
| 9 | `04_run_filter_object.Rmd` | (re-run for PDF) | `plots/04_Filter_object/Report-Filter-object-2026-09-12.pdf` |
| 10 | `05_run_summary_report.Rmd` | `processing file: 05_run_summary_report.Rmd` → `output file: 05_run_summary_report.knit.md` | `plots/05_Final_summary_report/Report-Final-summary-2026-09-12.html` |
| 11 | `05_run_summary_report.Rmd` | (re-run for PDF) | `plots/05_Final_summary_report/Report-Final-summary-2026-09-12.pdf` |


### Warnings in Upstream `job.err`

| Warning | Count |
|---------|-------|
| `incomplete final line found by readTableHeader on project_metadata.tsv` | 1 |
| `ggrepel: 18 unlabeled data points (too many overlaps). Consider increasing max.overlaps` | 4 |
| `ggrepel: 15 unlabeled data points (too many overlaps). Consider increasing max.overlaps` | 4 |
| `Package microtype Warning: Unable to apply patch footnote` | 4 |
| `Package fancyhdr Warning: \headheight is too small` | 4 |


### R Operations (from progress bars)

**`02A_run_seurat_qc.Rmd` per-sample:**
- `Calculating gene variances` (0→100%)
- `Calculating feature variances of standardized and clipped values` (0→100%)

---

## 5. Integrative Analysis — `job.out`

**File:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/job.out`

### Step-by-Step Rmd Processing

| Step | Rmd File | Processing | Output |
|------|----------|------------|--------|
| 1 | `01-integrative-analysis.Rmd` | `processing file: 01-integrative-analysis.Rmd` | `plots/Report-integrative-analysis-harmony-2026-09-12.html` |
| 2 | `01-integrative-analysis.Rmd` | (re-run for PDF) | `plots/Report-integrative-analysis-harmony-2026-09-12.pdf` |

### R Operations (from progress bars)

**`01-integrative-analysis.Rmd`:**
- 6 iterations of: 0→100% progress (gene variance calculations)
- `Using method 'umap'` (dimensionality reduction)
- Final: `output file: 01-integrative-analysis.knit.md`

**Total job.out lines:** 58

---

## 6. Integrative Analysis — `job.err`

**File:** `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/job.err`

### Warnings in Integrative `job.err`

| Warning | Count |
|---------|-------|
| `Package microtype Warning: Unable to apply patch footnote` | 1 |
| `Package fancyhdr Warning: \headheight is too small (68.9055pt): Make it at least 124.52832pt` | 1 |

### Additional Info

```
INFO:    Terminating squashfuse_ll after timeout
INFO:    Timeouts can be caused by a running background process
```

**Note:** This indicates the Singularity container terminated after timeout — likely cleanup after job completion.

---

## 7. Summary of Key Data from job.out/job.err

| Module | job.out Lines | job.err Lines | Steps Run | Warnings |
|--------|--------------|---------------|-----------|----------|
| FastQC | 10 | 88 | 4 samples + MultiQC | 0 |
| Upstream | 495 | 317 | 5 Rmd files (SoupX → Summary) | 13 |
| Integrative | 58 | 76 | 1 Rmd file (×2 runs) | 2 |

### Critical Findings from job.err/job.out

1. **Seurat QC is the heaviest step** — 30 chunks × 6 runs = 180 chunk executions (from upstream `job.out`)
2. **Container timeout in integrative** — `squashfuse_ll after timeout` message in job.err (informational, not failure)
3. **ggrepel warnings** — label overlap warnings suggest visualization could be improved
4. **microtype warnings** — LaTeX patching issue (cosmetic, not functional)
5. **No actual errors** — all jobs completed successfully (LSF reported "Successfully completed")
6. **No per-step timing in job.out** — only chunk progress metadata (no timestamps)

---

## 8. File Locations

| File | Path |
|------|------|
| FastQC job.out | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/fastqc-analysis/job.out` |
| FastQC job.err | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/fastqc-analysis/job.err` |
| Upstream job.out | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/job.out` |
| Upstream job.err | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/upstream-analysis/job.err` |
| Integrative job.out | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/job.out` |
| Integrative job.err | `analyses/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/analyses/integrative-analysis/job.err` |

---

