# Evidence-backed RCA — MantisGrid AI Hackathon 2026

A Track 1 project that investigates microservice incidents from metrics, traces and logs, routes bounded reasoning across GLM models, and produces source-backed explanations.

This is a participant project repository, not the official event repository. It packages the **12346 repair configuration**: service-scope hypotheses, metric semantics, diverse bounded candidate presentation, trace/log investigation, and comparative Strong-model review. The experimental multiscale/short-reference-window change (repair 5) is excluded.

## Event and provenance

The [MantisGrid AI Hackathon](https://github.com/MantisGridAI/hackathon-2026-official) took place in Palo Alto on September 17, 2026, 9:30am–3:00pm PDT. Track 1 asks “Why did this break?”; Track 2 addresses cluster efficiency. This project implements Track 1 only. See [event overview](docs/HACKATHON.md), [participant agreement](PARTICIPANT_AGREEMENT.md), and [source provenance](docs/PROVENANCE.md).

## Measured results

Same frozen 20 development cases, all seven task types, one run per version:

| Repairs | Partial | Fully solved | End-to-end time |
|---|---:|---:|---:|
| 1–4 | 37.50% | 4/20 | 556.7 s |
| 1–6 | 39.20% | 3/20 | 605.2 s |
| **1,2,3,4,6 (this runtime)** | **40.85%** | **4/20** | **584.9 s** |

All 20 answers returned under Docker-enforced 2 CPU / 8 GiB limits. Known token cost was $0.21966327; one request has unknown usage, so this is not total billing. **198 tests passed**, including real telemetry checks. These are public-development measurements, not hidden-test results, production-readiness proof or a statistically established improvement. The final version has not been rerun on all 70 cases. [Full report](REPORT.md) · [recorded results](eval/results/repair-ablation/README.md).

## Run the agent

Requirements: Docker-compatible engine; the [official development bundle](track-1/GET_DATA.md); a Featherless key for model calls. No raw dataset or key is included.

```bash
docker build -t mantis-rca .
# Export FEATHERLESS_API_KEY securely in your shell first.
mkdir -p out/my-run
docker run --rm --cpus 2 --memory 8g --memory-swap 8g \
  -e FEATHERLESS_API_KEY -e FEATHERLESS_BASE_URL \
  -v /absolute/path/Market-cloudbed-1:/data:ro \
  -v "$PWD/out/my-run":/out \
  mantis-rca python run.py --dataset /data --queries /data/query.csv --out /out
```

Set FEATHERLESS_BASE_URL only when an alternate endpoint is supplied. The default agent needs no --agent argument. Use a fresh output directory for each run. For a one-case live demo, append --limit 1. For offline best-guess mode, add -e RCA_MODE=deterministic to docker run.

Outputs: predictions.csv, evidence/&lt;row_id&gt;.md, usage.jsonl, and diagnostic provenance under --out. Missing telemetry and model failures remain explicit; valid formatting does not mean a correct diagnosis.

## Demo and architecture

- [Demo guide](DEMO.md): live CLI walkthrough and offline recorded Evidence Room.
- [Recorded interactive demo](demo/evidence-room/index.html): download/open locally; no key or API call. It replays an **older** measured 20-case run, including case 9, not this final version.
- [Architecture](docs/ARCHITECTURE.md): data → metrics/traces/logs → candidate ranking → Flash/Strong → validated evidence.
- [Evaluation harness](eval/README.md): unchanged official scorer, source/config manifests and matched comparisons.

## Development and tests

Python 3.12 with uv:

```bash
uv venv --python 3.12
uv pip install -r track-1/starter/requirements.txt
cd track-1/starter
../../.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Set RCA_TEST_DATA to the absolute official bundle path to include the five real-telemetry checks; otherwise they explicitly skip. Tests do not require paid model calls.

## AI usage and ownership

OpenAI Codex and delegated coding agents generated and revised the RCA modules, tests, evaluation tooling, documentation and demo under human direction. Human contributions included project requirements, hypothesis prioritization, experiment choices and review. Saved development records identify a GPT-6-family assistant but do not establish every exact model variant or assistant cost.

Runtime calls use Featherless GLM-5.3-Flash / GLM-4.7-Flash and GLM-5.1 / GLM-5.2; no external agent framework is used. The organizer starter supplies interfaces, baseline utilities and the unchanged official accuracy evaluator. Team implementation came through [catou88's repository](https://github.com/catou88/hackathon-2026-official); it is not claimed as solely authored by this repository owner.

[Original terms](LICENSE) and [data attribution](ATTRIBUTION.md) are preserved. No new blanket open-source license is asserted. This publication is a project archive; it does not establish acceptance by the event or completion of its submission form.
