# Life Patterns current state — 2026-09-11

Status: public-safe controlling overlay for `codex/discover-life-patterns-mvp`, draft PR #24.

## Current gate

The blind V5 semantic/contract gate and the public mechanical implementation gate have passed. The exact previously frozen calibration transport has now also been recovered and fully reverified.

A V5 owner-review candidate has been generated and technically smoke-tested. **The next action is owner usability review. Human collection remains unauthorized.**

## Accepted public V5 implementation

- record-containment repair: `320cb577f4adfbcc644c986f7f532feef0fbe80b`
- independent blind V5 review: `ce04642146c41a7d5d94f85360572c78de887682`
- all 47 carried findings resolved
- `semantic_change_required=false`
- implementation head: `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`
- CI `34623829382`: SUCCESS
- 675 passed, 7 expected skips, 0 failed
- Ruff clean
- strict mypy clean across 174 source files

Public verification receipt:

`state/LIFE-PATTERNS-V5-MECHANICAL-IMPLEMENTATION-VERIFIED-2026-09-11.json`

## Recovered calibration source identity

Outer transport:

- filename `Life-Patterns-Recurrence-Corrected-Human-Calibration-V2-PRIVATE-2026-09-08.zip`
- SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- 422297 bytes
- 15 members

Inner receipt:

- id `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 8 packets

All receipt-declared member hashes and packet content addresses reverified. Selected coverage remains exactly 44 episode + 22 series = 66 units. The outer and inner hashes identify different objects.

## V5 owner-review candidate

Public-safe receipt:

`state/LIFE-PATTERNS-V5-PRIVATE-UI-OWNER-REVIEW-CANDIDATE-2026-09-11.json`

Candidate identities:

- HTML SHA-256 `e0fd7e90fdb923cc03ec16e41470689267bb0a537a9ea2f9e59beb25eb3ebd27`
- HTML bytes `1607323`
- owner-review ZIP SHA-256 `0ff2a6db516a9005eea2c2a91e2b19597d81d97629684958a84473e6a25da2f5`
- ZIP bytes `632723`

The sandbox could not execute the canonical builder chain because the connected repository template chain could not be mounted locally and Git/network checkout is blocked. A portable execution adapter was therefore used while preserving the accepted V5 facet, hybrid/absence, stage, provenance, recurrence, and envelope semantics.

Architecture and limitation record:

`docs/research/LIFE_PATTERNS_V5_PRIVATE_PORTABLE_ADAPTER_2026-09-11.md`

Technical smoke passed for save/reload persistence, exact fallback semantics, R05-O2 separate affirmative plus four-part absence controls, R14-i four-part absence fail-closed behavior, claim-specific multi-source provenance, backup and attestation downloads, incomplete-export fail-closed behavior, zero external network requests, and zero console errors. Public-only synthetic export smoke also passed for pure absence, partial hybrid, ordered multi-stage/single-evidence-unit behavior, and recurrence-v2 fields.

Managed Chromium in this sandbox blocks normal local navigation, so DOM/interactions were exercised in-memory after the outer transport was independently cryptographically verified. This limitation is recorded in the receipt.

## Exact next action

Owner should review:

`Life-Patterns-V5-PRIVATE-Owner-Review-2026-09-11.zip`

If the owner accepts the UI, preserve the explicit acceptance and then make the accepted surface reproducible before human collection by either:

1. promoting/testing the portable adapter in the public repo with green CI; or
2. regenerating the accepted surface with `scripts/build_life_patterns_human_calibration_ui_v5_final.py` in an environment with a full local repo/template checkout.

Technical smoke does not equal owner acceptance.

## Hard boundaries

- no independent human collection before owner acceptance plus a green reproducible generation path;
- no automated participant coding before the revised independent human first pass is completed and frozen;
- no target-model scoring/reveal;
- generated private review files are not committed to the public repo;
- no merge/deploy, recruitment/contact, or spending without separate authorization.
