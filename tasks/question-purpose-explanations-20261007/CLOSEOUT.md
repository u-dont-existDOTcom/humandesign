# Question-purpose explanations — live closeout

## Status

Backend/runtime implementation is merged and live. The private Custom GPT editor is the only remaining boundary before the participant-facing GPT is mechanically instructed to display the explanation before every question.

## What is enforced

- Every one of the 25 active tendency-first routes has a curated, neutral `participant_purpose`.
- Every legacy route that remains eligible as a live probe receives a nonempty conservative purpose from its neutral planning target/family, with a generic fallback if neither exists.
- Fast-review and legacy final-synthesis clarifications expose nonempty `participant_purpose` separately from exact `question_text`.
- Already-saved pending clarifications are enriched on read without replacing the review, changing the question text/ID, or adding an answer/skip.
- The GPT instructions/package require `What this tests: <neutral purpose>` before every behavioral question and require the exact question itself separately.
- Purposes may name only the person-level tendency/distinction. They must not expose answer direction, scoring, Human Design/astrology targets, or diagnostic/validated-trait claims.

## Live evidence

Railway's current successful deployment is explicitly labeled `Life Patterns participant question purpose explanations 653734a`. The live `/action-openapi.yaml` is byte-identical to the tested repository schema and includes required `participant_purpose` in reviewer clarifications. The live health response reports the expected unchanged question-policy identity. The installed local reviewer purpose-related source hashes match the merged repository files and the worker is active.

## Verification already completed on the implementation

- focused tests: 64 passed;
- participant tests: 193 passed;
- repository tests: 1,019 passed, 6 astronomy-data skips;
- scoped Ruff: passed;
- mypy: 220 source files, passed;
- `git diff --check`: passed;
- existing-pending-clarification enrichment regression: passed without question replacement or clarification-history change.

## Remaining owner-only product-surface gate

Apply the delivered `Life-Patterns-GPT-question-purpose-update-2026-10-07` package to the **same existing GPT**: replace Instructions, replace only `TENDENCY-FIRST-GUIDE-v1.json`, and reimport the existing Action schema while preserving the current Bearer credential. Then select Update. Keep the same saved conversation and same Railway review.

Until that private editor step is applied, the backend returns the purpose metadata but the old GPT instruction set does not mechanically require displaying it before every question.
