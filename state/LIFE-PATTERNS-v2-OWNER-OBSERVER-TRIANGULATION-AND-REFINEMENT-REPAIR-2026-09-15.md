# Life Patterns v2 owner observer-triangulation and refinement repair — 2026-09-15

Status: **IMPLEMENTED / VERIFIED / DEPLOYED — OWNER RETEST REQUIRED**.

## Direct owner findings

Direct owner testing exposed two related product defects after the specificity-aware adaptive repair:

1. `Keep trying to pin it down` could repeat or lightly rephrase the already surfaced tentative synthesis instead of discovering anything new.
2. Broad self-evaluations could be accepted largely from first-person description without testing whether the pattern is externally visible, differs from outward presentation, or is described differently by familiar observers.

The owner also clarified the product purpose: Life Patterns is intentionally meant to produce useful person-specific evidence for later astrology / Human Design analysis **and** for InnerSignal. Avoiding target leakage must not be misinterpreted as making the measurement instrument indifferent to which behavioral dimensions are informative.

No private owner interview narrative is preserved in this receipt.

## Design decision: target-aware instrument, target-blind runtime

The current design distinction is:

- **instrument design may be target-aware**: development may deliberately prioritize neutral behavioral dimensions because they are likely to discriminate person models relevant to astrology / Human Design and to InnerSignal;
- **participant execution remains target-blind**: the runtime interviewer does not receive the participant's chart, target-model mapping, expected answer direction, score, or hidden theory label, and participant-facing questions remain behavior-first.

This prevents an unnecessary false choice between scientific blindness and collecting useful evidence. What remains prohibited is tailoring questions to the participant's known chart or leading toward expected target answers.

## Repair 1: `Keep trying` now means new inquiry

The active-proposal refinement path now has a dedicated refinement planner rather than reusing the ordinary synthesis planner.

On the first `Keep trying to pin it down` call:

- the button action is recorded as a conversational user turn;
- the refinement schema does not allow `surface_hypothesis`;
- the model is explicitly prohibited from repeating, restating, lightly rephrasing, or simply re-presenting the current synthesis;
- it must ask at most one genuinely decision-changing question, or state that no high-value unresolved discriminator remains;
- a defensive fallback converts any attempted repeated synthesis into a genuinely new observer-triangulation question rather than replaying the proposal.

Answers to refinement questions continue through the same dedicated refinement reasoning path.

Current limitation: this repair gathers new evidence without yet automatically generating a revised formal proposal from post-proposal evidence. The participant can still adjudicate/revise explicitly. Automatic model-generated proposal revision is a separate product change because it must preserve post-proposal provenance rather than pretending later evidence was pre-proposal evidence.

## Repair 2: observer / self triangulation

Broad evaluative self-labels such as balanced, chill, intuitive, independent, empathic, stubborn, sensitive, or rational are not treated as sufficiently discriminating merely because the participant endorses them.

When useful, an early neutral discriminator is now:

- whether people who know the participant well tend to describe them similarly or differently;
- whether outward presentation differs from inner experience.

Observer evidence is provenance-separated:

- `the participant says X about themself`;
- `the participant reports that familiar others say X`;
- direct behavioral/event reports

remain distinguishable. A secondhand observer report is useful evidence about externally visible reputation or self/observer convergence, but is **not** silently promoted into verified objective truth.

## Neutral high-value discriminator menu

The interviewer now has a non-mandatory menu and selects only the one unresolved dimension whose plausible answers would most change the formulation:

1. self-view vs familiar observer-view;
2. inner experience vs outward presentation;
3. baseline vs triggered state and recovery;
4. automatic first response vs deliberate/learned management or compensation;
5. context/domain stability;
6. timing, threshold, intensity, duration, escalation, stopping, recovery;
7. developmental continuity/change and learned adaptation;
8. decision phenomenology: what comes first in body, feeling, thought, attention, or action; immediate vs delayed clarity;
9. social entry/role: self-initiated vs responsive/recognized entry, one-to-one vs group, roles accepted/resisted;
10. energy/recovery: engagement, sustainable range, overload, stopping, retreat/restoration;
11. capacity vs preferred use, especially communication, persuasion, leadership, caregiving, confrontation;
12. relating/conflict/boundaries: closeness, reciprocity, sensitivity, first conflict response, repair/withdrawal, trust/access;
13. attention/cognition/work: focus, interruption, learning, synthesis, novelty/continuity, project selection, persistence/stopping;
14. values/purpose/salience: what reliably mobilizes effort or is easy to ignore;
15. sensory/environmental conditions that materially change functioning;
16. coexisting modes that differ by intensity, context, role, or timescale rather than forcing one trait pole.

This is explicitly **not a checklist** and does not restore quota-driven interrogation.

## Why this matters scientifically

A self-concept may differ materially from observable social presentation or from how familiar others describe the person. That discrepancy is itself potentially informative; collapsing the sources would lose information.

Similarly, later astrology / Human Design model comparison benefits more from neutral discriminators such as automatic-vs-deliberate response, decision timing, initiation/recognition, recovery dynamics, capacity-vs-preference, context dependence, and developmental shifts than from generic self-evaluations alone.

The same distinctions improve an InnerSignal person model without requiring external-theory labels in the interview.

## Verification / deployment

Implementation:

- `src/hdmatch/api/life_patterns_v2_owner_reasoning.py`
- `tests/unit/test_life_patterns_v2_owner_reasoning.py`

Application behavior commit: `96c5ef374d92e0e44d4c6811961e7e9b1878a90a`.

Regression/test commit: `17ef230d51c2298ac6ca0a69c5cc4c3922b4a46d`.

Final application/code checkpoint: `b46d480acf2209b5416f6ef158fd64de32a5358a`.

GitHub Actions run `34915009454`: **SUCCESS**. The preceding behavior/test run established **736 passed / 7 skipped**, Ruff passed, and exposed only a static typing issue at the dynamic refinement-planner boundary; the final checkpoint repairs that type boundary and passes tests, Ruff, and strict mypy.

Existing authenticated owner-only Railway service reused. Final deployment `f4a49e7d-b0b1-4929-a3ad-9bbb11092ef6` from source `b46d480acf2209b5416f6ef158fd64de32a5358a`: **SUCCESS**, application startup complete, `/healthz` HTTP `200`.

Health contract declares:

- `observer_triangulation=true`;
- `neutral_person_model_discriminators=true`;
- `refinement_repetition_guard=true`;
- existing `person_specificity_gate=true` and adaptive/no-quota flags remain.

No new service, public access, participant transcript persistence, target scoring, chart-aware runtime routing, or request-body logging was added.

## Next decision-changing owner evidence

Retest the same kind of broad self-description:

1. the first useful clarification should prefer observer/self or inner/outer discrimination when still unresolved rather than demanding an arbitrary episode;
2. after a synthesis, `Keep trying to pin it down` must produce a genuinely new question, never the same conclusion again;
3. answer that question and judge whether the next inquiry uses the new evidence rather than reopening settled material;
4. verify the interviewer remains selective instead of marching through the discriminator menu;
5. later test a different domain (decision-making, relationships/conflict, work/attention, energy/recovery, or values/purpose) to judge whether the neutral target-aware instrument captures useful person-specific distinctions.

A separate future product decision remains: whether to add a light adaptive coverage sweep after user-led pattern threads so important under-observed domains are not missed merely because the participant did not spontaneously volunteer them.

**There was never a completion policy.**