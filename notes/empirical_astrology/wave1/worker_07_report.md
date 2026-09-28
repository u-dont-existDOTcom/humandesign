# Worker W07 report — Personality B, book pp. 573–618

Source read in full for the assigned range: Dean, Mather, Nias & Smit (2022), *Understanding Astrology*, UA-3. The extraction starts with the portion of 7.6.1986.2 printed on book page 573 and stops at the end of book page 618. Section 7.6.2017.1 continues on page 619; material after the assigned boundary was not extracted.

## Coverage and counts

- Numbered UA sections covered: **36** (7.6.1986.2 through the assigned-page portion of 7.6.2017.1).
- Study-level sources represented: **61 unique citation strings**. This includes separately cited replications, reanalyses, validation studies, and comparator studies embedded in the UA commentary.
- Feature-level JSONL records: **130**.
- Full-text priorities: **A 91, B 30, C 4, D 5**.
- Result directions: **positive 51, null 50, opposite 13, mixed 12, unclear 3, nonempirical 1**.
- Likely reused datasets: **11 records flagged**, representing **6 underlying dataset families** after obvious label consolidation:
  1. Gauquelin professional datasets;
  2. Gauquelin 1966 heredity parent-child data;
  3. Gauquelin second heredity/married-couple data;
  4. Dean 1985 extreme-E/N data reused by Currey;
  5. Astro-Databank plus overlapping web-compiled serial-killer cases;
  6. David Hollins's 1915 horse-chart collection reused by de Thun.

Counts were computed directly from `worker_07_studies.jsonl`. Every record contains all 38 required schema fields; unavailable values are JSON `null`.

## Extraction decisions

- Multi-part studies were split when they tested independently meaningful outcomes, predictors, stages, subgroups, or replications. Examples include Carlson's three tests and later reanalysis, Niehenke's age/self-attribution corrections and specific aspect claims, Fuzeau-Braesch's twins plus audit and replication, and Ruis's timed versus untimed serial-killer samples.
- Original findings and UA criticism are kept separate. A positive `original_reported_result` can therefore coexist with a `ua_interpretation` that treats the result as confounded or unreplicated.
- Embedded non-astrology studies were retained only where they materially validate an outcome, reveal an artifact, or provide a research-design comparator. Purely methodological/nonempirical material is priority D.
- Exact quantitative details were transcribed where printed: sample sizes, counts, means/SDs, orbs, effect sizes, p-values, confidence thresholds, and replication statistics.
- Two source inconsistencies are explicitly flagged in `extraction_notes`: Chester-Lambert is described as N=69 while the printed table totals N=71; Mayer-Garms is described as 117 questionnaire respondents while the results heading uses N=137.

## Highest-value constraints and candidate signals

The strongest recurring constraints for an optimized empirical model are:

1. Whole-chart readings repeatedly failed blinded identity matching even with experienced astrologers, rich case files, documented times, or consensus groups.
2. Validated psychological profiles can be self-recognized, so a failed astrology match cannot always be dismissed as an impossible criterion.
3. Sun-sign knowledge/self-attribution and slow-planet birth-cohort effects can create small but highly significant personality correlations.
4. Flexible orbs, uncorrected multiplicity, post-hoc endpoints, dependent predictors, and rule stacking repeatedly turned noise into apparent signal.
5. Confidence, experience, and analyst consensus generally did not calibrate to correctness.
6. Relationship work needs independent partner responses, age/cohort-matched controls, fixed decoys, and explicit treatment of slow-planet aspects.
7. Interesting positives requiring original-text audit and independent replication include the shrinking Mars-rising/red-hair series, angular Sun/Jupiter with coded puppy dominance, the timed-sample Mutable-sign serial-killer excess, and the small Mars/Jupiter/Saturn sector score. None is ready for algorithm use from the review alone.

## Top 10 original sources to retrieve next

1. **Peter Niehenke, *Kritische Astrologie* (1987), plus APP 2(3), 10–15 (1984).** Largest and most technically informative personality dataset in the range; needed for exact questionnaire mappings, age correction, aspect definitions, split-half results, and raw effect tables.
2. **Shawn Carlson, “A double-blind test of astrology,” *Nature* 318, 419–425 (1985).** Foundational whole-chart/CPI design; retrieve with appendices or correspondence if available for complete randomization, rating, and attrition details.
3. **John McGrew and Richard McFall, *Correlation* 11(2), 2–10 (1992).** High-information collaborative matching test with excellent recorded times and extensive open-ended case files.
4. **Suitbert Ertel and Geoffrey Dean, *Personality and Individual Differences* 21(3), 449–454 (1996), together with Fuzeau-Braesch's 1992 original.** Essential audit trail for the 68.5% twin claim, 42 discrepancies, deterministic rescoring, and the O'Neill replication.
5. **Bernadette Brady, “The Australian parent-child research project,” *Correlation* 20(2), 4–38 (2002).** Needed for all 338 tests, exact control generation, rulership definitions, Moon-nodding calculations, and corrected statistics.
6. **Gerhard Mayer and Martin Garms, *Journal of Scientific Exploration* 26(4), 825–853 (2012).** Strong replication-oriented synastry design; retrieve exact sample Ns, simulation procedures, all z scores, and split-half tables.
7. **S. Fuzeau-Braesch and J.-B. Denis, *Journal of Scientific Exploration* 21(2), 281–293 (2007).** Retrieve coding protocol and dog-level/litter-level data to test the angular-Sun/Jupiter dominance result under blinded coding and clustered inference.
8. **Jan Ruis, *Correlation* 25(2), 7–44 (2007) and 28(2), 8–27 (2012).** Needed to reconstruct the 13 hypotheses, control simulations, timed/untimed overlap, all misses, and multiplicity.
9. **Kyösti Tarvainen, both papers in *Correlation* 28(1), 5–24 and 25–43 (2012).** Needed for statement-level Handbook mappings, professional-group results, composite definitions, and exact shuffled controls.
10. **Wyman and Vyse, *Journal of General Psychology* 135(3), 287–300 (2008).** Important Carlson near-replication and clean non-astrology positive control; retrieve exact Solar Fire templates, decoy assignment, ratings, and sun-sign-knowledge analysis.

## Coordinator cautions

- Do not count embedded validations or reanalyses as independent natal datasets when they reuse Carlson, Gauquelin, Dean, Fuzeau-Braesch, or other named source data.
- Do not pool subjective reading satisfaction with blinded predictive accuracy.
- Do not treat the 51 positive-direction records as 51 supportive studies: many are control validations, belief/artifact effects, post-hoc reanalyses, or positives that shrink/fail on replication.
- Preserve the page-boundary note for 7.6.2017.1 during merge so W07 and W08 do not silently duplicate the continuation on page 619.
