# Adaptive survey v2 capacity audit method

## Purpose

Measure whether a source-grounded, candidate-blind adaptive question bank has enough deterministic **predicted-claim partition capacity** to distinguish the verified 288,938 structural century intervals more finely than the clean V3.6 holistic profile.

This is not an empirical validation of Human Design. Official and historical Human Design sources are used only to preregister what the system claims before new participant evidence is observed. Actual chart-to-behavior information must be estimated later on independent blind participants.

## Frozen candidate bank

The bank is generated deterministically from three frozen catalogs:

- `mapping_v2_planet_roles.json`: Sun, Earth, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto role templates on Personality and Design sides;
- `mapping_v2_gate_catalog.json`: 64 paraphrased gate themes;
- `mapping_v2_channel_catalog.json`: 36 paraphrased channel themes.

This yields 1,408 planet/side/gate candidate items plus 36 channel items = **1,444 predeclared candidate items**. The interview is not intended to ask all 1,444. It selects among them adaptively.

The North and South Nodes are intentionally excluded from the primary natal trait bank. The official HD source describes the Nodes as environment/perspective and explicitly distinguishes the South Node from a personality trait. Nodal hypotheses belong in the existing separate environment/perspective research layer and may not improve the primary natal behavioral ranking.

Every participant-facing item uses an opaque `Q2-...` identifier and omits Human Design vocabulary, gate/channel numbers, planet names, chart side, and the predicted direction before reveal.

## Elicitation rules

Questions target repeated behavioral patterns, especially continuity and change from childhood into adulthood. They retain explicit context, exception, counterexample, `Other / context-dependent`, and `Unsure` routes.

Design-side claims are assigned lower introspective reliability than Personality-side claims and request repeated observable behavior or independent observations from close others.

A state that does not carry a queried gate/channel is **neutral**, not predicted to show the opposite trait. This prevents the capacity calculation from manufacturing binary personality predictions that the source system did not actually make.

## Adaptive selection

Among currently plausible candidate states, the next frozen item is selected by reliability-adjusted binary carrier/non-carrier split entropy. Selection can choose among preregistered items but cannot invent new wording, constructs, mappings, scoring directions, or predicates after seeing a participant answer.

Redundant items may still be useful for reliability checks, but they are not counted as independent information merely because they are separate questions.

## Century audit

The audit conditions first on the clean V3.6 participant-observable fingerprint, then measures the added deterministic partitioning from these source-grounded families:

1. Moon gate positions, Personality + Design;
2. complete channels;
3. Mercury gate positions, Personality + Design;
4. Venus gate positions, Personality + Design;
5. Sun/Earth gate positions, Personality + Design;
6. Mars gate positions, Personality + Design;
7. Jupiter gate positions, Personality + Design;
8. Saturn gate positions, Personality + Design;
9. Uranus gate positions, Personality + Design;
10. Neptune gate positions, Personality + Design;
11. Pluto gate positions, Personality + Design.

It reports each family's incremental entropy, a greedy family sequence, full-v2 fingerprint entropy, unique-fingerprint count, tie sizes, theoretical top-k ceilings, and the remaining gap to exact interval identity.

The full-v2 fingerprint is a model-space upper bound: clean V3.6 plus all preregistered selected planet-position claims plus channel structure. Reaching 18.140400 bits structurally would mean the frozen claim set can uniquely encode the cached intervals in the noiseless model. It would **not** mean human answers provide 18.140400 empirical bits.

## Leakage safeguard

The previously studied 1985 state and its candidate-exposed Moon/Mars refinements are not used to select universal v2 dimensions. Universal construction follows source provenance and global century-wide residual capacity, not whether a feature happens to isolate the known reference.

Outer-planet roles were added because an official HD source explicitly specifies their general planetary functions and the century-wide residual audit showed that their gate activations remained structurally available. They were not selected because of the known 1985 reference.

## Promotion criteria

Before this bank can be called scientifically predictive, it still requires a frozen participant-scoring model and blind holdout data. Promotion should depend on preregistered top-1/top-k recovery, calibration, robustness to response noise/context, and comparison with appropriate null/baseline models—not on the structural capacity audit alone.
