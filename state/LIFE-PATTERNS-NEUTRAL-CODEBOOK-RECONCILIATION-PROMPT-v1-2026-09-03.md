# Theory-blind reconciliation prompt — preserved v1

You are serving as an independent measurement-methods editor.

You will receive two independently developed theory-neutral behavioral codebooks for coding concrete first-person autobiographical episodes.

Your task is to reconcile them into one compact candidate codebook suitable for blind human pilot reliability testing.

You do not know what external hypotheses, theories, models, classifications, or predictions may eventually be compared with these behavioral measurements. Do not attempt to guess them and do not ask what they are.

## Inputs

Treat both supplied drafts as independent development evidence.

Neither draft is authoritative merely because it contains a construct.

Do not preserve a construct simply because both drafts contain something similar, and do not discard a construct simply because it appears in only one draft.

Make decisions only from measurement considerations such as:

- behavioral observability;
- clear prerequisites;
- distinguishability from neighboring codes;
- minimal hidden-cause inference;
- expected human coder reliability;
- preservation of counterexamples and context;
- missingness and abstention;
- coder burden;
- whether a distinction belongs at the episode level or should instead be derived across multiple coded episodes.

## Reconciliation principles

### 1. Prefer observable mechanisms over broad labels

Codes should describe what the narrator reports happening rather than assign personality traits, diagnoses, motives, virtues, deficits, or global characteristics.

### 2. Preserve genuinely different mechanisms

Do not merge two codes merely because they sometimes occur in the same episode or lead to the same outcome.

If they have meaningfully different prerequisites, actions, temporal positions, or evidentiary requirements, preserve the distinction.

### 3. Remove unnecessary duplication

If two constructs capture substantially the same behavioral evidence and their distinction would be difficult for trained coders to apply reliably, merge them.

Explain the merge.

### 4. Separate episode codes from derived summaries

Determine whether constructs concerning recurrence, stability across contexts, change over time, or other cross-episode properties should be:

- primary episode-level codes;
- derived summaries calculated from episode codes;
- or excluded.

Do not count the same evidence twice merely by coding both a behavior and a summary of that behavior as independent observations.

### 5. Avoid causal inference

Temporal sequence does not by itself establish that one event caused another.

Distinguish where necessary among:

- the narrator explicitly saying X affected Y;
- X occurring before Y;
- and a coder merely believing X probably affected Y.

### 6. Preserve abstention and missingness

A coder must be able to use:

- observed;
- contradicted;
- mixed;
- insufficient evidence;
- not applicable.

Non-action may be informative only when awareness, opportunity, and reasonable feasibility are supported.

### 7. Preserve sequence

When a person changes behavior during an episode, retain the sequence rather than reducing it to the final action.

### 8. Preserve context and counterevidence

Do not force a single global value when behavior differs across situations.

### 9. Do not optimize for external correspondence

Do not alter, retain, split, merge, or phrase a construct because it might correspond well to some unknown external theory or classification.

## Required output

Produce a complete reconciled candidate codebook.

For every final primary observable include:

1. stable neutral ID;
2. short behavioral name;
3. operational definition;
4. inclusion criteria;
5. exclusion criteria;
6. possible substantive values/subcodes;
7. minimum evidence requirements;
8. counterevidence;
9. relevant context modifiers;
10. 2–3 fictional boundary examples;
11. common coding mistakes.

Also define:

- the episode unit;
- non-action eligibility;
- evidence states;
- missingness;
- recurrence rules;
- person-level aggregation;
- sequence coding;
- context splitting;
- treatment of narrator global claims.

## Provenance requirement

For every final observable, include a non-substantive provenance field identifying which supplied draft constructs contributed to it.

For example:

`Source provenance: Draft A OBS012; Draft B NBM-E02`

This provenance is for auditability only. It must not affect whether the construct is retained.

## Reconciliation ledger

After the codebook, provide a table containing every substantive construct from both input drafts and classify it as:

- retained substantially intact;
- merged;
- narrowed;
- represented as a subcode;
- moved to context/modifier metadata;
- moved to a derived cross-episode summary;
- deferred for pilot testing;
- or excluded.

For every decision, give a short measurement-based reason.

No source construct may silently disappear.

## Unresolved decisions

Create a section listing distinctions for which you do not think conceptual reasoning alone is sufficient.

For each, specify what kind of blind pilot evidence should decide it.

Do not resolve uncertain distinctions merely to make the codebook look tidy.

## Pilot-readiness check

Finish by identifying:

- the highest-risk coder-confusion pairs;
- the most important episode-segmentation problems;
- which distinctions require special training examples;
- which constructs may be too rare for useful reliability estimates;
- and what should be measured separately in a first double-coding pilot.

Do not invent universal reliability thresholds.

## Version

Label the output:

`Neutral Behavioral Measurement Codebook — Theory-Blind Reconciled Candidate v1`

State explicitly that this exact reconciliation output must be preserved unchanged before any external hypothesis, target model, prediction, or model-fit result is revealed.

Produce the complete reconciliation in this response without asking clarifying questions.

---

The two preserved raw drafts were supplied after this prompt. This file intentionally does not duplicate those drafts; they are stored separately in `state/`.