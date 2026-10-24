# Primary-direction timelines — first working birth-to-arcs engine

24 October 2026. Research-only, auditable geometry and symbolic-age tool. **Not a historical method-complete implementation and not evidence of predictive validity.**

## Completed

The engine connects a timezone-aware birth instant and geographic latitude/longitude to primary-direction arcs for the seven classical bodies and two angles. Results retain three **separate**, named geometric algorithms:

- proportional semi-arcs, matching the audited Ptolemy/Gansten geometric model;
- Placidean under-the-pole, using signed oblique ascension/descension without the verified Morinus SE 8.0.0 zero-crossing error;
- Regiomontanian position circles, solved independently using a Cartesian great-circle intersection.

Body promissors are directed to other natal bodies and to exact Ascendant/Midheaven. The current contact profile is **conjunction only**. Rays/aspects, historical terms, lots, cusps other than ASC/MC, stars, subzodiacal variants and lunar secondary motion are *not* implemented. Cases where a position circle has no valid intersection remain explicit missing results.

Time keys are parameterized separately: Ptolemy one equinoctial degree of rotation per symbolic year, and a **modern** rational mean-solar diagnostic (360/365.2422 degrees per year). Neither is silently presented as Lilly's printed Naibod table. Model dates use a declared modern 365.2422-day mean year, not an authenticated historical calendar key.

Direction sense follows the Morinus-like shortest signed arc convention, not a universal traditional converse definition. No outcomes, death/illness, romance, status, spirituality, personality or empirical claims are inferred.

## Astronomy and reproducibility

Reuses the repository's strict SwissEphemerisProvider and SwissAstronomyReferenceProvider. The former hashes the actual local .se1 source files and verifies SWIEPH returned flags; the latter produces ecliptic and equatorial state. Input is apparent geocentric, true equator/equinox of date, tropical, east-positive geographic longitude. No silent Moshier fallback.

Official planetary and Moon files have been installed **outside the repository** on the owner's Zorin laptop:

    /home/joel/.local/share/hdmatch/ephemeris/1800-2399/

- sepl_18.se1: ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66
- semo_18.se1: 1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7

Origin: official Astrodienst Swiss Ephemeris public GitHub project aloistr/swisseph, ephe directory. Files are NOT included in the ZIP or committed to Git. This version explicitly supports 1800–2399 CE (the two downloaded file epochs) and geographic latitude −66° to +66° (the current Placidus ascendant routine). Out-of-range or missing-file inputs fail clearly.

## Run using Zorin's existing Python virtual environment

From this research checkout:

    cd /tmp/gansten-primary-directions-20261024
    export PYTHONPATH="$PWD/src"
    /home/joel/humandesign/.venv/bin/python -m hdmatch.astrology.cli \
      --utc 2000-01-01T12:00:00Z --latitude 45 --longitude-east 0 \
      --ephemeris-dir /home/joel/.local/share/hdmatch/ephemeris/1800-2399 \
      --method all --key ptolemy_one_degree_per_year --max-age 100 \
      --output /tmp/primary_direction_example.json

Select individual geometry by --method placidean_under_pole, --method proportional_semi_arc, or --method regiomontanian_position_circle. Alternative timing --key modern_mean_solar_diagnostic remains correctly labeled a contemporary mathematical convention. All output is stable, audit-oriented JSON with source file hashes, explicit coverage, symbolic ages and method provenance. The CLI refuses to overwrite existing outputs.

## Actual verification

Two *invented* birth examples, no participant histories:

1. 2000-01-01 12:00 UTC, 45° N, 0° E: 168 algorithm/body combinations evaluated; 114 conjunction contacts within a 100-symbolic-year window. Sun → MC 0.821313141° for all three methods, matching the independently inspected Morinus GUI 0.821°. Exact Ascendant is on the true local eastern horizon; three geometry methods reduce to the same angles for ASC/MC.
2. 2026-03-19 06:00 UTC, 45° N, 24° E: 146 contacts within 100 symbolic years. Sun → Moon direct 0.618803° under official Swiss-file astronomy using the signed Placidean under-pole formula. Original Morinus AppImage displays about 2.295° converse in the source-sign-bug case.

The three frozen Gansten synthetic reference arcs 42.17434402835047°, 42.20081504892782° and 46.449117851278395° are reproduced. Unit/property tests compare 500 deterministic random cases against the previously independently frozen geometry and include earlier Morinus sign-disagreement cases, strict file provenance, time-key separation and 0° boundary regression. The existing source-method 9,600-case audit remains distinct from these *new* Swiss-file input/output tests.

For tests run tests/unit/test_primary_directions.py alongside tests/unit/test_astronomy_reference.py and tests/unit/test_relationship_western_rrf.py, with HDMATCH_PRIMARY_DIR_EPHE_DIR pointing to the external local ephemeris folder. See VERIFICATION.json for exact commands and results.

## Boundaries and next integration stages

- Add historically sourced rays/aspects (promissor vs significator placement and ecliptic vs mundane), bounds/terms, secondary lunar motion, profections, and more significators.
- Reconcile historic timing with **literal Lilly Naibod** tables rather than substituting a rational mean-solar constant.
- Expand geographic domain, planetary latitude/secondary motion options, historical witnesses, calendar chronology, uncertainties and reference software parity.
- Preserve this module as isolated engineering research. Do NOT merge predictions into frozen Human Design or other astrology scoring or interpret mathematical dates as validated events. Later combined forward-blind testing is separate.

**Root outcome: partially complete.** A usable classical **conjunction-only** primary-direction timeline engine now runs from birth data with verified Swiss files. It is not a complete historically faithful predictive engine.
