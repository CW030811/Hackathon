# Fixed-panel repair experiments

Six configurations, each measured once on the same 20 public-development cases covering all seven task types. benchmark.json preserves the selection seed, quotas, original IDs and instructions. This is not a held-out benchmark.

Directories: baseline; fix12 (repairs 1,2); fix34 (1–4); fix5 (1–5); fix6 (1–6); fix12346 (published runtime).

Each directory includes an audit, frozen manifest/source hashes, predictions, per-case usage, external execution and resource measurements. Local paths are redacted and failed-scoring-point label text omitted from public JSON exports. Raw telemetry, full evidence ledgers, keys and caches are excluded. The final run additionally includes tests, routes and three example human-readable evidence files.

The final runtime must match fix12346/runtime-source-hashes.json. Other configurations are historical experiments, not runtime modes selected by flags. [Root report](../../../REPORT.md) explains the comparison and its limitations.

To reproduce a new matched experiment with the final runtime, follow ../../README.md and use these exact row IDs with a fresh output directory. Building another repair variant requires its historical source snapshot; compact result exports do not reconstruct those versions.
