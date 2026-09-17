# Life Patterns v2 — continuous-flow question-admission repair — 2026-09-17

## Owner findings

Direct owner testing identified four coupled participant-facing failures:

1. the next measurement-area question could ask something already answered earlier in the interview;
2. a routine `Continue interview` checkpoint required a click even though continuation was the only normal nonterminal action;
3. some questions remained low-value despite existing information-gain language in the interviewer prompt;
4. `Close — I’ll explain what needs changing` duplicated the always-available free-form textbox during synthesis review, while exact literal replacement wording is a genuinely different intent.

The owner supplied an exact browser audit/recovery checkpoint. It was inspected privately and is not committed. It showed the current server snapshot carrying only the current measurement-area conversation while earlier interview information lived mainly in client-side completed-result and aggregate-coverage summaries. That architecture could lose exact conversational memory across area boundaries even though compressed coverage metadata survived.

## Generating conditions

### Cross-area duplicate questions

The prior continuation route called `/coverage/next-session`, created a brand-new server session, and selected the next question from aggregate coverage plus accepted pattern summaries. Those summaries are useful planning metadata but are not a substitute for the participant's earlier answers. A construct could therefore be semantically answered yet remain available to be asked again.

### Redundant Continue checkpoint

Local topic completion and successful pattern adjudication exposed an internal workflow boundary as a participant action. In ordinary flow there was exactly one normal next operation: choose the next useful still-open distinction. Requiring a click added burden without adding participant authority.

### Weak question-quality enforcement

The interviewer already had prompt instructions to ask only decision-changing, nonredundant questions. That was a generation preference, not an independent admission boundary. A generated question could therefore reach the participant without a second check that identified the missing discriminator and demonstrated that materially different answers would alter the retained person model.

### Duplicate synthesis-feedback controls

The free-form textbox already accepted ordinary explanation, correction, nuance, and disagreement. `Close — I’ll explain what needs changing` merely focused that same textbox, so it duplicated the existing semantic action. Exact participant-authored replacement wording remains distinct because it requests literal storage rather than conversational interpretation.

## Repair

### One continuous recoverable session

Normal cross-area continuation now advances the same server session. The hidden ledger and conversation therefore continue accumulating instead of resetting at every measurement-area boundary.

Browser audit/recovery state also carries a bounded participant-answer memory. The continuation planner receives:

- still-open measurement dimensions;
- aggregate coverage metadata;
- accepted participant-authoritative pattern wording;
- the bounded participant-answer memory;
- the current continuous server conversation;
- operative hidden-ledger facts.

This memory is for redundancy suppression and planning; evidence admission remains governed by the existing hidden-ledger/source-provenance rules.

### Automatic continuation

After:

- a locally completed measurement area;
- an automatically recorded direct participant-authored person-specific pattern; or
- a successful participant judgment of a genuine interviewer inference,

the app automatically chooses the next admitted question. The ordinary `Continue interview` button is hidden. It appears only as an explicit retry frontier if next-question selection fails.

`Finish for now` is moved to a persistent fixed on-screen control and remains available throughout the interview. Pausing saves the current browser audit/recovery checkpoint.

### Explicit pre-send question admission

Questions now pass a separate model call before display.

For in-thread follow-ups the admission pass may:

- **admit** the proposed question;
- **replace** it with one better question; or
- **stop** the local thread when no useful question remains.

Admission requires all of the following:

1. the substantive question has not already been answered, including under different wording;
2. there is a named missing discriminator;
3. materially different plausible answers would change the person-specific characterization, scope, boundary, timing, mechanism, or a still-open measurement distinction;
4. the question is answerable from ordinary lived experience;
5. the expected information gain is worth another participant turn.

Cross-area continuation receives an additional final admission/replacement pass using the prior answer memory, coverage state, accepted patterns, current conversation, and operative facts. It must reject or replace vague, generic, normative, ordinary-human-default, redundant, or questionnaire-for-its-own-sake questions.

### Synthesis review simplification

The explanatory-revision button is hidden. Synthesis review now has two semantically distinct input channels:

- **ordinary free-form textbox** — feedback, disagreement, corrections, nuance, missing context, or explanation;
- **Write exact wording to record** — only when the participant wants literal replacement wording stored unchanged rather than interpreted conversationally.

The existing accept/reject/investigate/unresolved controls retain their separate workflow meanings.

## Implementation

- `src/hdmatch/api/life_patterns_v2_owner_continuous_flow.py`
- `src/hdmatch/api/life_patterns_v2_owner_continuous_flow_ui.py`
- `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- `tests/unit/test_life_patterns_v2_owner_continuous_flow.py`

Application head: `1b4f32ba16693df2a645fecb64dc00b10989cd62`.

## Verification

GitHub Actions run `35234856279`: **SUCCESS**.

- full unit/integration suite: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `2503e395-714d-487d-9d83-cf6e4b97aad6`: **SUCCESS** from application head `1b4f32ba16693df2a645fecb64dc00b10989cd62`.

Runtime evidence:

- application startup complete;
- `GET /healthz` returned HTTP **200 OK**.

## Mission Control

The corresponding privacy-bounded owner logic correction is durably captured on the existing universal-architecture correction branch:

`feedback/mission-control/SDF-20260917-LIFE-PATTERNS-CONTINUATION-QUESTION-ADMISSION-019.json`

Truth remains `CAPTURED_BRANCH_ONLY`.

## Next consumer-seam check

On refresh/recovery:

1. normal flow should proceed directly to the next useful question without a `Continue interview` checkpoint;
2. `Finish for now` should remain visibly available;
3. the next question should not semantically repeat earlier answers;
4. low-value candidate questions should be replaced or suppressed before display;
5. synthesis feedback should use the textbox, with only the separate literal exact-wording override remaining;
6. exact audit/recovery, progress, target-theory blindness, direct-report/inference handling, and fast adjudication must remain intact.

The subsequent scientific gate remains a fresh target-blind completed measurement freeze followed by the narrowly authorized owner-self DOB/time recovery regression against the frozen historical benchmark.
