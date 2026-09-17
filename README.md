# MantisGrid Hackathon — Root Cause Analysis Agent

A Track 1 project to identify failure onset, root-cause components, and reasons from telemetry, with verifiable evidence and measured GLM model routing.

> Requirements reviewed on September 17, 2026 against the [official repository](https://github.com/MantisGridAI/hackathon-2026-official/tree/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1). This update aligns project documentation; it does not claim that the starter has been integrated, the dataset inspected locally, or experiments completed.

## What We Are Building

The [official brief](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/README.md) asks for three deliverables:

1. **An unattended agent:** query the supplied telemetry and answer the requested failure time, component, and/or reason. Route model calls within the permitted GLM family on Featherless.
2. **An evaluation harness:** compare at least the routed agent with the same agent using a single model, reporting correctness, dollars, time, and variation across repeated runs.
3. **An explanation for every case:** show actual supporting telemetry, confidence, and alternatives ruled out. Always provide a best guess in the prediction; put uncertainty in the evidence, never invent supporting observations.

Track 1 is judged headlessly. A dashboard is not a required technical deliverable and must not displace evidence, evaluation, or packaging work.

## Official Inputs

As documented in [data.md](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/data.md):

- **Development bundle:** `Market-cloudbed-1`, approximately 1.3 GB zipped and 12 GB unpacked, containing metrics, logs, and traces.
- **Development cases:** 70 query rows; answers are in `dev/query_dev.csv` under `scoring_points`.
- **Case context:** a 30-minute window and a stated number of failures. Seven task types ask for different subsets of time, component, and reason.
- **Official judging:** 20 undisclosed cases from another deployment of the same shop, with different components. The public 70-case score is not the official test score.
- **Time handling:** metric/log timestamps use seconds; trace timestamps use milliseconds. Interpret task and answer times as UTC+8 and preserve source units when normalizing.

Use only the event-provided bundle. Do not download the original OpenRCA dataset, which includes judging answers. See [DATA_POLICY.md](DATA_POLICY.md) for schemas, label isolation, and local storage.

## Required Outputs and Submission Interface

The [submission specification](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/submission.md) requires a root Dockerfile and the following command inside the image:

```bash
python run.py --dataset /data --queries /data/query.csv --out /out
```

For each original `row_id`, the run must write:

| Output under `--out` | Purpose |
| --- | --- |
| `predictions.csv` | Columns `row_id` and `prediction`; the prediction contains one numbered object per stated failure. |
| `evidence/<row_id>.md` | Four sections: `Answer`, `Confidence`, `Evidence`, and `Ruled out`. |
| `usage.jsonl` | Starter-generated per-case timing and per-model usage for our own analysis. Judging uses organizer-side metering. |

Use the starter's `format_prediction()` rather than free-form serialization. The evaluator expects the requested keys in the relative order **datetime, component, reason**, exact component/reason strings, and exactly the stated failure count. Preserve original row IDs even when running a subset. Details and strict/partial scoring are in [EVALUATION.md](EVALUATION.md).

The final repository must also contain `REPORT.md` and `eval/` with the writeup, comparison harness, and results. These are implementation deliverables to add during development, not completed artifacts in this documentation update.

## Runtime Constraints

From the official [models](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/models.md) and [submission](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/submission.md) guides:

| Constraint | Requirement |
| --- | --- |
| Runtime models | The seven listed `zai-org/*` GLM models on Featherless; choose per call and support fallback. |
| Environment | `FEATHERLESS_API_KEY`; honor `FEATHERLESS_BASE_URL` when supplied. |
| Machine | 2 CPUs, 8 GB RAM, no GPU. |
| Per case | At most 10 minutes and $3. |
| Full judged run | At most 20 minutes and $25 for 20 cases; unreached cases score zero. |
| Runtime access | Read supplied dataset/query inputs; write artifacts and caches only under `--out`; no external access except the supplied model endpoint. |

The run budget permits only about one minute per case on average, including shared overhead. A ten-minute per-case ceiling is not an acceptable average. HTTP 200 can contain a model-capacity error: check the body, retry within budget, fall back, and preserve partial progress.

## First Execution Check: Official Starter

Run these in a separate official checkout, **not at the root of this repository**. First follow the official [GET_DATA.md](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/GET_DATA.md), placing its bundle at `track-1/data/Market-cloudbed-1/`:

```bash
cd hackathon-2026-official/track-1
python -m pip install -r starter/requirements.txt
make validate
make dev N=2
make score
```

The default heuristic uses no LLM. `make dev && make score` covers all 70 public cases. The published starter result is **0.073 mean partial score, with 2/70 cases fully solved**; this is an organizer-reported baseline, not our result.

When integrating, preserve `run.py`'s CLI and `solve(instruction, dataset_dir, ctx) -> Solution`. Set our agent as the default because judges do not pass `--agent`. Keep experiment outputs in separate directories to avoid mixing predictions or appended usage logs. Do not assume the unmodified starter is a sufficient final submission.

## Repository and Documentation

```text
.
├── README.md
├── CONTRIBUTING.md
├── PROJECT_SCOPE.md
├── DATA_POLICY.md
├── EVALUATION.md
├── .gitignore
├── .github/PULL_REQUEST_TEMPLATE.md
├── docs/ARCHITECTURE.md           # intentionally empty
└── data/
    ├── raw/.gitignore
    ├── processed/.gitkeep
    └── samples/.gitkeep
```

- [Project scope](PROJECT_SCOPE.md): deliverables, required behavior, priorities, and what remains undecided.
- [Data policy](DATA_POLICY.md): official data facts, integrity, processing, and answer isolation.
- [Evaluation](EVALUATION.md): official scoring, controlled model comparisons, budgets, and reporting.
- [Contributing](CONTRIBUTING.md): branches, commits, reviews, and implementation safeguards.
- [Architecture](docs/ARCHITECTURE.md): intentionally empty until starter/data inspection and manual RCA inform a team-reviewed design.

## Submission

Submit the public default-branch repository and English materials through the [official form](https://forms.gle/UbPSwZhKNfkovM8s5) **before September 17, 2026, 15:00 PDT**. Prepare a presentation of around **four minutes** showing a working case, its evidence, and the model comparison. Do not rely on the earlier two-minute/Devpost-only preparation notes.

Before submission, validate our actual agent, test the Docker entry point without `--agent`, finish `REPORT.md` and `eval/`, complete the AI disclosure below, and merge and push all intended work. The [participant agreement](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/PARTICIPANT_AGREEMENT.md) governs; the scoring-weight discrepancy in the starter is recorded in [EVALUATION.md](EVALUATION.md).

## AI Usage Disclosure
