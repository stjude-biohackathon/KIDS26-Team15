# Hackathon results

Artifacts from HPC testing and the event — logs, screenshots, ROI notes, and demo captures.

| File | Purpose |
|------|---------|
| [hackathon-test-results.md](./hackathon-test-results.md) | HPC test matrix (T1–T17) — **upstream** and **integrative** SNAP modules |

## Pair responsibilities

| Pair | Results role |
|------|----------------|
| **Lindsey/Sarthak** | Maintain test log; ROI tables (T15–T16); troubleshooting entries (T17) |
| **Rachana/A.S.M. Tanjim** | T1 (layout); T6 + T9 biology sign-off; T10–T11 (resource scaling, YAML overlay) |
| **Rojina/Antonia** | T2–T3, T7 (dry-run + WDL toggles); T4, T5, T8 (HPC submits + monitoring); T12–T14 (WDL chain, parallel workers, email) |

## Module run evidence

Log job IDs and outputs in **hackathon-test-results.md** for three runs:

1. **Upstream only** (`run_upstream: true`)
2. **Integrative only** (`run_integrative: true`)
3. **Upstream + integrative** (`run_upstream` + `run_integrative`)

## During the event

- Log pass/fail in **hackathon-test-results.md** (HPC only)
- Record LSF job IDs for upstream (T4) and upstream + integrative (T8) submits
- Add screenshots or links under each test row
- Tanjim signs off biology QC in the Module run evidence section (T6 upstream, T9 integrative)

## After the event

Add follow-up artifacts here as needed, for example:

- `roi-summary.md` — slide-ready legacy vs new comparison
- `demo-notes.md` — what worked in the live demo
- `screenshots/` — evidence images (if not hosted elsewhere)
