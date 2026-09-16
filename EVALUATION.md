# Evaluation

> **Pre-hackathon evaluation plan:** This document defines the evaluation principles and reporting structure based on information available before the event. Dataset-dependent scoring rules may be refined after the official Track 1 labels, incident structure, and evaluation resources are inspected. Core evaluation principles should be fixed before final testing and should not be changed simply because a result is unfavorable.

## 1. Purpose

This document defines how the Root Cause Analysis (RCA) system will be evaluated.

The evaluation should measure both diagnosis quality and diagnosis efficiency while remaining reproducible and resistant to label leakage.

The main goals are to determine:

- Whether the system identifies the correct root cause.
- Whether it localizes the correct component or entity.
- Whether its conclusions are supported by real telemetry evidence.
- How much time and model/tool usage are required per incident.
- How often the system fails, times out, or produces invalid output.

## 2. Pre-Hackathon Evaluation Boundary

Before the official event resources are released, we do not assume the exact:

- Label schema
- Incident count
- Root-cause taxonomy
- Component granularity
- Train/development/test split
- Ground-truth representation
- Official benchmark or scoring script

These dataset-dependent details may be added or refined after the official resources are inspected.

However, evaluation should remain consistent with the following principles:

- Ground truth must remain isolated from the RCA agent during evaluation.
- Evaluation incidents should not be used for prompt tuning or workflow tuning after evaluation begins.
- Free-text predictions should be normalized into a reproducible scoring representation whenever possible.
- Failures and timeouts must remain part of the denominator.
- Evaluation rules should be frozen before final testing.

## 3. Evaluation Unit

The expected evaluation unit is one incident.

For each evaluated incident, the evaluation record should capture, when available:

- Incident identifier
- Input context presented to the system
- Ground-truth root cause
- Ground-truth affected component or entity
- Agent prediction
- Supporting evidence returned by the system
- Diagnosis runtime
- Model calls
- Tool calls
- Token usage
- Estimated model cost
- Final run status

If the official incident structure differs, this section should be updated after the event data is inspected.

## 4. Primary Metric: Root Cause Top-1 Accuracy

The primary quality metric is **Root Cause Top-1 Accuracy**.

```text
Root Cause Top-1 Accuracy
=
Number of incidents with a correct top-1 root-cause prediction
/
Total number of evaluated incidents
```

The exact definition of a correct match depends on the official ground-truth format and must be fixed before final evaluation.

### Structured scoring

Whenever possible, root-cause scoring should use structured fields rather than direct free-text string comparison.

For example, an evaluation representation may separate:

```text
root_cause_component
root_cause_category
```

A prediction such as:

```text
The feature-service was CPU throttled.
```

may correspond to a structured representation such as:

```json
{
  "component": "feature-service",
  "cause": "cpu_throttling"
}
```

The actual schema must follow the official labels rather than being imposed in advance.

### Normalization

If labels and predictions use different wording for the same concept, normalization rules should be defined before final scoring.

Normalization must not be adjusted case-by-case after inspecting individual evaluation results.

## 5. Component Localization Accuracy

Component localization should be evaluated separately from root-cause classification when the labels support this distinction.

```text
Component Localization Accuracy
=
Number of incidents with the correct affected/root-cause component
/
Total number of evaluated incidents
```

This separation helps distinguish cases where the system:

- Identifies the correct component but the wrong failure mechanism.
- Identifies the wrong component but names a plausible failure type.
- Correctly identifies both the component and root-cause category.

The evaluation granularity may be service-, workload-, pod-, node-, or another level depending on the official labels.

## 6. Evidence Support

The RCA system should support its conclusions with real telemetry evidence rather than unsupported narrative reasoning.

Where feasible, each RCA result should include references to the evidence used during investigation, such as:

- Metric names and time windows
- Trace or span identifiers
- Log records or log-query results
- Entity identifiers
- Relevant metadata or configuration records

### Evidence Support Rate

An evidence-support measure may be reported when the available data and evaluation process support it.

A supported conclusion should satisfy two conditions:

1. The referenced evidence actually exists in the underlying data.
2. The evidence is relevant to the claim being made.

Evidence quality should not be assessed only by the same model that produced the RCA conclusion.

Possible validation methods include:

- Automated reference-validity checks
- Deterministic checks against telemetry queries
- Manual spot-checking
- Human review of evidence-to-claim consistency

The exact procedure should be documented before reporting an evidence-support metric.

## 7. Diagnosis Efficiency

The system should be evaluated not only on correctness but also on the resources required to reach a diagnosis.

For each incident, record when available:

```text
diagnosis_time
model_calls
tool_calls
input_tokens
output_tokens
estimated_cost
```

Recommended aggregate statistics include:

- Median diagnosis time
- P95 diagnosis time
- Average model calls per incident
- Average tool calls per incident
- Average input/output token usage
- Estimated cost per incident

Efficiency metrics should include failed and timed-out runs where applicable.

## 8. Failure Handling

Failures must not be silently removed from evaluation.

Examples include:

- Timeout
- Exception
- Invalid output
- Empty answer
- Tool failure that prevents diagnosis
- Agent loop that reaches a defined execution limit

Unless the official benchmark specifies otherwise, these cases remain part of the total number of evaluated incidents.

For example:

```text
10 incidents evaluated
6 correct
2 incorrect
2 timeout
```

The Root Cause Top-1 Accuracy is:

```text
6 / 10 = 60%
```

not:

```text
6 / 8 = 75%
```

A separate failure rate may also be reported.

## 9. Development vs Evaluation Data

If the organizers provide an official split, the project should follow it.

If no split is provided, the team should define and document a split after inspecting the dataset and before final evaluation.

### Development data

Development incidents may be used for:

- Prompt tuning
- Tool tuning
- Workflow design
- Debugging
- Error analysis
- Agent behavior refinement

### Evaluation data

Evaluation incidents should be used only for final or held-out testing after the evaluation protocol is fixed.

Once an incident's ground-truth answer has influenced prompt design, tool logic, rules, or manual tuning, that incident should no longer be treated as a truly unseen evaluation example.

## 10. Leakage Prevention

Ground-truth information must not be available to the RCA agent during evaluation.

Potential leakage sources include:

- Root-cause label fields
- Answer columns
- Incident annotations containing the solution
- Evaluation-only metadata
- Filenames that reveal the failure type
- Derived features that directly encode the label
- Tool outputs containing hidden ground truth
- Prompt text that includes the answer

Ground truth should be isolated from the agent context, tool-accessible data, and derived inputs used during evaluation.

Refer to `DATA_POLICY.md` for broader data-handling rules.

## 11. Reporting Format

The final evaluation should include a per-incident table when practical.

Example structure:

| Incident | RCA Correct | Component Correct | Evidence Supported | Time | Tool Calls | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| INC-001 | 1 | 1 | 1 | 8.2 s | 5 | success |
| INC-002 | 0 | 1 | 1 | 11.4 s | 7 | wrong RCA |
| INC-003 | 0 | 0 | 0 | 30.0 s | 10 | timeout |

Recommended summary metrics include:

- Root Cause Top-1 Accuracy
- Component Localization Accuracy
- Evidence Support Rate, if a valid procedure is defined
- Median diagnosis time
- P95 diagnosis time
- Average tool calls
- Average model calls
- Average token usage
- Estimated cost per incident
- Failure rate

No target threshold is defined before the official dataset is available.

## 12. Optional Breakdowns

If the number and diversity of incidents are sufficient, results may also be broken down by categories such as:

- Failure type
- Cluster
- Service or workload category
- Root-cause class
- Incident complexity

These breakdowns should only be reported when there are enough examples to make the comparison meaningful.

## 13. Event-Day Evaluation Review

After receiving the official Track 1 resources, the team should review this evaluation plan before implementing final scoring.

The review should confirm:

- The label schema
- Root-cause granularity
- Component granularity
- The evaluation unit
- Whether an official development/test split exists
- Which fields are ground truth and must be isolated
- How predictions will be normalized
- How failures and timeouts will be represented
- Which efficiency fields can be measured reliably
- Whether evidence support can be evaluated reproducibly

After these decisions are made, the evaluation protocol should be documented and frozen before final testing.

Final evaluation results should distinguish clearly between:

- Measured results
- Estimated quantities
- Manually reviewed results
- Unverified claims
