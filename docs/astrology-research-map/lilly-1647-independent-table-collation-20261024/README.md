# Lilly 1647 first-edition Naibod tables: independent photo collation

Date: 24 October 2026. Research-only mathematical/source work. Not proof of astrology's predictive efficacy.

## Immutable parent goal

Reconstruct distinct historically sourced astrology calculations, freeze their rule choices BEFORE participant answers are known, and eventually compare forward-blind predictions jointly against matched controls and decoys. This table audit is a bounded source-correction subtask, not a new mandatory barrier before using other valid systems.

## Two independent 1647 source copies, plus separate modern retype

1. Wellcome Collection, Christian Astrology, 1647, work ID s7z7c46y (https://wellcomecollection.org/works/s7z7c46y), IIIF manifest https://iiif.wellcomecollection.org/presentation/v2/b30338724. Printed pages 713, 714, and 715 correspond to zero-based canvas 747,748,749 (visually reconfirmed from each scanned printed-page header), each 3141 x 4249 pixels. Original JPEG pages with SHA256 hashes are included in facsimile_pages and SOURCE_PROVENANCE.json.
2. Independent Internet Archive original 1647 copy, identifier ca-william-lilly, whose printed page photos 713-715 already appear in prior gansten-lilly-original-1647-20261024.
3. The 2003 WorldAstrology retypesetting, CA-III.pdf, is a THIRD witness and remains unchanged in historical_naibod.py and its earlier CSV. It must not be silently overwritten with the 1647 digits.

Both originals are real photographs of FIRST-EDITION copies, not identical images and not the 2003 retypesetting.

## Complete row-by-row original-versus-retype comparison

LILLY_NAIBOD_1647_WELLCOME_VS_2003_BY_ROW.csv has 152 rows: 90 original degree table rows, 59 physically printed minute labels, one absent minute label 27, plus explicit editorial zero identities.

- All 90 original degree day/hour entries were independently examined and agree with the 2003 retype. Original printed year column at degrees 69-90 is YEAR=DEGREE+1, unlike modern retype YEAR=DEGREE: exactly 22 confirmed original-versus-retype differences.
- **NEW:** 1647 minute row 1' reads **5 days, 4 hours** in BOTH first-edition copies; the modern 2003 retype reads **6 days, 4 hours**. This is a new independently verified one-day source difference. It may be an original printing mistake. We preserve what each witness PRINTS, not what an astronomical progression would predict.
- Original 8'=44 days 10 hours; both witnesses agree on this anomalous number. The 27' row LABEL is missing in both first-edition copies and 2003 retype. Original 60'=374 days 14 hours; both witnesses share this unusual arithmetic.
- Six minute rows have faint, partially unreadable day/hour digits even in the higher-resolution scans: 25', 28', 39', 41', 44', 48'. The comparison CSV leaves original source day/hour values BLANK, retaining the newer 2003 candidate values only in expressly distinct columns.
- The 1647 printed 19°52' worked example concludes **20 years, 57 days, 21 hours**; the modern retype's final prose states **22 years**. This is a separate prose discrepancy, NOT an extra table-cell difference.
- The 1647 printed 11°55' worked example gives **12 years, 33 days, 14 hours**, matching the independently transcribed cells.

Total independently confirmed numeric TABLE CELL differences: **23** = 22 degree-year differences plus new minute-one day difference. This does not mean the still-faint six minute cells agree with the 2003 edition.

## Separate strict photographic-source calculator

New src/hdmatch/astrology/lilly_1647_photo.py keeps original 1647 numbers independent from the 2003 source data. For D=0..90 and M=0..59, the lookup uses original photo-confirmed years/days/hours only. It raises an explicit SourceWitnessUnavailable for missing minute 27 and for each of the six genuinely faint cells, with no interpolation or implicit borrowing from 2003. Seconds are outside source scope. Raw 80° 24-hour entry remains raw and normalizes only in result arithmetic.

Sample comparisons:

  Original photo 0°1' -> 0y 5d 4h
  2003 retype  0°1' -> 0y 6d 4h
  Original photo 69°1' -> 70y 9d 7h
  2003 retype  69°1' -> 69y 10d 7h
  Original photo 11°55' -> 12y 33d 14h
  Original photo 19°52' -> 20y 57d 21h

No default time keys, existing historical Naibod witnesses, numerical natal primary directions, production Human Design scoring, survey answers, or predictive claims were modified.

## Running on Zorin OS

The complete runnable checkout is saved at:

  $HOME/.local/share/hdmatch/research-checkouts/lilly-1647-minute-collation-engine

From that checkout:

  export PYTHONPATH="$PWD/src"
  $HOME/humandesign/.venv/bin/python -m hdmatch.astrology.lilly_1647_photo --degrees 69 --minutes 1

Regenerate exact row comparison offline:

  PYTHONPATH=src $HOME/humandesign/.venv/bin/python docs/astrology-research-map/lilly-1647-independent-table-collation-20261024/regenerate_collation.py

The three high-resolution Wellcome original JPEG source pages and provenance are included in the ZIP; no need for a full PDF download.

## Verification / still open

121 prior+new source/geometry/astronomy regression tests PASS. Exact commands, file hashes, Ruff and mypy outcomes are recorded in VERIFICATION.json. Previous default models and original source records remain frozen.

Six original minute cells remain UNCERTAIN, even though 2003 gives candidate numbers. They need a better source or independent direct verification. This is not a new fail-closed blocker for unrelated computations or for source-verified mathematical arms.

The owner root remains OPEN: historically accurate and differentiated calculations eventually entering a frozen, combined forward-blind empirical study. Neither original text agreement nor perfect mathematics establishes astrological prediction accuracy.
