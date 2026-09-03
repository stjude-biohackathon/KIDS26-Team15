# WILDS WDL Library

**Repository:** [WILDS WDL Library](https://github.com/getwilds/wilds-wdl-library)

The **WILDS WDL Library** is a centralized collection of reusable bioinformatics workflows and workflow components developed through the Fred Hutch **WILDS (Workflows, Informatics, and Data Science)** program. Its goal is to provide researchers with tested, production-ready WDL components instead of requiring every project to build workflows from scratch.

---

## Key Takeaway

**The WILDS WDL Library is not a workflow engine.**

Instead, it is a **reusable collection of WDL modules and pipelines** that can be executed using workflow engines such as:

- Sprocket
- Cromwell
- miniWDL
- PROOF
- Cirro

Think of it as a shared library of workflow building blocks and reference implementations.

---

# Main Goals

## 1. Reusable Workflow Infrastructure

Provide production-ready WDL tasks and workflows for common genomics and bioinformatics analyses.

Benefits include:

- Reduced duplication of effort
- Faster workflow development
- Standardized implementations
- Community-reviewed components

---

## 2. Modularity

Workflows are designed as composable building blocks that can be reused across projects.

Rather than creating a monolithic workflow, the library encourages:

```text
Module A
   ↓
Module B
   ↓
Module C
```

where individual modules can be mixed and matched to support custom analysis pipelines.

---

## 3. Reproducibility

Promote reproducible workflows through:

- Version-controlled WDL definitions
- Standardized workflow patterns
- Tested implementations
- Versioned container environments

This helps ensure analyses can be rerun and shared consistently across teams and institutions.

---

## 4. Scalable Computing Accessibility

Reduce the barrier to running workflows on modern compute infrastructure.

The library is designed to support execution across:

- HPC clusters
- Cloud platforms
- Local development environments

through workflow engines such as:

- Cromwell
- miniWDL
- Sprocket
- Fred Hutch PROOF
- Cirro

---

## 5. WDL Best Practices

Serve as reference implementations for:

- Workflow organization
- Task design
- Input management
- Testing strategies
- Documentation patterns

Researchers can learn WDL by studying production-quality examples.

---

## 6. Community-Driven Development

The library grows through collaboration between researchers and informatics groups.

The WILDS WDL Development Program helps convert existing research analyses into reusable, production-ready WDL workflows that can benefit the broader community.

---

# Architecture

The repository follows a two-level architecture:

```text
wilds-wdl-library/
├── modules/
└── pipelines/
```

---

## 1. Modules (`modules/`)

Modules are reusable task wrappers around individual bioinformatics tools.

Examples include:

- STAR
- BWA
- GATK
- SRA download
- Other commonly used genomics tools

### Characteristics

- Designed to be imported into other workflows
- Tested independently
- Often include example test workflows
- Can serve as workflow building blocks

Conceptually:

```text
STAR Alignment
BWA Mapping
GATK Variant Calling
SRA Download
```

Each module performs a specific task and can be reused across many workflows.

---

## 2. Pipelines (`pipelines/`)

Pipelines combine multiple modules into complete end-to-end analyses.

Examples range from:

- Small workflows (2–3 modules)
- Large workflows (10+ modules)

A typical pipeline may look like:

```text
SRA Download
        ↓
STAR Alignment
        ↓
Post-processing
        ↓
Reporting
```

### Included Resources

Most pipelines provide:

- Example `inputs.json`
- Documentation
- Usage examples
- Integration tests

These workflows can be used directly or adapted for local projects.

---

# How the Library Is Used

## Option 1: Run an Existing Pipeline

A complete workflow can be executed using a supported workflow engine:

```bash
sprocket run ww-sra-star.wdl @inputs.json
```

This approach is useful when an existing pipeline already solves the analysis problem.

---

## Option 2: Import Individual Modules

Modules can be imported into custom WDL workflows.

Example:

```wdl
import "https://raw.githubusercontent.com/getwilds/wilds-wdl-library/.../ww-sra.wdl" as sra_tasks
```

This enables workflow developers to reuse tested components instead of rewriting task definitions.

---

# Quality and Development Standards

The project emphasizes software engineering and workflow quality practices.

Key features include:

- Continuous Integration (CI) testing
- Automated validation
- Unit testing
- Integration testing
- Multi-executor compatibility testing
- Documentation and examples

This helps ensure workflows behave consistently across different workflow engines and execution environments.

---

# Why It Matters

Many bioinformatics groups struggle with:

- Repeatedly rewriting the same workflow components
- Inconsistent workflow implementations
- Limited testing and validation
- Difficulty sharing workflows across teams

The WILDS WDL Library addresses these challenges by providing a curated collection of reusable and tested workflow components.

For workflow developers, it serves as both:

1. A **library of reusable tasks**
2. A **reference for WDL best practices**

---

# Relationship to Sprocket

The WILDS WDL Library and Sprocket solve different problems:

| Component | Purpose |
|------------|---------|
| **WILDS WDL Library** | Provides reusable WDL workflows and modules |
| **Sprocket** | Executes and orchestrates WDL workflows |
| **Cromwell** | Executes WDL workflows |
| **miniWDL** | Executes and validates WDL workflows |

A useful analogy is:

```text
WILDS WDL Library = Workflow code
Sprocket = Workflow engine
```

You can use WILDS workflows with Sprocket, but the library itself does not execute workflows.

---

# Relevance to sc-rna-seq-snap

For a project such as **sc-rna-seq-snap**, the library provides useful design patterns for:

- Modular workflow organization
- Reusable task definitions
- Workflow testing
- Input/output standardization
- Containerized execution
- Dependency management

It can serve as a reference when converting existing Bash-driven pipelines into maintainable WDL workflows.

---

# Summary

The **WILDS WDL Library** is a community-driven collection of reusable WDL workflows and task modules designed to:

- Promote workflow reuse
- Improve reproducibility
- Encourage standardized workflow development
- Lower barriers to scalable computing
- Teach WDL best practices

Its primary value is enabling researchers to build production-quality workflows faster by leveraging tested, reusable workflow components rather than starting from scratch.


