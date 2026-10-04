# Owner-scale 81-turn latency result — final-render repair — 2026-10-04

## Scope

Development-only shadow benchmark using the recovered 81-turn owner participant source, GPT-5.6 Sol at xhigh, and the final-render/persistence repair. Persisted diagnostics are privacy-safe: no participant text, source-turn IDs, prompts, or content-derived hashes.

The first one-shot desktop-command attempt did not produce a report because its parent execution surface disappeared mid-turn. A persistent interactive terminal rerun completed normally. One accidentally surviving duplicate benchmark was identified and terminated; the measured persistent run then continued alone.

## Owner-scale shape

- Behavioral turns: 81.
- Eligible route cards: 76.
- Triage context: 95,951 serialized characters.
- Deterministic source-question matches: 54.
- Match-audit pairs: 54.
- Match-audit unique source turns: 80 of 81.
- Match-audit context: 95,728 serialized characters.

Therefore the supposedly local match audit is effectively a second full-interview pass on this owner-scale record.

## Completed semantic benchmark

Total semantic duration: **554.368 seconds (9m14.4s)**.

Per stage:
- GapTriage: 152.156s; 31,686 prompt tokens; 8,141 completion/output tokens.
- GapAdmission: 115.022s; 17,657 prompt tokens; 5,980 completion/output tokens.
- GapMatchAudit: 248.174s; 29,333 prompt tokens; 13,043 completion/output tokens.
- GapQuestionRender: 22.008s; 8,991 prompt tokens; 568 completion/output tokens.
- GapQuestionReview: 17.008s; 9,000 prompt tokens; 146 completion/output tokens.

The current end-only pipeline therefore does **not** meet the intended 1–3 minute clarification-critical-path target.

## Participant-facing shadow result

The run recommended three independently admitted routes. One question needed wording repair; the render/review path repaired it successfully, leaving zero participant-facing question rejections. This is diagnostic/tuning evidence, not fresh blind promotion evidence.

## Decision-relevant diagnosis

The dominant avoidable cost is GapMatchAudit: 248s, roughly 45% of total semantic time. Its intended local omission check expands to 54 pairs and 80/81 source turns, duplicating almost the entire interview after triage and admission have already run.

Next optimization should remove this near-full-source omission audit from the clarification-critical path or sharply bound its admissible input without reducing model effort or imposing a clarification-count cap. Full/omission reconciliation can remain available off the immediate question-return path.

## Remaining quality gate

Fresh post-repair blind validation is currently blocked by the Claude Code weekly quota. The fresh v17 generator returned the platform message that the weekly limit was reached and resets October 6 at 14:00 Africa/Nouakchott. No same-family substitute is accepted as the required cross-family check.
