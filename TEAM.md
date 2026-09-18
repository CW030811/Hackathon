# Team implementation and module map

The project is a five-module Track 1 RCA agent. The shared team implementation originated in [catou88/hackathon-2026-official](https://github.com/catou88/hackathon-2026-official); this repository publishes the final 12346 snapshot with attribution. Individual contributor identities are not inferred from coding-agent roles.

| Module | Responsibility | Runtime files under track-1/starter |
|---|---|---|
| M1 | Contracts, telemetry access, UTC+8 parsing, budgets and integration | agents/rca/contracts.py, data_access.py, runtime.py; run.py |
| M2 | Metric semantics, resource hypotheses, onset and replay | agents/rca/metrics.py, onset.py |
| M3 | Traces, dependencies, network hints, targeted logs and replay | agents/rca/traces.py, network.py, logs.py |
| M4 | Candidate ranking, follow-up, bounded GLM routing and comparative review | agents/routed.py; agents/rca/controller.py, ranking.py, prompts.py, routing.py; llm.py |
| M5 | Requested-field validation, factual evidence, offline scoring | agents/rca/validation.py, evidence.py; root eval/ |

[Module specifications](docs/modules/README.md) · [shared interfaces](docs/INTERFACES.md) · [architecture](docs/ARCHITECTURE.md) · [measured report](REPORT.md).

Development used Codex and delegated agents under human direction. Runtime inference is separate and uses the allowed GLM family. For changes, coordinate shared contracts, keep the runtime in its existing directory, preserve the scorer, and test module boundaries. No raw data or secrets belong in version control.
