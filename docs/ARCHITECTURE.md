# Architecture

The sole agent runtime lives in track-1/starter. The root Dockerfile copies it to /app; evaluation artifacts and demo content stay outside the runtime image.

```text
run.py: instruction + dataset
  → M1: UTC+8 case parsing, bounded telemetry access, runtime budgets
  → M2 metrics/onset + M3 traces/network/logs
  → M4: merge hypotheses, diversify candidates, one targeted follow-up
      → Flash → comparative Strong review when warranted
  → M5: validate requested fields, render factual evidence
  → predictions.csv + evidence/<row_id>.md + usage.jsonl

offline outputs + development labels → eval/ → scores and audit
```

M1 provides shared contracts and provenance-preserving data access. M2 constructs resource/onset hypotheses from observations rather than answer labels. M3 supplies independent trace competitors and targeted log comparisons. M4 owns ranking, presentation limits and GLM decisions. M5 checks field/count/reference consistency and renders measured evidence; it does not turn an uncertain hypothesis into a proven cause.

Runtime soft limits are 55 seconds per case, 1140 seconds per run, at most one follow-up, two model stages and four HTTP attempts per case. Service alternatives require observed cross-node replica support. Partial/missing coverage remains unknown. Prior model choices are advice, not measurements.

Detailed contracts: [INTERFACES.md](INTERFACES.md). Module specifications and historical ownership: [TEAM.md](../TEAM.md). Measured behavior and limitations: [REPORT.md](../REPORT.md).
