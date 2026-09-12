# Participant FAQ — SNAP, Sprocket, and resource scaling

**Audience:** Team members new to the project (e.g. remote participants onboarding before the hackathon)  
**Related:** [Problem & solution overview](./problem-and-solution-overview.md) · [Daedalus pitch](./daedalus-pitch.md) · [Hackathon runbook](../../project-management/hackathon-runbook.md) · [scripts/README.md](../../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md) · [Test log](../validation/hackathon-test-log.md)

---

## Context

This document answers common onboarding questions about **what problem we are solving**, **what the hackathon is actually testing**, and **where resource auto-scaling comes from** (hint: not Sprocket itself).

Start with the shorter [problem-and-solution-overview.md](./problem-and-solution-overview.md) if you want slide-ready talking points first.

---

## What problem are we solving?

The pain point is **manual setup** when running SNAP on St. Jude HSF/LSF:

- Turning modules on/off
- Setting CPU and memory per step
- Wiring dependencies between steps
- Re-doing all of that when sample count or Cell Ranger outputs change

The **legacy path** (`launch_full_pipeline.sh` plus per-module `lsf-script.txt` files) uses **static** resource requests and manual bash wiring. That is error-prone and labor-intensive.

The **new path** uses **WDL + Sprocket** plus a **custom resource estimator** so analysts mainly edit YAML toggles and run one launcher command.

---

## Is the hackathon task to convert bash scripts to WDL?

**Mostly no.** That conversion work is **largely already done** in the Victoria Knockout analysis repo.

| Piece | Role |
|--------|------|
| `scripts/generate-snap-wdl.R` | Builds `wdl/snap.wdl` from `workflow_profile` toggles |
| `scripts/launch-snap-sprocket.sh` / `launch-snap-downstream.sh` | Orchestrates generate → estimate → validate → submit |
| `scripts/estimate-snap-downstream-resources.R` | **Scales LSF resources** from sample count + Cell Ranger metrics |
| Existing R/bash under `analyses/*/` | Still the actual biology code; WDL tasks call into them |

**Hackathon focus:** test, document, and demonstrate that orchestrator (tests **T1–T17** in the [runbook](../../project-management/hackathon-runbook.md)) — upstream + integrative on HPC, biology sign-off, ROI vs legacy, troubleshooting, and slides.

---

## Does Sprocket auto-scale resources?

**No — and you did not miss anything in the Sprocket documentation.**

**Sprocket does not auto-scale resources** based on pipeline biology or data size. It:

- Runs WDL workflows on LSF
- Handles task dependencies, containers, and job submission

You pass **explicit** CPU, memory, queue, and related settings per task (via inputs / generated config). Sprocket executes with those values; it does not compute them.

### Where auto-scaling actually lives

**Auto-scaling in this project is our custom layer**, not a Sprocket feature:

1. `estimate-snap-downstream-resources.R` reads:
   - sample count (`project_metadata.tsv` or Cell Ranger output directories)
   - Cell Ranger `metrics_summary.csv` (cells per sample)
2. It scales from a baseline (**8 samples × 50k cells**) and applies **20% LSF memory headroom**
3. It writes `inputs/project_parameters.generated.yaml` and `inputs/generated_downstream.json`
4. Those feed `inputs/sprocket_inputs.json` → Sprocket runs with those resource values

### Mental model

```text
YAML toggles + biology config  →  generate WDL
Cell Ranger metrics            →  estimate resources (our R script)
Both                           →  sprocket validate / run (Sprocket)
```

At launch, `launch-snap-downstream.sh` runs these steps in order:

| Step | Script / command | Output |
|------|------------------|--------|
| 1. Generate WDL | `scripts/generate-snap-wdl.R` | `wdl/snap.wdl` |
| 2. Estimate resources | `scripts/estimate-snap-downstream-resources.R` | `inputs/project_parameters.generated.yaml`, `inputs/generated_downstream.json`, `inputs/sprocket_inputs.json` |
| 3. Check WDL | `sprocket check wdl/snap.wdl` | — |
| 4. Validate inputs | `sprocket validate wdl/snap.wdl @inputs/sprocket_inputs.json` | — |
| 5. Submit (if not dry-run) | `sprocket run ...` | LSF jobs |

See [scripts/README.md](../../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md) for full launcher and config details.

---

## Three ways to run downstream (config file per mode)

| How you launch | Config file used |
|----------------|------------------|
| **WDL / Sprocket** (`launch-snap-downstream.sh --submit`) | `inputs/project_parameters.generated.yaml` |
| **Full LSF chain** (`launch_full_pipeline.sh`) | `project_parameters.Config.yaml` |
| **Interactive / per-module LSF** | `project_parameters.Config.yaml` |

For WDL runs, modules load the **generated overlay** (scaled resources). Legacy bash paths read the **master YAML** only.

---

## `workflow_profile` examples (for T3, T4, and T7, T8)

Edit `project_parameters.Config.yaml` → `workflow_profile`, then run `bash launch-snap-downstream.sh` (dry-run) or `--submit` (HPC).

### Upstream only (T3, T4)

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

### Upstream + integrative (T7, T8)

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

## Where to read more

| Doc | Purpose |
|-----|---------|
| [Problem & solution overview](./problem-and-solution-overview.md) | Slide-ready problem/solution narrative |
| [Daedalus pitch](./daedalus-pitch.md) | Tool name, pitches, naming rationale |
| [Hackathon runbook](../../project-management/hackathon-runbook.md) | Schedule, team pairs, test matrix T1–T17, deliverables |
| [scripts/README.md](../../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md) | Launcher flow, YAML config, troubleshooting |
| [Test log](../validation/hackathon-test-log.md) | Live pass/fail log during the event |
| [vm-hpc-setup.md](../../docs/vm-hpc-setup.md) | HPC access and modules |
| [resources-snap.md](../../docs/resources-snap.md) · [resources-sprocket.md](../../docs/resources-sprocket.md) | Background on SNAP and Sprocket |

---

## Pair assignments (quick reference)

| Pair | Focus |
|------|--------|
| **Emma/Rojina/Antonia** | Code review and development (Emma Bishop, Rojina Sapkota, Antonia Chroni); live demo |
| **Rojina/Antonia (testing)** | Dry-run and St. Jude HPC testing only — Rojina Sapkota and Antonia Chroni (T2–T5, T7–T8, T12–T14) |
| **Rachana/A.S.M. Tanjim** | Layout, resource/YAML tests, biology sign-off (T1, T6, T9–T11) |
| **Lindsey/Rachana** | Hackathon test log ([hackathon-test-log.md](../validation/hackathon-test-log.md)) |
| **Lindsey/Sarthak** | Docs, PRs, ROI tables, legacy vs new comparison (T15–T17) |

**T15 input:** Antonia provides LSF log files from a legacy `launch_full_pipeline.sh` run for the side-by-side comparison and slides.

---

## One-line summary

> **Sprocket orchestrates; our R estimator scales resources from Cell Ranger metrics; the hackathon validates that the combined launcher works better than the legacy bash pipeline.**

---

**Maintainer:** KIDS26 Team 15 · **Last updated:** 2026-09-12
