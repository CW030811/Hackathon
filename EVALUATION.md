# Evaluation

> **Official-release alignment — September 17, 2026.** The official [scoring guide](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/scoring.md), [scorer](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/starter/score.py), [model guide](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/models.md), and [submission guide](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/submission.md) replace our pre-event Top-1 proposal as the primary scoring contract. No team benchmark results have been established by this document.

## 1. Evaluation Goals and Authority

Measure strict/partial correctness, evidence and explainability, evaluation quality, and dollars/time together. At minimum compare the routed agent with the **same agent on one model**. An interface is not a Track 1 scoring dimension; evidence and reproducible comparisons take priority over a dashboard.

**Unresolved weighting discrepancy:** the starter README states evidence 35% and accuracy 20%; the scoring guide says the participant agreement governs. Section 8 of the [agreement](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/PARTICIPANT_AGREEMENT.md) instead lists Technical Execution 40%, Innovation 30%, Potential Impact 20%, and Presentation 10%, with track-specific focus. It does not explicitly map those to 35%/20%. Ask organizers for the mapping; do not invent a combined weighted score. Both Track 1 guides emphasize evidence, while the agreement remains authoritative.

## 2. Evaluation Unit and Datasets

One evaluation unit is a **query row identified by its original `row_id`**, not necessarily one failure. Each instruction supplies a 30-minute window and a failure count; task types ask for different subsets of time, component, and reason (see [PROJECT_SCOPE.md](PROJECT_SCOPE.md)).

- Public development: 70 cases from `Market-cloudbed-1`, with `scoring_points` in `dev/query_dev.csv`.
- Official judging: the same 20 undisclosed cases for every team, from another deployment of the same shop, including unfamiliar components.
- The organizers allow tuning on all 70 public cases. Such scores must be labeled development results and can be optimistic.
- A local holdout is optional. If used, freeze it before tuning and group related failure windows where identifiable. Once inspected for tuning, it is no longer an unseen holdout.
- Do not download the original OpenRCA dataset or obtain the other deployment's answers. Keep labels, answer-derived artifacts, and case-specific solutions outside inference access.

## 3. Official Prediction and Matching Rules

Use `format_prediction()` from the official runner. Each `prediction` must contain one numbered object per failure, using the requested keys in this relative order:

```text
root cause occurrence datetime
root cause component
root cause reason
```

Rules that must be validated before scoring:

1. **Failure count:** exactly the number stated in the instruction. A mismatch zeros the whole case, including otherwise correct elements.
2. **Format:** the evaluator extracts fields with a regex, not a general JSON parser. Preserve key order and do not put newlines inside values. The official formatter's surrounding formatting is supported.
3. **Exact labels:** component and reason are exact string matches. Constrain outputs to real component candidates and the 15 official reason strings; do not add prefixes, remove pod suffixes, or substitute synonyms to make a mismatch pass.
4. **Time:** use `YYYY-MM-DD HH:MM:SS` in UTC+8; the allowed absolute error is **<= 60 seconds**.
5. **Requested fields:** only fields represented in that case's scoring points count. The runner recommends omitting unrequested fields; extra fields do not earn extra credit.
6. **Multiple failures:** output chronologically to follow submission guidance. The evaluator tries every ordering, so ordering alone does not change accuracy; incorrect count does.
7. **Row identity:** preserve original `row_id`, including non-contiguous subsets. `evidence/<row_id>.md` must use the same ID.

Keep the official `evaluate()` logic unchanged. Output validation and candidate canonicalization are allowed; relaxing the scorer's matching rules is not an official score.

## 4. Strict and Partial Scores

For each case, the evaluator finds the best matching permutation of predicted failures and counts correct requested elements across time, component, and reason. After the count gate:

```text
case partial score = matched scoring elements / all requested scoring elements
```

The official function rounds this case score to two decimal places. Reuse its result rather than reimplementing slightly different rounding or matching.

```text
mean partial score = mean of the planned cases' official case scores
strict / fully solved rate = cases with official score == 1.0 / planned cases
```

Report both, plus results by `task_1` through `task_7` and by easy/middle/hard. Optional component-, reason-, or time-specific diagnostics must be labeled supplemental, restricted to cases that request that field, and must not replace the official measures.

**Baseline interpretation:** the official heuristic reports **mean partial score 0.073** and **2/70 fully solved** on the public deployment. The former is not a 7.3% fully-solved rate; the latter is approximately 2.9%. This is a published starter result, not a team measurement and not a result on the hidden 20 cases. Published research results on the broader 335-case benchmark are a different evaluation population and must not be directly substituted for this baseline.

## 5. Completion Accounting: Do Not Lose Failed Cases

Freeze a planned case-ID manifest for each experiment. Check duplicates, missing IDs, unexpected IDs, evidence coverage, and statuses separately from answer correctness.

**Starter wrapper caveat:** `score.py` filters query rows to IDs present in predictions and inner-joins them. Its printed denominator therefore covers returned predictions, not necessarily every planned case. A truncated run can look better than it was.

Without changing the official matching function, make the team harness retain the full planned manifest, represent missing predictions as zero-scoring failures, and report both returned-case output and completion-adjusted totals when they differ. Do not count duplicate IDs twice or silently discard exceptions, timeouts, invalid outputs, and unreached cases.

Record execution status separately from correctness: a valid, completed answer can still be wrong. Always attempt a best guess for every failure, including degraded operation, while stating uncertainty in evidence. The runner's exception handler can produce an empty answer; catching the exception is crash containment, not satisfactory agent behavior.

## 6. Evidence Evaluation

Every case must write these sections:

```markdown
## Answer
## Confidence
## Evidence
## Ruled out
```

Check that the evidence actually exists and supports the stated observation. Retain source file, window/timezone, component, metric or trace/log reference, units, relevant query/transformation, and numerical result when used. Do not treat an existence check alone as proof of causality.

Review whether the explanation distinguishes observations from the hypothesis, identifies uncertainties and alternatives, and gives a reason for excluding candidates. If missing data prevents exclusion, say that; do not manufacture a healthy comparison.

The organizers check claims against raw files; evidence absent from the data scores zero. A wrong diagnosis can still have useful, honestly qualified evidence. A best guess is required in the prediction, but must never be presented as certainty in the explanation.

For our own checks, combine deterministic reference/number verification with manual review. Record how many cases/claims were checked and how they were selected. Do not let the same model's self-assessment stand alone as an evidence score.

## 7. Required Controlled Comparison

| Configuration | Role |
| --- | --- |
| Unmodified heuristic | Optional free reference; does not replace the model comparison. |
| Same agent, single model | Required control using a named permitted GLM model. |
| Same agent, routed models | Required routed configuration; document routing, fallbacks, and stopping. |

Use the same planned case IDs/order, telemetry access, tools, evidence requirements, scoring, and comparable budgets. Change the model-routing configuration rather than simultaneously changing unrelated tool or prompt logic and attributing all gains to routing.

Repeat configurations when practical and report repetition count and variation. If there is only one run, state that variability was not measured. Record actual models used, including fallbacks; a single-model control that fell back is not a pure single-model run. Document cold/warm cache conditions, preprocessing costs, model outages, and any other differences.

Use separate output directories per configuration and repetition. The starter appends `usage.jsonl`; reusing a directory can mix bills from different experiments. Do not compare only the successful subset from one configuration.

The official routed example supports `RCA_MODEL=<model>` to force a single-model control. This is a baseline experiment interface, not a routing policy selected for our final architecture.

## 8. Dollar Cost and Runtime

Record seconds per case, total elapsed run time, per-model calls/input/output tokens, estimated dollars per case, and completion. Report median, tail/max, and spread when the sample size supports them. Include loading, preprocessing, retry/fallback, and evidence-writing overhead in end-to-end runtime; startup outside per-case timers still consumes the total run budget.

Cost is measured in **dollars**, not token totals across different models. For the official reviewed price table, per million tokens:

| Model | Input USD/M | Output USD/M |
| --- | ---: | ---: |
| `zai-org/GLM-4.7-Flash` | 0.065 | 0.40 |
| `zai-org/GLM-5.3-Flash` | 0.15 | 0.50 |
| `zai-org/GLM-4.6` | 0.55 | 2.20 |
| `zai-org/GLM-4.7` | 0.55 | 2.20 |
| `zai-org/GLM-5` | 0.95 | 3.15 |
| `zai-org/GLM-5.1` | 1.30 | 4.30 |
| `zai-org/GLM-5.2` | 1.40 | 4.40 |

Use the official `cost.py` on `usage.jsonl` for development estimates and record the pricing revision. Availability and live prices can change; the official guide says judged calls are metered by organizers and priced at their published table. Do not confuse our estimates with their bill. Their key pays for judging; development credit is separate.

## 9. Hard Limits and Resilience Tests

- Per case: **10 minutes and $3**. Exceeding either zeros that case.
- Whole run: **20 minutes and $25 for 20 cases**. Reaching either stops the run; unreached cases score zero.
- Hardware: **2 CPUs, 8 GB RAM, no GPU**.
- Runtime: supplied model endpoint only; read mounted inputs, write only under `--out`, no downloads or package installs.

Set internal stops below those ceilings. Twenty minutes means roughly one minute per case on average, not ten minutes each. Save usable results after each case and preserve the runner's atomic prediction-file replacement.

Test HTTP-200 error bodies, absent `choices`, repeated capacity failures, fallback exhaustion, empty query results, memory pressure, and stopped runs. Bound retries in time as well as count. A model outage must not erase already-completed cases; evidence should disclose degraded reasoning.

## 10. Reporting and Acceptance

The final `REPORT.md` and `eval/` should include source/code revision, configuration and model choices, case manifest, tuning/holdout status, repetitions, strict/partial results by task, time/cost/completion, evidence audit, representative failures, and limitations. Do not fill report tables with illustrative numbers that look like measured results.

Before submitting:

1. Validate the actual agent, not just the default heuristic. In the official checkout, pass `AGENT=agents.yours` to applicable Makefile targets while developing.
2. Test the final Docker command **without `--agent`**, using the supplied key/endpoint and read-only dataset mount. Ensure our implementation is the default.
3. Check resource limits, every original row ID, output formatting, evidence coverage, and preserved partial progress.
4. Freeze configuration and local evaluation rules, run the comparison, and disclose any later debugging that used its results.
5. Complete the English report and roughly four-minute working presentation, fill README AI disclosure, and merge/push before **15:00 PDT on September 17, 2026**.

The validation/experiment code, Docker integration, and measured results are still to be implemented; this document defines their requirements, not their completion.
