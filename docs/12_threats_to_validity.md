# 12 — Threats to Validity

## Circularity
Synthetic cases are intentionally circular at the theory level.
They validate implementation only.

Human development fit is also in-sample by definition.
It develops the model but does not validate it.

## Researcher degrees of freedom
Repeatedly trying mappings/questions can manufacture apparent fit.

Mitigation:
- development/version logs;
- untouched test cohort;
- exact model hashes;
- automated baselines/permutation tests.

## Self-report reinterpretation
Participants who know their HD chart may reshape answers toward it.

Mitigation:
- prioritize HD-naive participants;
- collect responses before interpretation;
- ask examples/counterexamples;
- include observer/behavioral corroboration where possible.

## Birth-date leakage
Personality questionnaires can accidentally reveal age, season, birthday customs, cohort effects, or zodiac knowledge.

Mitigation:
- exclude such items;
- scan free text;
- use matched candidate universes;
- compare calendar/season baselines.

## Seasonality / cohort confounding
If day/month predicts behavior through non-HD social or seasonal mechanisms, a date-recovery effect is not necessarily HD-specific.

Mitigation:
- candidate universes within the same month/year;
- compare HD features with raw astronomical/calendar features;
- out-of-location replication.

## Exact-time uncertainty
Many birth records are rounded.

Mitigation:
- distinguish documented exact times from remembered times;
- model record precision;
- treat ±5/15/30 minute uncertainty as intervals where appropriate.

## Timezone ambiguity
Same UTC instant can have different local representations.
HD cannot identify timezone independently from identical UTC chart states.

## Trauma / body access
May affect reporting of decision phenomenology.

Mitigation:
- reliability modifier only;
- separate chart-resonance hypothesis from somatic-usability hypothesis;
- no automatic rescue explanation.

## Multiple testing
Trying many model variants inflates apparent success.

Mitigation:
- nested model selection;
- correction/transparent model count;
- final untouched test.
