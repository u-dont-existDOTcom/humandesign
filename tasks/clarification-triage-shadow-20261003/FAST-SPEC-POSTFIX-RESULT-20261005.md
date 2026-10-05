# Fast spec-only clarification path — post-fix result — 2026-10-05

## Owner outcome

Return high-quality clarification questions after a long Life Patterns interview without coupling the decision to full evidence synthesis, without lowering model effort, and without imposing an arbitrary clarification-count cap. Target for the clarification-critical path: roughly 1–3 minutes on the recovered 81-turn owner-scale record.

## Current fast path

The first-batch path now separates:
1. `GapSpecTriage`: source-first discovery of up to three route-level gap specs only.
2. `GapSpecAdmission`: independent route-level admission only.
3. Participant-facing render/review only for admitted routes that cannot safely use frozen canonical wording.
4. Broad omission/match audit deferred only when at least one gap has independently passed admission. A would-be no-question result still runs the omission audit before stopping.

No model-effort reduction or clarification-count stopping rule was introduced.

## Robustness repairs in this checkpoint

- Dependent admission now receives the frozen authority for required context-source routes. This lets an equivalent M11 source turn be evaluated against actual M11 authority when admitting PREFER-EXCHANGE.
- An admitted gap no longer disappears after one wording-only failure. The fast path permits one bounded rerender + wording-only re-review for routes rejected at the first render review.
- The retry does not reconsider whether the gap exists and does not loop indefinitely.

## Focused verification

- Ruff: passed.
- Focused shadow-triage tests: **38/38 passed**.
- Motivating failure replay after repair: **Y2 and Y8 both passed**.
- Full selected v16 tuning subset after repair: **6/6 passed**:
  - Y1 review-ready
  - Y2 M09 + G19
  - Y4 review-ready
  - Y7 PREFER-EXCHANGE
  - Y8 PREFER-EXCHANGE
  - Y10 G23 + allowed M05
- These are development/tuning cases only; they are not fresh promotion evidence.

## Owner-scale latency

Recovered owner record:
- 81 behavioral turns
- 76 eligible route cards
- GPT-5.6 Sol, xhigh

Final repaired fast-spec benchmark:
- total semantic time: **112.159s (1m52.2s)**
- GapSpecTriage: 65.137s; 25,992 prompt tokens; 3,067 output tokens
- GapSpecAdmission: 21.009s; 17,066 prompt tokens; 658 output tokens
- GapQuestionRender: 12.006s; 9,332 prompt tokens; 291 output tokens
- GapQuestionReview: 14.007s; 9,353 prompt tokens; 219 output tokens
- broad omission audit: deferred from the first-question critical path because independently admitted gaps existed

Participant-facing result contained three admitted routes, two rendered/reviewed questions, and zero question rejections.

Comparison:
- original full shadow path: 554.368s (9m14.4s)
- deferred-audit full-output path: 281.539s (4m41.5s)
- final fast-spec path: **112.159s (1m52.2s)**

The fast-spec path therefore meets the 1–3 minute owner target on this owner-scale run while preserving xhigh effort.

## Remaining evidence boundary

Fresh post-repair blind cross-family validation is still unavailable because Claude Code hit its weekly quota before a new packet could be generated. The recorded reset is October 6 at 14:00 Africa/Nouakchott. Per the owner cross-family rule, no same-family substitute is being called a fresh cross-family check.

This branch remains development/shadow evidence only until that fresh validation runs. No live participant behavior has been changed by this experiment.
