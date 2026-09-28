# Owner natal orb tightness and angularity check — 1985-01-29 05:25 EST Philadelphia

Date checked: 2026-09-27

## Inputs and calculation provenance

Recorded moment already present in the repository:
- 1985-01-29 05:25 EST, Philadelphia, PA
- 1985-01-29 10:25 UTC

The existing direct project calculation in `experiments/astrohd/exact_actual_v1_1_user_v3_6.json` gives:
- Ascendant = 277.9489002776866° = 7°56'56" Capricorn
- Midheaven = 211.86852465210126° = 1°52'07" Scorpio

The planetary figures below are a tropical geocentric ephemeris cross-check interpolated to 10:25 UTC from the Jan 29/30 daily positions. They are adequate for orb classification at the arcminute level; the repository's direct Swiss/Moshier calculation remains authoritative for production scoring.

Important correction to the first draft of this note: a generic astronomical query returned Moon/Pluto longitudes in an incompatible ecliptic reference and was not used in the final numbers below.

## Tight major aspects

Approximate major-aspect orbs at 10:25 UTC:

| Pair | Aspect | Orb |
|---|---|---:|
| Mars–Saturn | trine | 0°12'46" |
| Venus–Mars | conjunction | 0°27'21" |
| Venus–Saturn | trine | 0°40'08" |
| Mercury–Venus | sextile | 0°49'49" |
| Jupiter–Saturn | sextile | 1°07'46" |
| Mercury–Mars | sextile | 1°17'10" |
| Mars–Jupiter | sextile | 1°20'33" |
| Mercury–Saturn | sextile | 1°29'56" |
| Venus–Jupiter | sextile | 1°47'54" |
| Neptune–Pluto | sextile | 2°14'34" |
| Mercury–Jupiter | conjunction | 2°37'43" |
| Sun–Moon | square | ~3°09'43" |

This is a dense set of tight major aspects. Four are inside 1°; nine are inside 2°; eleven are inside 3°. The Sun–Moon square is just outside 3° but remains well within many ordinary natal orb conventions.

The most concentrated structure is a five-planet network:
- Mercury conjunct Jupiter;
- Venus conjunct Mars;
- Mercury/Jupiter sextile Venus/Mars;
- Mercury/Jupiter sextile Saturn;
- Venus/Mars trine Saturn.

In modern aspect-pattern terminology this creates overlapping very tight minor-grand-trine / small-talent-triangle geometry, with conjunctions effectively thickening two vertices. Treat the name as descriptive only; the measured orbs are the important part.

## Angularity

Using the repository's exact Swiss/Moshier angles and the tropical ephemeris cross-check:

- Pluto ≈ 4°43' Scorpio vs MC 1°52' Scorpio -> Pluto conjunct MC, orb ≈ **2°51'**.
- Neptune ≈ 2°29' Capricorn vs ASC 7°57' Capricorn -> Neptune conjunct ASC, orb ≈ **5°28'**.
- Moon ≈ 12°37' Taurus vs IC 1°52' Taurus -> about **10°45'** from IC; this is compatible with a fourth-house/angular-house emphasis but is not a tight angle conjunction under a 5–8° proximity convention.

Thus Pluto is the clearly tight angle contact. Neptune is moderately close to the Ascendant under common 5–8° modern angularity conventions.

## Relationship to the V3.6 AstroHD reverse-match

This matters because the V3.6 merged Western mapping explicitly uses many of these exact feature families:
- `mercury_saturn`
- `mercury_jupiter`
- `mercury_venus`
- `mercury_mars`
- `venus_mars`
- `mars_saturn`
- `sun_moon_hard`
- `pluto_mc`
- `neptune_angular`
- plus house/sign features tied to the exact angles.

At the recorded moment, the saved run reports Western rank #4 and merged AstroHD rank #2 against 876,601 hourly century candidates. The nearest hourly candidate, 10:42 UTC, ranked #1; minute refinement placed the local optimum at 10:36 UTC, 11 minutes after the recorded time.

Therefore the chart's dense tight-aspect structure and Pluto/Neptune angularity plausibly explain **why the frozen symbolic scoring model finds this date/time highly distinctive under its own rules**. They do not constitute independent validation, because those same feature families are part of the scoring model.

The repository correctly labels the V3.6 run **post-selection descriptive, not blind validation**. The mappings were frozen before the century scan, but the broader model-development process had prior access to owner information. A new held-out participant / preregistered time-twin analysis is required for independent evidence.

## Implication for the time-twin protocol

This owner chart is a useful motivating example for the preregistered orb-moderator test:
- primary theory-neutral question: birth time/place -> personality similarity;
- secondary moderator: are near-time pairs more similar when their shared chart contains unusually tight major aspects?
- secondary angularity moderator: does a tight planet-angle contact increase pair similarity?
- freeze an orb rule before outcomes are inspected and also analyze exact orb continuously.

Do not infer causal validity from this one chart or from the reverse-match rank.
