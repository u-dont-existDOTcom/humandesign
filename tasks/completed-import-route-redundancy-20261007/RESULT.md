# Completed imported-record redundancy repair — 2026-10-07

## Owner incident

A historically completed 81-turn Life Patterns candidate was asked the legacy canonical G15 six-hour work-energy scenario again. The source already contained historical G15, R07, R08, R09, WORK-RECOVERY, plus later R07/R08 retests. The record stored these historical route IDs under source.historical_question_id while canonical_question_id was null.

## Root cause

This was a semantic-routing bug, not a service/resource failure.

1. Imported route resolution ignored source.historical_question_id; deterministic answered/presented sets therefore missed most recovered historical routes.
2. Tendency-first successors were not linked to historical predecessor presentation for redundancy. A new policy ID could look unasked even when the substantive route had already been answered.
3. Completed-source metadata and the unrecovered-current-test warning were retained as raw provenance but not made active in clarification admission.
4. Same-family source turns were not explicitly attached as completed-record redundancy context.
5. A clarification generated before the tendency-first policy could persist in clarification_needed; deploying better policy did not automatically invalidate that stale pending question.

## Repair

- Imported records now resolve route identity in this order: valid canonical ID, verified historical route ID (including explicit retest aliases), then exact canonical wording. Raw source bytes remain untouched.
- Saved review states are normalized from their preserved original_record before continuation, so old queued work benefits without re-importing or rewriting the participant source.
- Historical routes and TF1 successors form one substantive lineage for answered/presented/skip logic.
- Completed historical imports expose their historical status and unrecovered-gap flag to triage/admission. Missing newer wording and unrecovered later turns are explicitly provenance gaps, not coverage permission.
- Same-family historical turns are supplied to completed-source triage/admission. A repair candidate must anchor relevant historical family evidence; an unrelated anchor is rejected.
- Legacy routes retired by tendency-first remain unavailable for fresh questions.
- On service startup, persisted fast-review clarifications whose route is now retired are cleared and requeued without fabricating an answer or skip. The semantic state is rebuilt from the immutable candidate plus only real clarification history.
- Current explicit participant stop/pause controls and exact historical wording remain preserved.

## Exact private regression

The exact 81-turn Library candidate was copied to temporary owner-machine storage and never committed. The deterministic check resolved historical G15, two R07-family answers, and two R08-family answers; legacy G15 became nonselectable and TF1-G15 became repair-only with seven work-energy family turns attached.

A GPT-5.6 Sol xhigh fast semantic run on that exact candidate returned no G15 or TF1-G15 clarification. A privacy-safe receipt is committed separately. One run selected TF1-G02, a direct general-tendency clarification with two source antecedents. A separate exact private run also returned no G15-family question. These are regression checks on this development record, not evidence of personality-test validity.

## Verification

Final current-head:
- focused route/runtime tests: 25 passed;
- full participant-review suite: 187 passed;
- repository pytest suite: 1,018 passed, 6 astronomy-data-dependent tests skipped;
- changed application/runtime files: Ruff passed with the repository's previously documented UP035/E501/I001 legacy exclusions; no new lint finding;
- mypy: 220 source files, no issues;
- git diff --check: passed.

The repository-declared root Ruff scope (src tests scripts) currently reports 883 pre-existing style errors. This task changes no file in that scope; the changed application files were checked directly. That baseline debt is not presented as a passing gate.

## Live-boundary requirement

Before closeout: deploy the exact tested application/worker bytes, verify health and worker identity, run a synthetic live review proving no retired canonical question is returned, and preserve the existing participant review rather than creating a duplicate. The private GPT Action/schema and Knowledge package do not need another editor update for this backend repair.
