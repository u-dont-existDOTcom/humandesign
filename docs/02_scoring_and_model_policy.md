# 02 — Scoring and Model Policy

## Canonical symbolic model

For new development runs, the canonical symbolic decoder is V4.3/V3.5.

Normative files:

- `reference/core/v4_3_scoring_algorithm.md`
- `reference/core/behavioral_target_combined_v3_5.md`
- `reference/core/human_design_search_instructions_fixed_candidate_blind(6).md` for original detailed mechanics not superseded by V4.3
- `docs/13_v4_3_migration_and_century_cache.md`

Legacy V4.1/V3.2 files are historical inputs only. Existing code/tests that implement them do not override the newer model.

## Symbolic tier

Use duration-weighted conditional prevalence and capped rubric bits:

```text
raw_bits_j = -log2(prevalence_j)
info_bits_j = min(6, raw_bits_j)
```

For the primary anchor of observation i:

```text
primary_support_i = salience_i * directness_i

evidence_primary_i =
    effective_confidence_i
    * primary_support_i
    * flexibility_factor_i
    * info_bits_primary_anchor
```

At most one structurally independent corroborator may contribute, capped at 15%:

```text
evidence_corr_i =
    0.15
    * effective_confidence_i
    * corr_support_i
    * corr_flexibility_factor_i
    * info_bits_corr_anchor
```

Alternative pathways compete; do not add them.

Contradictions remain:

```text
contradiction_bits_i =
    effective_confidence_i
    * contradiction_severity_i
    * 4
```

After dependency control:

```text
NetInformation =
    sum(evidence_rubric_bits)
    - sum(contradiction_rubric_bits)
```

Call these `rubric_bits`, never probability bits.

## Primary ranking

Rank exact stable intervals lexicographically by:

1. higher `NetInformation`;
2. fewer meaningful contradictions (`severity >= 0.50`);
3. higher `DetailedSupport`;
4. higher `CoreFit`;
5. longer exact stable duration.

Do not add CoreFit to NetInformation. Do not add an ad hoc coherence bonus. If all five are equal, the candidates are substantively tied.

## Effective confidence

Keep separate:

- behavioral confidence: how strongly the behavior is established;
- measurement reliability: how reliably the person can report that domain now.

```text
effective_confidence = behavioral_confidence * measurement_reliability
```

Reliability can only remove/downweight evidence. It cannot create support.

Unknown/depends/context-dependent answers may receive zero effective confidence when no stable direction is established.

## Dependencies

One underlying chart structure must not receive full information credit repeatedly because several questions paraphrase it.

Represent dependency clusters explicitly.

Alternative pathways compete; they are not summed as independent evidence.

A complete Channel and its component Gates are not independent evidence for the same observation. A Cross and its cardinal activations are not independent evidence. Corroborative reuse is capped as specified in V4.3.

## Interpretive flexibility

Every frozen mapping must declare a flexibility class before scoring:

```text
F1 = 1.00
F2 = 0.75
F3 = 0.50
F4 = 0.25 or unscored
```

This factor is mechanical. Do not assign custom decimals to improve a candidate.

## Required feature registry

Compile the union of all features referenced by frozen mappings.

V4.3 must be able to score at least the required M0-M2 fields used by the library, including when referenced:

- Type/Strategy;
- Authority;
- Centers;
- Profile;
- Definition;
- complete Channels;
- Gate + Line;
- Personality vs Design side;
- planetary carrier;
- Nodes;
- cardinal Sun/Earth activations;
- predeclared conjunction predicates.

If a frozen mapping references a feature absent from the candidate vector, raise a compliance error. Never interpret missing implementation support as `predicate_matches=False`.

## Duration-weighted conditional prevalence

Prevalence is estimated from the declared global UTC universe, never from a candidate file.

Use the frozen hierarchy from V4.3, for example:

```text
P(Type)
P(Authority | Type)
P(center signature | Type, Authority)
P(Profile | Type, Authority)
P(Channel | higher-level architecture)
P(cardinal activation | higher-level architecture)
P(Gate/Line | relevant higher-level architecture)
```

Use deterministic preregistered backoff when a conditional reference cell is too small.

## Post-selection refinement

Later clarification can be behaviorally valid while not being untouched confirmation.

Preserve:

- original observation;
- revised observation;
- revision class R1-R5;
- candidate-direction visibility;
- examples/counterexamples;
- selection risk;
- numeric confidence/weights and when they were frozen.

After an accepted target revision, rerun the complete declared candidate universe.

Always distinguish at minimum:

- frozen independent result;
- best-current descriptive/refinement result.

If numeric weights were selected after seeing the answer, that rerun is exploratory/descriptive rather than preregistered confirmation.

## Mapping compilation task

The current question bank is candidate-blind and does not by itself contain every server-side HD mapping key.

Codex must migrate the machine-readable mapping library to V4.3. For every mapping store at least:

- observation_id;
- dependency_cluster;
- question_ids;
- chart-feature predicate;
- predicted response rule;
- structural salience/class;
- mapping directness/class;
- flexibility class/factor;
- contradiction rule;
- prevalence parent/backoff metadata;
- source/rationale;
- status: `frozen | unresolved | empirical_only`.

If the repository does not contain enough information for a mapping, mark it `unresolved`. Do not invent one merely to improve recoverability.

## Anti-simplification requirement

A scorer may report `model_version=V4.3` only after the compliance gate passes.

The suite must fail if a mutation:

- removes the flexibility factor;
- drops Gate/Line/Channel/carrier support;
- treats missing required features as ordinary nonmatches;
- sums alternative pathways;
- disables dependency control;
- exceeds the corroboration cap;
- substitutes candidate-file prevalence;
- skips conditional prevalence;
- adds CoreFit to NetInformation;
- uses finalist-only rescoring after new evidence;
- silently falls back to a coarse astronomy model or invalid cache.

A reduced scorer must use a reduced model label and emit `v4_3_compliant=false`.

## Empirical tier

When human development data becomes available, fit:

```text
LLR_i(c) = log2(
    P(answer_i | chart_features_c)
    / P(answer_i | reference_universe)
)

EmpiricalScore(c) =
    sum effective_confidence_i * LLR_i(c)
```

Prefer regularized/hierarchical estimates, not raw rare-cell frequencies.

Human-learned mappings are versioned separately from theory-derived mappings.
