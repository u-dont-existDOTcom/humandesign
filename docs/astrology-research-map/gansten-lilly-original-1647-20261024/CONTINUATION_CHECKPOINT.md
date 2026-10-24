# Continuation checkpoint — Lilly original 1647 witness

Date: 2026-10-24. Original user outcome remains OPEN: accurate separate astrology systems, later frozen comparison against independent human data. This source subtask materially corrects the 2003 Naibod re-typeset but does not create a comprehensive predictive method.

## Source evidence and corrections accomplished

- Found and visually inspected *original 1647* Christian Astrology printed pp.713–715, located at original-volume PDF page photos 735–737. Photographic SHA-256 metadata is in ORIGINAL_1647_SOURCE_COMPARISON.json and 3 public-domain JPEGs are stored in facsimile_pages/.
- 1647 year column on p.713: 69°=70y4d3h, 70°=71y9d11h, 80°=81y62d24h, 90°=91y116d13h. The separate 2003 retyping instead assigns year=degree at rows 69–90. These are exactly 22 one-year-cell differences. Degree-day/hour columns remain inherited from modern witness with only selected original spot checks.
- Printed p.715 19°52' example concludes TWENTY years 57 days 21 hours, matching arithmetic; 2003 retype's 22-year conclusion is wrong. The original worked 11°55' example also matches 12y33d14h.
- Shared original abnormalities: absent minute 27', 8'=44d10h, 60'=374d14h vs 1° row inconsistency, and 80° hour value 24. Minute 44 small glyph uncertain. No hypothetical corrections or interpolation.
- New src/hdmatch/astrology/naibod_original_1647.py is a separate limited first-edition-comparison diagnostic, not a continuous main-engine key. The 2003 source code and CSV and all four prior time keys are deliberately unchanged. Critical metadata explicitly rejects a claim of *complete* original cell-by-cell transcription.
- New CSV 90 year comparisons, 22 corrections; six computed side-by-side examples; source inventory and source-image hashes; new CLI for selected D°M' lookup; 12 new regression tests (including photo SHA and warning provenance). Full relevant regression set 73 tests passing, lint and mypy tested separately.
- No actual human chart, event story, or outcome fitting; no production scorer modification. Root purpose anchored rather than expanding requirements.

## Next safe steps

1. Independently collate all original minute/day/hour figures, including faint minute 44, ideally using a second 1647 copy or higher-resolution photograph. Report differences without smoothing.
2. Add precisely sourced Brahe daily-solar-RA and Placidus cumulative solar-RA keys with Swiss-file time convention, beyond the fixed-rate diagnostics. If the historical source cannot disambiguate a convention, implement a separately named mathematical model with an uncertainty tag rather than pass as historically verified.
3. Once all planned source/method families are computed and frozen, build the intended joint forward-blind validation, controlling duplicate contacts and researcher degrees of freedom.

Publication status: isolated research branch research/gansten-lilly-original-1647-correction-20261024, parent branch research/gansten-lilly-naibod-time-keys-20261024.

Deliverable: a source-backed numerical correction and executable witness comparison, not a completed historically certified astrology forecast.
