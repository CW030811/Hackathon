# Project Scope

> **Official-release alignment — September 17, 2026.** Based on the [Track 1 brief](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/README.md) and its linked guides at official revision `314cca0bba49e1bb137aa9094d1dac4cdf7e4490`. Dataset facts below are documented by the organizers, not yet verified by our own inspection. Implementation choices remain open; official interface and evaluation constraints do not.

## 1. Objective

Build an unattended, evidence-driven RCA agent that uses the supplied microservice telemetry to identify the requested failure onset time, root-cause component, and/or reason, routes calls across the permitted GLM models on Featherless, and demonstrates the accuracy, dollar-cost, and runtime trade-offs against the same agent on a single model.

Every case must receive a best-guess prediction and an explanation grounded in actual observations. A guess is not a confirmed fact: uncertainty, missing evidence, and competing explanations belong in the evidence file.

## 2. Three Required Deliverables

### Agent

A Dockerized program that runs without human intervention on another deployment of the same system. Preserve the official command:

```bash
python run.py --dataset /data --queries /data/query.csv --out /out
```

Integrate through `solve(instruction, dataset_dir, ctx) -> Solution`. Preserve the starter runner's CLI, output formatting, and per-case persistence; set our agent as its default. The judge does not pass `--agent`.

### Evaluation

A reproducible harness under `eval/`, with at least a routed-versus-single-model comparison using the same agent, cases, tools, and scoring rules. Report strict and partial scores, dollars and seconds per case, run completion, and repeat-run variation. `REPORT.md` must explain the comparison, failure modes, limitations, and team changes to the starter.

### Explanation

For every original query `row_id`, write `evidence/<row_id>.md` containing `Answer`, `Confidence`, `Evidence`, and `Ruled out`. Observations and quantitative claims must be checkable against the supplied raw telemetry. Evidence quality is evaluated even when the selected diagnosis is wrong.

These requirements come from the official [submission](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/submission.md) and [scoring](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/scoring.md) guides.

## 3. Case Contract

The public `Market-cloudbed-1` bundle has 70 development query rows. Each instruction gives a 30-minute window and the number of failures. One query row is a case; it may contain multiple failures.

| Task type | Requested fields |
| --- | --- |
| `task_1` | Time |
| `task_2` | Reason |
| `task_3` | Component |
| `task_4` | Time and reason |
| `task_5` | Time and component |
| `task_6` | Component and reason |
| `task_7` | Time, component, and reason |

Only requested fields are scored. Emit exactly the stated number of failures; use the official formatter and exact component/reason vocabulary. Do not impose a generic single-incident or service-level schema. Time localization means estimating onset inside the supplied window, not detecting arbitrary future incidents.

Official judging uses 20 undisclosed cases from a different deployment of the same shop, including unfamiliar components. Discover component candidates from the provided telemetry rather than hard-coding the public deployment's names.

## 4. In Scope

- Inspect the official starter, reproduce its free heuristic baseline, and identify specific weaknesses before rebuilding functionality it already supplies.
- Parse the task, time window, required fields, and failure count from the allowed query input.
- Query relevant metrics, logs, and traces within the memory and time limits; correlate actual entity identifiers and dependencies.
- Distinguish onset from an anomaly peak, and a causal component from affected components.
- Investigate network-fault hypotheses using trace relationships; do not rely solely on metric rankings.
- Route GLM calls by need, implement budget-aware stopping and model fallback, and record actual model usage.
- Produce valid predictions, reproducible evidence, honest uncertainty, and alternative-hypothesis checks.
- Compare configurations fairly and report failures rather than selecting only successful demonstrations.
- Package an unattended root-Dockerfile submission and prepare an English working presentation of around four minutes.

## 5. Non-Negotiable Runtime Constraints

| Area | Official constraint |
| --- | --- |
| LLM inference | The seven permitted GLM `zai-org/*` models through Featherless. |
| Credentials/endpoint | Read `FEATHERLESS_API_KEY`; honor `FEATHERLESS_BASE_URL` if set. |
| Per case | 10 minutes and $3 maximum; exceeding either scores zero for that case. |
| Whole run | 20 minutes and $25 for all 20 cases; reaching either stops the run, and unreached cases score zero. |
| Hardware | 2 CPUs, 8 GB RAM, no GPU. |
| Data and network | Use supplied inputs; write outputs/caches only under `--out`; no runtime external access except the supplied model endpoint. |
| Model outages | Handle error bodies even on HTTP 200, retry within budget, fall back within GLM, and continue. |

Source: official [models.md](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/models.md). Development coding assistants are distinct from the submitted inference agent; see [CONTRIBUTING.md](CONTRIBUTING.md).

## 6. Out of Scope

- Autonomous remediation, infrastructure changes, future-incident prediction, or a full monitoring platform.
- A mandatory dashboard or interactive judging flow. Track 1 runs headlessly; an optional interface is only a presentation aid.
- Foundation-model training as the core project, non-GLM runtime inference, runtime package/data downloads, or other external APIs.
- Looking up answers, downloading the upstream OpenRCA dataset, baking development answers into the image, or carrying case-specific solutions into inference.
- Fabricated evidence or presenting an unsupported hypothesis as established fact.

## 7. Execution Priorities

First reproduce the official baseline and inspect real files. Then perform manual RCA on selected development cases, record useful queries and decision points, and agree which starter capabilities to retain or improve. Prioritize evidence correctness, trace-aware diagnosis, output validity, controlled routing comparisons, and Docker reproducibility over optional UI work.

The organizer reports the heuristic at **0.073 mean partial score and 2/70 fully solved cases**. It ranks metric anomalies, does not read logs/traces, and estimates time from a peak. These are starting observations to test, not a promise that a particular redesign will improve results.

## 8. Open Decisions and Review Window

`docs/ARCHITECTURE.md` remains completely empty. No database, framework, fixed tool count, or agent workflow is selected by this update.

After actual starter/data inspection and manual RCA, the team should review:

- Real `row_id` availability, timestamp parsing, candidate identifiers, and source-file coverage.
- Data access and cache strategy under the judged hardware and write restrictions.
- Tool interfaces and evidence representation demonstrated by manual investigation.
- Routing policy, fallback order, stopping budgets, and a comparable single-model control.
- Local experiment grouping and whether a genuine held-out development subset can be maintained.

Give those verified findings to the development AI, review its proposed architecture, then fill the architecture document. Update README, this scope, data policy, and evaluation together when facts change. Do not relax official constraints or scoring rules to fit an unfavorable result.

## 9. Definition of Done

The intended submission builds from a public default-branch checkout, runs the official Docker command without interaction or `--agent`, completes the assigned cases within resource limits, writes valid predictions and evidence keyed by original row IDs, and includes a reproducible model comparison in `REPORT.md` and `eval/`. The README must document actual setup and AI usage. None of these completion claims is implied merely by having these planning documents.
