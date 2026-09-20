## Analyst time and cost ROI (parameterized)

St. Jude does not publish an official HPC dollar rate. Analyst hourly rate uses **$100,000/year** (below the $108,680 midpoint of the public **Senior Bioinformatics Analyst** range, $78K–$139K → **$48.08/h**); see `roi-analysis-Lindsey-questions.md`. Base salary ÷ 2,080 work hours/year; not a fully loaded labor rate.

Analyst hands-on time is **not measured** in LSF logs. `roi_scenarios.csv` provides low/expected/high scenarios with formulas:

- **Labor savings per run** = (legacy analyst hours − Daedalus analyst hours) × hourly rate  
- **HPC savings per run** = (CPU-hours saved × CPU rate) + (memory GB-hours saved × memory rate)  
- **ROI** = ((annual benefit − implementation) / implementation) × 100  

**Conclusion type:** Estimated using assumptions (see CSV).

---

## More 

## Qualitative benefits (Daedalus)

Supported by workflow structure; not quantified in LSF metrics:

- Standardized WDL/YAML configuration and reproducible run IDs
- Automatic dependency wiring (upstream → integrative)
- Resource-aware requests via Daedalus collector
- Reduced manual LSF script editing and path hardcoding
- Improved provenance (`out/runs/`, `daedalus.db`)

---

## Limitations

1. Single cohort (4 samples); scalability to larger projects not measured here.
2. Legacy and Daedalus runs used slightly different submission dates/times; biology and inputs matched.
3. Only upstream + integrative modules were compared; the total pipeline ROI is incomplete (out of scope for Biohackathon)
4. One Daedalus upstream dev failure excluded from production metrics.
5. HPC and analyst dollar rates are parameterized, not official St. Jude pricing.
6. Legacy integrative turnaround includes manual upstream dependency wait (~1.8 h on same-day pair).
7. Integrative wall-time difference may reflect cluster load, not workflow changes.

---

## Recommendations

1. Right-size legacy-style requests: upstream memory could drop from 480 GB reserved toward ~27–34 GB based on observed peaks.
2. Continue using Daedalus native resource collector after each production run.
3. Document analyst setup/monitoring time in future comparisons.
4. Re-run comparison on a larger cohort before claiming facility-wide savings.



---

**Maintainer:** KIDS26 Team 15 / DNB Bioinformatics Core
