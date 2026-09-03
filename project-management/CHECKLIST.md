# Team Lead Checklist

Use this page to get the team moving. It is intentionally short: a three-day project needs enough structure to coordinate work, not a second project to maintain.

## Start Here

1. **Access your assigned team repository.** Organizers will provide the repository and add team members. Confirm that you can open it on GitHub and clone it to your computer. Follow [Git and GitHub basics](../docs/git-github-basics.md) for the full path.
2. **Complete the project profile.** Agree on the question, inputs, expected output, tools, and team roles before pursuing a large implementation.
3. **Make a small first change.** Create a branch, update this README or document a data source, commit the change, and open a pull request. Use the terminal steps in [Git and GitHub basics](../docs/git-github-basics.md) or [GitHub Desktop](https://desktop.github.com/) if you prefer a graphical interface.
4. **Ask for help early.** Record blockers in an issue, raise them at a check-in, or ask a mentor. See [troubleshooting](../docs/troubleshooting.md) for common recovery steps.

## The Team

- **Members and roles:** [team.md](team.md)
- **Hackathon runbook:** [hackathon-runbook.md](hackathon-runbook.md)
- **Test log:** [hackathon-test-results.md](../results/hackathon-test-results.md)
- **Current plan:** [project-plan.md](project-plan.md)

## Project Structure

Current layout for KIDS26 Team 15. The main work area is `analyses/sc-rna-seq-snap-Victoria-Knockout/`.

```text
KIDS26-Team15/
├── README.md                    Team profile and getting started
├── LICENSE.md                   Repository license
│
├── analyses/                    SNAP analysis projects
│   ├── sc-rna-seq-snap-Victoria-Knockout/   Active hackathon analysis (start here)
│   │   ├── launch-snap-downstream.sh        One-command downstream launcher
│   │   ├── launch_full_pipeline.sh          Legacy launcher (for ROI comparison)
│   │   ├── project_parameters.Config.yaml   Master workflow config (edit by hand)
│   │   ├── scripts/                         Launcher, estimator, WDL generator, tests
│   │   ├── wdl/                             Workflow definitions (snap.wdl, tasks.wdl, …)
│   │   ├── inputs/                          Sprocket JSON/YAML inputs (generated + test)
│   │   ├── data/                            Project metadata and staged inputs
│   │   ├── docs/                            ROI one-pager, run metrics, pipeline notes
│   │   ├── figures/                         QC plots and demo screenshots
│   │   └── out/                             Sprocket run outputs (not committed)
│
├── docs/                        Team learning guides and setup
│   ├── vm-hpc-setup.md          Shared VM + St. Jude HPC setup
│   ├── vm-local-only-setup.md   Local/Docker setup (no HPC)
│   ├── troubleshooting.md       Common errors and fixes
│   ├── git-github-basics.md     Git and GitHub workflow
│   ├── resources-snap.md          SNAP learning resources
│   ├── resources-sprocket.md    Sprocket learning resources
│   └── …                        WDL primer, trainings, AI guidance
│
├── project-management/          Team plan, roles, and event coordination
│   ├── CHECKLIST.md             This file — team lead checklist
│   ├── hackathon-runbook.md     Pairs, test matrix, 3-day timeline, demo prep
│   ├── project-plan.md          Goals, milestones, definition of done
│   ├── team.md                  Roster, pair assignments, deliverables
│   ├── meetings.txt             Sync notes and judge feedback
│   └── stjude-biohackathon-kids26-team15-info.xlsx   Team roster source
│
└── results/                     Event artifacts and test logs
    └── hackathon-test-results.md   Shared pass/fail log (Track C maintains)
```

**Quick start:** `cd analyses/sc-rna-seq-snap-Victoria-Knockout` then run `bash scripts/test-downstream-layout.sh`.

## Data, meta data and secrets
**Do not commit passwords, API keys, private information, or identifiable human or clinical data. Check the source and license before sharing external data or media.**

## Resources

- **Hackathon runbook:** [hackathon-runbook.md](hackathon-runbook.md) — pairs, test matrix, timeline, commands
- **VM and HPC setup:** [vm-hpc-setup.md](../docs/vm-hpc-setup.md) — shared VM + St. Jude HPC
- **VM / local-only setup:** [vm-local-only-setup.md](../docs/vm-local-only-setup.md) — no HPC, Docker + `sprocket.local.toml`
- **Test results log:** [hackathon-test-results.md](../results/hackathon-test-results.md) — Track C maintains during the event
- New to Git or GitHub: [Git and GitHub basics](../docs/git-github-basics.md)
- St. Jude trainings (GitHub + reproducibility): [resources-trainings.md](../docs/resources-trainings.md)
- WDL + Sprocket primer: [learning-path-wdl-sprocket-containers.md](../docs/learning-path-wdl-sprocket-containers.md)
- SNAP overview: [resources-snap.md](../docs/resources-snap.md)
- Sprocket overview: [resources-sprocket.md](../docs/resources-sprocket.md)
- Using Copilot agents: [AI assistance](../docs/ai-guidance.md)
- Stuck during setup: [troubleshooting](../docs/troubleshooting.md)
- SNAP launcher details: [scripts/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md)

## Contributing to your team
### A Simple Workflow

1. Pick a small task or write down a blocker.
2. Create a branch with a clear name, such as `add-project-profile` or `fix-data-path`.
3. Make one focused change and commit it with a short message.
4. Push the branch and open a pull request.
5. Ask another teammate to look at the change before merging.
6. Update the README or project notes when the change affects how someone uses the project.

The [Git and GitHub basics](../docs/git-github-basics.md) guide explains each step, including a GitHub Desktop workflow.

### A Pull Request Is Ready When

- The change has a clear purpose.
- A teammate can understand what changed.
- You have recorded how you checked it, or explained why checking was not possible.
- Relevant assumptions, data sources, and limitations are documented.
- The change does not include credentials or sensitive data.

Small, incomplete pull requests are welcome when they make the current state visible and clearly describe what remains.


## Reproducibility and Attribution

Make work easier to inspect and reuse by keeping inputs, decisions, methods, and limitations visible. Prefer small readable steps over unexplained one-off commands. Cite data, code, models, and external resources that your project depends on. These practices help the next person understand what happened.

This repository is a reusable template. See [LICENSE.md](../LICENSE.md) for the licensing terms and update the project profile and attribution when you create a team project.

## Code of Conduct

In this repository, we use St. Jude's Code of Conduct document, outlining our expectations for all participants. Ask for help early, give feedback about the work rather than the person, and make room for different levels of experience.

For details, please visit: https://issuu.com/sjcrh/docs/st._jude_code_of_conduct.


## Team Leads: Before the Event

- [x] Complete the [project profile](../README.md#project-profile).
- [ ] Agree on one communication channel and a short check-in rhythm.
- [x] Create first tasks in [project-plan.md](project-plan.md) and roles in [team.md](team.md).
- [ ] Cell Ranger complete for Victoria Knockout cohort.
- [ ] `project_metadata.tsv` present and valid.
- [ ] Apptainer `.sif` image accessible on HPC.
- [ ] One upstream-only job pre-submitted as demo backup.
- [ ] All teammates added to GitHub repo and can clone.
- [ ] VM and HPC access confirmed for each pair.
- [ ] Share [hackathon-runbook.md](hackathon-runbook.md) with the team.


## During the Hackathon

Follow the [hackathon runbook](hackathon-runbook.md) for the detailed timeline. **Schedule: Day 1 (4 h) · Day 2 (8 h) · Day 3 (4 h afternoon) · Demo 3:00–6:00 PM.**

### Day 1 — Align and start (4 h)

- [ ] Kickoff: confirm pairs (A/B/C/D) and shared test log.
- [ ] Everyone clones repo and runs T1 (`test-downstream-layout.sh`).
- [ ] Everyone runs T2 dry-run (`launch-snap-downstream.sh`).
- [ ] HPC pairs confirm `module load sprocket R singularity`.
- [ ] **Track A** (Rojina + Antonia): code audit started; issues filed.
- [ ] **Track B** (Sarthak): T1–T4 logged with screenshots.
- [ ] **Track C** (Lindsey + Rachana): test log open; PR review checklist ready.
- [ ] **Track D** (Tanjim + Antonia): HPC submit plan confirmed.
- [ ] End-of-day sync: blockers raised; Day 2 priorities set.

### Day 2 — Build and learn (8 h)

- [ ] **Track B** (Sarthak): T5–T8 (error handling, resource scaling).
- [ ] **Track A** (Rojina + Antonia): T9–T12 (YAML overlay, WDL safety, parallel workers).
- [ ] **Track D** (Tanjim + Antonia): T13–T16 (HPC submit, monitoring, biology sanity check).
- [ ] **Track C** (Lindsey + Rachana): T17–T19 (ROI comparison, troubleshooting doc updates).
- [ ] Mid-day sync: VM-only pairs hand off HPC tests to St Jude members.
- [ ] Record decisions in test log or GitHub issues.
- [ ] Draft 3-slide deck content (organizer template).
- [ ] Sign-off rows completed in [hackathon-test-results.md](../results/hackathon-test-results.md).

### Day 3 — Explain and hand off (4 h afternoon + demo 3:00–6:00 PM)

- [ ] Finalize 3-slide deck (organizer template) — Track C + D.
- [ ] Confirm 2–4 lightning presenters: Tanjim + Antonia (+ Sarthak and/or Lindsey).
- [ ] Rehearse 2-min lightning talk (total ≤ 2 min).
- [ ] Rehearse live demo flow for demo room.
- [ ] **3:00–4:00 PM:** Lightning presentations to judges.
- [ ] **After lightning:** Live demo in demo room; field judge questions.
- [ ] **4:00–6:00 PM:** Capture judge feedback in `meetings.txt` or shared doc.
- [ ] Open PRs merged or clearly documented as follow-up.


## During the Three Days (general guidance)

### Day 1: Align and start (4 h)

- Confirm the question, problem, or opportunity.
- Confirm the inputs and expected output.
- Make sure everyone can clone the repository and make a small change.
- Agree on branch, commit, and review habits.
- Complete smoke tests (T1–T2) and start parallel track work.

### Day 2: Build and learn (8 h)

- Keep tasks small enough to finish or review in one sitting.
- Record decisions that change the approach in a decision log (create `decisions.md` if useful).
- Document data sources, assumptions, and unexpected limitations as they appear.
- Check in at mid-day and redistribute work when someone is blocked.
- Draft 3-slide deck content before end of day.

### Day 3: Explain and hand off (4 h afternoon)

- Finalize the organizer 3-slide template deck.
- Rehearse the 2-minute lightning talk and live demo.
- Present to judges (3:00–4:00 PM lightning; demo room after).
- Capture what worked, what did not, and judge feedback (4:00–6:00 PM).
- Run the available checks and record their results.

# Final Output and Handoff

Use this space for the material that helps someone understand the project after the event.

- **Final demo or report:** [Add link to recording or slide deck]
- **Lightning talk:** 2 min, 3-slide organizer template, 2–4 presenters (Day 3, 3:00–4:00 PM)
- **Live demo:** Demo room after lightning; judge Q&A and feedback (3:00–6:00 PM)
- **Main result:** Resource-aware SNAP + Sprocket orchestrator tested on Victoria Knockout; ROI documented vs legacy `launch_full_pipeline.sh`
- **How to reproduce or run it:** [hackathon-runbook.md](hackathon-runbook.md) and [scripts/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md)
- **Test results:** [hackathon-test-results.md](../results/hackathon-test-results.md)
- **Code review:** `docs/code-review-notes.md` (created during event)
- **Data and source notes:** Victoria Knockout cohort in `analyses/sc-rna-seq-snap-Victoria-Knockout/`; see [ROI one-pager](../analyses/sc-rna-seq-snap-Victoria-Knockout/docs/Snap-Sprocket-ROI-one-pager.md)
- **Known limitations:** VM cannot submit to LSF; Day-1 Sprocket tuning required ~17 attempts before stable upstream success
- **Next steps:** Extend orchestrator to other automated SNAP modalities (sc-ATAC, sc-PARSE, etc.); multi-omics runs (e.g. sc-RNA-seq + sc-ATAC); multiple projects in parallel (`snap_multi_project.wdl`); CI layout check; production rollout across St. Jude SNAP projects

Keep generated figures and reports clearly named. Do not commit sensitive data or files that cannot be redistributed.

## Communications

Keep communication easy to find and easy to use during the event.

- **Primary channel:** [Slack general channel](https://stjudebiohackathon.slack.com/archives/C04JD4M3TCM)
- **Slack team channel:** [Add the team slack channel]
- **Team lead:** Antonia Chroni ([@AntoniaChroni](https://github.com/AntoniaChroni))
- **Demo lead:** Tanjim Hassan + Antonia Chroni
- **Test log owner:** Lindsey Warren + Rachana Pandey
- **Check-in times:** Day 1 end-of-day sync · Day 2 mid-day sync (see [runbook](hackathon-runbook.md))
- **Demo session:** Day 3, 3:00–6:00 PM (lightning 3:00–4:00 PM, then live demo + judge feedback)

Use `project-management/check-in.md` for short updates when useful (create the file if needed). Do not store private contact details or sensitive project information in this public repository.

## Optional Templates

- [Team and roles](team.md)
- [Project plan](project-plan.md)
- [Hackathon runbook](hackathon-runbook.md)
- [Test results log](../results/hackathon-test-results.md)
- [SNAP overview](../docs/resources-snap.md)
- [St. Jude trainings](../docs/resources-trainings.md)

Use only the templates that help. The repository should make progress easier, not require paperwork for its own sake.
