# MantisGrid AI Hackathon 2026

## Event

Organized by MantisGrid AI Inc., September 17, 2026, 9:30am–3:00pm PDT, in person in Palo Alto, California. Teams could have up to five members.

Official sources: [repository](https://github.com/MantisGridAI/hackathon-2026-official), [participant agreement](../PARTICIPANT_AGREEMENT.md), [Track 1 brief](../track-1/README.md), [submission guide](../track-1/docs/submission.md). The preserved agreement governs event rules; this page is a project-oriented summary.

## The two tracks

- **Track 1 — Root cause analysis:** an unattended agent, an evaluation harness and source-backed explanations of microservice failures.
- **Track 2 — Cluster efficiency:** analysis and visualization of resource waste and GPU-spend opportunities. This project does not implement Track 2.

## This project's task

The provided OpenRCA-derived Market-cloudbed-1 development bundle contains metrics, traces and logs, plus 70 public-development questions. Each question specifies an incident window and fault count. Seven task types request different combinations of onset time, component and reason. Judging uses a separate deployment with 20 undisclosed cases; public-development accuracy is not the official test score.

The runtime routes within the permitted GLM family on Featherless. The required Docker interface is python run.py --dataset /data --queries /data/query.csv --out /out. Limits are 2 CPUs /8 GB, 10 minutes/$3 per case, and 20 minutes/$25 for the judged run. Missing and uncertain data must be disclosed without withholding a best-guess answer.

The event requested an English public repository and a roughly four-minute working presentation through its submission form, before September 17 at 3pm PDT. This repository publication does not assert that a form was submitted, that this snapshot was accepted, or that later repairs were judged.

## Sources, data and rights

The repository builds on the official starter and team implementation, with [AI/source disclosure](PROVENANCE.md). Raw telemetry is intentionally absent; use the [official bundle instructions](../track-1/GET_DATA.md), not the full upstream OpenRCA dataset. Original [license terms](../LICENSE) and [dataset attribution](../ATTRIBUTION.md) are preserved.
