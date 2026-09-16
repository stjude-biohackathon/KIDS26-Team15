# KIDS26 Team 15 — Hackathon Runbook

**Project:** Resource-Aware Multi-Project Workflow Orchestrator for Scalable Single-Cell Analysis  
**Tool:** SNAP + Sprocket launcher (`launch-snap-downstream.sh`) in `analyses/sc-rna-seq-snap-Victoria-Knockout/`  
**Schedule:** Day 1 (4 h) · Day 2 (8 h) · Day 3 (4 h) · Demo 3:00–6:00 PM  
**Links:** [Test log](../deliverables/validation/hackathon-test-log.md) · [HPC setup](../docs/vm-hpc-setup.md) · [Roster xlsx](./stjude-biohackathon-kids26-team15-info.xlsx) · [Slack team15](https://stjudebiohackathon.slack.com/archives/C0BT8BF4JEL)

---

## Goal

Test, document, and demo the resource-aware SNAP + Sprocket orchestrator and show ROI vs legacy `launch_full_pipeline.sh`.

**Definition of done**

- [ ] ≥10 of 17 tests in [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md)
- [ ] T4 + T8 with LSF job IDs; biology sign-off T6 + T9
- [ ] Code-review notes or issues; ≥3 troubleshooting entries
- [ ] Wednesday progress report; 3-slide deck; 2-min lightning talk; live demo (or recording)

---

## Team

**Pair labels:** **HPC** = dry-run + St. Jude submits (T2–T5, T7–T8, T12–T14) · **Bio** = layout, biology QC, resource tests (T1, T6, T9–T11) · **Docs** = test log, PRs, ROI (T15–T17)

| Person | GitHub | Pair | Role | HPC / in-person |
| --- | --- | --- | --- | --- |
| Antonia Chroni | [AntoniaChroni](https://github.com/AntoniaChroni) | Code/dev · HPC | Tool author; code review; HPC testing; demo | Yes / Yes |
| Rojina Sapkota | [Rojinasap](https://github.com/Rojinasap) | Code/dev · HPC | Code review; dry-run, WDL toggles, HPC submits | Yes / Yes |
| Emma Bishop | [emjbishop](https://github.com/emjbishop) | Code/dev | Code review + development lead; demo | Remote |
| Clay McLeod | [claymcleod](https://github.com/claymcleod) | Code/dev · HPC | Code review, development, dry-run, HPC testing — as needed | Yes / remote |
| Lindsey Warren | [lrwarren94](https://github.com/lrwarren94) | Docs · Bio | Test log (with Rachana); PR hygiene | In-person |
| Rachana Pandey | [rachanapandey2016](https://github.com/rachanapandey2016) | Bio · Docs | Test log (with Lindsey); T1, T10–T11 | In-person |
| Sarthak Dhanke | [Sarztak](https://github.com/Sarztak) | Docs | ROI, legacy comparison, troubleshooting (T15–T17) | Remote |
| Tanjim Hassan | [asmtanjimhassan](https://github.com/asmtanjimhassan) | Bio | Biology sign-off T6, T9 | Remote |

| Pair | Lead | Deliverable |
| --- | --- | --- |
| HPC (Rojina, Antonia, Clay) | Rojina | T2–T5, T7–T8, T12–T14 logged; Antonia provides legacy LSF logs (T15) |
| Code/dev (Emma, Rojina, Antonia, Clay) | Emma | `docs/code-review-notes.md`; live demo |
| Bio (Rachana, Tanjim) | Rachana | T1, T6, T9–T11; Tanjim sign-off; legacy outputs from Antonia for QC |
| Docs (Lindsey, Sarthak) | Lindsey | `hackathon-test-log.md`, `docs/troubleshooting.md`, ROI slides |

Check-ins: Day 1 end · Day 2 mid-day · Demo Day 3.

---

## Setup (first 45 min)

```bash
git clone <team15-repo-url>
cd KIDS26-Team15/analyses/sc-rna-seq-snap-Victoria-Knockout
module load sprocket R singularity
bash scripts/test-downstream-layout.sh    # T1
bash launch-snap-downstream.sh            # T2 dry-run
```

No HPC access? Pair with **HPC** testers for T2–T5, T7–T8, T12–T14. Lindsey + Rachana maintain the test log (tester, date, pass/fail, job ID, notes, screenshot).

**Scope:** St. Jude HPC only — SNAP upstream + integrative on Victoria Knockout (4 samples, ~27k cells). YAML toggles, auto resource scaling, WDL validation, one-command launch.

---

## Test matrix (T1–T17)

Status: `PASS` | `FAIL` | `SKIP` | `BLOCKED`. Log in [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md).

| ID | Test | Owner | Command / action | Expected |
|----|------|-------|------------------|----------|
| T1 | Layout sanity | Bio | `bash scripts/test-downstream-layout.sh` | All WDL/input files present |
| T2 | Dry-run pipeline | HPC | `bash launch-snap-downstream.sh` | Regen → estimate → check → validate pass |
| T3 | Upstream WDL toggle | HPC | `run_upstream: true`; dry-run | Upstream task only |
| T4 | Upstream HPC submit | HPC | `bash launch-snap-downstream.sh --submit` | LSF job ID |
| T5 | Upstream LSF monitoring | HPC | `bjobs -u $USER`; tail stderr | Job visible; logs OK |
| T6 | Upstream biology QC | Bio | Review QC plots, counts | Tanjim sign-off |
| T7 | Upstream + integrative toggle | HPC | Both modules true; dry-run | Upstream → integrative chain |
| T8 | Upstream + integrative submit | HPC | `--submit` | LSF job ID |
| T9 | Integrative biology QC | Bio | Review Harmony, UMAP | Tanjim sign-off |
| T10 | Resource scaling | Bio | `estimate-snap-downstream-resources.R --update-yaml` | Resources updated |
| T11 | Generated YAML overlay | Bio | Inspect `project_parameters.generated.yaml` | Master YAML untouched |
| T12 | WDL module chain | HPC | Inspect dependency chain | Integrative depends on upstream |
| T13 | `snap_parallel_plan.R` safety | HPC | `SNAP_FUTURE_WORKERS=1` vs `2` | No NFS bus errors |
| T14 | Email notification | HPC | Confirm `CONTACT_EMAIL` on submit | Email received |
| T15 | Legacy vs new | Docs | Compare `launch_full_pipeline.sh` vs YAML toggles | Slide table |
| T16 | ROI timing | Docs | Time YAML edit + dry-run vs legacy | Minutes to launch-ready |
| T17 | Troubleshooting doc | Docs | Log HPC errors + fixes | `docs/troubleshooting.md` |

T3/T7 YAML examples: [participant FAQ](../deliverables/docs/participant-faq-snap-sprocket-resources.md#workflow_profile-examples-for-t3-t4-and-t7-t8). Code review targets: `launch-snap-sprocket.sh`, `estimate-snap-downstream-resources.R`, `generate-snap-wdl.R`, `snap_parallel_plan.R`, `snap-read-config.sh`.

---

## Schedule

| Day | Focus |
|-----|-------|
| **Day 1** (4 h) | Kickoff · T1–T2 · start T3–T4 · end-of-day sync |
| **Day 2** (8 h) | T3–T14 · T4/T8 submits · mid-day sync · draft slides |
| **Day 3** (4 h) | Sign-off · deck · rehearse lightning + demo |
| **Demo** (3–6 PM) | Lightning → demo room → judge Q&A |

**Wednesday report-out (60 s):** Lindsey, Antonia, Rojina, Rachana — [organizer note](../deliverables/reports/01-report-out-Wednesday-reception-email.md)

**Demo presenters:** Lindsey, Antonia, Rojina, Emma, Rachana · [Slides](../deliverables/docs/problem-and-solution-overview.md) · [Pitch](../deliverables/docs/daedalus-pitch.md) · Fallback: pre-submitted job + recording

---

## Checklists

**Pre-hackathon (lead)**

- [x] Cell Ranger, metadata, Apptainer, demo backup job, GitHub access, test log shared, HPC verified
- [x] Report-out speakers; legacy LSF logs; `CONTACT_EMAIL` set
- [ ] Organizer 3-slide template; event deck in `deliverables/slides/`

**Day-of**

- [ ] T1 + T2 logged; syncs Day 1 + Day 2; pair deliverables by Day 2 end
- [ ] Deck + rehearsal before 3:00 PM Day 3

---

## Risks

| Risk | Mitigation | Owner |
|------|------------|-------|
| Long runtime blocks demo | Pre-submit; show submitted state + recording | Antonia |
| Integrative waits on upstream | T4 Day 1; T8 Day 2 | HPC |
| Tanjim remote (+11 h) | Rachana pairs for T6, T9 | Rachana |
| NFS / parallel R | `SNAP_FUTURE_WORKERS=1`; document T13 | HPC |
| Remote, no HPC | Pair with HPC for T4, T8 | HPC |

---

## Session notes

### Day 3 — Demo (3:00–6:00 PM)

**Presenters:** Lindsey, Antonia, Rojina, Rachana

#### Judge feedback

[Notes]

### Day 2 — Mid-day sync

[Notes]

### Day 1 — End-of-day sync

[Notes]

---

## References

[Problem overview](../deliverables/docs/problem-and-solution-overview.md) · [Participant FAQ](../deliverables/docs/participant-faq-snap-sprocket-resources.md) · [scripts/README](../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md) · [wdl/README](../analyses/sc-rna-seq-snap-Victoria-Knockout/wdl/README.md) · [ROI one-pager](../analyses/sc-rna-seq-snap-Victoria-Knockout/docs/Snap-Sprocket-ROI-one-pager.md) · [SNAP](../docs/resources-snap.md) · [Sprocket](../docs/resources-sprocket.md)

**Maintainer:** Antonia Chroni / KIDS26 Team 15 · **Last updated:** 2026-09-16
