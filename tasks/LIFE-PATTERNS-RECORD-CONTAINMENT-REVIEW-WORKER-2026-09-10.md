# Life Patterns record-containment repair — independent blind re-review worker

Run this only after `tasks/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-WORKER-2026-09-10.md` has produced and pushed the v5 contract repair artifacts.

## Fresh-context requirement

Use a **fresh target-theory-blind context distinct from the v5 repair author**. Prefer a context also distinct from the earlier v4 reviewer.

Do not inspect Human Design, astrology, target mappings, birth/chart data, target-model outputs, participant-specific target results, model-fit results, or theory-exposed commentary.

## Exact instruction

Follow:

`state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-PROMPT-v1-2026-09-10.txt`

exactly.

Bind the review to the exact GitHub-visible v5 repair commit returned by the prior worker.

## Required outputs

Create exactly:

- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-RAW-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REVIEW-SUMMARY-v1-2026-09-10.json`

The raw review must contain all 45 original OA blocking IDs exactly once, `NR-001` exactly once, and `NR2-001` exactly once. Only genuine new material findings may be added as `NR3-*`.

`safe_for_implementation=true` is permitted only under the full gate in the substantive prompt. A passing review authorizes exposed-context mechanical implementation only; it does not authorize human calibration, automated participant coding, target scoring/reveal, merge/deploy, recruitment/contact, or spending.

## Stop boundary

Do not edit candidate/repair artifacts or implement anything. Commit/push only the two review outputs and return only the fields requested by the substantive prompt.
