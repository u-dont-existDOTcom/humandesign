# Fresh-context review prompt — scenario survey v7

Repository: `u-dont-existDOTcom/humandesign`
Branch: `chat/scenario-survey-v7-redesign-20260922`

Treat this as a fresh semantic/design review. Do not read or request the private participant transcript, birth data, chart outputs, target-model mappings, fit scores, or prior predictions.

Read, in order:
1. live default-branch `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md`;
2. `tasks/ACTIVE-TASK.json`;
3. `state/CURRENT-STATE.md` and `state/SCENARIO-SURVEY-V7-REDESIGN-20260922.md`;
4. `tasks/scenario-survey-v7-redesign-20260922/REDESIGN-RATIONALE.md`;
5. `tasks/scenario-survey-v7-redesign-20260922/interviewer-bank-v7.json`;
6. `tasks/scenario-survey-v7-redesign-20260922/INTERVIEW-PROTOCOL-v6.md`;
7. `tasks/scenario-survey-v7-redesign-20260922/EVIDENCE-GUIDE-v7.json`;
8. `tasks/scenario-survey-v7-redesign-20260922/REDESIGN-AUDIT.md` and `VERIFICATION.json`;
9. the non-private live-repair notes in `tasks/scenario-live-pilot-repair-20260920/` only if needed to verify that a repair actually addresses its stated failure.

Review goal: determine whether v7 is semantically ready for a fresh respondent pilot, not whether AstroHD is true.

Audit every canonical route for: premise sufficiency, one response task, construct discrimination, hidden assumptions, redundancy/mirror risk, antecedent admission, context binding, scoped interpretation, and natural-stop behavior. Pay special attention to whether the new global guards actually prevent repeats of the live-pilot failure classes.

Also check that `EX-SENSORY-CONFLICT-01` remains exploratory/unmapped and cannot receive canonical evidence credit.

Return:
- `BLOCKERS`: numbered, each with exact node/protocol location, failure mechanism, and minimum repair;
- `NONBLOCKING`: useful improvements that are not required before another pilot;
- `REGRESSIONS`: any v6 behavior made worse;
- `VERDICT`: exactly one of `READY_FOR_FRESH_PILOT` or `NOT_READY_FOR_FRESH_PILOT`;
- `semantic_change_required`: true/false.

Do not rank AstroHD models, infer the pilot participant, or use target-theory expectations to judge the survey.
