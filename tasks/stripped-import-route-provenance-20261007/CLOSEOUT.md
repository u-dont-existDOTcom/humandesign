# Stripped imported-route provenance repair — closeout

## Outcome

SATISFIED for the reported G15 incident.

The first repair was not sufficient: it invalidated the stale legacy G15 question, but the live existing review later emitted TF1-G15 during the legacy final-synthesis fallback. The reason was more specific than the original diagnosis: the candidate actually stored in Railway had preserved exact Q&A and record-level recovery metadata, but its historical per-turn route metadata had been stripped. Consequently, the final reviewer still saw the G15 lineage as unpresented.

The second repair resolves verified historical route identity in this order: explicit canonical ID; explicit top-level/nested historical ID; stable historical turn-ID suffix on a completed recovered record; then exact frozen question wording. It applies the same normalization to old saved worker state and to both fast and legacy route selection. It also requeues a persisted active canonical successor when the same substantive lineage is already present in the candidate, without fabricating an answer or skip.

## Real review verification

The same existing real review was preserved. Its pending TF1-G15 question was automatically cleared. Clarification history remained at one actual prior response; no fake answer or skip was added. The review re-entered reconciliation/omission checking and ultimately emitted TF1-G17 as a missing-piece follow-up rather than G15/TF1-G15. That G17 question is bound to two prior G17 source turns, so it is not being treated as a fresh canonical replacement.

No private review ID or participant source text is committed. See `LIVE-RECOVERY-RECEIPT.json`.

## Deployment

- Railway production: exact tested build `3b95b5614fb4e98d23261fa01f9dc5564981e7d8`, deployment succeeded.
- Local subscription reviewer: `release.stripped-route-3b95b56`, active.
- Question policy remains `tendency-first-v1-20261006`.
- No Custom GPT editor/Knowledge/Action change is required for this backend repair.

## Verification

- focused regression before merge: 28 passed;
- participant suite: 190 passed;
- repository pytest suite: 1,018 passed, 6 astronomy-data-dependent tests skipped;
- changed runtime/test scope lint: passed;
- mypy: 220 source files, no issues;
- exact private stripped 81-turn deterministic regression: G15 resolved, TF1-G15 treated as presented/repair-only, and TF1-G15 absent from both legacy bulk and ordinary fresh-question menus;
- universal unittest discovery: 26 passed.

Known repository-wide baseline debt was checked rather than hidden:
- `task_acceptance.py` fails on missing astrology oracle artifacts and missing project-local `.venv`;
- declared root Ruff scope has 883 pre-existing errors and this repair changes no file in that `src/tests/scripts` scope;
- canonical UDA audit reports 90 errors / 73 warnings on both the pre-repair base and repaired tree.

Those baseline failures are not represented as green and were not caused by this Life Patterns repair.

## Participant-facing state

Do not answer the obsolete G15 question. The existing review has already moved past it. The current pending item, if the GPT surfaces it, is the independently admitted G17 missing-piece follow-up. Continue in the same saved chat/review; do not create a replacement review.
