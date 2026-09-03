# Team and Roles

- **Team name:** KIDS26 Team 15
- **Team lead:** Antonia Chroni ([@AntoniaChroni](https://github.com/AntoniaChroni))
- **Communication channel:** [Slack general channel](https://stjudebiohackathon.slack.com/archives/C04JD4M3TCM) + team channel (TBD)
- **Project question/problem:** Can a resource-aware SNAP + Sprocket orchestrator replace manual LSF wiring for scalable single-cell analysis?
- **Expected output:** Tested downstream launcher, documented test results, code-review notes, 3-slide deck, 2-minute lightning talk, and live demo for judges
- **Tools and stack:** SNAP (`sc-rna-seq-snap`), WDL, Sprocket, R/Seurat, Apptainer/Singularity, LSF, YAML config

**Runbook:** [hackathon-runbook.md](../project-management/hackathon-runbook.md)  
**Test log:** [hackathon-test-results.md](../results/hackathon-test-results.md)  
**SNAP overview:** [resources-snap.md](../docs/resources-snap.md)  
**Roster:** [stjude-biohackathon-kids26-team15-info.xlsx](./stjude-biohackathon-kids26-team15-info.xlsx)

---

## Pair assignments

Assignments follow each person's `Task_to_assign` and `Task_to_assign: pairs` from the roster.

| Pair | Track | Members | Primary mission |
|------|-------|---------|-----------------|
| **A** | Code review | Rojina Sapkota + Antonia Chroni | Audit WDL, launcher scripts, resource estimator; file GitHub issues |
| **B** | Testing | Sarthak Dhanke | Run test matrix (T1–T8) on VM and HPC; log pass/fail with screenshots |
| **C** | Docs & PRs | Lindsey Warren + Rachana Pandey | PR reviews, troubleshooting docs, maintain test-results log |
| **D** | Support & demo | Tanjim Hassan + Antonia Chroni | Biology validation, slides and live demo; HPC golden-path submit |

---

## Roles

| Person | GitHub | Track | Task (self-assigned) | Main responsibility | HPC / St Jude |
| --- | --- | --- | --- | --- | --- |
| Antonia Chroni | [AntoniaChroni](https://github.com/AntoniaChroni) | A (lead) | — | Tool author; unblock pairs; float support | Yes |
| Rojina Sapkota | [Rojinasap](https://github.com/Rojinasap) | A | Check the code of the tool | Code review of WDL, scripts, resource logic | Yes (St Jude) |
| Sarthak Dhanke | [Sarztak](https://github.com/Sarztak) | B | Testing | Execute test matrix; document orchestration errors | Remote |
| Lindsey Warren | [lrwarren94](https://github.com/lrwarren94) | C | GitHub PRs/reviews: docs, code | PR hygiene, CI/CD review, doc structure | Memphis (in person) |
| Rachana Pandey | [rachanapandey2016](https://github.com/rachanapandey2016) | C | GitHub PRs/reviews: docs | Test log, troubleshooting, ROI tables for slides | Remote |
| Tanjim Hassan | [asmtanjimhassan](https://github.com/asmtanjimhassan) | D | Plus (support) | Seurat QC sanity checks; poster/slide design; demo narrative | Remote |

Roles can overlap during rotations. See the [runbook](./hackathon-runbook.md) for the three-day timeline (Day 1: 4 h · Day 2: 8 h · Day 3: 4 h + demo 3:00–6:00 PM).

---

## Deliverables by track

| Track | Lead | Output file(s) |
|-------|------|----------------|
| A — Code review | Rojina | `docs/code-review-notes.md` + GitHub issues |
| B — Testing | Sarthak | Rows in `results/hackathon-test-results.md` (T1–T8) |
| C — Docs & PRs | Lindsey | `results/hackathon-test-results.md`, `docs/troubleshooting.md` updates, PR merges |
| D — Support & demo | Tanjim | 3-slide deck (organizer template), 2-min lightning script, live demo, screen recording |
