# Life Patterns Neutral Codebook v1 — Leakage and Codability Audit

Date: 2026-09-03

## Artifact audited

`state/LIFE-PATTERNS-NEUTRAL-CODEBOOK-INDEPENDENT-DRAFT-v1-2026-09-03.md`

The audited artifact is preserved unchanged. This audit must not be used to silently edit v1. Any later revision must be separately versioned and must be completed before target-model fit/results are inspected.

## Generation provenance

- The substantive codebook was generated in a separate fresh ChatGPT account/chat.
- The generating chat was instructed not to use or infer any external personality, spiritual, diagnostic, biological, birth-derived, or typological theory.
- Human Design, AstroHD, astrology, charts, birth data, candidate models, and the target hypothesis were not disclosed to the generating chat.
- Important residual contamination risk: the seed prompt itself was authored in the current theory-exposed project chat. That prompt named several generic behavioral domains, including initiation/inhibition, decision process, uncertainty, pressure, conflict, social interaction, fatigue, and strong emotion. Therefore the generator was theory-blind, but the domain-selection prompt was not authored by a demonstrably theory-blind source.
- A fresh account removes conversation-history contamination but does not establish absence of relevant concepts from model pretraining. Pretraining exposure is treated as a residual risk, not as automatic disqualification.

## Leakage verdict

**No obvious semantic Human Design or astrology leakage detected in the codebook itself.**

The codebook does not reproduce recognizable target-theory structure or terminology. In particular, it does not encode Human Design types, strategy, authority, centers, gates, channels, profile, definition, incarnation cross, sacral yes/no, a special rule to wait for invitation/recognition, informing-before-action, emotional-wave/clarity doctrine, splenic authority, signature/not-self themes, or analogous theory-specific structures. It also does not encode zodiac signs, planets, houses, aspects, elements, or modalities.

Several observables are naturally adjacent to domains that Human Design or many other personality theories discuss:

- OBS001 optional engagement response;
- OBS002 reported cue guiding the next action;
- OBS004 action under unresolved uncertainty;
- OBS010 action initiation trigger;
- OBS022 emotion-linked action shift;
- OBS028 initiating social contact or coordination.

Those overlaps are not, by themselves, evidence of leakage. The definitions are generic behavioral operations and the codebook also covers many broad domains with no special Human Design salience: information seeking, option generation, preparation, obstruction response, feedback use, recognized errors, completion, repeated behavior, help seeking, interpersonal commitments, fatigue/load effects, repair, and disagreement behavior.

**Interpretation:** the content is suitable as a theory-blind development candidate, but the seed-prompt provenance prevents treating this single generation as the strongest possible contamination firewall for confirmatory use.

## Strong measurement features

1. Episode-level evidence is primary; global trait labels are explicitly downgraded.
2. Awareness, feasibility, and opportunity are required before non-action is interpreted.
3. `observed`, `contradicted`, `mixed`, `insufficient evidence`, and `not applicable` remain distinct.
4. Counterexamples and context dependence are preserved instead of averaged away.
5. Recurrence claims require more than one occurrence.
6. Narrative explanations are not automatically promoted to hidden causal mechanisms.
7. The codebook rejects evaluative global constructs such as resilience, rationality, willpower, confidence, leadership, and risk tolerance in favor of behaviorally anchored operations.
8. Context modifiers are recorded descriptively rather than assumed causal.
9. It explicitly warns against moral, diagnostic, cultural, and outcome-based inference.
10. It anticipates coder disagreement, observation-window effects, episode segmentation, retrospective compression, and opportunity-denominator problems.

## Measurement issues to address before validation-candidate freeze

### 1. Causal language sometimes exceeds the evidence rule

Several observables correctly warn against causal inference but still allow chronology to establish a functional relation.

Examples include:

- OBS002: `direct linguistic or chronological link` can overstate that a cue was *used* to select an action merely because it preceded it.
- OBS010: `directly sequenced proximal trigger` can turn a preceding event into a trigger without an explicit narrator link.
- OBS020: `directly supported link` between prior experience and later behavior needs a narrower operational rule.
- OBS022: a directly described emotion-to-action sequence can still be temporal co-occurrence rather than a reported influence.
- OBS035: event-linked temporal shifts must distinguish an explicit narrator connection from a descriptive before/after association.

A later blind revision should distinguish **reported influence** from **temporal antecedence/association** rather than letting sequence alone imply mechanism.

### 2. OBS011 and OBS026 are substantially redundant

OBS011 (`Transition from stated intention to action`) and OBS026 (`Intention–action correspondence`) share almost the same required evidence and several substantive values. OBS011 emphasizes initiation timing while OBS026 covers broader correspondence, but current boundaries are likely to produce duplicated coding and correlated target variables.

A later blind revision should either:

- make OBS011 a timing subfield of OBS026;
- split timing from correspondence with non-overlapping value spaces; or
- retire one after pilot reliability evidence.

This change must not be selected based on target-model performance.

### 3. Cross-episode descriptors are mixed with primary episode observables

OBS019, OBS034, and OBS035 operate at a different measurement level from most of the codebook:

- OBS019 repetition under recurring conditions;
- OBS034 context-linked variability;
- OBS035 change in repeated behavior over time.

These may be better treated as deterministic or adjudicated **derived summaries over episode-level codes**, rather than independently coded primary observables. Otherwise the same episode evidence can enter the target representation twice: once as a primitive code and again as a manually coded pattern-of-codes.

OBS020, OBS024, and OBS025 also require cross-episode or within-episode comparison and should be explicitly marked as comparative observables if retained.

### 4. Some observables are internally multidimensional

Examples:

- OBS016 contains both feedback **source** and feedback **response**.
- OBS017 contains detection, acknowledgment, verification, disclosure, correction, mitigation, and prevention actions.
- OBS031 contains multiple sequential disagreement behaviors.

Multi-label sequence coding is legitimate, but the schema should explicitly specify cardinality, ordering, and whether these are fields/subcodes rather than mutually exclusive categorical values.

### 5. `other specified` requires governance

Allowing `other specified` for every observable is useful during development but can become an uncontrolled shadow ontology. Pilot work should track its frequency and require separately versioned codebook revision when recurring `other specified` categories emerge.

### 6. Coder burden is high

Thirty-five observables, multiple context modifiers, evidence requirements, multi-step values, and cross-episode descriptors may be too costly for one-pass coding. Staged coding is likely preferable, but the exact workflow should be chosen from blind pilot reliability/effort evidence rather than target-model fit.

## Current scientific status

The artifact is **development-candidate content, not yet a validation-candidate ontology**.

It should not yet unlock tournament scoring because:

1. seed-prompt domain selection came from a theory-exposed project chat;
2. no independent replication of the domain selection has been performed;
3. no human-human coding reliability evidence exists;
4. no pilot has established episode segmentation, opportunity-denominator, multi-label, or cross-episode comparison reliability;
5. no blinded revision/freeze has yet promoted a stable subset to `validation_candidate`.

## Recommended contamination-control path

1. Preserve this v1 exactly as generated. **Done.**
2. Independently replicate codebook/domain generation in another clean chat using a much shorter prompt that does not enumerate behavioral domains. Freeze that output before any target theory is mentioned.
3. Compare the independently generated frameworks while both remain target-theory blind. Reconcile only on generic criteria such as behavioral observability, nonredundancy, evidence requirements, coder burden, and expected reliability.
4. Pilot on development interviews without chart/model outputs available to authors/coders.
5. Use human double-coding to identify unreliable distinctions, excessive missingness, overlap, and `other specified` drift.
6. Make any codebook revisions based only on those blind development findings and preserve a change log.
7. Freeze a validation-candidate version before any target-model performance is examined.
8. Only then create model mappings/adapters and run the preregistered comparison.

## Bottom line

The independent v1 is substantially better than a theory-authored construct list and shows no obvious direct Human Design/astrology leakage. Its largest contamination weakness is **not the codebook prose itself**; it is that a theory-exposed project chat supplied a relatively detailed domain-seeding prompt. Treating v1 as a development artifact and obtaining a minimally seeded independent replication before validation resolves most of that avoidable risk without requiring the unrealistic assumption that either humans or pretrained language models have literally zero prior astrology exposure.
