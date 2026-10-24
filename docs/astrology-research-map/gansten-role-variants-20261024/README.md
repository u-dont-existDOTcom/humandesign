# Primary directions — converse roles and significator aspects

Research checkpoint: 24 October 2026. Status: engineering-only, no human predictive validation.

## Immutable research purpose

Calculate historical astrology systems accurately from independently supplied natal data, preserve separate interpretations and calculation traditions, and later compare frozen predictions jointly with other astrology systems under genuinely blinded testing. The code here is **not** an empirically validated forecast.

## Source and limitations

The basis is the previously reviewed, purchased Martin Gansten book audit, not a fresh Kindle extraction. Reported locators are Ch. 1 pp. 5–7 and notes pp. 9–10 (promissor versus significator and converse), Ch. 5 pp. 65–71 (zodiacal aspects and role ownership), and Ch. 8 pp. 88–101 (contested traditional/modern converse, aspects and moving-angles distinctions). These are **paraphrases from the prior audit**, not recovered original quotations.

Historical authors disagree on permissibility of converse zodiacal and significator aspects; this code calculates explicitly labeled candidate geometries, not a claimed universally attested package. Nothing in this pass repairs the unresolved Bianchini/Morin latitude rules, Moon secondary motion, hyleg, Fortune, house cusps, fixed stars or event interpretation.

## New implemented constructions

The preexisting body_conjunctions, zodiacal_promissor_rays and mundane_proportional_semi_arc CLI profiles and their frozen JSON results stay unchanged. A new, independent profile --profile role_variants supports:

- bodily_conjunction: move natal body to a fixed natal body or angle.
- zodiacal_promissor_ray: add or subtract 60°, 90°, 120°, 180° in **ecliptic longitude** of the promissor (beta=0), then convert to true-of-date equatorial coordinates before directing. One opposition branch.
- zodiacal_significator_aspect: construct the significator's beta=0 ecliptic aspect point and move the **physical promissor body** toward it. Explicitly flagged as an experimental disputed construction. Does not permit angular significators.

Movement regimes are **not synonyms**:

1. direct_primary_motion: promissor (body/ray) moves forward to a fixed significator/body ray.
2. traditional_role_reversed_converse: fixed promissor or promissor-owned ray; the natal significator *body moves forward in primary motion*. Geometrical angular/meridian significators are excluded because moving an angle requires a separate historically sourced natal-longitude construction. Significator-owned aspects in this role-reversal mode are likewise not silently invented.
3. modern_reverse_rotation_diagnostic: retain moving/fixed roles but compute (360° minus forward arc) modulo 360°; **not** the older role-reversed converse.

The new code does not convert full forward arcs beyond 180° into easy short converse matches. The old "shortest signed" legacy convention remains separate. Symbolic age keys remain one-degree-per-year or distinctly named modern mean-solar diagnostic; calendar date model uses an explicitly modern 365.2422-day year, **not** an authentic Lilly Naibod printed table.

All natal states use local verified Swiss Ephemeris planetary and lunar files and their returned SWIEPH flags, with cached file SHA-256 provenance. The official .se1 files are kept outside Git.

## Geometric comparison and key anti-double-counting result

Frozen reference points: latitude 45°N, RAMC 0°, fixed (RA 50°, declination +15°), moving (RA 80°, declination −10°).

| Geometry | Direct forward | Traditional role-reversed | Modern reversed arc |
|---|---:|---:|---:|
| Proportional semi-arc | 42.174344028° | 304.341840702° | 317.825655972° |
| Under-the-pole | 42.200815049° | 304.342190906° | 317.799184951° |
| Regiomontanian | 46.449117851° | 304.301939265° | 313.550882149° |

**Critical equivalence:** For bodily, unprojected planetary significators, a fixed **promissor-owned ray P±ψ** with moving significator S in the traditional converse is mathematically the **same physical rotation** as a fixed **significator-owned ray P±ψ** with moving promissor S under direct motion, after swapping the named P/S roles. Item-by-item regression confirms all 288 of the matching example contacts are equal in arc/age. Their historical *meaning* need not coincide. Never count both as independent evidence of prediction. When the moving body is projected to the ecliptic or an angle is involved this particular equivalence is not assumed.

A direct raw arc and a 360° complementary reverse arc cannot both lie within the same 100° symbolic-age cap, except zero; an apparent absence of shared contacts in that comparison is mathematical, not a missing-calculation error.

## Exact synthetic output coverage

All from invented birth 2000-01-01 12:00 UTC, latitude 45°N, longitude 0°E, seven classical bodies, 100 symbolic years, three geometry models:

| Construction + regime | Evaluated | Contacts in window |
|---|---:|---:|
| Promissor ray; traditional role reversal | 882 | 288 |
| Promissor ray; modern reverse rotation | 1176 | 364 |
| Significator aspect; direct | 882 | 288 |
| Bodily conjunction; traditional role reversal | 126 | 36 |

**These are geometric candidates, not forecasts.** Larger option sets increase multiple-testing risk. Compare frozen method families independently and deduplicate equal rotations.

## Tests and usage

See VERIFICATION.json for SHA-256, exact test command, frozen-source comparisons and output schema. 48 relevant tests passed with independently frozen Cartesian/analytic geometry checks, strict type checking and code linting. Existing baseline JSON output remains exactly equal to the earlier sample.

Persistent local checkout on Zorin:

    /home/joel/Documents/astrology/gansten-primary-direction-roles-engine

Swiss files:

    /home/joel/.local/share/hdmatch/ephemeris/1800-2399

From the checkout:

    export PYTHONPATH="$PWD/src"
    /home/joel/humandesign/.venv/bin/python -m hdmatch.astrology.cli \
      --utc 2000-01-01T12:00:00Z --latitude 45 --longitude-east 0 \
      --ephemeris-dir /home/joel/.local/share/hdmatch/ephemeris/1800-2399 \
      --profile role_variants \
      --contact-construction zodiacal_promissor_ray \
      --rotation-regime traditional_role_reversed_converse \
      --output /tmp/traditional_direction_example.json

To compare explicit reverse rotation, set --rotation-regime modern_reverse_rotation_diagnostic. For an aspect belonging to the fixed significator, choose --contact-construction zodiacal_significator_aspect together with --rotation-regime direct_primary_motion. Invalid historical combinations fail closed. The CLI refuses overwriting output files.

## Open research frontier

Literal Lilly/Naibod table cells are NOT recovered sufficiently for a historical-exact time key; the earlier Gansten audit distinguished printed DMS values and anomalous literal rows from the modern rational approximation. Next: retrieve and reconcile those original table values and timing keys, verify original authorial aspect/converse precedents, then add separately sourced bounds/terms, Fortune, secondary motion and other interpretive rules. Keep frozen human predictions, posterior fitting and out-of-sample evidence distinct.

Research parent remains OPEN. Code remains isolated from the production Human Design scorer and no personal birth details or event histories were used.
