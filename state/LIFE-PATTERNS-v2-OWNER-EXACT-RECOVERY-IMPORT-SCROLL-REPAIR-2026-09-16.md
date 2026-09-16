# Life Patterns v2 — exact recovery, import, progress-unit, and scrolling repair — 2026-09-16

## Owner findings

Direct owner use identified four remaining development-surface defects:

1. the prior recovery copy preserved visible conversation only, while the exact hidden evidence ledger still lived only in the Railway process and could be lost on restart;
2. the UI had a save/download recovery affordance but no inverse import/restore control;
3. the progress card labeled still-open measurement dimensions as remaining questions even though one adaptive answer may satisfy several dimensions;
4. viewport movement followed the newest message rather than the next required action, and the initial answer box could be below the viewport without a persistent visible scrollbar.

## Repair

### Exact hidden-ledger recovery

`src/hdmatch/api/life_patterns_v2_owner_persistent.py` adds a checksum-bound JSON recovery snapshot containing the exact current server session state needed to resume the hidden ledger:

- conversation turns and IDs;
- current episode / pending-boundary / pattern-focus state;
- complete v2 record including fact revision lineage, proposals/adjudications if present, and source provenance hashes;
- proposal support and active proposal pointer;
- current ephemeral synthesis draft;
- last in-thread coverage/progress report.

The live service still does **not** persist private interview narrative to Git or a Railway volume. The browser periodically requests the exact snapshot and stores the latest copy in local browser storage. A downloaded recovery JSON contains the same server snapshot plus client aggregate coverage/results. On page reload after a server restart, the browser attempts to restore the latest exact snapshot automatically.

The recovery snapshot is mutable continuity state, **not** the final scientific measurement freeze.

### Import

The participant UI now provides both:

- **Download recovery JSON**
- **Import recovery JSON**

Exact `life-patterns-browser-recovery-v2` / `life-patterns-hidden-ledger-session-v2` files restore the hidden ledger without re-running the interview.

Older visible-only files such as the supervising Chat recovery `life-patterns-visible-recovery-v1` can also be imported for development continuity. Because those historical files never contained the old server ledger, they are explicitly marked `visible_transcript_only` and are blocked from masquerading as a clean scientific freeze.

### Progress unit

The progress card now reports **measurement areas still open**, not questions left. Percent remains a weighted coverage estimate; a partial dimension contributes partial progress. The note explicitly states that one answer can cover several areas.

### Scrolling

The page now:

- forces a vertical scrollbar to remain available;
- scrolls toward the next actionable surface (composer, synthesis judgment panel, or continuation controls), not merely the latest bubble;
- scrolls the opening answer box into view automatically;
- retains extra scroll padding around the sticky composer.

## Verification

Exact code/test checkpoint CI: GitHub Actions run `35049331970` — **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Regression coverage: `tests/unit/test_life_patterns_v2_owner_persistent.py` verifies exact hidden-ledger round-trip with stable fact IDs and draft synthesis, checksum rejection after modification, non-scientific status of legacy visible-only recovery, import controls, progress-area labeling, persistent scrollbar, and action-oriented scrolling.

Live Railway deployment: `cca4d5c8-fee7-4f30-a00a-34f4b4ba6299` from application head `389c6191989071c35253b24e36a43d28ba03d963` — **SUCCESS**. Runtime startup completed and `/healthz` returned HTTP 200.

## Important recovery boundary

The previously recovered owner JSON created in supervising Chat is a visible-transcript recovery and therefore cannot recreate the already-lost historical hidden fact IDs/provenance. The new import button can load it for development continuity, but it is not equivalent to an exact ledger recovery and cannot be used as the clean final DOB/time measurement freeze.

From this deployment forward, successful interview state is automatically backed up browser-side with the exact hidden ledger, so an ordinary Railway restart no longer requires restarting the interview from scratch on the same browser. Downloaded exact recovery JSON additionally supports manual restoration when browser-local state is unavailable.
