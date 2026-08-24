# Gauquelin 5-15 / VITALITY heterogeneity stress audit

**PHASE: DEVELOPMENT**

Date: 2026-08-24

This is a post-hoc robustness/heterogeneity audit of the already-selected 5-15 development candidate. It is not independent confirmation and does not change the frozen MoBa primary predictor.

## Overall development association

Among the 1,105 usable Gauquelin source-person IDs:

- 5-15 present: 12 / 123 = 9.76% VITALITY
- 5-15 absent: 51 / 982 = 5.19% VITALITY
- raw odds ratio: about 1.97

Selection-aware development evidence remains governed by `gauquelin_vitality_mpod_development_2026_08_24.md`, not by the raw post-selection Fisher test.

## Leave-one-profession-out

The overall direction remains positive after removing each profession separately:

| Excluded profession | Remaining N | OR |
| --- | ---: | ---: |
| ACTORS | 832 | 1.52 |
| SCIENCE | 888 | 1.90 |
| SPORTS | 745 | 2.23 |
| WRITERS | 850 | 2.22 |

Thus no single profession is necessary for the aggregate positive direction.

## Profession-specific heterogeneity

| Profession | N | VITALITY / 5-15 | VITALITY / no 5-15 | OR |
| --- | ---: | ---: | ---: | ---: |
| ACTORS | 273 | 6 / 27 | 20 / 246 | 3.23 |
| SCIENCE | 217 | 1 / 21 | 4 / 196 | 2.40 |
| SPORTS | 360 | 5 / 49 | 21 / 311 | 1.57 |
| WRITERS | 255 | 0 / 26 | 6 / 229 | 0.00 |

The writer subgroup is discordant. Counts are small and these subgroup analyses are post-hoc, so they are descriptive rather than separate significance tests.

## Birth-era heterogeneity

Using broad post-hoc birth-year bins:

| Birth era | N | VITALITY / 5-15 | VITALITY / no 5-15 | OR |
| --- | ---: | ---: | ---: | ---: |
| <=1859 | 297 | 2 / 26 | 9 / 271 | 2.43 |
| 1860-1889 | 292 | 1 / 24 | 19 / 268 | 0.57 |
| 1890-1919 | 362 | 8 / 64 | 13 / 298 | 3.13 |
| 1920+ | 154 | 1 / 9 | 10 / 145 | 1.69 |

Three of four bins are directionally positive, but 1860-1889 is opposite. This weakens any claim that the development association is population-invariant.

## Resampling stability

In 2,000 random half-samples of the development people, the raw 5-15 minus non-5-15 VITALITY-rate difference was positive in about 94.8% of samples, with a median difference near +4.6 percentage points.

A simple person bootstrap placed about 95.9% of replicate raw differences above zero, but the approximate 95% bootstrap interval still crossed zero (roughly -0.5 to +10.4 percentage points). These numbers are stability diagnostics only; they do not undo development selection.

## Consequence

The 5-15 candidate remains worth an independent test because its aggregate direction is not carried by one required profession and because it survived the earlier full-selection null more strongly than arbitrary raw-formula searches. However, the profession and era heterogeneity lowers confidence that the effect is universal and makes an external cohort substantially more informative than further optimization of Gauquelin.

The frozen MoBa protocol is unchanged. MoBa must be analyzed once under its frozen primary Activity outcome and model; this heterogeneity audit may not be used to retune that validation.
