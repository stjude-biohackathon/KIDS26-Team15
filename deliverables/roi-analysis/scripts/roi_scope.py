"""ROI phase definitions for Victoria Knockout legacy vs Daedalus comparisons."""

from __future__ import annotations

# Biohackathon: head-to-head on two downstream modules only.
BIOHACKATHON_PAIRED_MODULES: tuple[str, ...] = ("upstream", "integrative")

# Post-hackathon: five downstream modules compared legacy vs Daedalus.
POSTHACKATHON_PAIRED_MODULES: tuple[str, ...] = (
    "upstream",
    "integrative",
    "cluster",
    "cell_types",
    "rshiny",
)

# QC / alignments run for both workflow types (legacy LSF in export; Daedalus consumes same project outputs).
POSTHACKATHON_QC_ALIGN_MODULES: tuple[str, ...] = ("fastqc", "cellranger")

# Extra Daedalus downstream (post-hackathon); biological validation has no legacy counterpart.
POSTHACKATHON_DAEDALUS_ONLY_MODULES: tuple[str, ...] = (
    "de_go",
    "project_updates",
    "biological_validation",
)
