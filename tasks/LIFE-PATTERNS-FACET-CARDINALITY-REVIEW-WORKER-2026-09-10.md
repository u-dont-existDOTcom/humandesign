# Life Patterns facet cardinality repair — independent blind re-review worker

Run this only after `tasks/LIFE-PATTERNS-FACET-CARDINALITY-REPAIR-WORKER-2026-09-10.md` has produced and pushed the v4 contract repair artifacts.

## Fresh-context requirement

Use a target-theory-blind context distinct from the v4 repair author. Prefer a new context rather than the earlier reviewer so the re-review is independently replicated.

Do not inspect Human Design, astrology, target mappings, birth/chart data, target-model outputs, participant-specific target results, model-fit results, or theory-exposed commentary.

## Exact instruction

Follow:

`state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-PROMPT-v1-2026-09-10.txt`

exactly.

Bind the review to the exact GitHub-visible v4 repair commit returned by the prior worker.

## Required outputs

Create exactly:

- `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-RAW-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-FACET-CARDINALITY-REVIEW-SUMMARY-v1-2026-09-10.json`

The raw review must contain exactly the original 45 OA blocking IDs once each plus exactly one carried-forward `NR-001` row, with only genuine new material findings allowed as `NR2-*`.

`safe_for_implementation=true` is permitted only under the full gate in the substantive prompt. A passing review authorizes the exposed project context to begin mechanical implementation; it does not itself authorize human calibration, automated participant coding, target scoring/reveal, merge, or deployment.

## Stop boundary

Do not edit candidate/repair artifacts or implement anything. Commit/push only the two review outputs and return only the fields requested by the substantive prompt.
