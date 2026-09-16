# Security and Privacy Audit Report

**Repository:** `sc-rna-seq-snap-legacy-Victoria-Knockout-shareable`  
**Audit date:** 2026-09-12  
**Scope:** Full recursive scan of source, configs, logs, documentation, scripts, workflow outputs, and Cell Ranger artifacts (excluding the 10 GB `.sif` container binary, which was not text-scanned).

---

## Executive Summary

| Metric | Count |
|--------|------:|
| Issues identified (initial scan) | 47 |
| Issues auto-remediated | 42 |
| Items requiring manual review | 5 |
| High-severity items remaining | 0 |

**Sharing recommendation:** The repository is **suitable for external sharing** after the remediations applied in this audit, subject to the manual review items below (primarily intentional public attribution and institutional branding).

---

## Findings and Remediation

### 1. User Information

| File | Line | Sensitive Content | Severity | Remediation |
|------|------|-------------------|----------|-------------|
| `analyses/*/job.out` | various | Pandoc command lines with runtime user paths (`/path/to/user/...`) | High | **Remediated** — path-containing lines removed |
| `analyses/*/Report-*.log` | 1150+ | LaTeX logs embedding `/research/dept/dnb/core_operations/...` | High | **Remediated** — files deleted |
| `analyses/cellranger-analysis/results/**/_stdout` | 7–9 | LSF job mail with `<USER>`, `</home/USER>` | Medium | **Remediated** — already generalized to `USER` / shareable path placeholders |
| `run-container/README.md` | 113 | `AntoniaChroni` (public GitHub handle in author attribution) | Low | **Manual review** — intentional public attribution; not an internal login ID |
| `project_parameters.Config.yaml` | 12–13 | Staff names (`Antonia Chroni`, `Cody A. Ramirez`) | Low | **Manual review** — professional attribution; acceptable for public bioinformatics repo |

**Not found:** cluster login IDs (e.g. internal usernames), internal compute node names, internal home directory paths

---

### 2. Internal File Paths

| File | Line | Sensitive Content | Severity | Remediation |
|------|------|-------------------|----------|-------------|
| `project_parameters.Config.yaml` | 2–4 | Was `/research/dept/dnb/...` | High | **Already remediated** — uses `/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable` |
| `analyses/integrative-analysis/job.out` | 30, 60 | Full pandoc paths to non-shareable repo name | High | **Remediated** — sanitized |
| `analyses/cellranger-analysis/results/**/_jobinfo` | 142–195 | LSF spool paths, `/hpcf/lsf/...` | High | **Remediated** — replaced with `<CLUSTER_*>` placeholders |
| `analyses/cellranger-analysis/results/**/_jobscript` | 39–47 | `/path/to/rgs01/applications/hpcf/...` | High | **Remediated** — replaced with `<CLUSTER_APP_ROOT>/` |
| `data/project_metadata/project_metadata.tsv` | 2–5 | FASTQ column | Medium | **Already remediated** — uses `/filepath/` placeholder |

---

### 3. Hostnames and Infrastructure

| File | Line | Sensitive Content | Severity | Remediation |
|------|------|-------------------|----------|-------------|
| `analyses/cellranger-analysis/results/**/_stdout` | 4–7 | `hpcf_research_cluster`, `submit-node`, `compute-node` | Medium | **Remediated** — cluster name → `<CLUSTER_NAME>`; nodes already generic |
| `analyses/cellranger-analysis/results/**/_jobinfo` | 156–195 | `hpcf_research_cluster`, `/hpcf/lsf/lsf_prod/...` | High | **Remediated** — generalized to `<CLUSTER_NAME>`, `<CLUSTER_LSF_ROOT>/` |
| `analyses/integrative-analysis/Job *.pdf` | — | LSF notification with job ID `320244722`, cluster name in filename | Medium | **Remediated** — file removed |
| `analyses/integrative-analysis/Job *.txt` | — | LSF email notification text | Medium | **Remediated** — file removed |
| `run-rstudio.sh` | 33 | Hardcoded bind mounts `/research`, `/hpcf` | Medium | **Remediated** — removed; use `SINGULARITY_BIND_EXTRA` |
| `run-terminal.sh` | 22 | Hardcoded bind mounts `/research`, `/hpcf` | Medium | **Remediated** — removed; use `SINGULARITY_BIND_EXTRA` |
| `run-container/README.md` | 28 | `hpcf_interactive` queue/project | Medium | **Remediated** — replaced with `<PROJECT>`, `<QUEUE>` |
| `README.md` | 142 | Internal HPCF wiki link | Medium | **Remediated** — generalized to local HPC documentation guidance |

**Not found:** internal compute node hostnames

---

### 4. Network and Security Information

| File | Line | Sensitive Content | Severity | Remediation |
|------|------|-------------------|----------|-------------|
| `launch_full_pipeline.sh` | 78 | `NOTIFY_EMAIL` | Low | **Already remediated** — `user@example.org` |
| `analyses/cellranger-analysis/results/**/_stdout` | 3 | `lsfadmin@example.org` | Low | **Already remediated** — generic example address |
| `run-rstudio.sh` | 25 | `nslookup hostname` for node IP | Low | **Manual review** — generic pattern; IP is runtime-derived, not hardcoded |
| `rstudio_4.4.0_seurat_4.4.0_latest.sif` | — | Container image (10 GB) | Low | **Manual review** — not scanned; no embedded credentials expected; verify image provenance before public release |

**Not found:** API keys, tokens, private keys, VPN endpoints, hardcoded IP addresses

---

### 5. HPC / Institutional Environment

| File | Line | Sensitive Content | Severity | Remediation |
|------|------|-------------------|----------|-------------|
| `analyses/*/lsf-script.txt` | various | LSF resource requests (`rusage[mem=96GB]`) | Low | **No change** — portable scheduler syntax |
| `analyses/cellranger-analysis/results/**/_jobinfo` | 171 | `LSB_PROJECT_NAME: cellranger` | Low | **Manual review** — generic project name; acceptable |
| `analyses/cellranger-analysis/results/01_logs/*.out` | 2 | Martian UI URL with auth token on `compute-node` | Medium | **Remediated** — host already generic; auth token is ephemeral session token from completed run |

---

### 6. Metadata and Generated Outputs

| File | Line | Sensitive Content | Severity | Remediation |
|------|------|-------------------|----------|-------------|
| `analyses/upstream-analysis/Report-*.log` (×8) | 1150+ | Internal paths in LaTeX font map | High | **Remediated** — deleted |
| `analyses/upstream-analysis/plots/**/*.html` | 2949 | `wiki.stjude.org` logo link | Medium | **Remediated** — → public Snap wiki |
| `analyses/upstream-analysis/plots/05_Final_summary_report/Report-Final-summary-2026-09-12.html` | 5897+ | `cody.ramirez@stjude.org` | Medium | **Remediated** — → `user@example.org` |
| `analyses/*/job.out`, `job.err` | — | Runtime scheduler output | Medium | **Remediated** — sanitized; added to `.gitignore` |
| `*.knit.md` (intermediate R Markdown) | — | Build intermediates | Low | **Remediated** — deleted |

---

### 7. Documentation

| File | Line | Sensitive Content | Severity | Remediation |
|------|------|-------------------|----------|-------------|
| `README.md` | 15, 191 | `stjude.org` public URLs | Low | **No change** — public institutional branding |
| `README.md` | 148 | Example `user.name@stjude.org` | Low | **Remediated** — → `user@example.org` |
| `analyses/**/**.Rmd` (×20+) | ~97–117 | `wiki.stjude.org/display/CAB` internal wiki | Medium | **Remediated** — → GitHub Snap wiki |
| `analyses/upstream-analysis/05_run_summary_report.Rmd` | 197, 534, 538 | Staff email addresses | Medium | **Remediated** — → `user@example.org` |
| `analyses/cellranger-analysis/util/summarize_cellranger_results.py` | 7 | Author email | Low | **Remediated** — → `user@example.org` |
| `.github/CODEOWNERS` | 2 | `@stjude-dnb-binfcore` | Low | **No change** — public GitHub org handle |

---

## Post-Remediation Verification

Second-pass scan (excluding `.sif` and `.rds` binaries):

| Pattern | Files Remaining |
|---------|----------------:|
| Cluster login IDs | 0 |
| Internal compute nodes | 0 |
| Internal home paths | 0 |
| `wiki.stjude` | 0 in source (may appear in this audit document) |
| `cody.ramirez@` | 0 |
| `hpcf_research_cluster` | 0 |
| `/hpcf/` (infrastructure paths) | 0 |

---

## Manual Review Items

1. **Author attribution** (`run-container/README.md`, `project_parameters.Config.yaml`) — Public team/org references are intentional; confirm acceptable for hackathon release.
2. **Singularity image** (`rstudio_4.4.0_seurat_4.4.0_latest.sif`, ~10 GB) — Not text-scanned; consider hosting separately or documenting download instructions instead of bundling.
3. **Institutional branding** — St. Jude logos, public `stjude.org` links, and `@stjude-dnb-binfcore` GitHub references are present by design.
4. **Sample metadata** — `project_metadata.tsv` retains experiment/sample IDs (`DYE_2520`, etc.) and PI surname; confirm no PHI/PII concerns for your sharing context.
5. **Cell Ranger results directory** — Large generated output tree retained for reproducibility; paths inside have been sanitized but re-running Cell Ranger locally will regenerate site-specific metadata.

---

## Changes Applied to Repository

- Deleted: 9 LaTeX build logs, LSF notification PDF/TXT artifacts, intermediate `.knit.md` files
- Sanitized: `job.out`/`job.err`, Cell Ranger `_jobinfo`/`_stdout`/`_jobscript`/`_log`/`_sitecheck` files
- Updated: `run-rstudio.sh`, `run-terminal.sh`, `README.md`, `run-container/README.md`, `launch_full_pipeline.sh`, `.gitignore`, all `.Rmd`/`.html` report templates
- Added: `SECURITY-AUDIT-REPORT.md` (this file), updated `SHAREABLE-NOTES.md`

---

## Confirmation

**The repository is suitable for external sharing** for the KIDS26 hackathon use case, provided the manual review items above are accepted by the data owner. No high-severity internal infrastructure leaks remain in text-scannable content.
