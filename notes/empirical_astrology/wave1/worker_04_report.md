# Worker W04 extraction report

## Scope and completion

- Worker: **W04**
- Source: Dean, Mather, Nias & Smit (2022), *Understanding Astrology*, UA-2
- Assigned printed-book range: **pp. 387-450**, inclusive
- PDF pages read: **192-255**, inclusive (PDF page 2 is printed book p.197)
- Coverage: final Application Issues material on p.387 onward; all of Conferences & Surveys in the assigned range; Events through `7.4.1986.3` on p.450
- Extraction status: **complete for the entire assigned range**

The conference reports were treated as containers rather than single studies. Each separately testable dataset, replication, feature/outcome, control analysis, or quantitatively meaningful claim was extracted as its own record where the text allowed. The website postscript on pp.429-430 was also exhausted: low-detail listings were retained as acquisition records rather than silently discarded.

## Counts

| Measure | Count |
|---|---:|
| Distinct study-level source/citation strings | 191 |
| Feature-level JSONL records | 219 |
| Records flagged as likely dataset reuse/reanalysis | 52 |

### Full-text priority

| Priority | Count |
|---|---:|
| A | 128 |
| B | 63 |
| C | 26 |
| D | 2 |

### Reported-result direction

| Direction | Count |
|---|---:|
| Positive | 89 |
| Null | 51 |
| Opposite | 10 |
| Mixed | 29 |
| Unclear | 38 |
| Nonempirical | 2 |

The direction labels preserve the source-level reported result. They are not judgments about truth. In particular, many positive records are exploratory, post-hoc, uncorrected for multiplicity, or later contradicted; those limitations are separately captured in `ua_criticism`, `multiplicity_handling`, and `replication_or_reanalysis_refs`.

## Likely reused datasets

Fifty-two feature records were explicitly marked `likely_dataset_reuse: true`. The main recurring families are:

1. **Gauquelin professional, trait, ordinary-person, heredity, and sector datasets** — repeatedly reanalyzed for eminence gradients, harmonics, traits, coordinate systems, classifiers, physical moderators, and occupation effects.
2. **Bender & Timm's 295 German astrologers** — original questionnaire plus the review authors' factor analysis of the published correlation matrix.
3. **Smithers's 5,644-person prison dataset** — separated into violence, sex offences, and seven other offence categories.
4. **Press's 311 New York suicides plus 311 controls** — original three-way replication design, expanded analysis, astrologer judgments, and Currey's later pooled reanalysis.
5. **Kuypers's 72 fatal-road-accident cases** — repeatedly mined for signs, natal squares, houses, and primary directions.
6. **Hill/Thompson's 500 redheads** — later compared by Steffert with 1,128 research volunteers and 24,961 Gauquelin ordinary people.
7. **Landscheidt's golden-section/planetary-cycle claims** — later reanalyzed by Ertel with random-number and alternative-proportion controls.
8. **Tomaschek's earthquake collection** — revisited by Henry and compared with a separate controlled 900-earthquake analysis.
9. **Bradley's Jupiter Pluvius rainfall data** — reanalyzed as a lunar-period/Earth-rotation artifact.
10. **Fatal-accident/suicide primary-direction material** — revisited across Kuypers and Smit reports with inconsistent and null replications.

## Main extraction cautions for the coordinator

- Several conference positives give no original paper, exact N, correction, or sufficient statistics. They remain useful acquisition leads but cannot support an algorithm yet.
- The strongest apparent positives often arise after broad feature searches: Hoffmann's astrologer aspects, Astro-Databank/AstroInvestigators rank lists, financial-cycle work, earthquake configurations, and repeated mining of the Kuypers accident sample.
- The range contains unusually informative controls: wrong/opposite chart descriptions, sham dates/events, fictitious directions, unrelated-event controls, split replications, alternative coordinate systems, and explicit demographic/astronomical artifact analyses.
- Uniform sign/house/aspect expectations are repeatedly shown to be unsafe. Hièroz's Venus exposure counts, Startup's seasonal academic artifact, Tomaschek/Henry, Bradley/James, and Nelson/Hunter/Dean all support computing duration- and population-conditioned expectations.
- Conference summaries sometimes repeat the same data under a new analytical lens. The 52 reuse flags should be normalized to canonical dataset IDs before source counts are used in any meta-analysis.
- No inference was made where the review supplied only a study title. Such records have `result_direction: unclear` and the missing detail is explicit.

## Top 10 original sources to retrieve next

1. **Mark Urban-Lurain, multivariate profession classification (6th AA conference; related Astrological Journal material, 1987).** The reported held-out result is 26.3% versus 12.5% across eight Gauquelin professions and is the clearest explicit train/test classifier in this range. Retrieve code/model specification, split construction, feature count, confusion matrix, and leakage controls.
2. **Nona Press et al., “An astrological suicide study,” *Journal of Geocosmic Research* 2(2), 23-33 (1977-78), plus Press's 1993 expansion.** It is the broadest replicated null in the range: 311 cases, 311 controls, three groups, and roughly 100,000 factors.
3. **Suitbert Ertel's 1987 trait-artifact and paired planetary-type experiments.** These directly test whether Gauquelin trait effects survive blind re-extraction and expert/name-only judgments; exact pair allocations, hit counts, and planet-wise results are essential.
4. **Mavis Klein's synastry interpretation matching study (reported at the 6th AA conference, 1987, with fuller publication promised).** Both male and female rank distributions were nominally p<.01; retrieve questionnaire construction, decoy generation, couple response dependence, exclusions, and exact analysis.
5. **Mike O'Neill's 35,000-partner/17-million-control node study (reported at the 7th AA conference, 1988).** This is a very large synastry analysis whose significance disappears when Royal couples are added; obtain construction of artificial pairs, all tested bodies/orbs, and subgroup decisions.
6. **Judith Hill & Jacalyn Thompson's Mars/Redhead paper, together with Beverley Steffert's volunteer-effect reanalysis (1988).** The combined materials may distinguish a sampling/volunteer artifact from a residual redhead effect.
7. **Geoffrey Dean, “Nelson's radio forecasts” reanalysis, *Correlation* 3(1), 4-37 (1983).** It includes 5,507 operational forecasts, a mean r=.010, government/persistence controls, solar-flare checks, and factor-level planetary-index tests.
8. **Jean Barets, *L'Astrologie rencontre la science* (1977).** Its 96/112 political-advancement hit claim uses a comparatively explicit transit rule; the complete event list and matched non-event controls are needed to test it fairly.
9. **Nick Kollerstrom, “Lunar phase and wheat germination,” *Correlation* 4(1), 25-31 (1984), plus the 1941-42 failed replications.** This provides a reproducible biological protocol, an 8% reported mean difference, obvious temperature/noise sensitivity, and prior negative evidence.
10. **Kyösti Tarvainen, “One should know 100 persons when studying astrology,” *Astrological Journal* 53(3), 59 (2011).** Its 611-factor registry and simulation are directly useful for feature-prevalence, exposure, and sample-size planning even though they do not validate meanings.

## Output

- `data/empirical_astrology/wave1/worker_04_studies.jsonl`
- `notes/empirical_astrology/wave1/worker_04_report.md`
