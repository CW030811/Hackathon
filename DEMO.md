# Four-minute demo

## Offline recorded Evidence Room

Open demo/evidence-room/index.html locally, or serve this repository with:

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Then visit http://127.0.0.1:8765/demo/evidence-room/. No API key is needed. Replay does not run the agent or call a model.

**This is a historical run**, not the current 12346 runtime. Its dashboard correctly retains its original 0.346 partial /5-of-20 strict statistics and cases 9,0,60. Do not substitute the final 0.4085 score into that old replay.

1. 0:00–0:30: explain incident questions, telemetry and GLM routing.
2. 0:30–1:40: replay case 9. Discuss requested fields, source-backed observations and uncertainty; reveal the development score only after the investigation.
3. 1:40–2:30: compare wrong-answer case 0 and timeout case 60. A correct output can still have an incomplete model workflow.
4. 2:30–4:00: show the **current** REPORT.md repair table, case 40 recovery and case 26 regression. Explain the different historical demo panel and current fixed panel, unknown usage and lack of repeat variance.

demo/rca-investigation is an older illustrative UI concept, not an actual evaluation trace.

## Live current runtime

Build the root Dockerfile, obtain the official bundle and securely export the model key. Follow README.md's docker command with --limit 1 and a new output directory. Inspect predictions.csv, the matching evidence/<row_id>.md and usage.jsonl. Explain Answer, Confidence, Evidence and Ruled out, distinguishing observation from hypothesis.

Live inference makes real paid requests unless RCA_MODE=deterministic. Recorded replay is the no-cost presentation option. This guide is not a presentation recording or proof that the activity submission form was completed.
