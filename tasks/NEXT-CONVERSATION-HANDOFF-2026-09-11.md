# Life Patterns — next-conversation handoff — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

GitHub is canonical. Before substantive work, fetch the current PR #24 head and read:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-11.md`
3. `state/LIFE-PATTERNS-V5-PRIVATE-UI-OWNER-REVIEW-CANDIDATE-2026-09-11.json`
4. `tasks/LIFE-PATTERNS-V5-OWNER-USABILITY-REVIEW-2026-09-11.md`
5. `docs/research/LIFE_PATTERNS_V5_PRIVATE_PORTABLE_ADAPTER_2026-09-11.md`
6. `state/LIFE-PATTERNS-V5-MECHANICAL-IMPLEMENTATION-VERIFIED-2026-09-11.json`
7. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
8. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-VERIFIED-2026-09-10.json`
9. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
10. `state/CURRENT-STATE.md`

## Closed gates

The blind V5 semantic/contract gate passed at independent review commit `ce04642146c41a7d5d94f85360572c78de887682`: all 47 carried findings resolved, no blocking new finding, `semantic_change_required=false`, `safe_for_implementation=true`.

The public V5 mechanical implementation passed at code head `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`, CI `34623829382`: 675 passed, 7 expected skips, Ruff clean, strict mypy clean across 174 source files.

Do not redo those gates unless new evidence demonstrates a genuine defect.

## Exact calibration source — recovered and verified

Outer transport:

- `Life-Patterns-Recurrence-Corrected-Human-Calibration-V2-PRIVATE-2026-09-08.zip`
- SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- 422297 bytes / 15 members

Inner receipt:

- `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 8 packets

All receipt-bound member and packet hashes reverified. Coverage remains 44 episode + 22 series units.

## Private V5 owner-review candidate — ready

A private owner-review candidate was generated from the exact verified transport and technically smoke-tested.

Public-safe receipt:

`state/LIFE-PATTERNS-V5-PRIVATE-UI-OWNER-REVIEW-CANDIDATE-2026-09-11.json`

Private package identity:

- filename `Life-Patterns-V5-PRIVATE-Owner-Review-2026-09-11.zip`
- SHA-256 `0ff2a6db516a9005eea2c2a91e2b19597d81d97629684958a84473e6a25da2f5`
- bytes `632723`

The package itself is private and is not committed to GitHub.

Technical smoke passed save/reload persistence, exact fallback semantics, R05-O2 separate affirmative/four-gate absence behavior, R14-i four-gate pure absence fail-closed behavior, claim-specific multi-source provenance, progress/attestation downloads, incomplete-export fail-closed behavior, zero external network requests, and zero console errors. Public-only synthetic export smoke passed for pure absence, partial hybrid, ordered two-stage/single-evidence-unit behavior, and recurrence-v2 fields.

The sandbox could not execute the canonical compressed-template builder chain because the connected GitHub files cannot be mounted locally and Git/network checkout is blocked. A portable execution adapter preserving the accepted V5 semantics was used instead. The architecture and explicit smoke limitation are documented at `docs/research/LIFE_PATTERNS_V5_PRIVATE_PORTABLE_ADAPTER_2026-09-11.md`.

## Exact next gate — owner usability review

Run/follow:

`tasks/LIFE-PATTERNS-V5-OWNER-USABILITY-REVIEW-2026-09-11.md`

The owner should review representative units in the private package and return either explicit presentation acceptance or concrete usability defects. Do not treat this as a 66-unit annotation pass.

Technical smoke does not equal owner acceptance.

## After owner presentation acceptance

Before human collection, make the accepted surface reproducible through one of:

1. promote the portable adapter implementation plus focused tests to the public repo and obtain green CI against the V5 validator; or
2. regenerate the accepted surface with `scripts/build_life_patterns_human_calibration_ui_v5_final.py` in an environment with the complete local repo/template chain and smoke that exact result.

Only after owner acceptance + green reproducibility may the independent human first pass begin. Only after that pass is complete and frozen may automated participant coding begin.

## Hard boundaries

- no private exact text or generated private UI in public GitHub;
- no human collection before owner acceptance and green reproducibility;
- no automated participant coding before the revised independent human pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy, recruitment/contact, or spending without separate authorization.
