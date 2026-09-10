# Problem and solution overview

**Use for:** Slide 1–2 narrative, reception report-out, quick team onboarding  
**Go deeper:** [Participant FAQ](./participant-faq-snap-sprocket-resources.md) · [Hackathon runbook](../project-management/hackathon-runbook.md) · [Deck](../deliverables/slides/)

---

## The problem

Running SNAP single-cell pipelines on St. Jude HPC today means **manual LSF wiring**:

| Pain point | What analysts do today |
|------------|------------------------|
| Module selection | Edit bash flags or hand-edit LSF scripts per module |
| Resources | Pick fixed CPU/memory per step — often wrong for cohort size |
| Dependencies | Chain jobs manually; easy to run steps out of order |
| Re-runs | Reconfigure everything when sample count or Cell Ranger outputs change |

**Legacy path:** `launch_full_pipeline.sh` + static `lsf-script.txt` files under each `analyses/<module>/` folder.

**Cost:** Error-prone, labor-intensive, and hard to scale across projects.

---

## Our solution

A **resource-aware SNAP + Sprocket orchestrator** — one command replaces manual bash wiring:

```bash
bash launch-snap-downstream.sh          # dry-run + validate
bash launch-snap-downstream.sh --submit  # LSF submit
```

| Layer | What it does |
|-------|----------------|
| **YAML `workflow_profile`** | Turn modules on/off without editing bash |
| **`generate-snap-wdl.R`** | Build `wdl/snap.wdl` from toggles |
| **`estimate-snap-downstream-resources.R`** | Scale LSF CPU/memory from Cell Ranger metrics (our code — not Sprocket) |
| **Sprocket** | Validate WDL, submit tasks to LSF, manage dependencies |

```text
YAML toggles  →  generate WDL
Cell Ranger   →  estimate resources (R script)
Both          →  sprocket validate / run
```

---

## Slide talking points

### Slide 1 — Problem (Lindsey/Sarthak)

- Analysts spend time on **infrastructure**, not biology
- Legacy launcher uses **static** resources — OOM kills or wasted queue time
- Module toggles and LSF wiring are **scattered across bash scripts**

### Slide 2 — Solution (Rojina/Antonia + Rachana/Tanjim)

- **One launcher** — `launch-snap-downstream.sh`
- **YAML toggles** — `run_upstream`, `run_integrative`, etc.
- **Data-driven scaling** — resources from Victoria Knockout Cell Ranger metrics
- **HPC evidence** — upstream submit (T4) and upstream + integrative submit (T8)

### Slide 3 — Results (Lindsey/Sarthak + Rachana/Tanjim)

- ROI timing: legacy vs new (T15–T16)
- Biology sign-off on upstream and integrative outputs (T6, T9)
- See [Snap-Sprocket-ROI-one-pager.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/docs/Snap-Sprocket-ROI-one-pager.md)

---

## What the hackathon validates

We are **not** converting bash to WDL from scratch — that work is largely done. We are **testing and demonstrating** the orchestrator on Victoria Knockout (4 samples, ~27k cells):

- [Test log](../deliverables/validation/hackathon-test-log.md) — T1–T17 pass/fail
- Live demo — YAML toggle → dry-run → LSF submit
- Legacy comparison — Antonia provides LSF logs from `launch_full_pipeline.sh` (T15)

---

## One-line pitch

> **Replace manual LSF bash wiring with YAML toggles, data-driven resource scaling, and one-command Sprocket launch.**

---

**Maintainer:** KIDS26 Team 15 · **Last updated:** 2026-09-10
