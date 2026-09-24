# Transparent merged AstroHD V1.2 — prior-work scan — 2026-09-24

Status: **RESEARCH-BEFORE-REINVENTION COMPLETE FOR THE DIRECT DEVELOPMENT EXPERIMENT**.

Independent conception was frozen first in:
`ASTROHD-V12-TRANSPARENT-MERGED-INDEPENDENT-CONCEPTION-20260924.md`.

## Underlying problem

Build a transparent post-result development scorer that can reuse the frozen 19-domain behavioral translation while avoiding the lost/ambiguous Western predicate semantics of historical V1.1.

## Existing work map

### Already solved — reuse

**Astronomical positions and houses**

The repository already uses Swiss Ephemeris. Its official documentation exposes deterministic planetary positions and many house systems. The existing project helper `src/hdmatch/relationship/western.py` already computes tropical Placidus houses through Swiss Ephemeris.

Source:
- Swiss Ephemeris documentation: https://www.astro.com/swisseph/
- Swiss Ephemeris programming manual: https://www.astro.com/swisseph/swephprg.htm

**Major-aspect geometry**

Astrodienst documents the five standard major/Ptolemaic aspects: conjunction 0°, sextile 60°, square 90°, trine 120°, opposition 180°. The repository already implements exactly this set and a deterministic angular-separation classifier.

Source:
- https://www.astro.com/astrowiki/en/Aspect

**Project-native deterministic aspect baseline**

`src/hdmatch/relationship/western.py` freezes `DEFAULT_ASPECT_ORB = 3.0` degrees for its deterministic Western relationship features. This is not asserted to be the uniquely correct astrology orb. It is the strongest materially simpler project-native baseline because it already exists, is tested, and is independent of the owner's current recovery result.

Astrodienst explicitly notes that orb practice varies, and its own chart styles use different orb tables. That supports making the orb an explicit versioned rule rather than pretending there is one universal value.

Source:
- https://www.astro.com/astrology/in_aspect_e.htm

**House-system baseline**

The repository already uses Placidus. Swiss Ephemeris implements it, and Astrodienst describes it as the most widely used house system. Reusing it avoids adding an unnecessary house-system search dimension.

Source:
- https://www.astro.com/astrowiki/en/Placidus
- https://www.astro.com/swisseph/swisseph.htm

**Angular-house definition**

Astrodienst defines houses 1, 4, 7, and 10 as angular houses. V1.2 therefore interprets historical generic `*_angular` feature names as membership in one of those houses, not as an unstated orb around an axis.

Source:
- https://www.astro.com/astrowiki/en/Angular_House

### Partially solved — adapt

Historical V1.1 preserves:
- the 19 behavioral clusters;
- Western feature names and salience/directness weights;
- the per-side information-score form;
- the 6-bit single-feature information cap;
- merged algebra `max(HD,WA)+0.25*min(HD,WA)`.

But pair-feature aspect type/orb rules and some angle semantics were lost. They cannot be reconstructed uniquely.

### Genuinely unresolved remainder

1. Turn every surviving Western feature name into one explicit machine predicate.
2. Recompute feature prevalence under those new predicates on the declared universe.
3. Score the frozen current behavioral translation under the new registry.
4. Test the known owner failure before any broad new ranking claim.

## Disposition

**ADAPT + COMPOSE + EXPERIMENT**

- reuse Swiss Ephemeris;
- reuse existing project Placidus/major-aspect implementation;
- reuse the historical V1.1 cluster weights and scoring algebra where preserved;
- define a new explicit Western predicate registry;
- test it as V1.2 post-result development, not historical reconstruction.

## Strongest simpler baseline

Western-only V1.2 under the new registry.

Do **not** implement merged HD+Western scoring first. Historical V1.1 already showed Western-only exact rank #4 versus HD-only #18, and the current HD semantic path has failed repeatedly. The cheapest discriminating test is whether the newly transparent Western-only side improves the known owner failure.

If Western-only fails the direct development regression, stop before building the merged layer.

## Research debt

No claim is made that astrology is empirically validated personality science. This experiment tests whether a transparent deterministic astrology-derived feature family reproduces the project's owner-development benchmark. General predictive validity would require fresh/held-out participants.
