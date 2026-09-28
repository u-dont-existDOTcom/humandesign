# Worker W06 report — Personality A, book pages 527–572

## Scope and completion

I read the complete assigned range of Dean, Mather, Nias & Smit (2022), *Understanding Astrology*, directly from UA-3, book pages 527 through 572 inclusive. The extraction starts with section 7.6.1932.1 and includes all material printed through page 572 of section 7.6.1986.2.

The Shawn Carlson section begins on page 572 and continues into W07's range. W06 records only the subject-reading and same-Sun-sign control results actually printed on page 572, with an explicit continuation note; it does not pre-empt pages 573 onward.

## Counts

- Study-level source citations represented: **70** distinct citation strings.
- Feature-level JSONL records: **104**.
- Sections covered: **39**.
- Full-text priorities: **A 74**, **B 20**, **C 7**, **D 3**.
- Result directions: **positive 23**, **null 53**, **opposite 9**, **mixed 14**.
- Additional direction labels required for faithful extraction: **unclear 3**, **nonempirical 2**.
- Records flagged as involving a reused, split, reanalysed, or repeatedly reported dataset: **73**.

“Positive” above means only that the original report described a positive result. It does not incorporate Dean et al.'s criticism, which is stored separately. Many positive records are post-hoc, multiplicity-inflated, or nonreplicating.

## Likely reused or linked datasets

The following reuse/linkage groups were identified. Several groups generate multiple feature-level rows, so the list is shorter than the 73 flagged records.

1. Korsch/Koralle four-chart experiment: character, events, and control comparisons.
2. Jung's 483 marriages: N=180 pilot, N=220 and N=83 internal replications, and Tsutakawa multiplicity reanalysis.
3. Jylha's 430 marriages: transit-house and progressed-Moon analyses.
4. Noblitt's 155-student derivation sample and 91-student holdout.
5. Scully's 35 married couples and their random rematches: aspects and house overlays.
6. Claws's four-generation family and 18-person control: position and aspect comparisons.
7. Dean/Hedgcock's 102 analyzed volunteers: hand dimensions, element classification, independence, and chart/hand analyses.
8. Startup's 31-chart planetary-strength sample: trait tests, astrologer agreement, and E correlations.
9. Kranz's 60 subjects: personality and interest inventories; Shaban is a separate small analogue.
10. Oram's 59 mediums: original result, 30/29 split, non-medium controls, and 1,096 generated controls.
11. Gaynor's 54 timed charts: psychometric convergence and three-astrologer comparison.
12. Urban-Lurain's alcoholism data: 53 alcoholics, 217 derivation controls, and 230 additional controls.
13. Parker's 100 alcoholics/100 controls: original scan, corrected reanalysis, and random-chart calibration.
14. Pierce's 269 astrologers: pairwise symbolic similarity and factor analysis.
15. Startup's 66 astrologers and matched psychology-student comparisons: EPQ and 16PF analyses.
16. Bollen/Gauquelin heredity chain: selected family findings and the much larger 1966/1984 Gauquelin comparison.
17. Shanks's 960 couples drawn from Gauquelin's first heredity dataset, linked to the Jung/Müller replication chain.
18. Startup's 911 timed subjects: seven separately extracted aspect, harmonic, sector, and sign result families.
19. Ferguson's 1,043 dancers and 510 controls: nominated factors, discovered factors, and midpoint comparison.
20. López's 191 MMPI subjects: sign-related and aspect discriminant scans.
21. Dean's E/N program: 1,198-person parent pool, 288 extreme scorers, 160 whole-chart cases, and repeated feature/moderator analyses.
22. Guttman's 251 couples: 106 long-term and 145 short-term groups with rematched controls.
23. Black's 20 assault cases and Davis's separate 20-case attempted replication.
24. Marbell et al.'s 24 office workers across three small tests.
25. Carlson's interpretation set: 83 usable test-subject responses and 94 same-sign control responses on page 572.

## Main extraction-level conclusions

The range is dominated by null or failed-replication evidence once multiplicity, controls, or holdouts are introduced. Especially consequential results for later algorithm work are:

- Whole-chart E/N judgments by 45 astrologers were at chance despite extreme phenotypes, extensive practitioner freedom, and 10,800 chart judgments; experience, confidence, intuition, technique, and better birth data did not rescue performance.
- Startup's 911-subject program found no reliable aspect evidence across traditional directions, hard/soft classes, 108th-harmonic peaks, or 15-degree bins. Its few diurnal-sector/Gauquelin hints need exact-source retrieval before use.
- Dean's two-set extreme-E/N study found the high in-sample multivariate accuracy did not replicate; the only repeatable individual-factor signal was Sun-sign/extraversion in samples already vulnerable to self-attribution.
- Noblitt's best stepwise equations reversed or collapsed on an independent 91-person sample.
- Jung-style marriage contacts failed in Jung's own internal comparisons and in the larger Müller and Shanks replications.
- High-dimensional relationship, alcoholism, mediumship, occupation, trauma, and family-heredity searches repeatedly produced nominal peaks that disappeared under valid controls or replication.
- Barnum, authority-cue, and self-attribution studies show why personal acceptance of a reading cannot be treated as criterion validity.

## Top 10 original sources to retrieve next

1. **Geoffrey Dean (1985), “Can astrology predict E and N? The whole chart,” Correlation 5(2), 2–24.** Highest-value whole-chart test; obtain complete tables, judgment files if extant, exact control construction, dependence structure, and astrologer metadata.
2. **Michael Startup (1984), PhD thesis, *The Validity of Astrological Theory as Applied to Personality*.** Large N=911 and multiple preregistered/elicited feature families; exact three repeated Gauquelin effects and Sun-sector result are missing from the review excerpt.
3. **Geoffrey Dean (1985), “Can astrology predict E and N? Individual factors,” Correlation 5(1), 3–17.** Needed for exact factor definitions, replicate-set construction, all 132 tests, and multivariate selection details.
4. **JR Noblitt (1978), PhD thesis, *Celestial Concomitants of Human Behaviour*.** Contains the full 313-regression universe and independent 91-person follow-up, ideal for a clean overfitting/replication audit.
5. **Ulrike Kranz (1980), PhD thesis on astrologer-generated personality and interest inventories.** Needed for all per-scale correlations, belief/sign-knowledge moderator analyses, and exact astrologer-pair assignments.
6. **Shawn Carlson (1985), “A double-blind test of astrology,” Nature 318, 419–425, plus appendices/correspondence.** W06 captures only page-572 results; full protocol and later critiques are mandatory for interpreting this landmark study.
7. **CG Jung (1952/1960), “An astrological experiment,” together with RK Tsutakawa (1957) and the later Correlation reanalyses.** Needed to reconstruct all 50 contacts, three batches, sampling provenance, exact orb handling, and multiplicity.
8. **Geoffrey Dean and Ronald Hedgcock (1979/1980), “The elements vs psychology, astrology and palmistry,” Parts 1–2.** Provides exact element operationalization and raw morphology/EPI relations; relevant mainly as a constraint on element semantics and proxy validity.
9. **Graham Tyson (1979), PhD thesis, *The Social Psychology of Belief in Astrology*.** Combines large Sun-sign/career and personality nulls with blind matching, astrologer-rating, belief, and stress-selection analyses.
10. **Frances Scully (1978), Masters thesis, *Planetary position and marital status*.** Exact relationship-aspect and house-overlay tables with documented birth-time provenance and randomized controls; useful for modern permutation reanalysis.

Near-next tier: Gaynor 1981, Urban-Lurain 1981, Parker 1982 plus Dean's 1985 reanalysis, Pierce 1982 unpublished results, Ferguson 1984, López 1984, Guttman 1985, Black 1985/Davis 1978, and Marbell et al. 1986–87.

## Quality and boundary notes

- Every JSONL object contains every required schema field; unavailable values are `null`.
- Exact printed Ns, orbs, p-values, correlations, counts, and comparison groups were retained wherever the assigned pages supplied them.
- Original reported results, review interpretation, and review criticism are separate fields.
- Empirical analogues involving palmistry, graphology, and dowsing were retained because they are discrete studies inside the assigned range and directly inform control design; they are marked peripheral (`B`/`C`) rather than silently omitted.
- Traditional aphorisms and the rare-gift prevalence paper are retained as `D`/nonempirical methodological records so the section coverage remains auditable.
- No attempt was made to optimize an astrology algorithm or adjudicate whether astrology is true.
