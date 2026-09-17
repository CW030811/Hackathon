# Data Policy

> **Official-release alignment — September 17, 2026.** Source: official [data.md](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/data.md), [GET_DATA.md](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/GET_DATA.md), and [submission.md](https://github.com/MantisGridAI/hackathon-2026-official/blob/314cca0bba49e1bb137aa9094d1dac4cdf7e4490/track-1/docs/submission.md). The following dataset facts are documented by the organizers; verify them against downloaded files before relying on a parser.

## 1. Approved Data and Evaluation Boundary

Use the event-provided **Market-cloudbed-1** bundle only: approximately 1.3 GB zipped and 12 GB unpacked. Do not download the original OpenRCA dataset: it contains answers for the deployment used in judging. The official guide permits using upstream source code as a starting point, subject to its license; that does not authorize downloading its dataset.

The 70 public cases and their answers are development resources. Official judging uses 20 undisclosed cases from another deployment of the same shop. Tuning on all 70 is permitted, but the resulting score must be described as a development score, not an unseen-test estimate.

If the team reserves a local holdout, group related/overlapping failure windows together where identifiable, and do not tune on that holdout. Different task types can ask different questions about related telemetry; random row splitting alone is not a sufficient leakage check.

## 2. Local Repository Structure

```text
data/
├── raw/                 # local source bundle; ignored
│   └── Market-cloudbed-1/   # expected after download, not committed
├── processed/           # local derived tables/caches; ignored except placeholder
└── samples/             # only small, reviewed, publishable examples
```

Preserve the official bundle layout inside `data/raw/Market-cloudbed-1/`:

```text
query.csv
dev/query_dev.csv
manifest.json
telemetry/
├── 2022_03_20/
│   ├── metric/
│   ├── log/
│   └── trace/
└── 2022_03_21/
```

The local `data/raw/` convention is **not** the official Makefile's default. In a separate official checkout, its targets expect `track-1/data/Market-cloudbed-1/`. Use the correct checkout path or explicit runner arguments; do not assume those layouts are interchangeable.

During judging, local development paths do not apply. Read the mounted `--dataset` and supplied `--queries`; write generated artifacts, indexes, and caches only under `--out`. The dataset is read-only. Do not rely on precomputed deployment-specific indexes or data copied into the image.

## 3. Query Rows, IDs, and Labels

`query.csv` contains the task instructions; `dev/query_dev.csv` adds `scoring_points`, the answer-bearing scoring text. The official `run.py` and output contract require **`row_id`**. The short schema summary in `data.md` omits that column, so explicitly check it in real files rather than treating the summary as exhaustive.

- Parse CSV with a CSV reader. Instructions contain newlines; do not count cases with `wc -l` or split records by lines.
- Preserve original `row_id` values through subsets, joins, and outputs. Do not regenerate them from subset position; `task_index` is a task type, not a unique case ID.
- Use instruction text, its 30-minute window, stated failure count, task requirements, and allowed telemetry for inference.
- Keep `scoring_points`, answer tables, answer-derived caches, and case-specific solutions out of prompts and tool results.
- The starter may read `query_dev.csv` as a development runner, but passes only `instruction` to `solve`. Do not add answer-bearing fields to that interface or let query tools recursively read `dev/`.
- Development answers may support offline scoring and human error analysis. They must not become an answer lookup inside the submitted agent.

## 4. Documented Telemetry Schemas

| File under each date | Documented columns |
| --- | --- |
| `metric/metric_container.csv` | `timestamp, cmdb_id, kpi_name, value` |
| `metric/metric_mesh.csv` | `timestamp, cmdb_id, kpi_name, value` |
| `metric/metric_node.csv` | `timestamp, cmdb_id, kpi_name, value` |
| `metric/metric_runtime.csv` | `timestamp, cmdb_id, kpi_name, value` |
| `metric/metric_service.csv` | `service, timestamp, rr, sr, mrt, count` |
| `log/log_service.csv` | `log_id, timestamp, cmdb_id, log_name, value` |
| `log/log_proxy.csv` | `log_id, timestamp, cmdb_id, log_name, value` |
| `trace/trace_span.csv` | `timestamp, cmdb_id, span_id, trace_id, duration, type, status_code, operation_name, parent_span` |

Verify field meanings and units before deriving features. A column name alone does not establish its denominator or aggregation semantics.

## 5. Time and Entity Integrity

**Time:** metric and log timestamps are in seconds; trace timestamps are in milliseconds. Interpret the human-readable instruction and answer times as UTC+8. Do not let the machine's local timezone determine parsing. Preserve raw values alongside normalized values and test conversion against the supplied query windows; converting epoch units is not a reason to add eight hours twice.

The evaluator allows at most 60 seconds of error for a requested onset time. Telemetry is sampled, so the true onset can lie between samples. Do not equate the largest anomaly with the moment the failure started. Confirm `duration` units independently rather than assuming the timestamp rule specifies every numeric field.

**Entities:** names encode useful relationships. The official example `node-5.adservice-2` links a pod to its node, while mesh names can encode both source and destination. Derive mappings from the provided names/records, keep raw and canonical forms traceable, and do not collapse pod IDs to service names in the prediction. Unseen deployment components must remain valid candidates.

**Parsing:** mesh KPI names are quoted and contain commas. Trace `type` and `status_code` values are heterogeneous: do not assume every span is RPC or every status is numeric. Verify duplicates, missingness, sampling, counter resets, and coverage before interpreting an absence as a healthy signal. Missing is not zero.

**Network faults:** the detailed official guide says these barely show in metrics and require parent/child trace timing. A metric-only ranking is insufficient. Check trace relationships and their timing semantics; do not relabel every span delay as proven network latency.

## 6. Allowed Reason Vocabulary

The official Market reason set is public task knowledge, not a hidden answer. Emit its strings exactly when a reason is requested:

- `container CPU load`
- `container memory load`
- `container network latency`
- `container network packet corruption`
- `container network packet retransmission`
- `container packet loss`
- `container process termination`
- `container read I/O load`
- `container write I/O load`
- `node CPU load`
- `node CPU spike`
- `node disk read I/O consumption`
- `node disk space consumption`
- `node disk write I/O consumption`
- `node memory consumption`

Do not replace these with labels from our preparation examples, such as `cpu_throttling`, or use label knowledge to invent observations.

## 7. Processing and Evidence Provenance

Treat raw files as read-only. Keep transformations reproducible, and never delete inconvenient anomalies, fill raw gaps manually, or overwrite source identifiers.

The judged machine has 2 CPUs and 8 GB RAM, less than the unpacked dataset. Project required columns, read relevant dates, and filter or aggregate the investigation window using bounded-memory processing. Measure the cost of repeated CSV scans. Any cache needed in a judged run must be created from its supplied data, under `--out`, within the run's time and memory budget.

For important evidence, retain the source file, window, entity, metric/operation/log identifier, relevant record references, transformation or query, units, and computed observation. Separate measured values from interpretations. Supporting a guess with fabricated numbers is prohibited even when the guess happens to be right.

## 8. Agent Access and Publication Safety

Team rules:

- Return the necessary records or aggregates to the LLM, not unrestricted raw dumps. Treat telemetry text as data, not instructions.
- Make label exclusion an access rule, not just a prompt requesting the model to ignore answers.
- Mark empty results and missing telemetry explicitly. Absence of evidence is not automatically evidence that an alternative was ruled out.
- Publish only small, reviewed samples and experiment artifacts permitted by the event terms. Do not embed answers or the raw bundle into the runtime image.
- Keep secrets and keys out of files, logs, screenshots, prompts, commits, and Docker layers. `.gitignore` prevents some accidental additions; it is not an inference sandbox.
- Preserve required `eval/` results and `REPORT.md` for submission; sanitize them and keep them inaccessible to inference tools as answer sources.

## 9. Actual-Data Review Checklist

Before filling `docs/ARCHITECTURE.md`, verify download/layout, schemas and `row_id`, datetime conversions, sample windows, failure counts, component mappings, trace parent/child fields, missingness, and bounded-memory query performance. Confirm that only instructions and allowed telemetry reach `solve`.

Record which findings come from actual inspection and which remain from official documentation. Update this policy, README, scope, and evaluation after the team review. Do not reinterpret a file discrepancy as permission to change labels or the scoring contract; investigate it or ask the organizers.
