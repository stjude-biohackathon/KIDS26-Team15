# WDL/Sprocket vs Other Alternatives — Stakeholder Evaluation

**Updated:** 2026-09-18  
**Purpose:** Defensible comparison for stakeholders reviewing Daedalus orchestration choices  
**Scope:** WDL/Sprocket (chosen) vs legacy bash, Nextflow, Snakemake, other WDL engines, CWL, R-native, GUI, and cloud options  

---

## Executive summary

SNAP needed better orchestration on St. Jude LSF—not a full pipeline rewrite. We evaluated **nine approaches** against practical criteria: **migration effort**, **LSF/HPC fit**, **team skills**, **community pipeline reuse**, and **available evidence**.

**WDL + Sprocket (with Daedalus)** was chosen because it wraps existing R/bash modules in `analyses/*`, runs on the institution-supported HPC stack (`module load sprocket`, `lsf_apptainer`), validates workflows before submit, and delivered **measured gains vs the legacy bash launcher** on Victoria Knockout (−37% upstream wall time, +45 pp memory efficiency, identical biology).

Alternatives were viable in other contexts but weaker for this project:

- **Improved legacy bash** — lowest effort, but does not fix orchestration, validation, or resource waste at scale.
- **Nextflow / nf-core** — strong for greenfield or upstream-only pipelines; high rewrite cost for SNAP's custom downstream.
- **Snakemake, CWL, R-native, Galaxy, cloud** — technically possible; weaker St. Jude fit, higher adoption friction, or out of scope for HPCF production.

We did **not** run head-to-head runtime benchmarks against every alternative. Evidence is strongest for **WDL/Sprocket vs legacy bash** (measured ROI). Other comparisons are qualitative, based on migration cost and institutional fit.

**Recommendation:** WDL/Sprocket remains the defensible path for St. Jude SNAP on LSF today. Revisit other options only if compute strategy, upstream standardization (e.g. nf-core), or external collaboration requirements change.

---

## What we were replacing

The pain point was **manual LSF wiring** in the legacy SNAP launcher (`launch_full_pipeline.sh` + per-module `lsf-script.txt`):

| Legacy problem | What analysts did |
|----------------|-------------------|
| Module selection | Edit bash flags / LSF scripts per module |
| Resources | Fixed CPU/memory, often wrong for cohort size |
| Dependencies | Hand-chain `bsub -w "done(jobN)"` |
| Re-runs | Reconfigure everything when sample count changes |

The chosen path (Daedalus / `launch-snap-downstream.sh`) replaces that with:

```text
YAML toggles  →  generate WDL
Cell Ranger   →  estimate resources (R script)
Both          →  sprocket validate / run
```

---

## Evaluation criteria

All alternatives were assessed on the same axes:

| Criterion | Question |
|-----------|----------|
| **Migration effort** | How much of SNAP must be rewritten vs wrapped? |
| **LSF / HPC fit** | Does it run natively on St. Jude HPCF with documented support? |
| **Team skills** | Is there an onboarding path for this team? |
| **Community reuse** | Can we adopt nf-core, WILDS, or other shared modules? |
| **Resource scaling** | Can we size jobs from Cell Ranger metrics (Daedalus layer)? |
| **Evidence** | Do we have measured ROI or only qualitative assessment? |

---

## WDL Compared with Nextflow

Nextflow is considered the lingua franca of bioinformatics workflow languages. With the scalability  incredibly flexible, which comes with a tradeoff in complexity. If a team already has a Nextflow pipeline, it makes sense to continue using it. However, for teams working primarily with Bash or other scripts today, WDL can be faster to learn and set up. If complexity needs evolve over time, it may make sense to reconsider Nextflow.

WDL is intended to be user-friendly while still supporting the workflow features needed for bioinformatics. Nextflow offers more advanced features than WDL (i.e., functional programming), which makes sense for some bioinformatics workloads. However, those features are not necessary for the SNAP workflow.

WDL is developed as a community-driven open standard, while Nextflow is open source but not community-driven. The community-driven model fits with St. Jude's ethos and commitment to community collaboration and encourages sustainable longer-term adoption.

Finally, St. Jude benefits from having strong in-house talent that helps maintain the WDL language, which means expert advice is always close at hand.

## WDL Compared with CWL

WDL and CWL were identified as the two community-driven open standards for bioinformatics workflows.

WDL benefits from close involvement by people who understand both workflow language design and bioinformatics practice. In-house St. Jude talent helps support and develop the language. Having that expertise available within the organization makes it easier to get practical guidance when building workflows.

## Conclusion: why WDL?
1. **Ease of use:** WDL is designed to be readable and writable by humans, making workflows easier to understand and maintain.
2. **Community development:** WDL is an open, community-developed standard which aligns with the St. Jude Ethos.
3. **Strong typing:** WDL is a strongly typed language customized for bioinformatics. Types help catch mismatched inputs and other errors before execution.
4. **In-house support:** Having experienced WDL developers and users available within the organization is especially valuable when teams are learning the language or troubleshooting workflows.

Overall, the team decided that WDL strikes a practical balance between complexity and language features for the users of Daedalus.

---

## Technical notes on Workflow Graphs in WIDL

WDL workflows are represented as directed acyclic graphs (DAGs). Each task is a node, and the dependencies between tasks form the edges of the analysis graph.

By defining a workflow, a team makes the structure of the analysis explicit. The graph can be inspected before anything runs, which helps users understand dependencies, identify opportunities for parallel execution, and catch structural problems early.

Sprocket provides an execution environment for running WDL workflows, while WDL provides the language used to define the workflow and its dependencies.

---

**Maintainer:** KIDS26 Team 15 · **Status:** Draft for stakeholder review
