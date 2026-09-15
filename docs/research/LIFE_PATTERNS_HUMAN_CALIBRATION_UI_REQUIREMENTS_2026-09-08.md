# Life Patterns human-calibration UI requirements — 2026-09-08

Status: operational transport/UI requirement only. This does not alter the frozen codebook, ontology, procedure, calibration selection, packet bytes, response schemas, or scientific chronology.

## Problem

The verified private human-calibration handoff is currently machine-oriented: the auditor would have to inspect packet JSON and hand-edit JSONL response rows. That is inappropriate as the default human workflow and creates avoidable transcription/schema errors unrelated to the behavioral judgment being calibrated.

The human task is substantive judgment; JSON is only the interchange format.

## Required interface

Before asking an independent auditor to complete the first pass, provide a theory-neutral local/offline annotation UI that:

1. loads the already-verified private human-calibration handoff without sending participant text to a server;
2. verifies the frozen handoff receipt/file hashes before presenting any case;
3. renders one assigned episode/series × observable unit at a time in ordinary language;
4. shows the observable definition, inclusion/exclusion criteria, minimum evidence requirements, allowed substantive values, exact source segments, relevant context, and any frozen non-action/Other-Specified rules needed for that unit;
5. keeps transfer summaries clearly secondary to exact participant source segments;
6. offers ordinary controls for `observed`, `insufficient`, and `not_applicable`, permitted values, value relation, source citations, missingness, non-action gate, recurrence floor where applicable, context qualifiers, and notes;
7. prevents impossible/schema-invalid combinations instead of expecting the auditor to know JSON structure;
8. keeps episode and repeated-series evidence visibly separate;
9. includes the independence/exposure attestation as an ordinary form;
10. exports the exact existing response contract: completed episode JSONL, completed series JSONL, and completed attestation JSON, without changing identities or fixed constants;
11. makes no network requests and contains no Human Design/chart/birth/target-model information, expected answers, automated labels, or consensus;
12. does not use AI or automate the human judgment.

A UI-generated response must validate under the existing frozen response schemas and human-calibration validator exactly as a hand-authored JSONL response would. UI implementation details have no authority to reinterpret the codebook.

## Narrator global claims and recurring self-report

The statement `I always X` is **not zero evidence**. It is direct evidence that the narrator reports/perceives X as recurrent. The measurement distinction is:

- it is evidence for a **narrator recurrence/global claim**;
- it is not by itself an **episode-level observed behavior**, because no bounded episode has been supplied;
- it does not establish the literal universal proposition that X occurred on every possible opportunity;
- it does not by itself establish an occurrence count unless the narrative also establishes repeated opportunities/instances;
- where the source provides a bounded repeated-series report with enough recurrence information and exact participant text, the separate series-evidence layer can code that recurrence without pretending it is an episode.

The same principle distinguishes a behavioral recurrence claim (`I always checked the door before leaving`) from a trait label (`I am always cautious`). The former is relevant behavioral self-report; the latter is primarily a narrator interpretation unless concrete behavior is supplied.

The current frozen first pass must apply the frozen measurement rules consistently. If pilot evidence later shows that the treatment of global/series self-report is too strict or too permissive, that is a theory-blind post-pilot revision question and requires a new version rather than silent reinterpretation mid-pass.

## Operational gate

The independent human first pass remains the scientific gate. The usable annotation UI is an operational prerequisite for collecting it without imposing a software-engineering task on the auditor. Do not expose automated labels while building or using the UI.
