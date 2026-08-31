# Pro meta-review ruling: owner-source acquisition independence

Date: 2026-08-30

## Identity and verdict

- Feedback: `SDF-20260830-OWNER-SOURCE-INDEPENDENCE-001`.
- Shared lane: `supervision-architecture/20260830-90a230e`.
- Conversation: `https://chatgpt.com/c/6a937aa4-1db8-83ea-813a-350bbab44ddf`.
- Reviewed architecture commit/tree:
  `90a230e85f78063080dc627ec36a0237c3234f72` /
  `c841043cc96cd274872e8a7363651625705edf38`.
- Verdict: `ACCEPT_WITH_REVISION`.
- Owner decision required: `NO`.
- Current task boundary blocked: `NO`.
- AstroHD task authorized by this meta-review: `NO`.
- Universal architecture mutated by this read-only review: `NO`.

The Pro reviewer resolved the ambiguity as acquisition provenance rather than byte integrity. It
accepted the packet-bound bootstrap and companion SHA-256 values as reported identities but did
not claim to have independently recomputed those three hashes.

## Controlling ruling for this worker

A deterministic hash over exact owner text copied by the same worker verifies the preserved
bytes, not independent acquisition, completeness, provider origin, or inclusion of every owner
correction. The current receipt is therefore classified as:

```text
contract_to_captured_source_alignment: MATCH
owner_source_capture_integrity: VERIFIED
owner_source_acquisition_mode: WORKER_COPIED
owner_source_receipt_capability: INTEGRITY_ONLY
owner_source_receipt_comparison: NOT_INDEPENDENT
contract_to_owner_alignment: PARTIAL
completion_claim_type: WORKING
root_terminalization_allowed: false
release_permission: false
```

The worker may continue safe, reversible, in-scope contributing work while preserving these
limits. This ruling does not validate S6, H1, the AstroHD scientific design, authors, privacy
controls, or any other task-specific decision.

It may not authorize or claim `READY_FOR_RELEASE`, `OWNER_OUTCOME_ACHIEVED`, root completion,
publication, deployment, migration, release, irreversible mutation, or equivalent terminal
acceptance.

## Terminal and release-adjacent source gate

Before any root completion, release, publication, deployment, migration, or irreversible action,
the source capability must be either `INDEPENDENT_SOURCE_VERIFIED` or `OWNER_REATTESTED`, the
owner-source epoch/hash and all material corrections must be current, and contract-to-owner must
be `MATCH`. Every other applicable outcome, evidence, scientific, privacy, safety, and release
gate must also pass independently.

An independent direct observer can satisfy acquisition provenance without a provider message ID.
Conversely, an Extra High reader or Mission Control actor that only rehashes the worker's copy
does not create independence.

## Required universal revision

The meta-review directs the shared architecture lane to create a new epoch that:

- separates captured-source integrity from acquisition independence;
- updates the bootstrap and four supervision patterns;
- bumps `OBJECTIVE-RECONCILIATION.json`, `ACTIVE-TASK.json`, and
  `RESEARCH-SUPERVISION-VERDICT.json` from schema v1 to v2;
- adds explicit capture, acquisition, capability, comparison, and source-gate fields;
- adds hostile tests for worker-copied exact text, omitted owner text, owner re-attestation,
  attempted integrity-only release, actor-label laundering, and independent observation without
  a provider locator;
- preserves historical records and projects legacy states fail-closed; and
- reissues the exact architecture commit, tree, and content hashes after the full universal test
  suite passes.

This project records the ruling and adopts the conservative active-worker state. It does not
silently edit the universal supervision repository.
