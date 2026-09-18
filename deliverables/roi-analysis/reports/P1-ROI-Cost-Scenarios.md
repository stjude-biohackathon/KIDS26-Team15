# P1 · ROI Analysis: Cost Scenarios (Low / Expected / High)

**Date:** 2026-09-16  
**Source:** `docs/roi_scenarios.csv` + `docs/data-analyst-time.md`  
**Assumptions:** St. Jude HPC pricing + Senior Bioinformatics Analyst salary

---

## 1. Cost Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Analyst hourly rate | **$48.08/hr** | $100K/year ÷ 2,080 hrs (below midpoint of $78K-$139K range) |
| HPC CPU rate | $0.02-0.05/hr | St. Jude estimate (not official) |
| HPC memory rate | $0.001-0.002/GB-hr | St. Jude estimate (not official) |
| Implementation hours | 40-80 hrs | Team estimate |
| Maintenance hours | 8-20 hrs/year | Team estimate |

---

## 2. Scenario Analysis

### 2.1 Low Scenario

| Metric | Legacy | Daedalus | Delta |
|--------|--------|----------|-------|
| Analyst hours/run | 4 | 1 | -3 hrs |
| HPC runs/year | 12 | 12 | - |
| Analyst savings/run | - | - | **$144.24** |
| HPC savings/run | - | - | **$1.43** |
| **Total savings/run** | - | - | **$145.67** |

| Item | Value |
|------|-------|
| Annual savings | $1,748 |
| Implementation cost (40 hrs × $48.08) | $1,923 |
| Annual maintenance (8 hrs × $48.08) | $385 |
| **Net annual benefit** | **-$360** |
| **ROI** | **-32.6%** |
| Payback (runs) | 13.7 |

---

### 2.2 Expected Scenario

| Metric | Legacy | Daedalus | Delta |
|--------|--------|----------|-------|
| Analyst hours/run | 6 | 1.5 | -4.5 hrs |
| HPC runs/year | 24 | 24 | - |
| Analyst savings/run | - | - | **$216.36** |
| HPC savings/run | - | - | **$2.14** |
| **Total savings/run** | - | - | **$218.50** |

| Item | Value |
|------|-------|
| Annual savings | $5,244 |
| Implementation cost (60 hrs × $48.08) | $2,885 |
| Annual maintenance (12 hrs × $48.08) | $577 |
| **Net annual benefit** | **$1,782** |
| **ROI** | **48.1%** |
| Payback (runs) | 14.3 |

---

### 2.3 High Scenario

| Metric | Legacy | Daedalus | Delta |
|--------|--------|----------|-------|
| Analyst hours/run | 8 | 2 | -6 hrs |
| HPC runs/year | 48 | 48 | - |
| Analyst savings/run | - | - | **$288.48** |
| HPC savings/run | - | - | **$3.04** |
| **Total savings/run** | - | - | **$291.52** |

| Item | Value |
|------|-------|
| Annual savings | $13,993 |
| Implementation cost (80 hrs × $48.08) | $3,846 |
| Annual maintenance (20 hrs × $48.08) | $962 |
| **Net annual benefit** | **$9,185** |
| **ROI** | **136.1%** |
| Payback (runs) | 18.4 |

---

## 3. Summary Table

| Scenario | Runs/Year | Annual Savings | Net Benefit | ROI | Payback (runs) |
|----------|-----------|----------------|-------------|-----|----------------|
| Low | 12 | $1,748 | -$360 | -32.6% | 13.7 |
| Expected | 24 | $5,244 | $1,782 | 48.1% | 14.3 |
| High | 48 | $13,993 | $9,185 | 136.1% | 18.4 |

---

## 4. Key Insights

### 4.1 Analyst Time Dominates Savings

| Scenario | Analyst Savings | HPC Savings | % of Total |
|----------|----------------|-------------|------------|
| Low | $1,492 (99%) | $17 (1%) | Analyst 99% |
| Expected | $2,164 (99%) | $26 (1%) | Analyst 99% |
| High | $2,885 (99%) | $30 (1%) | Analyst 99% |

**HPC compute savings are negligible at St. Jude pricing ($0.02-0.05/core-hr).**

### 4.2 What Drives ROI

| Factor | Impact |
|--------|--------|
| Analyst hours saved per run | **Dominant** — 3-6 hrs × $48/hr = $144-288/run |
| Runs per year | Linear scaling — more runs = more savings |
| Implementation cost | One-time hit — 40-80 hrs |
| HPC rates | Minimal impact at St. Jude pricing |

### 4.3 Break-even Analysis

| Scenario | Break-even (runs) | Break-even (months at 2 runs/mo) |
|----------|-------------------|----------------------------------|
| Low | 13.7 | 6.9 months |
| Expected | 14.3 | 7.2 months |
| High | 18.4 | 9.2 months |

---

## 5. Comparison with Legacy Compute-Only Analysis

### 5.1 Previous Analysis (Compute Only)

| Item | Value |
|------|-------|
| Legacy compute cost | $0.75/run |
| Daedalus compute cost | $0.42/run |
| Compute savings | $0.33/run (44%) |

### 5.2 Full Analysis (Compute + Analyst)

| Item | Value |
|------|-------|
| Legacy total cost | $240-384/run (analyst + compute) |
| Daedalus total cost | $48-96/run (analyst + compute) |
| **Total savings** | **$192-288/run (80-87%)** |

**Analyst time is 600-900x more expensive than HPC compute at St. Jude pricing.**

---

## 6. Recommendations

1. **Focus on analyst time reduction** — HPC savings are trivial at St. Jude pricing
2. **Target 24+ runs/year** for positive ROI (expected scenario)
3. **Document actual analyst time** in future runs for more accurate estimates
4. **Consider fully-loaded labor rate** (benefits, overhead) for more conservative estimates
5. **Re-run comparison on larger cohort** before claiming facility-wide savings

---

*Based on parameterized assumptions from `roi_scenarios.csv`. Not official St. Jude pricing.*
