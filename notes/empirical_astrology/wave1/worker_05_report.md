# Worker W05 report — later Events + Gauquelin Topics

## Scope and completion

- Assigned book range: Dean, Mather, Nias & Smit (2022), *Understanding Astrology*, pp.451–526.
- Source read directly: UA-2 pp.451–494 and UA-3 pp.495–526.
- Coverage: every numbered summary beginning in the range, from `7.4.1986.4` through `7.5.2019.1`.
- The three summaries beginning on book p.450 (`7.4.1986.1`–`7.4.1986.3`) were not extracted because they belong to W04's range. The continuation of `7.5.2018.1` on p.526 was read. `7.5.2019.1`, which begins on p.526 and continues outside the range, was recorded only for the material present on p.526.
- All independently testable embedded studies, replications, corrected reanalyses, and feature-level results printed in the range were split into their own records where the text permitted it.

## Counts

| Measure | Count |
|---|---:|
| Numbered UA source summaries covered | 76 |
| Additional embedded standalone study groups | 3 |
| Distinct citation/source groups in JSONL | 79 |
| Feature-level JSONL records | 146 |
| Records flagged as likely dataset reuse | 86 |
| Distinct citation groups with likely reuse | 50 |

### Full-text priority

| Priority | Records |
|---|---:|
| A | 111 |
| B | 18 |
| C | 3 |
| D | 14 |

The large A queue is intentional. This range contains unusually consequential nulls, replications, technical reanalyses, and recurring Gauquelin datasets. Most cannot safely inform an algorithm from the review summary alone.

### Result direction

| Direction | Records |
|---|---:|
| Positive | 37 |
| Null | 58 |
| Opposite | 10 |
| Mixed | 18 |
| Unclear | 9 |
| Nonempirical | 14 |

## Likely reused datasets

The main repeated lineages are:

1. **Gauquelin eminent-professional archive** — repeatedly reanalysed for sectors, aspects, signs, houses, harmonics, midpoints, personality, eminence, painters, writers, physicians, sports champions, and day/night effects. Records derived from it must be grouped by person/source before any train/test split.
2. **Gauquelin heredity/family archive** — reused for planetary heredity, the 2,174/2,824 marriage synastry studies, Vara's 2,823 marriages, Stanway's Paris parents, and birth-time-reporting analyses.
3. **Kuypers' 72 fatal traffic-accident cases** — repeatedly analysed for squares, Pluto/Ascendant, houses, primary directions, and related event-timing claims; some cases were explicitly selected because they fit directions.
4. **Thomassen/van Roekel 500 violent deaths** — original analysis and post-hoc reanalysis share the same cases; only the later 1,500-death sample is fresh replication.
5. **Hill/Polit great-earthquake selections** — initial, extended, review reanalysis, and later follow-ups overlap the same event family and selection rules.
6. **Westran public-record relationships** — first and second N=1,300 sets, the timed N=447 subset, and the dependence-reduced N=386 subset are related analyses, not four independent validations.
7. **Klein California work-injury data versus Swedish replication** — these are independent and must remain separate; the Swedish N=2,865 result failed to replicate the California N=1,023 signal.
8. **Paris 12th heredity cohorts** — the 1923–1931 and 1931–1939 cohorts are temporally distinct replications from the same registration system and locality.
9. **Meier/Plantiko painters** — 66% of N=192 and 80% of N=1,740 came from the Gauquelin archive; the apparent Vehlow-house replication vanished after those cases were removed.
10. **Ruis marriage samples** — N=2,174 and N=2,824 substantially overlap the same Gauquelin family archive; the larger sample is an extension, not an untouched replication.

## Highest-value findings for later model design

- **Conventional natal aspects received major negative tests.** Gauquelin's N=15,334 analysis and Ertel's N=20,528 exactness test found no useful aspect effects. O'Neill's 7,868-factor scan across 15,942 professionals found no stable conventional feature beyond small known Gauquelin patterns.
- **Event-timing systems repeatedly failed fresh or controlled tests.** This includes primary directions, progressions, transits at death, accident transits, Vedic accidental-death matching, and birth-time rectification. Stachniewicz's 6,466,063-death analysis is the strongest broad null for planet-to-planet natal/transit mortality features.
- **Several attractive positives fail independent replication.** Klein's California Sun/injury result failed in 2,865 Swedish accidents; the tuned hard-transit signal from 500 violent deaths reversed in 1,500 fresh deaths; Harris's IVF development model failed its independent clinic sample.
- **Most apparent synastry effects vanish under valid comparison.** Ruis's 2,174 and 2,824 marriages are null under 2×2/control-variance-aware tests. Westran's repeated Sun–Venus count pattern is worth reconstructing, but the published p-values are invalid and corrected effect estimates are near zero. Partner age-gap matching is an essential slow-planet control.
- **Birth-time provenance is not a nuisance variable; it is central.** Planetary effects often weakened as official time precision improved. Midnight avoidance, hour rounding, changing registration practice, and era/locality must be explicit fields and grouping variables.
- **Rectification needs a maximum-over-search null.** In one 720-interval search the probability of at least one eight-hit peak was 0.84. A visually impressive best time is meaningless unless compared with the full candidate-time universe.
- **Pseudoreplication recurs.** Hueber analysed person-days as independent; Gauquelin's character-trait work analysed traits rather than people; IVF treatments were nested within women; event studies often counted many transits per person. The independent unit must be the person, couple, event series, or site actually sampled.
- **Astronomical geometry can mimic moderation.** Mars day/night effects followed Sun–Mars conjunction/opposition geometry; house-dependent angle aspects appear equally in shuffled controls; transit availability can be cohort-specific.
- **Tiny effects and small p-values must stay separate.** Examples include stock-return lunar effects around `r≈0.01`, business outcomes `r=.017–.063`, corrected synastry `phi≈.002–.003`, and an optimistic hypothetical death-transit effect around `r=.003`.
- **Belief-mediated effects are a separate family.** Dragon-year fertility and possibly lunar market sentiment can be genuine behavioral effects without supporting a direct celestial mechanism. Astrology knowledge/exposure should be measured and modeled, not pooled with physical-effect claims.

## Top 10 original sources to retrieve next

1. **Slawomir Stachniewicz (2009), unpublished paper, “Planetary transits at 6,466,063 deaths.”** Obtain the manuscript, code, control generator, and ideally derived tables. It is the highest-powered broad null in the range.
2. **Mick O'Neill (1994), APP 10(2), 8–22, “Gauquelin data tested for 7868 chart factors.”** Obtain the full factor registry, split definitions, tables, and any surviving code/data.
3. **David Peter Valentiner (1988), *An Empirical Study of Astrology and Personality*.** Obtain the full unpublished paper, exact harmonic test definitions, validation table, and Mars–Achievement result.
4. **Suitbert Ertel (1988), Correlation 8(1), 5–21.** Retrieve the exact-aspect curves and professional subgroup results for the N=20,528 negative aspect study.
5. **Paul Westran (2006; 2021), *When Stars Collide* and Correlation 33(2), 13–33.** Obtain relationship-level data and code so Sun–Venus contacts can be recomputed with couple-label permutation, dependence controls, and valid effect sizes.
6. **Bert Terpstra (1990–1992), AinO rectification series.** Retrieve code/rules and case-level event lists for Chandu, Greene, other subjects, and random controls.
7. **Jan F. Ruis (1992–1994), AinO marriage-synastry series.** Obtain actual/control aspect counts, control-generation code, couple identifiers, overlap between N=2,174 and N=2,824, and orb-series results.
8. **Thomas Shanks (1987/1988), unpublished ACS Gauquelin analysis.** Seek the 67-page handouts/printouts and 100-control extension; it may be the most complete unpublished conventional-chart scan before O'Neill.
9. **Rüdiger Plantiko (2009), Zeitschrift für Anomalistik 9, 82–107.** Retrieve painter identifiers, source flags, house calculations, shuffled-time controls, and post-Gauquelin-removal results.
10. **Hervé Delboy (1999), “Transits” in *Comment démontrer l'astrologie*.** Retrieve event-level data, raw unsmoothed 1° separation counts, control dates, and all angle-selection steps; this is necessary to separate the traditional-angle null from the selected novel-angle artifact.

Close alternates for acquisition are Hueber's 1997 thesis (for a corrected multilevel mood analysis), the full Klein/Dobyns/Pottenger work-injury chain, and Tarvainen & Godbout's 2020 rounding simulation.

## Extraction cautions

- `original_reported_result` always states the source author's reported outcome; `ua_interpretation` and `ua_criticism` are kept separate.
- Exact numbers were copied when printed. No absent p-value, sample size, orb, or effect size was inferred.
- `likely_dataset_reuse=true` is conservative: it marks known or strongly indicated reuse/extension of a recurring archive. It is not a claim that every individual case overlaps.
- A source called “positive” may still be unusable; direction records what was reported, while priority and criticism record whether original material and reanalysis are required.
