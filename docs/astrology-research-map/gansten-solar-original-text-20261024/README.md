# Brahe and Placidus — original-text attribution check

Research checkpoint 24 October 2026. This audit corrects source labels but not astronomical calculations or existing output data.

## Root research objective

Build independently calculable historical astrology systems, freeze their rules in advance, and eventually compare their prospective predictions jointly on untouched blinded human questionnaire evidence. Mathematical reproducibility does NOT imply predictive usefulness.

## Brahe, De Nova Stella (1573)

Inspected the Latin in a critical scholarly transcription (edited by J. L. E. Dreyer), dedicatory meteorological-calendar letter around original folio G1r/G1v:

https://tekstnet.dk/books/brahe-t_de-nova-stella/010/

The passage explicitly distinguishes the Sun's true non-uniform daily motion from abstract uniform motion, with equatorial rotation corresponding to a symbolic year in nativities. In the SAME passage Brahe switches to the Moon's true variable daily movement to derive an equatorial arc for each meteorological calendar day. These are two separate applications.

LIMIT: The 1573 passage does NOT specify that the natal birth-day endpoints must be the two adjacent LOCAL TRUE SOLAR MIDNIGHTS. That detail remains a later Gansten-informed computational interpretation. The original 1573 page photograph was not independently viewed; this is a critically edited Latin transcription.

## Placidus, via John Cooper's Primum Mobile (1814)

Downloaded the public-domain edited English translation of the original Placidus de Titis Tabulae Primi Mobilis (1657). Examined original scan pages at:
  https://iapsop.com/ssoc/1814__cooper___primum_mobile.pdf

Printed pp.23-25 correspond to PDF pp.40-42 (1-based). Three page PNGs and their hashes are included in source_page_images and SOURCE_WITNESS_AUDIT.json.

Verified by inspection of the scanned pages:
- Thesis 58, printed p.23: Sun's successive daily movement linked to sequential years, mentioning the same equal hour of birth.
- Thesis 65, printed pp.24-25: the right-ascensional interval of Sun on first subsequent day governs first year, second day governs second year, and so on. This supports the core geometry of the existing cumulative solar-RA calculation as a mathematical model of Cooper's account.
- Thesis 60, printed p.23: angles CANNOT be directed in converse.
- Theses 61-62, printed pp.23-24: zodiacal rays are explicitly NOT admitted in converse by this presentation of Placidus; only mundane rays/parallels are relevant to such converse aspects.

CRITICAL: The generic traditional_role_reversed_converse + zodiacal_promissor_ray calculation in the earlier engine is still a mathematically defined candidate, but is incompatible with this 1814 presentation of Placidus. Do NOT promote it to a historically authenticated Placidus converse-zodiacal rule. Other authors may have different converse rules; this is NOT a universal ban.

LIMIT: This is an 1814 edited English translation. The 1657 LATIN original is catalogued (Wellcome, Google Books), but the corresponding folios were not independently checked against Cooper. Modern Swiss Ephemeris, UT/TT, true equator-of-date and midnight definitions are not being falsely attributed to the original text.

## Nonbreaking implementation

A new source_witness_scope.py module records source-specific assessments:
- partial_source_support for Brahe's true varying solar daily motion, without claiming the original specified true-midnight endpoints;
- compatible_selected_rule for cumulative true solar RA from the 1814 Placidus translation;
- incompatible_witness for Cooper's prohibition on converse zodiacal rays or on moving angles;
- not_established where no inspected original passage decides the case.

This is an evidence classifier, not a new fail-closed architecture gate. The generic mathematical calculations continue working. SolarRAEngine outputs now add a primary_source_scope field, replacing the obsolete claim that the Brahe original had not been consulted.

SOURCE_SCOPED_SYNTHETIC_CHECK.json verifies that every pre-existing Brahe or Placidus solar-key synthetic chart contact (arc, symbolic age, model date, candidate count) is numerically EXACTLY unchanged. Only source metadata was expanded. All previous fixed keys, historical Lilly tables and production models remain unchanged.

## Files and usage

Complete public-domain 1814 scan saved on the authorized Zorin machine:

    $HOME/Documents/books/astro/Placidus_Primum_Mobile_Cooper_1814.pdf

Selected printed pages 23-25 and a source witness comparison are bundled in this research checkpoint.

Full runnable research checkout location after publication:

    $HOME/Documents/astrology/gansten-solar-primary-source-engine

Regenerate the source-labelled synthetic example:
    cd "$HOME/Documents/astrology/gansten-solar-primary-source-engine"
    export PYTHONPATH="$PWD/src"
    HDMATCH_PRIMARY_DIR_EPHE_DIR="$HOME/.local/share/hdmatch/ephemeris/1800-2399" \
      $HOME/humandesign/.venv/bin/python \
      docs/astrology-research-map/gansten-solar-original-text-20261024/regenerate_source_examples.py

The original CLI and older time keys are unchanged; source provenance is more exact. No user's or third party's personal birth/event data was used.

## Next frontier

Examine the original 1657 Latin Placidus thesis 58-65 to see whether the 1814 editor accurately retained all source restrictions; verify Brahe's original 1573 facsimile if accessible; finish Lilly's remaining original day/hour/minute collation. These are source-fidelity refinements, not mandatory prerequisites to working engineering candidates or evidence of predictive accuracy. Keep the eventual frozen combined forward-blind test as the main objective.
