# Worker W08 report — Research Issues A (book pp. 619–685)

## Scope and method

I read the complete assigned range directly from Dean, Mather, Nias & Smit (2022), *Understanding Astrology*, UA-3, book pages 619–685 (PDF pages 126–192). The range contains 80 numbered 7.7 sections. I recorded every numbered section, and split embedded empirical studies, reanalyses, controls, and independently meaningful feature results into separate JSONL records. Page 685 starts 7.7.2005.1, but its substance continues on page 686; I recorded only the heading/opening scope and explicitly handed the continuation to W09.

The extraction distinguishes original claims from the review authors' interpretation. Missing statistics remain null or are explicitly described as absent. Quantities shown below are computed from the JSONL.

## Counts

- Study-level source/citation groups: **98**
- Feature-level JSONL records: **126**
- Full-text priority: **A 44 / B 30 / C 16 / D 36**
- Result direction: **positive 11 / null 20 / opposite 4 / mixed 23 / unclear 12 / nonempirical 56**
- Likely reused named datasets: **16** (the same historical datasets often generate several feature records)

## Main extraction findings

1. **Astronomical definitions and controls matter before psychology.** Lunar parallax can shift the Moon by roughly half a degree in many charts and up to about one degree, while planetary-pair separations and retrograde states are strongly nonuniform. Any small-orb or aspect-frequency test must reproduce the same reference frame, ephemeris, historical interval, time/location distribution, and uncertainty.
2. **Harmonic waves did not independently replicate.** Like-sample correlations for UK/US doctors, clergy, and polio cases averaged approximately zero, whereas overlapping subsets or shared demographic structure correlated. Moving averages can manufacture persuasive waves from random data.
3. **Feature proliferation is a recurring failure mode.** Planetary nodes, arc transforms, minor points, and retrospective progression lists multiply the number of available hits. Opportunity counts, frozen registries, multiplicity correction, and untouched validation are therefore algorithm requirements rather than optional refinements.
4. **The largest direct aspect test in this range was null.** Startup tested 911 people, 32 consensus aspect pairs, and 121 predicted links; results were no better than chance despite power for tiny effects.
5. **Whole-chart matching remained poor.** The Indiana 23-chart test and follow-up were worse than chance and had poor inter-astrologer agreement. The three-study review found no valid rules or whole-chart readings, weak confidence calibration, poor retest agreement, and acceptance of wrong-chart readings. The broader matching synthesis did not differ from chance.
6. **Prior astrological knowledge is a demonstrated confound.** The significant Sun-sign/extraversion zig-zag (N=2,324, p=0.000005) disappeared in people unfamiliar with sign meanings. Prior knowledge must be measured before testing, with astrology-naive analysis primary.
7. **Jack Chandu's programme contains valuable but methodologically weak leads.** It reports an opposite Venus–Uranus result in 5,000 homosexual/bisexual cases, comparisons of ten house systems, nulls for added factors, a 5° major-aspect exercise, and mixed rectification results. Lack of controls, modern criterion measures, blinding, exact definitions, and inferential statistics makes original recovery mandatory before algorithm use.
8. **A probabilistic synthesis cannot rescue invalid inputs.** Dean's IRT demonstration on 120 extreme-EPI cases produced flat random-like curves for binary Sun/Moon sign indicators. Calibration must follow, not substitute for, held-out feature validation.

## Likely reused datasets

- Addey/Tobey professional solar-degree totals: UK and US doctors; UK and US clergy.
- Addey UK polio totals, including overlapping full samples/subsets.
- Addey's 970 nonagenarians, 1,025 polio cases, and 7,302 UK doctors reused in the 1997 harmonic history/reanalysis.
- The 120 extreme-EPI cases from UA 7.6.1985.2 reused for the 1993 IRT demonstration.
- Mayo–White–Eysenck and Smithers–Cooper Sun-sign/EPI datasets reused in later self-attribution analysis.
- Carlson (1985), Dean (1985/1986), and McGrew & McFall (1990) reused by Heukelom's 1991 three-test review.
- The astrologer-matching corpus summarized at N=47 in 2001 and updated to N=70 in Chapter 8.
- Chandu's 100-person development sample reused across criterion, sign/aspect, added-factor, and ten-house-system comparisons.

## Top 10 original sources to retrieve next

1. **Michael Startup (1985), British Journal of Social Psychology 24, 307–315**, plus the 1984 Goldsmiths thesis — exact 121 tests, aspect/orb definitions, effect estimates, and multiplicity handling.
2. **Jack Chandu, *Kosmodiagnostisch Analyse Systeem* (1976) and the 1980 English update** — raw tables, criterion definitions, control construction, house-system scoring, Venus–Uranus contact definition, and sample provenance.
3. **Dean & Mather, *Recent Advances in Natal Astrology* (1977), pp.143–152, 263, 294** — complete harmonic correlations, data provenance, peak calculations, and node opportunity counts.
4. **John Addey primary harmonic datasets and writings**, especially *Selected Writings* (1976) and solar/aspect-orb tables — recover unsmoothed counts and exact preprocessing.
5. **Carl Payne Tobey's 1937 *American Astrology* doctor/clergy solar-degree series** — independent raw totals and sampling frames for reproducible harmonic reanalysis.
6. **Mark Pottenger/Scott Vail aspect-frequency work** (1989 articles; *Astrological Research Methods*, 1995:203–233; 1986 tables) — ephemeris, cadence, station definition, and full pair-frequency tables.
7. **Carol S. Mull (1986), “Encounter with Academia”**, plus the underlying 23×23 choices and follow-up — exact hits, agreement, methods, and participant/chart provenance.
8. **Mayo, White & Eysenck (1978) and Smithers & Cooper (1978)** with follow-ups — subgroup Ns, knowledge measure, effect sizes, and raw/aggregate sign-by-EPI data.
9. **Geoffrey Dean (1993), Correlation 12(1), 10–27** — IRT routines, calibration details, the 120-case data, parameters, and fit statistics.
10. **T. Patrick Davis (1997), Correlation 16(2), 3–9**, plus all six *Aspects* contest notices, entries, and answer keys — recover the rare prospective tasks and exact outcomes.

## Coordinator cautions

- Several “positive” records are positive controls, astronomical nonuniformities, or documented psychological self-attribution effects; they are **not** positive evidence for natal astrology.
- `likely_dataset_reuse` is deliberately true on historical syntheses and overlapping subsets. Deduplicate by underlying case set, not citation title.
- The same Chandu sample supports many published percentages; it must count as one development dataset, not many replications.
- The apparent N=9,297 in the Addey historical record is a sum of three described samples and should not be treated as independent from the detailed harmonic records.
- W09 should own the substantive extraction of 7.7.2005.1 beginning page 686; W08 includes only the page-685 boundary record.
