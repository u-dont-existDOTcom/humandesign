# Life Patterns H1 Content-Authority Binding — Execution Receipt

Date: 2026-09-03

Status: **IMPLEMENTED AND CI-GATED AS VERIFICATION/IMPORT INFRASTRUCTURE ONLY**

Branch: `codex/discover-life-patterns-mvp`

Verified implementation head: `0a948cf32a72678f519bc37f9916a441bc04a85d`

PR: #24

## What this milestone does

Life Patterns now has a one-way, receipt-based authority binding layer for future substantive neutral measurement content.

Primary implementation:

- `src/hdmatch/evaluation/h1_authority.py`
- `tests/unit/test_h1_authority.py`
- `tests/unit/test_neutral_measurement_readiness.py`

The layer:

- pins the exact already-frozen Survey-v2 H1 exposure-adjudication specification rather than inventing a second clean-author policy;
- accepts only externally validated H1 adjudication receipts;
- verifies content-address integrity of those receipts;
- rechecks the frozen eligible-branch semantics before an H1 receipt may participate in authority;
- requires sufficient evidence, no unresolved missing facts, and an eligible adjudication outcome;
- binds author eligibility to the exact H1 artifact and exact neutral-content freeze hash;
- requires every construct author referenced by the authorship receipt to have a matching eligible H1 receipt;
- requires a content-review receipt bound to the same exact content hash;
- prevents content approved for validation from silently changing during review;
- requires any reviewer who substantively influences content to carry an eligible H1 reference;
- derives the compact `HumanContentAuthorityReceipt` consumed by the neutral ontology layer only after the full authority bundle passes verification;
- stores authority bundles as immutable canonical content-addressed artifacts.

## Exact reused H1 specification lock

The implementation binds these already-frozen Survey-v2 artifacts:

- contract version: `survey-v2-h1-exposure-adjudication-contract-v1.0.0`
- contract SHA-256: `b26e8ca398eb805125ed4ea475243e1d0cb5134bee4c509dd29223355ff1b070`
- request schema SHA-256: `1c7f55040d473fd8f4b47107b0edd296a448d9a5121845e907c6fd5eaf412240`
- adjudicator prompt SHA-256: `236c3cfe5fbfc9ee3e03abfa49a3b7c5030276226a953778bb1dc0bef95f8100`
- output schema SHA-256: `9ec56a40cac3c6d31650ae5983083e74985b9ccca56bf2b616cba5787fb9c46c`
- H1 freeze manifest SHA-256: `e920ac03ae51c811c2ed4fd54a7e7c28076c8769833c193ff40ea33d57337a80`
- required adjudication model family under that frozen contract: `gpt-5.6-sol`

This is reuse/composition, not a new exposure-classification methodology.

## What is explicitly NOT implemented or authorized

This milestone does **not**:

- run H1 exposure adjudication;
- call `gpt-5.6-sol` or any other model for H1 adjudication;
- classify a human author as clean/eligible;
- collect or contact candidate human authors;
- manufacture or repair an eligibility result;
- create substantive neutral constructs;
- authorize participant recruitment, deployment, merge, spending, or model execution;
- establish construct validity or reliability.

The existing Survey-v2 H1 freeze manifest itself explicitly freezes a specification only and does not authorize implementation/execution or H1 authorship. This Life Patterns layer preserves that boundary.

## Measurement-readiness closure

The same gated head also closes a downstream scoreability leak in `neutral_measurement.py`.

A validation coding run is now blocked from `scoreable_for_model_tournament=True` when:

- it contains no coded episode records;
- any used observable has not reached `validity_status == validation_candidate`;
- any used observable lacks a declared human reliability baseline (`human_baseline_evaluated` or `automation_evaluated`);
- or any previously existing scoreability blocker is present.

Automation remains separately blocked unless it carries a human-benchmark automation-validation receipt.

This prevents H1 authorization alone from being mistaken for measurement validity/reliability.

## Exact CI gate

GitHub Actions run: `33794321062`

PR merge checkout: merge commit `0ee40d928d860cbe69f933fb2533da3b085bfd37`, merging implementation head `0a948cf32a72678f519bc37f9916a441bc04a85d` into the current PR base used by CI.

Results:

- `python -m pytest`: **412 passed, 6 skipped**;
- skips: 3 shallow-checkout audit-commit skips and 3 Swiss-Ephemeris-environment skips;
- `ruff check src tests --ignore E501,I001`: **all checks passed**;
- `mypy src/hdmatch`: **success, no issues in 137 source files**.

## Genuine next blocker

Substantive confirmatory measurement work now requires a real external human deliverable that this theory-exposed AI is not eligible to author:

1. an exact neutral ontology/codebook content artifact authored/substantively revised only by eligible H1 human author(s);
2. the matching externally validated H1 adjudication receipt(s), bound to that exact content-freeze hash and authorship window;
3. a content-review receipt bound to the same hash, with any content-influencing reviewer also H1-eligible;
4. human development/double-coding work sufficient to produce the required reliability evidence and advance selected observables to validation-candidate status.

Until those artifacts exist, the correct next state is to remain fail-closed. Real model adapters or a tournament execution layer must not invent neutral aliases or mappings in place of the missing human-authored measurement content.
