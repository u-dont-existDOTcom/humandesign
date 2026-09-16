# Life Patterns current state — 2026-09-16

V2 independent semantic review: **PASS**. Semantic change required: `false`.

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER FINALIZATION-FLOW RETEST, THEN FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, participant authority over person-level patterns, and the episode-fact/person-pattern firewall.

No private owner interview narrative is stored in repository state.

## Current participant-facing flow

`participant-led characteristic evidence -> all-answer/all-dimension neutral coverage assessment -> dynamic information-gain follow-up for remaining gaps -> participant synthesis judgment -> finite Continue interview path -> explicit missingness -> local SHA-256 freeze/export -> owner-only post-freeze DOB/time recovery regression`

The runtime receives no chart, birth target, expected answer direction, target mapping, candidate score/rank, or historical AstroHD crosswalk.

## Fixed measurement, dynamic interview

The active `life-patterns-recoverability-coverage-v2` blueprint contains **23 required neutral dimensions**. These are fixed constructs, not a fixed question order.

Current rules:

- one natural answer may satisfy multiple dimensions;
- completed dimensions are skipped;
- partial dimensions ask only for the missing discriminator;
- still-open material is selected by expected information gain and conversational continuity;
- accepted prior information is reused for planning across later questions without becoming new evidence;
- canonical screeners are fallback wording, not the participant script;
- broad self-labels retain their semantic scope rather than being collapsed to the first investigated subdomain;
- familiar-observer/self and inner/outer distinctions are used when they materially change interpretation;
- the participant-facing progress card exposes approximate percent complete plus rough remaining-question/time ranges without revealing the category queue.

Coverage states remain `unassessed`, `partial`, `sufficient`, `unknown`, `inapplicable`, `declined`; silence is never absence.

## Synthesis-review frontier

Free-form chat remains available whenever a synthesis is unsettled. Conversational explanation and exact replacement wording remain separate paths; exact wording has Back navigation.

The generic continue-discovery choice is now a single visible **Keep investigating** action. A participant who already knows what is wrong can say so directly in chat. Internal refinement modes are no longer exposed as two confusing generic buttons.

## Transactional finalization repair

Owner use exposed `proposal ... has multiple adjudications` around synthesis acceptance.

The recoverability layer had previously mutated the core participant adjudication before running a fallible post-decision coverage assessment. Those dependent steps lacked one enclosing transaction, so a coverage failure could leave an adjudication committed while the browser reported failure. Retrying could then attempt a second adjudication of the same proposal.

The live candidate now:

- snapshots full session/core state before finalization;
- rolls back the whole response if any dependent post-decision work fails;
- clears the active proposal pointer only after a successful response;
- blocks repeated in-flight decision clicks in the browser.

Receipt: `state/LIFE-PATTERNS-v2-OWNER-FINALIZATION-FLOW-REPAIR-2026-09-16.md`.

## Finite post-acceptance continuation

The visible `Explore another pattern` action is removed. **Continue interview** is the primary next action after acceptance. The adaptive interviewer itself may move into a new pattern/domain when that is the highest-information unresolved material, but the participant is no longer offered an unlimited parallel branch that undermines the finite completion horizon.

## Owner DOB/time recoverability criterion

A fresh frozen interview must preserve enough behavioral information to reproduce the historical owner AstroHD development result. Coverage alone cannot pass.

Historical benchmark:

- exact recorded moment hourly rank no worse than **#2**;
- correct date remains **#1 distinct refined neighborhood**;
- refined peak remains within **11 minutes** of the recorded time.

Frozen baseline: `reference/research/life_patterns_astrohd_owner_recovery_baseline_v1.json`.
Executable gate: `src/hdmatch/evaluation/life_patterns_owner_recovery_gate.py`.
Development-only post-freeze crosswalk: `reference/research/life_patterns_astrohd_owner_recovery_crosswalk_v1.json`.

## Pre-scoring freeze

**Freeze/export measurement** creates a local SHA-256-frozen JSON bundle from participant-adjudicated results and aggregate coverage. Only after freeze may the narrowly authorized owner-self historical recovery regression run.

## Mission Control

Owner-explicit logic corrections are durably captured on the UDA branch `feedback/mission-control-logic-corrections-20260915`, draft PR #127, with truth state **`CAPTURED_BRANCH_ONLY`**.

Latest correction artifact: `feedback/mission-control/SDF-20260916-LIFE-PATTERNS-FINALIZATION-CHOICE-FLOW-010.json`.

## Verification / deployment

- application head: `cef6ad16546448355a3e624016b46333b2730573`;
- finalization-flow regression head: `d68380b0d33ace513f6b705cd27283e2fe1aa79f`;
- GitHub Actions run `35044113034`: **SUCCESS** — tests, Ruff, strict mypy;
- Railway deployment `6126c7b7-d207-4552-a12f-65304be89ea5`: **SUCCESS** from exact application head `cef6ad16546448355a3e624016b46333b2730573`;
- application startup complete;
- `/healthz`: HTTP **200 OK**.

The development surface remains passwordless under prior explicit owner authority. Passwordless development access does not authorize external participant recruitment/collection.

## Current gate

Owner consumer-seam retest:

1. refresh/reopen the live app;
2. accept a surfaced synthesis once; no multiple-adjudication error should appear;
3. verify only one generic investigation action is visible and direct chat correction remains available;
4. after acceptance, verify Continue interview is primary and Explore another pattern is absent;
5. continue until the fixed measurement surface is complete or explicitly missing;
6. freeze/export the measurement;
7. only after freeze, run the owner-self historical DOB/time recovery procedure;
8. if recovery is worse than the benchmark, revise the instrument rather than weakening the criterion.

General target-model activity remains closed. Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware questioning, external-participant target scoring, merge/release, publication, production expansion, and unapproved spending.

**There was never a completion policy.**
