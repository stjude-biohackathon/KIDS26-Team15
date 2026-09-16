# Shareable Copy Notes

This repository is a sanitized copy of `sc-rna-seq-snap-legacy-Victoria-Knockout` prepared for external sharing (e.g., KIDS26 hackathon participants).

## What was changed

- Internal filesystem paths replaced with `/sc-rna-seq-snap-legacy-Victoria-Knockout-shareable` placeholders
- User-specific directory names removed from logs and configs
- Internal cluster hostnames, node names, and system mail addresses generalized (`compute-node`, `lsfadmin@example.org`)
- Usernames (cluster login IDs) replaced with `USER`
- LSF job completion notification PDFs and email artifacts removed
- LaTeX build logs (`Report-*.log`) with embedded internal paths removed
- Internal wiki links (`wiki.stjude.org`) replaced with public Snap wiki URLs
- Staff email addresses in reports replaced with `user@example.org`
- Singularity bind mounts for `/research` and `/hpcf` removed; use `SINGULARITY_BIND_EXTRA` for site-specific mounts
- Cell Ranger LSF metadata (`_jobinfo`, `_stdout`, etc.) sanitized for cluster infrastructure details
- See `SECURITY-AUDIT-REPORT.md` for the full audit trail

## What is preserved

- Original `project_metadata.tsv` (sample IDs, experiment metadata, conditions)
- Full pipeline structure, scripts, configs, and analysis outputs
- Legacy LSF `launch_full_pipeline.sh` orchestration workflow
- Cell Ranger and downstream analysis results

## Before running

1. Clone or copy this repo to your preferred location
2. Update `project_parameters.Config.yaml` with your local paths
3. Replace FASTQ paths in `data/project_metadata/project_metadata.tsv` if running from raw data
4. Set `NOTIFY_EMAIL` in `launch_full_pipeline.sh` if using LSF email notifications
