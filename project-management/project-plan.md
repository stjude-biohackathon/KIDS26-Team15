# Project Plan

**Runbook:** [hackathon-runbook.md](./hackathon-runbook.md)  
**VM / HPC setup:** [vm-hpc-setup.md](../docs/vm-hpc-setup.md) · [vm-local-only-setup.md](../docs/vm-local-only-setup.md)  
**Test log:** [hackathon-test-results.md](../results/hackathon-test-results.md)  
**SNAP overview:** [resources-snap.md](../docs/resources-snap.md)  
**Analysis repo:** `analyses/sc-rna-seq-snap-Victoria-Knockout/`

---

## Goal

By the end of the hackathon (6–10 hours), the team will have **tested, documented, and demonstrated** the new SNAP + Sprocket resource-aware downstream orchestrator (`launch-snap-downstream.sh`) and shown measurable ROI over the legacy `launch_full_pipeline.sh` path.

Specific outcomes:

1. Test matrix (T1–T20) executed and logged with pass/fail evidence
2. Code-review notes and GitHub issues for any bugs found
3. Updated troubleshooting docs from real VM/HPC errors
4. 5-minute demo + slides showing YAML toggles, auto-scaling, and one-command launch

A full upstream Seurat run completing on HPC is a **bonus**, not required for success.

---

## Tools

| Tool | Role |
|------|------|
| [sc-rna-seq-snap](https://github.com/stjude-dnb-binfcore/sc-rna-seq-snap) | Single-cell analysis modules (upstream → R Shiny); see [resources-snap.md](../docs/resources-snap.md) |
| [Sprocket](https://github.com/stjude-rust-labs/sprocket) | WDL workflow runner on St. Jude HPC |
| WDL | Workflow definition (`wdl/snap.wdl`, `snap_multi_project.wdl`) |
| `launch-snap-downstream.sh` | One-command launcher (dry-run or `--submit`) |
| `estimate-snap-downstream-resources.R` | Auto-scale LSF CPU/memory from Cell Ranger metrics |
| Apptainer/Singularity | Container runtime for R/Seurat modules |
| LSF | Job scheduler on St. Jude HPC |
| Victoria Knockout cohort | Test dataset (4 samples, ~27k cells) |

---

## First Tasks

### Before the event (team lead)

- [ ] Cell Ranger complete for Victoria Knockout — Antonia
- [ ] `project_metadata.tsv` present and valid — Antonia
- [ ] Apptainer `.sif` image accessible on HPC — Antonia
- [ ] One upstream-only job pre-submitted as demo backup — Antonia + Jason
- [ ] All teammates added to GitHub repo — Antonia
- [ ] VM and HPC access confirmed for each pair — Antonia

### Day of — Phase 0 (everyone, first 45 min)

- [ ] Clone repo and enter analysis directory — All
- [ ] T1: `bash scripts/test-downstream-layout.sh` — All pairs
- [ ] T2: `bash launch-snap-downstream.sh` dry-run — All pairs
- [ ] Open shared test log — Track C

### Day of — Parallel tracks (hours 1–5)

- [ ] Track A: Code audit of launcher, estimator, WDL generator — Rojina + Antonia
- [ ] Track B: Run T1–T8, log results with screenshots — Sarthak + David
- [ ] Track C: Maintain test log, review PRs, draft troubleshooting — Lindsey + Rachana
- [ ] Track D: HPC golden-path submit (T13–T16), capture demo assets — Jason + Tanjim

### Day of — Wrap-up (hours 5–8)

- [ ] Sync at 3 h mark: redistribute HPC handoffs for blocked VM pairs — All
- [ ] Slides draft (1–2 slides per track) — All
- [ ] Demo rehearsal + backup screen recording — Track D
- [ ] Sign-off in test-results log — All track leads

---

## Milestones

| When | Focus | Expected outcome |
|------|-------|------------------|
| **Hour 0–1** | Setup, clone, smoke tests (T1–T2) | Everyone passes layout + dry-run on their environment |
| **Hour 1–3** | Parallel track work | Each pair has first deliverable started |
| **Hour 3** | Sync + blocker triage | VM/HPC gaps documented; HPC pairs pick up blocked tests |
| **Hour 3–5** | Continue testing + incorporate findings | T1–T16 logged; issues filed; troubleshooting updated |
| **Hour 5–7** | Slides + demo prep | 6–8 slides drafted; demo rehearsed once |
| **Hour 7–8** | Buffer | PR merges, final sign-off, backup recording if HPC slow |

**6-hour compressed version:** Skip T4, T8, T12, T20; shorten slide time to 1 h.

---

## Definition of Done

The project is complete when:

- [ ] At least **12 of 20 tests** logged with status in `results/hackathon-test-results.md`
- [ ] At least **one HPC submit** (T13) documented with job ID
- [ ] **Code-review notes** committed or issues filed for any major findings
- [ ] **Troubleshooting doc** updated with at least 3 real errors + fixes
- [ ] **5-minute demo** rehearsed (live or recorded fallback)
- [ ] **Slides** cover: problem, solution, how it works, ROI, limitations

### If done early — stretch goals

- Test `snap_multi_project.wdl` (T20)
- Compare `SNAP_FUTURE_WORKERS=1` vs `2` on HPC (T12)
- Open PRs for any quick fixes found during code review
- Add GitHub Actions check: `bash scripts/test-downstream-layout.sh`

---

## Risks and Questions

| Risk | Mitigation | Owner |
|------|------------|-------|
| VM cannot run `sprocket` or submit to LSF | VM pairs do dry-run + YAML tests (T1–T6); HPC pairs run T7+ | Antonia |
| Long upstream runtime blocks demo | Pre-submit one job before event; demo shows submitted state + recording | Jason |
| Apptainer `.sif` missing on VM | Resource estimation and config tests only on VM | Sarthak |
| NFS bus errors with parallel R workers | Default `SNAP_FUTURE_WORKERS=1`; document in T12 | Rojina |
| Remote teammates lack HPC access | Pair with St Jude members (Jason, Rojina) for submit tests | Antonia |
| Git clone slow on event day | Pre-clone on shared drive or distribute zip | Lindsey |

**Open questions:**

- [ ] Which Slack channel is the team channel?
- [ ] Are hackathon VMs pre-loaded with `module load sprocket R singularity`?
- [ ] Is Victoria Knockout Cell Ranger output staged and accessible to all testers?
