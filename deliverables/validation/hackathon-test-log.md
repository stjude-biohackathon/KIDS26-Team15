# KIDS26 Team 15 — Hackathon Test Log

**Runbook (commands, owners, schedule):** [hackathon-runbook.md](../../project-management/hackathon-runbook.md)  
**Maintained by:** Lindsey/Sarthak · **Analysis repo:** `analyses/sc-rna-seq-snap-Victoria-Knockout/`

Fill in one row per test. Status: `PASS` | `FAIL` | `SKIP` | `BLOCKED`.

---

## Session summary

| Field | Value |
|-------|-------|
| **Date** | |
| **Environment** | St. Jude HPC |
| **SNAP modules tested** | Upstream · Integrative |
| **SNAP repo commit or branch** | |
| **Tests completed** | / 17 |
| **Tests passed** | |
| **Tests failed** | |
| **Tests blocked** | |
| **Upstream LSF job ID** | |
| **Upstream + integrative LSF job ID** | |
| **Overall readiness** | Ready for demo / Needs fixes / Blocked |

### Blockers encountered

| Blocker | Who hit it | Workaround |
|---------|------------|------------|
| | | |

---

## HPC test log (T1–T17)

See [hackathon-runbook.md](../../project-management/hackathon-runbook.md) for commands.

| ID | Test | SNAP module(s) | Owner | Tester | Date | Status | Notes | Screenshot / link |
|----|------|----------------|-------|--------|------|--------|-------|-------------------|
| T1 | Layout sanity | — | Rachana/A.S.M. Tanjim | | | | `bash scripts/test-downstream-layout.sh` | |
| T2 | Dry-run pipeline | — | Rojina/Antonia | | | | `bash launch-snap-downstream.sh` | |
| T3 | Upstream — WDL toggle | `run_upstream` | Rojina/Antonia | | | | Only `run_upstream: true`; dry-run; WDL has upstream task only | |
| T4 | Upstream — HPC submit | `run_upstream` | Rojina/Antonia | | | | `bash launch-snap-downstream.sh --submit`; record LSF job ID | |
| T5 | Upstream — LSF monitoring | `run_upstream` | Rojina/Antonia | | | | `bjobs -u $USER`; tail upstream stderr | |
| T6 | Upstream — biology QC | `run_upstream` | Rachana/A.S.M. Tanjim | | | | QC plots, cell counts, filters (Tanjim sign-off) | |
| T7 | Upstream + integrative — WDL toggle | `run_upstream` + `run_integrative` | Rojina/Antonia | | | | Both modules true; dry-run; WDL chain correct | |
| T8 | Upstream + integrative — HPC submit | `run_upstream` + `run_integrative` | Rojina/Antonia | | | | `--submit`; record LSF job ID | |
| T9 | Integrative — biology QC | `run_integrative` | Rachana/A.S.M. Tanjim | | | | Harmony outputs, integrated object, UMAP (Tanjim sign-off) | |
| T10 | Resource scaling | upstream + integrative | Rachana/A.S.M. Tanjim | | | | `estimate-snap-downstream-resources.R`; check `generated_downstream.json` | |
| T11 | Generated YAML overlay | — | Rachana/A.S.M. Tanjim | | | | Inspect `project_parameters.generated.yaml` after dry-run | |
| T12 | WDL module chain | upstream → integrative | Rojina/Antonia | | | | Verify dependency chain in generated WDL | |
| T13 | `snap_parallel_plan.R` safety | upstream | Rojina/Antonia | | | | `SNAP_FUTURE_WORKERS=1` vs `2` on upstream run | |
| T14 | Email notification | — | Rojina/Antonia | | | | Confirm `CONTACT_EMAIL` fires on submit | |
| T15 | Legacy vs new comparison | — | Lindsey/Sarthak | | | | `launch_full_pipeline.sh` vs `workflow_profile` table for slides | |
| T16 | ROI timing | — | Lindsey/Sarthak | | | | Minutes to launch-ready on HPC | |
| T17 | Troubleshooting doc | — | Lindsey/Sarthak | | | | Errors logged in `docs/troubleshooting.md` | |

---

## Module run evidence

Record job IDs and key outputs for the two primary module tests.

### Upstream module (`run_upstream: true`)

| Field | Value |
|-------|-------|
| **LSF job ID** | |
| **Submit date/time** | |
| **Wall-clock** | |
| **CPU / memory request** | |
| **Peak RAM** | |
| **Cells post-QC** | |
| **Key output files** | e.g. `seurat_obj_merged_filtered.rds`, QC reports |
| **Biology sign-off (Tanjim)** | ☐ Pass · ☐ Fail · Notes: |

### Integrative module (`run_integrative: true`)

| Field | Value |
|-------|-------|
| **LSF job ID** | |
| **Submit date/time** | |
| **Wall-clock** | |
| **CPU / memory request** | |
| **Peak RAM** | |
| **Key output files** | e.g. `seurat_obj_integrated_harmony.rds`, Harmony reports |
| **Biology sign-off (Tanjim)** | ☐ Pass · ☐ Fail · Notes: |


### Integrative module (`run_upstream` + `run_integrative`)

| Field | Value |
|-------|-------|
| **LSF job ID** | |
| **Submit date/time** | |
| **Wall-clock** | |
| **CPU / memory request** | |
| **Peak RAM** | |
| **Key output files** | e.g. `seurat_obj_integrated_harmony.rds`, Harmony reports |
| **Biology sign-off (Tanjim)** | ☐ Pass · ☐ Fail · Notes: |

---

## Failures and issues

Record any `FAIL` or `BLOCKED` test in detail. Link GitHub issues where filed.

| ID | Severity | Summary | Steps to reproduce | Expected | Actual | Issue link |
|----|----------|---------|-------------------|----------|--------|------------|
| | critical / major / minor | | | | | |

---

## ROI notes (Lindsey/Sarthak — for slides)

### Legacy vs new comparison (T15)

**Legacy evidence:** Antonia Chroni will provide LSF log files from the legacy `launch_full_pipeline.sh` run.

| Dimension | `launch_full_pipeline.sh` | `launch-snap-downstream.sh` |
|-----------|---------------------------|-----------------------------|
| Launch command(s) | | |
| Module toggles | | |
| Resource config | | |
| Validation before submit | | |

### Timing (T16)

| Step | Legacy (min) | New (min) |
|------|--------------|-----------|
| Configure modules | | |
| Set resources | | |
| Launch-ready on HPC | | |

---

## Troubleshooting additions (T17)

List new entries added to [troubleshooting.md](../../docs/troubleshooting.md) during the event.

| Error / symptom | Fix | Added by |
|-----------------|-----|----------|
| | | |

---

## Sign-off

| Pair | Lead | Complete? | Notes |
|------|------|-----------|-------|
| Lindsey/Sarthak — Docs, PRs, ROI | Lindsey Warren | ☐ | |
| Rojina/Antonia — Code, HPC submit, demo | Rojina Sapkota | ☐ | |
| Rachana/A.S.M. Tanjim — Testing, biology | Rachana Pandey | ☐ | |
