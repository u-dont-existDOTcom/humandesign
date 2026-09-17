# Current state

## Life Patterns — 2026-09-17

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER CONTINUOUS-FLOW / QUESTION-QUALITY / SINGLE-FEEDBACK-CHANNEL RETEST, THEN FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, participant-authoritative person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

No private owner interview narrative is committed. Private interview content remains browser-local unless the owner explicitly exports/uploads an audit/recovery checkpoint.

## Current participant-facing architecture

**Fixed 23-dimension target-blind recoverability surface / one continuous adaptive interview / same-session hidden ledger across measurement areas / separate pre-send question admission / automatic cross-area continuation / persistent Finish-for-now escape / direct participant self-report distinguished from interviewer inference / one free-form synthesis correction channel / progress and liveness at the active end / exact browser-local hidden-ledger audit/recovery / local pre-scoring freeze / owner-only post-freeze DOB-time recovery regression.**

Current rules:

- simple is fine; generic/high-base-rate is not a useful Life Pattern;
- a person-specific pattern already explicitly stated by the participant may be recorded from its original source without a redundant approval screen;
- any interviewer-added synthesis/inference still requires participant judgment;
- fixed scientific coverage does not imply fixed question order or category-by-category interviewing;
- one natural answer may satisfy several measurement dimensions;
- prior answers must suppress semantically duplicate later questions;
- no arbitrary episode/counterexample quota;
- broad participant labels preserve their intended cross-domain scope;
- progress reports approximate percent plus measurement areas still open, not a question count;
- browser audit/recovery snapshots preserve potentially defective working state for debugging; exactness does not imply scientific validity;
- participant decisions do not wait on a redundant second LLM coverage call.

Runtime elicitation receives no participant chart, birth target, expected answer direction, target-model mapping, candidate score/rank, or historical AstroHD crosswalk.

## Latest owner evidence and correction

The owner supplied an exact browser audit/recovery checkpoint. It was inspected privately and is not committed. The checkpoint showed that the then-current server snapshot held only the newest measurement-area conversation while earlier knowledge survived mainly as accepted result wording and aggregate coverage metadata. This directly explained how a question could be substantively answered earlier and nevertheless be selected again after crossing a measurement-area boundary.

The owner also corrected three product-flow assumptions:

1. an internal local-topic boundary should not require a participant `Continue interview` click when the next normal action is uniquely determined;
2. generation-time instructions such as “ask only useful questions” are insufficient if a low-value question can still reach the participant; the candidate question itself needs an admission check;
3. backend distinctions among explanatory correction and exact replacement wording do not justify multiple participant text-entry controls when one textbox can express both intents.

Receipt: `state/LIFE-PATTERNS-v2-OWNER-CONTINUOUS-FLOW-QUESTION-ADMISSION-2026-09-17.md`.

## Same-session continuation and recoverable answer memory

Normal cross-area continuation keeps the same server session, conversation, operative facts, corrections, and hidden ledger instead of creating a fresh coverage session.

Browser audit/recovery state carries a bounded participant-answer memory plus a question-admission audit log. The continuation planner receives that memory together with current conversation, operative facts, accepted participant-authoritative patterns, aggregate coverage, and still-open neutral dimensions.

For older exact browser snapshots that predate explicit answer memory, recovery now seeds redundancy memory from accepted result wording plus any raw participant turns still present in the server snapshot. This cannot recreate old raw answers that were never persisted anywhere, but it uses every recoverable prior participant-authoritative statement to reduce duplicate questioning.

## Question admission

Normal follow-up questions pass a separate pre-send gate after generation. The gate may admit, replace, or stop the question.

A displayed question must identify a genuinely missing discriminator, have materially different plausible answers capable of changing the retained person model or still-open measurement distinction, be answerable from lived experience, not be semantically already answered, and be worth another participant turn.

Cross-area questions receive a final admission/replacement pass using the broader answer memory and accumulated measurement state. Generic, ordinary-human-default, vague, redundant, normative, or questionnaire-for-its-own-sake candidates should be replaced before display.

Admission rationale is stored only as audit/planning metadata in the browser recovery bundle; it is not participant evidence.

## Continuous participant flow

After local topic completion, direct participant-authored pattern recording, or successful adjudication of a real interviewer inference, the app automatically selects the next admitted question. There is no routine `Continue interview` checkpoint. A Continue-style control appears only as a retry if next-question selection fails.

`Finish for now` remains a persistent visible pause control throughout the interview and saves the current browser checkpoint.

## Synthesis review

The always-visible textbox is now the **single participant text-entry channel** for an inferred synthesis. It can carry disagreement, explanation, correction, nuance, missing context, or participant-authored replacement wording.

Both `Close — I’ll explain what needs changing` and `Edit exact wording myself` are hidden. If literal wording is intended, the participant can state that intent in the same textbox rather than entering another edit mode.

Buttons remain only for genuinely distinct state transitions such as accepting the inference, asking the interviewer to keep investigating, rejecting/stopping, or leaving it unresolved.

## Recovery boundary

Exact browser recovery preserves the current working hidden ledger plus client-side answer memory, coverage aggregation, question-admission audit metadata, and workflow phase. A restored checkpoint remains unvalidated and cannot become the scientific freeze merely because it resumes exactly.

Private narrative is not persisted to Git or a Railway volume.

## Verification / live deployment

Exact deployed application head: `56796a842ef3bc453f12f65c138458656e441490`.

Regression checkpoint: `f861ac5d26f6e11aceb3c69804e416e15db612c9`.

GitHub Actions run `35239835457`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `3588d15c-4865-4c0d-ba37-331d5ac84483`: **SUCCESS** from the exact application head.

Runtime evidence: application startup complete; `GET /healthz` returned HTTP **200 OK**.

The development surface remains passwordless under prior explicit owner authority. This does not authorize external participant collection/recruitment.

## Recoverability criterion

Active blueprint: `life-patterns-recoverability-coverage-v2`, 23 required neutral dimensions with explicit missingness states.

Coverage completion alone cannot pass. A fresh target-blind interview must be frozen/exported locally before the narrowly authorized owner-self historical AstroHD recovery regression, which still requires:

- exact recorded moment hourly rank no worse than **#2**;
- correct date as the **#1 distinct refined neighborhood**;
- refined peak within **11 minutes** of recorded time.

## Mission Control capture

Owner-explicit logic corrections remain durably captured on the UDA branch `feedback/mission-control-logic-corrections-20260915`, draft PR #127, truth state **`CAPTURED_BRANCH_ONLY`**.

Current records for this correction chain:

- `feedback/mission-control/SDF-20260917-LIFE-PATTERNS-CONTINUATION-QUESTION-ADMISSION-019.json`;
- `feedback/mission-control/SDF-20260917-LIFE-PATTERNS-SINGLE-SYNTHESIS-TEXT-CHANNEL-020.json`.

The second record corrects the first repair's remaining UI over-separation: a distinct backend intent does not automatically require a distinct participant control.

## Current gate

Owner consumer-seam retest:

1. refresh/recover the current development interview;
2. ordinary completion should flow automatically into the next admitted question without a Continue checkpoint;
3. Finish for now should remain visible;
4. previously answered material should not be asked again under new wording;
5. low-value candidate questions should be replaced/suppressed by the pre-send admission gate;
6. inferred-synthesis correction should use one textbox rather than multiple edit modes;
7. progress, exact recovery, direct-report/inference handling, and fast adjudication must remain intact;
8. once those product seams pass, complete a fresh target-blind interview, Freeze/export measurement, then run the owner-self historical AstroHD recovery regression.

Focused completion command:

`python -m pytest tests/unit/test_life_patterns_v2_owner_continuous_flow.py tests/unit/test_life_patterns_v2_owner_natural_flow.py tests/unit/test_life_patterns_v2_owner_liveness.py tests/unit/test_life_patterns_v2_owner_import_resume.py tests/unit/test_life_patterns_v2_owner_persistent.py tests/unit/test_life_patterns_v2_owner_resilient.py tests/unit/test_life_patterns_v2_owner_finalization_flow.py tests/unit/test_life_patterns_v2_owner_dynamic_coverage.py tests/unit/test_life_patterns_v2_owner_scope.py tests/unit/test_life_patterns_v2_owner_recoverability.py tests/unit/test_life_patterns_v2_owner_recoverability_ui.py tests/unit/test_life_patterns_owner_recovery_gate.py -q`

Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware elicitation, external-participant target scoring, merge/release, publication/validation claims, production expansion, and unapproved spending.

**There was never a completion policy.**
