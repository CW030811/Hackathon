# Evaluation

The unchanged official scorer measures requested onset, component and reason fields, exact fault count, string labels and timestamp tolerance. Output-shape validity, workflow completion and diagnostic correctness are reported separately.

[REPORT.md](REPORT.md) contains current measured results and limitations. [eval/README.md](eval/README.md) provides executable planning, scoring and replay commands. The published 12346 run uses the same frozen 20 cases and order as the repair controls, includes all seven tasks, and retains all planned cases in the denominator.

Runtime never reads development labels. Offline scoring alone uses dev/query_dev.csv. Use a fresh output directory and record source/config hashes, model attempts, unknown usage, wall time, resource limits and repetitions. A single run provides no repeat variance. Comparisons across different panels or runtime versions do not establish routing savings.

Historical full-70 results belong to the pre-repair baseline. The final version has no repeated matched single-model control or hidden-deployment result. These limitations are explicit findings, not completed acceptance claims.
