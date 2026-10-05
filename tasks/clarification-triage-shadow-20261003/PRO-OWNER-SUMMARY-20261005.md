# Life Patterns — Pro review result

Date: October 5, 2026
Decision: Accepted after repairs for controlled integration. Not deployed.

## What was checked and changed

The current Pro review replaced the pending Claude check at the owner's request. It was not a cross-family or untouched blind review: the development history was supplied in the conversation.

Six new deterministic contract tests reproduced five defect classes in the previously published candidate:

1. Omission recovery could bypass independent admission and reverse an answered/low-information rejection. Recovered candidates now require a separate complete-source admission; an omission detector cannot override the independent veto.
2. A rejected question could remain selected even after both wording checks failed. The code now distinguishes an admitted gap from a usable, approved question.
3. Pending or unresolved review could be reported or scored as ready. Pending, unresolved, wording-failed, and ready states now remain distinct.
4. Five or more presentations of one route could exceed an audit binding limit. The audit now retains all source references within the existing 1,000-turn import bound.
5. A valid paraphrased antecedent could exclude a dependent follow-up before semantic review. The fast menu now permits semantic-context candidates while retaining actual-source and independent-equivalence checks.

## Verification

- Six new contract tests: all failed before repair and passed afterward.
- Focused shadow suite: 44 passed.
- Complete participant suite: 160 passed, including the 44 focused tests.
- Affected-file Ruff checks: passed.
- Six newly authored full-bank semantic cases: six passed, with all 78 eligible question routes visible and no unrelated-route masking. Targets were frozen before execution.

The semantic cases covered complete answers, an unidentified money purpose, an untagged/paraphrased antecedent, a distant later answer resolving an apparent gap, explicit corrections and skips, and two independent gaps including a contradiction. One application-model run was performed per case. This is development evidence, not human predictive validation or a population error-rate estimate.

## Repaired 81-turn benchmark

Model setting: gpt-5.6-sol, xhigh.

| Stage | Semantic seconds |
|---|---:|
| Gap-spec triage | 75.142 |
| Independent gap admission | 14.008 |
| Question rendering | 14.007 |
| Wording review | 11.007 |
| Total | 114.164 |

The repaired stage produced three usable questions with no wording rejections in approximately 1 minute 54 seconds. This preserves the preceding candidate's approximately two-minute first-batch result without reducing configured reasoning effort.

This measures the first clarification batch, not the entire final review. The broader omission audit remained explicitly pending; final evidence synthesis was not marked complete. No promise that every interview finishes within three minutes is supported by this single measurement.

## Current operational state

The pending Claude review has been replaced and completed. No additional Claude quota wait is required for this review.

The repaired code, review, synthetic evidence and integration contract were saved in u-dont-existDOTcom/humandesign and remotely verified on branch:

`pro/gap-triage-review-20261005`

Published review commit:

`6c96b7a602a5c41543e573fe3a27f216d5e1e45d`

Repaired executable code commit:

`a39228f89c12a3a03742efd5b067a7477dffadc2`

The live Engine, worker, HTTP API and Custom GPT files remain unchanged. No deployment, new GPT ZIP, participant submission or freeze was performed. The live API's one-question transport does not yet become a batch-answer API merely because the shadow code returns multiple questions.

Remaining work is integration and deployment: preserve approved-question delivery, complete-source admission for recovered omissions, source-bound deferred audits, information-based stopping and final evidence synthesis. The detailed integration contract is included in the full packet placed in the owner's Downloads folder:

`Life-Patterns-Pro-Review-2026-10-05.zip`

Do not update the Custom GPT from an old ZIP expecting this speedup; the backend must first use the repaired stage.
