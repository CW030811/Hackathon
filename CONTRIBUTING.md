# Contributing

Working conventions for our MantisGrid AI Hackathon 2026 Track 1 team. See [README.md](README.md) for project navigation and [PROJECT_SCOPE.md](PROJECT_SCOPE.md) for the official-release requirements.

## 1. Fresh Work and Attribution

Before the event, keep preparation to documentation, research, planning, and non-functional repository setup. Judged team implementation must be created during the official competition window.

The [participant agreement](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/PARTICIPANT_AGREEMENT.md) permits licensed open-source libraries and supplied starter kits. Use the official starter rather than recreating its runner, but preserve required attribution and meaningfully improve it. Do not misrepresent organizer-provided functionality as team-built work. After the deadline, only permitted bug fixes/deployment repairs, not new features, may be added.

## 2. Branching

Do not develop directly on `main` unless the team explicitly agrees that a very small documentation-only change can be committed directly.

Create one focused branch per task:

- `feat/<name>` — new functionality
- `fix/<name>` — bug fixes
- `docs/<name>` — documentation
- `test/<name>` — tests and evaluation
- `refactor/<name>` — restructuring without intended behavior changes

Examples: `feat/trace-analysis`, `feat/model-routing`, `fix/time-conversion`, `docs/readme-update`.

## 3. Commit Messages

Use a short, descriptive type and summary:

```text
feat: add trace evidence queries
fix: preserve UTC+8 onset timestamps
docs: align evaluation with official scorer
test: compare routed and single-model configurations
refactor: simplify agent state
```

Keep changes small and focused. Avoid unrelated edits in one commit and save working checkpoints frequently.

## 4. Pull Requests and Coordination

Sync with the latest practical `main`, check the change locally, and use the PR template to explain what changed, why, and how it was verified. Keep review lightweight but meaningful; ask a teammate to review shared interfaces and core logic when practical.

Notify affected teammates before changing shared files. In particular, coordinate `run.py`, prediction formatting, query identifiers, timestamp normalization, model-client behavior, and evidence schema. The implemented architecture is documented in `docs/ARCHITECTURE.md`; module contracts are in `docs/INTERFACES.md`.

## 5. Official Track 1 Integration Safeguards

These are constraints from the official [submission](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/submission.md) and [models](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/models.md) guides:

- Keep the CLI `python run.py --dataset ... --queries ... --out ...` compatible. Implement `solve(instruction, dataset_dir, ctx) -> Solution` and use `format_prediction()`.
- Set our final agent as the runner default; judging does not pass `--agent`. Preserve per-case output persistence and original `row_id` values.
- Keep one unambiguous root Dockerfile. Install dependencies at build time; the judged run has no external access except the supplied model endpoint.
- Use only permitted GLM models for submitted LLM inference. Read `FEATHERLESS_API_KEY` and honor `FEATHERLESS_BASE_URL`; never bypass the supplied endpoint.
- Check error bodies even when HTTP status is 200. Bound retries, fall back within the family, and keep going when one model is unavailable.
- Respect 2 CPUs/8 GB/no GPU, 10 minutes/$3 per case, and 20 minutes/$25 for the whole 20-case run.
- Read supplied data without modifying it. All runtime outputs and caches must be under `--out`.
- Keep exact requested prediction keys, exact labels, and stated failure counts. Always emit a best guess, with uncertainty in the evidence.
- Produce `Answer`, `Confidence`, `Evidence`, and `Ruled out` sections. Do not fabricate observations, references, units, or quantitative results.

## 6. Upload and Data Rules

Commit useful source, tests, documentation, safe configuration templates, and reviewed evaluation artifacts. Do not commit keys, tokens, passwords, secret `.env` files, private credentials, raw bundles, large derived tables, temporary files, or unnecessary machine-specific settings.

The local structure remains:

```text
data/
├── raw/
├── processed/
└── samples/
```

Raw and large processed data stay local; small samples require review and publication permission. Do not modify original data in place. During judging, write derived outputs under `--out`, not these development paths.

Follow [DATA_POLICY.md](DATA_POLICY.md): no original OpenRCA dataset download, no answer-bearing `scoring_points` or answer artifacts in inference, and no hard-coded deployment-specific solutions. Keep required `eval/` results and `REPORT.md` available for judges without exposing them as answer sources to the agent.

If a secret is committed, notify the team and rotate/revoke it; merely deleting the latest copy is insufficient.

## 7. AI-Assisted Development

Development assistants and submitted inference are different roles. The agreement permits AI coding tools for development; the Track 1 runtime uses the specified GLM family on Featherless.

Record the models, coding assistants, frameworks, substantial AI-generated changes, team work, and reused starter components. Review and understand generated code before merging. The final README must disclose actual usage; do not invent entries before work occurs.

## 8. Before Merging

- [ ] The change is focused and synchronized with the latest practical `main`.
- [ ] Verification is described; documentation-only changes identify runtime checks as not applicable.
- [ ] No secrets, unauthorized data, or answer leakage are introduced.
- [ ] Relevant shared interfaces and documentation are updated and communicated.
- [ ] Applicable CLI, formatter, row-ID, evidence, endpoint, and resource checks pass.
- [ ] AI-assisted changes are understood; experiment numbers are measured or explicitly labeled otherwise.

## 9. Keep the Process Lightweight

Prefer clear ownership, small reviews, reproducible evidence, and a working headless submission. An optional UI must not delay the required agent, evaluation, explanation, Docker check, or submission. Merge intended work to the default branch before the official deadline; the organizers judge what they clone, not an unmerged development branch.
