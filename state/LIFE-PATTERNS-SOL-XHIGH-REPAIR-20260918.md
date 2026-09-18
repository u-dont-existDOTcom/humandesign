# Life Patterns — Sol xhigh repair delivery

Date: 18 September 2026, UTC.
Status: IMPLEMENTED, DEPLOYED, HOSTED CI PASSED, AND BOUNDED REAL-MODEL CHECKS COMPLETED.
The owner’s general question-quality outcome remains open until natural use establishes it. The previous failed owner evaluation is not erased by this delivery.

## Model actually in use

The existing survey now requests **GPT-5.6 Sol with xhigh reasoning for all model work**: interpreting participant intent, evidence extraction, question planning, question review, synthesis review, and coverage assessment. There is no Astra routing and no automatic weaker-model fallback. The live health endpoint reports this configuration; final test responses returned `gpt-5.6-sol` and their request metadata records `xhigh`.

The initial candidate retained Luna for extraction. A live test showed that source classification is semantic, not merely mechanical bookkeeping, so that split was removed before final delivery. Ordinary saving, revision checks, and interface state remain deterministic application code.

Semantic output ceilings allow up to 25,000 total output/reasoning tokens; this is a ceiling, not a claim that each call uses them. Incomplete provider output is rejected rather than silently admitted. Recovery diagnostics retain allowlisted requested/returned model, effort, timing and token usage, not raw reasoning or credentials.

## Interview behavior changed

### Repair the question before measuring the answer

The app first distinguishes an actual answer, a request to clarify or challenge the interviewer, a mixture of those, an explicit topic change, and an explicit pause. Pure process feedback can explain, withdraw or repair the disputed question on the same topic. It does not add behavioral facts, count as new coverage, trigger a synthesis, or imply consent to finish.

Mixed messages keep actual life information, using exact source spans with their qualifications and the original complete utterance preserved. A correction to a substantive claim about the participant is not discarded merely because it accompanies criticism of the app. Historical process-only material can be quarantined from current interviewing without deleting its archive or silently rewriting accepted records.

### Ask coherent, useful questions

The planner and final admission step now explicitly check supported premises, unchanged scope and an answerable distinction. A method and its goal are not automatically rival motivations. Willingness and opportunity are different variables; action and feeling can coexist. A qualifier belonging to one category must not be transferred to a contrasting category. Open, concrete questions are preferred over manufactured personality dichotomies.

The active topic, earlier source-bound answers, corrections and resolved patterns are available throughout. The candidate being checked is not accidentally treated as a previously asked question. Older summary-only knowledge is marked as planning context, not recovered source evidence. An area can be deferred when no worthwhile question remains without being falsely marked scientifically complete.

These are stronger reasoning conditions and state controls, not a mathematical guarantee that every generated question is valid.

### Stop recycled and mislabelled syntheses

Exact repeated wording is suppressed. Semantic review compares meaning with prior accepted, disputed or rejected patterns and asks what materially changes. Shared evidence may support a genuinely different relationship; overlap alone does not ban a new inference. A review explaining an added inference must point to wording actually present in the current candidate.

A direct self-report uses original source authority and does not require the participant to agree with themselves again. This still requires exact wording, same-turn cited evidence, supported scope and semantic endorsement. It no longer depends on the extractor having assigned one particular evidence label. Invalid proposed interpretations no longer produce a generic fallback interrogation. A pending inference cannot announce that the area is complete.

Older restored drafts are checked before presenting approval controls again. A duplicate or unsupported unjudged draft can be withdrawn without changing historical accepted patterns or inventing an adjudication. The existing one-textbox interface, automatic continuation, Your patterns, pause/resume and checkpoint protections remain in place.

## What the actual model test showed

A separate synthetic interview was created through the normal live app. No owner session or private interview was read or mutated. Recovery used only that test interview’s unaltered server-issued backup. The development test was deliberately small, not a model tournament.

In the first candidate, the synthetic participant described preparing notes for unfamiliar teams when expectations were unclear. Sol asked about unfamiliar teams where the expected level of detail was already clear: a coherent attempt to distinguish two conditions present in the account. When asked to explain, it stayed with that distinction, added no behavioral facts, and did not finish the topic. When process feedback accompanied a conditional self-report, the source span was separated correctly.

The test then exposed a real remaining defect: Sol correctly classified the new wording as direct, but an older backend rule vetoed auto-recording because the extractor had labelled the facts `positive_occurrence`. That caused redundant confirmation. This was not counted as a pass. The follow-up removed the label dependency while retaining source safeguards and moved extraction to Sol xhigh.

On the corrected deployment, the same unaltered synthetic checkpoint was recovered. The direct report was recorded from its original source without a new Yes event. The interview then selected a new question about how the participant entered the volunteer project. Repeating the already-recorded statement did not create another pattern or approval screen. Actual extraction returned Sol and used attributed self-report labels. The synthetic test interview was then paused.

Across the two candidates there were **19 observed model calls**: 13 on the initial candidate and 6 on the corrected candidate. All six final calls requested and returned Sol, with xhigh requested. Initial evidence includes the two historical Luna extraction calls and the discovered failure; neither is concealed by the final result.

## Verification and delivery identity

| Boundary | Result |
|---|---|
| Deployed application commit | `78543a9f876b1105c4d62757b8b5f5119cc7b5e5` |
| Exact source tree | `5f9b75195342bf6f8fc3533d3f98efbfddc96761` |
| Live build | `survey-sol-xhigh-2026-09-18.2` |
| Railway deployment | `bbd8db1a-a898-42ca-9694-646b781871e3` |
| Final hosted CI | PR run `35295117795` and push run `35295114783`: SUCCESS |
| Hosted jobs | Python tests, Ruff, strict mypy and actual browser workflow: PASS |
| Browser regressions | 15 scenarios; no page errors; 320, 375, 414, 768, 1024 and 1440-pixel widths checked |
| Local implementation checkpoint | 842 passed, 7 environment/history skips; one existing Starlette/httpx warning |
| Local corrective checkpoint | 57 affected tests passed, including the new extractor-label and same-source protections |
| Types and lint | Strict mypy: 208 source files; Ruff passed with the repository’s existing E501/I001 exclusions |
| Live page | HTTP 200, 30,713 bytes, SHA-256 `33dde8dc8c3b808d0715bc1a958d3aacfdaa4674587a67848a8fe43dfd3f5a82` |

The deployed HTML matched the verified implementation. Model selection was checked through the live profile and actual response metadata, not inferred from a default in source code. Changes were isolated on a unique writer and integrated after exact head checks. The existing development pull request remains draft/open/unmerged. No protected-main merge, new service, public recruitment, access-policy change or chart-aware interviewing occurred.

## Limitations and next use

This is evidence that the repaired pathways work in a small real-model development sample, not an accuracy estimate or a promise that Sol will never ask a poor question. The private owner failure was not replayed live. Some semantic protections are model judgments and remain fallible. Native mobile keyboard, complete accessibility conformance, production-scale concurrency and scientific validity were not newly certified.

Xhigh is slower than the earlier lightweight calls. In the corrected sample, reviewing the existing direct report took about six seconds, and selecting the next area took about a minute. These are observations from a small sample, not performance guarantees. The application preserves the operation and pause/recovery state during that work; no reasoning-effort downgrade was used to hide latency.

Next: refresh the existing Life Patterns tab and continue the saved checkpoint. The app will recheck an old pending draft before asking for judgment again. General question usefulness and faithful interpretation remain the next owner-evaluation boundary; no new plan approval is needed.

## Evidence and recovery pointers

- `artifacts/life-patterns/sol-xhigh-repair-20260918/browser-regressions.json`
- `artifacts/life-patterns/sol-xhigh-repair-20260918/live-model-checks.json`
- `artifacts/life-patterns/sol-xhigh-repair-20260918/deployment-receipt.json`
- `tasks/SURVEY-SOL-XHIGH-REPAIR-20260918.md`

The canonical test observer was used for the implementation loop, browser checks and subsequent actual-model checks. The first ordinary live smoke call (approximately 30.04 seconds) was outside that observer and is disclosed separately; no complete-telemetry claim is made. Temporary checksummed transfer workflows self-removed from the delivered application tree. Synthetic session identifiers and the private owner backup are not published in these evidence files.

**There was never a completion policy.** Preserve `state/OWNER-CORRECTION-2026-09-02.md`; bookkeeping does not create a new scientific-completeness gate.
