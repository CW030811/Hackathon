## What changed?

Briefly describe the change.

## Why?

Explain the requirement or issue addressed.

## How was it verified?

Give commands/results or documentation checks. Mark runtime checks not applicable for docs-only changes. For experiments, identify configuration, case set, output directory, and measured versus estimated results.

## Affected Areas

- [ ] Telemetry queries / preprocessing
- [ ] Traces / logs
- [ ] Agent / model routing / fallback
- [ ] Predictions / evidence
- [ ] Evaluation / cost / runtime
- [ ] Docker / submission interface
- [ ] Documentation / presentation
- [ ] Other

## Checklist

- [ ] The change is focused and shared-interface changes were communicated.
- [ ] No secrets, unauthorized data, or inference-time answer leakage are included.
- [ ] Relevant documentation is updated; results are not fabricated.
- [ ] Applicable official CLI, key order, failure count, original row ID, and evidence-format checks pass.
- [ ] Applicable endpoint, budget, and resource constraints were checked.
- [ ] Verification distinguishes our implementation from the untouched starter; the final default-agent behavior is preserved where relevant.
