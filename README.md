# MantisGrid Hackathon — Root Cause Analysis Agent

An evidence-driven AI agent for diagnosing root causes of distributed-system incidents using metrics, logs, and traces.

## Overview

This repository contains our team's project for the **MantisGrid AI Hackathon 2026**.

We are participating in **Track 1: Root Cause Analysis**. The project explores how an AI agent can investigate incidents across distributed systems by correlating metrics, traces, and logs, forming root-cause hypotheses, validating them against telemetry, and producing an evidence-backed RCA report.

## Hackathon & Track

**Event:** MantisGrid AI Hackathon 2026  
**Date:** September 17, 2026  
**Track:** Track 1 — Root Cause Analysis

Track 1 focuses on determining why incidents occur by analyzing telemetry from distributed systems.

Official event page: https://mantisgrid-ai-hackathon-2026.devpost.com/

## Problem

In a distributed system, the component where an error appears is not necessarily the component that caused the incident.

A downstream resource bottleneck may increase latency, which can trigger upstream timeouts and eventually cause user-facing failures. Effective root cause analysis therefore requires correlating signals across system entities, telemetry types, time, and request dependencies.

The investigation may involve:

- **Metrics** — identify when and where abnormal behavior begins.
- **Traces** — localize slow or failed request paths across services.
- **Logs** — identify concrete failure evidence such as timeouts, OOM events, retries, or connection failures.

The goal is not only to identify a plausible cause, but to support the conclusion with traceable evidence.

## Project Goal

Our goal is to build an RCA agent that can:

1. Inspect telemetry around an incident.
2. Identify suspicious components and abnormal signals.
3. Generate root-cause hypotheses.
4. Query additional evidence to validate or reject those hypotheses.
5. Return a root-cause assessment with supporting evidence and explicit uncertainty.

The agent should distinguish between the **root cause**, the **propagation path**, and the **observed symptoms** rather than treating the first visible error as the cause.

## Planned RCA Workflow

```text
Incident
   │
   ▼
RCA Agent
   │
   ├── Metrics Analysis
   ├── Trace Analysis
   └── Log Analysis
          │
          ▼
   Evidence Collection
          │
          ▼
   Hypothesis Validation
          │
          ▼
      RCA Report
```

The intended investigation workflow is:

1. Start from an incident and its investigation window.
2. Inspect telemetry for abnormal signals and suspicious components.
3. Use traces to localize slow or failed request paths.
4. Use logs to verify concrete failure mechanisms.
5. Correlate evidence by time, component, and request dependency.
6. Validate competing hypotheses using additional telemetry when necessary.
7. Produce the most strongly supported root-cause assessment without claiming more than the available evidence supports.

## Expected Inputs and Outputs

_To be completed once the official hackathon data, schemas, and resources are released._

## Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) — collaboration, branching, commit, pull request, data-handling, and repository contribution rules.

Additional documentation will be linked here as it is created.

## Contributing

Team members should follow the collaboration and repository conventions defined in [CONTRIBUTING.md](CONTRIBUTING.md).

## AI Usage Disclosure
