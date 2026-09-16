# Current state

## Life Patterns — 2026-09-16

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER FINALIZATION-FLOW RETEST, THEN FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, participant-adjudicated person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

No private owner interview narrative is committed. Repository state contains only abstract product findings, neutral measurement definitions, mechanical regressions, and privacy-bounded owner-authorized logic-correction receipts.

## Current participant-facing architecture

**Target-aware instrument design / target-blind runtime / fixed 23-dimension recoverability surface / dynamic information-gain questioning / visible adaptive progress / transactional synthesis finalization / local pre-scoring freeze / owner-only post-freeze DOB-time recovery regression.**

The interviewer currently preserves:

- person-specificity: recurrence alone is not useful if it is merely a high-base-rate human regularity;
- adaptive burden: no arbitrary episode/counterexample quota;
- self-view versus familiar-observer and inner versus outer distinctions when informative;
- global-label scope: a broad claim cannot be silently narrowed to the first investigated subdomain or generalized beyond evidence;
- dynamic cross-thread reuse: prior accepted information prevents redundant later questioning, but internal planning context is not participant evidence;
- fixed scientific coverage with adaptive order/wording: one answer may satisfy several dimensions; completed material is skipped; partial material asks only for the missing discriminator;
- free-form chat in every nonfinal synthesis-review state;
- separate explanatory feedback versus exact-wording authoring, with Back navigation;
- a persistent progress bar with approximate percent complete plus rough remaining-question/time ranges;
- participant authority over person-level synthesis;
- a finite default continuation after every settled pattern.

Runtime elicitation receives no participant chart, birth target, expected answer direction, target-model mapping, candidate score/rank, or historical AstroHD crosswalk.

## Latest owner-found defect: synthesis finalization could half-commit

Direct owner use surfaced `proposal ... has multiple adjudications` around final synthesis acceptance.

Causal path:

1. the core participant adjudication mutated the in-memory record;
2. the recoverability layer then ran a fallible post-decision coverage assessment;
3. those two operations had no outer transaction;
4. if coverage failed, the browser saw an error even though the adjudication could remain committed;
5. retrying naturally attempted a second adjudication of the same proposal, which the accepted v2 contract correctly rejects.

The browser also lacked an in-flight decision guard, so repeated clicks were another duplicate-request path.

### Repair

The live candidate now wraps participant decision + post-decision coverage work in one session transaction. Any failure restores the complete pre-decision state. A successful response clears the active proposal pointer. The browser ignores repeated in-flight decisions and temporarily disables synthesis controls during finalization.

Regression coverage includes rollback after a simulated post-decision failure and successful proposal closure.

Receipt: `state/LIFE-PATTERNS-v2-OWNER-FINALIZATION-FLOW-REPAIR-2026-09-16.md`.

## Simplified synthesis choices

The prior visible distinction between `Keep trying to pin it down` and `No — keep investigating` leaked internal refinement-state semantics into participant choice. Both meant, at product level, "do not settle yet; gather more information."

The visible generic continuation is now simply **Keep investigating**. If the participant already knows what is wrong or missing, the always-visible chat box / `Close — I’ll explain what needs changing` path is the explicit correction route. `Reject and stop this thread`, `Leave it unresolved for now`, and exact-wording editing retain separate meanings.

## Finite post-acceptance continuation

The visible `Explore another pattern` branch has been removed from the participant flow. The normal post-acceptance action is **Continue interview**, which lets the target-blind information-gain selector choose the next unresolved material. If a genuinely new pattern is the best next question, the interviewer can reach it dynamically without an unlimited parallel branch.

This preserves the meaning of the progress horizon and prevents the UI from presenting an effectively endless optional questionnaire beside a finite scientific instrument.

## Recoverability measurement + progress

Active blueprint: `life-patterns-recoverability-coverage-v2`, with **23 required neutral dimensions** and coverage states `unassessed`, `partial`, `sufficient`, `unknown`, `inapplicable`, `declined`.

The participant-facing progress card keeps category names/order hidden while exposing an approximate completion horizon. Its question/time estimate is deliberately rough because one answer may close several dimensions and answer length varies.

## Owner hard criterion: preserve DOB/time recovery

The new interview fails if a fresh frozen result no longer preserves enough behavioral information for the historical owner AstroHD recovery.

Historical development benchmark:

- exact recorded moment hourly rank no worse than **#2**;
- correct date remains the **#1 distinct refined neighborhood**;
- refined peak remains within **11 minutes** of recorded time.

Frozen baseline: `reference/research/life_patterns_astrohd_owner_recovery_baseline_v1.json`.
Executable gate: `src/hdmatch/evaluation/life_patterns_owner_recovery_gate.py`.
Development-only crosswalk: `reference/research/life_patterns_astrohd_owner_recovery_crosswalk_v1.json`.

Coverage completion alone cannot pass this gate.

## Pre-scoring freeze

**Freeze/export measurement** creates a local SHA-256-frozen JSON bundle from participant-adjudicated results and aggregate coverage. Target-aware owner scoring occurs only after this local freeze.

## Mission Control correction capture

Owner-explicit logic corrections are durably captured on the UDA branch `feedback/mission-control-logic-corrections-20260915`, draft PR #127. Current truth: **`CAPTURED_BRANCH_ONLY`**.

Latest artifact: `feedback/mission-control/SDF-20260916-LIFE-PATTERNS-FINALIZATION-CHOICE-FLOW-010.json`.

## Verification / live deployment

Current application head: `cef6ad16546448355a3e624016b46333b2730573`.

Finalization-flow regression head: `d68380b0d33ace513f6b705cd27283e2fe1aa79f`.

GitHub Actions run `35044113034`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `6126c7b7-d207-4552-a12f-65304be89ea5`: **SUCCESS** from application head `cef6ad16546448355a3e624016b46333b2730573`.

Runtime evidence:

- application startup completed;
- `GET /healthz` returned HTTP **200 OK**.

The development surface remains passwordless under prior explicit owner authority. This does not authorize external participant collection/recruitment.

## Current gate

Owner consumer-seam retest is next:

1. refresh/reopen the live app; old in-memory sessions from the prior deployment are not a valid retest;
2. accept one surfaced synthesis once and verify no `multiple adjudications` error appears;
3. confirm there is one visible generic continuation: **Keep investigating**;
4. confirm a specific objection can still be typed directly and exact-wording editing remains reversible;
5. after acceptance, confirm **Continue interview** is the primary next action and `Explore another pattern` is absent;
6. continue the dynamic interview while checking progress and non-redundancy;
7. freeze/export the completed measurement;
8. only after freeze, run the narrowly authorized owner-self historical DOB/time recovery regression;
9. if recovery is worse, revise the instrument rather than weakening the benchmark.

Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware elicitation, external-participant target scoring, merge/release, publication/validation claims, production expansion, and unapproved spending.

**There was never a completion policy.**
