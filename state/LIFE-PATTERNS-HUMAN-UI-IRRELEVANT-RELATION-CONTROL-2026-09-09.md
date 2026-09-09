# Life Patterns human UI — irrelevant single-value relation control

Date: 2026-09-09

Status: owner-detected pre-collection human-interface defect; corrected before any qualifying independent human first pass.

## Defect

The human calibration UI displayed a value-relation dropdown labelled in substance “if more than one behavior is selected, how do they relate?” even when the auditor had selected exactly one behavioral value.

That control had no human decision to collect in the single-value case. The machine response contract already represents one selected value with `value_relation = single`, so asking the auditor to choose `One behavior` after they had visibly selected one behavior was redundant bookkeeping and could create confusion or invalid states.

## Correction

Presentation-only:

- exactly one selected behavior → `value_relation = single` is encoded automatically and no relation control is shown;
- zero selected behaviors → no relation control is shown;
- two or more selected behaviors → the relation control appears and asks only the discriminating question: whether the selected behaviors occurred in an established order;
- the human choices for multiple values are `ordered_sequence` versus `unordered_multiple`; the single-value option remains a hidden serialization value only;
- internal behavioral code IDs are hidden from the human-facing list;
- the existing value IDs, response schema, selected units, private evidence, content-addressed handoff, recurrence semantics and blinding remain unchanged.

## General interface principle

Do not expose a conditional metadata field when its value is already determined by the user's preceding substantive choice. Collect a human judgment only where multiple valid states remain. Machine provenance/serialization should be automatic when deterministic.

## Boundary

This correction is not a measurement revision, resampling event, annotation, consensus operation or target-model action. Automated coding remains blocked until the independent human first pass is completed and frozen.
