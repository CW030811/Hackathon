# Source and experiment provenance

This participant repository is maintained at https://github.com/CW030811/Hackathon. It is not the official organizer repository and does not claim sole authorship of the team's work.

- Organizer: https://github.com/MantisGridAI/hackathon-2026-official.
- Team development repository: https://github.com/catou88/hackathon-2026-official.
- Pre-repair source baseline: 0aba33114b3bc4f9d315dfde905ef4c88b04bc28 in the team repository.
- Published runtime: the frozen repairs 1,2,3,4 snapshot plus the exact repair-6 controller/prompt/routing delta. Repair 5 is excluded.
- Measured image ID: sha256:4a5e7031b17a5e192707fd461dad0c33ba75d6642fb6ca522c055b0730c7bad7.
- Per-file runtime SHA256: [runtime-source-hashes.json](../eval/results/repair-ablation/fix12346/runtime-source-hashes.json).

The team source snapshot is imported without rewriting this repository's existing history. Older experiments retain their original source hashes and must not be represented as runs of this final runtime. Local filesystem paths are redacted in the newly exported manifests; source hashes, scores, configuration, original IDs and usage are preserved. Raw ledgers and development answer files are excluded.

OpenAI Codex and delegated coding agents performed implementation, tests, debugging, experiment tooling, documentation and demo construction under human direction. Human direction included task scope, diagnostic hypotheses, experiment selection and review. The saved records describe a GPT-6-family coding assistant but do not establish all exact variants or assistant-token costs. Runtime inference uses only the documented GLM models and has separate usage accounting.

Original organizer terms remain in LICENSE and PARTICIPANT_AGREEMENT.md. Team additions are not represented as organizer-authored or as solely authored by this repository owner. No blanket replacement license is added.
