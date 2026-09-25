# AstroHD theory-language exposure signal specification

> **DRAFT — NON-AUTHORITY — RESEARCH DESIGN INPUT — NO RUNTIME EFFECT**

## Name and interpretation

The feature is a `theory-language exposure signal`.

Do not call a participant “contaminated.”

The signal means only:

> The transcript contains observable language evidence consistent with possible prior
> exposure to recognizable astrology/Human Design terminology.

It must never assert:

- that prior exposure changed the participant's answers;
- intentional chart matching;
- knowledge of the hidden target chart;
- invalidity of the response;
- causation; or
- model success or failure.

## Inputs permitted

The future detector may use only:

- participant response text;
- preceding questionnaire/interviewer text;
- speaker identity and transcript ordering;
- explicitly supplied response-language metadata; and
- a separately frozen/versioned theory-language codebook.

It must not receive:

- birth data;
- target chart;
- chart classifications;
- predicted traits;
- scoring results;
- rule matches;
- prediction fit;
- model confidence;
- hit/miss status; or
- downstream outcome information.

## Required evidence dimensions

Represent these independently rather than collapsing them into a single contamination
score.

1. Lexical specificity:

   - `theory_specific`
   - `context_dependent`
   - `ordinary_language_excluded`

2. Provenance:

   - `participant_spontaneous`
   - `participant_after_interviewer_same_term`
   - `quoted_or_reported_source`
   - `provenance_unknown`

3. Stance:

   - `affirmed`
   - `neutral_or_quoted`
   - `rejected`
   - `stance_unknown`

4. Language assessability:

   - `assessable`
   - `not_assessable`
   - `language_unknown`

Do not infer semantic stance automatically. The data model supports stance annotation;
runtime text defaults to `stance_unknown` unless stance is explicitly supplied by an
authorized annotation process.

## Exact matching policy for the draft implementation

No LLM similarity scoring, embeddings, target-chart matching, fuzzy semantic inference,
stemming-based expansion, or ontology inference is authorized.

Codebook matching, where tested, is limited to frozen codebook entries using:

- Unicode NFKC normalization;
- case folding;
- whitespace normalization; and
- phrase/token-boundary matching.

Ordinary-language exclusion entries never count as theory-specific exposure evidence.
A `context_dependent` occurrence remains context-dependent and is not promoted
automatically.

A participant occurrence of a codebook phrase after the interviewer has previously
used that same normalized codebook phrase is recorded as
`participant_after_interviewer_same_term`, not `participant_spontaneous`.

This field describes sequence/provenance only. It does not infer that the interviewer
caused the participant's answer.

## Paraphrases

No open-ended paraphrase detection is authorized.

The only paraphrases eligible for automated matching are expressions that a future
Pro/Extra-High review has explicitly added as frozen codebook entries before relevant
participant answers are analyzed.

Generic semantic resemblance to Human Design or astrology descriptions must not be
converted into exposure evidence.

## Multilingual handling

Do not perform automatic language inference for this feature. Use explicit language
metadata if already available.

A response is `assessable` only when a frozen codebook exists for the supplied
language. If there is no applicable frozen codebook, return `not_assessable`. If
language metadata is unavailable, return `language_unknown`.

Do not translate responses and classify the translation as though it were equivalent
evidence.

## Quoted or rejected terminology

Terminology may indicate exposure while simultaneously being quoted or rejected.
Lexical occurrence/exposure evidence and stance are therefore separate fields.

A rejection must not erase the occurrence. A quotation must not be silently converted
into participant endorsement.

## Privacy

The feature may use only authorized questionnaire/transcript material. It must not
search or ingest:

- social media;
- browsing history;
- communities followed;
- purchases;
- unrelated biographical records; or
- external participant dossiers.

## Current permitted effects

For the current owner pilot, this feature may affect none of:

- eligibility;
- stopping;
- questionnaire prompting;
- interviewer behavior;
- scoring;
- lock/reveal behavior;
- primary analysis; or
- participant exclusion.

It is diagnostic/stratification metadata only. No production wiring is authorized in
this task.

A future prospectively specified sensitivity analysis is scientifically possible but
is not currently authorized for implementation.

## Circularity invariant

The signal must be target-chart-blind and prediction-blind.

Holding a transcript and codebook constant while changing any hidden target-chart or
scoring information must be incapable of changing the exposure result.

## UNRESOLVED — REQUIRES REASONING/OWNER AUTHORITY BEFORE IMPLEMENTATION

- whether a future protocol should collect an explicit post-questionnaire prior-exposure self-report
- whether any future validation protocol should prespecify exposure-stratified sensitivity analyses
- whether future construct-coverage review ultimately justifies adding, removing, or changing questionnaire prompts
