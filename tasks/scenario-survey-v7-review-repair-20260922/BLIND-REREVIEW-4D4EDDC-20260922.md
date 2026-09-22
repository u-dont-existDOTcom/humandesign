2026-09-22 21:19:05 GMT (UTC+00:00)

BLOCKERS

1. `F0.question/planning_targets` in [interviewer-bank-v7.json](/tmp/humandesign-v7-blind-rereview/tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json:195), protocol “Before every next question” steps 4 and 7, and evidence-guide `D05.audience_adaptation` ([line 103](/tmp/humandesign-v7-blind-rereview/tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json:103)). F0 presents only one audience, while the credited example requires an unprompted comparison with family. A normal answer can reveal wording or persuasion strategy, but not audience adaptation. Because this is the sole route for the facet, a fresh pilot will either leave it systematically unanswered or overcredit ordinary phrasing. Minimum repair: hold the proposal constant and request one matched comparison between two specified audiences as a single response task.

2. `M11.question/interpretation_limit` ([line 227](/tmp/humandesign-v7-blind-rereview/tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json:227)), protocol discrimination rule step 7, source-requirements `sufficiency` ([line 401](/tmp/humandesign-v7-blind-rereview/tasks/scenario-graph-convergence-20260919/source/source-requirements-v2.json:401)), and evidence-guide `X08.offer_and_leverage` ([line 723](/tmp/humandesign-v7-blind-rereview/tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json:723)). The prompt supplies the hours contributed, proposed exchange, and fairness rationale; the credited fictional answer merely repeats them. That allows stimulus content to masquerade as respondent-originated leverage and makes the ordinary answer nearly tautological. Minimum repair: either have the respondent formulate an exchange from concrete costs and needs without supplying the proposed rationale, or specify a concrete objection and credit only the respondent’s answer-originated response to it.

3. `G15`, `R07`, and `R08` in the bank—especially `R07/R08.kind = matched_variant` and their `G15` context binding—plus protocol “Scene sufficiency” workload rule and evidence-guide `D14.ordinary_engagement`, `D14.burst`, and `D14.prolonged_overload`. G15 leaves the work type unspecified, while R07/R08 introduce mentally demanding computer work alongside the duration/intensity change. They are therefore not matched workload variants; observed differences can reflect task modality rather than intensity or duration. Minimum repair: use the same specified or respondent-selected work type across all three routes and vary only the intended workload dimensions.

4. `G17.question/interpretation_limit` ([line 1041](/tmp/humandesign-v7-blind-rereview/tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json:1041)), protocol premise-sufficiency and discrimination steps 6–7, and evidence-guide `D16.challenge_threshold` ([line 409](/tmp/humandesign-v7-blind-rereview/tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json:409)). Whether the wrong time affects anyone is omitted, even though the node acknowledges that its consequences may require clarification and the credited example introduces that missing condition. The literal action answer is therefore underdetermined and correction may be nearly forced, while the protocol would have to repair or suppress the route before exposure. Minimum repair: supply confidence and a concrete consequence, preferably with a matched lower-consequence variant, or make the threshold-determining question the initial task.

NONBLOCKING

1. Make `M07` explicitly contrast what came easily with what required learning; “How did you come to be good at it?” more reliably elicits acquisition history than both halves of `X05.ease_and_learning`.

2. Split or condition the planning metadata for `PREFER-INFLUENCE`: an answer after F0/G05 supports `D05.preferred_use`, while an answer after M11 supports `X08.preferred_use`; one exact-context answer does not automatically support both.

3. Make the already narrow evidence semantics explicit in planning metadata for `G10`, `PHYSICAL-CLOSENESS`, and `ROUTINE-CHANGE`. Their guide readings support schedule autonomy, physical-affection preference, and voluntary novelty choice respectively—not complete stable direction, sensuality, or response to disruption.

4. Specify or deliberately solicit the missing condition in `G25`—particularly the reason for the two failures to appear—because trust change can depend materially on that explanation.

5. Add explicit `context_requirement` fields to `CARE-RESPONSIBILITY`, `CARE-LIMIT`, and `ROMANCE-FADE`. Their admissions currently provide adequate semantic protection, but they are the only three canonical routes lacking the otherwise universal field.

STRONGEST_REMAINING_WEAKNESS

The planning targets are sometimes broader than what the literal prompt can elicit without premise echo, unsolicited comparison, or additional clarification.

AREAS_NOT_EVALUATED_OR_UNDERSTOOD

- Whether AstroHD or its constructs are true or valid.
- Chart recovery, target-model mappings, fit scores, or predictions.
- Private participant material, birth data, or chart data.
- Prior findings, producer rationale, repair history, audits, or reconciliation.
- Runtime implementation, deployment, recruitment, or scoring behavior.
- Candidate-commit verification from `REVIEW-IDENTITY.txt` and all other excluded repository files.

VERDICT

NOT_READY_FOR_FRESH_PILOT

semantic_change_required

true