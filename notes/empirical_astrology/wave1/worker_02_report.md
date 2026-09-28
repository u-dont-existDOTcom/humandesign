# Worker W02 — application issues A

**Scope:** Dean, Mather, Nias & Smit (2022), *Understanding Astrology*, UA-2 PDF, book pages **273–329 inclusive** (PDF pages 78–134). Read all 57 assigned pages directly, including page images for graphs with non-extractable labels. Section 7.2.1957.1 starts on book p.272, so this file extracts only its continuation on pp.273–274. Section 7.2.1993.2 begins on p.329 and continues in W03's range; only its p.329 setup is recorded here. Every one of the 53 section headings intersecting this range has at least one audit record, including D records where the section is not a new empirical study.

## Counts

| Measure | W02 count |
|---|---:|
| Distinct citation strings / provisional study-level sources | 97 |
| Feature-level JSONL records | 107 |
| Priority A / B / C / D | 41 / 45 / 7 / 14 |
| Direction positive / null / opposite / mixed / unclear / nonempirical | 20 / 37 / 10 / 14 / 3 / 23 |
| Records explicitly annotated for reuse, overlap, or separation | 26 |

The 97 figure counts distinct `citation_raw` strings, **not** 97 independent experiments or datasets: some strings group several cited works, and several different publications use one cohort. The direction categories report what is described in this range, including non-astrological analogies (Tarot, palmistry, graphology) that illuminate methodology. They are not vote counts about whether astrology works. A priority means retrieve the original before algorithm use; it does not mean the result supports astrology.

## Findings and high-risk interpretation traps

- **Strong-looking result selected away in replication:** Heukelom's four-profession test had seven of 19 astrologers match all four preselected charts (chance expectation 0.8), then zero of 17 did so on a new unselected four-chart set. The second paper did not retain the complete hit distribution. Treat the first and second panels as distinct chart sets but overlapping astrologers.
- **Apparent medical signal disappeared after testing multiplicity:** Pounds screened 250 timed hospital-confirmed hypoglycemia cases against 1,500 controls on many chart dimensions. Saturn hemisphere produced unadjusted p=.002 (continuity-corrected .003) and am/pm p=.02, but the review reports no significance after correction. The author's intended Venus/Jupiter/Mars/outer-planet signature did not emerge.
- **Reversed interpretations were accepted:** Dean's 11 authentic-chart clients accepted 250/261 designated aspect meanings (96%); 11 different volunteers given opposite-pattern charts accepted 207/214 (97%). The groups differed in recruitment and the astrologer knew condition. This is a control on personal validation, not a randomized estimate of aspect effect. The 1984 counselling pilot mention appears to reuse these same 22 people; do not sum cohorts.
- **Prenatal epoch rectification:** Hone, Tarvainen and additional direct checks offer quantitative failures or no precision gain. Tarvainen reports average 18-minute errors in three timing sets and only 28 eligible times in a hypothetical 1,440-minute birth day. Marr's event-contact orb histogram has no zero-orb peak. The epoch discussion starts before W02's page boundary, so W01's last page may contain additional background.
- **Jonas fertility and sex claims:** Positive 98.5%/94%/87% claims lacked accessible original data in the review. Kimball–Kautz (500 selected women, 400 with child sex), Christilles (3,650 timed births, indirect birth-Moon proxy), Tarvainen (37,947 Gauquelin mothers) and fraternal-twin logic offer distinct checks with distinct timing limitations. Tarvainen's r around .001 must not be mistaken for a practically large effect just because the dataset makes small values significant. None of this licenses reproductive guidance.
- **Fixed stars and houses:** Jay's 1,000-chart fixed-star study reports selected qualitative confirmations without controls or probability calculations; exact magnitude/latitude/orb rules are extracted. Tarvainen's Finnish house comparison used 93 of ~500 members and separate student samples (18 and 11). Its p.329 graphic supplies only approximate bar heights, not exact counts; the JSONL labels them as estimates. Neither exercise is a blinded behavioral comparison of house systems.
- **Other reference standards:** The Montana study's published first/second/third count for 12 readers prints 4/7/2, which sums to 13; the review suspects 4/6/2. Do not repair it silently. Grange's unpublished four-way comparison supplies a personality-test/Barnum/graphology baseline against an astrological reading. The Martindales' element–temperament effects concern semantics and poetry, not birth charts.

## Likely dataset reuse and overlap

1. Gauquelin heredity mothers in Tarvainen 2014 may recur in other workers' Gauquelin sections.
2. Dean's 22 authentic/reversed consultation subjects appear in the 1984 pilot, the 1977.2 cross-reference and the full 1987.4 account. The two subsequently switched clients and earlier 44 mail raters are separate examples.
3. Gouchon's four midpoint pairs share the same 21 plane-crash subjects; his 21,700 death transits are another table with provenance unknown.
4. Pounds's broad screen and Saturn finding share the same 250 cases and 1,500 controls.
5. Cummings et al.'s blind matching and later counselling share twelve participants; its 220-person survey is a separate sample.
6. Heukelom's two profession-chart rounds share astrologer recruitment, with different chart sets.
7. Boot and Sietsma debate the same two house-sale horary examples, not new replications.
8. Neher's Tarot results are described in both 1986.2 and 1990.2. Blackmore's original and two replication cohorts are distinct.
9. Tarvainen's Finnish 93 respondents provide both cusp and planet judgments; the student groups are separate.
10. Kimball–Kautz's 400 offspring-sex cases are nested in their selected 500-person fertility material.

## Ten originals for coordinator acquisition

Rank reflects impact on model decisions and the risk of misreading summary-only evidence. Closely linked reports are shown together but must be counted as distinct publications on acquisition.

| Rank | Original source | What the original must resolve |
|---:|---|---|
| 1 | Wout Heukelom, *Tijdschrift Astrologie* 2(2), 12 (1978) **and** 3(1), 24–25 (1979) | Preselection, chart provenance, all second-round hits. |
| 2 | F Sims Pounds Jr, *Seventy-Five Windows* (1978) | Full testing family, Saturn counts, control construction, predeclared hypothesis. |
| 3 | Geoffrey Dean, *Skeptical Inquirer* 11(3), 257–266 (1987), plus accessible notes | Recruitment, reverse-chart construction, item-level data and the 1984 duplicate. |
| 4 | Kyösti Tarvainen, *APP* 9(1), 26–28 (1993) | Prenatal-epoch algorithm, 85/460 cases, randomized-time control, interval errors. |
| 5 | Eugen Jonas (ed.), *Chapters of Scientific Astrology* (1969) and original 100-case sex trials, if locatable | Whether reported 94/87% trials, dates and raw records exist; avoid promotional retellings. |
| 6 | Kimball & Kautz, unpublished California work (1974–1977), if locatable | Selection from questionnaires/abortions, actual conception timing, angle statistics, child-sex counts. |
| 7 | Kyösti Tarvainen, *NCGR Research Journal* 4, 23–32 (2014) | Gauquelin-mother reuse, circular phase statistics, pregnancy-error simulation and r curve. |
| 8 | Felix Jay, *Astrological Journal* 27(3), 140–144; 27(4), 207–214 (1985) | Fixed-star catalogue, outcome coding, inclusion rule, multiple comparisons, apparent declination inconsistency. |
| 9 | Mary Cummings et al., *Kosmos* 8(2), 5–26 (1978) | Resolve impossible 4/7/2 ranking and ascertain independence of interpretations. |
| 10 | Graham Tyson, *Personality and Individual Differences* 5(2), 247–250 (1984) | Five-way matching and independent personality score covariance. |

**Additional A queue:** Blackmore 1983 on three Tarot matching samples; Grange 1982 (unpublished) on four-way ranking; Christilles 1973; Martindale 1988 for semantic controls; Tarvainen 1992 Finland house questionnaire; original Gauquelin/Sadoul 1972 blind Astroflash test. Search for originals can adjust priority but should not transform missing denominators into estimates.

## Method and limits

All records cite the UA-2 review and preserve its original-study report separately from `ua_interpretation` and `ua_criticism`. `source` duplicates the full raw citation when the review does not identify a distinct bibliographic field; `source_type` is a coarse format classification. Null means the review did not provide the information. Exact numerical details from p.329 and the Ivtzan p.302 graphic were visually inspected; p.329 bar heights remain explicitly approximate. No original study full text was consulted or independently verified in this wave. Several old proceedings, unpublished data and personal communications may not be recoverable. The files are an acquisition map and extraction corpus, not an optimized algorithm or evidence synthesis.
