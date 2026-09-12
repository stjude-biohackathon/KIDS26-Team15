# VM and HPC Setup — KIDS26 Team 15

**Project:** Resource-Aware SNAP + Sprocket Orchestrator  
**Context:** One shared VM for the team + St. Jude HPC for real pipeline runs  
**Related:** [hackathon-runbook.md](../project-management/hackathon-runbook.md) · [hackathon-test-log.md](../deliverables/validation/hackathon-test-log.md) · [resources-snap.md](./resources-snap.md) · [vm-local-only-setup.md](./vm-local-only-setup.md) (no HPC)

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

**HPC testers:** Rojina Sapkota and Antonia Chroni only. 

```text
module load sprocket R singularity

Apptainer image:
  rstudio_4.4.0_seurat_4.4.0_latest.sif
  (path set in project_parameters.Config.yaml → resource_profile.container_image)

LSF queue access for workflow submit tests
Read access to Victoria Knockout analysis data and Cell Ranger outputs
```

---


**Maintainer:** KIDS26 Team 15  
**Last updated:** 2026-09-12
