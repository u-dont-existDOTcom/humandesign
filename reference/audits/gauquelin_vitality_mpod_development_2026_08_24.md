# Gauquelin VITALITY minimal-predictive-object development audit

**PHASE: DEVELOPMENT**

Date: 2026-08-24

This audit records unrestricted/post-hoc hypothesis discovery on the Gauquelin character-trait data. These data are explicitly development data: they may influence formulas and target definitions, but no result here is independent confirmation or evidence of generalization.

## Data

The inspected workbook contains 4,353 trait-person rows. Deduplication by source-person identifier yielded 1,110 source IDs; five had conflicting recorded birth times, leaving 1,105 usable people for this development pass. The archive contains exact date, hour/minute, place/coordinates, profession, source-person identifiers, trait terms, and Gauquelin planetary-sector columns.

Important limitation: the 35 archival trait terms have Gauquelin planetary-category history. This dataset is therefore unsuitable as a final astrology-naive validation cohort. It is used here as a hypothesis-generation sandbox.

Astronomy for this exploratory pass used the reduced Moshier implementation after a mechanical parity check against the repository's verified 1985 reference case. It reproduced the visible reference activations/bodygraph exactly, but this run is **not canonical V4.3** because the repository's production Swiss `.se1` provenance requirement was not satisfied.

## Phase routing

Two-question checksum:

1. May these data influence the hypothesis/model? **YES.**
2. May these data establish that the selected hypothesis generalizes? **NO.**

Accordingly, post-hoc feature search, target decomposition, exhaustive subset search, perturbation tests, repeated cross-validation, and failure inspection were deliberately allowed.

## Initial frozen AstroHD/Sacral target

The original single-target experiment used the repository's existing symbolic Sacral-energy mapping. A broad archival target grouped `ACTIVE`, `ENERGETIC`, `VITALITY`, and `DYNAMIC`; a narrower sensitivity target grouped `ENERGETIC`, `VITALITY`, and `DYNAMIC`.

The broad and narrow aggregate targets showed small directional associations with Sacral definition, but the aggregate grouping was later decomposed because its constituent words did not behave as one empirical construct.

## Unrestricted raw-astronomy search: negative result

A low-complexity grammar of roughly 6,100 astronomical basis functions was searched, including:

- Personality and Design longitudes and speeds;
- single-body harmonics;
- same-side pairwise phase differences;
- orientation-sensitive sums;
- Personality-to-Design differences;
- limited cross-side differences.

Conventional controls included exact birth-year indicators, profession, timezone, day-of-year harmonics, hour-of-day harmonics, latitude/longitude terms, and annotation/citation intensity.

Greedy short formulas could add apparent cross-validated AUC on the development data. However, rerunning the **entire formula-selection procedure after shuffling astronomy between people** routinely produced gains of the same size. The unrestricted raw-astronomy winner was therefore rejected as null-like development overfit.

The same failure occurred when roughly 2,000 HD gate/channel/core features were allowed to compete freely: the selected gains were not unusual under full-selection shuffles.

### Numerical grammar bug found and excluded

Personality Sun minus Design Sun is mechanically fixed at approximately 88 degrees by the Design-moment definition. Tiny root-solver/floating-point residuals could be magnified by standardization and falsely appear predictive. Deterministically fixed or near-constant derived features must be removed before future symbolic-regression/search work; numerical variation in a mathematical constant is not a physical predictor.

## Constrained Sacral-mechanism minimization

Rather than search arbitrary astronomy, the next pass minimized the already-motivated Sacral prediction.

Sacral definition can arise through 11 channels:

`20-34`, `10-34`, `2-14`, `5-15`, `29-46`, `27-50`, `6-59`, `42-53`, `3-60`, `9-52`, `34-57`.

Every nonempty subset was evaluated: all **2,047** possibilities. For each candidate subset, the predictor was whether at least one selected channel was defined. Selection was repeated under shuffled chart/channel assignments to estimate how large a best-of-2,047 result appears under the null.

## Trait decomposition

The earlier aggregate energy target concealed strong heterogeneity:

- `ENERGETIC`: null-like under the exhaustive subset-selection null.
- `DYNAMIC`: null-like.
- `ACTIVE`: somewhat unusual but not compelling after full selection.
- `VITALITY`: materially more unusual than the other three and became the development target for minimization.

This decomposition is post-hoc and therefore belongs entirely to DEVELOPMENT. Its purpose is to generate a precise external hypothesis, not to claim significance from the Gauquelin cohort.

## VITALITY result

There were 63 people carrying the archival `VITALITY` label among the 1,105 usable people.

### Smallest one-channel candidate

The strongest one-channel subset was **5-15**.

Observed archival rates:

- channel 5-15 present: 12 / 123 = **9.76%** VITALITY;
- channel 5-15 absent: 51 / 982 = **5.19%** VITALITY;
- absolute difference: about **+4.56 percentage points**.

Under the strong conventional-control residual scan, the 5-15 score was `0.0233882274`. In 1,000 full chart-assignment shuffles, 25 shuffled searches produced a one-channel maximum at least this large. Using the conservative `(ge + 1)/(N + 1)` convention gives an empirical development-selection p-value of about **0.026** for the one-channel complexity class.

Five-fold cross-validation, used only as a development ranking/stability tool, showed about **+0.0094 AUC** beyond the strong conventional control model for the 5-15 indicator.

### Development-best five-channel subset

The best five-channel subset was:

`2-14 OR 5-15 OR 29-46 OR 6-59 OR 3-60`

Its residual score was `0.0297393277`. Four of 1,000 shuffled searches had a five-channel maximum at least as large; six of 1,000 shuffled searches had an overall best-across-all-subset-sizes maximum at least as large. The corresponding conservative empirical rates are approximately 0.005 within size five and 0.007 after allowing the selected subset size to vary.

Five-fold development cross-validation added about **+0.0299 AUC** beyond the same strong control model for the five-channel indicator.

Because this is more optimized and more complex, it is retained only as a **secondary external-validation candidate**. The smaller 5-15 object is the primary candidate.

## Gate-level interaction check

The 5-15 association is not reproduced by either gate marginally:

- Gate 5 active anywhere: little/no incremental signal;
- Gate 15 active anywhere: little/no incremental signal;
- Gate 5 OR Gate 15: little/no useful signal;
- Gate 5 **AND** Gate 15, i.e. channel 5-15: the development signal appears.

This makes the candidate an interaction/co-occurrence hypothesis rather than a generic Gate 5 or Gate 15 effect.

## Raw mathematical compression of 5-15

Using the frozen Rave wheel:

- each gate sector is `360 / 64 = 5.625°`;
- Gate 5 occupies `[251.375°, 257.000°)`;
- Gate 15 occupies `[88.250°, 93.875°)`;
- their forward sector separation is `35 * 5.625° = 196.875°`.

A raw representation equivalent to channel 5-15 for the standard 26 Personality/Design activations is therefore:

```text
Z_5_15 =
    1[at least one activation lies in 251.375° <= λ < 257.000°]
    AND
    1[at least one activation lies in 88.250° <= λ < 93.875°]
```

No named HD interpretation is required to evaluate this object.

## Geometry perturbation audit

These perturbations were all inspected on DEVELOPMENT data and are not confirmatory tests.

### Joint orientation rotation

Keeping the 5.625° widths and the 196.875° separation fixed, both windows were rotated together in 0.25° steps over 360°.

- actual HD orientation score: `0.0211644175`;
- rank: **12 / 1,440** rotations (top ~0.83%);
- best development rotation: +271.25°, score `0.0257514781`.

The fact that another rotation fits development somewhat better is exactly why the HD orientation must be frozen and tested externally rather than retuned.

### Separation perturbation

Holding Gate 5's window fixed and varying the second window's separation in 0.125° increments:

- exact 196.875° separation score: `0.0211644175`;
- exact separation rank: **3 / 2,880**;
- development-best separation: 196.625°, score `0.0218027842`.

Restricting alternatives to the 63 other equal 5.625° sector separations, the actual **35-sector separation ranked #1 of 63**.

### Window width perturbation

Holding the exact gate centers fixed and varying both widths from 1° to 15° in 0.125° increments:

- exact 5.625° width rank: **2 / 113**;
- development-best width: 5.0°;
- the response forms a nearby ~5–5.7° plateau rather than uniquely identifying 5.625°.

When testing equal divisions `n = 24..128`, `n=64` ranked **3 / 105**. Thus the development evidence is more specific to the relative gate geometry/orientation than to a uniquely optimal number 64.

## Body-family minimization: rejected for now

Searching which celestial-body families are needed can produce a much smaller subgroup with a large apparent VITALITY rate. However, when the full body-subset selection procedure was repeated under shuffled assignments, the best body-subset result was not exceptional enough to promote. Therefore the validation candidate keeps the full standard 26 activation set rather than selecting a post-hoc body subset.

## Historical-coding sensitivity

Because `VITALITY` is classified in the source workbook under Gauquelin Mars/Saturn categories, a sensitivity model added the workbook's Mars and Saturn sector variables to the conventional controls. The development-best Sacral subset remained in the extreme tail of 500 full-selection shuffles (2/500 at least as large).

Adding all five Gauquelin planet-sector encodings weakens the result substantially. That analysis is difficult to interpret as a conventional-confound adjustment because those variables are themselves competing astronomical encodings. The result is recorded rather than used to rescue or reject the candidate.

## Birth-time robustness

Uniformly shifting the historical birth times by ±15, ±30, and ±60 minutes changed the 5-15 classification for only a very small fraction of records and preserved the direction of the development association. The candidate is therefore not mainly a one-minute boundary artifact.

## Development conclusion

The unconstrained formula hunt did **not** produce evidence distinguishable from a best-of-many null. The useful result came from minimizing one already-motivated AstroHD mechanism and then decomposing the archival phenotype.

The smallest candidate worth spending independent validation data on is therefore:

> **The raw two-window co-occurrence equivalent to Human Design channel 5-15 predicts higher vitality/energy.**

The five-channel subset is retained as a secondary development-selected candidate. Neither is validated by this audit.

## External-validation firewall

No individual-level outcome data from the proposed NCDS validation cohort were accessed during this development search. The validation specification is frozen separately before any such outcome data are opened.
