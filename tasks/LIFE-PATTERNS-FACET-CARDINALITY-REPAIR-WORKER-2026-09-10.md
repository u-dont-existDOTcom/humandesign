# Life Patterns facet cardinality repair — fresh blind worker

Run this only after confirming PR #24 still contains the second blind review commit `4f51d075cb200e57820486e4f9686d81c7fc604f` in its history.

## Fresh-context requirement

Use a NEW target-theory-blind context. It must not be the theory-exposed project/owner chat. Prefer a context that did not author the v3 candidate and did not perform the second blind review.

Do not inspect Human Design, astrology, target mappings, birth/chart data, target-model outputs, participant-specific target results, model-fit results, or theory-exposed commentary.

## Exact instruction

Follow:

`state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-PROMPT-v1-2026-09-10.txt`

exactly.

The repair is intentionally contract-only. The previous review resolved 38/45 original blockers, all R05 blockers, and absence/missingness semantics. Do not reopen those semantic decisions merely because implementation is still blocked.

## Required outputs

Create exactly:

- `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v4-CANDIDATE-2026-09-10.json`
- `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-SUMMARY-v1-2026-09-10.json`

The disposition must contain exactly these eight IDs once each:

`OA-007, OA-011, OA-076, OA-084, OA-085, OA-114, OA-121, NR-001`.

If you determine that a substantive codebook semantic change is required, do not make it. Set `semantic_change_required=true`, explain the blocker in the summary, commit the required outputs, and stop.

## Stop boundary

Do not edit existing candidate/review artifacts. Do not implement software/UI/package changes, run participant coding or annotation, start human calibration, score/reveal any target model, merge/deploy, contact/recruit anyone, or spend money.

After push, return only the fields required by the substantive prompt.
