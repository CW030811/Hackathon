# Data Policy

> **Pre-hackathon policy:** This document defines data-handling principles based on information available before the event. Dataset-specific rules may be revised after the official Track 1 resources are released and inspected.

This policy governs how competition data should be read, transformed, stored, exposed to AI systems, and used for development and evaluation.

The goal is to preserve data integrity, prevent evaluation leakage, and keep the Root Cause Analysis workflow reproducible and evidence-based.

## 1. Scope

This policy applies to all Track 1 data used by the project, including official telemetry, incident information, labels, metadata, and any derived datasets created by the team.

Track 1 is expected to provide real telemetry including metrics, traces, and logs, together with labelled incidents. Additional resources may also be provided during the event.

This document does **not** assume any specific:

- File format
- API structure
- Schema
- Field name
- Dataset size
- Storage layout
- Identifier convention
- Telemetry backend

These details will be documented only after the official resources are inspected.

## 2. Core Principles

All data work should follow these principles:

1. Preserve the original source data.
2. Keep ground-truth answers isolated from the RCA agent during evaluation.
3. Do not treat missing data as zero.
4. Use deterministic data processing for filtering, aggregation, and calculation whenever practical.
5. Provide the agent with relevant evidence rather than unrestricted raw datasets whenever practical.
6. Keep transformations reproducible and traceable.
7. Revise data-specific assumptions after inspecting the actual event resources.

## 3. Repository Data Structure

The repository uses the following data structure:

```text
data/
├── raw/
├── processed/
└── samples/
```

### `data/raw/`

Stores original competition data locally when files must be downloaded for analysis.

Rules:

- Treat raw data as read-only.
- Do not modify source files in place.
- Do not commit raw competition data to Git by default.
- Keep original filenames and structure when practical so sources remain traceable.
- If the event provides data through an API or remote service, local copies are not required unless useful for development and permitted by the event rules.

The repository is configured so files placed in `data/raw/` are ignored by Git by default.

### `data/processed/`

Stores reproducible outputs derived from raw or remotely queried data.

Examples may include:

- Cleaned tables
- Normalized timestamps
- Joined telemetry
- Aggregated metrics
- Reconstructed trace relationships
- Derived incident windows

Rules:

- Do not overwrite raw data.
- Transformation logic should be reproducible from code or clearly documented steps.
- Derived files should retain enough identifiers to trace important evidence back to its source when possible.
- Large processed outputs should not be committed unless they are necessary and appropriate for the final repository.

### `data/samples/`

Stores small, safe examples that may be useful for testing, documentation, or reproducibility.

Rules:

- Keep samples small.
- Include only data that the event rules permit the team to publish.
- Remove or exclude evaluation-only answers when they are not required.
- Do not create samples that accidentally expose ground-truth root causes to the RCA agent.

## 4. Raw Data Integrity

Original data must remain distinguishable from team-generated outputs.

Do not:

- Edit raw telemetry manually
- Delete anomalous records because they appear inconvenient
- Fill missing values directly inside raw files
- Rename fields inside the only copy of source data
- Replace original timestamps or identifiers

If corrections or normalization are required, create a processed representation and document the transformation.

## 5. Ground Truth and Label Isolation

Labelled incidents may contain known answers used for development or evaluation.

Ground-truth information must not be exposed to the RCA agent when evaluating whether the agent can independently identify a root cause.

Potential answer-bearing information may include fields describing:

- Root cause
- Root-cause component
- Fault category
- Expected diagnosis
- Correct incident explanation

The exact answer-bearing fields will be identified after the official schema is inspected.

During evaluation:

```text
Incident Context + Allowed Telemetry
                ↓
             RCA Agent
                ↓
          Predicted RCA

Ground Truth
     ↓
Evaluation only
```

Ground truth should be used by evaluation logic, not as investigation context for the agent.

## 6. Development and Evaluation Separation

If the official resources provide an explicit development/test split, follow it.

If no split is provided, the team should define and document a separation strategy before reporting evaluation results.

Principles:

- Do not tune prompts using incidents that are being treated as final evaluation cases.
- Do not manually design incident-specific rules after inspecting evaluation answers.
- Do not expose hidden labels through tool outputs, filenames, metadata, or intermediate tables.
- Avoid placing highly similar fragments of the same incident across development and evaluation sets when such grouping can be identified.
- Document the final split strategy in the evaluation documentation.

## 7. Time, Missing Values, and Entity Integrity

Telemetry analysis depends on correct time and entity relationships.

Before using a dataset, verify when applicable:

- Timestamp format
- Timestamp unit
- Timezone
- Sampling interval
- Duplicate records
- Missing records
- Counter resets
- Entity identifiers
- Entity restarts or identifier changes
- Relationships among clusters, nodes, workloads, services, pods, traces, spans, logs, and incidents

Do not assume that a missing observation means a value of zero.

Do not compare timestamps across sources until their units and timezone interpretations are understood.

Do not merge records only because names look similar when stable identifiers or stronger relationships are available.

## 8. AI and LLM Data Access

The RCA agent should receive the minimum useful evidence needed to investigate an incident.

Prefer this pattern:

```text
Official Data / Data Store
          ↓
Deterministic Query or Processing Layer
          ↓
Filtered / Aggregated Evidence
          ↓
RCA Agent
```

Examples of deterministic processing include SQL, dataframe operations, trace reconstruction, filtering, aggregation, and statistical calculations.

Avoid using an LLM as the primary engine for operations that can be computed deterministically.

When practical:

- Restrict tool queries to relevant incident windows.
- Return structured evidence rather than entire datasets.
- Preserve record identifiers so conclusions can be traced back to evidence.
- Keep evaluation-only labels inaccessible to agent tools.
- Handle empty results explicitly rather than encouraging the model to infer missing evidence.

The exact agent-access model will be revised after the official data interfaces are known.

## 9. Publication and Repository Safety

Before committing any competition data or derived artifact, verify that it is allowed to be published.

Do not commit:

- Private credentials
- API keys or access tokens
- Restricted event resources
- Large raw competition datasets by default
- Ground-truth data when publication would violate event rules or undermine evaluation

If uncertain, keep the data local until the event rules or organizers clarify its publication status.

## 10. Event-Day Data Review

After receiving the official Track 1 resources, complete a data review before implementing the main RCA workflow.

The review should identify:

1. Every provided file, API, database, or resource.
2. Actual formats and schemas.
3. Important identifiers and relationships.
4. Timestamp formats, units, and timezones.
5. Missing-data behavior and obvious data-quality issues.
6. Ground-truth or answer-bearing fields.
7. Which fields are safe for the RCA agent to access.
8. Development and evaluation boundaries.
9. Additional telemetry or metadata not anticipated before the event.
10. Required updates to this document and related project documentation.

After the review, update this policy where necessary so the written rules reflect the actual dataset rather than pre-hackathon assumptions.
