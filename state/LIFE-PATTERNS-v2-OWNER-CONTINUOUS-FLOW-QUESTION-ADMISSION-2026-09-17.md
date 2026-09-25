# Life Patterns v2 — continuous-flow question-admission repair — 2026-09-17

## Owner findings

Direct owner testing identified four coupled participant-facing failures:

1. the next measurement-area question could ask something already answered earlier in the interview;
2. a routine `Continue interview` checkpoint required a click even though continuation was the only normal nonterminal action;
3. some questions remained low-value despite existing information-gain language in the interviewer prompt;
4. synthesis review exposed multiple text-entry controls even though the always-available textbox could already carry explanation, correction, nuance, or replacement wording.

The owner supplied an exact browser audit/recovery checkpoint. It was inspected privately and is not committed. It showed the current server snapshot carrying only the newest measurement-area conversation while earlier interview information lived mainly in client-side completed-result and aggregate-coverage summaries. That architecture could lose exact conversational memory across area boundaries even though compressed coverage metadata survived.

## Generating conditions

### Cross-area duplicate questions

The prior continuation route called `/coverage/next-session`, created a brand-new server session, and selected the next question from aggregate coverage plus accepted pattern summaries. Those summaries are useful planning metadata but are not a substitute for the participant's earlier answers. A construct could therefore be semantically answered yet remain available to be asked again.

### Redundant Continue checkpoint

Local topic completion and successful pattern adjudication exposed an internal workflow boundary as a participant action. In ordinary flow there was exactly one normal next operation: choose the next useful still-open distinction. Requiring a click added burden without adding participant authority.

### Weak question-quality enforcement

The interviewer already had prompt instructions to ask only decision-changing, nonredundant questions. That was a generation preference, not an independent admission boundary. A generated question could therefore reach the participant without a second check that identified the missing discriminator and demonstrated that materially different answers would alter the retained person model.

### Duplicate synthesis-feedback controls

The free-form textbox already accepted ordinary explanation, correction, nuance, disagreement, and participant-authored wording. The first repair correctly hid `Close — I’ll explain what needs changing`, but initially retained a separate exact-wording button because literal storage was a different backend intent. The owner correctly identified that this still leaked an internal intent taxonomy into the UI: a single flexible text field can express both ordinary correction and a literal replacement request.

## Repair

### One continuous recoverable session

Normal cross-area continuation advances the same server session. The hidden ledger and conversation therefore continue accumulating instead of resetting at every measurement-area boundary.

Browser audit/recovery state also carries a bounded participant-answer memory. The continuation planner receives:

- still-open measurement dimensions;
- aggregate coverage metadata;
- accepted participant-authoritative pattern wording;
- the bounded participant-answer memory;
- the current continuous server conversation;
- operative hidden-ledger facts.

This memory is for redundancy suppression and planning; evidence admission remains governed by the existing hidden-ledger/source-provenance rules.

For older exact browser snapshots that predate explicit `answer_memory`, recovery now seeds the redundancy memory from accepted participant-authoritative result wording plus any raw participant turns that remain in the server snapshot. This cannot recreate raw answers that the older architecture never saved anywhere, but it preserves all recoverable prior content for repeat suppression.

### Automatic continuation

After:

- a locally completed measurement area;
- an automatically recorded direct participant-authored person-specific pattern; or
- a successful participant judgment of a genuine interviewer inference,

the app automatically chooses the next admitted question. The ordinary `Continue interview` button is hidden. It appears only as an explicit retry frontier if next-question selection fails.

`Finish for now` is a persistent fixed on-screen control throughout the interview. Pausing saves the current browser audit/recovery checkpoint.

### Explicit pre-send question admission

Questions pass a separate model call before display.

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

The admission rationale is saved in the browser audit/recovery bundle as planning/audit metadata so a future uploaded snapshot can show why a questionable question passed the gate. It is not participant evidence.

### Synthesis review simplification

There is now **one participant text-entry channel** during inferred-synthesis review: the ordinary always-visible textbox.

It handles:

- disagreement;
- explanation of what is wrong or missing;
- nuance or context;
- corrected/replacement wording.

Both `Close — I’ll explain what needs changing` and `Edit exact wording myself` are hidden. If the participant specifically wants literal wording rather than conversational interpretation, the UI asks them to state that intent in the same textbox (for example `Exact wording: …`) rather than exposing another editor mode.

The remaining buttons are kept only when they perform genuinely different workflow transitions: accept the inference, keep investigating with another useful question, reject/stop, or leave unresolved.

## Implementation

- `src/hdmatch/api/life_patterns_v2_owner_continuous_flow.py`
- `src/hdmatch/api/life_patterns_v2_owner_continuous_flow_ui.py`
- `src/hdmatch/api/life_patterns_v2_owner_deployed_app.py`
- `tests/unit/test_life_patterns_v2_owner_continuous_flow.py`

Exact deployed application head: `56796a842ef3bc453f12f65c138458656e441490`.

Regression checkpoint: `f861ac5d26f6e11aceb3c69804e416e15db612c9`.

## Verification

GitHub Actions run `35239835457`: **SUCCESS**.

- unit/integration tests: PASS;
- Ruff: PASS;
- strict mypy: PASS.

Railway deployment `3588d15c-4865-4c0d-ba37-331d5ac84483`: **SUCCESS** from application head `56796a842ef3bc453f12f65c138458656e441490`.

Runtime evidence:

- application startup complete;
- `GET /healthz` returned HTTP **200 OK**.

## Mission Control

The original continuous-flow/question-admission correction remains durably captured as logic record 019. The follow-up correction—backend intent distinctions do not require separate participant text-entry controls—is captured separately as:

`feedback/mission-control/SDF-20260917-LIFE-PATTERNS-SINGLE-SYNTHESIS-TEXT-CHANNEL-020.json`

Both remain `CAPTURED_BRANCH_ONLY` on the existing Mission Control draft branch.

## Next consumer-seam check

On refresh/recovery:

1. normal flow should proceed directly to the next useful question without a `Continue interview` checkpoint;
2. `Finish for now` should remain visibly available;
3. the next question should not semantically repeat earlier answers;
4. low-value candidate questions should be replaced or suppressed before display;
5. inferred-synthesis feedback should expose one textbox rather than multiple edit modes;
6. exact audit/recovery, progress, target-theory blindness, direct-report/inference handling, and fast adjudication must remain intact.

The subsequent scientific gate remains a fresh target-blind completed measurement freeze followed by the narrowly authorized owner-self DOB/time recovery regression against the frozen historical benchmark.
