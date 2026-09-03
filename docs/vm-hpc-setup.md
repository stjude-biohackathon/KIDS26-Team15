# VM and HPC Setup — KIDS26 Team 15

**Project:** Resource-Aware SNAP + Sprocket Orchestrator  
**Context:** One shared VM for the team + St. Jude HPC for real pipeline runs  
**Related:** [hackathon-runbook.md](../project-management/hackathon-runbook.md) · [hackathon-test-results.md](../results/hackathon-test-results.md) · [resources-snap.md](./resources-snap.md) · [vm-local-only-setup.md](./vm-local-only-setup.md) (no HPC)

---

## Summary

| Environment | Role | Required for |
|-------------|------|--------------|
| **Shared VM** | Coordination hub — git, YAML edits, dry-run validation, docs, slides | T1–T11, T17–T19 (mostly) |
| **St. Jude HPC** | Execution engine — Sprocket submit, Apptainer, LSF jobs | T3 submit, T7, T12–T16, T20 |
| **Personal laptop** | IDE, Copilot/LLM, SSH client, slide editing | All tracks (parallel to VM) |

**Do not plan to run full Seurat upstream on the shared VM.** Use HPC for any `launch-snap-downstream.sh --submit` test.

---

## What to request from organizers

### Shared VM (one per team)

```text
OS:        Linux (RHEL 8+ or Ubuntu 22.04+)
CPU:       8 vCPU
RAM:       32 GB
Storage:   100 GB
Network:   outbound HTTPS (git, GitHub) + SSH to St. Jude HPC

Pre-installed:
  - git, tmux, screen, curl, jq
  - bash, vim or nano
  - R 4.x + packages: yaml, jsonlite, readr (for resource estimator)
  - VS Code Server (code-server) OR SSH access for VS Code Remote
  - Team repo cloned and readable by all participants
```

### Per participant (own laptop)

```text
- GitHub account with repo access
- Git client
- VS Code (with Remote-SSH) and/or RStudio locally
- GitHub Copilot or preferred LLM (optional; runs locally, not on VM)
- Browser for GitHub, slides, shared docs
```

### St. Jude HPC (required for real testing)

```text
module load sprocket R singularity

Apptainer image:
  rstudio_4.4.0_seurat_4.4.0_latest.sif
  (path set in project_parameters.Config.yaml → resource_profile.container_image)

LSF queue access for workflow submit tests
Read access to Victoria Knockout analysis data and Cell Ranger outputs
```

**Sprocket reference:** [sprocket.bio/overview.html](https://sprocket.bio/overview.html)

---

## What to request vs skip

| Item | Request? | Notes |
|------|----------|-------|
| GitHub Copilot / LLM | ✅ Per person (laptop) | Not a VM install; each teammate uses their own tool |
| Claude API / AI Foundry | ⚠️ Optional | Helpful for coding; not required to run or demo the orchestrator |
| VS Code | ✅ Yes | Prefer **code-server** on VM or **Remote-SSH** from laptops |
| R + RStudio | ✅ Yes (limited) | Needed for `estimate-snap-downstream-resources.R`; avoid many concurrent RStudio sessions |
| Jupyter + conda | ⚠️ Optional | SNAP downstream is R/Rmd; skip unless doing extra Python analysis |
| Docker | ❌ Skip | Production path uses **Apptainer/Singularity** on HPC, not Docker |
| Sprocket | ✅ HPC | May not install on a generic VM; dry-run steps work without it |
| GPU | ❌ Skip | No GPU step in this SNAP downstream workflow |
| 100 GB VM RAM | ❌ Skip | Overkill; 32 GB is enough for dry-run and docs |
| 100 GB storage | ✅ Yes | Repo, logs, screenshots; `.sif` only if local container tests are needed |
| 8 vCPU | ✅ Yes | Enough for shared coordination; heavy compute stays on HPC |

---

## VM vs HPC capability matrix

| Task | Shared VM | St. Jude HPC |
|------|:---------:|:------------:|
| Clone repo, edit YAML | ✅ | ✅ |
| `bash scripts/test-downstream-layout.sh` | ✅ | ✅ |
| `bash launch-snap-downstream.sh` (dry-run) | ✅ | ✅ |
| `estimate-snap-downstream-resources.R` | ✅ | ✅ |
| `sprocket check` / `validate` | ⚠️ if `module load sprocket` works | ✅ |
| `launch-snap-downstream.sh --submit` | ❌ | ✅ |
| `bjobs`, LSF monitoring | ❌ | ✅ |
| Email notifications on submit | ❌ | ✅ |
| Full Seurat upstream run | ❌ (too slow) | ✅ |
| `SNAP_FUTURE_WORKERS` parallel test (T12) | ❌ | ✅ |

If Sprocket is unavailable on the VM, Tracks B and C continue with T1–T6 and T9–T11; St. Jude members (Jason, Rojina, Antonia) run T7+ and T13–T16 on HPC.

---

## Shared VM workflow (one machine, many people)

### Use tmux, not one desktop session

```bash
tmux new -s team15

# Suggested windows
# 0: Track C — docs / test log
# 1: Track B — dry-run commands (one runner at a time)
# 2: Track A — code review
# 3: Track D — demo / slides
```

**Rule:** Only **one person** runs launcher commands (`launch-snap-downstream.sh`, `sprocket`, `Rscript` estimator) at a time. Others edit docs, review code, or work on laptops in parallel.

### Suggested track split

| Track | VM | HPC |
|-------|----|-----|
| A — Code review | Read scripts/WDL in VS Code | Optional `sprocket validate` |
| B — Testing | T1–T6, resource estimator dry-run | T3 submit, T7–T8, T13–T16 |
| C — Docs & PRs | Test log, markdown, PR reviews | Collect HPC screenshots from others |
| D — Demo | Slides, demo script | Golden-path submit + `bjobs` |

---

## Pre-hackathon setup checklist (team lead)

Complete before event day to save 1–2 hours.

- [ ] Shared VM provisioned with specs above
- [ ] All teammates have VM SSH access (or shared account + tmux agreement)
- [ ] Repo cloned on VM: `KIDS26-Team15/analyses/sc-rna-seq-snap-Victoria-Knockout`
- [ ] `bash scripts/test-downstream-layout.sh` passes on VM
- [ ] R available: `Rscript --version`
- [ ] HPC access confirmed for Jason, Rojina, Antonia (submit tests)
- [ ] On HPC: `module load sprocket R singularity` works
- [ ] Cell Ranger complete for Victoria Knockout
- [ ] `data/project_metadata/project_metadata.tsv` present
- [ ] Apptainer `.sif` path valid in `project_parameters.Config.yaml`
- [ ] One upstream-only job pre-submitted on HPC (demo backup)
- [ ] tmux session `team15` created; window layout agreed
- [ ] Shared test log linked: [hackathon-test-results.md](../results/hackathon-test-results.md)

---

## Day-of verification (first 15 minutes)

Run on the **shared VM**:

```bash
cd KIDS26-Team15/analyses/sc-rna-seq-snap-Victoria-Knockout

git status
bash scripts/test-downstream-layout.sh
bash launch-snap-downstream.sh    # dry-run only
Rscript --version
```

Run on **HPC** (St. Jude members):

```bash
module load sprocket R singularity
sprocket --version
Rscript --version
singularity --version

cd /path/to/sc-rna-seq-snap-Victoria-Knockout
bash launch-snap-downstream.sh    # dry-run
```

Log results in [hackathon-test-results.md](../results/hackathon-test-results.md) (T1, T2).

---

## Common blockers and fixes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `sprocket: command not found` on VM | Sprocket not installed on VM | Use HPC for validate/submit; VM does layout + YAML tests only |
| Dry-run fails on missing Cell Ranger | Metrics not staged | Complete Cell Ranger on HPC or pass `--estimated-cells-per-sample` to estimator |
| `singularity: command not found` | Module not loaded | `module load singularity` on HPC before launch |
| VM feels slow with everyone logged in | Concurrent RStudio / heavy R | One runner at a time; use VS Code for editing; run R estimator once |
| Cannot submit from VM | No LSF on VM | Expected — hand off T13–T16 to HPC pair |
| Container pull / path error | Wrong `container_image` in YAML | Use full path to local `.sif`; re-run launcher to regenerate `sprocket_inputs.json` |
| NFS bus error with parallel R | `SNAP_FUTURE_WORKERS > 1` in container | Default `SNAP_FUTURE_WORKERS=1`; document in T12 on HPC |

See also [troubleshooting.md](./troubleshooting.md) and [scripts/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md).

---

## Request text for organizers (copy-paste)

> **KIDS26 Team 15 — infrastructure request**
>
> We are testing a SNAP + Sprocket workflow orchestrator for single-cell RNA-seq. We need:
>
> 1. **One shared Linux VM:** 8 vCPU, 32 GB RAM, 100 GB disk, git, tmux, R 4.x, VS Code Server (or SSH for Remote-SSH), outbound access to GitHub and St. Jude HPC.
> 2. **Per participant:** GitHub repo access; personal IDE with optional Copilot/LLM on their own laptop.
> 3. **St. Jude HPC (required):** `module load sprocket R singularity`, LSF submit access, Seurat Apptainer image, read access to Victoria Knockout Cell Ranger outputs.
>
> We do **not** need GPU, Docker, or 100 GB RAM on the VM. Full pipeline execution will run on HPC, not the shared VM.

---

**Maintainer:** KIDS26 Team 15  
**Last updated:** 2026-09-01
