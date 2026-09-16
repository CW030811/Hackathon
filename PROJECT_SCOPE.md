# Project Scope

> **Pre-hackathon scope:** This document reflects information publicly available before the event. Data-dependent assumptions and implementation details may be revised after the official hackathon resources are released and inspected.

## 1. Objective

Build an evidence-driven Root Cause Analysis (RCA) agent that investigates distributed-system incidents using available telemetry, including metrics, traces, and logs, and returns the most supported root-cause hypothesis with supporting evidence.

The system should favor evidence-backed conclusions over unsupported certainty and should explicitly communicate uncertainty when the available data is insufficient.

## 2. Core Problem

In distributed systems, the component where an error appears may not be the component that originally caused the incident.

A failure can propagate across multiple services and infrastructure layers, producing downstream latency, retries, timeouts, resource pressure, and user-facing errors. Effective RCA therefore requires correlating signals across time, system entities, and request dependencies.

The project focuses on distinguishing among:

- **Root cause** — the underlying failure that initiated or primarily drove the incident
- **Failure propagation** — how the failure affected dependent components
- **Symptoms** — observable consequences such as elevated latency, errors, retries, or timeouts

## 3. Primary User Scenario

A user selects or provides an incident for investigation.

The system should then:

1. Inspect telemetry around the incident window.
2. Identify abnormal signals and suspicious components.
3. Generate one or more root-cause hypotheses.
4. Collect additional evidence relevant to those hypotheses.
5. Validate, weaken, or reject hypotheses based on the available evidence.
6. Produce an RCA report that explains the most supported conclusion and any remaining uncertainty.

Conceptually:

```text
Incident
   ↓
Investigation
   ↓
Evidence
   ↓
Root-Cause Hypotheses
   ↓
Validation
   ↓
RCA Report
```

## 4. In Scope

### Incident Investigation

- Investigating a known incident or incident time window
- Comparing behavior before, during, and when useful after the incident
- Narrowing the investigation from broad anomalies to specific suspicious entities

### Telemetry Analysis

- Metrics analysis
- Trace analysis
- Log analysis
- Correlation across timestamps and system entities
- Use of additional event-provided metadata when it is relevant to RCA

### Root Cause Reasoning

- Identifying suspicious components
- Generating root-cause hypotheses
- Comparing competing explanations
- Validating hypotheses against available telemetry
- Distinguishing root causes from propagated symptoms
- Avoiding causal claims that are not supported by evidence

### Evidence Handling

- Linking conclusions to supporting telemetry records or derived results
- Constructing an incident timeline when the data supports it
- Preserving enough provenance for conclusions to be inspected or reproduced
- Reporting uncertainty and missing evidence when necessary

### Evaluation

- Comparing RCA outputs against labeled incidents when permitted by the event data
- Evaluating root-cause identification separately from component localization when appropriate
- Measuring diagnosis quality together with practical factors such as latency, model usage, tool usage, and cost
- Keeping evaluation labels isolated from the RCA agent during testing

## 5. Out of Scope

The following are not primary project objectives unless official event requirements or the provided data materially change the scope.

### Autonomous Remediation

- Automatically restarting pods or services
- Changing resource requests or limits
- Scaling workloads
- Modifying production infrastructure
- Applying configuration changes without human review

### Incident Prediction

- Predicting future incidents as a primary objective
- Building a continuous anomaly-detection or alerting platform as the main deliverable

The project focuses on diagnosing incidents rather than independently detecting or predicting them unless the official Track 1 workflow requires otherwise.

### Full Observability Platform

- Replacing Prometheus, Grafana, Datadog, or similar monitoring systems
- Building a complete general-purpose telemetry platform
- Reproducing every monitoring or visualization capability available in existing observability products

### Foundation Model Training

- Training a foundation model from scratch
- Fine-tuning a foundation model as a core requirement

Model training or fine-tuning may be reconsidered only if the official resources and time constraints provide a strong reason to do so.

### Unsupported Causal Claims

The system should not infer causes that cannot be supported by the provided evidence.

For example, telemetry may support a conclusion that CPU throttling preceded latency degradation, but without configuration or deployment evidence the system should not claim that a particular deployment changed a CPU limit.

## 6. Expected Investigation Capabilities

The RCA system should aim to answer the following questions.

### What changed?

Identify abnormal telemetry or notable changes around the incident window.

### Where did it happen?

Identify suspicious services, workloads, pods, nodes, dependencies, or other entities when those entities are represented in the provided data.

### How did the failure propagate?

Use timestamps, traces, dependencies, and other available evidence to explain how the incident affected downstream or upstream components.

### Why is this the most likely root cause?

Provide evidence that supports the leading hypothesis and, where useful, evidence that weakens competing hypotheses.

### What remains uncertain?

Identify missing evidence, unresolved ambiguity, and reasonable alternative explanations when the data does not support a definitive conclusion.

## 7. Definition of a Successful RCA

A successful RCA should provide, when supported by the available data:

1. A clearly identified suspected root cause.
2. The affected component or entity at an appropriate level of granularity.
3. Supporting evidence from available telemetry or metadata.
4. A coherent incident timeline or causal sequence.
5. A distinction between the likely root cause and downstream symptoms.
6. Explicit uncertainty when evidence is incomplete or conflicting.

A successful result should be inspectable and evidence-backed rather than only a free-form model explanation.

## 8. Data-Dependent Assumptions

Track 1 is expected to provide real telemetry including metrics, traces, and logs, together with labeled incidents.

Exact schemas, file formats, identifiers, dataset sizes, timestamp conventions, available metadata, data-access mechanisms, and relationships between data sources are **not assumed in advance**.

Additional resources may include system metadata, workload information, configuration data, dependency information, event records, or other telemetry-related inputs. If such resources are provided, they may be incorporated into the RCA workflow when they improve evidence quality or diagnosis accuracy.

After the official event resources are released, the team should review and update this section based on the actual data before committing to implementation details.

## 9. Scope Priorities

When time is limited, development should prioritize:

1. Correctly reading and understanding the provided data.
2. Completing one end-to-end RCA workflow.
3. Producing conclusions that are directly supported by evidence.
4. Evaluating the workflow across multiple incidents rather than demonstrating only one successful case.
5. Improving usability and presentation after the core workflow is reliable.
6. Adding optional features only after the primary RCA workflow works end to end.

The project should prefer a smaller, testable, evidence-backed system over a broader system with incomplete diagnosis logic.
