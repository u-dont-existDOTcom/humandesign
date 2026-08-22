# V4.3 Canonical Scoring Algorithm

## Status

This file is the implementation-facing scoring contract for the V4.3 Human Design reverse matcher. It is normative together with the frozen behavioral target. If code and this file disagree, the code is non-compliant until the discrepancy is adjudicated and versioned.

Human Design is an experimental symbolic framework here. `rubric_bits` are not probabilities.

## 1. Mandatory calculation tier

A V4.3 global matcher must calculate and retain the full M0-M2 candidate feature registry before scoring:

- Personality and Design activations separately;
- body/planet carrier;
- Gate and Line;
- Nodes under the frozen convention;
- cardinal Sun/Earth activations;
- Centers;
- complete Channels;
- Type and Strategy;
- Authority;
- Profile;
- Definition topology;
- hanging/dormant Gates and possible bridges where derivable;
- circuitry metadata when referenced by mappings;
- Cross derivation.

M3/M4 fields are mandatory whenever a frozen mapping references them. Missing required fields are errors, not neutral absence.

## 2. Compile-time model freeze

For every observation freeze:

```text
observation_id
behavioral_statement
behavioral_confidence
measurement_reliability
dependency_cluster
elicitation_stage
revision_class / selection_risk where applicable
```

For every allowed pathway freeze:

```text
primary structural anchor
structural salience S
mapping directness D
flexibility class + factor F
optional independent corroborator
contradiction rule + severity
prevalence parent hierarchy
source/rationale
status: frozen | unresolved | empirical_only
```

Compile `required_feature_registry` from all frozen predicates. V4.3 requires 100% runtime coverage.

## 3. Fixed factors

### Structural salience

```text
Type/Strategy architecture                  1.00
Authority architecture                      1.00
Diagnostic Center                           0.90
Profile / specific profile-line behavior    0.85
Complete Channel                            0.80
Cardinal Sun/Earth activation               0.75
Definition                                  0.65
Repeated Gate / thematic Node               0.55
Other prominent planetary activation        0.45
Ordinary hanging Gate                       0.35
Generic symbolism                           0.15
```

### Mapping directness

```text
Direct      1.00
Strong      0.75
Plausible   0.50
None        0.00
```

### Interpretive flexibility

```text
F1 narrow/constrained                 1.00
F2 moderately constrained             0.75
F3 broad archetype                    0.50
F4 very flexible/post-hoc             0.25 or unscored
```

Do not tune arbitrary decimals after seeing candidates.

## 4. Effective confidence

```text
Ceff_i = behavioral_confidence_i × measurement_reliability_i
```

Unknown/unreportable answers use `Ceff = 0`. Reliability can only downweight.

## 5. Core Architecture Fit

Frozen blocks:

```text
Type + Strategy       30
Authority             30
Diagnostic Centers    25
Profile                15
```

Use the V3/V4 exact block rules. Exclude genuinely unreportable blocks from the denominator before search.

```text
CoreFit = 100 × earned_core_points / available_core_points
```

CoreFit is reported separately and is never numerically added to NetInformation.

## 6. Detailed support

For pathway p:

```text
primary_support_p = S_primary × D_primary
corr_support_p    = S_corr × D_corr

pathway_support_p = min(
    1,
    primary_support_p + 0.15 × strongest_independent_corr_support_p
)
```

Alternative pathways compete:

```text
support_i = max(pathway_support_i1, pathway_support_i2, ...)
```

After dependency control:

```text
DetailedSupport = 100 × Σ(Ceff_i × support_i) / Σ(Ceff_i)
```

## 7. Duration-weighted conditional prevalence

Prevalence always comes from the declared global UTC universe, never the supplied candidate set.

Default frozen hierarchy:

```text
P(Type)
P(Authority | Type)
P(center signature | Type, Authority)
P(Profile | Type, Authority)
P(Channel | higher-level frozen architecture)
P(cardinal activation | higher-level frozen architecture)
P(Gate/Line activation | relevant higher-level architecture)
```

Back off through a predeclared hierarchy if the conditional reference cell is too small.

```text
raw_bits_j  = -log2(p_j)
info_bits_j = min(6, raw_bits_j)
```

## 8. Evidence rubric bits

Primary evidence:

```text
E_primary = Ceff_i
            × primary_support
            × flexibility_factor_primary
            × info_bits_primary_anchor
```

At most one structurally independent corroborator:

```text
E_corr = 0.15
         × Ceff_i
         × corr_support
         × flexibility_factor_corr
         × info_bits_corr_anchor
```

```text
E_pathway = E_primary + E_corr
```

Alternative pathways compete. Use the highest legitimate pathway evidence; do not sum alternatives.

## 9. Dependency control

Within one dependency cluster:

- keep only the strongest positive evidence pathway;
- cap contradiction to the strongest legitimate instance;
- do not double-count Channel + component Gates;
- do not double-count Cross + its cardinal activations;
- do not multiply repeated descriptions of the same mechanism;
- do not treat alternative mechanisms as independent evidence.

## 10. Contradictions

Only a predeclared direct opposing behavior is penalized:

```text
contradiction_bits_i = Ceff_i × contradiction_severity_i × 4
```

Missing support is neutral.

## 11. Net information

```text
NetInformation = Σ dependency-controlled evidence_rubric_bits
                 - Σ dependency-controlled contradiction_rubric_bits
```

## 12. Primary rank

Exact intervals are ranked lexicographically by:

```text
1. higher NetInformation
2. fewer meaningful contradictions (severity >= 0.50)
3. higher DetailedSupport
4. higher CoreFit
5. longer exact stable duration
```

If all five are equal, the states are substantively tied. UTC start may order display only.

Forbidden: `CoreFit + NetInformation`, `100 + rubric_bits`, coherence bonuses, finalist-only rescoring, or another scalar that changes this ordering.

## 13. Exact interval engine

Search exact scoring-relevant boundary intervals, including Design-side boundaries induced by the exact 88-degree solar-arc Design timestamp. Never claim minute precision from a coarse grid.

Production runs fail closed if the declared Swiss/JPL ephemeris files are absent or an unapproved fallback would be used.

## 14. Precomputed century store

Default project cache:

```text
1926-08-22T00:00:00Z <= t < 2026-08-23T00:00:00Z
```

Store exact interval feature vectors in Zstandard-compressed Parquet shards with a cryptographic manifest. Also cache duration-weighted prevalence tables keyed by universe hash and prevalence-policy version.

Normal search:

```text
verify cache → verify feature coverage → load prevalence → score every interval
→ merge score-identical adjacent states where permitted → rank → robustness/audit
```

Rebuild only when astronomy/feature policy changes or the cache horizon is extended.

## 15. Post-selection refinement

Behavioral validity and inferential independence remain separate.

For a new answer batch:

- preserve raw answer;
- unknown/depends can remain unscored;
- classify revisions R1-R5;
- record whether candidate direction was visible;
- freeze numeric weights before scoring if the rerun is intended as confirmatory;
- rerun the complete universe after any accepted revision;
- preserve both frozen-independent and best-current-descriptive results.

Weights chosen after answers are seen make that particular rerun exploratory/descriptive.

## 16. Required hardening tests

The test suite must deliberately mutate the implementation and prove failure when any of these occur:

- flexibility factor removed;
- Gate/Line/Channel/carrier mappings silently dropped;
- candidate vector lacks a required feature;
- M0-only scorer claims V4.3;
- alternative pathways summed;
- corroboration exceeds 15%;
- same Channel/Gates double-counted;
- candidate-file prevalence substituted for global prevalence;
- conditional prevalence silently skipped;
- CoreFit added to NetInformation;
- unknown answer forced to a side;
- only finalists rescored after new evidence;
- fixed-day Design timestamp used;
- coarse interval misses an interior boundary;
- ephemeris fallback occurs silently;
- cache manifest/hash mismatch is ignored;
- required feature coverage is below 100%.
