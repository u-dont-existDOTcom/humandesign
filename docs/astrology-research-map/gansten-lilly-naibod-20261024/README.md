# Lilly / Naibod historical timing tables — source and arithmetic audit

Research checkpoint: 24 October 2026. No empirical astrology validation.

## Parent owner goal

Implement independently reproducible historical astrology calculations so method variants can eventually be frozen, tested together with other astrology traditions, and evaluated against blinded human evidence. Do not select timing formulas by fitting them to familiar life events.

## Witness and scope

The accessible textual basis for this pass is William Lilly, Christian Astrology, Book III, third measure of time according to Naibod, reproduced in a WorldAstrology re-typeset PDF (copyright 2003):

https://www.worldastrology.net/wp-content/uploads/2008/12/CA-III.pdf

The degree table is printed page 713 (PDF zero-based page 226), minute table page 714 (PDF page 227), and worked examples page 715 (PDF page 228). These page images were VISUALLY INSPECTED; numerical rows were not inferred from OCR alone.

CRITICAL LIMIT: the original 1647 printed page images were NOT independently inspected. This PDF is a modern retypesetting rather than a facsimile scan. Apparent numerical and textual errors may come from the transcription rather than Lilly's original publication. All historical claims below are explicitly about this accessible re-typeset witness.

The previously purchased Gansten Primary Directions book audit Ch.6 pp.73-79 distinguishes 1 degree/year, Naibod mean-solar key, Brahe birth-date solar right-ascensional key, and Placidus variable true-solar key. Cardan priority and original historical second values remain contested in the audit.

## Implemented now

1. Literal edition-scoped data: degree rows 1–90 and minute rows 1–60 (with absent minute 27 clearly marked), original displayed day/hour/year fields, and numerical integrity warnings. File: LILLY_NAIBOD_2003_RETYPED_LITERAL_CELLS.csv. The literal lookup code is in src/hdmatch/astrology/historical_naibod.py.
2. Standalone lookup accepts ONLY integer D°M' with D=0–90 and M=0–59. Unknown row 27', non-integer input, or other missing positions raise an explicit error. It sums the literal components and normalizes hours and 365-day years without silently changing source digits. It deliberately cannot be used as a continuous/default timing key, because the table omits cells and contains ambiguities.
3. Two separately named, FIXED-RATE diagnostics now available to the existing CLI and calculation families:
   - naibod_59m08s_fixed_diagnostic = exactly 0°59'08" per symbolic year = (59*60+8)/3600 degrees/year.
   - naibod_exact_360_over_365_25_diagnostic = exact 360/365.25 degrees/year.
   These rates differ by approximately 0.254620 angular seconds/year. NEITHER diagnostic reproduces the re-typeset table row by row. The old one-degree/year and modern 360/365.2422 keys remain unchanged, as do all previously frozen default outputs.

For a 75° arc, the rational 360/365.25 model gives 76.093750 model-years, while fixed 59'08" gives about 76.099210823 model-years (approximately two days later using 365.25 days per year). These are arithmetic models, not evidence for a real event.

## Source inconsistencies preserved, not corrected

Printed page | Witness value | Integrity question
--- | --- | ---
713 | degree 68° extra days 364 → at degree 69° reset to 4 days, while year count only increases 68→69 | The uncarried year would create a discontinuity if used literally; original-edition bookkeeping needs checking
713 | 80° = 80yr +62 days +24 hours | Hour 24 is non-normalized; preserved
714 | 7'=43d6h; 8'=44d10h; 9'=55d14h | The 8' cell likely has an erroneous day value, not silently replaced
714 | 27' missing; 28', 29', 30' shifted-looking numeric sequence | Preserve raw labels, do not fill 27'
714 | 44'=271d8h | Unusual hour value, needs original witness
714 | 60'=374d14h vs 1°=1y5d8h =370d8h | Physically equivalent arc yields a difference of four days six hours
715 | 19°52' intermediate sum =19y422d21h | With 365d years, arithmetic gives 20y57d21h; text concludes 22y57d21h, a two-year difference

The source-anomaly register is LILLY_SOURCE_ANOMALIES.json and preserves the exact evidentiary limitation. DO NOT claim these are errors in Lilly's original first edition before seeing those printed pages.

The other verified worked example reproduces without anomaly: 11°55' = (11y58d21h + 339d17h) = 12y33d14h after carrying.

## Run locally on Zorin

The complete versioned research checkout should be installed at:

    $HOME/Documents/astrology/gansten-lilly-naibod-time-keys-engine

The external official SWIEPH files are at:

    $HOME/.local/share/hdmatch/ephemeris/1800-2399

Run literal table lookup (NO event forecast):

    cd $HOME/Documents/astrology/gansten-lilly-naibod-time-keys-engine
    export PYTHONPATH="$PWD/src"
    $HOME/humandesign/.venv/bin/python -m hdmatch.astrology.historical_naibod --degrees 11 --minutes 55

Run a synthetic sky-direction example with an explicitly named continuous diagnostic:

    $HOME/humandesign/.venv/bin/python -m hdmatch.astrology.cli \
       --utc 2000-01-01T12:00:00Z --latitude 45 --longitude-east 0 \
       --ephemeris-dir $HOME/.local/share/hdmatch/ephemeris/1800-2399 \
       --key naibod_59m08s_fixed_diagnostic \
       --output /tmp/naibod_59m08s_timeline.json

For exact rational 360/365.25, instead choose --key naibod_exact_360_over_365_25_diagnostic.
The original defaults remain unchanged. Model dates are modern 365.2422-day arithmetic, NOT verified original printed year boundaries.

## Reproduction and assurance

- 152 rows in the CSV: 91 degree labels including one added 0° identity; 61 minute labels 0–60 including one added 0' identity and one missing 27' cell record.
- Unit tests cover literal visually observed cells, two worked examples, missing 27', 68°/69° rollover, 60' versus 1° and 24-hour carry.
- All four fixed annual-rate choices are distinct and separately labeled, with numeric comparison at 75°.
- Swiss-file ephemeris remains local, with verified return flags and source SHA-256 in existing engine records. No ephemeris binary copied into this ZIP or Git.
- Full relevant source-engine regression tests, Ruff and mypy results in VERIFICATION.json. Existing astrology prediction scoring remains untouched.

## Next frontier

Obtain and independently inspect genuine first-edition or contemporary Lilly printed pages 713–715 and adjudicate each anomalous cell. Do not invent corrections. Then complete other historically sourced timing methods (Brahe daily solar RA at birth and Placidus accumulated solar RA) with proper original-convention, coordinate, sidereal/UT and Julian-date definitions. After historical geometry and timing variants are independently verified, freeze specific candidate predictions and proceed to combined forward-blind comparisons with multiplicity controls.

Root empirical research remains OPEN. This packet is a numerical source audit and engineering improvement only.
