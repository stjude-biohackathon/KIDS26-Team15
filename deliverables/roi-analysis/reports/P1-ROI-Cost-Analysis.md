# P1 · ROI Analysis: Cost Calculation

**Source:** `deliverables/roi-analysis/roi-analysis-Lindsey-questions.md` + run data

---

## 1. Cost Assumptions

### HPC Infrastructure Cost (St. Jude)

| Item | Value | Source |
|------|-------|--------|
| Per-core cost | **$0.024/hour** | Michael Brewer, Director - HPC at St. Jude |
| Memory included | 32 GB per core | Bundled with core cost |
| GPU cost | $2.50/hour (8 cores + 32GB) | Not used in this workflow |


### Personnel Cost (St. Jude)

| Item | Value | Source |
|------|-------|--------|
| Salary range | $78,000 – $139,360/year | St. Jude job posting (Senior Bioinformatics Analyst) |
| Assumed salary | **$100,000/year** | Below midpoint; typical hire |
| Work hours | 2,080 hours/year | 40h × 52 weeks |
| **Hourly rate** | **$48.08/hour** | $100,000 ÷ 2,080 |

---

## 2. SNAP Legacy — Compute Cost

### Upstream Analysis

| Metric | Value |
|--------|-------|
| Cores allocated | 16 |
| Wall-clock | 6,445s (1.79 hours) |
| Core-hours | 16 × 1.79 = **28.6 core-hours** |
| Cost | 28.6 × $0.024 = **$0.69** |


### Integrative Analysis

| Metric | Value |
|--------|-------|
| Cores allocated | 10 |
| Wall-clock | 954s (0.265 hours) |
| Core-hours | 10 × 0.265 = **2.65 core-hours** |
| Cost | 2.65 × $0.024 = **$0.06** |


### Total Compute Cost

| Run | Core-hours | Cost |
|-----|-----------|------|
| Upstream | 28.6 | $0.69 |
| Integrative | 2.65 | $0.06 |
| **Total** | **31.25** | **$0.75** |

**Note:** Memory is bundled with core cost (32GB per core). No additional memory charge.

---

## 3. SNAP Legacy — Waste Analysis

### Memory Waste

| Run | Total Requested | Avg Used | Waste | Waste % |
|-----|-----------------|----------|-------|---------|
| Upstream | 480 GB | 47 GB | 433 GB | **90%** |
| Integrative | 960 GB | 14 GB | 946 GB | **98.5%** |


### CPU Waste

| Run | Allocated Core-time | Actual CPU Time | Waste | Waste % |
|-----|---------------------|-----------------|-------|---------|
| Upstream | 103,120s | 7,304s | 95,816s | **92.9%** |
| Integrative | 9,540s | 642s | 8,898s | **93.3%** |


### Cost of Waste

| Run | Actual Cost | Cost if Right-sized | Waste Cost |
|-----|-------------|---------------------|------------|
| Upstream | $0.69 | ~$0.05 (at 10% utilization) | **$0.64** |
| Integrative | $0.06 | ~$0.004 (at 6.7% utilization) | **$0.056** |
| **Total** | **$0.75** | **~$0.054** | **~$0.70** |

**93% of compute spend is wasted on over-provisioning.**

---

## 4. Analyst Time Estimate (Legacy Workflow)

### Manual Steps Required (Legacy `launch_full_pipeline.sh`)

| Step | Estimated Time | Description |
|------|----------------|-------------|
| Edit bash flags | 5 min | Toggle RUN_* flags in launcher |
| Set resources | 10 min | Manually choose CPU/memory per module |
| Chain dependencies | 5 min | Wire `done(JOBID)` expressions |
| Debug/fix errors | 15 min | OOM kills, wrong resources, queue issues |
| **Total per run** | **35 min** | |


### Additional Time When Things Change

| Scenario | Estimated Time | Description |
|----------|----------------|-------------|
| Sample count changes | 20 min | Reconfigure resources, re-chain jobs |
| Cell Ranger outputs change | 15 min | Re-tune memory for downstream |
| Queue wait time | 30 min | Monitor job status, troubleshoot failures |
| **Total per re-run** | **65 min** | |


### Analyst Cost Per Run

| Scenario | Time | Cost (@ $48.08/h) |
|----------|------|-------------------|
| Initial run | 35 min | **$28.05** |
| Re-run (changes) | 65 min | **$52.09** |

---

## 5. Daedalus — Projected Cost

### Expected Improvements

| Dimension | Legacy | Daedalus | Savings |
|-----------|--------|----------|---------|
| Compute utilization | 7-10% | ~80% (auto-scaled) | **87% reduction** |
| Memory utilization | 1.5-10% | ~80% (auto-scaled) | **87% reduction** |
| Analyst time per run | 35 min | 5 min (YAML edit) | **86% reduction** |
| Re-run time | 65 min | 5 min | **92% reduction** |
| Pre-submit validation | None | Sprocket check | Prevents failed runs |

### Projected Compute Cost (Daedalus)

| Run | Current Cost | Projected Cost | Savings |
|-----|--------------|----------------|---------|
| Upstream | $0.69 | ~$0.09 (87% less) | $0.60 |
| Integrative | $0.06 | ~$0.008 | $0.052 |
| **Total** | **$0.75** | **~$0.10** | **$0.65** |

### Projected Analyst Cost (Daedalus)

| Scenario | Legacy Cost | Daedalus Cost | Savings |
|----------|-------------|---------------|---------|
| Initial run | $28.05 | $4.01 (5 min) | **$24.04** |
| Re-run | $52.09 | $4.01 | **$48.08** |

---

## 6. ROI Summary (Per Run)

| Category | Legacy Cost | Daedalus Cost | Savings |
|----------|-------------|---------------|---------|
| Compute | $0.75 | $0.10 | $0.65 |
| Analyst (initial) | $28.05 | $4.01 | $24.04 |
| **Total** | **$28.80** | **$4.11** | **$24.69** |

**ROI per run: 86% cost reduction**

---

## 7. Annualized Impact (Stretch Goal)

### Assumptions

| Assumption | Value |
|------------|-------|
| Projects per year | 10 |
| Runs per project | 3 (initial + 2 re-runs) |
| Total runs per year | 30 |

### Annual Savings

| Category | Per Run | Annual (30 runs) |
|----------|---------|------------------|
| Compute | $0.65 | $19.50 |
| Analyst time | $24.04 | $721.20 |
| **Total** | **$24.69** | **$740.70** |

### Scaled Across Teams

| Scale | Teams | Annual Savings |
|-------|-------|----------------|
| Single team | 1 | $741 |
| Department | 5 | $3,705 |
| Institution | 20 | $14,814 |

**Note:** Analyst time dominates savings (97% of total). Compute savings are minimal at St. Jude's pricing, but would be significant at commercial cloud rates ($0.50-2.00/core-hour).

---

## 8. Key Takeaways

1. **Compute is cheap at St. Jude** — $0.75 total for both runs. The real cost is analyst time ($28/run).
2. **Over-provisioning is 93%** — both CPU and memory are massively over-allocated.
3. **Daedalus saves analyst time** — YAML toggles + auto-scaling + one-command launch = 86% time reduction.
4. **Validation prevents failed runs** — Sprocket check before submit avoids wasted compute and analyst debugging time.
5. **Scales linearly** — More projects/runs = proportional savings in analyst time.

---

