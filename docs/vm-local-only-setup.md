# VM / Local-Only Setup — KIDS26 Team 15 (No HPC)

**Project:** Resource-Aware SNAP + Sprocket Orchestrator  
**Use when:** No St. Jude HPC access — shared VM, personal laptops, or Docker runner only  
**HPC alternative:** [vm-hpc-setup.md](./vm-hpc-setup.md)  
**Hackathon runbook:** [hackathon-runbook.md](../project-management/hackathon-runbook.md)  
**SNAP overview:** [resources-snap.md](./resources-snap.md)

---

## Summary

You **can** run a solid hackathon without HPC, but not with the exact same commands unchanged. The production launcher (`launch-snap-downstream.sh`) targets **LSF + Apptainer** on St. Jude HPC.

| Tier | What you prove | Infrastructure |
|------|----------------|----------------|
| **Tier 1 — Validation** | YAML toggles, WDL gen, resource scaling, `sprocket check`/`validate` | Shared VM: 8 vCPU, 32 GB RAM |
| **Tier 2 — Live run** | One upstream module via Sprocket + Docker | Runner machine: 16 vCPU, **64 GB RAM**, Docker |
| **Tier 3 — Biology only** | Seurat modules work (bypasses orchestrator) | Docker + module scripts |

**Recommended for one shared VM:** Tier 1 for everyone + Tier 2 on **one designated runner** (laptop or second VM).

---

## Architecture (no HPC)

```text
┌─────────────────────────────────────────────────────────────┐
│  Shared VM (32 GB) — all teammates                          │
│  git · YAML · code review · docs · dry-run · slides         │
│  R scripts: generate WDL, estimate resources                │
│  sprocket check / validate (no live Seurat run)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ optional
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Runner machine (64 GB) — one person at a time            │
│  Docker + Sprocket + sprocket.local.toml                    │
│  sprocket run … upstream-only                               │
└─────────────────────────────────────────────────────────────┘
```

---

## What to request from organizers (no HPC)

### Shared VM (coordination hub)

```text
OS:        Linux (Ubuntu 22.04+ or RHEL 8+)
CPU:       8 vCPU
RAM:       32 GB
Storage:   100 GB
Network:   outbound HTTPS (GitHub)

Pre-installed:
  - git, tmux, curl, jq
  - R 4.x + packages: yaml, jsonlite, readr
  - Sprocket CLI (https://sprocket.bio/installation.html)
  - VS Code Server (code-server) OR SSH for VS Code Remote
  - Team repo cloned
```

### Runner machine (optional — one per team)

```text
CPU:       8–16 vCPU
RAM:       64 GB minimum
Storage:   150–200 GB
Software:  Docker, Sprocket CLI, R 4.x
Data:      Victoria Knockout Cell Ranger outputs pre-staged
```

### Per participant (own laptop)

```text
- Git, VS Code (Remote-SSH to VM)
- GitHub Copilot / LLM (optional, runs locally)
- Docker Desktop (optional — if acting as runner)
```

### Not required

| Item | Why skip |
|------|----------|
| LSF / `bsub` | HPC only |
| Apptainer / Singularity | Use Docker backend locally |
| GPU | No GPU steps in this workflow |
| 100 GB VM RAM | 64 GB on runner only if doing live Seurat |
| Jupyter / conda | SNAP downstream is R/Rmd |
| Cell Ranger on event day | Pre-stage outputs only |

---

## Local Sprocket config

Use **`sprocket.local.toml`** in the analysis repo (Docker backend, not LSF):

**File:** `analyses/sc-rna-seq-snap-Victoria-Knockout/sprocket.local.toml`

```toml
[run]
backend = "local_docker"

[run.backends.local_docker]
type = "docker"
max_concurrency = 2

[run.workflow.scatter]
concurrency = 4
```

Production HPC config remains in `sprocket.toml` (`lsf_apptainer`). Do not overwrite it.

**Sprocket Docker backend reference:** [sprocket.bio/configuration/backends/docker.html](https://sprocket.bio/configuration/backends/docker.html)

---

## YAML changes for local runs

In `project_parameters.Config.yaml`, point the container image at Docker (not a local `.sif`):

```yaml
resource_profile:
  container_image: "docker://achroni/rstudio_4.4.0_seurat_4.4.0:latest"
```

For **validate-only** (Tier 1), the image string is checked by Sprocket but the container does not need to execute.

For **live runs** (Tier 2), pull the image first:

```bash
docker pull achroni/rstudio_4.4.0_seurat_4.4.0:latest
```

Upstream-only profile for first live test:

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

## Important: launcher vs local workflow

`launch-snap-downstream.sh` / `launch-snap-sprocket.sh` **require Apptainer/Singularity** on PATH (even for dry-run) and use `sprocket.toml` (LSF). On a VM without Singularity, **run the steps below manually** instead of the root launcher.

### Tier 1 — Validation (shared VM, no Docker execution)

```bash
cd analyses/sc-rna-seq-snap-Victoria-Knockout

# Layout check (no Sprocket)
bash scripts/test-downstream-layout.sh

# Generate WDL from workflow_profile toggles
Rscript scripts/generate-snap-wdl.R --output wdl/snap.wdl

# Estimate resources; refresh inputs/project_parameters.generated.yaml
Rscript scripts/estimate-snap-downstream-resources.R \
  --snap-root . \
  --output inputs/generated_downstream.json \
  --update-yaml

# Sprocket syntax + input validation (local Docker config)
sprocket check wdl/snap.wdl
sprocket validate wdl/snap.wdl @inputs/sprocket_inputs.json --config sprocket.local.toml
```

If Cell Ranger metrics are missing, add:

```bash
Rscript scripts/estimate-snap-downstream-resources.R \
  --snap-root . \
  --estimated-cells-per-sample 8208 \
  --output inputs/generated_downstream.json \
  --update-yaml
```

### Tier 2 — Live run (runner machine only)

```bash
cd analyses/sc-rna-seq-snap-Victoria-Knockout

# Repeat Tier 1 steps after any YAML change, then:
sprocket run wdl/snap.wdl @inputs/sprocket_inputs.json --config sprocket.local.toml

# Monitor
ls -la out/runs/sc_rna_seq_snap_downstream/_latest/calls/
```

Use **tmux** on the runner; only one live run at a time. Expect **1–3+ hours** for upstream on 4 samples.

### Tier 3 — Module scripts without Sprocket (biology check only)

Does **not** test the orchestrator; validates Seurat modules in Docker:

```bash
docker pull achroni/rstudio_4.4.0_seurat_4.4.0:latest
docker run --platform linux/amd64 -it \
  -v "$(pwd)":/home/rstudio/sc-rna-seq-snap \
  achroni/rstudio_4.4.0_seurat_4.4.0:latest bash

# inside container:
cd /home/rstudio/sc-rna-seq-snap/analyses/upstream-analysis
bash run-upstream-analysis.sh
```

See [run-container/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/run-container/README.md).

---

## Install Sprocket (VM or laptop)

Pick one method from [sprocket.bio/installation.html](https://sprocket.bio/installation.html):

```bash
# Example: run via Docker without installing the binary
docker run --rm ghcr.io/stjude-rust-labs/sprocket:latest --help

# Or install binary to PATH, then:
sprocket --version
```

Verify Docker:

```bash
docker info
```

---

## No-HPC test matrix

Log results in [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md). Use IDs **L1–L18**. Status: `PASS` | `FAIL` | `SKIP` | `BLOCKED`.

| ID | Test | Tier | Owner track | Environment | Command / action | Expected |
|----|------|------|-------------|-------------|------------------|----------|
| **L1** | Layout sanity | 1 | B | VM | `bash scripts/test-downstream-layout.sh` | Required files present |
| **L2** | WDL generation | 1 | A | VM | `Rscript scripts/generate-snap-wdl.R --output wdl/snap.wdl` | `wdl/snap.wdl` updated |
| **L3** | Resource estimation | 1 | B | VM | `Rscript scripts/estimate-snap-downstream-resources.R --snap-root . --output inputs/generated_downstream.json --update-yaml` | JSON + generated YAML created |
| **L4** | Upstream-only WDL | 1 | A | VM | Set `run_upstream: true` only; re-run L2 | WDL contains upstream task only |
| **L5** | Three-module WDL | 1 | A | VM | Enable upstream + integrative + cluster; re-run L2 | Three tasks in generated WDL |
| **L6** | `sprocket check` | 1 | B | VM | `sprocket check wdl/snap.wdl` | No syntax errors |
| **L7** | `sprocket validate` | 1 | B | VM | `sprocket validate wdl/snap.wdl @inputs/sprocket_inputs.json --config sprocket.local.toml` | Validation passes |
| **L8** | Docker image in YAML | 1 | B | VM | `container_image: docker://achroni/rstudio_4.4.0_seurat_4.4.0:latest` | Re-run L3–L7 |
| **L9** | Error — bad path | 1 | B | VM | Break `root_dir` in YAML; re-run L3 | Clear error message |
| **L10** | Error — missing metadata | 1 | B | VM | Rename `project_metadata.tsv`; re-run L3 | Error cites missing metadata |
| **L11** | Generated YAML overlay | 1 | A | VM | Inspect `inputs/project_parameters.generated.yaml` | Master YAML unchanged |
| **L12** | Module dependency chain | 1 | A | VM | Disable middle module; re-run L2 | Skipped module bypassed in WDL |
| **L13** | Legacy vs new comparison | 1 | C | VM | Compare `launch_full_pipeline.sh` vs `workflow_profile` | Table for slides |
| **L14** | ROI timing | 1 | C | VM | Time YAML edit + L2–L7 vs legacy bash | Minutes to validate-ready |
| **L15** | Troubleshooting doc | 1 | C | VM | Log real errors + fixes | Updates to `troubleshooting.md` |
| **L16** | Docker image pull | 2 | D | Runner | `docker pull achroni/rstudio_4.4.0_seurat_4.4.0:latest` | Image available locally |
| **L17** | Live upstream run | 2 | D | Runner | `sprocket run … --config sprocket.local.toml` (upstream only) | Task completes or logs visible |
| **L18** | Biology sanity | 2 | D | Runner | Review upstream QC / cell counts | Tanjim sign-off |

### Mapping from HPC matrix (if comparing plans)

| HPC ID | Local equivalent |
|--------|------------------|
| T1 | L1 |
| T2 | L2 + L3 + L6 + L7 |
| T3 submit | L17 |
| T5–T6 | L9–L10 |
| T7–T8 | L3 (+ `--estimated-cells-per-sample` for L3 variant) |
| T9–T11 | L11–L12 |
| T12 parallel workers | SKIP (HPC/NFS concern; not applicable locally) |
| T13–T15 | L17 (+ monitor `out/runs/…`) |
| T16 | L18 |
| T17–T19 | L13–L15 |
| T20 multi-project | SKIP unless time — validate `snap_multi_project.wdl` only |

### Definition of done (no HPC)

- [ ] L1–L7 pass on shared VM
- [ ] L13–L15 complete (ROI + troubleshooting)
- [ ] At least **12 of 18** local tests logged
- [ ] Slides + 5-min demo (show L7 validate live; L17 recording optional)
- [ ] L17–L18 are **stretch** — not required if runner lacks 64 GB RAM

---

## Shared VM workflow (one machine, many people)

```bash
tmux new -s team15
# Window 0: Track C — docs / test log
# Window 1: Track B — L1–L10 (one command runner at a time)
# Window 2: Track A — code review
# Window 3: Track D — slides / runner coordination
```

**Rules:**

- Only **one person** runs `Rscript` / `sprocket` commands on the VM at a time.
- **Never** run L17 on the 32 GB shared VM — use the runner machine.
- Everyone else edits docs, reviews PRs, or works on laptops in parallel.

---

## Pre-hackathon checklist (no HPC)

- [ ] Shared VM provisioned (8 vCPU, 32 GB, 100 GB)
- [ ] Sprocket CLI installed on VM (`sprocket --version`)
- [ ] R 4.x on VM (`Rscript --version`)
- [ ] Repo cloned; L1 passes
- [ ] Cell Ranger outputs for Victoria Knockout accessible to runner (copy or mount)
- [ ] Runner machine identified (64 GB RAM, Docker)
- [ ] Docker image pulled on runner (L16)
- [ ] `container_image` set to `docker://…` in YAML for local tests
- [ ] Optional: pre-run L17 upstream once for demo backup artifacts

---

## Day-of verification (first 15 minutes)

**On shared VM:**

```bash
cd KIDS26-Team15/analyses/sc-rna-seq-snap-Victoria-Knockout
bash scripts/test-downstream-layout.sh
Rscript scripts/generate-snap-wdl.R --output wdl/snap.wdl
sprocket check wdl/snap.wdl
```

**On runner (if doing Tier 2):**

```bash
docker info
docker images | grep rstudio
sprocket validate wdl/snap.wdl @inputs/sprocket_inputs.json --config sprocket.local.toml
```

Log L1, L2, L6 in [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md).

---

## Common blockers (no HPC)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `launch-snap-downstream.sh` fails immediately | Requires Singularity | Use **manual Tier 1 steps** above, not the HPC launcher |
| `sprocket: command not found` | Not installed | Install from [sprocket.bio](https://sprocket.bio/installation.html) |
| `validate` fails on container image | `.sif` path in YAML | Set `docker://achroni/rstudio_4.4.0_seurat_4.4.0:latest` |
| `docker: command not found` on VM | Docker not on shared VM | Run L16–L17 only on runner laptop |
| OOM during L17 | Insufficient RAM | Use 64 GB runner; upstream-only; reduce concurrency in `sprocket.local.toml` |
| Missing Cell Ranger metrics | Data not staged | `--estimated-cells-per-sample 8208` or copy metrics from HPC |
| VM slow with everyone logged in | Concurrent R/sprocket | One runner at a time; use tmux queues |

---

## Request text for organizers (copy-paste, no HPC)

> **KIDS26 Team 15 — infrastructure request (no HPC)**
>
> We are testing a SNAP + Sprocket workflow orchestrator for single-cell RNA-seq without St. Jude HPC access.
>
> 1. **One shared Linux VM:** 8 vCPU, 32 GB RAM, 100 GB disk, git, tmux, R 4.x, Sprocket CLI, VS Code Server, GitHub access.
> 2. **Per participant:** GitHub access; personal laptop with VS Code and optional Copilot.
> 3. **Optional runner machine (team-provided):** 64 GB RAM, Docker, for one live pipeline test.
> 4. **Pre-staged data:** Victoria Knockout Cell Ranger outputs (we provide copy instructions).
>
> We do **not** need LSF, Apptainer, GPU, or 100 GB VM RAM.

---

## Related files

| File | Purpose |
|------|---------|
| [sprocket.local.toml](../analyses/sc-rna-seq-snap-Victoria-Knockout/sprocket.local.toml) | Docker backend config for local/VM |
| [sprocket.toml](../analyses/sc-rna-seq-snap-Victoria-Knockout/sprocket.toml) | Production LSF + Apptainer (HPC) |
| [vm-hpc-setup.md](./vm-hpc-setup.md) | Plan when HPC **is** available |
| [hackathon-runbook.md](../project-management/hackathon-runbook.md) | Pairs, timeline, full HPC test matrix |

---

**Maintainer:** KIDS26 Team 15  
**Last updated:** 2026-09-01
