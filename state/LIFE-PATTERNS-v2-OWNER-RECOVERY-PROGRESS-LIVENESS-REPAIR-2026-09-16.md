# Life Patterns v2 — recovery progress + liveness repair — 2026-09-16

## Owner finding

Direct owner testing of the recovered-interview path exposed three linked consumer-seam defects:

1. long-running reconstruction/finalization calls could leave the UI looking idle for several seconds;
2. the progress card could remain at `Preparing…` after recovery;
3. after accepting a recovered synthesis, `Continue interview` could incorrectly report coverage complete even though the recovered audit snapshot still had many open dimensions.

The supplied private audit/recovery snapshot was inspected outside Git. It showed that coverage was materially incomplete; no private interview narrative is committed here.

## Generating condition

The recovery path restored participant answers and aggregate coverage rows but bypassed the normal fresh-session bootstrap that loads the 23-dimension coverage blueprint. Client progress therefore had coverage data but an empty blueprint. The progress renderer interpreted that as “not initialized,” while `incompleteCoverage()` evaluated an empty blueprint as having zero missing dimensions and could therefore emit a false completion claim.

Separately, several model-backed operations disabled buttons or waited on network/model work without a persistent participant-facing liveness surface. The request was alive, but the UI did not expose that state clearly.

## Repair

Participant-facing implementation:

- `src/hdmatch/api/life_patterns_v2_owner_liveness_ui.py`
- `src/hdmatch/api/life_patterns_v2_owner_liveness.py`
- deployment wrapper now serves the liveness-aware app.

Behavioral changes:

- every recovery/restore path calls `ensureCoverageBlueprint()` before restored coverage is rendered or completion is evaluated;
- `Continue interview` re-checks that the blueprint is loaded before computing missing dimensions;
- restored aggregate coverage therefore maps against the actual 23-dimension blueprint instead of an empty array;
- long operations show a dedicated indeterminate **Working on it…** card;
- accepting a synthesis shows **Saving that and updating interview progress…** while adjudication/coverage work is in flight;
- recovered-transcript reconstruction shows **Rebuilding the recovered interview and preparing a synthesis…**;
- `Continue interview` shows **Choosing the next useful question…** while the adaptive selector runs;
- import/start-clean actions also expose liveness instead of appearing idle.

The working indicator reports request liveness only. It is intentionally separate from the scientific interview-progress percentage.

## Regression

`tests/unit/test_life_patterns_v2_owner_liveness.py` checks:

- blueprint loading before exact and transcript-only recovery rendering;
- explicit liveness feedback for reconstruction, adjudication, and next-question selection;
- `Continue interview` cannot test for completion before the blueprint is loaded;
- app state exposes the three repaired participant-facing guards.

## Scientific boundary

This repair changes client state hydration and UX liveness only. It does not change the accepted v2 evidence semantics, the target-theory-blind runtime, the 23-dimension blueprint, or the post-freeze DOB/time acceptance criterion.

## Next consumer-seam check

Reload the recovered audit snapshot. Expected behavior:

1. restored progress should resolve from `Preparing…` to an actual approximate percentage/open-area count;
2. reconstruction/finalization/continue operations should visibly show that work is in progress;
3. after accepting the recovered synthesis, `Continue interview` should advance into remaining measurement areas rather than incorrectly claiming completion.
