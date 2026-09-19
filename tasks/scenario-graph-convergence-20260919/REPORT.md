# Scenario-first survey — graph audit and convergence

19 September 2026. Candidate: **scenario-bank-v6.0-20260919**. Text-only design; owner pilot remains paused.

## Judgment

**The final complete review required no further changes to the questions, follow-up rules or evidence interpretations. This now meets the owner's requested “changed almost nothing; it's good” boundary in my design judgment.**

That statement describes the final pass, not the entire turn. The initial audit made two question-wording changes, repaired one missing context link and normalized the context metadata of self-contained questions. It also corrected one fictional illustration and narrowed one interpretation example. The new graph audit model itself needed repairs before its final confirmation. None of those changes is hidden by the final zero-change result.

This is same-context semantic review supported by explicit-state tests. It is not independent review, validation with people, a live test of the Railway interviewer, or proof of full AstroHD recovery.

## What converged

| Reviewed layer | Earlier work in this turn | Final complete sweep |
| --- | --- | --- |
| Question wording | 2 of 79 prompts revised; no new questions | 0 changes |
| Scene context | M02 linked to M01; 40 self-contained context fields clarified | 0 changes |
| Interpretation guide | 1 scene-aligned illustration; 1 calm-versus-concern clarification | 0 changes |
| Graph admission model | Fixed comparison and inherited-topic handling | 0 changes |
| Scope | All 79 entries, 73 interpretation guides, 28 families and 136 graph links reviewed | No identified material defect left open |

The last row describes review coverage, not questionnaire accuracy or evidence sufficiency. The 73 labels remain planning aids, not 73 mandatory answers or a full-profile score. The final sweep includes the 32 frozen prior dialogue examples and 16 graph-focused examples. All are authored examples, not new participant observations.

## The graph helps because the links have different meanings

`GRAPH-EXPLORER.html` contains a readable overview, a friend-invitation example and 28 topic diagrams. Every question has an expandable text panel with its actual wording, admission condition and interpretation limit. The document is searchable, offline and read-only: it collects no responses and is not a replacement application.

The graph separates three relations:

- **Context candidate:** an earlier scene or answer that can supply a follow-up's referent. Alternatives are not a list of required previous questions. An equivalent volunteered answer can supply the context.
- **Topic association:** related material that may help navigation but is not a prerequisite. A standalone question does not become impossible merely because an associated question has not been asked.
- **May inform:** information a question could elicit. Presenting it never establishes that information; the actual answer must support the narrower claim.

The protocol remains the authority for meaning. The graph is a maintained index over it, not a fixed route through all 79 entries. Mermaid source is supplied in `SCENARIO-GRAPH.md`; the bundled diagrams were rendered with Graphviz from the same graph records. Native GitHub Mermaid rendering was not separately tested.

## Small questionnaire repairs

The method-change question now names a specific task: following instructions to set up a shared calendar, with the invitation step failing. It no longer asks the respondent to invent what is being set up.

The prolonged-workload question now explicitly resets from the manageable-work baseline and asks about energy at the end of that period, matching the response task used for the other workload scenes. Intensity, duration and rest remain explicitly bundled conditions, not a one-factor causal experiment.

The pressure-aftermath question referred to “that person” but had no recorded context link. It now points to the original pressure scene. After an intervening topic, its delivered wording must name that scene, rather than rely on proximity.

The interpretation guide now preserves both parts of “I'd become concerned but stay calm.” Calmness does not establish that no emotion changed. A separate illustration was aligned with its actual meeting-place scene. The original fictional transcripts were not rewritten.

## Repairs found in the new graph model

A contrast can be expressed in one reply: “Unasked, I'd do a small task; if asked, I'd coordinate.” Requiring two separate answer events would cause redundant questioning. The model now requires distinct conditions, not distinct messages.

An explicitly declared earlier-versus-current contrast intentionally changes time perspective. It must not be rejected as accidental context drift. Undeclared role or time changes remain incompatible.

Generic follow-ups inherit the actual answer's topic. Closing a romantic context also closes a mood-afterward question about that context, even though the question's catalog family is emotion. Conversely, closing the friend-company topic must not disable an open reason probe about an unrelated promise. Source scope, not the generic question's catalog location, controls this decision.

These changes organize the already-intended conversation. They add no compulsory questions, fixed interview length, model calls or new participant-data collection.

## Verification and its limits

The final focused run passed **22 test methods**. It checks graph consistency, all-entry pause and already-answered behavior, explicit antecedents, alternative context sources, superseded and nonparticipant sources, comparison records, inherited privacy scopes and four deliberately damaged graph variants. These are tests of explicitly annotated records, not a natural-language classifier. False semantic annotations can still produce false admissions.

The offline presentation passed **9 checks**, including searchable question access, unique element IDs, no page errors, no network requests and no mobile page overflow. Desktop and mobile screenshots were inspected. The browser disallowed file-URL navigation, so the check loaded the exact generated HTML using `set_content`; it did not disable the restriction. On narrow screens, diagrams scroll inside their containers and equivalent readable text remains available.

The final test run took 0.038 seconds. The canonical observer recorded 0.37 seconds across two focused runs during its 1,131.81-second observation window, with no forced redundant-green reruns. These timings are execution evidence, not measures of semantic quality.

## Sources and preservation

The input is the frozen readiness design at `55b894227022df3aee8ffd96a95e10f2a02ffe6c`. Its source manifest and the reproduced candidate's exact bytes were checked. The question-evaluation method reuses the project's existing cognitive-interviewing research; the graph adapts the current living-Mermaid-map guidance rather than introducing a new psychometric framework.

Primary method references previously checked for this design: CDC/NCHS Cognitive Interviewing, https://www.cdc.gov/nchs/ccqder/question-evaluation/cognitive-interviewing.html ; GOV.UK Question pages, https://design-system.service.gov.uk/patterns/question-pages/ ; Mermaid flowchart syntax, https://mermaid.js.org/syntax/flowchart.html . These sources support question evaluation and representation practices, not the validity of this particular survey.

The latest owner request was saved privately as design feedback and its export was verified. The private archive contains five events and zero actual pilot answers. Personal content and content-derived hashes are not in this public packet. Per-turn answer preservation remains required when the owner resumes; neither background monitoring nor automatic Railway synchronization is claimed.

## Current boundary

The design has converged at this review boundary. No further general rewriting pass is indicated by an identified defect. Actual use may reveal something not covered by these examples, but no known basic design problem is being handed to the owner to diagnose.

The pilot stays paused until the owner resumes it. Application implementation, inference-VM contact or wake, deployment, recruitment, chart scoring and claims of scientific validity remain outside this completed step.
