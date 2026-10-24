# Lilly Naibod: original 1647 photographic-source corrections

Research checkpoint: 24 October 2026. Parent goal remains open: build reliable, separately sourced historical astrology calculations for future combined, prospective blinded testing.

## Original witness inspected

Public-domain page photographs of William Lilly's Christian Astrology, printed 1647, pp. 713, 714 and 715. Wikimedia Commons original-volume entry:

https://commons.wikimedia.org/wiki/File:Christian_Astrology_%28IA_ca-william-lilly%29.pdf

The image files correspond to PDF scan image pages 735-737 (1-based) and are in facsimile_pages/ with SHA-256 recorded in ORIGINAL_1647_SOURCE_COMPARISON.json. The digitization and arithmetic of a separate WorldAstrology 2003 re-typeset version remain unchanged in the parent branch; their provenance and source anomalies must not be merged.

## Correction 1: degree-table year carry at 69

Original printed p.713 visibly reads:

| Equatorial arc | 1647 YEARS | 1647 DAYS | 1647 HOURS | 2003 retype YEARS |
|---|---:|---:|---:|---:|
| 68° | 68 | 364 | 0 | 68 |
| 69° | 70 | 4 | 3 | 69 |
| 70° | 71 | 9 | 11 | 70 |
| 80° | 81 | 62 | 24 | 80 |
| 90° | 91 | 116 | 13 | 90 |

Across degree rows 69 through 90, the original year's column is one greater than the degree label. These 22 year values were lost in the modern 2003 retypesetting. The apparent missing carried year of the earlier audit is thus a 2003 witness defect, not a demonstrated flaw in Lilly's first-edition table.

The new diagnostic code independently corrects ONLY the photographically verified 1647 YEARS column. Its day/hour values are reused from the 2003 transcription with selected spot-checks against the original. No exhaustive original day/hour-cell collation is claimed.

## Correction 2: 19°52′ worked example

The original printed p.715 takes 19 years and 422 days and 21 hours, carries 365 days into one year, and explicitly concludes TWENTY years, 57 days and 21 hours. The 2003 retypesetting concludes 22 years, two years too high relative to the worked arithmetic. This discrepancy does NOT originate in the original Lilly conclusion. The other worked example (11°55′) agrees across both witnesses at 12 years, 33 days and 14 hours.

## Shared abnormalities retained

The minute-table page 714 in the original scan also omits the printed row 27′, shows 8′=44d10h (anomalous between 7′=43d6h and 9′=55d14h), and shows 60′=374d14h (inconsistent with the one-degree entry if 365 days make a year). Degree-table p.713 prints 24 hours in the 80° row. These are observed anomalies, not inferred corrections. The minute-44′ hour glyph is faint in this page photograph; a higher-resolution or independent witness is needed to certify that cell.

## Source comparison files

- naibod_original_1647.py — strict first-edition year-column comparison and arithmetic diagnostic, preserving the separate 2003 witness and missing minute-27 cell.
- YEAR_COLUMN_1647_VS_2003.csv — 90 degree-year rows, with 22 verified corrections and source-caveat fields.
- SELECTED_EXAMPLE_COMPARISONS.json — six selected source comparisons.
- ORIGINAL_1647_SOURCE_COMPARISON.json — audit receipts, three photo hashes, source and unresolved questions.
- facsimile_pages — 3 public-domain 1647 page images; no substantial modern-retypeset pages copied here.
- tests/unit/test_naibod_original_1647.py — original-versus-retyped year values, example conclusion, evidence hashes, and unchanged previous data.

The source comparison is NOT registered as a continuous primary-direction time key, and is not enabled as a default for the event/timeline engine. Modern time-key constants and all earlier geometric profiles remain unchanged.

## How to run on Zorin

Persistent research checkout:

    $HOME/Documents/astrology/gansten-lilly-original-1647-engine

From that checkout:

    export PYTHONPATH="$PWD/src"
    $HOME/humandesign/.venv/bin/python -m hdmatch.astrology.naibod_original_1647 --degrees 69 --minutes 0

The original comparison reports 70y4d3h for 69°0′; the 2003 witness reports 69y4d3h. For 19°52′ both tables calculate 20y57d21h, while only the 2003 final prose disagrees. The minute-27 row still returns an explicit error rather than made-up data.

## Current research boundary

The three 1647 photo pages, core source-comparison claims and SHA-256 checks have been verified. Other cells were only spot-checked; the original full table is not yet a diplomatic transcription. Formal witness differences, geometric engine correctness, and out-of-sample predictive validity remain three separate evidence categories.

Next: independent cell-by-cell collation for all minute and day/hour entries using clearer first-edition sources, then a separately sourced Brahe birth-date solar right-ascension key and Placidus cumulative true-solar right-ascension key, preserving different conventions. No human natal outcomes used for selection.
