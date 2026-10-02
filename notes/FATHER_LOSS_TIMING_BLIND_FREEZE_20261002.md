# Father-loss timing blind guess — freeze

Date: 2026-10-02
Status: retrospective blind-development guess. The owner's answer has not been inspected.

## Endpoint

Guess the timing of the owner's father's death, described only as a major turning point.

This endpoint is **father death / irreversible father loss**, not generic family stress, not relationship loss, and not "major life crisis."

## Natal targets

To reduce interpretive flexibility, use only the most cross-tradition father/parental targets:
- natal Sun;
- natal Saturn;
- the IC/MC parental axis, counted once.

Do not add house rulers, Nodes, lots/parts, outer-planet natal symbolism, or generic "death" houses after seeing the result.

## Timing families

### Slow transits
Bodies:
- Saturn
- Uranus
- Neptune
- Pluto

Qualifying aspects:
- conjunction
- square
- opposition

Orb:
- <=1.0 degree

Targets:
- Sun
- Saturn
- IC/MC axis

### Secondary progressions
Bodies:
- progressed Sun
- progressed Moon

Qualifying aspects:
- conjunction
- square
- opposition

Orb:
- <=0.5 degree

Targets:
- Sun
- Saturn
- IC/MC axis

### Solar arcs
Bodies:
- solar-arc Moon
- solar-arc Saturn
- solar-arc Uranus
- solar-arc Neptune
- solar-arc Pluto
- solar-arc ASC/MC axis

Qualifying aspects:
- conjunction
- square
- opposition

Orb:
- <=0.5 degree

Targets:
- Sun
- Saturn
- IC/MC axis

Solar-arc Sun is excluded because it duplicates secondary-progressed Sun.

### Annual profection context
A window receives a context bonus if its center date lies in:
- a 4th-house or 10th-house profection year; or
- a year whose annual ruler is Sun or Saturn.

Profection context cannot create a score by itself.

## Scoring window

Use a centered 3-calendar-month window.

For each unique qualifying contact appearing anywhere in the window:
- slow transit to Sun or Saturn: 2.0
- slow transit to IC/MC axis: 2.5
- progression to Sun or Saturn: 1.5
- progression to IC/MC axis: 2.0
- solar arc to Sun or Saturn: 1.5
- solar arc to IC/MC axis: 2.0

Exactness multiplier:
```
1 - 0.5 * orb_degrees
```

Multi-family bonus:
- x1.20 if >=2 timing families qualify;
- x1.35 if all 3 timing families qualify.

Profection context multiplier:
- x1.15 when active.

## False-positive discipline

The scan must rank the entire life timeline before the owner reveals the answer.

Return:
- one primary guess;
- one runner-up;
- their score/rank;
- nearby high-scoring false-candidate years if any.

After reveal, the guessed windows remain frozen as hits or misses. Do not add new father significators to rescue the outcome.

## Scientific boundary

This is an exploratory astrology test, not an evidence-based method for inferring deaths. It must not be used to predict another living person's future death.


## Pre-scan dependency clarification

Added before generating any ranked dates:

- IC and MC are one parental axis; conjunction to one and opposition to the other count once.
- A solar-arc angle pair is likewise one directed axis.
- Construction-identity conjunctions are excluded: progressed Sun conjunct natal Sun at the progression origin and solar-arc body conjunct its identical natal body solely because the solar arc begins at zero. Later square/opposition contacts remain eligible.
- Repeated passes of the same method/body/target/aspect inside one 3-month window count once at closest orb.
