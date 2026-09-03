# Learning Path: WDL, Sprocket, and Containers

A recommended reading order for building bioinformatics workflows. Follow these steps in sequence — each builds on the last.

**Curated by:** Clay McLeod and Antonia Chroni (August 31, 2026)

**Related team docs:**

- [resources-snap.md](resources-snap.md) — what SNAP is and how the analysis pipeline is organized
- [resources-sprocket.md](resources-sprocket.md) — what Sprocket does and how the repo is organized
- [resources-wilds-wdl.md](resources-wilds-wdl.md) — overview of the WILDS WDL Library
- [resources-trainings.md](resources-trainings.md) — St. Jude GitHub team guide and reproducibility course

---

## Step 1 — Study expert WDL examples

Start by reading production-quality WDL before writing your own. The [WILDS WDL Library](https://github.com/getwilds/wilds-wdl-library) is a collection of tested, reusable bioinformatics modules and pipelines.

| Resource | Link |
|----------|------|
| Library website | [getwilds.org/wilds-wdl-library](http://getwilds.org/wilds-wdl-library/) |
| Example module (BWA) | [modules/ww-bwa](https://github.com/getwilds/wilds-wdl-library/tree/main/modules/ww-bwa) |

**Why start here:** These modules are tested across multiple WDL execution engines and reflect high-quality development patterns. Use them as reference implementations, not just copy-paste snippets.

---

## Step 2 — Learn WDL 1.3 (the language)

Target **WDL 1.3** — this is what Sprocket supports and what you should write.

| Resource | Link |
|----------|------|
| OpenWDL documentation | [docs.openwdl.org/overview.html](https://docs.openwdl.org/overview.html) |

**What to know:** OpenWDL docs are engine-agnostic (Cromwell, miniWDL, Sprocket, and others all run WDL). Everything in these docs applies to Sprocket because Sprocket runs standard WDL.

---

## Step 3 — Install and configure Sprocket

Once you understand WDL syntax, set up the engine that will run your workflows.

| Resource | Link |
|----------|------|
| Sprocket overview | [sprocket.bio/overview.html](https://sprocket.bio/overview.html) |
| Installation (local laptops) | [sprocket.bio/installation.html](https://sprocket.bio/installation.html) |

**On the St. Jude cluster**, you can skip local installation:

```bash
module load sprocket
```

**Scope note:** For hackathon work, the overview and installation pages are usually enough. See [resources-sprocket.md](resources-sprocket.md) for a deeper look at CLI commands and repo layout.

---

## Step 4 — Understand containers

Neither the WDL nor Sprocket guides go deep on containers, but real workflows depend on them. Work through these in order:

| Order | Topic | Link |
|-------|-------|------|
| 4a | What containers are and why they matter | [AWS: What is a container?](https://aws.amazon.com/what-is/cloud-containers/) |
| 4b | Install Docker Desktop (build and run containers locally) | [Docker: Introduction](https://docs.docker.com/get-started/introduction/) |
| 4c | Write container images with Dockerfiles | [Docker: Writing a Dockerfile](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/) |

**Why this matters:** WDL tasks run inside container images. You need Docker locally to build and test images; on HPC, Sprocket typically runs them via Apptainer/Singularity.

---

## At a glance

| Step | Goal | Time investment |
|------|------|-----------------|
| 1 | See what good WDL looks like | Browse examples |
| 2 | Learn WDL 1.3 syntax and concepts | Read OpenWDL docs |
| 3 | Install Sprocket and run a workflow | Follow installation guide |
| 4 | Build and use container images | Work through Docker guides |

---

## Checklist

Use this to track your progress:

- [ ] Read at least one WILDS module (e.g. [ww-bwa](https://github.com/getwilds/wilds-wdl-library/tree/main/modules/ww-bwa))
- [ ] Review [OpenWDL overview](https://docs.openwdl.org/overview.html) for WDL 1.3
- [ ] Install Sprocket locally **or** confirm `module load sprocket` works on cluster
- [ ] Read the container intro and install Docker Desktop
- [ ] Complete the Dockerfile tutorial
