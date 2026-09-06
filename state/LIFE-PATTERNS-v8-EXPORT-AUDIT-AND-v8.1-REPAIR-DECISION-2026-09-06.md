# Life Patterns v8 export audit and bounded v8.1 repair decision

Audit date: 2026-09-06. This is the audit date, not an inferred interview date.
Status: development-only procedural audit. No codebook content, model mapping, research result, or runtime deployment is changed.

## Recommendation

Retain the completed pattern-first interview and its original transfer record. Do not restart the ten domains or request another complete autobiography. Apply a source-first, at-most-four-question repair pass for material unresolved issues, then export automatically. Four is a participant-burden limit for this repair, not a reliability threshold or sample-size claim.

The participant reported that v8 was better but lengthy, that some questions felt obvious, and that recorded uncertainties were not always followed up. This is evidence about this interview experience, not proof that all respondents would answer the same way or that the instrument has low discrimination in a population.

The generic repair packet is:

`state/LIFE-PATTERNS-v8.1-TARGETED-REPAIR-AND-QUESTIONING-ADDENDUM-2026-09-06.txt`

The original v8 prompt and original transfer are not overwritten. The new packet contains no participant autobiographical narrative or target-model information. It should be used in the original interview conversation where sources may still be accessible.

## Inspected sources and scope

- PR #24 freshly read at head `2eceb8714b28e274074e982f06fad5bf8da2e730`, open/draft/unmerged.
- Exact v8 interview prompt read at that commit: `state/LIFE-PATTERNS-PATTERN-FIRST-LONGITUDINAL-INTERVIEW-PROMPT-v8-2026-09-05.txt`; blob `d1dc5dab0a98af1d141cf6a142acfafa90ef25c1`.
- Participant-supplied JSON transfer, inspected locally without publishing its narrative.
- Participant-supplied excerpt and feedback in this conversation, not a full original interview transcript.

A fresh review of production behavior, Railway, model performance, and the entire repository was not needed for this bounded prompt/export audit and was not performed. The PR description is not proof of current deployed behavior.

## Structural checks actually performed

The supplied file parsed as JSON. It contains 10 attempted domains, 14 pattern claims, 12 series reports, 16 episodes, and 55 indexed participant-turn descriptions. Pattern, series, and episode IDs are unique. Referenced pattern/series/episode IDs and references into the participant-turn index resolve. These checks establish internal referential structure only, not provenance fidelity, completeness, historical truth, or coding reliability.

The exported support labels are 7 anchored_series, 3 multiple_episodes, 2 one_episode_only, and 2 self_report_only.

Three records fail necessary structural conditions of their own frozen v8 labels:

| Record | Stored label | Linked support | Audit finding |
|---|---|---|---|
| PAT-001 | anchored_series | 0 episodes; 2 series | The v8 definition requires a detailed episode plus an additional comparable occurrence. |
| PAT-007 | anchored_series | 0 episodes; 1 series | Repeated-series evidence remains useful, but the stored episode-anchored label is unsupported by the links. |
| PAT-010 | multiple_episodes | 1 episode; 1 series | The v8 definition requires at least two distinct supporting episodes. |

Do not silently relabel the participant's account or demand extra stories to rescue these labels. Preserve the original labels and attach a technical audit. The numerical conditions are necessary, not sufficient: matching counts do not prove detail, comparability, independence, or the asserted developmental history.

## Material findings

### 1. Question routing used effort inefficiently

The shown exchange revisited a context question and then requested increasingly specific anchoring. The follow-up seeking an instance of retrospectively unwanted action also narrowed the broader reported pattern. Such a prompt may elicit a negative-outcome subset rather than clarify the full original claim.

The v8 instructions permit a multi-step loop of pattern, context, history, anchor, recurrence, and exception for every domain. Two factual follow-ups per episode do not cap the total domain burden. Generic context checks and compulsory examples can consume that burden while real semantic gaps remain.

Repair: retain pattern-first interviewing; ask only when the answer could change the account, scope, temporal placement, or evidence interpretation. Do not ask whether context matters abstractly. Reuse already supplied details. Do not optimize for unusual or apparently distinctive answers.

### 2. Uncertainty is recorded, but its disposition is not

A text uncertainty field does not say whether a question was asked, already answered, forgotten, unanswerable, declined, deferred, or unnecessary. The supplied partial transcript cannot establish that every uncertainty was never asked about.

PAT-014 explicitly lacks an anchor for one branch of a conditional statement. PAT-002 lacks a concrete anchor. PAT-011 lacks timing for a reported change. PAT-009 qualifies continuity across life periods. These are candidates for checking the original source first, not automatic demands for four additional stories.

Repair: keep a short issue ledger and record why each remaining gap persists. Prioritize meaning and conditional-branch gaps before adding episodes. Preserve honest uncertainty rather than pressing for false precision.

### 3. Exceptions require proposition-level checks

Two differently described responses need not be incompatible. An action, internal experience, outcome, and different life period must not be treated as mutually exclusive simply because their words differ.

The supplied record already contains one participant correction of an apparent exception. PAT-004 and PAT-008 also warrant rechecking their exception links against the precise scoped claims. These are review flags, not adjudicated recodings. No new participant response is necessary when the original source already resolves the logic.

### 4. Provenance is incomplete, despite internally valid IDs

The source index contains summaries of participant messages, not their complete exact text. There is no full sequence of interviewer questions and follow-ups, exact displayed review batches, or exact approval responses. Some episode excerpts are present, but those excerpts cannot verify every adjacent claim. The actual source conversation remains necessary for stronger verification.

The pattern field named participant_claim_text is generally a paraphrase; v8 allowed a close factual paraphrase, so the name must not be taken as proof of a quotation. All 16 episode objects lack explicit per-episode review-status/history/correction fields. This does not prove episodes were unreviewed: v8 allowed selective episode review and underspecified export provenance.

Repair: recover accessible source text and review context; otherwise mark it unavailable. Never reconstruct a verbatim transcript from the summary index. Keep quotation, paraphrase, inference, correction, and participant approval separate. A finding of source incompleteness must not be inflated into a claim that the underlying events are false.

### 5. Developmental claims need support by life period

Several claims combine current behavior, childhood recurrence, and change over time. Multiple adult episodes do not establish childhood recurrence. Broad age descriptions and unanchored relative dates cannot support arbitrarily precise age-indexed comparisons.

Repair: retain all useful age information and its uncertainty. Ask for a range or life period only when it materially changes a stated change claim. Do not calculate ages from external birth details or interpret an early observation as a pure baseline. Preserve patterns that have only self-report support without pretending that support is absent or independently corroborated.

### 6. Completion states are conflated

The transcript excerpt shows an avoidable stop before export. The file's complete_after_pattern_review status does not establish complete evidence, complete source verification, or resolved uncertainties.

Repair: distinguish conversation completion, participant review, evidence limitations, and export completion. Export automatically after the final necessary review response. Partial or unresolved records are permitted; they must not be described as fully verified.

## Bounded existing-work scan and reuse decision

This is an adaptation of established questionnaire pretesting and source-provenance practices, not an invention of a new measurement theory.

- CDC/NCHS cognitive interviewing examines comprehension, recall, judgment, and response processes. Its purpose is diagnosing question problems, not estimating population characteristics from a convenience pilot. Reuse selective cognitive probes and explicit respondent-feedback analysis.
  https://www.cdc.gov/nchs/ccqder/question-evaluation/cognitive-interviewing.html
- U.S. Census Appendix A2 covers cognitive interviews, behavior coding, respondent debriefing, and subset testing. Reuse interaction-level auditing to identify repeated questions, interpretation problems, and unnecessary burden. Full interviewer context is needed for that audit.
  https://www.census.gov/about/policies/quality/standards/appendixa2.html
- U.S. Census Standard A2 calls for understandable, answerable questions, manageable burden, logical skip sequences, and clear wording. These support fixing routing rather than demanding more participant detail.
  https://www.census.gov/about/policies/quality/standards/standarda2.html
- Mokkink et al., 2025, COSMIN perspective, DOI 10.1016/j.jclinepi.2025.111879, distinguishes relevance, comprehensiveness, and comprehensibility. Adapt that distinction; this project is not claiming COSMIN validation or treating a health-outcome framework as a ready-made behavioral codebook.
  https://pubmed.ncbi.nlm.nih.gov/40562250/

Already addressed by existing work: diagnosing confusing/redundant questions, testing burden and skip logic, recording response processes. Partially addressed: semantic prioritization of follow-ups in an LLM conversation. Not established: this prompt's participant burden, population discrimination, coding accuracy, or sensitivity to real longitudinal change. Not appropriate here: claiming calibrated adaptive-test information gain without a calibrated item bank or using target-model fit to choose interview questions.

Decision: adapt/reuse these methods and the project's existing immutable-original/supplement separation. Keep the ten domains and frozen codebook unchanged. Do not add a bespoke relevance score, infer general response prevalence, or begin confirmatory model scoring.

## Acceptance checks for the repair packet

These are specified behavioral checks, NOT claimed results of live model testing:

1. Already answered fact -> source reference, not another question.
2. Two compatible responses -> no automatic counterexample assignment.
3. Repeated-series report without a dated incident -> preserve as reported recurrence; do not fabricate a concrete episode.
4. Stored evidence-label mismatch -> transparent audit, not participant re-interview to inflate support.
5. Unsupported conditional branch -> neutral optional clarification, not assumed confirmation.
6. Unknown age -> range/unknown, never guessed precision.
7. Participant cannot recall -> stop that probe and record disposition.
8. Four clarification attempts used -> no replacement questions to chase completeness.
9. Final review response -> export in the same assistant turn.
10. Missing exact transcript -> unavailable flag, never reconstructed quotations.

## Privacy and delivery boundary

The participant's raw transfer file, names, third-party allegations, intimate details, and autobiographical excerpts are not included in this repository audit or the generic prompt. The original remains in the participant-provided attachment and is not authorized for public GitHub publication. No coder was contacted. No merge, deployment, paid model run, measurement coding, or target-model evaluation was performed. The v8.1 addendum changes prompt instructions only; it is not an implemented runtime importer or proven interview improvement.
