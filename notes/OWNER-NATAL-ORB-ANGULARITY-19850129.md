# Owner natal orb tightness and angularity check — 1985-01-29 05:25 EST Philadelphia

Date checked: 2026-09-27

## Inputs and calculation provenance

Recorded moment already present in the repository:
- 1985-01-29 05:25 EST, Philadelphia, PA
- 1985-01-29 10:25 UTC

The existing direct project calculation in `experiments/astrohd/exact_actual_v1_1_user_v3_6.json` gives:
- Ascendant = 277.9489002776866° = 7°56'56" Capricorn
- Midheaven = 211.86852465210126° = 1°52'07" Scorpio

Independent astronomical longitudes were checked for 10:25 UTC. The angle calculation agrees with the repository's direct Swiss/Moshier output to within about 0.005°.

The project Western code uses the five major aspects (0/60/90/120/180) and a default 3° maximum orb.

## Tight major aspects under the project's 3° cutoff

Approximate geocentric tropical longitudes at 10:25 UTC yield:

| Pair | Aspect | Orb |
|---|---|---:|
| Mars–Saturn | trine | 0°12'27" |
| Venus–Mars | conjunction | 0°27'33" |
| Venus–Saturn | trine | 0°39'59" |
| Mercury–Venus | sextile | 0°49'45" |
| Jupiter–Saturn | sextile | 1°07'44" |
| Mercury–Mars | sextile | 1°17'18" |
| Mars–Jupiter | sextile | 1°20'10" |
| Mercury–Saturn | sextile | 1°29'44" |
| Neptune–Pluto | sextile | 1°45'11" |
| Venus–Jupiter | sextile | 1°47'43" |
| Mercury–Jupiter | conjunction | 2°37'28" |
| Sun–Moon | square | 2°39'32" |

This is a dense set of tight major aspects. Four are inside 1°; ten are inside 2°; all twelve survive the project's deliberately tight 3° cutoff.

The most concentrated structure is a five-planet network:
- Mercury conjunct Jupiter;
- Venus conjunct Mars;
- Mercury/Jupiter sextile Venus/Mars;
- Mercury/Jupiter sextile Saturn;
- Venus/Mars trine Saturn.

In modern aspect-pattern terminology this creates overlapping very tight minor-grand-trine / small-talent-triangle geometry, with conjunctions effectively thickening two vertices. Treat the name as descriptive only; the measured orbs are the important part.

## Angularity

Using the repository's exact Swiss/Moshier angles:

- Pluto ≈ 4°14' Scorpio vs MC 1°52' Scorpio -> Pluto conjunct MC, orb ≈ **2°22'**.
- Neptune ≈ 2°29' Capricorn vs ASC 7°57' Capricorn -> Neptune conjunct ASC, orb ≈ **5°28'**.
- Moon ≈ 12°08' Taurus vs IC 1°52' Taurus -> about 10°16' from IC; this is an angular-house placement but not a tight angle conjunction under a 5–8° proximity convention.

Thus Pluto is clearly tightly angular by common modern conventions; Neptune is moderately angular under 5–8° conventions. Pluto–MC is the strongest time/place-specific angle contact.

## Relationship to the V3.6 AstroHD reverse-match

This matters because the V3.6 merged Western mapping explicitly uses many of these exact features:
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

Therefore the chart's unusually dense tight-aspect structure and Pluto/Neptune angularity plausibly explain **why the frozen symbolic scoring model finds this date/time highly distinctive under its own rules**. They do not constitute independent validation, because those same features are part of the scoring model.

The repository correctly labels the V3.6 run **post-selection descriptive, not blind validation**. The mappings were frozen before the century scan, but the broader model-development process had prior access to owner information. A new held-out participant / preregistered time-twin analysis is required for independent evidence.

## Implication for the time-twin protocol

This owner chart is a useful motivating example for the preregistered orb-moderator test:
- primary theory-neutral question: birth time/place -> personality similarity;
- secondary moderator: are near-time pairs more similar when their shared chart contains unusually tight major aspects?
- secondary angularity moderator: does a tight planet-angle contact increase pair similarity?
- keep the project's fixed 3° major-aspect cutoff for one confirmatory specification and analyze exact orb continuously as the main tightness variable within the moderator layer.

Do not infer causal validity from this one chart or from the reverse-match rank.
