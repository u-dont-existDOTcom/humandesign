# Astronomy reference + progression ablation v1

Status: experimental protocol. Coordinate and progression alternatives must be frozen before participant evidence is inspected.

## 1. What the astronomy objection actually means

The project must distinguish two questions that are often collapsed:

1. **Where was a body according to modern astronomy?**
2. **How should that physical state be projected into an astrological symbol system?**

The current production chart engine already uses locally pinned Swiss Ephemeris files rather than ancient hand tables. Its normal chart input is nevertheless a derived quantity: geocentric tropical ecliptic longitude of date. That is an astrological/coordinate convention layered on top of modern ephemeris calculation.

Precession therefore does not imply that the tropical calculation is an arithmetic mistake. Tropical signs are defined relative to the equinox. A sidereal zodiac uses a different stellar reference convention, with an explicit ayanamsa. IAU constellations are different again: they are irregular two-dimensional sky regions, not twelve equal 30-degree longitude bins.

The scientific question is not which convention is philosophically correct. It is whether any frozen projection of an accurate astronomical state adds out-of-sample predictive information about behavior.

## 2. Preserve source astronomy before projection

`hdmatch.chart.astronomy_reference` introduces a provenance-bearing astronomy state. The v1 record can preserve, per body:

- UTC observation instant and Julian day UT;
- provider/version and source-file identities;
- observer origin and declared native frame;
- ecliptic longitude, latitude, and distance;
- right ascension and declination;
- Cartesian position and velocity.

The richer Swiss adapter rejects a calculation when the returned flags do not contain `FLG_SWIEPH`. It is deliberately labelled **geocentric/ecliptic-of-date**, not ICRF or barycentric.

The existing one-minute 1926–2026 AstroHD cache remains useful for fast tropical candidate search. It is a derived cache, however, not the canonical astronomy archive, because it stores longitude rather than the richer state above.

## 3. Competing projection hypotheses

All alternatives must be named and frozen before evidence scoring.

| ID | Projection | Required source information | v1 status |
| --- | --- | --- | --- |
| A0 | Tropical, equinox-of-date, equal 30-degree signs | ecliptic longitude | implemented |
| A1 | Sidereal, named ayanamsa, equal 30-degree signs | longitude + frozen ayanamsa name/value | transform implemented |
| A2 | Actual IAU constellation | full sky position + versioned IAU boundaries | fail-closed until boundary dataset is checked in |
| A3 | AstroHD/Human Design gate mapping | validated project gate mapper | existing pipeline; explicit adapter still required |

A2 must never be approximated by subtracting an offset from longitude. Real constellation membership needs the official two-dimensional boundary geometry and therefore RA/Dec (or an equivalent transform into the boundary frame).

For A1, the ayanamsa name and numeric value used at the event instant are part of the frozen prediction provenance. We must not try several ayanamsas and keep the one that happens to rank the participant best.

## 4. Modern numerical reference audit

The project should not write its own N-body integrator. Mature modern ephemerides are a stronger reference.

For the participant interval, use a JPL DE440-family source as an independent numerical oracle where licensing/deployment permits. Differential testing should sample:

- random timestamps across the certified historical interval;
- every body used by AstroHD;
- sign, gate, line, and aspect boundaries more densely than ordinary timestamps;
- retrograde stations and fast lunar motion;
- angles/houses separately with exact location and Earth-rotation inputs.

For each sample, record the physical/angular discrepancy between the pinned Swiss computation and the independent JPL result. Then calculate whether that discrepancy can change a symbolic assignment. Tiny numerical differences far from a boundary are scientifically irrelevant; tiny differences at a boundary can change a categorical prediction and must be audited.

The Swiss files remain acceptable if the differential audit demonstrates agreement within a preregistered tolerance. Replacing a mature ephemeris simply because it is called “astrological” would not improve the experiment.

## 5. Angles and houses are a separate audit

Ascendant/MC depend on more than planetary ephemerides. They require a correctly resolved civil time, geographic coordinates, Earth rotation/sidereal time, and an explicit house/angle convention.

Therefore the outstanding Ascendant/MC discrepancy must be resolved before angles become confirmatory predictors. The audit should preserve:

`local civil tuple -> IANA timezone/fold -> UTC -> geographic lat/lon -> Earth-rotation convention -> angle calculation`

and compare at least two independent implementations at random locations/times and at the known disputed case.

## 6. Progressions are a longitudinal hypothesis, not a post-hoc repair

`hdmatch.chart.progressions` freezes the initial secondary-progression convention:

> one ephemeris day after birth = one tropical year of elapsed life.

For a real observation date, the mapping is deterministic and stored with the exact progressed ephemeris instant. A future participant prediction freeze can therefore create an age-indexed progression trajectory before the interview reveals the participant trajectory.

The interview should collect developmental history independently:

- early childhood;
- school years;
- adolescence;
- early adulthood;
- later adulthood/current period;
- onset, disappearance, recurrence, context, and counterexamples.

Avoid forcing fixed age bins if the participant reports a clearer natural transition. Preserve their reported ages/ranges so the temporal prediction can be scored with uncertainty rather than rewritten to match a progression exactly.

## 7. Progression ablation

Do not decide that progressions work because they explain one known biography. Compare frozen models across held-out participants:

| ID | Model |
| --- | --- |
| M0 | natal AstroHD only |
| M1 | natal + secondary progressions |
| M2 | natal + ordinary age/development/context controls, no progression |
| M3 | natal + progressions + ordinary development/context controls |

Primary questions:

1. Does M1 outperform M0 on held-out longitudinal behavior?
2. Does M3 outperform M2, showing incremental information beyond ordinary development?
3. Does the progression layer improve true-birth-state recovery without increasing false matches elsewhere?
4. Are transition predictions calibrated when the participant reports uncertain onset ages?

The progressed Moon should be evaluated separately from slow progressed bodies because it operates on a much shorter developmental timescale and can otherwise inflate degrees of freedom.

## 8. Person-level “astrology fit” is itself a testable variable

Do not assume equal fit across people. Predefine a participant-level predictability score from held-out dimensions, then ask whether high-fit participants can be identified **without using their evaluation answers**.

Possible preregistered moderators include:

- prediction uniqueness/discriminability in the candidate universe;
- stability of the match under small birth-time perturbations;
- proportion of frozen dimensions that have strong mapping support;
- consistency of observed behavior across life periods.

Do not define a “high-fit person” merely as somebody whose chart scored well and then use that same score as the explanation.

## 9. Freeze order for the scientific participant test

Before behavioral evidence is visible to the scorer, freeze:

1. resolved birth instant/location provenance;
2. astronomy provider/kernel/file hashes and coordinate frame;
3. projection hypothesis IDs and all parameters;
4. natal prediction set;
5. age-indexed progression predictions, if that arm is enabled;
6. scoring mappings and tolerances;
7. candidate universe and ranking rule.

Only then collect the longitudinal behavioral profile. Coordinate-system and progression comparisons are confirmatory only if their alternatives and selection rule were frozen at this stage.

## 10. External references

- JPL Solar System Dynamics, planetary ephemeris export: https://ssd.jpl.nasa.gov/planets/eph_export.html
- JPL Horizons: https://ssd.jpl.nasa.gov/horizons/
- International Astronomical Union, constellations: https://www.iau.org/public/themes/constellations/
- Swiss Ephemeris programming manual: https://www.astro.com/swisseph/swephprg.2.10.pdf
