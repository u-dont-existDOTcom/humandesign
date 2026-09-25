# Life Patterns development coding manual v1

Status: **frozen development manual** for partial-source v8/v8.1 transfer evidence. This is not a validation manual and does not promote the transfer corpus to a canonical behavioral freeze.

## Purpose and blind

Apply the supplied theory-neutral Life Patterns measurement package to participant-reported behavioral evidence. Do not use or infer any external model, typology, birth-derived system, diagnosis, spiritual framework, personality score, or target hypothesis.

Target-model, birth/chart, prediction, fit, rank, and outcome information must be unavailable during coding.

## Measurement authority

Use substantive measurement inputs in this order:

1. immutable reconciled theory-blind codebook v1;
2. frozen theory-blind non-action ambiguity-resolution amendment;
3. content-addressed resolved codebook view v2;
4. resolved development ontology;
5. Structured Coding Procedure V2, including the exact non-action and Other Specified registries;
6. this manual;
7. the supplied development evidence task.

The amendment changes only the explicitly resolved subcodes. `R07-a` and `R16-d` are retired in the resolved view and must never be emitted. Use the resolved replacements and clarified evidence rules exactly.

## Evidence layers are distinct

There are two development evidence kinds.

### Episode task

A `DevelopmentEpisodeCodingTask` contains one bounded behavioral episode reconstructed from the participant's v8/v8.1 transfer material. It is development-only and may have only partial exact source coverage. Its `exact_source_segments` are primary evidence. Its `episode_narrative`/transfer summary is secondary orientation and must never substitute for missing exact source support when asserting an observed value.

Do not split or merge the episode. Do not import another episode or a global pattern claim unless that material is present in an exact source segment in the task.

### Repeated-series task

A `DevelopmentSeriesCodingTask` contains a participant report that behavior recurred across multiple opportunities or occasions. It is **not an episode** and must never be counted as one. Exact source segments are primary evidence; summary fields are secondary orientation.

A series may support recurrence only when the participant's exact language establishes repeated occurrence. Do not convert vague generic language into a fabricated count. `minimum_reported_occurrences` is a conservative floor, not an estimate of the true number. Use 2 only when the source establishes at least two occurrences, 3 when it establishes at least three, and a larger number only when the source itself supports that lower bound. If recurrence cannot be established, use `insufficient`.

Initial series coding does not infer whether a detailed episode is included in the series. Unless an explicit anchor candidate and evidence are supplied by a later task, use no anchor identity/relation.

## Primary state

Use only:

- `observed`
- `insufficient`
- `not_applicable`

Use `not_applicable` only when the observable's prerequisite circumstance is affirmatively absent. Use `insufficient` when the prerequisite may apply but the exact evidence cannot support a reliable decision.

Do not encode person-level `mixed` or `contradicted` states in primary evidence coding. Cross-evidence distributions and contradictions are derived later.

## Substantive values and sequences

For `observed`:

- emit only value IDs allowed by the exact resolved ontology;
- never invent, rename, merge, or split values;
- use `single` for one supported value;
- use `ordered_sequence` for two or more supported values whose relevant order is established;
- preserve the order exactly;
- use `unordered_multiple` only when multiple values are independently supported but their relevant order cannot be established;
- do not emit multiple values as a hedge between alternatives; use `insufficient` instead.

## Other Specified

Use the registered `OS`/Other Specified value only when the observable prerequisite is satisfied, the concrete behavior belongs within the observable, and none of its listed resolved values adequately represents the behavior.

An observed Other Specified response requires a concrete `other_specified_description` grounded in exact source evidence. Do not use Other Specified as a substitute for insufficient evidence.

## Non-action gate

A registered non-action value may be coded only when all four elements are established from the evidence:

1. awareness;
2. meaningful opportunity/window;
3. reasonable feasibility;
4. established non-occurrence during that window.

If any element is unclear or not established, do not assign the substantive non-action value. Use `insufficient`. Silence or non-mention is never non-action.

A coded non-action value requires `asserts_non_action=true` and a fully established `NonActionGateAssessmentV2`. A value not registered as non-action must not be converted into a non-action inference merely because it involves delay, decline, waiting, reduced participation, stopping, or later action.

## Missingness and uncertainty

Allowed missingness flags are:

- `UNK`
- `APPROX`
- `CONFLICTING-RECALL`
- `UNCLEAR-AGENCY`
- `UNCLEAR-AWARENESS`
- `UNCLEAR-OPPORTUNITY`
- `UNCLEAR-FEASIBILITY`
- `UNCLEAR-WINDOW`
- `UNCLEAR-SEQUENCE`
- `UNCLEAR-ENDPOINT`

Use a flag only when that uncertainty matters to applying the observable. Do not manufacture missingness merely because an unrelated detail is absent.

Approximate ages/life phases remain approximate. Do not turn a remembered life period into a precise date or onset. A behavior reported by a given age is not automatically established as having begun at that age.

## Source provenance

Observed episode and series annotations require exact source-segment citations from the supplied task. Do not cite a transfer summary as primary source evidence.

Episode responses may cite exact segments as supporting evidence, counterevidence, and influence evidence. Series responses cite exact segments supporting the repeated report. Citations outside the task are forbidden.

A participant-stated explanation is evidence that the participant reported that explanation, not proof of objective causation.

## Influence

For episode coding:

- `none_reported`: no relevant influence relation is recorded;
- `narrator_explicit_influence`: the participant explicitly says one event/state affected, prompted, changed, prevented, or contributed to another;
- `temporal_precedence_only`: the relevant event/state preceded another but influence was not established.

Never upgrade chronology alone to explicit influence.

## Context and global claims

Record context only when directly supplied. Do not infer demographic, moral, clinical, motivational, cultural, or personality explanations.

A statement such as "I always...", "usually...", or "I never..." belongs to a repeated-series/global evidence layer. It does not make an individual episode observed unless the episode's own exact source evidence satisfies the observable.

Conversely, one vivid episode does not establish a recurring person-level pattern.

## Theory exposure

Preserve the task's participant theory-exposure provenance. Do not infer hidden exposure. Exposure metadata is not a substantive behavioral value.

## No confidence theater

Do not invent numerical confidence, personality scores, rankings, latent trait levels, or typology assignments. Use explicit insufficiency and missingness.

## Development boundary

All outputs under this manual are development-only. They cannot be promoted to validation merely because multiple automated passes agree. Independent human calibration and a separately frozen validation route remain required before any confirmatory target-model comparison.
