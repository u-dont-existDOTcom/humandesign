# Partner Multidomain 1000 Null Benchmark V2 — Frozen Specification

Status: **development / exploratory**.

Freeze date: 2026-08-25.

This specification is frozen before the V2 1,000-partner results are generated.
It must not be edited to improve Joel-Bee rank after results are visible.

## Question

Does the Joel-Bee pair show unusually concordant future **life-state patterns**, rather than merely similar timing of astrological activation?

The V2 benchmark compares four independently generated Western-astrology domains plus one pair-specific Human Design corroboration domain:

1. relationship / attachment;
2. economic / resource mode;
3. home / community mode;
4. work / purpose mode;
5. HD pair integration / openness / material bridge.

Geographic concordance is **not numerically scored in V2** because Bee's exact birth time and exact Cameroon birthplace remain unresolved. No houses, angles, progressed angles, relocation charts, or astrocartography are used for any V2 null partner.

## Astronomy

Production astronomy: verified SWIEPH only, fail closed on Moshier fallback.

Pinned files:

- `sepl_18.se1` SHA-256 `ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66`
- `semo_18.se1` SHA-256 `1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7`

Tropical, geocentric longitude. True Node for HD natal mechanics.

## Horizon and sampling

Monthly snapshots:

`2026-01-15` through `2040-12-15`, at 12:00 UTC.

## Birth inputs

Joel:

`1985-01-29T10:25:00Z`

Bee is carried as three representative unknown-time states, with none selected from pair fit:

- early: `1989-06-19T05:00:00Z`
- mid: `1989-06-19T12:00:00Z`
- late: `1989-06-19T17:00:00Z`

These are representative states, not a substitute for final exact civil-day enumeration.

## Null pools

Seed: `202608252052`

N = 1000 per direction.

Joel comparison pool: 1,000 uniformly sampled UTC birth moments from
`1984-06-19T00:00:00Z <= t < 1994-06-19T00:00:00Z`.

Bee comparison pool: 1,000 uniformly sampled UTC birth moments from
`1980-01-29T00:00:00Z <= t < 1990-01-29T00:00:00Z`.

The terms `women` and `men` are descriptive labels for the intended comparison question only; biological sex is not an astronomical input.

## Western monthly domain state vectors

Every domain at every month is represented by four continuous components in `[0,1]`:

1. `support` — opportunity/ease/expansion;
2. `structure` — consolidation/commitment/stability;
3. `change` — liberation/dissolution/deep restructuring;
4. `stress` — hard-pressure/disruption.

The score is based on **temporal pattern concordance of these state vectors**, not on a claim that any component is an empirically validated life-outcome probability.

### Domain natal targets

`relationship`:
- Moon
- Venus
- Mars

`economy`:
- Venus
- Jupiter
- Saturn
- Sun

`home_community`:
- Moon
- Venus
- Jupiter
- Saturn

`work_purpose`:
- Sun
- Mercury
- Mars
- Jupiter
- Saturn

### Transit moving bodies

- Jupiter
- Saturn
- Uranus
- Neptune
- Pluto

### Secondary-progressed moving bodies

- progressed Sun
- progressed Moon
- progressed Mercury
- progressed Venus
- progressed Mars

Secondary progression convention: one ephemeris day per tropical year of life (`365.2422 d`).

### Orbs

Transit Gaussian-kernel sigma:

- Jupiter 2.5°
- Saturn 2.0°
- Uranus 1.5°
- Neptune 1.5°
- Pluto 1.5°

Progression Gaussian-kernel sigma:

- progressed Sun 1.0°
- progressed Moon 1.5°
- progressed Mercury 1.0°
- progressed Venus 1.0°
- progressed Mars 1.0°

Major aspects only:

`0°, 60°, 90°, 120°, 180°`.

### Component rules

For every moving-body / natal-target pair, calculate Gaussian proximity to the nearest declared aspect.

`support` receives:

- Jupiter at conjunction: 1.00
- Jupiter sextile/trine: 1.00
- Jupiter square/opposition: 0.25
- relevant progressed-body conjunction/sextile/trine: 0.75

`structure` receives:

- Saturn conjunction: 0.75
- Saturn sextile/trine: 1.00
- relevant progressed-body conjunction/sextile/trine: 0.50

`change` receives:

- Uranus conjunction: 1.00; sextile/trine 0.60; square/opposition 0.90
- Neptune conjunction: 0.90; sextile/trine 0.55; square/opposition 0.80
- Pluto conjunction: 1.00; sextile/trine 0.60; square/opposition 0.90
- relevant progressed-body conjunction: 0.75; square/opposition 0.60

`stress` receives:

- Saturn square/opposition: 1.00; conjunction 0.35
- Uranus square/opposition: 0.90
- Neptune square/opposition: 0.80
- Pluto square/opposition: 0.90
- relevant progressed-body square/opposition: 0.50

Within one monthly domain/component, take the **maximum** eligible activation rather than summing many correlated hits.

Transit component contributions are multiplied by `0.80`; progression contributions by `1.00`.

### Relevant progressed bodies by domain

`relationship`: pMoon, pVenus, pMars, pSun

`economy`: pVenus, pMars, pSun

`home_community`: pMoon, pVenus, pSun

`work_purpose`: pSun, pMercury, pMars

Progressed bodies not listed for a domain do not contribute to that domain.

## Domain similarity

For each domain, flatten the 180 monthly 4-component state vectors to one vector and compute cosine similarity between the two people.

Report each domain separately.

The Western multidomain score is the unweighted mean of the four domain similarities.

No domain weight may be changed after seeing results.

## Exploratory categorical interpretations

These labels are descriptive summaries only and do not affect ranking.

Per month:

`relationship_stable_candidate` if:
- support >= 0.40
- structure >= 0.30
- stress < 0.60

`economic_independence_candidate` if:
- change >= 0.50
- support >= 0.25
- stress < 0.75

This means a candidate month for major resource-system liberation with enough support to avoid reading pure disruption as independence. It does **not** mean literal zero currency use.

`home_community_settlement_candidate` if:
- support >= 0.40
- structure >= 0.25
- stress < 0.60

`work_purpose_reorientation_candidate` if:
- change >= 0.50

For each pair, report overlap fractions for these categorical states. They are diagnostic, not part of the primary Western score.

## Human Design pair domain

For each month, calculate natal gates for both people using exact 88-degree Design roots, then overlay slow transit gates from:

- Jupiter
- Saturn
- Uranus
- Neptune
- Pluto
- true Node

Produce three binary monthly components:

1. `single_definition` — connection chart has one definition component;
2. `eight_plus_one` — exactly eight defined Centers / one open Center;
3. `material_bridge_21_45` — Channel 21-45 is complete in the connection+transit state.

The HD pair score is:

`mean(single_definition, eight_plus_one, material_bridge_21_45)`

over all months/components.

This is a research rubric, not a compatibility probability.

## Joint V2 score

Within each null pool, convert these five metrics to z-scores:

- relationship similarity
- economy similarity
- home/community similarity
- work/purpose similarity
- HD pair score

Then:

`joint_v2 = mean(the five z-scores)`

Equal weights only.

For each real Bee time state, report Joel's rank and percentile against his 1,000 comparison partners.

For each Bee state as focal person, report Joel's rank and percentile against Bee's 1,000 comparison partners.

## Predeclared interpretation thresholds

- top 5% in one direction: interesting but insufficient;
- top 5% in both directions: strong exploratory pair-specific signal;
- top 1% in both directions: unusually strong exploratory signal;
- below top 10% in either direction: do not describe the pair as unusually concordant under V2.

No percentile is a soulmate probability.

## Known prior information

The 2030-2032 region was already discussed before V2. Any concentration there is development evidence, not untouched confirmation.

The V1 null benchmark was also already observed and was not exceptional. V2 is a new frozen model, but because it is motivated by that V1 result it is still development, not independent validation.

## Required output

Save:

`reference/research/partner_multidomain_1000_results_v2.json`

Include:

- freeze spec path/hash;
- seed and pool definitions;
- SWIEPH file hashes;
- all real-state domain scores;
- all real-state categorical overlap diagnostics;
- domain-specific ranks/percentiles;
- joint ranks/percentiles;
- reciprocal results;
- null summary statistics;
- limitations.
