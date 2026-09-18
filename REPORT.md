# Evidence-backed RCA: final repair configuration

## Outcome

The published runtime is repairs **1,2,3,4,6**, excluding repair 5's multiscale trace windows and short-reference metric windows. On the fixed seven-task public-development panel it returned 20/20 answers, scored **0.4085 mean partial**, and fully solved **4/20** in **584.9 seconds**. This is the highest observed partial score in the single-run repair series, not a reliable estimate of superiority or hidden-deployment performance.

## Controlled repair series

All rows below use the same case IDs/order, official scorer, 2 CPU / 8 GiB Docker limits, 55-second case /1140-second run soft budgets, at most one follow-up and two model stages. Source changes are intentional. OS cache and model variation are uncontrolled.

| Configuration | Partial | Fully solved | Seconds | Known USD |
|---|---:|---:|---:|---:|
| Baseline | 0.3085 | 3/20 | 447.1 | 0.122504 |
| Repairs 1,2 | 0.3085 | 3/20 | 444.0 | 0.105224 |
| Repairs 1,2,3,4 | 0.3750 | 4/20 | 556.7 | 0.199689 |
| Repairs 1,2,3,4,5 | 0.2500 | 2/20 | 595.2 | 0.244436 |
| Repairs 1,2,3,4,5,6 | 0.3920 | 3/20 | 605.2 | 0.243741 |
| **Repairs 1,2,3,4,6** | **0.4085** | **4/20** | **584.9** | **0.219663** |

Costs are frozen official-price estimates from reported tokens. The last four configurations each have unknown request usage; their known costs are lower bounds, not complete bills. Artifact manifests record source hashes and runtime configuration. [Results](eval/results/repair-ablation/README.md).

Panel IDs: 3,4,5,10,11,12,13,19,22,26,32,33,34,38,40,42,46,51,57,68. Task 4 has two cases, each other task has three. Selection used task-stratified SHA256 ordering with seed rca-staged-repair-v1, unique instruction windows, and no labels/prior scores. The same panel was subsequently used to compare/select repairs; it is development data, not a holdout.

## What the repairs do

1. Build observed service scopes and cross-node replica alternatives; retain node/pod candidates and avoid duplicate episodes.
2. Correct near-zero CPU noise handling and metric-family/direction semantics; preserve replay parameters.
3. Present diverse source/mechanism/scope candidates with compact factual evidence and a 32,000-byte prompt cap; record shortlist versus presentation pruning separately.
4. Consider independent trace competitors during targeted follow-up; compare log matches against reference periods and preserve source locations.
5. Experimental multiscale trace / short metric reference windows: **excluded from the published runtime** after mixed development results.
6. Strong receives Flash choices and unresolved questions for comparative review. Prior choices remain visible but are advice, not facts. Unknown network subtype alone is not grounds for repeated model escalation.

Compared with 123456, 12346 restored case 40 from 0 to 1, but case 26 fell from 0.67 to 0; other scores were unchanged. Case 26's Flash and Strong requests both returned valid selections, taking about 8.55 and 5.47 seconds, and chose the same incorrect candidate. Its regression was not a request timeout. Case 40's score is correct while its evidence validation remains degraded: accuracy and evidence sufficiency are distinct.

Compared with 1234, cases 10/13 improved and case 26 regressed. The +1.65 percentage-point gain over 123456 comes from only two changing cases and should not be treated as statistically established.

## Execution, evidence and limitations

Final run: 39 HTTP attempts, 34 valid responses, two empty responses, two invalid duplicate-episode responses and one request deadline failure. No telemetry tool interruptions were recorded. All 15 actual comparative Strong reviews retained Flash candidate IDs in their input; that is not proof the final choices were correct. Reported known cost is $0.21966327, with incomplete usage.

Peak Python-child RSS was 513,736,704 bytes; container cgroup peak including cache was 3,715,919,872 bytes, below its 8 GiB limit. All 198 tests passed, including five real-data checks. The runtime source hashes match the frozen measured image. Prior evidence replay checks sampled transforms and locators, not every aggregate or causal claim.

Logs were actually queried in the repair experiments, but the chosen literal patterns often had no hits. This does not prove that all logs were healthy or adequately modeled. Trace dependence is not causality; network subtypes, correlated resource signals, onset precision and candidate ranking remain major weaknesses. Case 26 is a priority for further candidate-recall/presentation/selection diagnosis.

## Historical 70-case and model comparisons

The pre-repair baseline (0aba331) completed all 70 public cases in four independent batches (20/20/20/10): partial 0.306, 10/70 fully solved, 1,633.1 seconds summed external batch time, and $0.4351014 known token cost with incomplete pricing. This is **not the final 12346 version**, and the batches reset runtime state/budgets. [Baseline artifacts](eval/results/baseline-full70/summary.json).

A historical two-case same-agent single-model/routed experiment exists in [the earlier report](docs/history/REPORT-pre-ablation.md). Empty routed responses and the tiny sample prevent a routing-benefit claim. There is no repeated matched single-model comparison for the final runtime, no variance estimate, no final 70-case rerun, and no hidden-deployment result.

## Reproducibility and disclosure

Use eval/run_comparison.py for frozen, label-free inference plans and offline scoring; see eval/README.md. Runtime reads whitelisted telemetry, never development answer fields. The Docker image copies only track-1/starter; reports, public predictions and historical demo outputs are not agent inputs.

The publication preserves this repository's own history and imports a reviewed team-source snapshot, not upstream Git history. No raw data, keys, full ledgers or agentstest alternative are included. Official terms and team/AI provenance are documented in README.md and docs/PROVENANCE.md.
