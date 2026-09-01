# KIDS26 Team 15 — Hackathon Runbook

**Project:** Resource-Aware Multi-Project Workflow Orchestrator for Scalable Single-Cell Analysis  
**Tool under test:** SNAP + Sprocket downstream launcher (`launch-snap-downstream.sh`)  
**Analysis repo:** `analyses/sc-rna-seq-snap-Victoria-Knockout/`  
**Time budget:** 6–10 hours (testing + slides + demo)  
**VM / HPC setup:** [vm-hpc-setup.md](../docs/vm-hpc-setup.md) · [vm-local-only-setup.md](../docs/vm-local-only-setup.md)  
**Team roster source:** [stjude-biohackathon-kids26-team15-info.xlsx](./stjude-biohackathon-kids26-team15-info.xlsx)

---

## What we are testing

The new orchestrator replaces manual LSF wiring with:

1. **YAML `workflow_profile` toggles** — turn modules on/off without editing bash flags
2. **Auto resource scaling** — `estimate-snap-downstream-resources.R` reads Cell Ranger metrics
3. **WDL + Sprocket validation** — `sprocket check` / `validate` before submit
4. **One-command launch** — `bash launch-snap-downstream.sh [--submit]`

**Success criteria:** Each track produces a documented artifact (test log, code-review notes, PR, or demo capture). A full upstream Seurat run finishing on HPC is a bonus, not required.

---

## Team and pair assignments

Assignments follow each person's `Task_to_assign` from the team roster, with David paired into testing (no task was listed for him).

| Pair | Members | Track | Primary mission |
|------|---------|-------|-----------------|
| **A — Code review** | Rojina Sapkota + Antonia Chroni | Audit | Review WDL, launcher scripts, resource estimator; file GitHub issues |
| **B — Testing** | Sarthak Dhanke + David George | Execute | Run the test matrix on VM and HPC; log pass/fail with screenshots |
| **C — Docs & PRs** | Lindsey Warren + Rachana Pandey | Quality | PR reviews, troubleshooting docs, test-results write-up |
| **D — Support & demo** | Tanjim Hassan + Jason Vu | Biology + demo | Validate Seurat outputs, HPC golden-path submit, slides and live demo |

### Skill highlights (for cross-support)

| Person | Strengths | HPC / St Jude access |
|--------|-----------|----------------------|
| Antonia Chroni | Tool author; Apptainer, WDL, SNAP orchestration | Yes |
| Rojina Sapkota | WDL, Sprocket, scRNA-seq, Seurat | Yes (St Jude) |
| Sarthak Dhanke | Pipelines, Docker/K8s, Apptainer basics | Remote |
| David George | sc/snRNA-seq, Python, R, cloud | Remote |
| Lindsey Warren | Bash, CI/CD, GitHub, containers/cloud | Memphis (in person) |
| Rachana Pandey | scRNA-seq, HPC, reproducible pipelines | Remote |
| Tanjim Hassan | Seurat QC, scRNA-seq biology, CLI tools | Remote |
| Jason Vu | HPC, data viz, Python/R | Yes (St Jude) |

---

## Environment setup (everyone, first 45 min)

### 1. Clone and enter the analysis repo

```bash
git clone <team15-repo-url>
cd KIDS26-Team15/analyses/sc-rna-seq-snap-Victoria-Knockout
```

### 2. VM smoke test (no LSF required)

```bash
bash scripts/test-downstream-layout.sh
bash launch-snap-downstream.sh          # dry-run: regen WDL, estimate, check, validate
```

### 3. HPC smoke test (Pairs A, B, D — St Jude access)

```bash
module load sprocket R singularity
sprocket --version
Rscript --version
bash launch-snap-downstream.sh          # dry-run on HPC
```

### 4. Create the shared test log

Track C maintains [hackathon-test-results.md](../results/hackathon-test-results.md). All pairs log results there (or a linked Google Doc mirror). One row per test; include: tester, date, environment (VM/HPC), pass/fail, notes, screenshot link.

---

## VM vs HPC strategy

| Capability | VM | HPC |
|------------|:--:|:---:|
| `test-downstream-layout.sh` | ✅ | ✅ |
| `launch-snap-downstream.sh` dry-run | ✅ | ✅ |
| Resource estimation (`estimate-snap-downstream-resources.R`) | ✅ | ✅ |
| YAML / `workflow_profile` editing | ✅ | ✅ |
| `sprocket check` / `validate` | ⚠️ needs `module load sprocket` | ✅ |
| `launch-snap-downstream.sh --submit` | ❌ | ✅ |
| LSF monitoring (`bjobs`) | ❌ | ✅ |
| Email notifications | ❌ | ✅ |

**If VM blocks Sprocket:** VM pairs focus on T1–T6 and T9–T11; HPC pairs (Jason, Rojina, Antonia) run T7–T8 and T13–T16.

**Pre-hackathon prep (team lead):** Submit one upstream-only run on HPC before the event so the demo has artifacts even if the live job is still running.

---

## Test matrix

Record results in `results/hackathon-test-results.md`. Status values: `PASS` | `FAIL` | `SKIP` | `BLOCKED`.

| ID | Test | Owner | VM | HPC | Command / action | Expected result |
|----|------|-------|:--:|:---:|------------------|-----------------|
| **T1** | Layout sanity | B | ✅ | ✅ | `bash scripts/test-downstream-layout.sh` | All expected WDL/input files present |
| **T2** | Dry-run pipeline | B | ✅ | ✅ | `bash launch-snap-downstream.sh` | WDL regen → estimate → `sprocket check` → `validate` pass |
| **T3** | Upstream-only toggle | B | ✅ dry | ✅ submit | Set only `run_upstream: true` in `project_parameters.Config.yaml`, re-launch | WDL contains upstream task only; job submits on HPC |
| **T4** | Three-module chain | B | ✅ dry | ✅ if time | Enable `run_upstream`, `run_integrative`, `run_cluster` | Matches `inputs/downstream_test_3modules.json` intent |
| **T5** | Error handling — bad path | B | ✅ | — | Break `root_dir` or `container_image` in YAML, dry-run | Clear, actionable error message |
| **T6** | Error handling — missing metadata | B | ✅ | — | Rename `project_metadata.tsv`, dry-run | Error cites missing metadata |
| **T7** | Resource scaling | B | ✅ | ✅ | `Rscript scripts/estimate-snap-downstream-resources.R --snap-root . --output inputs/generated_downstream.json --update-yaml` | JSON reflects sample count; `future_globals_*` updated |
| **T8** | Resource override | B | ✅ | — | Re-run estimator with `--estimated-cells-per-sample 8208` | Higher memory/CPU vs default |
| **T9** | Generated YAML overlay | A | ✅ | ✅ | Inspect `inputs/project_parameters.generated.yaml` after dry-run | Master YAML untouched; scaled resources in overlay |
| **T10** | WDL must not be hand-edited | A | ✅ | — | Manually edit `wdl/snap.wdl`, run `sprocket check` | Fails or is overwritten on next launch |
| **T11** | Module dependency chain | A | ✅ dry | — | Toggle middle module off, inspect generated WDL | Skipped module bypassed; chain intact |
| **T12** | `snap_parallel_plan.R` safety | A | — | ✅ | Run upstream with `SNAP_FUTURE_WORKERS=1` vs `2` | No NFS bus errors; document behavior |
| **T13** | HPC golden-path submit | D | — | ✅ | `bash launch-snap-downstream.sh --submit` (upstream only, tmux) | LSF job ID returned |
| **T14** | LSF monitoring | D | — | ✅ | `bjobs -u $USER`; tail task stderr | Job visible; logs accessible |
| **T15** | Email notification | D | — | ✅ | Confirm `CONTACT_EMAIL` in YAML; watch inbox on submit | Workflow submitted email received |
| **T16** | Biology sanity check | D | — | ✅ | Review upstream QC plots / cell counts after partial run | Counts and filters look reasonable (Tanjim signs off) |
| **T17** | Legacy vs new comparison | C | ✅ | — | Compare `launch_full_pipeline.sh` flags vs `workflow_profile` | Side-by-side table for slides |
| **T18** | ROI timing | C | ✅ | — | Time: edit YAML + dry-run vs reading legacy bash deps | Minutes-to-launch-ready for slide |
| **T19** | Troubleshooting doc | C | ✅ | ✅ | Log every real error + fix from all tracks | Entries added to `docs/troubleshooting.md` |
| **T20** | Multi-project dry-run | D | ✅ dry | ✅ if time | `sprocket validate wdl/snap_multi_project.wdl -i inputs/multi_project_downstream.json` | Validates without submit |

**Test log:** Fill in [hackathon-test-results.md](../results/hackathon-test-results.md) as tests complete.

---

## Track deliverables

### Track A — Code review (Rojina + Antonia)

**Output:** `docs/code-review-notes.md` + GitHub issues for any bugs found

| File / area | Review focus |
|-------------|--------------|
| `scripts/launch-snap-sprocket.sh` | Dry-run → validate → submit flow matches docs |
| `scripts/estimate-snap-downstream-resources.R` | Scaling logic, 20% memory headroom, edge cases |
| `scripts/generate-snap-wdl.R` + `wdl/tasks.wdl` | Module toggles, dependency chain |
| `scripts/snap_parallel_plan.R` | `SNAP_FUTURE_WORKERS` defaults; NFS/container safety |
| `scripts/snap-read-config.sh` + `snap_read_config.R` | Config precedence consistency |

**Issue template:**

```markdown
**Severity:** critical / major / minor
**Found by:** <name>
**Steps:** ...
**Expected:** ...
**Actual:** ...
```

---

### Track B — Testing (Sarthak + David)

**Output:** Completed rows in `results/hackathon-test-results.md` for T1–T8

- David validates biology-relevant outputs where applicable (cell counts, QC thresholds).
- Sarthak owns orchestration errors and retry logic.
- Screenshot every PASS and FAIL.

---

### Track C — Docs & PRs (Lindsey + Rachana)

**Output:** Polished docs + reviewed/merged PRs from other tracks

| Task | File |
|------|------|
| Consolidate test log | `results/hackathon-test-results.md` |
| Add VM vs HPC troubleshooting | `docs/troubleshooting.md` |
| Quick-start for testers | `docs/hackathon-quickstart.md` (optional, if time) |
| PR review checklist | See below |
| ROI table for slides | 1 slide: analyst time, core-hours, OOM risk |

**PR review checklist:**

- [ ] Shell scripts: `set -euo pipefail` where appropriate; no hardcoded personal paths
- [ ] YAML changes: only `project_parameters.Config.yaml` edited by hand
- [ ] WDL: generated by `generate-snap-wdl.R`, not hand-edited
- [ ] Docs: commands tested on VM or HPC
- [ ] No secrets, credentials, or private data committed

---

### Track D — Support & demo (Tanjim + Jason)

**Output:** 5-minute demo script + backup screen recording

**Demo script (5 min):**

1. Show `workflow_profile` toggles in `project_parameters.Config.yaml` (30 s)
2. Run dry-run — show `sprocket validate` passing (1 min)
3. Show `inputs/generated_downstream.json` — 8 cores vs legacy 16 (1 min)
4. Show LSF job running or completed upstream QC output (2 min)
5. Next steps: multi-project scatter (30 s)

**Fallback:** If HPC job is still running, demo shows submitted state + pre-recorded walkthrough.

---

## Timeline (10 h max)

| Time | Activity | Who |
|------|----------|-----|
| **0:00–0:15** | Kickoff: pairs, shared test log, VM/HPC access check | All |
| **0:15–0:45** | Setup: clone, T1 smoke test | All |
| **0:45–3:00** | Parallel track work | A: code audit · B: T1–T4 · C: doc skeleton · D: T13 smoke |
| **3:00–3:30** | Sync: blockers, reassign HPC handoffs | All |
| **3:30–5:30** | Continue testing + incorporate findings | B: T5–T8 · A: issues · C: T17–T19 · D: T14–T16 |
| **5:30–7:00** | Slides draft (1–2 slides per track) | All |
| **7:00–8:00** | Demo rehearsal + backup recording | D + Antonia |
| **8:00–8:30** | Buffer for HPC delays / final PR merges | All |

**6-hour version:** Skip T4, T8, T12, T20; shorten slide time to 1 h.

---

## Slide ownership

| Slide | Owner | Content |
|-------|-------|---------|
| Problem | Track C | Manual LSF: 6–8 hr analyst time, fixed 16 CPU |
| Solution | Track B | One YAML + one command; auto-scale diagram |
| How it works | Track A | Module chain + `workflow_profile` screenshot |
| ROI | Track C | Table from T17–T18 |
| Live demo | Track D | Screen recording or live dry-run + HPC status |
| Limitations / next steps | Antonia | VM constraints; Day-1 tuning caveat |
| Team & learnings | All | One bullet per person |

---

## Key commands reference

```bash
# Project root
cd analyses/sc-rna-seq-snap-Victoria-Knockout

# Layout check (no submit)
bash scripts/test-downstream-layout.sh

# Dry-run: regenerate WDL, estimate resources, validate
bash launch-snap-downstream.sh

# Submit to LSF (HPC only)
bash launch-snap-downstream.sh --submit

# Resource estimate only
Rscript scripts/estimate-snap-downstream-resources.R \
  --snap-root . \
  --output inputs/generated_downstream.json \
  --update-yaml

# Monitor after submit
bjobs -u $USER
tail -f out/runs/sc_rna_seq_snap_downstream/_latest/calls/upstream/attempts/0/stderr

# tmux (recommended for long runs)
tmux new -s snap
bash launch-snap-downstream.sh --submit
# Detach: Ctrl+b then d
```

### Example upstream-only `workflow_profile`

```yaml
workflow_profile:
  run_upstream: true
  run_integrative: false
  run_cluster: false
  run_contamination_removal: false
  run_cell_types: false
  run_clone_phylogeny: false
  run_de_go: false
  run_rshiny: false
```

---

## Pre-hackathon checklist (team lead)

- [ ] Cell Ranger complete for Victoria Knockout cohort
- [ ] `project_metadata.tsv` present and valid
- [ ] Apptainer `.sif` image accessible on HPC
- [ ] One upstream-only job pre-submitted (demo backup)
- [ ] All teammates added to GitHub repo / team
- [ ] Shared test log location communicated
- [ ] VM access confirmed; HPC accounts verified for St Jude members
- [ ] `CONTACT_EMAIL` set in `project_parameters.Config.yaml`

---

## Day-of checklist (all pairs)

- [ ] T1 passes on my environment
- [ ] At least one dry-run (T2) logged
- [ ] Findings shared in sync at 3 h mark
- [ ] Deliverable for my track committed or PR opened
- [ ] Slide draft contributed
- [ ] Demo rehearsed once

---

## References

- [scripts/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md) — launcher details and troubleshooting
- [wdl/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/wdl/README.md) — WDL scope and module table
- [Snap-Sprocket-ROI-one-pager.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/docs/Snap-Sprocket-ROI-one-pager.md) — ROI narrative for slides
- [resources-snap.md](../docs/resources-snap.md) — SNAP learning resources
- [resources-sprocket.md](../docs/resources-sprocket.md) — Sprocket learning resources
- [learning-path-wdl-sprocket-containers.md](../docs/learning-path-wdl-sprocket-containers.md) — WDL + containers primer

---

**Maintainer:** Antonia Chroni / KIDS26 Team 15  
**Last updated:** 2026-09-01
