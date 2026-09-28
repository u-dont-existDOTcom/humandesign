# Unique-person / unique-chart hypothesis — preregistration candidate

Date: 2026-09-28

## Question

Do people with more statistically unusual personality/behavior profiles also have more statistically unusual birth-chart geometry?

This is distinct from DOB recoverability. A chart can be rare without personality matching it, and a personality can be unusual without being predictable from birth data.

The owner case motivated the hypothesis and therefore must be treated as discovery-only, not confirmatory evidence.

## Core design principle

Compute two rarity scores independently:

1. **Person uniqueness** from behavior/personality measurements with no birth/chart information.
2. **Chart uniqueness** from date/time/place with no personality information.

Freeze both algorithms before pairing the two columns. Then test whether the scores covary across untouched participants.

## Person-uniqueness measurement

Primary measurement should not be a direct question such as "are you unique?" Use a broad validated facet-level personality battery plus the existing theory-blind Life Patterns / Survey-v2 evidence where appropriate.

Recommended primary statistical score:
- standardize each frozen personality facet against an external or held-out normative reference;
- estimate a shrinkage/robust covariance matrix;
- compute multivariate Mahalanobis distance from the normative center;
- convert distance to an empirical percentile / tail probability.

Secondary robustness score:
- k-nearest-neighbor local density in the same standardized facet space;
- low local density = unusual trait combination.

Avoid interpreting one extreme trait as equivalent to a globally unusual profile.

### Informant replication

To capture the owner's "other people also say I am unusual" observation without relying on reputation:
- recruit preferably two independent informants who know each participant well;
- have informants complete the same observable trait/facet battery independently;
- calculate self uniqueness and informant-derived uniqueness separately;
- preregister informant-consensus uniqueness as a secondary/stronger measure;
- do not tell informants the chart hypothesis.

A direct "how unique is this person?" rating may be collected only as a secondary subjective variable, not the primary uniqueness outcome.

## Chart-uniqueness measurement

Do **not** use the owner-fitted V1.4d six-rule signature as the primary cross-person chart score.

Primary theory-neutral geometry score:
- exact tropical geocentric positions from the frozen ephemeris;
- all 45 unordered pairs among Sun–Pluto;
- distance to the nearest predeclared major aspect (0/60/90/120/180);
- predeclared angular distances to ASC/MC (or nearest of ASC/MC/DSC/IC);
- optionally a separately declared location-free planetary-only score and location/time-sensitive angular score;
- estimate multivariate local density against a very large reference universe of birth moments;
- chart uniqueness = negative log2(reference density), or an empirical rarity percentile.

Secondary chart scores:
- full frozen rule-library signature rarity (not an owner-selected subset);
- Human Design structural-state rarity;
- simple aspect-tightness density;
- angular exactness rarity.

Keep these separate rather than searching for whichever one correlates best.

## Primary statistical test

H0: person uniqueness and chart uniqueness are independent.

Primary test:
- Spearman correlation between frozen person-uniqueness percentile and frozen theory-neutral chart-uniqueness percentile.

Secondary:
- robust regression / rank regression;
- self-report uniqueness vs chart uniqueness;
- informant uniqueness vs chart uniqueness;
- agreement between self and informant uniqueness;
- location-free planetary rarity vs angle-dependent rarity.

Use permutation testing by shuffling complete birth tuples among participants while keeping personality records fixed. This gives a direct empirical null without assuming normality.

## Confounds / stratification

Predeclare treatment of:
- age/cohort;
- sex/gender only if the normative personality instrument requires it;
- country/language/cultural reference population;
- birth-time precision/rounding;
- prior astrology/HD exposure;
- self-selection into the study.

Do not define "unique people" after observing chart rarity.

## Approximate sample size

For a two-sided alpha=.05 correlation test at 80% power, Fisher-z approximations are:
- true rho=.30 -> about 85 participants;
- rho=.25 -> about 124;
- rho=.20 -> about 194;
- rho=.15 -> about 347.

A practical first confirmatory cohort is therefore ~200 participants if the target is a modest rho≈.20 effect. A 300–400 participant cohort is preferable if smaller effects matter and for informant/subgroup analyses.

A small 30–50-person pilot is useful only for checking measurement reliability and workflow, not for a persuasive uniqueness correlation.

## Stronger prediction

If both hypotheses are true:
1. chart geometry predicts personality at least weakly; and
2. rare chart configurations generate more distinctive personality combinations,

then chart uniqueness should predict **personality uniqueness prospectively**.

A stronger preregistered extension is:
- compute chart uniqueness before behavioral data are scored;
- predict that higher chart uniqueness produces higher personality uniqueness;
- separately test whether higher chart uniqueness also produces better concealed-DOB recovery.

The two outcomes must not be conflated.

## Owner status

The owner's current V1.4d six-rule conjunction is known to be structurally rare (9 of 52,596,001 century minute positions), and the owner's broader tight-aspect geometry was also unusual in random-chart benchmarks. The owner's perceived/behavioral uniqueness cannot be used to test the new hypothesis because the hypothesis was generated after inspecting the owner case.

The owner can remain a motivating development example only.

## Relation to existing project safeguards

This protocol extends rather than replaces:
- `docs/14_responder_heterogeneity.md`;
- `docs/23_survey_v2_recoverability.md`;
- the Survey-v2 candidate-blind human-measurement contracts.

The critical new requirement is an independently frozen **person-uniqueness metric** and a target-independent **chart-uniqueness metric** before confirmatory participants are paired.
