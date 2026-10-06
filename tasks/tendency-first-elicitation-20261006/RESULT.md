# Tendency-first question selection — 2026-10-06

## Diagnosis
The October 1 question-alignment audit explicitly classified the meal-cost M11 scenario as a replacement candidate and drafted a direct general-pattern question. Later fast-review and intro/progress/recovery releases left that draft unactivated. The reviewer was therefore faithfully enforcing the old stimulus rather than implementing the requested tendency-first interview. Completing a scene was being accepted as information gain without requiring a material unresolved person-level pattern. Prior engineering/transport passes did not prove that requested elicitation behavior.

## Repair
A separately versioned tendency-first policy now supplies 25 direct usual-pattern questions under TF1 identifiers and retires 30 replaced/demoted originals from new elicitation. Original v7 wording, evidence guide, historical source and instrument hash remain unchanged; the policy has a separate identity. Examples are optional aids, not mandatory role-play or independent corroboration. An adequate general answer is enough. Conditional patterns remain valid; no fixed trait, forced frequency or repeated example is required.

Fast selection, independent admission, omitted-gap checking, question rendering/review, full-evidence fallback, and the HTTP worker-result validator share the policy. A full-review compacting branch initially omitted the new selected-route authority; its new consumer test detected that and the branch was repaired. Old selected questions cannot reappear through that fallback.

An old M11 skip suppresses TF1-M11 and its preference/dependent variants. Existing pending answers/skips are ingested exactly; no historical answer is rewritten, no skipped question is silently answered, and a new version is not a reason for a full re-interview. Previously issued questions retain their original wording in history.

The new route identifiers do not automatically grant legacy facet scores. The independent evidence reviewer must check exact answer content against a facet's actual contract; source-supported observations remain usable even when they need an empty facet list. This changes elicitation, not the scientific validity of personality inference. No diagnosis or population-level validation is claimed.

## Verification
- 18 focused policy/HTTP/batch/reconciliation tests passed, including rejection of the old canonical meal prompt, skip propagation, unchanged historical bank, exact import, and full-review selected-route authority.
- Full affected participant suite: 178 passed.
- Full repository suite: 1,018 passed; six astronomy-data-dependent tests skipped.
- Root CI lint and mypy passed. The wider application lint scan reports the same three pre-existing style findings (two UP035 and one SIM105 in legacy engine/context code); changed/new logic has no added substantive lint finding.
- Three fixed, isolated, full-menu model probes passed: an adequate general answer needed no question; an unresolved general reference produced TF1-M11 directly, not meal role-play; the old meal skip produced no replacement or dependent question. These are synthetic pipeline checks, not an actual private-GPT interaction or proof of personality validity.
- Frozen protocol/bank/evidence guide, CF-003 and Action schema bytes match the previous integrated release.

## Delivery boundary
The GPT package is version 2026-10-06.2-tendency-first. Replace Instructions and add TENDENCY-FIRST-GUIDE-v1.json as the seventh Knowledge file. Existing six Knowledge files, Action and credential remain. Consent-only opening, useful progress and latest-source recovery are preserved. The private GPT editor is not changed by repository work.

Deployment and live test receipts are recorded separately when actually completed. No real participant record was read or modified by the regression probes. This repair does not request a new answer to the user's skipped question or restart their review.
