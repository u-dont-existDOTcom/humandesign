# Life Patterns current state — 2026-09-11

Status: public-safe controlling overlay for `codex/discover-life-patterns-mvp`, draft PR #24.

## Current gate

The blind V5 semantic/contract gate and public V5 mechanical implementation gate have passed. The exact frozen private calibration transport was recovered and fully reverified.

Owner review then found one **presentation defect** in the first private V5 candidate: the broad observable question could clearly apply while the closest specific value was an absence-dependent value that correctly could not be asserted unless its four-part evidence gate was fully established. The generic `Not enough information` fallback therefore sounded as if it denied the obvious applicability of the story.

This is **not a reason to weaken the absence gate**. The accepted V5 semantics already distinguish:

- `observed`: at least one specific substantive value or affirmative component is sufficiently established;
- `insufficient`: the general situation may apply, including clearly applying, while the specific distinction cannot be supported without inference;
- `not_applicable`: the prerequisite situation itself is affirmatively absent; non-mention is not enough.

An R2 private owner-review candidate now makes that distinction explicit. **The next action is owner usability review of R2. Human collection remains unauthorized.**

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

## Frozen calibration source

Outer transport:

- `Life-Patterns-Recurrence-Corrected-Human-Calibration-V2-PRIVATE-2026-09-08.zip`
- SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- 422297 bytes / 15 members

Inner receipt:

- `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 8 packets

All receipt-declared member hashes and packet content addresses reverified. Coverage remains exactly 44 episode + 22 series = 66 units.

## Owner usability feedback 001

Public-safe disposition:

`state/LIFE-PATTERNS-V5-OWNER-USABILITY-FEEDBACK-001-2026-09-11.json`

The R2 presentation repair:

- keeps the observable-specific behavioral question;
- changes the next prompt to **`Which statement best matches the evidence?`**;
- labels observed as **`Yes — a specific behavior below is established`**;
- keeps **`Doesn't apply to this story`** for affirmative absence of the prerequisite situation;
- changes insufficient to **`Not enough information for a specific behavior`** and explicitly says the general situation can still clearly apply;
- labels absence-dependent choices before selection;
- when an absence gate is incomplete, explains that the value cannot be counted and directs the reviewer to the specific-value insufficient state rather than implying the story is irrelevant.

The four-part absence gate, V5 machine states, selected units, private source, recurrence semantics, and target-theory blind are unchanged.

## Private R2 owner-review candidate

Private package identity only:

- filename `Life-Patterns-V5-PRIVATE-Owner-Review-R2-2026-09-11.zip`
- SHA-256 `d5293e0a363c0aa210c8c4031959534c065b375b158335569f4d63098757f5c9`
- 633219 bytes
- HTML SHA-256 `55b4a92b73cf42a58f43339c792a6f53c475311395eec2f96c3e3bbf431290a9`
- HTML bytes `1608348`

The previous owner-review ZIP `0ff2a6db…a25da2f5` is superseded for owner review.

Targeted smoke verified JavaScript syntax, the revised evidence-state wording, pre-labelled absence-dependent choices, and actionable handling of the previously problematic R05 absence-dependent shape. Managed sandbox Chromium still blocks direct local navigation, so that limitation remains part of the private package receipt; no private candidate bytes are committed publicly.

## Exact next action

Owner reviews the R2 private package. In the previously problematic choice-resolution shape, confirm that it now makes sense to say the general situation clearly applies while choosing `Not enough information for a specific behavior` if the absence-dependent value cannot satisfy all four evidence checks.

If R2 is accepted, promote the same **presentation-only** repair into the canonical public builder with focused tests and green CI before human collection begins.

## Hard boundaries

- no independent human collection before explicit owner acceptance plus green reproducible generation of the accepted surface;
- do not weaken the four-part absence gate merely to make a narrative fit a value;
- no automated participant coding before the revised independent human first pass is complete and frozen;
- no target-model scoring/reveal;
- private exact text and generated private UI remain outside public GitHub;
- no merge/deploy, recruitment/contact, or spending without separate authorization.

## Preserved owner correction

**There was never a completion policy.** That premise was invented earlier and must not be recreated or inferred from artifact counts.
