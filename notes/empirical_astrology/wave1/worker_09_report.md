# Worker W09 report — Research Issues B + Chapter 7 summary

## Scope and boundary

- Worker: `W09`
- Assigned printed book pages: **686–754**
- Source read directly: Dean, Mather, Nias & Smit (2022), *Understanding Astrology*, UA-3 PDF.
- Covered sections: `7.7.2005.2` through `7.7.2020.13`, plus the opening of `7.8` printed on pp.753–754.
- `7.7.2005.1` begins on printed p.685 and was left to W08 even though its final paragraph appears at the top of p.686. This preserves the non-overlapping study-start boundary.
- The Chapter 7 summary continues on printed p.755 in UA-4; that continuation belongs to W10 and was not duplicated here.

## Extraction counts

| Measure | Count |
|---|---:|
| Distinct source documents/reports | 64 |
| Empirical or data-bearing source documents | 50 |
| Feature-level JSONL records | 91 |
| Priority A | 62 |
| Priority B | 9 |
| Priority C | 4 |
| Priority D | 16 |
| Positive | 40 |
| Null | 17 |
| Opposite | 3 |
| Mixed | 11 |
| Unclear | 5 |
| Nonempirical | 15 |
| Records explicitly flagged for likely dataset reuse | 21 |

“Positive” preserves the original reported direction. It does **not** mean that UA accepted the finding. Many positive records are precisely the cases UA attributes to multiplicity, bad controls, semantic circularity, self-attribution, astronomical base rates, or overfitting.

## Reused or overlapping datasets

The 21 flagged records collapse mainly into these recurring clusters:

1. Church of Light → Lois Rodden → AstroDataBank, including McDonough, Bergen, and the Rajopadhye opposite-group analyses.
2. Gauquelin professional data.
3. Gauquelin couple/family/heredity data reused across Tarvainen, Gillman, Kampherbeek/NVWOA, and related analyses.
4. Addey's 7,302 UK doctors.
5. Roberts–Greengrass's 128-person time-twin sample, later discussed again in Chapter 8.
6. Within-paper reused cohorts: Godbout's biography/chart sets, Bhandary's 150 mental-health charts, Rajopadhye's opposite groups, and the paired Kampherbeek calculations.

The coordinator should assign canonical dataset IDs before treating these as independent replications.

## Highest-value findings for an empirical algorithm

1. **Expected frequencies must be conditional, not uniform.** Barbot's 10-million-date simulation and Vail–Pottenger's duration tables show large planet-pair, aspect, orb, epoch, and retrogradation effects. The canonical scorer should calculate duration- and sample-weighted prevalence over the exact universe.
2. **Opportunity counts can manufacture relationship hits.** Bagley's harmonic-contact rules had an approximate chance probability of `0.999997` for at least one claimed contact after all harmonics, planets, and aspects were counted.
3. **Large-N significance is not useful by itself.** Waller's random MMPI-gender links became overwhelmingly significant at N=81,485. Tarvainen's mathematician effects were at most `r=.032`, with mean about `.0065`.
4. **High-dimensional discovery needs a locked holdout.** McDonough's 300,000-factor AstroDataBank scan did not replicate. Bergen's >65 `p=.001` findings were fewer than the roughly 80 expected by chance from about 80,000 tests.
5. **The control generator is part of the model.** Ruis's three carefully built controls differed significantly; simple shuffling does not remove self-attribution, cohort, demographic, or astronomical dependencies.
6. **Semantic matching requires an empirical null.** Godbout's significant N×N biography/chart matches were not exceptional relative to random-predictor expectations. UA's simulation showed chance hits were not fixed at one and that keyword clouds heavily interfered with genuine matches.
7. **Prior astrology exposure can create the predicted behavior.** Clobert et al.'s three experiments found own-horoscope valence changed cognition/performance with mean `r≈.06`. Lu et al. showed translation-created stereotypes, hiring and dating discrimination, but almost no intrinsic Big Five or job-performance relationship.
8. **Exact opposite groups are a strong exclusion design.** Rajopadhye et al.'s Vedic tests produced 544 effect sizes with mean `r=-.000`, SD `.028`, and mean p-value `.482`. The agreed 41-rule system did not distinguish extreme opposite outcomes.
9. **Negative replication must remain explicit.** Kampherbeek/NVWOA found planetary-sequence heredity in the opposite direction under both calculation variants (`p=.23`, `.15`) after Gillman's `p<.0001` claim.
10. **Agreement bounds accuracy.** Bhandary's claimed mental-illness effects (`phi=.560/.626`) are incompatible with low or negative astrologer agreement (`.267/-.111`) unless judge-level reporting or analysis is wrong. Raw per-rater predictions are mandatory before use.

## Top 10 original sources to retrieve next

1. **McDonough & Phillipson (2006), Correlation 24(1), 34–40** — locate any surviving AstroDataBank analysis code, factor registry, control-generation rules, and replication logs behind the 300,000-factor scan.
2. **Barbot (2013), “Aspects in ten million charts 5000 BC to 5000 AD”** — obtain the full correction table, date/time generator, ephemeris, rounding, and code.
3. **Vail & Pottenger (1986), *Tables for Aspect Research*** — digitize pair-by-degree duration tables and verify them against the canonical ephemeris.
4. **Bergen (2014), *The Astrology Code*** — recover the full test universe, all group Ns, control definitions, and unselected results for a multiplicity audit.
5. **Mercadé (2017), *Diseño experimental para la contrastación del hecho astrológico*** — obtain subject-level pilot outcomes, chart-awareness measures, control-chart construction, and planned IPA/IM definitions.
6. **Godbout (2019), Kepler Conference characterology analysis** — obtain all 5,996 factor definitions, keyword dictionaries, thesaurus transformations, controls, and feature-elimination path.
7. **Godbout (2020), Correlation 32(2), 13–41** — obtain the 73 biographies/charts, birth-source ratings, vocabulary extraction, complete N×N matrices, ranks, and code.
8. **Tarvainen (2020), Correlation 32(2), 55–61** — obtain all mathematician birth dates, 18 aspect definitions, full orb search, one-/two-tailed tests, and 1,000 control sets.
9. **Lu et al. (2020), JPSP 119(6), 1359–1378** — obtain preregistrations, item-level Big Five data, randomized label materials, job-performance models, and all subgroup effects.
10. **Rajopadhye et al. (2021), IJAR 7(5), 74–85 plus AstrologyYesOrNo materials** — obtain the exact four/five opposite-group cohorts, all 41 executable rules, weights, 544 effect sizes, code, and planned replications.

## Coordinator cautions

- Treat multiple feature records from one paper or dataset as dependent evidence.
- Preserve original claims separately from UA's criticism; the JSONL does this explicitly.
- Do not infer missing Ns, p values, effect sizes, or methods from UA's prose.
- Several book/blog/conference reports are Priority A because their definitions or data are necessary to reproduce or falsify influential claims, not because the review judged them credible.
- The 15 nonempirical records are retained as Priority D because they define methodological arguments and failure modes that recur in the empirical literature; they must not enter a quantitative effect synthesis.
