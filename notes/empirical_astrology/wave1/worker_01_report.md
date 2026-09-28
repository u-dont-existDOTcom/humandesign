# W01 extraction report — UA book pages 197–272

Source: Dean, Mather, Nias & Smit, *Understanding Astrology* (2022), [UA-2 PDF](https://astrology-and-science.com/UA-2.pdf), complete assigned range. The PDF's first page is book p.197. The range has 7.1 Signs through p.266 and the start of 7.2 Application Issues on pp.267–272. The next study after the boundary belongs to W02; the 1957 prenatal-epoch summary on p.272 is included here only to its page boundary.

## Counts and coverage

- **83 review section summaries** covered; **129 feature-level JSONL records** (one per distinct reported study/result when separable).
- **117 provisional source citation keys** in the JSONL. This counts review summaries and embedded originals/reanalyses; it is *not* a deduplicated count of unique source documents. The coordinator should normalize citations. Every section in the assigned range has at least one record.
- Full-text priorities: A **85**, B **26**, C **8**, D **10**.
- Result directions: positive **35**, null **39**, opposite **8**, mixed **33**, unclear **6**, nonempirical **8**. These count feature records, including exploratory or artifact-prone reported positives; they are *not* vote counts on astrology.
- Primary sources obtained: **0**. The mandatory A queue marks the original full texts needed before algorithm use. `original_reported_result` is taken from the review's account of each original, and `ua_interpretation` and `ua_criticism` are kept separate. `null` means the excerpt did not provide the field; no missing p value or effect was inferred.

## Dataset reuse and conflict flags

1. The **ORC 1,026 British adults** recur under 7.1.1950.2 (blind trait choices) and 7.1.1973.1 (forecast outcomes). Distinct analyses of the same people.
2. **Kuypers 438 + 736 marriage pairs** recur under 7.1.1978.1 and 7.1.1982.1; the latter adds 253 + 257. Tellegen's 201 are separate. The 1974 Mark/Gilbert 446 divorce pairs and 446 controls are separate.
3. **Gauquelin archives** recur as professional groups, heredity couples, and comparison sets; code by underlying archive and subgroup before pooling.
4. **Sachs Swiss marriage/divorce and crime counts** are reused in the Ertel and von Eye reanalyses, which are separate analytical records, not new cohorts.
5. **Fuzeau-Braesch 524 French students** recur in the 1997 article, 1999 book, and 2009 account, all one cohort. **Metzner's 156 conference subjects** recur in color and somatotype papers.
6. **1975 and 1981 sign-guessing panels** were two separate 12-person tests but share astrologers; 7.1.1983.2 discusses the latter again.
7. The heading of 7.1.1992.2 says **8,379**, while the printed groups add **5,174 + 3,232 = 8,406**. Resolve in original. The 2015 Schwartz heading's N=34,000 refers to trait-specific filtering, while the Facebook source sample was 46,092.
8. The 1957 entry says “nine studies 1957–2009”, but book p.272 contains only Hièroz's nine timed cases and 36 method-case calculations. Do not claim the later eight studies were extracted in W01; they fall on subsequent book pages.

## Ten originals to retrieve next

| Rank | Original | Why |
|---|---|---|
| 1 | Mark & Gilbert, AFA Bulletin 36(8), 8–10 (1974) | Positive divorce double-link result, exact sign orb 16°, missing birth times, small effect; obtain raw pairing and control construction. |
| 2 | Fuzeau-Braesch, *Journal of Scientific Exploration* 11(3), 297–316 (1997), referee comments; and 1999 book | Access claimed 524 birth dates and 38 scores, all tested outcomes, omitted standard deviations and selection procedure. |
| 3 | Tarvainen, *Correlation* 32(1), 33–46 (2018) | Polarity weights, shuffled Gauquelin controls, subgroup effects and birth-time provenance. |
| 4 | Oshop & Foss, *Journal of Scientific Exploration* 29(1), 9–34 (2015) | Exact 1st/6th Jyotisha rule, navamsha, control-generation and celebrity selection. |
| 5 | Harvey, *Astrological Journal* 14(4), 19–21 (1972); Allen original and Addey 1971 | Father Moon-sign/child-sex replication chain, lost degree counts and moving averages. |
| 6 | Tiggle MA thesis (1976), then Tiggle & Fiebert *Perceptual and Motor Skills* 49, 858 (1979) | Exact hostility/aspect/house score, orb weights, sex split and multiplicity. |
| 7 | Noonan, *Journal of Research of the AFA* 3(1), 17–26 (1986) | Striking reported commander-chart rank match with internally inconsistent ranks and N. |
| 8 | Michelson et al., *CAO Times* 3(1), 21–23; 3(2), 9–13 (1977) | Retrieve alleged out-of-sample neonatal replication, full candidate-feature universe, corrected contingency. |
| 9 | Schwartz (2015) original blog and associated Facebook corpus analysis | Large unconstrained phenotype test; precise multiple-testing, traits, age and sign-confound controls. |
| 10 | Castille, CURA “A link between birth and death” original tables | Huge birthday/same-sign signal; separate birthday behavior from angular sign association. |

## Constraints for coordinator

- Preserve original claims even when the review's criticism is persuasive; this extraction does not adjudicate truth.
- Case-only counts need time/place/stratum-matched birth frequencies and orbital-duration correction. Clock-time features also need documented birth-time quality.
- Treat any sign-belief/self-rating effect with sign familiarity, cueing, desirability, and interviewer leakage as measured confounders. Several studies experimentally or by stratification show these matter.
- Any sign, house, angle, aspect, orb or harmonic feature from an A record remains a **candidate for full-text audit**, not a validated algorithm coefficient. The 16° sign link, the 4°/8° hostility aspects, 10°/15° angularity changes, 12th-harmonic orbs, and Venus/Mars relationship patterns require exact preregistered definitions and untouched datasets.
- Some historical vignettes and theoretical notes were assigned D; they are recorded for complete page coverage and can be excluded from quantitative synthesis.
