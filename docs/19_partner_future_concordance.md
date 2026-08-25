# 19 — Partner Future-Concordance Forecasting Protocol

## Purpose

This module asks a stricter question than ordinary synastry or Human Design connection analysis:

> If two people are actually going to share a future life, do independently generated forecasts for each person converge on the same relationship status, economic mode, home/community structure, work/purpose state, and geographic region during the same period?

The method is designed to reduce post-hoc storytelling. It does **not** assume that strong attraction, synastry, or a favorable connection chart proves that two people are destined to remain together.

This is a separate research track from natal V4.3 reverse matching and from the static relationship mechanics in `docs/18_relationship_analysis.md`.

## Core principle: predict each life separately first

Do **not** start from the pair chart and ask how to make a reunion story fit.

For partner A and partner B:

1. calculate each natal chart independently;
2. generate a future life-state timeline for A without inspecting B's timeline;
3. freeze timeline A;
4. generate a future life-state timeline for B without inspecting A's timeline;
5. freeze timeline B;
6. only then compare the two timelines;
7. after the independent comparison, add pair-specific synastry/connection timing as a separate corroborative layer.

When one partner has an unknown birth time, generate every materially distinct natal/time state for that local civil day and retain only predictions that are robust across all states as unconditional claims. Time-dependent predictions remain explicitly conditional.

## Forecast horizon

Default exploratory horizon:

```text
now -> +15 years
```

For long-cycle questions such as permanent economic independence, long-term settlement, or retirement from conventional earning, extend to +30 years or later.

The horizon and temporal resolution must be frozen before inspecting pair concordance.

Recommended default resolution:

- exact roots for major aspect/HD boundaries;
- monthly or quarterly state summaries;
- annual summary vector for null-distribution comparison.

## Multi-domain future state vector

For every time bucket, generate a state vector rather than a single `romance yes/no` flag.

### 1. Romantic / attachment state

Allowed descriptive categories include:

- solitary / no major bond;
- dating/opening;
- intense but unstable bond;
- stable partnership;
- relationship restructuring;
- separation/closure;
- unknown / insufficient signal.

Do not infer a specific partner from an individual chart alone.

### 2. Economic mode

Distinguish:

- conventional employment/earning;
- entrepreneurial/high-leverage earning;
- financially supported/dependent;
- money-light;
- substantially money-independent;
- literal moneyless living;
- transition/unclear.

`Money-independent` means money no longer organizes daily survival even if some currency transactions still occur. Do not silently equate it with literal zero monetary use.

### 3. Home / community mode

Examples:

- private individual household;
- couple household;
- shared household;
- land/farm-based living;
- intentional community;
- nomadic/travel-heavy;
- institutional setting;
- unsettled/transition.

### 4. Social environment

Examples:

- solitary/private;
- couple-centered;
- family-centered;
- networked/community-centered;
- public-facing;
- retreat/contemplative.

### 5. Work / purpose mode

Examples:

- intensive project-building;
- conventional career;
- teaching/healing/service;
- entrepreneurial exchange;
- domestic/care role;
- retreat/contemplation;
- public leadership/visibility;
- low-work / subsistence / supported life.

### 6. Geographic state

Preserve several layers:

- country/region corridor;
- latitude/longitude corridor when astrocartography supports it;
- foreign vs natal-country residence;
- urban vs rural;
- tropical/temperate or other broad environmental signature;
- settled vs mobile.

Do not claim an exact city when the technique supports only a broad line/corridor.

### 7. Belonging / settlement

Examples:

- uprooted;
- searching;
- temporary base;
- long-term settled;
- strong community belonging;
- home-building/property focus.

### 8. Family / care responsibility

Examples:

- low caregiving load;
- partner care;
- child/family care;
- community care;
- high dependency/rescue burden;
- unclear.

### 9. Spiritual / psychological orientation

Examples:

- outward action;
- contemplative withdrawal;
- spiritual study;
- healing/service;
- existential restructuring;
- ordinary/stable baseline.

## Western astrology layer

Use a declared tropical/geocentric standard with verified SWIEPH data.

### Primary developmental techniques

Use, in order:

1. secondary progressions;
2. exact transits to natal planets/angles;
3. progressed angles and progressed Moon when birth time is known;
4. solar arcs as an explicitly separate exploratory layer unless independently validated;
5. solar/lunar returns only when a narrower interval needs refinement.

For economic/community/home hypotheses, do not rely only on Venus or the 2nd house. Evaluate relevant combinations across:

- 2nd/8th house and rulers/resources;
- 4th house/home/land;
- 6th/10th work structure;
- 7th partnership;
- 9th/12th foreign/retreat themes;
- Jupiter/Saturn/Uranus/Neptune/Pluto cycles;
- progressed Sun/Moon/Venus/Mars;
- exact natal aspect activations.

### Astrocartography / relocation

Calculate with verified SWIEPH equatorial coordinates.

At minimum support:

- Sun/Moon/Mercury/Venus/Mars/Jupiter/Saturn/Uranus/Neptune/Pluto;
- ASC/DSC/MC/IC lines;
- broad corridor distance;
- relocation chart confirmation for candidate places.

A place becomes strong pair evidence only if **both independently generated location forecasts overlap** during the same time period.

## Human Design layer

Keep Human Design dynamic forecasting separate from Western astrology.

Eligible layers:

- Uranus opposition chart;
- Chiron return chart;
- Saturn return chart where relevant;
- candidate-specific transit overlays;
- temporary channel/center definition;
- split bridges;
- relationship connection chart under transits;
- progression/developmental modules explicitly documented by the project.

Global Cycle themes are low-specificity background and must not be treated as strong pair evidence by themselves.

## Collective-vs-individual specificity weighting

A shared forecast is less impressive when millions of people receive the same symbolism.

Freeze a specificity class before comparison:

| Specificity | Example | Default weight |
|---|---|---:|
| S1 | exact personal progression/aspect to natal planet/angle | 1.00 |
| S2 | natal-house/angle or HD individual life-cycle activation | 0.85 |
| S3 | pair-specific synastry/connection activation | 0.75 |
| S4 | slow planet to natal planet without angle/house specificity | 0.60 |
| S5 | sign ingress / HD global cycle shared by a population | 0.25 |

Weights are research rubric values, not empirical probabilities.

## Birth-time uncertainty weighting

For a partner with unknown time:

- `robust_across_all_states = 1.00`;
- `robust_across_majority = 0.60`;
- `single-state-only = conditional/unscored for pair-wide claim`.

Do not choose the unknown birth-time state merely because it increases future concordance with the other partner.

## Independent timeline freeze

Each individual timeline must record:

```json
{
  "person_id": "opaque-id",
  "natal_input_hash": "...",
  "ephemeris_hash": "...",
  "forecast_model_version": "...",
  "horizon": ["2026-01-01", "2040-12-31"],
  "techniques": ["secondary_progressions", "transits", "astrocartography", "HD_life_cycles"],
  "timeline_hash": "...",
  "other_partner_timeline_visible": false
}
```

No pair-concordance scoring may occur until both timeline hashes are frozen.

## Shared-life concordance

After both timelines are frozen, compare time-aligned state vectors.

For domain `d` and time bucket `t`:

```text
concordance_dt =
    state_agreement(A_dt, B_dt)
    × specificity_weight_dt
    × confidence_A_dt
    × confidence_B_dt
    × birth_time_robustness_dt
```

Then:

```text
SharedLifeConcordance = Σ domain_weight_d × concordance_dt
```

### Default domain weights

Before empirical calibration, use equal weights for:

- relationship status;
- economic mode;
- home/community mode;
- location corridor;
- work/purpose mode.

Social environment, belonging, family/care, and spiritual orientation are corroborative secondary domains and must not dominate the result merely because they are easier to narratively match.

Do not tune domain weights after seeing a known couple.

## Harder convergence patterns

The following are stronger than simultaneous romance activation alone:

1. both predict stable partnership in the same period;
2. both predict the same economic transition;
3. both predict the same home/community mode;
4. both independently point to overlapping geographic corridors;
5. both predict compatible work/purpose states;
6. pair-specific synastry/HD connection mechanics become supportive during the same interval.

Example of a high-information hypothesis:

```text
Both people independently enter a stable partnership,
become substantially money-independent,
move toward land/community living,
and independently favor the same Southeast Asian corridor
within the same 18-month window.
```

That is materially more discriminating than `both have good Venus transits`.

## Pair-specific corroboration after independent timelines

Only after timelines A and B are frozen, calculate:

### Western

- synastry transit activation;
- progressed-to-natal cross-aspects;
- progressed-to-progressed aspects;
- progressed composite where a valid birth time exists;
- composite transits;
- relocation/composite geography as exploratory layers.

### Human Design

- static connection fingerprint;
- transiting temporary Centers/Channels;
- split bridges;
- changing 9+0 / 8+1 / etc. surface state;
- pair-specific electromagnetic/compromise activation where mechanically defined.

These may strengthen or weaken a shared-life hypothesis but do not rewrite the already frozen individual timelines.

## Random-partner null distribution

A high concordance score is not meaningful until compared with how often similar overlaps arise by chance.

For a focal person A:

1. choose a preregistered null partner pool;
2. sample at least 1,000 partners for development, preferably 10,000+ for final exploratory work;
3. match broad age/sex/geographic constraints appropriate to the research question;
4. calculate the same independent future-state timeline for every null partner;
5. compute `SharedLifeConcordance(A, null_i)` using the exact frozen model;
6. locate the real partner in the empirical null distribution.

Report:

- percentile;
- number of null partners exceeding the real partner;
- strongest domains responsible for the difference;
- sensitivity to unknown birth time;
- sensitivity to collective low-specificity features.

Do not call a high percentile a soulmate probability.

## Reciprocal null test

Where useful, also evaluate partner B against a null pool rather than only A against alternatives.

A pair is more interesting if the overlap is unusual in **both directions**.

## Anti-overfitting safeguards

The module MUST:

- preserve both independent timelines before pair comparison;
- preserve misses and non-overlaps;
- avoid selecting a forecast window because the pair already reunited there;
- avoid changing birth-time rectification to improve pair concordance;
- distinguish collective/global-cycle effects from individual-specific effects;
- distinguish literal claims (`moneyless`) from broader constructs (`money-independent`);
- never infer a specific partner from an individual chart alone;
- never use pair concordance to alter natal V4.3 NetInformation.

## Prospective validation

The strongest use is prospective.

Freeze a future hypothesis such as:

```text
2029-10 through 2031-06:
- both partners independently show stable-bond activation;
- both show reduced dependence on conventional earning;
- both show movement toward community/land-based settlement;
- both location forecasts overlap in the same broad region;
- pair-specific connection mechanics become less obstructed.
```

Define in advance what counts as:

- hit;
- partial;
- miss.

Do not move the window afterward.

## Output format

Every pair forecast report should include:

```text
Forecast protocol version:
Person A natal/time certainty:
Person B natal/time certainty:
SWIEPH verification status:
Forecast horizon:
Individual timeline A hash:
Individual timeline B hash:
Domains compared:
High-specificity overlaps:
Low-specificity/collective overlaps:
Geographic overlap:
Pair-specific corroboration:
Null-pool definition:
Null percentile:
Unknown-time sensitivity:
Strongest contradictions/non-overlaps:
Prospective frozen windows:
Overall status: exploratory / development / prospective
```

## Implementation target

Add a separate package rather than overloading static relationship analysis:

```text
src/hdmatch/relationship/
    future_state.py
    concordance.py
    null_partners.py
    western_timing.py
    hd_timing.py
    geography.py
```

Suggested pure-Python APIs:

```python
forecast_individual_life_state(...)
freeze_individual_timeline(...)
compare_frozen_timelines(...)
calculate_pair_specific_corroboration(...)
run_null_partner_distribution(...)
```

The pair-future module consumes deterministic natal/ephemeris outputs and produces a separate research report. It must not modify the natal reverse-matching model.
