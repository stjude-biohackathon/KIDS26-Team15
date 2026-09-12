# KIDS26 Team 15 — Hackathon Test Log

**Runbook (commands, owners, schedule):** [hackathon-runbook.md](../../project-management/hackathon-runbook.md)  
**Maintained by:** Lindsey Warren and Rachana Pandey · **Analysis repo:** `analyses/sc-rna-seq-snap-Victoria-Knockout/`

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

## Test log (T1–T17)

Owners, commands, and expected results: [hackathon-runbook.md](../../project-management/hackathon-runbook.md#test-matrix-t1t17).

| ID | Test | Tester | Date | Status | Notes | Screenshot / link |
|----|------|--------|------|--------|-------|-------------------|
| T1 | Layout sanity | | | | | |
| T2 | Dry-run pipeline | | | | | |
| T3 | Upstream — WDL toggle | | | | | |
| T4 | Upstream — HPC submit | | | | LSF job ID: | |
| T5 | Upstream — LSF monitoring | | | | | |
| T6 | Upstream — biology QC | | | | Tanjim sign-off | |
| T7 | Upstream + integrative — WDL toggle | | | | | |
| T8 | Upstream + integrative — HPC submit | | | | LSF job ID: | |
| T9 | Integrative — biology QC | | | | Tanjim sign-off | |
| T10 | Resource scaling | | | | | |
| T11 | Generated YAML overlay | | | | | |
| T12 | WDL module chain | | | | | |
| T13 | `snap_parallel_plan.R` safety | | | | | |
| T14 | Email notification | | | | | |
| T15 | Legacy vs new comparison | | | | | |
| T16 | ROI timing | | | | | |
| T17 | Troubleshooting doc | | | | | |

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

### Upstream + integrative chain (`run_upstream` + `run_integrative`)

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
| Lindsey/Rachana — Test log | Lindsey Warren · Rachana Pandey | ☐ | |
| Lindsey/Sarthak — Docs, PRs, ROI | Lindsey Warren | ☐ | |
| Emma/Rojina/Antonia — Code review, development, demo | Emma Bishop | ☐ | |
| Rojina/Antonia — Dry-run and St. Jude HPC testing | Rojina Sapkota | ☐ | |
| Rachana/A.S.M. Tanjim — Testing, biology | Rachana Pandey | ☐ | |
