# Brahe birth-day and Placidean accumulated solar-RA timing

24 October 2026. Research-only, NOT empirically validated forecasting.

## Parent objective

Preserve reproducible historical astrology calculations and independently differentiated source rules for later prospective, blinded comparison alongside the other astrology systems. Do not select methods by fitting them to already-known life events.

## Source and method separation

The prior purchased Gansten Primary Directions audit (chapter 6, pp.73–80) distinguishes these two constructions:

- BRAHE: the Sun's apparent right-ascension change across the local true-solar midnights bracketing birth is treated as a fixed equatorial rotation in one symbolic year.
- PLACIDUS: calculate the total postnatal apparent Sun right-ascension advance; find the number of elapsed postnatal solar days whose accumulated RA equals the directional arc. This is a variable-rate root-solving problem, not a constant natal-day rate.

A 2009 Skyscript discussion attributed to Martin Gansten independently supports the midnight-to-midnight Brahe definition and its frequent mislabeling as Kepler. The present code derives its ancient-method interpretation from the prior Gansten audit; original Brahe De Stella Nova (1573) and Placidus primary texts were NOT re-read this turn. In particular, modern Swiss astronomy cannot be claimed identical to a Renaissance ephemeris.

## Implemented astronomical conventions

New standalone Python module: src/hdmatch/astrology/solar_time_keys.py

Named CLI switches:
  --solar-time-key brahe_true_midnight_birth_day
  --solar-time-key placidus_cumulative_true_solar_ra

Brahe: solve Sun's local LOWER-meridian transit as its geocentric hour angle H_sun=180 degrees, not UTC midnight or precisely 24h after birth. Find both local true solar midnights, compute their actual elapsed interval and Sun RA difference, then divide the primary-direction arc by the resulting fixed birth-day RA rate. Record the exact two UTC instants and rate in JSON provenance.

Placidus: evaluate and unwrap RA Sun(birth + d postnatal days) minus RA Sun(birth), identify the correct day bracket, and invert with bisection to fractional day. Interpret postnatal days as symbolic years.

SwissEphemerisProvider is reused with declared and SHA-256 hashed local .se1 files. Each solar sample verifies Swiss-file and equatorial returned flags, actual used planetary file, and natal file provenance. Geocentric, tropical, apparent RA of true equinox-of-date, UT input/Swiss TT handling, longitude east positive.

Resulting model dates use the explicitly modern 365.2422 days/year policy, not a reconstructed ancient anniversary convention. No life events were used.

## Integration without backwards breakage

The CLI adds --solar-time-key as an OPT-IN alternative to the existing --key; the two cannot be combined. All old defaults remain unchanged. It supports body conjunctions, zodiacal promissor rays, mundane semi-arc phase, and declared role-variant direct/traditional-converse/reversed-rotation profiles.

Requested age window must be (0,100]. The geometry stage first generates a broader 125-degree contact set, then assigns solar symbolic ages and filters to the requested window, to avoid prematurely losing candidates near age 100. Output metadata describes this preselection and each selected solar key. No unsupported historical method is silently substituted.

Run on Zorin after cloning this branch:
  cd "$HOME/Documents/astrology/gansten-solar-timekey-engine"
  export PYTHONPATH="$PWD/src"
  "$HOME/humandesign/.venv/bin/python" -m hdmatch.astrology.cli \
      --utc 2000-01-01T12:00:00Z --latitude 45 --longitude-east 0 \
      --ephemeris-dir "$HOME/.local/share/hdmatch/ephemeris/1800-2399" \
      --solar-time-key brahe_true_midnight_birth_day \
      --output /tmp/example_brahe_solar_key.json

For cumulative-solar timing change the solar key to placidus_cumulative_true_solar_ra.

## Magnitude of method differences: 75-degree synthetic arc

Season and longitude                  Ptolemy  Fixed 59'08"  Brahe    Placidus
2000-01-01 12:00 UTC 45N 0E           75.000    76.099     67.889    74.737
2000-07-01 18:00 UTC 34S 70W          75.000    76.099     72.550    78.604
2026-03-19 06:00 UTC 45N 24E          75.000    76.099     82.196    78.442

These are purely numerical example ages, not dates at which any real event was predicted. Brahe's birth-day rates in these cases are 1.104737842, 1.033765163, and 0.912455622 degrees/year respectively. Using one preferred historical key after seeing actual events would inflate apparent predictive success.

## Independent assurance

- The numerical true-midnight algorithm agrees with independent Swiss rise_trans lower-transit calls at SIX time points across three chart dates/locations to within ~0.02 seconds.
- Placidus accumulated solar-RA inversion checked at ten named ages and 45 seeded randomly chosen ages; solar motion monotonic and positive on the restricted domain.
- Every original geometric arc is unchanged. Synthetic January 2000, 100-year output retains 126 Brahe vs 114 Placidus conjunction contacts.
- Existing zodiacal/mundane/role calculators accept either solar profile. Aspects' branch identities remain separate, avoiding a false duplication in an initially miskeyed test.
- Earlier original 1647 Lilly Naibod and 2003 retypeset witnesses remain unchanged and do not become a synthesized false literal key.
- At checkpoint: 85 relevant tests pass; Ruff lint and mypy pass, with exact commands/files in VERIFICATION.json.

## Unfinished

Independently inspect original 1573 Brahe and 17th-century Placidean source definitions and more than one software implementation to assess exact historical fidelity. Complete photographic collation of the remaining Lilly 1647 minute/day/hour cells, separate from modern retypesetting. Freeze method families and prospective target rules BEFORE using human data; account for multiplicity/double-counting.

Root research OPEN; work committed only to an isolated research branch, not production or empirical prediction.
