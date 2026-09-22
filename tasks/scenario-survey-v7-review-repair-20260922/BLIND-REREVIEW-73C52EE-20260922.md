2026-09-22 23:01:53 +00:00

BLOCKERS

1. `interviewer-bank-v7.json` node `M04` (lines 642–650); protocol “Scene sufficiency” (lines 40–42); `EVIDENCE-GUIDE-v7.json` facet `X03.will_vs_available_energy` (lines 643–650). The question stipulates that the respondent still intends to finish, while the guide credits continued intention as part of the supported distinction. That gives stimulus-supplied content evidence credit, contrary to source-requirements sufficiency. It prevents respondents who would reconsider their intention when depleted from expressing the target distinction and can misclassify conditional execution as sustained will. Minimum repair: remove the stipulated intention and ask one task about what tiredness changes in their intention, then credit only their answer-originated distinction; alternatively narrow the target and guide explicitly to execution under stipulated intention, without claiming evidence about their will.

2. `interviewer-bank-v7.json` node `R08` (lines 882–900); protocol “Before every next question” item 7 and “Scene sufficiency” workload/matched-variant rules (lines 19 and 46–48); `EVIDENCE-GUIDE-v7.json` facet `D14.prolonged_overload` (lines 368–375). Six working days per week necessarily leave weekly seventh days, but “without any longer recovery period” does not say whether those days provide rest or other load. Respondents must invent a material recovery condition. The extreme four-week workload also makes lower energy nearly forced, as reflected by the guide’s exemplar, reducing discrimination. Fresh-pilot answers could therefore reflect different imagined off-days or the normative fatigue response rather than comparable individual variation. Minimum repair: specify the nonwork-day activity and recovery assumptions unambiguously, then recalibrate or replace the workload so materially different energy courses remain plausible.

NONBLOCKING

1. `M05`/`M06` and evidence-guide facets `X04.cue_form`/`X04.context_and_limits`: describe `M05` support as the respondent treating the presented deviation as meaningful, rather than “reporting” a cue supplied by the stimulus.

2. `OWNERSHIP` and evidence-guide facet `D19.status_ownership`: binding the question to a concrete tool—or a tool explicitly named first by the respondent—would reduce variation caused by silently imagining different privacy, legal, cost, or control properties.

3. `R06` and evidence-guide facet `D13.conflict_effect`: specifying whether the accusation feels unfair, partly fair, or uncertain would reduce predictable “it depends” answers. The current conditional-answer rules make this nonblocking.

4. Exploratory node `EX-SENSORY-CONFLICT-01` is structurally isolated: it resides outside canonical questions, has no planning target, disables automatic evidence credit, declares itself unmapped, and appears nowhere in the evidence guide. An optional protocol-level sentence could duplicate that separate-block restriction for defense in depth.

STRONGEST_REMAINING_WEAKNESS

Even after repair, most evidence remains narrow, scene-sensitive hypothetical self-report rather than observed behavior or demonstrated capacity.

AREAS_NOT_EVALUATED_OR_UNDERSTOOD

- Whether AstroHD is true or recoverable.
- Empirical reliability, validity, calibration, or actual fresh-respondent performance.
- Runtime/application implementation, deployment, recruitment, or interviewer compliance.
- Private participant material or prior pilot results.
- Producer rationale, repair history, prior audits, reviews, or verdicts.
- Birth/chart data, target-model mappings, fit scores, or predictions.
- Candidate commit identity recorded in `REVIEW-IDENTITY.txt`, which was outside the permitted read set.

VERDICT

NOT_READY_FOR_FRESH_PILOT

semantic_change_required

true