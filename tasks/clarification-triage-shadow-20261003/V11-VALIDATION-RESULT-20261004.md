# V11 untouched validation result — 2026-10-04

## Frozen design

The v11 packet and blind adjudication targets were committed and pushed before any v11 implementation replay. Nine cases were scored by Sonnet/high + Opus 5.5/max consensus; S5 was frozen unscored because the adjudicators disagreed about PREFER-EXCHANGE.

## Untouched result

First implementation replay: **8/9 scored cases passed**.

The only failure was S8:
- expected: G23 + M09;
- actual: M09 only;
- the source contained two nearby, materially conflicting shared-meal attention answers;
- the conservative source-question matcher did not recognize the first G23 paraphrase because dinner/notice did not lexically overlap enough with meal/attention.

V11 is therefore tuning evidence, not promotion evidence.

## Bounded repair

The repair does not broaden route coverage or add full evidence coding:
1. normalize ordinary meal wording (dinner, lunch, supper) to meal and notice-word forms to attention only inside the conservative question matcher;
2. attach a bounded ±2 behavioral-turn context window to each matched source-question/route pair;
3. let GapMatchAudit classify a contradictory_gap when non-superseded route-specific responses in that local window materially conflict;
4. treat that status like a source-exposed recoverable gap while preserving the existing independent-for-batch and admission safeguards.

Focused verification after the repair: **24/24 tests passed** and Ruff passed.

A contaminated S8 replay then returned and admitted exactly G23 + M09 in about 49 seconds. That confirms the repair mechanism but does not count as fresh quality evidence.

## Remaining gate

Promotion still requires a new untouched exact-authority packet after this repair, followed by repeated-run stability. Latency on the owner-scale 81-turn record must also be re-measured because the source-match audit adds semantic work.
