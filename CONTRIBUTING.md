# Contributing

Thank you for contributing to the MantisGrid AI Hackathon 2026 project.

This repository is used by our team for **Track 1: Root Cause Analysis (RCA)**. This document defines the working conventions we will follow so that contributions remain easy to review, merge, and trace during the hackathon.

## 1. Fresh Work Policy

To comply with the hackathon's fresh-work requirement, we distinguish clearly between pre-hackathon preparation and competition implementation.

### Before the official hackathon starts

Allowed preparation includes:

- Documentation and research notes
- Architecture discussions and planning
- Repository scaffolding
- Contribution guidelines and templates
- Learning materials and non-functional preparation

Do **not** implement competition features in advance.

### During the hackathon

- All judged implementation should be created during the official competition window.
- Functional code, integrations, analysis pipelines, agents, dashboards, and evaluation logic should be implemented during the event.
- Commit history should make it clear when implementation work was created.

## 2. Branching

Do not develop directly on `main` unless the team explicitly agrees that a very small documentation-only change can be committed directly.

Create a branch for each task using one of the following prefixes:

- `feat/<name>` — new functionality
- `fix/<name>` — bug fixes
- `docs/<name>` — documentation
- `test/<name>` — tests or evaluation
- `refactor/<name>` — code restructuring without changing intended behavior

Examples:

```text
feat/metrics-analysis
feat/trace-analysis
feat/log-analysis
feat/agent
feat/ui
fix/trace-parser
docs/readme-update
```

Keep each branch focused on one clear task whenever possible.

## 3. Commit Messages

Use short, descriptive commit messages based on a simplified Conventional Commits format.

Examples:

```text
feat: add metrics comparison tool
fix: handle missing trace spans
docs: update RCA workflow
test: add incident evaluation cases
refactor: simplify agent state
```

Guidelines:

- Keep commits small and focused.
- Avoid mixing unrelated changes in one commit.
- Write messages that make the purpose of the change clear.
- Commit working checkpoints frequently during the hackathon so changes remain easy to trace and revert.

## 4. Pull Requests

Before opening a pull request:

1. Pull or rebase against the latest `main`.
2. Make sure the code runs locally.
3. Keep the PR focused on one task.
4. Briefly describe:
   - What changed
   - Why it changed
   - How it was tested or verified

Prefer small pull requests that can be reviewed and merged quickly.

During the hackathon, review should be lightweight but meaningful. A teammate should check the change when practical, especially for shared interfaces, core agent logic, data-processing code, and files that affect multiple modules.

## 5. Repository and Upload Rules

The repository should contain only files that are useful for building, running, evaluating, or explaining the project.

### Appropriate to commit

- Source code
- Tests
- Documentation
- Configuration templates
- Small sanitized sample datasets
- Evaluation scripts and results
- Reproducible notebooks when they are part of the project workflow

### Never commit

- API keys
- Access tokens
- Passwords
- `.env` files containing secrets
- Private event credentials
- Cloud credentials
- Personal credentials
- Large raw datasets unless explicitly allowed and necessary
- Temporary files
- Local IDE settings that are not required by the team
- OS-generated files

Examples of files that should not be committed:

```text
.env
*.key
credentials.json
secrets.json
.DS_Store
```

Secrets must be loaded through environment variables or another approved local configuration mechanism.

If a secret is accidentally committed, notify the team immediately and rotate or revoke the exposed credential rather than only deleting the file in a later commit.

## 6. Data Handling

Track 1 may involve telemetry and incident data such as metrics, logs, traces, and labeled incidents.

Use the following structure when appropriate:

```text
data/
├── raw/
├── processed/
└── samples/
```

Guidelines:

- Keep large raw datasets local unless the event explicitly allows and requires them to be committed.
- Treat `data/raw/` as local-only by default.
- Commit only small, sanitized samples when they are useful for testing, documentation, or reproducibility.
- Do not modify original raw data in place; write transformed data to `data/processed/`.
- Document any important preprocessing steps that affect interpretation or evaluation.
- Do not expose labels or ground-truth information to an agent if doing so would invalidate evaluation.

## 7. Team Coordination

Before editing a shared core file, notify the team when there is a realistic chance that another teammate is working on the same file.

Prefer separate modules and clear ownership of active tasks whenever possible.

For example, implementation may eventually be separated into areas such as:

```text
src/
├── metrics/
├── traces/
├── logs/
├── agent/
└── ui/
```

The exact project structure may change during the hackathon. The goal is not to enforce a rigid architecture, but to reduce merge conflicts and make ownership clear.

When interfaces between modules change, communicate the change before merging so dependent work can be updated quickly.

## 8. AI-Assisted Development

AI coding assistants and models may be used during development as permitted by the event rules.

Contributors should keep track of:

- AI coding assistants used
- Models used
- Agent frameworks used
- Major components substantially generated or modified with AI assistance
- Major components designed and implemented directly by team members

This information will be summarized in the final project README and submission materials.

AI-generated code should still be reviewed, tested, and understood by the team before it is merged.

## 9. Before Merging

Use this checklist before merging a change into `main`:

- [ ] My branch is based on the latest practical version of `main`.
- [ ] The code runs locally or the documentation renders correctly.
- [ ] No secrets, credentials, or private tokens are included.
- [ ] Large raw data is not committed unnecessarily.
- [ ] The change is limited to one clear task or purpose.
- [ ] Relevant documentation is updated when needed.
- [ ] Shared interfaces or core files were communicated to affected teammates.
- [ ] AI-assisted work has been reviewed and is understood by the team.

## 10. Keep the Process Lightweight

This is a time-limited hackathon project. These rules are intended to reduce mistakes, merge conflicts, and compliance risks without slowing the team down.

When in doubt, prefer:

- Small changes
- Clear ownership
- Fast communication
- Reproducible analysis
- Evidence-backed conclusions
- A clean and understandable commit history
