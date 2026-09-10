# KIDS26 Team 15 — Hackathon Runbook

**Project:** Resource-Aware Multi-Project Workflow Orchestrator for Scalable Single-Cell Analysis  
**Tool under test:** SNAP + Sprocket downstream launcher (`launch-snap-downstream.sh`)  
**Analysis repo:** `analyses/sc-rna-seq-snap-Victoria-Knockout/`  
**Time budget:** Day 1 (4 h) · Day 2 (8 h) · Day 3 (4 h afternoon) + demo session 3:00–6:00 PM  
**Test log:** [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md)  
**HPC setup:** [vm-hpc-setup.md](../docs/vm-hpc-setup.md)  
**Roster:** [stjude-biohackathon-kids26-team15-info.xlsx](./stjude-biohackathon-kids26-team15-info.xlsx)

---

## Goal

By the end of the hackathon, the team will have **tested, documented, and demonstrated** the resource-aware SNAP + Sprocket orchestrator (`launch-snap-downstream.sh`) and shown measurable ROI over legacy `launch_full_pipeline.sh`.

**Success requires:** upstream HPC submit (T4) and upstream + integrative submit (T8) logged with job IDs; biology sign-off (T6, T9); each pair produces a documented artifact.

### Definition of done

- [ ] At least **10 of 17 tests** logged in [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md)
- [ ] **T4** and **T8** documented with LSF job IDs
- [ ] **Biology sign-off** on upstream (T6) and integrative (T9)
- [ ] Code-review notes committed or issues filed for major findings
- [ ] **Troubleshooting doc** updated with ≥3 real errors + fixes
- [ ] **3-slide deck** (organizer template): problem, solution, results/impact
- [ ] **2-minute lightning talk** rehearsed (Lindsey, Antonia, Rojina, Rachana)
- [ ] **Live demo** rehearsed (or recorded fallback ready)

---

## Team

Assignments follow `Task_to_assign: pairs` from the roster.

| Pair | Members | Primary mission |
|------|---------|-----------------|
| **Lindsey/Sarthak** | Lindsey Warren + Sarthak Dhanke | GitHub PRs/reviews, docs, automated ROI and project impact |
| **Rojina/Antonia** | Rojina Sapkota + Antonia Chroni | Code development and review; HPC testing; live demo lead |
| **Rachana/A.S.M. Tanjim** | Rachana Pandey + Tanjim Hassan | Testing results/biology of sc-RNA; GitHub PR review |

| Person | GitHub | Pair | Main responsibility | HPC |
| --- | --- | --- | --- | --- |
| Antonia Chroni | [AntoniaChroni](https://github.com/AntoniaChroni) | Rojina/Antonia (lead) | Tool author; code review; HPC submit; live demo | Yes |
| Rojina Sapkota | [Rojinasap](https://github.com/Rojinasap) | Rojina/Antonia | Dry-run + WDL toggles (T2–T3, T7); HPC submits (T4, T5, T8); WDL chain (T12–T14) | Yes |
| Lindsey Warren | [lrwarren94](https://github.com/lrwarren94) | Lindsey/Sarthak | PR hygiene, doc structure, test log maintenance | Memphis |
| Sarthak Dhanke | [Sarztak](https://github.com/Sarztak) | Lindsey/Sarthak | ROI tables (T15–T16), legacy vs new comparison, PR review | Remote |
| Rachana Pandey | [rachanapandey2016](https://github.com/rachanapandey2016) | Rachana/A.S.M. Tanjim | Layout (T1); resource + YAML tests (T10–T11); log pass/fail | Remote |
| Tanjim Hassan | [asmtanjimhassan](https://github.com/asmtanjimhassan) | Rachana/A.S.M. Tanjim | Biology sign-off (T6, T9) | Remote (async) |

### Deliverables by pair

| Pair | Lead | Output |
|------|------|--------|
| Lindsey/Sarthak | Lindsey | `deliverables/validation/hackathon-test-log.md`, `docs/troubleshooting.md`, PR merges, ROI for slides |
| Rojina/Antonia | Rojina | `docs/code-review-notes.md` + issues; T2–T5, T7–T8, T12–T14; live demo; Antonia provides legacy-run LSF log files (T15) |
| Rachana/A.S.M. Tanjim | Rachana | Test log rows T1, T6, T9–T11; biology sign-off T6, T9 |

**Communications:** [Slack team15](https://stjudebiohackathon.slack.com/archives/C0BT8BF4JEL) · Check-ins: Day 1 end · Day 2 mid-day · Demo Day 3, 3:00–6:00 PM

---

## Tools

| Tool | Role |
|------|------|
| [sc-rna-seq-snap](https://github.com/stjude-dnb-binfcore/sc-rna-seq-snap) | Single-cell analysis modules |
| [Sprocket](https://github.com/stjude-rust-labs/sprocket) | WDL workflow runner on St. Jude HPC |
| `launch-snap-downstream.sh` | One-command launcher (dry-run or `--submit`) |
| `estimate-snap-downstream-resources.R` | Auto-scale LSF CPU/memory from Cell Ranger metrics |
| Apptainer/Singularity | Container runtime for R/Seurat modules |
| Victoria Knockout cohort | Test dataset (4 samples, ~27k cells) |

---

## What we are testing

The orchestrator replaces manual LSF wiring with:

1. **YAML `workflow_profile` toggles** — turn modules on/off without editing bash flags
2. **Auto resource scaling** — `estimate-snap-downstream-resources.R` reads Cell Ranger metrics
3. **WDL + Sprocket validation** — `sprocket check` / `validate` before submit
4. **One-command launch** — `bash launch-snap-downstream.sh [--submit]`

**Scope:** St. Jude **HPC only** — SNAP **upstream** and **integrative** modules on Victoria Knockout.

---

## Environment setup (first 45 min — HPC)

```bash
git clone <team15-repo-url>
cd KIDS26-Team15/analyses/sc-rna-seq-snap-Victoria-Knockout
module load sprocket R singularity
bash scripts/test-downstream-layout.sh    # T1
bash launch-snap-downstream.sh            # T2 dry-run
```

Remote teammates without HPC login pair with **Rojina/Antonia** for submit tests (T4, T8).

Lindsey/Sarthak maintains [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md). One row per test: tester, date, pass/fail, LSF job ID, notes, screenshot link.

**Pre-hackathon (team lead):** Submit one upstream-only run before the event as demo backup.

---

## Test matrix (T1–T17)

Record results in [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md). Status: `PASS` | `FAIL` | `SKIP` | `BLOCKED`.

| ID | Test | Module(s) | Owner | Command / action | Expected result |
|----|------|-----------|-------|------------------|-----------------|
| **T1** | Layout sanity | — | Rachana/A.S.M. Tanjim | `bash scripts/test-downstream-layout.sh` | All expected WDL/input files present |
| **T2** | Dry-run pipeline | — | Rojina/Antonia | `bash launch-snap-downstream.sh` | WDL regen → estimate → check → validate pass |
| **T3** | Upstream — WDL toggle | `run_upstream` | Rojina/Antonia | Only `run_upstream: true`; dry-run | WDL contains upstream task only |
| **T4** | Upstream — HPC submit | `run_upstream` | Rojina/Antonia | `bash launch-snap-downstream.sh --submit` | LSF job ID returned |
| **T5** | Upstream — LSF monitoring | `run_upstream` | Rojina/Antonia | `bjobs -u $USER`; tail upstream stderr | Job visible; logs accessible |
| **T6** | Upstream — biology QC | `run_upstream` | Rachana/A.S.M. Tanjim | Review QC plots, cell counts, filters | Tanjim signs off upstream outputs |
| **T7** | Upstream + integrative — WDL toggle | both | Rojina/Antonia | Both modules true; dry-run | WDL chain: upstream → integrative |
| **T8** | Upstream + integrative — HPC submit | both | Rojina/Antonia | `bash launch-snap-downstream.sh --submit` | LSF job ID returned |
| **T9** | Integrative — biology QC | `run_integrative` | Rachana/A.S.M. Tanjim | Review Harmony outputs, UMAP | Tanjim signs off integrative outputs |
| **T10** | Resource scaling | both | Rachana/A.S.M. Tanjim | `estimate-snap-downstream-resources.R --update-yaml` | JSON reflects sample count; resources updated |
| **T11** | Generated YAML overlay | — | Rachana/A.S.M. Tanjim | Inspect `project_parameters.generated.yaml` | Master YAML untouched; scaled resources in overlay |
| **T12** | WDL module chain | upstream → integrative | Rojina/Antonia | Inspect generated WDL dependency chain | Integrative depends on upstream |
| **T13** | `snap_parallel_plan.R` safety | upstream | Rojina/Antonia | `SNAP_FUTURE_WORKERS=1` vs `2` | No NFS bus errors; document behavior |
| **T14** | Email notification | — | Rojina/Antonia | Confirm `CONTACT_EMAIL` on submit | Workflow submitted email received |
| **T15** | Legacy vs new comparison | — | Lindsey/Sarthak | Compare `launch_full_pipeline.sh` vs `workflow_profile` | Side-by-side table for slides |
| **T16** | ROI timing | — | Lindsey/Sarthak | Time YAML edit + dry-run vs legacy bash | Minutes-to-launch-ready on HPC |
| **T17** | Troubleshooting doc | — | Lindsey/Sarthak | Log every real HPC error + fix | Entries in `docs/troubleshooting.md` |

**Module run evidence** (in test log): job IDs for (1) upstream-only, (2) integrative-only, (3) upstream + integrative chain.

---

## Pair work details

### Rojina/Antonia — code, HPC, demo

Review: `launch-snap-sprocket.sh`, `estimate-snap-downstream-resources.R`, `generate-snap-wdl.R`, `snap_parallel_plan.R`, `snap-read-config.sh`.

**Antonia:** Provide LSF log files from the legacy `launch_full_pipeline.sh` run for Lindsey/Sarthak (T15 legacy vs new comparison).

Issue template: **Severity** · **Found by** · **Steps** · **Expected** · **Actual**

### Rachana/A.S.M. Tanjim — testing and biology

Rachana: T1, T10, T11. Tanjim: biology sign-off T6, T9. Screenshot every PASS and FAIL.

### Lindsey/Sarthak — docs, PRs, ROI

PR checklist: `set -euo pipefail`; YAML edits only in `project_parameters.Config.yaml`; WDL generated not hand-edited; no secrets committed.

**T15 input:** Antonia will provide LSF log files from the legacy run for the side-by-side comparison and slides.

---

## Demo prep (Day 3)

### Wednesday reception report-out (60 seconds)

At the beginning of the reception, each team gives a brief, **60-second report-out** highlighting their day. This can include key updates, progress made, notable accomplishments, or anything else your team would like to share.

**Action required:** Identify who from your team will give the report-out. If that person will not attend the reception, designate a teammate who will be present to share the update on your team's behalf.

| Report-out speakers | Confirmed? |
|-------------------|------------|
| Lindsey Warren, Antonia Chroni, Rojina Sapkota, Rachana Pandey | ☑ |

Organizer note: [01-report-out-Wednesday-reception-email.md](../deliverables/reports/01-report-out-Wednesday-reception-email.md)

**Slide narrative:** [problem-and-solution-overview.md](../docs/problem-and-solution-overview.md) · **Onboarding FAQ:** [participant-faq-snap-sprocket-resources.md](../docs/participant-faq-snap-sprocket-resources.md)

**3-slide template:**

| Slide | Owner | Content |
|-------|-------|---------|
| 1 — Problem | Lindsey Warren | Manual LSF wiring: analyst time, fixed resources, error-prone bash flags |
| 2 — Solution | Antonia Chroni, Rojina Sapkota, Rachana Pandey | YAML toggles + one-command launcher; HPC evidence (T4, T8) |
| 3 — Results | Lindsey Warren, Rachana Pandey | ROI (T15–T16), biology (T6, T9), limitations, next steps |

**Slide 3 — next steps:** sc-ATAC, sc-PARSE; multi-omics (sc-RNA + sc-ATAC); `snap_multi_project.wdl`; CI layout check; production rollout.

**Presenters:** Lindsey Warren, Antonia Chroni, Rojina Sapkota, Rachana Pandey

**Live demo:** Show `workflow_profile` toggles → dry-run + `sprocket validate` → scaled resources in `inputs/generated_downstream.json` → LSF status or completed outputs. **Fallback:** submitted state + pre-recorded walkthrough.

---

## Three-day schedule

| Day | Hours | Focus |
|-----|-------|-------|
| **Day 1** | 4 h | Align, setup, T1–T2; start T3–T4 |
| **Day 2** | 8 h | T1–T14 logged; T4, T8 submits; draft slides |
| **Day 3** | 4 h | Polish deck, rehearse |
| **Day 3 demo** | 3:00–6:00 PM | Lightning (3:00–4:00) → demo room → judge Q&A |

### Day 1 (4 h)

| Block | Activity | Who |
|-------|----------|-----|
| 0:00–0:30 | Kickoff: pairs, test log, HPC access | All |
| 0:30–1:15 | Clone, T1, T2 dry-run | All |
| 1:15–3:00 | Parallel work | Rojina/Antonia: T2–T3 · Rachana/A.S.M. Tanjim: T1 · Lindsey/Sarthak: test log |
| 3:00–4:00 | Sync; schedule T4; Day 2 priorities | All |

### Day 2 (8 h)

| Block | Activity | Who |
|-------|----------|-----|
| 0:00–3:00 | Parallel work | Rojina/Antonia: T4–T5, T7–T8, T12–T14 · Rachana/A.S.M. Tanjim: T6, T9–T11 · Lindsey/Sarthak: T15–T17 |
| 3:00–3:30 | Mid-day sync | All |
| 3:30–7:30 | Continue testing; draft slide content | All |
| 7:30–8:00 | Day 2 wrap | Pair leads |

### Day 3 (4 h + demo)

| Block | Activity |
|-------|----------|
| 0:00–1:00 | Final sign-off; merge PRs or document follow-ups |
| 1:00–2:00 | Finalize 3-slide deck |
| 2:00–3:00 | Rehearse lightning + live demo |
| 3:00–6:00 PM | Lightning → demo room → judge feedback (capture in [Session notes](#session-notes)) |

---

## Checklists

### Pre-hackathon (team lead)

- [x] Cell Ranger complete for Victoria Knockout
- [x] `project_metadata.tsv` present and valid
- [x] Apptainer `.sif` accessible on HPC
- [x] One upstream-only job pre-submitted (demo backup)
- [x] Teammates added to GitHub repo
- [x] Shared test log location communicated
- [x] HPC accounts verified; remote members know handoff process
- [ ] Organizer 3-slide template downloaded
- [ ] Event deck added to `deliverables/slides/` (filename TBD; separate from kickoff `kickoff/kids26-team15-2026-09-04.pptx`)
- [x] Report-out speaker (and backup) designated for Wednesday reception
- [x] Legacy-run LSF log files provided by Antonia (`launch_full_pipeline.sh`; for T15)
- [ ] `CONTACT_EMAIL` set in `project_parameters.Config.yaml`

### Day-of (all pairs)

- [ ] T1 passes; T2 dry-run logged
- [ ] Findings shared at Day 1 and Day 2 syncs
- [ ] Pair deliverable committed or PR opened by end of Day 2
- [ ] Legacy-run LSF log files received from Antonia (T15 legacy vs new comparison)
- [ ] 3-slide content contributed; lightning + demo rehearsed before 3:00 PM Day 3

---

## Risks

| Risk | Mitigation | Owner |
|------|------------|-------|
| Long runtime blocks demo | Pre-submit upstream; demo shows submitted state + recording | Antonia |
| Integrative waits on upstream | Submit T4 Day 1; chain T8 Day 2 | Rojina |
| Tanjim remote (+11 h CDT) | Async updates; Rachana pairs for T6, T9 sign-off | Rachana |
| NFS bus errors with parallel R | Default `SNAP_FUTURE_WORKERS=1`; document in T13 | Rojina |
| Remote members lack HPC | Pair with Rojina/Antonia for T4, T8 | Antonia |

**Stretch goals if done early:** T13 worker comparison; `snap_multi_project.wdl`; GitHub Actions layout check; PRs for quick fixes.

---

## Key commands

```bash
cd analyses/sc-rna-seq-snap-Victoria-Knockout
bash scripts/test-downstream-layout.sh
bash launch-snap-downstream.sh              # dry-run
bash launch-snap-downstream.sh --submit       # HPC submit
Rscript scripts/estimate-snap-downstream-resources.R --snap-root . \
  --output inputs/generated_downstream.json --update-yaml
bjobs -u $USER
```

### `workflow_profile` — upstream only (T3, T4)

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

### `workflow_profile` — upstream + integrative (T7, T8)

```yaml
workflow_profile:
  run_upstream: true
  run_integrative: true
  run_cluster: false
  run_contamination_removal: false
  run_cell_types: false
  run_clone_phylogeny: false
  run_de_go: false
  run_rshiny: false
```

---

## Session notes

### Day 3 — Demo session (3:00–6:00 PM)

**Presenters:** Lindsey Warren, Antonia Chroni, Rojina Sapkota, Rachana Pandey

#### Judge feedback

[Capture notes during demo room session]

---

### Day 2 — Mid-day sync

[Notes]

---

### Day 1 — End-of-day sync

[Notes]

---

## References

- [Problem & solution overview](../docs/problem-and-solution-overview.md)
- [Participant FAQ — SNAP, Sprocket, and resource scaling](../docs/participant-faq-snap-sprocket-resources.md)
- [scripts/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md)
- [wdl/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/wdl/README.md)
- [Snap-Sprocket-ROI-one-pager.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/docs/Snap-Sprocket-ROI-one-pager.md)
- [resources-snap.md](../docs/resources-snap.md) · [resources-sprocket.md](../docs/resources-sprocket.md)
- [learning-path-wdl-sprocket-containers.md](../docs/learning-path-wdl-sprocket-containers.md)

**Maintainer:** Antonia Chroni / KIDS26 Team 15 · **Last updated:** 2026-09-10
