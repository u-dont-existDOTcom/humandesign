# V14 untouched validation result — 2026-10-04

## Frozen design

The v14 source packet and blind targets were committed and pushed before implementation replay. Nine cases were scored. V7 was frozen unscored because the two admitted blind adjudicators disagreed. V2 was a mixed target requiring G20 and permitting G19.

## Untouched result

First implementation replay: **6/9 scored cases passed**.

Failures:
- V3: expected M09; triage proposed M09; admission rejected it for multiple-response-task + unsupported-extension.
- V4: expected G19; triage proposed G19; admission rejected it for already-answered + low-information-gain + unsupported-extension.
- V5: expected PREFER-EXCHANGE; triage proposed PREFER-EXCHANGE; admission rejected it for already-answered + low-information-gain.

Passing scored cases: V1, V2, V6, V8, V9, V10.
V7 remained unscored and returned review-ready.

## Diagnosis

This is not primarily a route-discovery failure. In all three failed scored cases, GapTriage selected the frozen-correct route. The loss happened because GapAdmission currently couples two different judgments:
1. whether a materially unresolved route-level gap exists; and
2. whether the exact generated question wording is admissible.

V3 demonstrates pure question-form failure erasing a valid route. V4/V5 demonstrate answeredness/information-gain disagreements at the route level, with V4 also carrying a wording-extension failure.

The architecture must therefore separate the gap/spec object from its rendered question. V14 is tuning evidence, not promotion evidence.

## Cross-family architecture review

A fresh Claude Opus 5.5/max review of the generalized failure class recommended:
- make a route-level gap spec the full-source admission object;
- require citation-bound, contradiction-aware answeredness at exact distinction + scope;
- evaluate rendered wording separately from the spec;
- repair/recheck wording only after the gap itself is admitted;
- use local match/audit evidence as citations and narrow adjudication input rather than as an automatic override;
- avoid serial full-source recovery as the default path because it would increase latency and rescue bias.

No production behavior is changed by this result.
