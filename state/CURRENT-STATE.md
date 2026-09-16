# Current state

## Life Patterns — 2026-09-16

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER RECOVERY/PROGRESS/LIVENESS RETEST, THEN FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

No private owner interview narrative is committed. Repository state contains abstract product findings, neutral measurement definitions, mechanical regressions, and privacy-bounded owner-authorized logic-correction receipts only.

## Current participant-facing architecture

**Target-aware instrument design / target-blind runtime / fixed 23-dimension recoverability surface / dynamic information-gain questioning / in-thread adaptive progress / ephemeral working synthesis until participant judgment / transactional finalization / exact browser-local hidden-ledger audit/recovery / importable recovery snapshots / explicit long-operation liveness / local pre-scoring freeze / owner-only post-freeze DOB-time recovery regression.**

Current behavior includes:

- person-specificity: recurrence alone is not useful if it is merely a high-base-rate human regularity;
- no arbitrary episode/counterexample quota;
- observer/self, inner/outer, context, scope, developmental, timing, and other neutral discriminators only when decision-changing;
- global-label scope preservation;
- fixed scientific coverage with adaptive order and wording;
- prior answers may satisfy multiple dimensions and should prevent duplicate later questions;
- long-thread planning keeps the practical conversation in view and treats semantic rewording as repetition;
- free-form chat in every nonfinal synthesis-review state;
- one visible generic continuation: **Keep investigating**;
- `Continue interview` as the finite default after a settled pattern; no visible unlimited `Explore another pattern` branch;
- progress during an active thread, expressed as approximate percent plus **measurement areas still open**, not a fictitious question count;
- working syntheses remain ephemeral until participant judgment and refinement can end with an actual updated synthesis;
- exact hidden-ledger working state is automatically checkpointed browser-side and can be downloaded/imported for audit/recovery;
- audit/recovery exactness is explicitly not scientific validity;
- page scrolling follows the next participant action and a vertical scrollbar is always available;
- long-running operations expose a visible **Working on it…** state;
- participant authority over durable person-level patterns.

Runtime elicitation receives no participant chart, birth target, expected answer direction, target-model mapping, candidate score/rank, or historical AstroHD crosswalk.

## Latest owner consumer-seam failure: restored progress + request liveness

Direct owner testing of the reconstructed-recovery path exposed a second-order recovery defect.

Observed behavior:

1. transcript reconstruction could take several seconds while the UI looked effectively idle;
2. **Yes — keep that** could take several seconds without a clear in-flight message;
3. the Interview progress card remained at `Preparing…` after recovery;
4. after acceptance, `Continue interview` could incorrectly report that coverage was complete.

The owner supplied a private audit/recovery snapshot. It showed that the interview was materially incomplete (only a small minority of the 23 required dimensions were complete), so the completion message was demonstrably a client-state bug rather than a valid scientific result. The private snapshot itself is not committed.

### Generating condition

The recovery path restored answer/coverage state but bypassed the normal fresh-session bootstrap that loads the fixed 23-dimension coverage blueprint. Thus the client had restored coverage rows but an empty reference universe:

- the progress renderer interpreted the blueprint as not initialized and stayed at `Preparing…`;
- `incompleteCoverage()` evaluated an empty blueprint as zero missing dimensions and could therefore emit a false completion claim.

Separately, request liveness existed internally while several model-backed operations had no persistent user-visible in-flight surface. Disabled controls or delayed responses were not enough feedback.

### Repair

Receipt: `state/LIFE-PATTERNS-v2-OWNER-RECOVERY-PROGRESS-LIVENESS-REPAIR-2026-09-16.md`.

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_liveness_ui.py`;
- `src/hdmatch/api/life_patterns_v2_owner_liveness.py`;
- deployment wrapper now serves the liveness-aware app.

Current behavior:

- every exact or transcript-only recovery path loads the real coverage blueprint before restored progress is rendered;
- `Continue interview` explicitly ensures the blueprint is loaded before it evaluates whether anything remains open;
- a dedicated indeterminate request-liveness card appears during slow operations;
- recovered-transcript reconstruction displays **Rebuilding the recovered interview and preparing a synthesis…**;
- participant acceptance displays **Saving that and updating interview progress…**;
- `Continue interview` displays **Choosing the next useful question…**;
- recovery import / clean-start operations also expose an in-flight state.

Scientific progress and request-liveness progress are intentionally separate concepts.

## Recovery architecture

Receipt: `state/LIFE-PATTERNS-v2-OWNER-EXACT-RECOVERY-IMPORT-SCROLL-REPAIR-2026-09-16.md`.

The browser preserves a checksum-bound snapshot of the exact current *working* hidden ledger for crash recovery/audit. A working snapshot may contain a defect; exact restoration proves state preservation, not correctness. It is not canonical measurement data and is not the scientific freeze.

The working snapshot contains the resumable hidden state needed for audit:

- conversation with turn IDs;
- current episode/boundary/pattern-focus state;
- full v2 record including fact revision lineage and source-provenance hashes;
- proposal support / active proposal state;
- current ephemeral synthesis draft;
- latest in-thread progress report.

Private narrative remains browser-local unless the participant explicitly downloads/uploads a checkpoint. It is not persisted to Git or a Railway volume.

### Older visible-transcript recovery boundary

Older files that never contained the hidden ledger can restore their visible conversation for development continuity. The app can reconstruct a new explicitly non-scientific working ledger from exact participant utterances and then produce a current synthesis or needed follow-up, but that reconstructed ledger is not represented as the lost original ledger and cannot become the clean scientific freeze.

## Progress / scrolling corrections

The progress card reports **open measurement areas**, not a question count. One natural answer may cover several areas; a partial area may require additional turns. The time estimate is explicitly approximate.

The UI forces a vertical scrollbar and scrolls toward the next actionable surface—answer composer, synthesis judgment, recovery action, or continuation controls—rather than merely the newest chat bubble.

## Long-thread resilience

Active safeguards remain:

- planner/refinement context retains the practical thread;
- answered semantic distinctions must not be re-asked under new wording;
- one thread must not be expanded to exhaust every adjacent standardized dimension;
- refinement may end with a current `surface_hypothesis` rather than only saying questioning is done;
- tentative syntheses stay out of the durable v2 record until judgment;
- coverage can update before adjudication;
- participant finalization remains transactional.

Receipt: `state/LIFE-PATTERNS-v2-OWNER-LONG-THREAD-RESILIENCE-REPAIR-2026-09-16.md`.

## Verification / live deployment

Exact liveness-aware application head: `625ec596fd4098096357f5cb3c7bee522ce4d5ea`.

Regression checkpoint head: `a71ab72d39dd46c0793ac5ec207640bf62186e21`.

GitHub Actions run `35115906379`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `54e829be-6fe5-4570-9321-609468b414ff`: **SUCCESS** from exact application head `625ec596fd4098096357f5cb3c7bee522ce4d5ea`.

Runtime evidence:

- application startup complete;
- `GET /healthz` returned HTTP **200 OK**.

The development surface remains passwordless under prior explicit owner authority. This does not authorize external participant collection/recruitment.

## Recoverability measurement and hard owner criterion

Active blueprint: `life-patterns-recoverability-coverage-v2`, with 23 required neutral dimensions and explicit missingness states.

A fresh completed interview still fails if it does not preserve enough behavioral information for the historical owner AstroHD recovery:

- exact recorded moment hourly rank no worse than **#2**;
- correct date remains the **#1 distinct refined neighborhood**;
- refined peak remains within **11 minutes** of recorded time.

Coverage completion alone cannot pass. The fresh interview must be frozen/exported locally before the narrowly authorized owner-self AstroHD recovery is run.

## Mission Control correction capture

Owner-explicit logic corrections remain durably captured on the UDA branch `feedback/mission-control-logic-corrections-20260915`, draft PR #127. Current truth remains **`CAPTURED_BRANCH_ONLY`**.

Latest privacy-bounded artifact: `feedback/mission-control/SDF-20260916-LIFE-PATTERNS-LIVENESS-AND-BLUEPRINT-HYDRATION-015.json`.

## Current gate

Owner consumer-seam retest is next. Immediate checks:

1. refresh/reopen the recovered development checkpoint;
2. progress should resolve to a real approximate percentage/open-area count rather than remain at `Preparing…`;
3. reconstruction, acceptance, and continue-interview operations should visibly show an in-flight working state;
4. after accepting the recovered synthesis, `Continue interview` must advance into remaining measurement areas rather than falsely saying coverage is complete;
5. confirm long threads still avoid semantic duplicate questions and can end in an actual current synthesis;
6. once the product seam passes, complete a fresh target-blind interview, Freeze/export measurement, then run the owner-self historical AstroHD recovery regression.

Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware elicitation, external-participant target scoring, merge/release, publication/validation claims, production expansion, and unapproved spending.

**There was never a completion policy.**
