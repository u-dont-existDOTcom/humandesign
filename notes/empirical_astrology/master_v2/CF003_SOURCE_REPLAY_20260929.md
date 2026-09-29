# CF-003 source replay: adjusted planetary dominance

Date: 2026-09-29. Scope: reproduce mechanically available source arithmetic and inventory the data needed for the **chart-conditioned target** and correct null. This is development/source replay, not new human validation, model activation or a Pro decision. The frozen Pro files are untouched.

## Originals and source inventory

| Item | Original and locally checked SHA-256 | Usable content |
| --- | --- | --- |
| Discovery/training | Godbout & Coron, *Correlation* 35(2), 2023, pp.11–29; `2023 Vol 35 02 c20233502v2.pdf`; `780b8422d77059892b57c395d9cf3c2b40f828706b0c2ed51a7bcabb0b03aac6` | Methods, seven factors, illustrated six-row training extract (Table 9), aggregate three-cell Table 10; **not** all 189 person records. |
| Person-disjoint replication | Godbout & Coron, *Correlation* 36(1), 2023, pp.49–60; `2023 Vol 36 01 c20233601.pdf`; `a4c0da056639aa0833dd96229a4efc3817395729b26c361875f24322f5092f44` | Names of all 61 (Table 1, p.50), aggregate nine-cell Tables 2–4 (pp.51–52); **not** 61 chart portraits, per-person outcomes or nine individual success vectors. |
| Reused comparison | Godbout, *Correlation* 36(2), 2024, pp.33–48; `2024 Vol 36 02 c20243602.pdf`; `d50048c5a6f34c06ef6eaa0cc77439243c55137c514149d8f09b304d5862195d` | Appendix Figure 5, p.46, prints **all 250 names and each first biographical dominant**; that is one rank per person, not the ten portrait score vectors, higher biographical ranks, or APD predictions. Article states 250=prior 189+61; not an independent cohort. |
| CF-004 overlap comparator | Godbout & Brun, *Correlation* 38(1), issue PDF dated 2026; `2026 Vol 38 01c20263801.pdf`; `e3ad72ee69c213ebe79739c025c91357fd7c112eefc8468bbdb43911ee9e8e73` | Figure 2, p.42, names all 68 southern participants. The 73 northern Le Monde cases are reported reuse of the earlier Godbout sample. |

The owner-provided `/home/joel/Documents/astrology/correlations journal/` directory (including a depth-3 check) contains journal PDFs only; it has no CSV, XLS/XLSX, ZIP, software executable, word lists or supplemental export. This finding concerns the inspected directory, **not** an assertion that authors never retained data. The [publisher’s training abstract](https://correlationjournal.com/a-model-for-planetary-dominanceconvincing-evidence-from-biographical-analysis/) and [replication abstract](https://correlationjournal.com/replication-of-the-adjusted-planetary-dominance-model-testing-an-independent-sample-of-61-biographies/) expose no person-level supplements. No purchase or author contact occurred; no paid PDFs were copied into Git.

## Exact pipeline specified in the originals, and its reproducibility limits

1. Training N=189 comprises 73 *Le Monde* profiles reused from Godbout 2020 plus 116 other notable persons (original paper pp.12–13). An endnote also mentions **22 acquaintances** answering a personality-keyword questionnaire, but their relationship to the 189 and whether their outcome construction differed from the cited biographies is not mapped in a complete roster; this is an unresolved source detail, alongside processing chronology, birth-record precision and exclusions. Replication N=61 uses A-initial Astrodatabank names with Rodden AA/A birth times and excludes times ending `xx:00` (36(1) p.50); the article explicitly says these are distinct from training 189. The 2024 N=250 comparison recombines them.
2. Extract biography words from Wikipedia/Britannica/Universalis or the cited profiles; the paper describes 6,000–35,000 words per biography, a Biographical Word Extractor and thesaurus-based removal of ambiguous terms (35(2) pp.16–18). Nearly half the initially extracted words are said to be unsuitable. Neither the complete biographies/version dates nor the cleaning thesaurus and selected word lists are supplied for 189/61.
3. For **each person's actual chart**, duplicate one candidate planet twice in Mastro Expert to triple that planet's interpretive presence, generating ten distinct chart-conditioned word-score portraits (35(2) pp.18–21). For each candidate planet, sum scores of chart-generated words found in the person's cleaned biography and divide by the score sum of all that planet's chart words (p.21). Rank all ten normalized scores; this is the **biographical target**. Chart, software, dictionary and settings are therefore needed even to recalculate the target for a wrong biography. Published examples and 2024 first-rank symbols are not a substitute for the full 250 × 10 scores/denominators, ties and word profiles.
4. Discovery screened 42 chart factors, retained 18 and fitted seven weights using Excel Solver to maximize matches against these very training targets (35(2) pp.21–24). Seven published contributions: major aspect to Moon 8.3; ≥5 major aspects 8.2; modern Ascendant ruler 7.6; planet in Placidus XII 5.3; modern Descendant ruler 5.2; major aspect to Ascendant 4.7; within ±5° of Placidus IX center 1.9. Major aspect types 0/60/90/120/180°, and endnote 4 gives nominal orbs for aspect classes; the exact Mastro version, factor code, solver configuration, ties, records of what was fixed before N=61, software outputs and all input charts are absent. A new implementation with inferred settings would **depart** from the published pipeline.
5. The 61-person replication evaluates nine combinations of top 1/2/3 biography ranks × 1/2/3 APD prediction tries. It uses chance proportions from 30,000 **shuffles of completed** training targets/predictions, then a one-sided normal-tail test in N=61. These nine sums refer to one repeated sample; no joint per-person statistic or assignment-respecting null is published.

## Independent printed-table arithmetic check

Run `python scripts/empirical_astrology/reproduce_cf003_20260929.py` to regenerate `reference/empirical_astrology/cf003_source_replay_20260929.json`. The script is independent of `scripts/correlation_archive_arithmetic_20260929.py`; it recomputes expected counts, z statistics, one-sided normal tails and standardized differences **from the rounded published null proportions**, and asserts that all printed p values agree to within 6% (rounding sensitivity). It never treats p values as calibrated evidence for an astrology effect.

| Biographical rank max | Predictor tries | Reported success / N | Reported chance rate | Expected (rounded) | Reported p |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 13/61 | 10.7% | 6.5 | .00372 |
| 1 | 2 | 24/61 | 20.6% | 12.6 | .000152 |
| 1 | 3 | 29/61 | 31.1% | 19.0 | .00274 |
| 2 | 1 | 23/61 | 21.4% | 13.1 | .000961 |
| 2 | 2 | 39/61 | 39.0% | 23.8 | .0000317 |
| 2 | 3 | 43/61 | 54.6% | 33.3 | .00624 |
| 3 | 1 | 29/61 | 31.9% | 19.4 | .00432 |
| 3 | 2 | 42/61 | 54.8% | 33.4 | .0135 |
| 3 | 3 | 47/61 | 71.8% | 43.8 | .182 **fails .05 even as reported** |

The training article's three printed Table 10 counts are 92, 135 and 158/189 at rank max 3, with null rates .319/.548/.718 and reported p values 3.56×10⁻⁷, 2.08×10⁻⁶ and 1.61×10⁻⁴; the same arithmetic check matches their z and p within the rounding tolerance. Training estimates are **fitted/discovery results**, not validation. This independently reproduces **table arithmetic conditional on printed aggregates**, not the 189/61 persons, underlying 30,000 shuffle values, or the published null-generating computation.

Printed prose differs from the authoritative tables in two additional places: training p.25 describes 158 successes against expected **151.6**, whereas Table 10 p.24 gives expected **135.8** (rounded .718×189=135.702); replication p.53 describes **43.8 successes** against expected **33.3**, whereas Table 4 p.52 gives **47 successes** against expected **43.8**. We retain the original numbers and label the discrepancies; neither mismatch permits back-inference of subject-level results. The 2024 appendix first-rank-only symbols cannot resolve higher rank or ties.

## Actual cross-article overlap check

Direct visual name comparison between 2024 Appendix Figure 5 (250 pooled people), 2023 Table 1 (the 61 test people) and 2026 Figure 2 (68 southern people) finds **at least six printed-name matches**: test 61 = **Salvador Allende; Claudio Arrau**; training 189 = **Raymond Barre; Che Guevara; Xaviera Hollander; Luc Jouret**. The disjoint 61 roster contains A-surname names only, and the last four appear in the pooled 250 appendix, so their prior subcohort is the 189. Machine-readable provenance and limitations appear in `reference/empirical_astrology/correlation_overlap_source_replay_20260929.json`. Alias/transliteration differences, participant IDs and biographies used by each study remain unaudited; six is a verified lower bound, not a definitive all-alias match count. The paper also reports reuse of all 73 northern profiles from the prior 73 *Le Monde* training subset; this is paper-described cohort reuse, not a separate replication.

## Missing inputs and executable boundary

| Proposed reproduction | Current status | Exact missing input |
| --- | --- | --- |
| Printed nine-cell replication and three-cell training **arithmetic** | **Completed**, conditional on paper aggregate counts and rounded null rates. | Exact unrounded null probabilities if byte-level p replication is wanted. |
| 189/61 source-target reconstruction and all nine person-level success vectors | **Blocked by unpublished source exports**, despite public 61 names, 250 first targets and illustrative six-row training table. | Stable IDs, birth records, ten chart-conditioned full Mastro portrait word-score/denominator vectors per person, dated biography texts, cleaning corpus/rules, precise software/settings, complete target ranks/ties and fixed seven-factor score/prediction vectors. |
| Confirmed *full* cross-cohort intersections | **Partial, six exact visual matches.** | Machine-readable 250/141 identifiers, cross-study birth records and alias tables, 73 northern roster, recruitment/version records. |
| Original 30,000 finished-output shuffles | **Cannot replay exactly.** | Original ordered individual predictor/target vectors, algorithm, seed and unrounded draw results. Its replay alone would not correct chart-conditioned coupling. |
| Correct chart/assignment-respecting biography-specific null | **Not executable or declared frozen.** | All stage inputs above plus predeclared exchangeability covariates/strata, statistic for the nine correlated endpoints, ties, draw count/seed. Holding each chart and seven-factor predictor fixed while reassigning complete biography profiles requires **recomputing affected target words and ten chart-specific similarity scores**; shuffling finished target labels is invalid here. |
| Original adaptive training-search null | **Not executable.** | Full 42-to-18-to-seven selection logs, solver configuration and training inputs. This is separate from the fixed 61-person analysis. |

No new feature, weight, validation claim or prospective protocol change follows from this mechanical replay. Report failures and incomplete source states in any subsequent Pro handoff.
