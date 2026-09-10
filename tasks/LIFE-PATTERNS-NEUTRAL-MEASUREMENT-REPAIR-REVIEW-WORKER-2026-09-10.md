# Life Patterns neutral measurement repair — second fresh blind review worker

Use this wrapper only **after** the first fresh blind repair worker has committed the three candidate repair artifacts required by `tasks/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-WORKER-2026-09-10.md`.

## Fresh-context requirement

Use a second new target-theory-blind context that did not author the candidate repair. Do not inspect Human Design, astrology, target mappings, birth/chart data, target-model outputs, participant-specific model results, model-fit results, or the exposed project review.

Follow:

`state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-PROMPT-v1-2026-09-10.txt`

exactly.

## Inputs

Before review, verify the authoritative blind audit commit remains:

`7ea0641e0913815306f8c182be5e7e8b18115fff`

and read the candidate repair from the GitHub-visible commit returned by the first repair worker. Do not review uncommitted local drafts if a committed candidate exists.

## Required outputs

Create exactly:

- `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-RAW-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-NEUTRAL-MEASUREMENT-REPAIR-REVIEW-SUMMARY-v1-2026-09-10.json`

The raw review must contain exactly one OA row for each of the original 45 blockers, plus only genuinely new material `NR-*` findings if needed.

Mechanically verify before commit:

- exactly 45 OA rows;
- OA IDs exactly equal the original blocking set with no duplicates;
- all rows parse as JSON and use the exact required fields;
- summary counts reconcile with the raw rows;
- `safe_for_implementation=true` only when every OA blocker is RESOLVED and no NR row blocks implementation.

Commit and push the two review artifacts, then return only:

- GitHub-visible commit SHA;
- SHA-256 and byte size of each review file;
- OA row count and NR row count;
- summary `safe_for_implementation` value;
- blocking IDs, if any;
- statement that no candidate artifact was edited;
- statement that no target-model information was used.

## Stop boundary

Do not implement the repair, modify UI/package/handoff, code participant evidence, run automated annotation/human calibration, target scoring/reveal, merge/deploy, contact/recruit, or spend money.
