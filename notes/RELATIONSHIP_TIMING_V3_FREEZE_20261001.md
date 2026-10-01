# Relationship Timing V3 — development freeze before future scan

Date: 2026-10-01
Status: development model; future scan not yet inspected at freeze time.
Supersedes for development comparison: Relationship Timing V2 only if the post-freeze future scan is generated without changing this file.

## Endpoint

Predict **major relationship / romance activation windows**, not relationship quality and not acute danger.

Historical development positives used to motivate this version:
- summer 2005;
- relationship onset in spring 2013;
- mid-2018;
- late-2025 / January-2026 relationship activation window.

Historical false-peak controls:
- the prior model's 2004 peak;
- the prior model's 2010–2011 peak.

These are development cases only. They cannot validate V3.

## Core change from V2

V2 let any sufficiently dense set of relationship transits produce a high score.

V3 is hierarchical:

```
relationship-state gate
    -> transit-trigger score
```

A transit pile-up cannot create a major relationship window unless an independent slower state indicator is active.

## Time unit

Score a centered 3-calendar-month event window:
- previous month;
- center month;
- next month.

The center month is the reported peak month.

This tolerates uncertain historical recall without allowing arbitrary wide windows.

## Direct relationship targets

- natal Venus;
- natal Moon because it is the 7th ruler;
- ASC/DSC treated as one axis.

## Stage 1 — relationship-state gate

The 3-month window is eligible if at least one of these independent state families is active:

### A. Annual profection state
At any date in the window:
- profected house is 5th or 7th; OR
- annual ruler is Venus or Moon.

### B. Secondary-progression state
A progressed personal body (Sun, Moon, Mercury, Venus, Mars) forms a major aspect
(conjunction, sextile, square, trine, opposition) within <=0.5° of Venus, Moon/7th ruler, or ASC/DSC.

### C. Solar-arc state
Either:
- solar-arc Moon, Mercury, Venus, or Mars forms a major aspect within <=0.5° of Venus, Moon/7th ruler, or ASC/DSC; OR
- any scored solar-arc body forms a major aspect within <=0.5° of ASC/DSC.

Solar-arc Sun is excluded because it duplicates secondary-progressed Sun by construction.

## Stage 2 — slow-transit trigger score

Only in an eligible state window, collect unique qualifying contacts from:
- Jupiter;
- Saturn;
- Uranus;
- Neptune;
- Pluto.

Targets:
- Venus;
- Moon/7th ruler;
- ASC/DSC.

Aspects:
- conjunction, sextile, square, trine, opposition.

Orb:
- <=1.0° at any point in the centered 3-month window.

Collapse repeated passes of the same transiting body × natal target × aspect to the closest pass in the window.

Base weight:
- ASC/DSC contact: 2.5
- Venus or Moon contact: 2.0

Exactness multiplier:
```
1 - 0.5 * orb_degrees
```
so a 0° exact hit gets 1.0 and a 1° hit gets 0.5.

State-family bonus:
```
score *= 1 + 0.20 * (number_of_active_state_families - 1)
```

No bonus is awarded merely for having more transit contacts outside the state gate.

## Development repair criterion

Before V3 may replace V2 prospectively:
1. summer 2005, spring 2013, mid-2018 and Jan-2026-era windows must all remain nonzero;
2. the rejected 2004 and 2010/11 romance peaks must score zero or below the weakest true development window;
3. future scan must be generated without changing targets, orbs, weights, gate, time window, or state definitions.

This is necessary development regression, not validation.

## Relationship danger and childbirth remain separate endpoints

V3 relationship activation must not be used to claim success on:
- acute relationship danger;
- exact childbirth timing.

Those endpoints remain governed by the separate longitudinal discrimination policy and require their own models.

## False-positive policy

All evaluation follows `docs/23_longitudinal_event_discrimination_policy.md`.

Future predictions may supersede V2 only by explicit versioned artifact created before the future window begins.
