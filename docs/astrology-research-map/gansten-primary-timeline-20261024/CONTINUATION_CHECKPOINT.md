# Continuation checkpoint — primary directions

Date: 2026-10-24.
Owner continuation goal: move beyond Morinus and build reliable birth-to-primary-directions calculation support for humandesign.

State: PARTIALLY SATISFIED. The new research-only Swiss-file birth/time/location-to-timeline component works for seven classical bodies directed to other classical bodies and exact ASC/MC, bodily conjunctions only. Not a complete historical prediction engine, not promoted to production, no human predictive validation.

Previous audited source and Morinus comparison branches remain intact. The signed-AO/DO workaround is independently implemented in our geometry, not patched into Morinus. Three historically distinguishable geometries remain separate. Timing has Ptolemy one equinoctial degree per symbolic year and an explicitly contemporary mean-solar diagnostic; neither is disguised as the literal printed Lilly Naibod table.

Created:
- src/hdmatch/astrology/geometry.py
- src/hdmatch/astrology/sky.py
- src/hdmatch/astrology/timeline.py
- src/hdmatch/astrology/cli.py
- tests/unit/test_primary_directions.py
- docs/astrology-research-map/gansten-primary-timeline-20261024/README.md
- docs/astrology-research-map/gansten-primary-timeline-20261024/VERIFICATION.json
- two strictly Swiss-provenanced synthetic JSON timeline examples.

Assurance: 22 relevant tests pass; strict mypy and ruff pass. Independent synthetic geometry reference values match, and a concrete Swiss birth chart crosses the RA 0° boundary without the Morinus direct/converse reversal. No personal birth chart, outcome fitting or human data used. External official Swiss ephemeris files are held locally outside Git; source SHA-256 is in VERIFICATION.json.

Next: historically sourced direction of zodiacal promissor and significator aspects, latitude options and Bianchini handling, original Lilly timing tables, lunar secondary motion, Lots/terms, all traditional contact variants and independent reference engine parity. Only afterward can candidate rules enter the intended frozen combined forward-blind astrology test.

Root research project remains OPEN; no owner decision presently needed for continuing internal research.
