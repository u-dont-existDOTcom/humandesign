# Life Patterns owner pilot — public-safe design audit

**Status:** development evidence only. This audit is based on one known development participant and does not estimate population prevalence or validate a personality instrument. The exact private source and review identifier are not committed.

## Inputs inspected

- Exact private source-only interview: 79 participant answers.
- The same live independent-review result after three clarification rounds.
- Participant-facing final-submission screenshot and safe validation diagnostic.
- Frozen public route/question authority and current GPT/runtime contracts.

## Aggregate response signals

These counts are lexical/structural diagnostics, not psychological findings:

| Signal | Count |
|---|---:|
| Answers inspected | 79 |
| Answers explicitly using a “depends” condition | 13 |
| Answers explicitly expressing uncertainty / not knowing | 9 |
| Answers of 10 words or fewer | 31 |
| Answers of 5 words or fewer | 10 |
| Answers of 3 words or fewer | 6 |
| Explicit recorded question-design feedback events | 4 |

Shortness alone is not a failure. The decision-relevant pattern is that several short, obvious, premise-driven or under-specified responses could pass through as if they settled a recurring-person pattern unless the reviewer evaluates information gain and construct discrimination.

The four explicit design-feedback events occurred on public route IDs `WORKING-METHOD`, `ROMANCE-FADE`, `B0`, and `G10`. They represented four different defects:

1. a rational response to an adequate method was mistaken for novelty/stability evidence;
2. an obvious inverse of an earlier closeness question was asked as a separate task;
3. the entire scene was repeated when only one missing clause should have been asked;
4. a follow-up asked for a boundary the participant regarded as already implicit.

## Additional response-derived redesign priorities

The exact answers exposed several additional public route-level risks beyond the four explicit complaints. These are **development triage labels**, not claims that every answer on the route is invalid:

| Risk class | Public route IDs observed in this pilot | Design consequence |
|---|---|---|
| Prompt largely supplies the rational answer or invites a tautology | `WORKING-METHOD`, `ROOM-EFFECT`, `CORRECTION-REASON`, `R13`, `M11` | Require evidence that plausible answers would discriminate a person-level pattern; otherwise retire/demote or ask a narrower non-obvious boundary. |
| Broad prompt naturally produces context dependence but does not elicit the deciding boundary | `G09`, `G15`, `ROUTINE-CHANGE`, `M09` | Treat named conditions as useful; do not force a pole. Ask one boundary only when it can materially change interpretation. |
| Very short/generic response can be mistaken for a trait merely because coverage exists | `G04`, `STATUS`, `M03`, `G03`, `G02` | Judge semantic sufficiency, not answer presence or length. Preserve unresolved/conditional rather than inventing a broad trait. |
| Full scene repeated when only one clause was missing | `B0` | Acknowledge established content and ask only the missing feeling, threshold, condition or response. |
| Obvious inverse/duplicate of an earlier question | `ROMANCE-FADE` | Ask only for additional weakening conditions not already implied by the earlier closeness answer. |

Most of the high-risk canonical routes are already retired from ordinary new elicitation by the tendency-first policy. Remaining legacy probes are now subject to the stronger source-exposed-gap and material-information-gain gates. No blanket minimum-answer-length rule was added: a short answer can be decisive, while a long answer can still be non-discriminating.

## Final-review defects

The live final review contained six admitted evidence entries but did not tell the participant what neutral construct/distinction each entry measured. One entry also combined two disconnected source tasks—recognition value and ownership/use concern—under one apparent finding. This makes it hard to evaluate whether the answer actually informed the intended construct and can make a narrow observation look like one broad trait.

## Approval-flow defect

The participant was warned generally that Action approval cards might occur, but the live flow did not reliably show the required immediate sentence before the final Action. A clarification round also left another external call/permission interaction after the participant believed the first Allow would complete the round. A lifetime fixed count is impossible because clarifications are adaptive, but the remaining calls within the current phase are knowable and should be stated before the participant leaves.

## Metadata defect

The post-freeze module asked whether ChatGPT Memory was enabled. That is not the relevant observable contamination boundary for this Custom GPT flow. The research record should instead capture whether birth/chart/Human Design information was actually visible in the authorized conversation/source, while chart-familiarity questions remain post-freeze to avoid priming.

## Final-submission defect

The server required exact primary and CF-003 objects, but the Custom GPT Action interface exposed free-form object parameters unreliably. The request was rejected before storage. The repair transports each exact frozen object as a verified raw JSON string, then parses and validates it through the unchanged server-side scientific/storage checks.

## Design rules derived from the pilot

1. **Information gain before coverage.** Missing route coverage is never enough. An answer must distinguish materially different person-level readings.
2. **Conditionality is evidence, not evasion.** A “depends” answer that names discriminating conditions can be useful. A bare “depends” remains unresolved rather than being forced into a pole.
3. **Obvious/premise-driven answers are not traits.** Rational compliance with supplied constraints, tautologies and obvious inverses are not promoted into recurring-pattern evidence.
4. **Ask only the missing clause.** Acknowledge what is already established; do not restate a full scene to extract one omitted feeling, threshold or condition.
5. **Process feedback stays separate.** “This is redundant/obvious/under-specified” is instrument feedback, not personality evidence. A substantive answer in the same reply may still be coded separately.
6. **One coherent construct per evidence item.** Related subfacets may remain together; disconnected measurement tasks must be split.
7. **Make measurement inspectable.** Every final-review entry names the neutral measured distinction, conditions and exact supporting quotes. Multiple distinctions are displayed separately.
8. **Invite resistance early.** Participants are explicitly told that challenging a weak question is useful data. This reduces pressure to supply a low-information answer merely to proceed.
9. **Phase-local permission forecast.** State the known remaining service calls and possible permission cards for the current phase, then show the exact Allow instruction immediately before each consequential Action.

## Limits

This pilot can expose logical, usability and implementation defects. It cannot establish how often other participants would challenge weak prompts, whether the revised questions discriminate in a population, or whether any measured construct predicts an external target. Those require separate development participants and untouched validation data.
