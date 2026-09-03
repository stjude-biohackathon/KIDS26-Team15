# Project Plan

**Runbook:** [hackathon-runbook.md](./hackathon-runbook.md)  
**VM / HPC setup:** [vm-hpc-setup.md](../docs/vm-hpc-setup.md) · [vm-local-only-setup.md](../docs/vm-local-only-setup.md)  
**Test log:** [hackathon-test-results.md](../results/hackathon-test-results.md)  
**SNAP overview:** [resources-snap.md](../docs/resources-snap.md)  
**Analysis repo:** `analyses/sc-rna-seq-snap-Victoria-Knockout/`

---

## Goal

By the end of the hackathon (Day 1: 4 h · Day 2: 8 h · Day 3: 4 h afternoon + demo 3:00–6:00 PM), the team will have **tested, documented, and demonstrated** the new SNAP + Sprocket resource-aware downstream orchestrator (`launch-snap-downstream.sh`) and shown measurable ROI over the legacy `launch_full_pipeline.sh` path.

Specific outcomes:

1. Test matrix (T1–T20) executed and logged with pass/fail evidence
2. Code-review notes and GitHub issues for any bugs found
3. Updated troubleshooting docs from real VM/HPC errors
4. Organizer **3-slide template** deck + **2-minute lightning talk** + live demo for judges (3:00–6:00 PM, Day 3)

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

- [x] Cell Ranger complete for Victoria Knockout — Antonia
- [ ] `project_metadata.tsv` present and valid — Antonia
- [ ] Apptainer `.sif` image accessible on HPC — Antonia
- [x] One upstream-only job pre-submitted as demo backup — Antonia
- [ ] All teammates added to GitHub repo — Antonia
- [ ] VM and HPC access confirmed for each pair — Antonia

### Day 1 — Align and start (4 h)

- [ ] Kickoff: confirm pairs (A/B/C/D) and shared test log — All
- [ ] Clone repo and enter analysis directory — All
- [ ] T1: `bash scripts/test-downstream-layout.sh` — All
- [ ] T2: `bash launch-snap-downstream.sh` dry-run — All
- [ ] Open shared test log — Track C
- [ ] Track A: Code audit started — Rojina + Antonia
- [ ] Track B: T1–T4 logged with screenshots — Sarthak
- [ ] Track D: HPC submit plan confirmed — Tanjim + Antonia
- [ ] End-of-day sync: blockers and Day 2 priorities — All

### Day 2 — Build and learn (8 h)

- [ ] Track A: Code audit of launcher, estimator, WDL generator (T9–T12) — Rojina + Antonia
- [ ] Track B: Run T5–T8, log results with screenshots — Sarthak
- [ ] Track C: Maintain test log, review PRs, draft troubleshooting (T17–T19) — Lindsey + Rachana
- [ ] Track D: HPC golden-path submit (T13–T16), capture demo assets — Tanjim + Antonia
- [ ] Mid-day sync: redistribute HPC handoffs for blocked VM pairs — All
- [ ] Draft 3-slide deck content (organizer template) — Track C + D

### Day 3 — Explain and hand off (4 h afternoon + demo 3:00–6:00 PM)

- [ ] Final test sign-off in test-results log — All track leads
- [ ] Finalize 3-slide deck — Track C + D
- [ ] Rehearse 2-min lightning talk (2–4 presenters) — Tanjim + Antonia (+ Sarthak/Lindsey)
- [ ] **3:00–4:00 PM:** Lightning presentations to judges (2 min, 3-slide template)
- [ ] **After lightning:** Live demo in demo room; capture judge Q&A and feedback
- [ ] **4:00–6:00 PM:** Demo session continues; feedback documented — Presenters + Track C

---

## Milestones

| When | Focus | Expected outcome |
|------|-------|------------------|
| **Day 1 (4 h)** | Setup, clone, smoke tests (T1–T2), start parallel tracks | Everyone passes layout + dry-run; T1–T4 started; test log open |
| **Day 1 end** | Sync + blocker triage | VM/HPC gaps documented; Day 2 priorities assigned |
| **Day 2 (8 h)** | Parallel track work + documentation | T1–T16 logged; issues filed; troubleshooting updated |
| **Day 2 end** | 3-slide content drafted | Slide 1–3 content ready; demo screenshots captured |
| **Day 3 (4 h afternoon)** | Polish + rehearse | Deck final; lightning + live demo rehearsed once |
| **Day 3, 3:00–4:00 PM** | Lightning talks | 2-min presentation to judges (2–4 presenters, 3-slide template) |
| **Day 3, 3:00–6:00 PM** | Live demo + judge feedback | Demo room walkthrough; Q&A captured |

---

## Definition of Done

The project is complete when:

- [ ] At least **12 of 20 tests** logged with status in `results/hackathon-test-results.md`
- [ ] At least **one HPC submit** (T13) documented with job ID
- [ ] **Code-review notes** committed or issues filed for any major findings
- [ ] **Troubleshooting doc** updated with at least 3 real errors + fixes
- [ ] **3-slide deck** (organizer template) covers: problem, solution, results/impact
- [ ] **2-minute lightning talk** rehearsed with 2–4 presenters
- [ ] **Live demo** rehearsed (or recorded fallback ready)

### If done early — stretch goals

- Test `snap_multi_project.wdl` (T20) — multiple projects in parallel
- Compare `SNAP_FUTURE_WORKERS=1` vs `2` on HPC (T12)
- Open PRs for any quick fixes found during code review
- Add GitHub Actions check: `bash scripts/test-downstream-layout.sh`
- Document extension path to other SNAP modalities (sc-ATAC, sc-PARSE) and multi-omics pairing (sc-RNA-seq + sc-ATAC)

---

## Risks and Questions

| Risk | Mitigation | Owner |
|------|------------|-------|
| VM cannot run `sprocket` or submit to LSF | VM pairs do dry-run + YAML tests (T1–T6); HPC pairs run T7+ | Antonia |
| Long upstream runtime blocks demo | Pre-submit one job before event; demo shows submitted state + recording | Antonia |
| Apptainer `.sif` missing on VM | Resource estimation and config tests only on VM | Sarthak |
| NFS bus errors with parallel R workers | Default `SNAP_FUTURE_WORKERS=1`; document in T12 | Rojina |
| Remote teammates lack HPC access | Pair with St Jude members (Rojina, Antonia) for submit tests | Antonia |
| Git clone slow on event day | Pre-clone on shared drive or distribute zip | Lindsey |

**Open questions:**

- [x] Which Slack channel is the team channel?
- [ ] Are hackathon VMs pre-loaded with `module load sprocket R singularity`?
- [ ] Is Victoria Knockout Cell Ranger output accessible to all testers? 
