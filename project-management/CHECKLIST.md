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

Use the folders that fit your project. You do not need to fill every folder. The following is just a suggestion, yours might look different.

```text
data/raw/           Original inputs; do not edit in place
data/processed/     Cleaned or transformed data
models/             Models, predictions, or model notes
project-management/ Team plan, roles, decisions, and check-ins
results/            Test logs, ROI notes, and event artifacts
src/                Reusable code, organized by purpose
docs/               Optional learning and troubleshooting guides
assets/             Images or other supporting project assets
```

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

Follow the [hackathon runbook](hackathon-runbook.md) for the detailed timeline. Summary:

### Hour 0–1: Align and start

- [ ] Kickoff: confirm pairs (A/B/C/D) and shared test log.
- [ ] Everyone clones repo and runs T1 (`test-downstream-layout.sh`).
- [ ] Everyone runs T2 dry-run (`launch-snap-downstream.sh`).
- [ ] HPC pairs confirm `module load sprocket R singularity`.

### Hour 1–3: Parallel track work

- [ ] **Track A** (Rojina + Antonia): code audit started; issues filed.
- [ ] **Track B** (Sarthak + David): T1–T4 logged with screenshots.
- [ ] **Track C** (Lindsey + Rachana): test log open; PR review checklist ready.
- [ ] **Track D** (Tanjim + Jason): HPC golden-path submit (T13).

### Hour 3: Sync

- [ ] Blockers raised; VM-only pairs hand off HPC tests to St Jude members.
- [ ] Redistribute work if anyone is stuck.

### Hour 3–5: Build and learn

- [ ] Track B: T5–T8 (error handling, resource scaling).
- [ ] Track A: T9–T12 (YAML overlay, WDL safety, parallel workers).
- [ ] Track D: T14–T16 (monitoring, email, biology sanity check).
- [ ] Track C: T17–T19 (ROI comparison, troubleshooting doc updates).
- [ ] Record decisions in test log or GitHub issues.

### Hour 5–8: Explain and hand off

- [ ] Slides drafted (1–2 per track).
- [ ] Demo rehearsed once (live or recorded fallback).
- [ ] Sign-off rows completed in [hackathon-test-results.md](../results/hackathon-test-results.md).
- [ ] Open PRs merged or clearly documented as follow-up.


## During the Three Days (general guidance)

### Day 1: Align and start

- Confirm the question, problem, or opportunity.
- Confirm the inputs and expected output.
- Make sure everyone can clone the repository and make a small change.
- Agree on branch, commit, and review habits.

### Day 2: Build and learn

- Keep tasks small enough to finish or review in one sitting.
- Record decisions that change the approach in a decision log (create `decisions.md` if useful).
- Document data sources, assumptions, and unexpected limitations as they appear.
- Check in briefly and redistribute work when someone is blocked.

### Day 3: Explain and hand off

- Decide what the final demo and booth must show as a team.
- Make the main workflow understandable to someone who was not in the room.
- Capture what worked, what did not, and what should happen next.
- Run the available checks and record their results.

# Final Output and Handoff

Use this space for the material that helps someone understand the project after the event.

- **Final demo or report:** [Add link to recording or slide deck]
- **Main result:** Resource-aware SNAP + Sprocket orchestrator tested on Victoria Knockout; ROI documented vs legacy `launch_full_pipeline.sh`
- **How to reproduce or run it:** [hackathon-runbook.md](hackathon-runbook.md) and [scripts/README.md](../analyses/sc-rna-seq-snap-Victoria-Knockout/scripts/README.md)
- **Test results:** [hackathon-test-results.md](../results/hackathon-test-results.md)
- **Code review:** `docs/code-review-notes.md` (created during event)
- **Data and source notes:** Victoria Knockout cohort in `analyses/sc-rna-seq-snap-Victoria-Knockout/`; see [ROI one-pager](../analyses/sc-rna-seq-snap-Victoria-Knockout/docs/Snap-Sprocket-ROI-one-pager.md)
- **Known limitations:** VM cannot submit to LSF; Day-1 Sprocket tuning required ~17 attempts before stable upstream success
- **Next steps:** Multi-project scatter (`snap_multi_project.wdl`), CI layout check, production rollout to additional SNAP projects

Keep generated figures and reports clearly named. Do not commit sensitive data or files that cannot be redistributed.

## Communications

Keep communication easy to find and easy to use during the event.

- **Primary channel:** [Slack general channel](https://stjudebiohackathon.slack.com/archives/C04JD4M3TCM)
- **Slack team channel:** [Add the team slack channel]
- **Team lead:** Antonia Chroni ([@AntoniaChroni](https://github.com/AntoniaChroni))
- **Demo lead:** TBD
- **Test log owner:** TBD
- **Check-in time:** Hour 3 sync (see [runbook](hackathon-runbook.md))

Use `project-management/check-in.md` for short updates when useful (create the file if needed). Do not store private contact details or sensitive project information in this public repository.

## Optional Templates

- [Team and roles](team.md)
- [Project plan](project-plan.md)
- [Hackathon runbook](hackathon-runbook.md)
- [Test results log](../results/hackathon-test-results.md)
- [SNAP overview](../docs/resources-snap.md)
- [St. Jude trainings](../docs/resources-trainings.md)

Use only the templates that help. The repository should make progress easier, not require paperwork for its own sake.
