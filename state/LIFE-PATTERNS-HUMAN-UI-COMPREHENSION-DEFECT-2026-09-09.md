# Life Patterns human-calibration UI comprehension defect — 2026-09-09

Status: **blocking human-use defect** discovered before any qualifying independent human first pass. This record is theory-neutral and does not change the frozen participant evidence, selected calibration units, target-model blind, or substantive recurrence correction.

## Owner-observed failure

The owner opened the private offline calibration UI and identified a concrete human-comprehension failure on an episode × observable unit where the exact source described the narrator **offering help to another person**, while the assigned observable was `NBM-R16 — Help seeking/use`.

The current UI presented the observable definition, `Observed / Insufficient / Not applicable`, behavioral subcodes, source checkboxes labelled only `Supporting / Counterevidence / Influence source`, and a generic `Narrator influence / precedence` section.

The result was predictably ambiguous to a non-codebook author:

- it was not explicit that `NBM-R16` asks about **the narrator seeking/accepting/using another person's help**, not the narrator offering help to someone else;
- `Supporting` had no plain-language object — supporting *what* was unclear before a code was selected;
- the generic influence field appeared to ask for a relation unrelated to the current observable;
- advanced metadata and codebook jargon were visible before the simple human judgment had been made;
- the UI did not explain that a calibration unit is one **specific behavior question applied to one story**, and that a clean `No / prerequisite absent` is a legitimate result rather than an instruction to make the story fit the observable.

## Correct interpretation of the example

Under the frozen `NBM-R16` semantics, the narrator is the person whose behavior is being coded. `NBM-R16` concerns how that narrator requests, signals for, accepts, declines, delegates to, or uses **another person's assistance** for the narrator's concrete task/need.

Therefore an episode that only shows the narrator **offering assistance to someone else** does not by itself satisfy R16. If exact source contains no narrator-side need/helper relationship, the R16 prerequisite is absent and the appropriate state is `not_applicable`.

The pairing itself is not proof of a sampling bug: the frozen calibration samples episode-observable units before labels, so some non-matching units are expected and are useful for testing false-positive rejection. The defect is that the current interface makes that ordinary negative judgment difficult to understand.

## `Supporting` semantics

`supporting_source_segment_ids` means: exact source segment(s) that support the **specific behavioral annotation selected for the current observable**. It does not mean “supports the story,” “supports the observable generally,” or “supports the project.”

The current label `Supporting` is therefore insufficiently scoped and must not remain in the human UI.

For an observed code, the human-facing label should be equivalent to:

> Use this quote as evidence for the behavior I selected.

Counterevidence should be presented as an optional qualifier to the selected code, not as an unexplained parallel category.

## Narrator influence / precedence semantics

The underlying field is causal-provenance metadata. It distinguishes:

- `narrator_explicit_influence`: the narrator explicitly says an earlier event/state affected the behavior being coded;
- `temporal_precedence_only`: the earlier event merely occurred before the behavior, with no influence claim;
- `none_reported`: no such relation is being recorded.

It is **not** a general question about who influenced whom in the story. In the owner example, the phrase equivalent to “I saw she was sad, so I offered…” may express narrator-stated influence on the *help-offering action*, but that is irrelevant to an R16 help-seeking unit if R16 itself is not observed.

The UI must therefore scope this field to the **currently coded behavior**, hide it for `insufficient/not_applicable`, and move it behind an optional advanced disclosure for observed episode codes.

## Required transport correction

Do not collect a human first pass with the current UI/kit. Preserve existing files and receipts as historical transport artifacts, but supersede them for human use with a presentation-only revision that keeps the exact response contracts unless a stricter schema version is independently required.

The corrected interface must:

1. put a plain-English **question for this unit** above the codebook detail;
2. explicitly define `narrator = the person whose story is being coded`;
3. state that some story/question pairs legitimately do not match and must not be forced;
4. map states to ordinary human decisions while preserving exact exported values:
   - `observed` → `Yes — clearly shown`;
   - `not_applicable` → `No — this situation does not meet the prerequisite`;
   - `insufficient` → `Can't tell — not enough evidence`;
5. give observable-specific subject/boundary clarification, especially distinctions such as `seeking help` versus `offering help`;
6. collapse formal include/exclude/minimum-evidence rules behind optional detail;
7. show source-citation controls only when they have a clear role and label them with their object;
8. scope influence metadata to the selected behavior and hide it unless relevant;
9. collapse missingness/context/language/coder-note fields as optional advanced detail;
10. hide or de-emphasize internal IDs and transport metadata not needed for judgment;
11. keep the measurement-bearing evidence, selected 44+22 units, response values, blinding boundary, and no-network/no-AI behavior unchanged;
12. receive a new browser smoke pass on the exact private HTML before auditor delivery.

## Sampling note

The current deterministic 44 episode + 22 series selection contains deliberately unlabeled episode/observable and series/observable units. Because selection occurred before any automated labels, it can include true positives, negatives, and ambiguous units.

Do **not** reselect units now merely because one observed pairing is an obvious negative; doing so after seeing evidence would create post-selection. First repair the human transport. After the independent first pass is frozen, inspect the state/value coverage. If the frozen random-stratified sample contains too few observed substantive-value cases for reliable value-level calibration, pre-specify a separate second-stage calibration design rather than silently treating this sample as evidence it cannot provide.

## Scientific boundary

This defect was found before a qualifying independent human response existed. Fixing human comprehension now does not contaminate human-vs-automated comparison, provided no automated labels or target-model outputs are consulted and the substantive measurement/selected evidence are not tuned to an expected result.
