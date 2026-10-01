# Progressed-chart timing policy V2

Date: 2026-10-01
Status: development policy; scientific validity not established.

## Scope

Secondary progressions and solar-arc directions are dynamic timing hypotheses. They are **not natal personality features** and must not silently enter the natal personality-to-DOB reverse matcher.

The natal chart remains the fixed candidate fingerprint. A progressed chart additionally requires an observation/event date, so it answers a different question: whether a dated state or transition is associated with a birth-derived dynamic chart.

## Secondary-progression convention

Use the repository's frozen day-for-year convention:
- one ephemeris day after birth = one tropical year of elapsed life;
- observation timestamps must be explicit and timezone-aware;
- calculate the progressed instant deterministically from the natal UTC instant and observation UTC instant.

For the current event-timing development layer:
- progressed bodies: Sun, Moon, Mercury, Venus, Mars;
- default tested aspects: conjunction, sextile, square, trine, opposition;
- default event-timing orb: <=0.5 degrees;
- targets must be frozen by event domain before outcomes are inspected.

These aspect/orb choices are a development hypothesis, not a universal astrology rule.

## Domain-first target selection

Do not scan every progressed contact and narrate the most convenient one afterward.

Before scoring a domain, freeze its natal targets. Example relationship target set used by Relationship Timing V2:
- natal Venus;
- natal 7th ruler;
- ASC/DSC treated as one axis.

Other domains require their own preregistered target sets and cannot inherit the relationship target set by convenience.

## Solar arcs

Treat solar arcs as a separate timing family.

- Solar-arc positions are natal positions advanced by the progressed-Sun solar arc.
- If secondary-progressed Sun is already scored, **do not also score solar-arc Sun**: they are mathematically the same longitude under this construction and would double-count one signal.
- Count an angle axis once. For example, conjunct DSC and opposite ASC are the same geometry, not two independent hits.
- Current development event-timing orb: <=0.5 degrees.

## Profections and other context layers

Annual profections may modify or gate a dated direct contact, but they do not create a timing hit by themselves.

For Relationship Timing V2:
- 5th- or 7th-house profection can amplify a qualifying direct relationship contact;
- a Venus- or Moon-ruled year can provide a smaller modifier;
- no profection points are awarded in a month with no direct timed contact.

Do not generalize those relationship-specific modifiers to other domains without a separately frozen rule.

## Dependency control

Before scoring:
1. identify mechanically dependent features;
2. collapse equivalent angle contacts;
3. remove duplicate constructions such as progressed Sun + solar-arc Sun;
4. count repeated passes by the same method/body/target/aspect once per declared scoring interval unless the protocol explicitly models pass sequence.

A dense list of correlated astrological descriptions is not independent evidence.

## Validation discipline

Progressions must not be introduced after a natal prediction misses as an ad hoc rescue.

For retrospective development:
- label revealed events as development data;
- model changes motivated by them cannot be validated on those same events.

For prospective tests:
- freeze observation/event windows, domain targets, aspects, orbs, dependencies, scoring and model version before outcome reveal;
- preserve misses and negative windows;
- compare against a natal-only baseline and simple time/null baselines.

## Personality-to-DOB matching boundary

Default rule: **no change to the natal personality-to-DOB matcher.**

Reason:
- personality-to-DOB asks for a persistent natal fingerprint;
- progressions encode age/observation-date-dependent state;
- mixing them into the natal score would make the candidate depend on when the questionnaire was answered and could leak age/calendar information rather than personality information.

A dynamic layer may be tested separately only when the questionnaire contains explicitly dated change/state observations. Such a test must:
- freeze the observation date independently of candidate DOB;
- score dynamic observations separately from persistent-trait observations;
- compare incremental out-of-sample value over the same natal-only model;
- never allow dynamic-state evidence to repair the natal fingerprint post hoc.

If the dynamic layer does not improve untouched validation, it remains excluded from personality-to-DOB matching.
