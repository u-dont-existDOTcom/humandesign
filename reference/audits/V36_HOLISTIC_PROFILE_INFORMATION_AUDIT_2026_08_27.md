# V3.6 holistic-profile information audit — 2026-08-27

## Purpose

Measure how much deterministic century-wide discrimination is present in the old V3.6 holistic behavioral mapping family, without confusing its V4.3 rubric-bit score with Shannon information.

The audit uses the verified structural century cache (`288,938` intervals) and reports two partitions:

1. **participant-observable fingerprint** — channel/gate alternatives intended to explain the same behavior are collapsed to one observable construct; this is the conservative quantity relevant to survey design;
2. **mapping-pathway fingerprint** — every matched structural mapping remains distinct; this is a mechanical upper bound and is not treated as information a participant can necessarily report.

The clean variant excludes the two explicitly post-selection carrier refinements from the 2026-08-22 descriptive audit. The best-current variant includes them only to quantify their effect; it is not independent evidence.

## Results

| Metric | Clean V3.6 | Best-current incl. post-selection carriers |
|---|---:|---:|
| Active mappings | 42 | 44 |
| Observable constructs | 26 | 28 |
| Distinct observable fingerprints | 54,307 | 57,420 |
| Observable entropy, interval-uniform | **15.006554 bits** | 15.089878 bits |
| Observable entropy, duration-weighted | 14.947304 bits | 15.027760 bits |
| Median observable tie | 9 | 9 |
| p90 observable tie | 32 | 31 |
| p95 observable tie | 43 | 41 |
| Maximum observable tie | 111 | 111 |
| Uniform exact-state top-1 ceiling | 18.795% | 19.873% |
| Uniform top-5 ceiling | 59.128% | 60.888% |
| Uniform top-10 ceiling | 78.845% | 80.158% |
| Mapping-pathway entropy | 16.492393 bits | 16.506653 bits |

Exact interval identity over `288,938` states contains `18.140400` bits. The clean observable model therefore remains `3.133846` bits short of unique average discrimination, equivalent to about `8.78` equally likely states per observable fingerprint.

For comparison, the production compact questionnaire has only `8.084955` bits of canonical-answer entropy. The clean V3.6 holistic observable profile therefore adds `6.921600` bits, or about **121.23×** as much partitioning capacity.

## 1985 reference state

Reference timestamp used only to inspect the previously studied V3.6 state: `1985-01-29T00:22:30Z`.

Clean observable fingerprint:

- tie size: **11** states;
- interval-uniform specific information: **14.680969 bits**;
- duration-weighted specific information: `14.431113` bits.

Clean mapping-pathway fingerprint:

- tie size: 4 states;
- interval-uniform specific information: `16.140400` bits.

Best-current observable fingerprint after adding the two known post-selection carrier refinements:

- tie size: **1**;
- interval-uniform specific information: **18.140400 bits**.

That last uniqueness is descriptive only. The two carrier mappings were added after the 1985 candidate had already been exposed, so their subject-specific jump from an 11-state tie to a singleton must not be counted as independent confirmation or used to tune a future blind survey.

## Greedy clean observable sequence

The clean model reaches its full 15.006554-bit observable entropy after 19 informative observables. In greedy interval-uniform order:

1. `ORGANIZED_DETAIL` — +0.999257 bits
2. `INSIGHT_TO_STRUCTURE` — +0.998099
3. `PURPOSE_STRUGGLE` — +0.996173
4. `ORIGINAL_CONTRIBUTION` — +0.991919
5. `ENTERPRISE_PERSUASION_PATTERN` — +0.982386
6. `CONSEQUENTIAL_CORRECTION` — +0.972463
7. `EXISTENTIAL_MYSTERY` — +0.963280
8. `PROFILE_LINE6_PHASES` — +0.918011
9. `RHYTHM_ROUTINE` — +0.893398
10. `AUTHORITY_SOMATIC` — +0.878359
11. `VALUES_RESPONSIBILITY` — +0.861786
12. `CONTINUITY_PRESERVATION` — +0.831766
13. `RETREAT_PRIVACY` — +0.796426
14. `RESOURCE_SOVEREIGNTY` — +0.735032
15. `CONCENTRATED_FOCUS` — +0.638456
16. `PROFILE_LINE5_PROJECTION` — +0.593544
17. `NEEDS_SENSITIVITY` — +0.530637
18. `PROFILE_24` — +0.258813
19. `CONTRADICTION:MASTERY_REPETITION` — +0.166748

After those, the six center observables and `TYPE_ENTRY` add zero further noiseless partition entropy because their distinctions are already implied by the richer observable fingerprint. They can still be useful as noisy corroboration/error-checking; zero incremental entropy does not mean they are behaviorally meaningless.

## Survey-design implication

The immediate bottleneck is survey discrimination, not ephemeris generation. A next-generation interview should preserve the V3.6-style nuanced/contextual observables and add new independently justified behavioral distinctions specifically chosen to split the residual tie groups. It should not merely add more paraphrases of Type, Authority, or center themes.

The reference 1985 clean tie requires `log2(11) = 3.459432` additional ideal bits to isolate mechanically. On average the clean V3.6 partition requires `3.133846` more ideal bits. Since human responses are noisy, the design goal should be a unique predicted fingerprint plus redundant independent measurements, not merely reaching the 18.140400-bit identity ceiling on paper.
