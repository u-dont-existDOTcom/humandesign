# CF-005 source-table arithmetic replay

Date: 2026-09-29. Scope: **existing-source development arithmetic, conditional on the printed counts**. No independent people, matched controls, new human observations, prospective outcome data, source-model repair or clinical inference were added.

## Source and executable record

Original: Daigno, *Correlation* **38(2)** (2026), pp. 13–28, Tables 3–6 and appendices C.2/D.2. Owner-held complete issue PDF `/home/joel/Documents/astrology/correlations journal/2026 Vol 38 02 c20263802.pdf`, SHA-256 `5d6a87dc0e5aff058d007a66b2104035a27b639a566fa078ab1e0539d7af1024`. The local issue was inspected directly. The paid PDF and its extracted text are not redistributed.

Run `python scripts/empirical_astrology/reproduce_cf005_tables_20260929.py --output reference/empirical_astrology/cf005_source_replay_20260929.json`. The script transcribes all 16 aspect rows with observed event counts, event opportunities, calendar/control counts and printed one-sided p-values; it asserts their exact-binomial arithmetic and the printed eight-comparison threshold. It separately checks both whole-cohort and all six period-partition two-proportion calculations. This is a replay of a **conditional numerical procedure**, not an endorsement of its independence assumptions or control selection.

| Printed test family | Event/opportunity counts | Control event/opportunity counts | Conditional aggregate z | Conditional one-sided p | Outcome visible in the source |
|---|---:|---:|---:|---:|---|
| French cases, eight aspects pooled | 73/517 | 3555/37425 | 3.5485 | .000194 | Aggregate positive under the paper's event-opportunity comparison. |
| Serial cases, eight aspects pooled | 101/630 | 6241/64496 | 5.3543 | about 4.3×10⁻⁸ | Aggregate positive under the same calculation. |
| French, final temporal third (1894–1930) | 23/197 | 3034/30506 | .8081 | .210 | Failed temporal subset; retained. |

Using the paper's .00625 threshold within each eight-aspect table, French **Mercury conjunct Mars** passes (.00231); serial **Mercury conjunct Mars** (.00010) and **Venus conjunct Mars** (.00309) pass. These are the *reported, conditionally computed* within-table results. Some temporal conjunction rows fail: French Mercury conjunction reported p=.15124 and .44856 in later thirds; serial reported p=.05906 and .76209 in the first two thirds. The per-cell counts for those conjunction-by-period rows are embedded in figure/raster tables and were **not** transcribed into the executable dataset, so those particular p-values are explicitly reported, not reproduced. The six pooled temporal partitions, including failures, are included in the JSON.

## Reproduction boundary

The event opportunities and aspect hits can recur within a person; the two reported denominators are not independent person counts. Calendar-day ephemeris/control events and shuffled planet components do not supply matched human controls. The issue does not deliver immutable individual-case vectors with repeated-event links, the frozen 2026 Wikidata person roster/source date and duplicate-exclusion log, or the code/configuration for generating controls. Running its appendix's present-day Wikidata query could produce a different cohort and would not replay its historical analysis. A person-clustered, era/site matched uncertainty calculation, verified overlap against other case series and a correctly specified source null remain unavailable. These limits are preserved from the paid-archive Pro decision; reproducing table arithmetic does **not** turn the reported association into a clinical or individual-risk feature.
