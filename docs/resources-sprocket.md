# Sprocket

**Repository:** [Sprocket](https://github.com/stjude-rust-labs/sprocket)

Sprocket is a high-performance bioinformatics workflow engine developed by St. Jude Rust Labs and built around the **Workflow Description Language (WDL)**. It provides the infrastructure needed to define, validate, execute, and monitor scientific workflows at scale, from local development environments to HPC systems. 

---

## Key Takeaway

**Sprocket is not an analysis tool.**

It is a **WDL-native workflow platform** that serves as an orchestration layer for bioinformatics workflows. Instead of manually chaining scripts and scheduler jobs, researchers define workflow logic in WDL while Sprocket manages execution, dependencies, scheduling, monitoring, and recovery. 

---

## Why Was Sprocket Created?

Bioinformatics pipelines are often composed of many shell, R, and Python scripts connected through custom orchestration logic. As workflows grow in complexity, it becomes increasingly difficult to manage:

- Dependencies between steps
- Resource allocation
- Error handling and retries
- Reproducibility
- Portability across computing environments

Sprocket addresses these challenges by providing a standardized workflow execution framework based on WDL. 

---

## Main Goals

Sprocket enables workflows to be:

- **Portable** across computing environments
- **Validated and linted** before execution
- **Reproducible** through standardized workflow definitions
- **Scalable** across HPC and container platforms
- **Observable** through execution tracking and monitoring

The project is designed to support large-scale scientific computing workloads and targets orchestration of **20,000+ concurrent jobs**. 

---

# Core Functionality

## 1. Workflow Execution

The primary execution command is:

```bash
sprocket run
```

Sprocket executes complete WDL workflows while managing:

- Task dependencies
- Workflow inputs and outputs
- Conditional execution
- Scatter/gather parallelization
- Backend scheduling

Supported execution environments include:

- Docker
- LSF + Apptainer/Singularity
- SLURM
- Other configurable backends

This allows the same workflow definition to run across different infrastructures with minimal changes. 

---

## 2. WDL Development Toolchain

Sprocket provides a complete set of tools for developing and validating WDL workflows.

| Command | Purpose |
|----------|---------|
| `sprocket check` | Static analysis and validation |
| `sprocket lint` | Workflow linting |
| `sprocket format` | Auto-format WDL files |
| `sprocket validate` | Validate workflow inputs |
| `sprocket inputs` | Generate JSON/YAML input templates |
| `sprocket analyzer` | Language Server Protocol (LSP) support |
| `sprocket explain` | Explain validation and linting rules |

These tools help developers identify workflow issues before jobs are submitted to an HPC cluster. 

---

## 3. Testing and Documentation

Sprocket also supports workflow testing and documentation.

### Testing

```bash
sprocket dev test
```

Runs unit and integration tests for WDL workflows. 

### Documentation

```bash
sprocket dev doc
```

Generates workflow documentation automatically. 

### Workflow Management API

```bash
sprocket dev server
```

Provides an HTTP server that supports:

- Workflow submission
- Run monitoring
- Status tracking
- Retry operations
- Task log access



---

## 4. Configuration Management

Workflow execution behavior is controlled through a configuration file:

```text
sprocket.toml
```

Common configuration options include:

- Execution backend
- Queue selection
- Resource limits
- Container configuration
- Scatter concurrency settings
- Job naming conventions

Example:

```toml
[run.backends.default]
type = "lsf_apptainer"
max_scatter_concurrency = 200
job_name_prefix = "snap"
```



---

# Architecture

At a high level, the repository contains both a command-line application and reusable workflow libraries.

```text
sprocket/
├── src/                  # CLI implementation
├── crates/wdl-*          # WDL parser and execution libraries
├── python/sprocket_bio   # Python bindings
├── tests/                # Integration and system tests
└── test-configs/         # Example backend configurations
```



---

## Major Components

### WDL Libraries (`wdl-*`)

Provide the underlying workflow infrastructure:

- WDL parser
- Abstract Syntax Tree (AST)
- Static analysis
- Workflow engine
- Formatter
- Linter
- Language Server (LSP)

### Python Bindings (`sprocket_bio`)

Allow workflows to be controlled programmatically from Python. 

---

# Why It Matters for Bioinformatics

For workflows such as:

- scRNA-seq
- scATAC-seq
- Multiome
- Spatial genomics

Sprocket acts as a workflow orchestration layer on top of existing analysis tools and scripts.

Instead of manually managing execution with scheduler chains such as:

```bash
bsub job1
bsub job2 -w "done(job1)"
bsub job3 -w "done(job2)"
```

workflow dependencies can be declared in WDL and executed automatically by Sprocket. 

Benefits include:

- Improved reproducibility
- Simplified dependency management
- Easier testing and validation
- Standardized workflow definitions
- Native HPC execution
- Better monitoring and recovery
- Easier reruns of failed workflow stages

---

# Example Use Case: sc-rna-seq-snap

For a pipeline such as **sc-rna-seq-snap**, Sprocket could orchestrate workflow modules like:

```text
fastqc
└── cellranger
    └── upstream
        └── integrative
            └── cluster
                └── cell_types
                    └── de_go
```

while preserving:

- Existing R scripts
- Existing module structure
- Existing containers
- Existing outputs

In this model, Sprocket becomes the execution and scheduling layer while the scientific analysis code remains unchanged. 

---

# Summary

Sprocket is a **WDL-native workflow platform** that provides:

- Workflow orchestration
- HPC scheduling
- WDL development tools
- Workflow testing
- Configuration management
- Monitoring and recovery capabilities

Its primary value is enabling scalable, reproducible, and maintainable bioinformatics workflows while integrating seamlessly with HPC environments such as **LSF + Apptainer**. 
