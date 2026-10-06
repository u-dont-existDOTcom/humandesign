# Life Patterns collection correction — 2026-10-06

Version: **2026-10-06.1-intro-progress-recovery**.

## Owner outcome

Remove the unnecessary modality and earlier-life setup questions; retain actual research consent. Show meaningful remaining answering effort. Recover the current canonical interview rather than asking the participant to choose between copies of an older partial source. Preserve the accepted fast-review workflow, exact source, optional skipping, and scientific boundaries.

## Defects and correction

The prior release fixed service-stage waiting estimates but left the main interview with a reply-count/topic footer. That did not answer how much interviewing remained. Its root Instructions still explicitly requested three setup answers. Its recovery guide required choosing between multiple candidates before reading/comparing their contents and did not require cross-schema/alias pagination or source-lineage comparison before treating a shortlist as current. The owner test exposed those gaps.

The updated root now asks only for research consent when needed and says exactly, “You are welcome to type or talk.” Participants may switch freely. Useful earlier-life questions are included by study default, but explicit opt-outs and skips are respected. Study defaults are labelled as defaults, not invented participant consent. Modality is recorded only from reliable metadata or a participant statement; otherwise it remains unknown. No mode confirmation is needed at freeze.

Progress must include remaining questions and estimated answering minutes until independent review, based on the actual current revisable plan. A percentage, when defensible, describes that plan only. A count/topic footer alone is forbidden. Estimates use reliable pace evidence or an explicit planning assumption, not a promised deadline. The guide requires updating the plan as answers resolve tasks and explaining material increases rather than indefinitely repeating “a few more questions.” Service waiting is separate.

A verified completed/saturated historical interview has zero new local main-interview questions planned. It proceeds to independent review after any genuinely missing consent and exact source backups. The reviewer may still request admissible clarifications; historical completion is not final evidence-review readiness or scientific freeze.

Recovery now searches canonical aliases and each allowed schema, follows relevant pagination, parses actual sources, compares exact Q&A and provenance, and distinguishes upload time from evidence time. Verified successors and equivalent duplicates are selected without an unnecessary user choice. A largest count, newest schema, or upload date alone is insufficient. Empty or partial new files do not displace fuller source. Conflicting or unrelated plausible lineages still require a minimal choice. Known missing newer source pauses interviewing; incomplete search cannot claim exhaustive latest recovery.

In the reported private incident, direct local comparison confirmed 81 Q&A in the candidate and recovered extension, exact Q&A equality between those two representations, and the preserved 79 answers as their exact prefix. The older source has 19 actual user messages. The 19 count described the wrong old source; it was not evidence that the later answers disappeared. The record's unrecovered-later-turn caveat remains intact. No private answer strings, source hashes or participant files are included here or in the update archive.

## Verification

Five new document-boundary tests first failed against the old shipped contract. After the edits, the repository suite passed **1,018 tests**, with **six astronomy-data-dependent skips**. The full participant suite passed **170 tests** after reconciling stale text assertions without removing source-fidelity safeguards. Repository and affected application lint passed; mypy reported no issues in 220 source files.

Five bounded, isolated application-model next-reply probes exercised the actual updated Instructions and two operational guides with explicitly synthetic state:

1. New opening: one consent question, with type/talk welcome, no mode or earlier-life question.
2. Partial Library results: continue canonical search/pagination, do not prematurely select or ask a behavioral question.
3. Verified successor: select the current candidate-format extension automatically, preserve the missing-turn caveat, and plan zero new local interview questions.
4. Remaining effort: with 12 completed tasks, four required remaining questions and up to three conditional extras, return 4–7 questions / 4–14 answering minutes under a stated 1–2-minute assumption, approximately 65–75% of the current plan.
5. Conflicting sources: ask for the authoritative source rather than silently selecting the newer upload.

All five targeted checks passed in one configured gpt-5.6-sol/xhigh application-model run per case. These are controlled next-reply simulations, not a live private Custom GPT test or an actual Library-search benchmark. The opening's numeric initial plan was model-provisional, not calibrated duration evidence. The private source comparison separately used actual retrieved files. No research submission, participant freeze, or new paid API inference was performed.

## Delivery and unchanged surfaces

The update archive is `Life-Patterns-GPT-intro-progress-recovery-update-2026-10-06.zip`. It contains the new Instructions and BOTH operational Knowledge guides. Replace Instructions, RECOVERY-GUIDE-v2.md and ACTION-HANDOFF-GUIDE-v1.md in the existing GPT. Keep the other four Knowledge files, existing Action and Bearer credential unchanged. Select Update to apply the editor draft.

Instructions occupy **7,920 characters on the strict line-break count**. The full bundle and update manifest pin exact file hashes. The frozen protocol, question bank, evidence guide and CF-003 module are unchanged. Runtime service, worker and Action schema bytes are unchanged; this is a collection-package correction, not a backend redeployment.

The private Custom GPT editor has not been modified by these repository operations. Package delivery, merged source, test evidence and installed GPT behavior are separate facts. The owner must apply all three replacements for the new collection contract to reach that GPT. An unchanged old recovery guide would preserve the very conflict this update removes.
