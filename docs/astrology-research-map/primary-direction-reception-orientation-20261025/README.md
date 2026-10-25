# Lilly first edition: mutual reception and angular progression research

**Date:** 25 October 2026. **Owner root goal OPEN:** historically auditable methods from multiple astrology traditions, frozen before comparison with untouched forward-blind human evidence and independently matched controls. This branch handles a narrow Western primary-source and synthetic feature subtask; it does **not** establish astrology's predictive validity.

## New original source evidence

Five public-domain images of William Lilly, *Christian Astrology* (original London 1647 printing), printed pp.112,510,511,515,517, from the Wellcome digitization b30338724, are preserved under `witness_pages/`. Other relevant original pages (101–105,115,654–655,670) remain in the earlier two first-edition research packets. For close interpretation, see `PRIMARY_WITNESS_FINDINGS.md`; the accompanying PDF study by Rumen Kolev was consulted as **secondary historical criticism** (1998), not as a replacement for the photographed first printing.

The source p.112 worked cases verify sign-domicile reception (Sun in Aries, Mars in Leo), daytime triplicity reception (Venus Aries, Sun Taurus), and term reception (Venus 24° Aries, Mars 16° Gemini). Reciprocity is required; a planet being in another planet's dignity one way is **not mutual reception**. The p.115 +5 for mutual domicile and +4 for mutual exaltation are **alternative same-factor point slots**, not unlimited additive bonuses. Mixed-category reciprocal hosting is mathematically enumerable, but whether it has the same interpretive status as Lilly's worked **same-category** reciprocal examples is unresolved. Crucially, Lilly discusses two planets serving as **significators** in an actual question; an arbitrary natal planet pair does not automatically qualify as an operative direction interpretation.

For angle directions, p.515 works with **RA(promissor) − RAMC** and p.517 with **oblique ascension(promissor) − oblique ascension(Ascendant)**. The witnessed source arithmetic is implemented independently in `src/hdmatch/astrology/lilly_angle_progression.py`, without pretending these two examples reproduce every Argolus direction. The original p.515 list has an apparent 7°45′ Mercury-term arc while its displayed operands and subsequent subtraction give 7°25′; both printed observations are retained. The p.510–511 forward/backward examples concern constructed dexter/sinister zodiacal aspect rays, not proof of a universal *modern converse* time-motion convention.

## Frozen mathematical comparison — 96 older synthetic charts

Before counting anything, the historical witness, source-coded reception predicates, method-specific angle examples, tests and explicit no-human-data contract were committed to `humandesign` branch `research/primary-direction-reception-orientation-20261025` (precommit `286bbc5`). The inputs are **exactly the earlier 672 source-visible planet rows and 216 direction contacts** from the preceding published, independently replayed 96-chart artificial panel. Original parent file hashes are checked. No new birth tuples, life events, human questionnaires, score thresholds or favorable event-selection rules were introduced.

| Frozen-source mathematical count | Result |
| --- | ---: |
| Synthetic natal charts | 96 |
| Unordered reciprocal-hosting planet pairs, all dignity types | **462** |
| Of these, at least one **same dignity type** is reciprocal | **172** |
| Mixed-types-only reciprocal hosting, authorial significance unresolved | **290** |
| Charts containing at least one same-type reciprocal pair | **89 / 96** |
| Previously frozen favorable Midheaven–Jupiter aspect contacts | **47** |
| Of those 47, Jupiter in any same-type reciprocal dignity | **19** |
| Of those 47, Jupiter in reciprocal domicile or exaltation | **8** |
| Authoritatively complete Lilly Jupiter-strength verdicts | **0** |
| Human outcome observations or predictive validations | **0** |

Multiple same-type dignities can occur for one unordered pair: the sum of distinct per-mode counts therefore need not equal 172. The 47 Midheaven–Jupiter items are *contact exposures*, not 47 independent people. These figures reflect source-visible **structural features in a nonrepresentative stratified synthetic chart panel**, not prevalence in people or accuracy. In particular, p.112's two-significator context is not established by enumerating all 21 classical planet pairings; no pair is upgraded to a fulfilled personal-life prediction.

The MC arithmetic agrees to floating precision with the already implemented three geometric labels for a zero-declination promissor to the exact meridian: this is a **special-case equivalence**, not three independent tests or a global Argolus algorithm. Ascendant oblique-ascension examples reproduce Lilly's printed subtraction but do not authenticate the full 17th-century tables or angular-house latitude variants.

## Reproducibility and scope

`build_reception_inventory.py` computes these source predicates purely from frozen earlier CSV/JSON, then emits the four source-feature JSON results. `verify_reception_replay.py` recomputes all four files and checks their bytes exactly; the results are captured in `RECEPTION_REPLAY_VERIFICATION.json`. Regression tests in `tests/unit/test_lilly_reception_orientation_1647.py` check original worked examples, source-specific orientation, exact sign/reception distinction, ordering, data hashes and explicit unresolved predictions. The previously published partial-dignity source engine and the prior 96-chart study are not overwritten.

**Remaining owner outcome:** determine historically correct conditional strength, reception applicability to angular significators, and direction roles/time convention from primary evidence; then lock event outcomes, permitted birth-time uncertainty, baseline exposure-years, dependence/multiplicity and prospective assessment before opening genuinely untouched human evidence. A separately named *modern diagnostic primary-directions arm* could be tested earlier if fully preregistered, but it must not be called verified authentic Lilly.

**Study result:** source arithmetic and synthetic feature counting reproducible; **human predictive accuracy UNTESTED**.
