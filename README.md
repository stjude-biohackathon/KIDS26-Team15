# KIDS26 Team 15 — Resource-Aware SNAP Orchestrator

**Question:** Can a resource-aware SNAP + Sprocket orchestrator replace manual LSF wiring for scalable single-cell analysis?

**Expected output:** Tested downstream launcher, documented HPC test results, code-review notes, 3-slide deck, 2-minute lightning talk, and live demo for judges.

**Team lead:** Antonia Chroni ([@AntoniaChroni](https://github.com/AntoniaChroni))  
**Slack:** [Team channel](https://stjudebiohackathon.slack.com/archives/C0BT8BF4JEL) (team15)

---

## Start here

| Doc | Purpose |
|-----|---------|
| [Hackathon runbook](project-management/hackathon-runbook.md) | Team, schedule, test spec (T1–T17), deliverables, checklists, demo prep |
| [Problem & solution overview](docs/problem-and-solution-overview.md) | Slide-ready problem/solution narrative |
| [Participant FAQ](docs/participant-faq-snap-sprocket-resources.md) | Onboarding: WDL vs bash, resource scaling, pair roles |
| [Test log](deliverables/validation/hackathon-test-log.md) | Live pass/fail log — fill in during the event |
| [HPC setup](docs/vm-hpc-setup.md) | St. Jude HPC access and modules |
| [Team roster (xlsx)](project-management/stjude-biohackathon-kids26-team15-info.xlsx) | Source of truth for pair assignments |

**Quick start:** `cd analyses/sc-rna-seq-snap-Victoria-Knockout` then `bash scripts/test-downstream-layout.sh`

---

## Repo layout

```text
KIDS26-Team15/
├── README.md                              This file
├── analyses/sc-rna-seq-snap-Victoria-Knockout/   Main work area (launcher, WDL, scripts)
├── docs/                                  Problem overview, onboarding FAQ, setup, learning resources
├── project-management/
│   ├── hackathon-runbook.md               Operational guide (read this before Day 1)
│   └── stjude-biohackathon-kids26-team15-info.xlsx
└── deliverables/
    ├── validation/hackathon-test-log.md   Shared test log
    ├── reports/                           Event report-outs
    └── slides/                            Kickoff deck + event deck (TBD; see README there)
```

**Tools:** SNAP (`sc-rna-seq-snap`), WDL, Sprocket, R/Seurat, Apptainer, LSF, YAML config · Victoria Knockout cohort (4 samples, ~27k cells)

**Schedule:** Day 1 (4 h) · Day 2 (8 h) · Day 3 (4 h afternoon) · Demo 3:00–6:00 PM

---

## Contributing

1. Branch → focused change → PR → teammate review → merge.
2. Do not commit secrets, credentials, or private data.
3. See [Git and GitHub basics](docs/git-github-basics.md) if needed.
