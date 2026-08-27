# 23 — AstroHD Relationship Overlay

Status: descriptive composition protocol; not an empirically validated compatibility model.

## Purpose

Define how to answer an AstroHD relationship question without silently inventing a new compatibility scalar or conflating natal reverse matching with relationship validation.

AstroHD relationship analysis is currently a **composition** of two established layers already represented in this repository:

1. deterministic Human Design partnership mechanics from `docs/18_relationship_analysis.md` and `src/hdmatch/relationship/analysis.py`;
2. Western synastry as inter-chart planetary aspects, using the frozen astronomical conventions already employed by the AstroHD and Castille synastry work.

This is adaptation/composition, not a claim that a validated joint AstroHD partnership model already exists.

## Existing-work scan and reuse decision

Before defining this overlay, reuse the strongest existing project work:

- Ra-style HD partnership surface: combined Centers, composite Definition, Electromagnetic/Dominance/Compromise/Companionship, shared Gates, and Sun/Earth-to-Node geometry;
- AstroHD natal layer: tropical geocentric planetary positions, major aspects, signs, angularity, and houses where location is resolved;
- Castille static-synastry design: inter-chart aspects are calculated mechanically and are not pre-labelled as globally beneficial or adverse for empirical fitting;
- conventional Western synastry practice: interpret inter-chart aspects only after understanding each natal chart, and distinguish attraction/intensity from durability or ease.

Decision: **compose/adapt**, do not invent a new weighted relationship score.

## Calculation hierarchy

### 1. Preserve both natal charts independently

For each partner preserve:

- HD Type, Authority, Profile, Definition, Gates, Channels, and Centers;
- tropical geocentric planetary longitudes;
- major natal aspects;
- Ascendant/MC/houses only when exact birthplace coordinates and civil-time resolution are available.

Do not use relationship fit to change either natal chart.

### 2. Run canonical HD partnership analysis unchanged

Calculate the full V1 relationship surface from `docs/18_relationship_analysis.md`.

This layer remains authoritative for statements specifically attributed to Human Design. AstroHD does not replace or reweight the HD mechanics.

### 3. Add Western synastry as a separate evidence layer

Calculate inter-chart aspects using the same major-aspect family used by the frozen Castille design:

- conjunction 0°;
- sextile 60°;
- square 90°;
- trine 120°;
- opposition 180°.

For a concise descriptive report, prioritize exact/tight aspects, normally <=3° orb, before considering wider conventional orbs. Preserve exact orb and direction/person ownership.

Do not convert the count of harmonious/challenging aspects into a compatibility percentage.

### 4. Add house overlays only where geometrically identified

A planet from Partner B can be placed in Partner A's houses whenever Partner A's exact natal houses are known; Partner B's birthplace is not required for that one-sided overlay because only B's planetary longitude and A's cusps are needed.

The reciprocal overlay requires Partner B's resolved birthplace coordinates and houses.

If only a country or broad region is supplied, do not guess an Ascendant, MC, houses, or reciprocal house overlay. Report the planetary/aspect layer as invariant and the angle/house layer as unresolved.

### 5. Compare convergence and tension across systems

The reader-facing synthesis should explicitly distinguish:

- **convergence** — HD and Western layers independently point toward a similar experiential hypothesis;
- **new information** — Western synastry adds a theme not present in the HD surface, or vice versa;
- **tension** — the two symbolic systems imply different phenomenology;
- **unresolved** — required birth-location/time data or validated mapping is absent.

Convergence is not scientific corroboration unless the layers have demonstrated independent out-of-sample predictive validity. Shared astronomical inputs can also create dependency.

## Interpretation guardrails

- Attraction, spark, intensity, split-bridging, outer-planet contacts, or Nodal contacts must not be translated into `soulmate`, `meant to be`, or guaranteed durability.
- Saturn contacts may be described conventionally as structure/stability/constraint themes, but not as proof of marriage longevity.
- Pluto/Neptune contacts may be described conventionally as intensity/transformation or idealization/permeability themes, but not as proof of trauma, obsession, deception, or spiritual destiny.
- Difficult aspects are not automatically negative and harmonious aspects are not automatically positive.
- Real-world maturity, consent, communication, power asymmetry, attachment history, and behavior outrank symbolic compatibility claims.
- Do not expose speculative private psychology of an absent third party as established fact.

## Current validation boundary

The repository's existing merged AstroHD model is a natal behavioral/reverse-matching model, not a frozen relationship-outcome model.

The Castille static-synastry work tests whether date-stable Western inter-chart aspects can distinguish real from matched synthetic partners. Until a successful untouched result and a separately frozen joint HD+Western pair model exist, AstroHD relationship readings remain **descriptive composition**, not a validated probability of compatibility or relationship quality.

## Future empirical model

A genuine AstroHD partnership model should be built only after separate HD and Western pair baselines are evaluated. Compare at minimum:

- R-HD: canonical HD relationship mechanics only;
- R-WA: Western synastry only;
- R-AstroHD: preregistered combination of both;
- R-C: non-symbolic demographic/context baseline where appropriate.

The joint layer is useful only if it improves untouched pair prediction over the strongest separate baseline without post-hoc weighting.