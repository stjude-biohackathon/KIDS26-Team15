# Daedalus — name and pitch

**Daedalus** is the working name for our resource-aware SNAP + Sprocket orchestrator (`launch-snap-downstream.sh`).

**Related:** [Problem & solution overview](./problem-and-solution-overview.md) · [Participant FAQ](./participant-faq-snap-sprocket-resources.md) · [Slides](../slides/)

---

## 30-second pitch

> Single-cell pipelines on HPC shouldn’t require hand-wiring every module, guessing CPU and memory, and re-editing bash every time a cohort changes.
>
> **Daedalus** is our YAML-driven launcher for SNAP downstream analysis. You toggle modules in `workflow_profile`, run one command, and Daedalus generates WDL, scales LSF resources from Cell Ranger metrics, validates with Sprocket, and submits to the cluster.
>
> We built it to replace the legacy `launch_full_pipeline.sh` path — same biology, less infrastructure friction, and resources that grow with your data.

---

## 60-second pitch (demo / reception)

> **Problem:** Today, running SNAP on St. Jude LSF means static bash scripts, fixed resource requests, and manual job chaining. That’s slow to configure, easy to get wrong, and painful when sample count or Cell Ranger outputs change.
>
> **Solution — Daedalus:** A resource-aware orchestrator on top of SNAP, WDL, and Sprocket. Analysts edit YAML module toggles and biology parameters — not LSF wiring. Daedalus generates the workflow, estimates CPU and memory from cohort size and Cell Ranger metrics, validates before submit, and launches with a single command.
>
> **Why it matters:** Sprocket runs the workflow; our R estimator sizes the jobs — Sprocket doesn’t auto-scale for you. Daedalus fills that gap and gives us one reproducible path from Victoria Knockout config to upstream and integrative runs on HPC.
>
> **Hackathon goal:** Test, document, and show measurable ROI versus the legacy launcher — with real LSF job IDs and biology sign-off.

---

## One-liner

> **Daedalus turns YAML module toggles and Cell Ranger metrics into validated, resource-aware SNAP runs on LSF — one command instead of manual bash wiring.**

---

## Why we chose “Daedalus”

In Greek myth, **Daedalus** was the master craftsman — the architect who designed complex, interlocking systems (the labyrinth, the wings) that had to work as a whole. That maps to what this tool does:

| Myth | Our orchestrator |
|------|------------------|
| Designs complex systems that must fit together | Wires optional SNAP modules into one dependency-aware WDL workflow |
| Builds structure others navigate safely | Replaces ad hoc bash/LSF scripts with validated, repeatable launches |
| Crafts with precision | Scales resources from data (Cell Ranger metrics), not guesswork |

**Why not something more literal?** Names like “pipeline launcher” describe function but don’t stick in a talk. **Daedalus** signals *orchestration and craft*, not a new clustering or integration method — so it won’t be confused with Seurat, Harmony, or Scanpy-style analysis tools.

**Why not SCALR or Scala?** We considered acronyms closer to “scaling,” but **Scalr** (Terraform orchestration) and **scaLR** (scRNA-seq ML) are too easy to confuse; **SCALA** is already a published single-cell multimodal tool. **Daedalus** is distinctive in our context when we introduce it as *the St. Jude SNAP orchestrator*.

**How to say it in slides:** *“Daedalus — our SNAP + Sprocket orchestrator”* on first mention; then just “Daedalus.”

---

## Slide footer (optional)

**Daedalus** · Resource-aware SNAP orchestrator · YAML toggles · WDL + Sprocket · St. Jude HPC

---

**Maintainer:** KIDS26 Team 15 · **Last updated:** 2026-09-10
