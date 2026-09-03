# Life Patterns Neutral Codebook — Reconciliation / Pilot Milestone Receipt

Date: 2026-09-03

Status: development milestone only. No merge, deploy, recruitment, spending, validation promotion, or target-model execution is authorized.

## Preserved substantive artifacts

- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-DRAFT-v1-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-REPLICATION-DRAFT-v1-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-REPLICATION-CROSSWALK-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-RECONCILIATION-PROMPT-v1-2026-09-03.md`
- `state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-THEORY-BLIND-RECONCILED-CANDIDATE-v1-2026-09-03.md`

The reconciled candidate was produced in a theory-blind context from the two preserved source drafts. It contains 22 primary episode-level observables and explicitly moves cross-episode recurrence, context variability, temporal change, and several state-linked comparisons into metadata/derived summaries to avoid double-counting the same underlying evidence.

## Theory-leakage disposition

No obvious direct Human Design/AstroHD/astrology-specific construct leakage was identified in the first draft, minimally seeded replication, or reconciled candidate.

The initial detailed prompt was authored by a theory-exposed project context and therefore remains documented as a prompt-steering contamination risk. That risk is addressed at the development stage by the separately preserved minimally seeded replication and blind reconciliation. It is not represented as proof of zero pretraining exposure or construct validity.

## Blind human reliability protocol

Added:

- `docs/research/LIFE_PATTERNS_NEUTRAL_CODEBOOK_BLIND_PILOT_PROTOCOL.md`

The protocol requires independent pre-adjudication human coding, explicit non-action prerequisites, separate reliability reporting for segmentation/applicability/value/sequence/missingness/context/derived summaries, preserved original coder outputs, and theory-blind post-pilot revision.

## Machine-checkable contracts

Added:

- `src/hdmatch/evaluation/theory_blind_authority.py`
- `tests/unit/test_theory_blind_authority.py`
- `src/hdmatch/evaluation/pilot_reliability.py`
- `tests/unit/test_pilot_reliability.py`

The theory-blind authority contract supports human or AI substantive authorship but keeps validation promotion blocked unless required independent replication/reconciliation and blind human-human reliability evidence exist.

The pilot receipt contract content-addresses the development corpus manifest, independent first-pass freeze, and post-freeze adjudication chain.

## Policy/spec updates

Updated:

- `docs/research/LIFE_PATTERNS_THEORY_BLIND_CONTENT_AUTHORITY_POLICY.md`
- `docs/research/LIFE_PATTERNS_NEUTRAL_MEASUREMENT_BRIDGE_SPEC.md`

They now reflect the owner-approved theory-blind authorship policy, the preserved reconciliation, the blind-pilot chronology, and the generic authority/pilot receipt implementations.

## Remaining implementation mismatch

`src/hdmatch/evaluation/neutral_measurement.py` still wires `frozen_for_validation` to the legacy `HumanContentAuthorityReceipt` / H1 human-only field.

The generic theory-blind authority contract is implemented, but the core ontology gate has not yet been generalized. This must not be bypassed by fabricating a legacy human receipt for AI-authored content.

This mismatch is not currently blocking development because the reconciled codebook cannot legitimately be promoted to validation status until real blind human reliability evidence exists anyway.

## Scientific next dependency

Actual progress beyond development infrastructure requires blind human double-coding under the frozen pilot protocol. No coder recruitment/contact or spending has been authorized in this milestone.

## CI

The final CI result for the current milestone head should be recorded here once the latest workflow run completes. Earlier fully gated code milestone: `0a948cf32a72678f519bc37f9916a441bc04a85d` — 412 passed, 6 expected skips, Ruff clean, mypy clean across 137 source files.
