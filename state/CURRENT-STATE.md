# Current state

## Life Patterns — 2026-09-17

Active task: `life-patterns-v2-astrohd-recoverability-owner-retest` — **OWNER CONTINUOUS-FLOW / QUESTION-QUALITY RETEST, THEN FRESH TARGET-BLIND MEASUREMENT + POST-FREEZE RECOVERY REQUIRED**.

PR #24 remains **draft / open / unmerged**.

## Accepted scientific substrate

The accepted v2 hidden evidence contract remains unchanged: open-world episode facts, participant-authoritative person-level patterns, append-only correction/provenance, genuine-absence gating, immutable evidence timing, target-theory blindness, and the episode-fact/person-pattern firewall.

No private owner interview narrative is committed. Private interview content remains browser-local unless the owner explicitly exports/uploads an audit/recovery checkpoint.

## Current participant-facing architecture

**Fixed 23-dimension target-blind recoverability surface / one continuous adaptive interview / same-session hidden ledger across measurement areas / separate pre-send question admission / automatic cross-area continuation / persistent Finish-for-now escape / direct participant self-report distinguished from interviewer inference / progress and liveness at the active end / exact browser-local hidden-ledger audit/recovery / local pre-scoring freeze / owner-only post-freeze DOB-time recovery regression.**

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

## Latest owner correction: continuous flow and question admission

An owner-supplied exact browser audit/recovery checkpoint was inspected privately. It showed a key architectural cause of repeated questions: the current server snapshot contained only the newest measurement-area conversation, while earlier interview knowledge survived mainly as compressed client-side pattern/coverage summaries. The private checkpoint itself is not committed.

The owner also identified that the ordinary `Continue interview` checkpoint was unnecessary, `Finish for now` should remain available instead, some questions still lacked obvious information value, and the explanatory synthesis-review button duplicated the free-form textbox.

Receipt: `state/LIFE-PATTERNS-v2-OWNER-CONTINUOUS-FLOW-QUESTION-ADMISSION-2026-09-17.md`.

### Same-session continuation

Normal progression no longer creates a fresh server session at each measurement-area boundary. The same server session continues, so the conversation, hidden ledger, corrections, and operative facts accumulate through the interview.

A bounded participant-answer memory is also preserved in browser audit/recovery state and supplied to cross-area planning alongside aggregate coverage, accepted patterns, current conversation, and operative facts.

### Explicit pre-send question-quality gate

The prior system had information-gain/redundancy language in the generator prompt, but no independent admission boundary. Every generated question now receives a separate pre-send check.

A question is admitted only if it names a genuinely missing discriminator, has materially different plausible answers that could change the retained person model or a still-open measurement distinction, is answerable from lived experience, is not semantically already answered, and is worth another participant turn.

The admission pass may **admit**, **replace**, or **stop** an in-thread question. Cross-area questions get an additional final admission/replacement pass using the accumulated answer memory and measurement state. Generic, normative, ordinary-human-default, redundant, or questionnaire-for-its-own-sake prompts should therefore be replaced before they reach the participant.

### Continuous participant flow

After local topic completion, automatic recording of a direct participant-authored pattern, or successful judgment of a genuine interviewer inference, the app automatically chooses the next admitted question. There is no routine `Continue interview` click. The old control is hidden and is exposed only as a retry if next-question selection actually fails.

`Finish for now` is now a persistent fixed on-screen control. Pausing saves the current browser audit/recovery state.

### Synthesis review controls

The ordinary textbox is the sole channel for normal synthesis feedback: disagreement, explanation, correction, nuance, or missing context.

`Close — I’ll explain what needs changing` is hidden because it duplicated that textbox action.

`Write exact wording to record` remains because it has a different contract: the participant is supplying literal replacement wording to store unchanged rather than asking the interviewer to interpret conversational feedback.

Accept / reject / keep-investigating / unresolved retain their distinct workflow meanings.

## Recovery boundary

Exact browser recovery preserves the current working hidden ledger plus client-side answer memory, coverage aggregation, and workflow phase. A restored checkpoint remains unvalidated and cannot become the scientific freeze merely because it resumes exactly.

Older snapshots created before continuous-flow answer memory cannot reconstruct participant utterances that were never contained in those snapshots. The current architecture prevents that loss going forward by keeping one accumulating session and answer memory.

## Verification / deployment

Current continuous-flow application head: `1b4f32ba16693df2a645fecb64dc00b10989cd62`.

GitHub Actions run `35234856279`: **SUCCESS**.

- full unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `2503e395-714d-487d-9d83-cf6e4b97aad6`: **SUCCESS** from the exact application head.

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

Latest privacy-bounded correction: `feedback/mission-control/SDF-20260917-LIFE-PATTERNS-CONTINUATION-QUESTION-ADMISSION-019.json`.

## Current gate

Owner consumer-seam retest:

1. refresh/recover the current development interview;
2. ordinary completion should flow automatically into the next question without a Continue checkpoint;
3. Finish for now should remain visible;
4. previously answered material should not be asked again under new wording;
5. candidate questions should be replaced/suppressed when they fail the explicit information-value/redundancy gate;
6. normal synthesis feedback should use the textbox, while exact literal replacement remains a separate explicit action;
7. progress, exact recovery, direct-report/inference handling, and fast adjudication must remain intact;
8. once those product seams pass, complete a fresh target-blind interview, Freeze/export measurement, then run the owner-self historical AstroHD recovery regression.

Focused completion command:

`python -m pytest tests/unit/test_life_patterns_v2_owner_continuous_flow.py tests/unit/test_life_patterns_v2_owner_natural_flow.py tests/unit/test_life_patterns_v2_owner_liveness.py tests/unit/test_life_patterns_v2_owner_import_resume.py tests/unit/test_life_patterns_v2_owner_persistent.py tests/unit/test_life_patterns_v2_owner_resilient.py tests/unit/test_life_patterns_v2_owner_finalization_flow.py tests/unit/test_life_patterns_v2_owner_dynamic_coverage.py tests/unit/test_life_patterns_v2_owner_scope.py tests/unit/test_life_patterns_v2_owner_recoverability.py tests/unit/test_life_patterns_v2_owner_recoverability_ui.py tests/unit/test_life_patterns_owner_recovery_gate.py -q`

Still unauthorized: external participant collection/recruitment, automated participant coding, chart-aware elicitation, external-participant target scoring, merge/release, publication/validation claims, production expansion, and unapproved spending.

**There was never a completion policy.**
