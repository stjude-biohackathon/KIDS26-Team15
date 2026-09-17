# Why WDL and Sprocket?

## Notes on WDL vs. Nextflow

St. Jude and Fred Hutch use WDL and Sprocket for bioinformatics workflows. The following notes summarize why the combination can be a practical choice for teams building or modernizing workflows.

## WDL Compared with Nextflow

People often describe Nextflow as complex. If a team already has a Nextflow pipeline, it may make sense to continue using it. However, for teams working primarily with Bash or other scripts today, WDL can be faster to learn and set up.

WDL is intended to be more user-friendly while still supporting the workflow features needed for bioinformatics. It is open source and supported by a community of users and contributors.

A related concern is governance and long-term trust. Nextflow is owned by a company, while WDL is developed as a community-driven open standard. The community model can reduce concerns about unexpected changes to user agreements or licensing terms.

A useful summary from the discussion was:

> WDL can do 95% of what Nextflow does with 15% of the complexity.

The exact percentages are a rule-of-thumb rather than a benchmark, but the underlying point is that WDL aims to provide the capabilities most bioinformatics teams need without requiring the full complexity of a larger workflow ecosystem.

## An Open Standard for Bioinformatics

WDL and CWL were identified as the two community-driven open standards for bioinformatics workflows.

WDL also benefits from close involvement by people who understand both workflow language design and bioinformatics practice. The main language designer is in-house at Fred Hutch, and Clay helps support and develop the language. Having that expertise available within the organization makes it easier to get practical guidance when building workflows.

## Why WDL?

The discussion highlighted four main advantages:

1. **Ease of use:** WDL is designed to be readable and writable by humans, making workflows easier to understand and maintain.
2. **Community development:** WDL is an open, community-developed standard rather than a format controlled solely by one vendor.
3. **Strong typing:** WDL is a strongly typed language customized for bioinformatics. Types help catch mismatched inputs and other errors before execution.
4. **In-house support:** Having experienced WDL developers and users available within the organization is especially valuable when teams are learning the language or troubleshooting workflows.

Overall, WDL strikes a practical balance between complexity and language features for the bioinformatics community.

## Workflow Graphs

WDL workflows are represented as directed acyclic graphs (DAGs). Each task is a node, and the dependencies between tasks form the edges of the analysis graph.

By defining a workflow, a team makes the structure of the analysis explicit. The graph can be inspected before anything runs, which helps users understand dependencies, identify opportunities for parallel execution, and catch structural problems early.

Sprocket provides an execution environment for running WDL workflows, while WDL provides the language used to define the workflow and its dependencies.
