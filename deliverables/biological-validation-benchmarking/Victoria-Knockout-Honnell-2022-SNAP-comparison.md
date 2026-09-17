# Victoria Knockout (legacy) SNAP Analysis vs Honnell et al. 2022

**Created:** 2026-09-18  
**Purpose:** Review notes linking the Honnell et al. 2022 paper to upstream and integrative SNAP results in the Victoria Knockout cohort.  
**Paper:** [Honnell et al. 2022, *Nature Communications*](https://doi.org/10.1038/s41467-021-27924-y) — *Identification of a modular super-enhancer in murine retinal development*  
**Paper PDF:** `KIDS26-Team15/docs/papers/Honnell_etal_2022_NatureCommunications.pdf`  
**SNAP project:** `sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/`

---

## Executive summary

The Honnell et al. 2022 paper and the Victoria Knockout SNAP project study the **same biological system** (Vsx2 super-enhancer knockouts in mouse retina, Dyer lab), but at **different analysis stages**. The paper reports annotated scRNA-seq biology; the SNAP run has completed **upstream QC** and **Harmony integrative analysis** only. Downstream modules needed to reproduce the paper's cell-type conclusions (clustering, retinal annotation, DE) have **not yet been run**.


---

## What the paper is about

Honnell et al. 2022 maps a **modular Vsx2 super-enhancer (CRC-SE)** upstream of the *Vsx2* gene in the developing and adult mouse retina. *Vsx2* is expressed in retinal progenitor cells (RPCs), bipolar neurons, and Müller glia.


### Key scRNA-seq findings from the paper

In the Honnell (2022) paper, the only information provided is scRNA-seq results with cell type annotations (Muller glia, RPC, Bipolar neurons, amacrine, etc.). Our analysis is not annotated with cell types. I also thoroughly reviewed the supplementary information section of the paper. You can check the supplementary info - dataset 5 (for scRNA-seq only). There are cell numbers per cell type and total cells for WT, OrJ, and Vsx2-SE KO. https://www.nature.com/articles/s41467-021-27924-y

There is no information regarding QC reports, DoubletFinder, UMAP creation, or other analysis information in the paper. Only consistency I could find is in the methods section. The top 3,000 variable features were selected which is consistent with our project parameter input. Although it's not that significant.


| Finding | Observation |
|--------|-------------|
| **Full SE deletion (Vsx2-SEΔ/Δ)** | Complete loss of bipolar neurons; those cells appear to switch fate toward **rods and Müller glia** |
| **RPC proliferation** | Normal in the full SE deletion (unlike classic *Vsx2* knockouts) |
| **Modular architecture** | **R0-37 / R1-28** → RPC proliferation and retinal size; **R3-17** → bipolar neuron specification |
| **Adult retina (Fig. 6E–F)** | UMAPs across WT, R1-28, CRC-SE, R3-17, R0-37, and *orJ* strains, with stacked bar plots of cell-type proportions — bipolar cells absent in CRC-SE and R3-17 |

### Paper authorship and code

- First author: **Victoria Honnell** (project name "Victoria Knockout" refers to this work)
- PI: **Michael A. Dyer**
- scRNA-seq processing code: [CodyRamirez/StJude_Scripts — Vsx2_SE](https://github.com/CodyRamirez/StJude_Scripts/tree/main/Vsx2_SE) ([Zenodo](https://doi.org/10.5281/zenodo.5777750))
- Sequencing data: GEO **GSE169262** (reference genome mm10 in paper)

---

## Victoria Knockout (legacy) SNAP cohort

**Metadata:** `sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/data/project_metadata/project_metadata.tsv`

| Sample | Condition | Tissue | Technology |
|--------|-----------|--------|------------|
| DYE_2519 | wt | Mouse retina | 10X v3 |
| DYE_2520 | wt | Mouse retina | 10X v3 |
| DYE_2521 | knock-out | Mouse retina | 10X v3 |
| DYE_2522 | knock-out | Mouse retina | 10X v3 |

- **Genome:** GRCm39 (Cell Ranger 2024-A) — paper used mm10 (minor reference difference)
- **PI / experiment:** Dyer lab; experiment label "Victoria Knockout"
- **Open question:** Metadata does not specify which Vsx2-SE deletion module the knock-out samples represent (e.g., full CRC-SE vs R3-17). Confirm from original sample records.

---

## Upstream analysis — what was done

**Location:** `analyses/upstream-analysis/`  
**Reports:** `plots/04_Filter_object/Report-Filter-object-2026-09-12.{html,pdf}`

### Pipeline steps completed

1. CellRanger alignment (from `cellranger-analysis` module)
2. Per-sample Seurat QC (min 300 genes, 500 UMIs, 10% mtDNA)
3. scDblFinder doublet detection
4. Merge of all 4 libraries

### Post-QC cell counts

| Sample | Condition | Cells (final) |
|--------|-----------|---------------|
| DYE_2519 | wt | 3,464 |
| DYE_2520 | wt | 5,432 |
| DYE_2521 | knock-out | 5,278 |
| DYE_2522 | knock-out | 7,049 |
| **Total** | | **~21,223** |

Team 15 runbook estimate: ~27k cells pre-QC → ~21k post-QC (consistent).

### Key outputs

- `results/04_Filter_object/seurat_obj_merged_filtered.rds`
- Per-sample QC UMAPs colored by `condition` (wt vs knock-out)

### Biological relevance at this stage

Upstream confirms data quality and shows per-sample structure. It does **not** yet label retinal cell types (rods, bipolar, Müller glia, etc.) — that is the paper's Fig. 6E level of interpretation.


---

## Integrative analysis — what was done

**Location:** `analyses/integrative-analysis/`  
**Reports:** `plots/Report-integrative-analysis-harmony-2026-09-12.{html,pdf}`

### Configuration (`project_parameters.Config.yaml`)

```yaml
use_harmony_integration: "YES"
integration_method: "harmony"
variable_value: "ID"          # integrate across sample IDs
condition_value1: "condition" # wt vs knock-out for visualization
```

### What was produced

- Harmony batch correction across 4 samples
- Harmonized UMAP embedding (cells group by biology, not library)
- Preliminary `seurat_clusters` at resolution 0.8
- Output: `results/seurat_obj_integrated_harmony.rds`

### Relation to paper

Analogous to the paper's side-by-side UMAPs in **Fig. 6E**, but with wt and knock-out overlaid in one embedding after batch correction.

---

## What has NOT been run yet

In `launch_full_pipeline.sh`, downstream steps are **disabled**:

```
RUN_CLUSTER=0
RUN_CELL_TYPES=0
RUN_DE_GO=0
```

| Paper result | SNAP module needed |
|-------------|-------------------|
| UMAP with retinal cell types labeled | `cell-types-annotation` (gene markers: `retinal_cell_type_top50_gene_markers-2-UPDATED.tsv`) |
| Bipolar cell loss in KO | Clustering + annotation → compare bipolar proportion wt vs KO |
| Fate switching to rods/Müller glia | Cell-type proportion bar plots (like Fig. 6F) |
| *Vsx2* expression in bipolar vs Müller glia | Feature plots / DE (`de-go-analysis`) |
| Differential expression by condition | `de-go-analysis` |

---

## Side-by-side comparison

| Layer | Paper | SNAP results (as of 2026-09-12) |
|-------|-------|----------------------------------|
| **Biological question** | How modular Vsx2 SE domains control RPC proliferation vs bipolar fate | Same retina KO system (wt vs knock-out) |
| **Data** | scRNA-seq, adult rod-depleted retina across SE deletion strains | scRNA-seq, 4 adult retina libraries (10X v3) |
| **Analysis stage** | Annotated UMAPs + cell-type proportions + genotype comparisons | QC + Harmony integration complete |
| **Key biology visible now?** | Yes — bipolar loss, fate switching | **Not yet** — needs clustering, retinal annotation, and DE |

---

## Analysis flow (conceptual)

```
Paper (Honnell et al. 2022)
  Vsx2 SE modular deletions
    → scRNA-seq (adult + E14.5)
    → cell-type annotation
    → bipolar loss in CRC-SE / R3-17
    → fate switch → rods / Müller glia

SNAP (current state)
  4 retina libraries (2 wt + 2 KO)
    → upstream: QC + merge (~21k cells)     ✓ DONE
    → integrative: Harmony integration       ✓ DONE
    → cluster + annotate + DE                ✗ NOT RUN
```

---

## Next steps to test paper predictions

1. **Confirm KO genotype** for DYE_2521 and DYE_2522 (which SE deletion strain).
2. **Run** `cluster-cell-calling` and `cell-types-annotation` (retinal gene markers already configured in `project_parameters.Config.yaml`).
3. **Compare** cell-type proportions wt vs knock-out (expect reduced bipolar if CRC-SE or R3-17 deletion).
4. **Run** `de-go-analysis` for condition-specific DE and pathway enrichment.
5. **Optional:** Compare UMAP/cluster structure to paper Fig. 6E (GEO GSE169262).

### Expected biology if KO is full SE or R3-17 deletion

- Reduced or absent bipolar cluster in KO samples
- Relative increase in rods and Müller glia
- Other photoreceptor/neuronal populations largely preserved
- *Vsx2* expression changes in bipolar but maintained in Müller glia

---

## References and paths

| Resource | Path or link |
|----------|--------------|
| Paper | `KIDS26-Team15/docs/papers/Honnell_etal_2022_NatureCommunications.pdf` |
| SNAP shareable repo | `sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/` |
| Project config | `sc-rna-seq-snap-legacy-Victoria-Knockout-shareable/project_parameters.Config.yaml` |
| Team 15 runbook | `KIDS26-Team15/project-management/hackathon-runbook.md` |
| Paper DOI | https://doi.org/10.1038/s41467-021-27924-y |
| Paper GEO | GSE169262 |

---

*Maintainer notes: Generated during KIDS26 Team 15 hackathon prep for biology sign-off (T6, T9) and paper-to-pipeline context.*
