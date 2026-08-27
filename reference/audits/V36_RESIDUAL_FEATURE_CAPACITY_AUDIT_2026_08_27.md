# V3.6 residual-feature capacity audit — 2026-08-27

## Purpose

Identify which structural chart distinctions still contain discrimination after conditioning on the full clean V3.6 participant-observable profile.

This is a survey-design diagnostic, not behavioral validation. A feature receives information-capacity credit only when it splits states that the 26-observable clean V3.6 profile leaves tied. High residual capacity means the feature is a priority for source and operationalization research; it does not mean the feature has a true behavioral correlate.

## Baseline

Verified century universe: 288,938 structural intervals.

Clean V3.6 participant-observable baseline:

- 26 observables;
- 54,307 observable fingerprints;
- 15.006554 interval-uniform bits;
- 14.947304 duration-weighted bits;
- median tie 9 states; p95 43; max 111;
- previously studied 1985 reference observable tie: 11 states.

## Highest residual structural capacity

Capacity below is incremental **after** the clean V3.6 observable fingerprint.

| Feature | Incremental uniform bits | Combined exact top-1 ceiling | 1985 reference tie after feature |
|---|---:|---:|---:|
| all Personality+Design activation vector | 2.912339 | 88.925% | 1 |
| active-gate set, either side | 2.725070 | 80.648% | 1 |
| Personality activation vector | 2.370282 | 65.054% | 2 |
| Design activation vector | 2.368779 | 64.991% | 1 |
| Design active-gate set | 2.321029 | 63.434% | 1 |
| Personality active-gate set | 2.319792 | 63.404% | 2 |
| Personality Moon gate | **2.141942** | 57.263% | 2 |
| Design Moon gate | **2.139833** | 57.199% | 3 |
| channels | **2.100149** | 57.441% | 4 |
| Personality Mercury gate | 1.374102 | 37.646% | 5 |
| Design Mercury gate | 1.373363 | 37.618% | 5 |
| Personality Venus gate | 1.355834 | 37.249% | 5 |
| Design Venus gate | 1.353428 | 37.231% | 4 |
| Personality Mars gate | 1.284871 | 36.037% | 5 |
| Design Sun/Earth gate | 1.284489 | 35.580% | 5 |
| Design Mars gate | 1.282040 | 35.993% | 1 |
| Personality Earth gate | 1.252221 | 35.158% | 5 |

The complete activation vector still does not itself close the whole average 3.133846-bit clean-profile gap: clean V3.6 + full gate-position vector reaches 256,937 distinct fingerprints and an 88.9% structural top-1 ceiling. Therefore a scientifically useful survey cannot rely on a single omitted category; it needs several independently justified observables and redundancy for human response noise.

## Priority for universal survey expansion

The global ranking, rather than the known subject-specific tie, should drive what gets researched first.

1. **Moon activations** are the strongest single-planet omission by a wide margin: ~2.14 residual bits on either side.
2. **Channels** still contain ~2.10 residual bits despite many channel/gate themes already present in V3.6; this means the old holistic profile covered only a subset of bodygraph distinctions.
3. **Mercury and Venus activations** are the next strongest single-position families at ~1.35–1.37 bits.
4. **Sun/Earth and Mars** remain useful at roughly 1.25–1.28 bits each.
5. Multi-activation sets/vectors have very high capacity, but they are not participant observables. They are guides for finding several narrower behavioral hypotheses, not answer categories themselves.

For every new survey dimension, require a documented pre-existing HD claim, a participant-observable operationalization that does not use HD vocabulary, explicit context/exception handling, and a frozen predicted-response rule before blind participants are seen.

## Known 1985 reference caution

Within the 11-state reference tie, Design Mars alone happens to make the previously studied 1985 reference state unique. That fact must **not** determine universal survey construction: Design Mars 61 was already one of the two candidate-exposed refinements in the old V3.6 descriptive audit. Selecting it because it isolates the known state would reproduce the exact leakage the blind protocol is designed to prevent.

The same caution applies to any feature selected because it helps this one known reference. Use the global residual-capacity ranking to prioritize source research, then freeze a generic question/mapping set before new participants.

## Survey architecture implication

A fixed question count is the wrong target. The interviewer should maintain a predicted candidate partition and select the next preregistered question by expected information gain subject to reliability and dependency constraints. Persistent behavioral patterns, childhood-to-adult continuity/change, context, exceptions, and free-form `Other` elaboration should remain the primary elicitation style. Redundant questions can be retained for reliability without pretending they add independent bits.
