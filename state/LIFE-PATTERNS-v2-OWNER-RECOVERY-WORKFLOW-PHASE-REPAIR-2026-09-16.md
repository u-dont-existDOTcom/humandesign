# Life Patterns v2 — recovery workflow-phase repair — 2026-09-16

## Owner finding

After progress restoration was repaired, a recovered checkpoint could still end visually at the prior tentative synthesis with only the generic composer visible. The saved state had already adjudicated that synthesis, so the participant had no meaningful next action even though the data itself had restored.

## Verified mechanism

The recovery endpoint restored semantic/session data but exposed only `pattern_active` to the UI. `pattern_active=false` collapsed two different states:

1. ordinary interview state, where the composer is correct;
2. post-adjudication state, where the correct next surface is the settled result plus **Continue interview / Finish for now**.

The owner-provided audit checkpoint contains a participant adjudication with decision `accept`, while both the active proposal and ephemeral draft are absent. That is a settled post-adjudication session, not a blank-composer state.

## Repair

`PersistentRecoverabilityCoverageSession.recovery_status()` now exposes an explicit workflow phase:

- `synthesis_review` when an ephemeral synthesis is awaiting judgment;
- `post_adjudication` when the current session contains a participant adjudication and no active draft;
- `interview` otherwise.

It also exposes the latest adjudication decision and its participant-approved/proposal wording for UI reconstruction.

The recovery UI now renders by workflow phase rather than using `no active draft => show composer` as a default. A restored post-adjudication session hides the composer, reconstructs the settled result card, and exposes the finite continuation controls. Active syntheses still restore their judgment controls; ordinary interview sessions restore the composer.

## Verification

Regression coverage: `tests/unit/test_life_patterns_v2_owner_import_resume.py`.

GitHub Actions run `35118533701`: **SUCCESS** — tests, Ruff, and strict mypy all passed.

Railway deployment `0887ea20-2f36-40be-8f7b-f00405d0fa8e`: **SUCCESS** from application head `c983764ed4f09ac3c9dd5e7bf3796984f73e231d`; `/healthz` returned HTTP 200.

## Next consumer check

Refresh the existing browser checkpoint. If its current session was already adjudicated, the restored page must show the settled result plus **Continue interview / Finish for now**, not a blank answer box. If a synthesis is genuinely still awaiting judgment, the synthesis decision controls must appear instead.
