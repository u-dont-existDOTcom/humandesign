# Lilly horary retrospective — result — 2026-09-24

Status: **EXPLORATORY RETROSPECTIVE PILOT COMPLETE / NO PREDICTIVE ADVANTAGE SHOWN / NOT VALIDATION**.

## v0 frozen perfection-only arm

Prediction freeze SHA-256: `b3953fbf6cfd96ea0a5ea3c8fafce770694bf3757798a4168e2412cc35ec5f7b`.
Outcome-coding SHA-256: `a76829fd3e9dd3f161fda6ebfaed824c86d4dac04889f8d2db72c0909c616f89`.
Evaluation SHA-256: `c98adc7bc7ae937b96e0b42895ee706190f1806705813992286dd7f8a66ac8ed`.

Frozen predictions: 9 cases -> 0 YES, 7 NO, 2 DEFER.
Three archived threads did not actually contain a final binary employer decision and remain UNKNOWN rather than being coerced to NO.

Among 6 cases with definite outcomes, v0 answered 4 and got 3 correct: 75% selective accuracy, 66.7% coverage, and 50% correct-yield per evaluable case. Exact binomial p versus 0.5 = 0.625; exact 95% CI = 19.4%-99.4%. On the four cases v0 answered, the trivial majority-class baseline was also 75%, so v0 added no predictive advantage.

Strict outcome-unexposed subset: 5 inputs, 3 definite outcomes, only 1 non-DEFER prediction. It was correct, but coverage was only 33.3%; p=1.0. This is not useful evidence.

## Chapter LXXXII source repair v1

Freeze SHA-256: `256a65eb8893e0862138514656d0dc72e3efe9ccd8d244725bad061bb10ee294`.
Development prediction SHA-256: `7ae9d011d856427988ee3376d8b1f19b87e291c631c92143043bf09467cef161`.

v1 added only explicit source-native affirmative clauses from Lilly Chapter LXXXII: principal perfection, L10 reception of L1/Moon, L10-in-1st faster-than-L1, and L10-in-1st joined to a benefic. No fitted weights were introduced.

Development predictions became 7 YES / 2 NO / 0 DEFER. On the six definite development outcomes, v1 got 4/6 correct = 66.7%. It recovered the known positive cases that v0 missed, but created enough false positives to fall below the predeclared 75% v0 accuracy gate. Therefore v1 **DEV_FAIL / NOT ADMITTED TO A FRESH HOLDOUT**. No reception type or clause was removed after seeing the failures.

## Interpretation

This pilot does not show evidence that the tested Lilly operationalizations predict job outcomes above trivial baselines. The negative result is bounded: v0 is too restrictive relative to Lilly, while literal Chapter-LXXXII affirmative composition is too permissive on this small development set. A stronger test of Lilly-as-practiced would require a source-frozen full judgement protocol or blinded expert readers, then a substantially larger untouched corpus.

## Durable corpus

The source/catalog schema is tracked under `research/horary_known_outcomes/`. The outcome key and queryable SQLite truth database remain outside the decoder root to preserve future blinding. A portable truth package is separately persisted in the owner Library. Raw forum snapshots remain private evidence and are represented portably by source URLs and SHA-256 hashes rather than redistributed wholesale.
