# V12 untouched validation result — 2026-10-04

## Frozen design

The v12 packet and exact blind targets were committed and pushed before implementation replay. Sonnet/high and Opus 5.5/max agreed on all 10 route sets, so all 10 were scored.

## Untouched result

First implementation replay: **9/10 passed**.

The only failure was T4:
- expected: PREFER-EXCHANGE;
- actual: review ready;
- T4 contained a natural paraphrase of M11 with an actual answer but no literal canonical_question_id;
- PREFER-EXCHANGE requires a bound M11 antecedent;
- the validator already supports an actual answered antecedent with equivalent_context=true, but shadow route eligibility only recognized literal canonical context-source IDs.

## Bounded repair

The repair changes only dependent-route eligibility:
1. conservatively match source questions against routes that serve as context sources;
2. expose a dependent route when one of its required context-source routes has such a source-question match;
3. attach context_match_turn_ids/context_match_route_ids as binding hints;
4. require a selected dependent route to use the real matched turn as antecedent_turn_ids with equivalent_context=true;
5. keep independent admission responsible for validating context and usefulness.

This does not make missing coverage sufficient and does not bypass dependent-route admission.

Focused verification: **25/25 tests passed** and Ruff passed.

A contaminated T4 replay then proposed and admitted exactly PREFER-EXCHANGE in about 31 seconds. That is tuning evidence only.

## Remaining gate

Promotion requires a new untouched exact-authority packet after this repair, followed by an unchanged repeat for stability. Owner-scale 81-turn latency must then be re-measured because match/audit/recovery work adds semantic calls.
