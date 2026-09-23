# Post-freeze scorer translation protocol — 2026-09-23

Status: **frozen-method candidate before either new birth-search result is opened**.

## Boundary

The target-blind neutral measurement is already frozen. Its private final neutral profile SHA-256 is `7dc6333e42510c0fad145c2a90a6385051b20637b82da30281f6bc80361320a7`.

Only now may scorer-specific semantics be exposed. Translation must not feed backward into the neutral profile, question selection, coding, or adjudication.

Run the V1.1 and clean V4.3 translations in separate fresh contexts from the same frozen neutral profile. Neither translator receives birth data, chart states, candidate scores/ranks, historical winner dates/times, or the other translator's output.

## Behavioral-confidence scale

Use the pre-existing V3 behavioral-confidence classes; do not invent custom decimals:

- `1.00`: repeated, specific, stable, or explicitly emphasized across contexts/time;
- `0.75`: clear and specific but based on fewer contexts or less repetition;
- `0.50`: moderately supported, context-sensitive, or somewhat interpretive;
- `0.25`: weak, tentative, generic, or newly reported without corroboration;
- `0.00`: unknown / do not score.

Confidence is confidence that the **scorer-specific behavioral claim** is established by the frozen neutral evidence. It is not confidence in Human Design, astrology, a chart candidate, or the historical scorer.

## Direction

For every pre-existing crosswalk row classify the frozen neutral evidence as:

- `supported`: the scorer-specific behavioral claim is supported to the stated confidence;
- `not_established`: the frozen neutral evidence does not establish that scorer-specific behavioral claim.

`not_established` gives the positive claim confidence `0.00` unless a **pre-existing scorer contradiction mapping** already represents a separately translated negative behavioral claim. Translation may not invent a new opposite chart mapping.

Coverage status (`full`, `partial`, `uncovered`) is evidence context, not an automatic numeric conversion. A fully measured neutral domain can contradict a historical claim; a partial domain can still clearly support a narrow historical claim.

## V1.1 merged HD + Western translation

Use only the frozen `historical_merged_cluster_crosswalk` and the historical V1.1 behavioral target/model semantics.

For each historical cluster freeze:

- neutral domain;
- relation (`supported | not_established`);
- translated behavioral confidence from the five-value scale;
- supporting neutral facet IDs and bounded evidence summary;
- conditions/limits;
- rationale.

For a future reconstructed V1.1 scorer, the translated behavioral confidence replaces the old cluster behavioral-confidence value. HD/Western structural feature definitions, salience/directness tuples, `rho=0.25`, `cap_multiplier=1.25`, contradiction definitions, astronomy, birthplace convention, search universe, and ranking procedure remain historical/frozen. No cluster is added or structurally remapped.

The V1.1 search remains blocked unless a reconstructed scorer first reproduces the historical frozen V1.1 result exactly enough to satisfy the declared reproduction gate. An approximation must be labeled unresolved, not pass.

## Clean V4.3 / NetInformation translation

Use only the frozen `clean_v36_information_crosswalk`, the frozen V4.3 base mapping plus its pre-ranking v2 overlay, and exclude all mappings flagged `post_selection=true` from the primary comparison.

For each crosswalk observable freeze:

- neutral domain;
- relation (`supported | not_established`);
- translated behavioral confidence from the five-value scale;
- supporting neutral facet IDs and bounded evidence summary;
- conditions/limits;
- rationale.

Resolve each positive crosswalk `observable` deterministically before scoring: if it exactly matches a frozen mapping ID, select that mapping only; otherwise it names a dependency cluster and selects all candidate-unexposed mappings in that cluster. An `observable` of the form `CONTRADICTION:X` selects the pre-existing contradiction cluster `X`. Unknown selectors fail closed. Only `supported` rows with nonzero confidence enter scoring.

For candidate-unexposed mappings selected by a positive observable, use:

`effective_mapping_confidence = min(frozen_mapping_confidence, translated_behavioral_confidence)`.

This preserves every pre-existing structural mapping/directness/salience/flexibility cap while preventing the new survey from claiming stronger behavioral evidence than either source permits.

For a mapped pre-existing contradiction cluster, the translation decides whether that *negative behavioral claim* is supported. Its translated confidence analogously caps the frozen contradiction confidence. No new contradiction is created.

Non-crosswalk behavioral clusters are excluded from the survey-instantiated primary NetInformation total. The historical frozen V4.3 `core` block is not re-used as survey evidence because the owner-recovery crosswalk did not instantiate it from the neutral measurement; therefore CoreFit is treated as constant/unavailable for this survey-instantiated comparison rather than silently importing the historical target. For the same reason, exact states that differ only in historical core fields but have identical translated mapping/contradiction matches are merged before the duration tie-break. Ranking otherwise preserves NetInformation descending, meaningful contradictions ascending, DetailedSupport descending, then stable duration. This must be labeled a **survey-instantiated clean V4.3/NetInformation crosswalk run**, not the untouched historical V4.3 audit.

## Freeze-before-search rule

Both translated profiles must be serialized and SHA-256 frozen before either scorer's new candidate ranking is generated or inspected. After either search result is opened, no translation confidence, direction, included cluster, or scoring adapter rule may be changed within this run.

Candidate-exposed Personality-Moon-24 and Design-Mars-61 refinements are excluded from the primary V4.3 comparison and may only be run later as a separately labeled historical descriptive diagnostic.
