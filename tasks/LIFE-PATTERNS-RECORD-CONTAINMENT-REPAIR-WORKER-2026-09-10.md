# Life Patterns NR2-001 record-containment repair worker

Run this in a **fresh target-theory-blind context** distinct from the reviewer that authored `f5f02c976b11fbabc7c136f9c80fbd312600d91d`.

Do not inspect Human Design, astrology, target mappings, birth/chart data, target-model outputs, participant-specific target results, model-fit results, or theory-exposed commentary.

## Exact instruction

Follow:

`state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-PROMPT-v1-2026-09-10.txt`

exactly.

Bind the work to the exact GitHub-visible commits named in that prompt. The repair is contract-only. `semantic_change_required=false` from the independent review means the defect is expected to be representational, but if the repairer independently concludes a substantive semantic change is necessary, it must stop and report that rather than make the change.

## Required outputs

Create exactly:

- `state/LIFE-PATTERNS-FACET-RELATION-CONTRACT-v5-CANDIDATE-2026-09-10.json`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-DISPOSITION-v1-2026-09-10.jsonl`
- `state/LIFE-PATTERNS-RECORD-CONTAINMENT-REPAIR-SUMMARY-v1-2026-09-10.json`

The disposition must contain exactly one `NR2-001` row. Do not edit v4, either prior review, the codebook clarification, software, UI, or package artifacts.

## Stop boundary

Commit/push only the three repair outputs. `safe_for_blind_re_review=true` does not authorize implementation. A separate fresh target-theory-blind re-review is mandatory before engineering work can resume.
