# Historical RCA Evidence Room

Open index.html locally; Chart.js and recorded run data are embedded. No API key or model call is required. This replays an earlier 20-case run: 0.346 partial, 5/20 fully solved, 608.960 seconds. It is **not** a replay of the final repairs 12346.

The builder validates the historical runtime and verification-summary artifacts before embedding structured events, bounded evidence excerpts and human-readable evidence. To regenerate, provide the original local run and matching historical team checkout:

```bash
python build_demo.py --run /path/to/recorded-run --repo /path/to/matching-historical-checkout
```

Those full local ledgers are not distributed. The frozen source runtime was 97c759682d72832d4f008fdf13b1d1c4f218f03e; the historical submission snapshot was d5142782de9b841651ab2ae2fcfa83c3a7170925 in the team repository.

See the root DEMO.md for the walkthrough and REPORT.md for the current runtime results. Chart.js retains its embedded MIT license notice.
