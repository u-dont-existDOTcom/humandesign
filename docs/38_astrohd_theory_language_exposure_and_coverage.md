# AstroHD theory-language exposure and questionnaire coverage

Status: draft evaluation design; no participant-runtime or scoring change authorized.

## Decision boundary

The user proposed noticing when a participant's questionnaire language is unusually
close to astrology or Human Design terminology, allowing the person to continue, and
retaining an internal signal that prior theory-language exposure may be present.

Verified ChatGPT Extra High returned `REVISE`. The admissible construct is a
**chart-blind theory-language exposure signal**, not a participant-contamination label.
It means only that the collected transcript contains wording consistent with prior
exposure to astrology or Human Design terminology. It does not establish that the
participant altered an answer, knew a target result, endorsed the theory, intentionally
matched a description, or caused bias in an estimate.

The classifier may use only:

- participant text;
- the exact preceding interviewer/question text and turn order;
- who introduced a term first;
- the declared language and language-assessability state; and
- a versioned, frozen language codebook.

It must not receive birth data, chart features, hidden classes, predictions, scores,
results, confidence, hits, or misses. It must not use social profiles, browsing history,
community membership, purchases, or any source outside the collected transcript.

## Operational attributes

Each lexical observation preserves separate attributes rather than collapsing them
into a psychological conclusion:

- specificity: `theory_specific`, `context_dependent`, or
  `ordinary_language_exclusion`;
- source: `participant_spontaneous`, `interviewer_introduced_or_echoed`, or
  `participant_quoted_or_reported`;
- participant stance: affirmative, neutral quotation, explicit rejection, previous
  exposure mention, or unresolved; and
- language assessability: fully, partially, or not adequately assessable.

Exact theory-specific wording used spontaneously is an exposure signal. A term repeated
only after the interviewer introduces it is prompt echo and cannot elevate the prior-
exposure signal. Quotation or explicit rejection can show that a term was encountered,
but cannot be treated as endorsement. Common words such as *authority*, *profile*, or
*energy* are context-dependent and never sufficient on their own. Generic semantic
resemblance is deliberately left unresolved rather than guessed. An unsupported
language is `not_adequately_assessable`, never automatically clean.

The v0.1 English codebook is a draft instrument, not a validated classifier. The
design intentionally tolerates false negatives rather than attaching a false-positive
label to a participant.

## Consequences and analysis lanes

For the present owner pilot, every signal is diagnostic or stratification metadata
only. Eligibility, interview stopping, prompt flow, scoring, exclusion, and the primary
analysis remain unchanged. The participant continues the experiment.

A future version may preregister a secondary sensitivity analysis stratified by this
signal, but that is not currently authorized. An optional direct self-report about
prior astrology/HD exposure could be asked only after the questionnaire to avoid
priming; adding it is also not currently authorized. Neither possibility may be
silently promoted into the current primary analysis.

## Synthetic dry run

The implementation includes synthetic cases for spontaneous jargon, ordinary wording,
ambiguous common words, interviewer echo, generic paraphrase, quotation/rejection,
multilingual code-switching, unsupported language, and identical transcript text under
two nominally different hidden-chart cases. The callable classifier has no chart or
prediction parameter, and identical transcripts produce identical assessments.

Artifacts:

- `reference/research/astrohd_theory_language_codebook_v0_1.json`
- `reference/research/astrohd_theory_language_exposure_fixtures_v0_1.json`
- `reference/research/astrohd_theory_language_exposure_dry_run_v0_1.json`
- `scripts/audit_astrohd_theory_language_exposure.py`

## Existing questionnaire coverage

Extra High accepted an investigation of whether future scoring validation needs more
questions, but rejected any predetermined expansion count. There is no scientific
basis for “70 more,” and no numeric question target is authorized.

The current source audit finds:

| Artifact fact | Count |
| --- | ---: |
| Question-bank records | 81 |
| Non-validation records | 76 |
| Validation records | 5 |
| Mapping rules | 82 |
| Frozen mapping rules | 27 |
| Unique frozen-mapped questions | 23 |
| Empirical-only questions | 6 |
| Unresolved questions | 52 |

The 76 and 23 values are descriptive facts, not a completion policy, respondent
requirement, or choice between denominators. The bank already contains 58 question
records outside the frozen-mapped subset. Those records have different phases and
purposes and cannot be presumed useful, but they must be audited before writing more.

The frozen rules contain 22 direct and 5 strong mappings. Repeated probes and multiple
rules in one dependency cluster are multiple indicators of a construct, not independent
confirmations. The generated audit exposes these dependencies and keeps validation
questions separate. Its prompt-language scan found four context-dependent codebook
occurrences and no theory-specific occurrence; that scan is a lexical leakage check,
not a measure of participant exposure.

## Future-item evaluation rule

A candidate item must be justified by a prospectively stated construct or rule gap and
evaluated for direct versus indirect evidence, incremental and discriminative value,
reliability, response process, redundancy, respondent burden, theory-language leakage,
demand characteristics, and multilingual handling. Accepted wording, mapping, scoring,
and analysis lane must be frozen before participant answers are inspected. Findings
after that freeze can inform only a later version.

The endpoint is the smallest questionnaire that adequately represents the prospectively
defined construct space with sufficient independent evidence and acceptable response
quality. The number of questions is a consequence of that audit, never an input.

Coverage artifacts:

- `reference/research/astrohd_current_questionnaire_coverage_audit_v1.json`
- `reference/research/astrohd_future_item_evaluation_template_v1.json`
- `scripts/audit_astrohd_questionnaire_coverage.py`

## Non-goals in this draft

- no participant-contamination label;
- no questionnaire denominator or additional-item quota;
- no current item, mapping, threshold, exclusion, scoring, prompt-flow, or lock change;
- no automatic theory-language paraphrase model;
- no optional exposure self-report; and
- no inference from chart fit, prediction agreement, or observed hit/miss outcomes.
