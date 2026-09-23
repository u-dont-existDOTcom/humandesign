# Historical V1.1 merged scorer reconstruction boundary — 2026-09-23

Status: **TECHNICALLY UNRESOLVED / NEW-PROFILE SCORING NOT ADMITTED**.

## Recovered exactly

The frozen historical model, target-side exact-score decomposition, hourly universe, Moshier-era ephemeris cache, and minute-refinement receipts remain available.

The recovered scoring algebra is strongly constrained and internally reproduces the stored per-cluster decomposition:

- each HD or Western side selects the strongest matched feature;
- feature evidence follows the historical V3 family: behavioral confidence × frozen salience/support × frozen directness/flexibility × capped rarity information;
- rarity information is capped at 6 rubric bits;
- HD contradiction penalties use the historical 4-bit cap family;
- the cross-system cluster merge is `max(HD, Western) + 0.25 × min(HD, Western)`, bounded by the stored `cap_multiplier=1.25`.

The stored exact cluster scores satisfy the 25% merge algebra exactly. Several HD and Western sign/house scores also algebraically match the recovered information-score form.

The historical coarse cache is intact at `data/ephemeris/astrohd_generic_v1`, uses explicit Moshier flags, and covers the 876,601 hourly-candidate procedure.
## Missing historical semantics

The one-off scanner implementation and a normative feature-predicate registry were not recovered from:

- Git history, reflogs, or dangling Git objects;
- the old August project checkout and untracked files;
- local Codex session stores from August 24–25;
- the August 24 GitHub Actions run/artifact history;
- prior-conversation retrieval;
- personal Library search for the V1.1 model/feature names.

A contemporaneous earlier Western scanner was recovered from the Library and documents a generic `has_aspect(..., max_orb=6.0)` helper. That is useful provenance but does not uniquely reconstruct V1.1: the V1.1 feature names do not preserve which aspect types or angle rules each pair used, and the frozen scores are inconsistent with treating every named pair as the same generic 6° all-major-aspect predicate.

For example, the exact birth has a tight Mercury–Saturn sextile. If `mercury_saturn` meant generic all-major ≤6°, it would outscore the stored Mercury-in-Capricorn explanation for `structure_discovery`, contradicting the frozen exact decomposition. Conversely, `meaningful_work_not_constant` has only `mars_saturn` on the Western side and therefore requires a Mars–Saturn predicate that *does* match the exact natal trine.

The frozen sole-feature Mars–Saturn score implies feature prevalence about `0.23547`; generic all-major ≤6° over the historical hourly cache gives about `0.26289`. The Venus–Mars exact score implies about `0.26520`; the same generic predicate gives about `0.28899`. Reasonable alternative aspect-orb tables can approach either value but are not uniquely identified.
## Minute-refinement clue and limitation

At the recorded `1985-01-29T10:25Z` moment, Pluto is about `2.86°` from the Midheaven. At the historical refined peak `10:36Z`, Pluto is essentially exactly conjunct the Midheaven; at the nearest hourly `10:42Z`, it is about `1.55°` away. This strongly suggests angle/orb-sensitive Western behavior in the lost implementation, but the exact `pluto_mc`, `neptune_angular`, and related predicate/rarity rules are not preserved normatively.

Because multiple plausible predicate definitions can reproduce selected historical details while changing the century-wide ranking, reverse-fitting one convenient implementation to the known owner result would not establish that it is the historical scanner.

## Gate decision

The predeclared calibration rule requires a reconstructed V1.1 scorer to reproduce the frozen historical benchmark **before** scoring the new translated profile. Exact reproduction cannot currently be established from the surviving implementation evidence.

Therefore:

- frozen V1.1 behavioral translation SHA-256 remains `4211b1ee3941b1dabf5aba3677386cda1a68837a11ebbaa6ac618040f9ac5aa2`;
- that private translation is **not scored** with an approximation;
- the V1.1 owner recoverability gate remains **TECHNICALLY UNRESOLVED**;
- no pass/fail is inferred for the new survey under V1.1 until the historical feature predicates are recovered or a reconstruction independently reproduces the frozen old score/rank/refinement signature.