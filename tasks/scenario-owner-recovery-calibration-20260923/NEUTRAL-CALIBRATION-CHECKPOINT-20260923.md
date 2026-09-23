# Owner neutral calibration checkpoint — 2026-09-23

## Frozen input

Private measurement freeze SHA-256:
`7a6398de3c591e7dd8cc907b90c7312171452e6c13624a96e3f01826d6944863`

Participant-answer records: **68**

No birth/chart/model/candidate-ranking information was included in the neutral coding packet.

## Independent neutral coding

Two fresh GPT-5.6 Sol xhigh coding contexts independently reviewed the same frozen 68-answer packet against the neutral 73-facet contract.

Coder A:
- private output SHA-256: `538402a5d5f64ad4b75f08ba86943aab9d99d3011e14b040547032783966aa35`
- sufficient facets: 38
- partial facets: 11
- unknown facets: 3
- unassessed facets: 21
- fully covered neutral domains: 9 / 31
- partially covered neutral domains: 19 / 31
- uncovered neutral domains: 3 / 31

Coder B:
- private output SHA-256: `84be173203360e9d2370612ec492ae6dcec2bedd05540ced6f72ce7d4eec3e5c`
- sufficient facets: 42
- partial facets: 14
- unknown facets: 3
- unassessed facets: 14
- fully covered neutral domains: 9 / 31
- partially covered neutral domains: 19 / 31
- uncovered neutral domains: 3 / 31

The coders differ on 13 / 73 facet statuses but agree on the domain-level calibration shape.

## Decision

The completed owner pilot is **not yet a fully calibrated v7 neutral profile**. This does not mean the earlier pilot was unfinished. It means the pilot was completed, then its own evidence exposed several v6 questions as invalid, underspecified, tautological, or construct-mismatched; v7 subsequently replaced those routes. The old answers cannot simply be credited to the repaired constructs.

Do not open the participant to target-aware adaptive questioning. Additional questions must be selected from neutral evidence gaps only, with no birth/chart/model/rank information supplied to the selection context.

## Follow-up lane

The first target-blind repaired route selected for remeasurement is v7 `F0`, a matched audience-familiarity comparison. Its exact question was privately frozen before response. `F0` is a replacement measurement for a material repaired gap, not a generic decision to keep interviewing because some domain remains partial. Do not require exhaustive 73-facet completion; stop when remaining neutral gaps cannot materially change the declared recovery test.

The first F0 response is now privately preserved in the working measurement (69 answers total). A fresh target-blind incremental coder did **not** force-fit that response to the intended F0 facet and found one narrow missing piece remains. The raw response, participant-specific finding, and coding output remain outside Git.

After sufficient additional neutral measurements are collected:
1. create a new immutable private measurement freeze;
2. rerun independent neutral coding;
3. freeze/adjudicate the final neutral profile;
4. only then apply the historical post-freeze owner-recovery crosswalk and birth search.

No birth-recovery result has been claimed from the incomplete profile.
