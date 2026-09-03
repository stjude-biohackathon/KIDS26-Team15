# KIDS26 Team 15 — Hackathon Test Results

**Owners (Track C):** Lindsey Warren + Rachana Pandey  
**Runbook:** [hackathon-runbook.md](../project-management/hackathon-runbook.md)  
**Setup:** [vm-hpc-setup.md](../docs/vm-hpc-setup.md) (HPC) · [vm-local-only-setup.md](../docs/vm-local-only-setup.md) (no HPC) · [resources-snap.md](../docs/resources-snap.md)  
**Analysis repo:** `analyses/sc-rna-seq-snap-Victoria-Knockout/`

Fill in one row per test during the event. Status values: `PASS` | `FAIL` | `SKIP` | `BLOCKED`.

Use **T1–T20** if you have St. Jude HPC access. Use **L1–L18** for VM/local-only testing.

---

## Session summary

| Field | Value |
|-------|-------|
| **Date** | |
| **Setup mode** | HPC / local-only / both |
| **Environment(s) tested** | Shared VM / runner laptop / HPC |
| **SNAP repo commit or branch** | |
| **Tests completed** | / 20 (HPC) or / 18 (local) |
| **Tests passed** | |
| **Tests failed** | |
| **Tests blocked** | |
| **Overall readiness** | Ready for demo / Needs fixes / Blocked |

### Blockers encountered

| Blocker | Who hit it | Workaround |
|---------|------------|------------|
| | | |

---

## Local / no-HPC test log (L1–L18)

See [vm-local-only-setup.md](../docs/vm-local-only-setup.md) for commands.

| ID | Test | Tier | Tester | Date | Env | Status | Notes | Screenshot / link |
|----|------|------|--------|------|-----|--------|-------|-------------------|
| L1 | Layout sanity | 1 | | | VM | | `test-downstream-layout.sh` | |
| L2 | WDL generation | 1 | | | VM | | `generate-snap-wdl.R` | |
| L3 | Resource estimation | 1 | | | VM | | `estimate-snap-downstream-resources.R` | |
| L4 | Upstream-only WDL | 1 | | | VM | | `run_upstream: true` only | |
| L5 | Three-module WDL | 1 | | | VM | | upstream + integrative + cluster | |
| L6 | `sprocket check` | 1 | | | VM | | | |
| L7 | `sprocket validate` | 1 | | | VM | | `--config sprocket.local.toml` | |
| L8 | Docker image in YAML | 1 | | | VM | | `docker://achroni/rstudio_…` | |
| L9 | Error — bad path | 1 | | | VM | | | |
| L10 | Error — missing metadata | 1 | | | VM | | | |
| L11 | Generated YAML overlay | 1 | | | VM | | | |
| L12 | Module dependency chain | 1 | | | VM | | | |
| L13 | Legacy vs new comparison | 1 | | | VM | | for slides | |
| L14 | ROI timing | 1 | | | VM | | minutes to validate-ready | |
| L15 | Troubleshooting doc | 1 | | | VM | | | |
| L16 | Docker image pull | 2 | | | Runner | | stretch | |
| L17 | Live upstream run | 2 | | | Runner | | `sprocket run` + local.toml | |
| L18 | Biology sanity | 2 | | | Runner | | Tanjim sign-off | |

---

## HPC test log (T1–T20)

See [hackathon-runbook.md](../project-management/hackathon-runbook.md) for commands.

| ID | Test | Owner | Tester | Date | Env | Status | Notes | Screenshot / link |
|----|------|-------|--------|------|-----|--------|-------|-------------------|
| T1 | Layout sanity | B | | | VM / HPC | | `bash scripts/test-downstream-layout.sh` | |
| T2 | Dry-run pipeline | B | | | VM / HPC | | `bash launch-snap-downstream.sh` | |
| T3 | Upstream-only toggle | B | | | VM / HPC | | `run_upstream: true` only in YAML | |
| T4 | Three-module chain | B | | | VM / HPC | | upstream + integrative + cluster | |
| T5 | Error handling — bad path | B | | | VM | | Break `root_dir` or `container_image` | |
| T6 | Error handling — missing metadata | B | | | VM | | Rename `project_metadata.tsv` | |
| T7 | Resource scaling | B | | | VM / HPC | | `estimate-snap-downstream-resources.R` | |
| T8 | Resource override | B | | | VM | | `--estimated-cells-per-sample 8208` | |
| T9 | Generated YAML overlay | A | | | VM / HPC | | Inspect `project_parameters.generated.yaml` | |
| T10 | WDL must not be hand-edited | A | | | VM | | Edit `wdl/snap.wdl`, re-run check | |
| T11 | Module dependency chain | A | | | VM | | Toggle middle module off | |
| T12 | `snap_parallel_plan.R` safety | A | | | HPC | | `SNAP_FUTURE_WORKERS=1` vs `2` | |
| T13 | HPC golden-path submit | D | | | HPC | | `launch-snap-downstream.sh --submit` | |
| T14 | LSF monitoring | D | | | HPC | | `bjobs -u $USER`; tail stderr | |
| T15 | Email notification | D | | | HPC | | Confirm `CONTACT_EMAIL` fires | |
| T16 | Biology sanity check | D | | | HPC | | QC plots / cell counts (Tanjim sign-off) | |
| T17 | Legacy vs new comparison | C | | | VM | | `launch_full_pipeline.sh` vs `workflow_profile` | |
| T18 | ROI timing | C | | | VM | | Minutes to launch-ready | |
| T19 | Troubleshooting doc | C | | | VM / HPC | | Errors logged in `troubleshooting.md` | |
| T20 | Multi-project dry-run | D | | | VM / HPC | | `snap_multi_project.wdl` validate | |

---

## Failures and issues

Record any `FAIL` or `BLOCKED` test in detail. Link GitHub issues where filed.

| ID | Severity | Summary | Steps to reproduce | Expected | Actual | Issue link |
|----|----------|---------|-------------------|----------|--------|------------|
| | critical / major / minor | | | | | |

---

## ROI notes (Track C — for slides)

### Legacy vs new comparison (L13 / T17)

| Dimension | `launch_full_pipeline.sh` | `launch-snap-downstream.sh` |
|-----------|---------------------------|-----------------------------|
| Launch command(s) | | |
| Module toggles | | |
| Resource config | | |
| Validation before submit | | |

### Timing (L14 / T18)

| Step | Legacy (min) | New (min) |
|------|--------------|-----------|
| Configure modules | | |
| Set resources | | |
| Launch-ready | | |

---

## Troubleshooting additions (L15 / T19)

List new entries added to [troubleshooting.md](../docs/troubleshooting.md) during the event.

| Error / symptom | Environment | Fix | Added by |
|-----------------|-------------|-----|----------|
| | VM / HPC | | |

---

## Sign-off

| Track | Lead | Complete? | Notes |
|-------|------|-----------|-------|
| A — Code review | Rojina Sapkota | ☐ | |
| B — Testing | Sarthak Dhanke | ☐ | |
| C — Docs & PRs | Lindsey Warren | ☐ | |
| D — Support & demo | Jason Vu | ☐ | |
