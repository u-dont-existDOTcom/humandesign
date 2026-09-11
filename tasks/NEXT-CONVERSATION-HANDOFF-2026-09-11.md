# Life Patterns — next-conversation handoff — 2026-09-11

Repository: `u-dont-existDOTcom/humandesign`
Branch: `codex/discover-life-patterns-mvp`
Draft PR: `#24`

GitHub is canonical. Before substantive work, fetch the current PR #24 head and read:

1. `tasks/ACTIVE-TASK.json`
2. `state/LIFE-PATTERNS-CURRENT-STATE-2026-09-11.md`
3. `state/LIFE-PATTERNS-V5-OWNER-USABILITY-FEEDBACK-001-2026-09-11.json`
4. `tasks/LIFE-PATTERNS-V5-OWNER-USABILITY-REVIEW-2026-09-11.md`
5. `state/LIFE-PATTERNS-V5-MECHANICAL-IMPLEMENTATION-VERIFIED-2026-09-11.json`
6. `state/LIFE-PATTERNS-V2-PRIVATE-FREEZE-VERIFIED-2026-09-08.json`
7. `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-VERIFIED-2026-09-10.json`
8. `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
9. `state/CURRENT-STATE.md`

## Closed gates

The blind V5 semantic/contract gate passed at independent review commit `ce04642146c41a7d5d94f85360572c78de887682`: all 47 carried findings resolved, no blocking new finding, `semantic_change_required=false`, `safe_for_implementation=true`.

The public V5 mechanical implementation passed at code head `35a2daf7a9cf0628e976b7b57f810c2f90a2bf02`, CI `34623829382`: 675 passed, 7 expected skips, Ruff clean, strict mypy clean across 174 source files.

Do not redo those gates unless new evidence demonstrates a genuine defect.

## Frozen calibration source

Outer transport:

- `Life-Patterns-Recurrence-Corrected-Human-Calibration-V2-PRIVATE-2026-09-08.zip`
- SHA-256 `f038237a6a1ce776bb28846b76ff49339e7a9e7f28d33c5d1ad877e0d916d837`
- 422297 bytes / 15 members

Inner receipt:

- `LPHB2-F34245FAE32B513DDCFE`
- SHA-256 `f34245fae32b513ddcfe22b7d21081997e8c28e18fccd25b962c30af2fe0a78f`
- 8 packets

All receipt-bound member and packet hashes reverified. Coverage remains 44 episode + 22 series units.

## Owner usability defect 001 — diagnosed as presentation only

The first private owner-review candidate is superseded.

Owner feedback exposed a contradiction in the human presentation: a broad observable question could be clearly applicable while the closest specific substantive value was absence-dependent and correctly could not satisfy its required four-part gate. The generic `Not enough information` fallback sounded as if it denied the obvious applicability of the story.

The accepted V5 semantics already support the needed distinction:

- `observed` requires a sufficiently established **specific** value/affirmative component;
- `insufficient` can apply even when the general situation clearly applies but no specific distinction can be supported without inference;
- `not_applicable` requires affirmative absence of the prerequisite situation.

The four-part absence gate is **not** weakened.

Public-safe disposition:

`state/LIFE-PATTERNS-V5-OWNER-USABILITY-FEEDBACK-001-2026-09-11.json`

## Private R2 owner-review candidate

Private package identity:

- filename `Life-Patterns-V5-PRIVATE-Owner-Review-R2-2026-09-11.zip`
- SHA-256 `d5293e0a363c0aa210c8c4031959534c065b375b158335569f4d63098757f5c9`
- 633219 bytes
- HTML SHA-256 `55b4a92b73cf42a58f43339c792a6f53c475311395eec2f96c3e3bbf431290a9`
- HTML bytes `1608348`

R2 changes only the human presentation:

- evidence-state prompt: `Which statement best matches the evidence?`
- observed: `Yes — a specific behavior below is established`
- not applicable: `Doesn't apply to this story`
- insufficient: `Not enough information for a specific behavior`
- insufficient copy explicitly says the general situation can still clearly apply;
- absence-dependent choices are labelled before selection;
- incomplete absence gates explain that the value cannot count and point to the specific-value insufficient state instead of implying the story is irrelevant.

The package itself remains private and is not committed to GitHub.

## Exact next gate — owner review of R2

The owner should review representative units in the R2 package, especially the previously problematic R05 shape, and return either:

1. explicit presentation acceptance; or
2. another concrete usability defect.

This is not the 66-unit annotation pass. Technical smoke does not equal owner acceptance.

## After R2 presentation acceptance

Promote the same presentation-only repair into the canonical public builder with focused tests and green CI. Only after owner acceptance + green reproducibility may the independent human first pass begin. Only after that pass is complete and frozen may automated participant coding begin.

## Hard boundaries

- do not weaken the four-part absence gate to make a narrative fit;
- no private exact text or generated private UI in public GitHub;
- no human collection before owner acceptance and green reproducibility;
- no automated participant coding before the revised independent human pass is frozen;
- no target-model scoring/reveal;
- no merge/deploy, recruitment/contact, or spending without separate authorization.
