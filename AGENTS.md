# Repository guidance

The sole runtime is track-1/starter. Read docs/INTERFACES.md and the affected module specification before runtime changes. Preserve the official CLI and unchanged scorer. Keep development labels exclusively in offline evaluation. Never commit credentials, raw telemetry, full caches or model private reasoning.

The published configuration is repairs 1,2,3,4,6; repair 5 is excluded. REPORT.md distinguishes the final fixed-panel run from historical 70-case and demo results. Do not update measured numbers without a new isolated experiment. Run relevant tests, including real checks when RCA_TEST_DATA is available. Do not launch paid model calls solely for documentation verification.

Preserve source attribution, original terms and existing work. Commit/push only when explicitly requested. Do not publish the unrelated agentstest implementation.
