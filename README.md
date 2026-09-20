# KIDS26 Team 15 — Resource-Aware SNAP Orchestrator

**Question:** Can a resource-aware SNAP + Sprocket orchestrator replace manual LSF wiring for scalable single-cell analysis?

**Expected output:** Tested downstream launcher (for two Snap modules), documented HPC test results, code-review notes, 3-slide deck, 2-minute lightning talk, and live demo for judges.

**Team lead:** Antonia Chroni ([@AntoniaChroni](https://github.com/AntoniaChroni))  
**Code review & development leads:** Clay McLeod, Emma Bishop, Antonia Chroni  
**Dry-run & HPC testers:** Clay McLeod, Antonia Chroni, Rojina Sapkota (only St Jude HPC users)  
**Biology assessment leads:** Rachana Pandey, A.S.M. Tanjim Hassan
**WDL and ROI analysis leads:** Lindsey Warren, Sarthak Sunil Dhanke

**Slack:** [Team channel](https://stjudebiohackathon.slack.com/archives/C0BT8BF4JEL) (team15)

---

## Start here

| Doc | Purpose |
|-----|---------|
| [Hackathon runbook](project-management/hackathon-runbook.md) | Team, schedule, test spec (T1–T17), deliverables, checklists, demo prep |
| [Problem & solution overview](deliverables/docs/problem-and-solution-overview.md) | Slide-ready problem/solution narrative |
| [Daedalus pitch](deliverables/docs/daedalus-pitch.md) | Tool name, 30/60s pitches, naming rationale |
| [Participant FAQ](deliverables/docs/participant-faq-snap-sprocket-resources.md) | Onboarding: WDL vs bash, resource scaling, pair roles |
| [Test log](deliverables/validation/hackathon-test-log.md) | Live pass/fail log — fill in during the event |
| [HPC setup](docs/vm-hpc-setup.md) | St. Jude HPC access and modules |
| [Team roster (xlsx)](project-management/stjude-biohackathon-kids26-team15-info.xlsx) | Source of truth for pair assignments |

**Quick start:** `cd analyses/sc-rna-seq-snap-Victoria-Knockout` then `bash scripts/test-downstream-layout.sh`

---

## Repo layout

```text
KIDS26-Team15/
├── analyses/
│   ├── sc-rna-seq-snap-legacy-Victoria-Knockout-shareable    Results from Legacy Run
│   └── sc-rna-seq-snap-sprocket-Victoria-Knockout-shareable  Results from Daedalus Run
├── data/                                  project_metadata
└── deliverables/
│   ├── biological-validation-benchmarking/ Biological comparisons and assessments
│   ├── docs/                              Pitches, problem overview, participant FAQ
│   ├── reports/                           Event report-outs
│   ├── roi-analysis/                      ROI analysis
│   ├── reports/                           Event report-outs
│   ├── slides/                            Kickoff deck + event deck (TBD; see README there)
│   └── wdl-stakeholder-evaluation/        Assessment of WDL vs various workflow languages
├── docs/                                  HPC setup, troubleshooting, learning resources
├── LICENSE.md
├── project-management/
│   ├── hackathon-runbook.md               Operational guide (read this before Day 1)
│   └── stjude-biohackathon-kids26-team15-info.xlsx
└── README.md                              This file
```

**Tools:** SNAP (`sc-rna-seq-snap`), WDL, Sprocket, R/Seurat, Apptainer, LSF, YAML config · Victoria Knockout cohort (4 samples, ~27k cells)

**Schedule:** Day 1 (4 h) · Day 2 (8 h) · Day 3 (4 h afternoon) · Demo 3:00–6:00 PM

---

## Contributing

1. Branch → focused change → PR → teammate review → merge.
2. Do not commit secrets, credentials, or private data.
3. See [Git and GitHub basics](docs/git-github-basics.md) if needed.


---

**Maintainer:** KIDS26 Team 15 · Generated during KIDS26 Team 15 Biohackathon 26 (September 16-18, 2026)

