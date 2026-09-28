# Worker W10 report — Chapter 8 synthesis

## Scope completed

- Worker: `W10`
- Source: Dean, Mather, Nias & Smit (2022), *Understanding Astrology*
- Assigned range: book pages **755–862**, inclusive (UA-4 PDF pages 1–108)
- Sections exhausted: **8.1 through the last line of 8.9.10.2 printed on page 862**
- Output: `data/empirical_astrology/wave1/worker_10_studies.jsonl`

The range was read consecutively from the source PDF. Records emphasize Chapter 8's cross-study conclusions and empirical results that add quantitative detail, methodological constraints, independent replications/reanalyses, or a new dataset. Explicit Chapter 7 cross-references are retained and flagged as overlaps rather than silently duplicated. Historical exposition and untested opinion were not converted into study records merely because they had a citation.

## Extraction counts

| Measure | Count |
|---|---:|
| Distinct study/source citations | 128 |
| Feature-level JSONL records | 130 |
| Priority A | 82 |
| Priority B | 33 |
| Priority C | 15 |
| Priority D | 0 |
| Positive | 12 |
| Null | 87 |
| Opposite | 11 |
| Mixed | 16 |
| Unclear | 4 |
| Records flagged for likely dataset/source reuse or explicit Chapter 7 overlap | 25 |

`Unclear` is reported in addition to the requested positive/null/opposite/mixed counts because it is a permitted schema value and prevents inconclusive studies from being forced into a direction.

## Cross-study conclusions most relevant to model design

1. **Sun-sign traits and compatibility:** Large surveys, personality studies, national marriage registers, and illness datasets converge on no practically useful sign effect once prior knowledge, response error, multiplicity, demographics, or held-out replication are handled. The repeatable positive phenomenon is self-attribution after exposure to sign descriptions, not a birth-derived trait signal.
2. **Whole-chart and high-dimensional searches:** Large searches by Niehenke, O'Neill, McDonough and others do not rescue traditional factors. Freedman's noise simulation and the Chapter 8 examples make person-split validation, feature-count penalties, and untouched evaluation mandatory.
3. **Synastry:** The 19-study synthesis excluding Jung gives mean `r=0.0004`; 2,824 Gauquelin married couples give about `r=0.0006` for interchart-aspect counts. Van de moortel's attraction study gives the one isolated result worth a preregistered replication (`mean r=0.085`), but its best test fails multiplicity correction and it lacks randomized-chart controls.
4. **Astrologer/chart matching:** Seventy tests involving roughly 2,400 charts and more than 1,000 astrologers give mean `r=0.031`, with observed variation explained by sampling error and likely publication bias. Higher-quality subsets, case histories, experience, confidence, technique, intuition, and neural networks do not rescue performance.
5. **Interpretation specificity:** Clients cannot select authentic readings once cues are removed (`mean r=-0.025`). Starword split exactly 15/15 authentic/control; Astro*Intelligence averaged only `phi=0.06`. Inter-astrologer agreement is about `0.098`, and ANOVA attributes 42% of reading variance to astrologers rather than charts.
6. **Time twins:** The 2,101-person London NCDS cohort is the strongest result in the range. Across 110 variables its mean serial correlation is `r=-0.003`; biological twins provide strong positive controls (`MZ=.58`, `DZ=.43`). Sensitivity tests could detect roughly one genuinely similar pair in 110, yet did not. Exact angular-Saturn, ability, hypochondriasis, and stillbirth contrasts were also null or opposite.
7. **Prediction:** Audits of thousands of public predictions, mundane cycles, transits, Indian astrology, horary, finance, and earthquakes fail prospectively. Brady-Lehman's cricket result is an especially clear development/holdout warning: 67.5% after predictor selection, 50% on six new matches.
8. **Wrong charts and degree areas:** Wrong charts repeatedly produce accepted narratives, while controlled authentic/control tests fail. Degree-symbol systems disagree; small-sample degree findings fail in samples up to 35,665 occupations. These results strongly constrain any algorithm that permits post-hoc symbolic substitution.
9. **Non-astrological mechanisms:** Expectancy, cue leakage, base-rate neglect, publication bias, flexible symbolism, pattern perception, and jointly discovered coincidences reproduce much of the apparent signal. These should be modeled as explicit threats, not pooled with natal evidence.

## Likely reuse and overlap flags

The 25 flagged records include:

- explicit Chapter 7 overlaps: Nelson radio forecasts; Press suicide charts; Niehenke aspect/personality data; O'Neill's Gauquelin-professional scan; McDonough's Astro-Databank scan; De Schrijver rectification; Dudley road-death matching; Narlikar and Rajopadhye Vedic tests; and the Dean/Eysenck intuition/experience corpus;
- recurring **Gauquelin** professional, heredity, and biography datasets;
- recurring **Eysenck/Dean** personality/matching datasets;
- recurring **Astro-Databank** timed-birth data;
- Steyn's same South African police-applicant population used for the 2011 sign study and 2013 one-day time-twin analysis;
- Roberts–Greengrass data reanalysed by French et al.;
- Tomaschek's earthquake claim followed by corrected-null and independent replications.

The coordinator should canonicalize these at the dataset level before counting independent evidence.

## Top 10 originals to retrieve next

1. **Dean & Kelly (2003), Journal of Consciousness Studies 10(6–7), 175–198** — NCDS time twins, positive controls, sensitivity analysis, exact-time subtests.
2. **The 70-test astrologer matching corpus and its source list in UA 8.10** — needed to reproduce the central `r=0.031` synthesis and publication-bias analysis.
3. **Niehenke, UA 7.6.1987.3 original study** — 3,290 timed births, 500-item questionnaire, aspect meanings.
4. **McDonough, UA 7.7.2003.2 original report/data** — approximately 300,000 features in 30,000 Astro-Databank births; critical for reuse and leakage auditing.
5. **Ruis (1993), Correlation 12(2), 20–43** — 2,824 married couples, 77 interchart aspects at 5° orb, 500 randomized matchings.
6. **Van de moortel (1998), Correlation 17(1), 50–53** — isolated attraction/synastry signal requiring exact reconstruction and replication.
7. **Roberts & Greengrass (1994) plus French et al. (1997), JSE 11(2), 147–155** — original 1,400-pair time-twin data and artifact-correcting reanalysis.
8. **Steyn (2011; 2013)** — 65,268-person South African sign/Big-Five study and the reused one-day time-twin subset.
9. **Austin et al. (2006; 2008), Journal of Clinical Epidemiology** — 5.3-million-person discovery/replication and 100,000-control selective-inference demonstration.
10. **Voas (2007), *Ten Million Marriages*** — highest-powered sun-sign compatibility test, including response-error corrections and all 144 pairing effects.

## Boundary note

Book page 862 ends mid-account of the 1983 superprize. W10 captured every result printed through that page, including 34 submitted entries and the disguised control being the sole success stated there. Any later judging details belong to the next page range and were not imported across the assignment boundary.
