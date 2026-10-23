# Gansten primary directions — historical reconciliation and geometric parity

**Status (2026-10-23): SOURCE_COMPARE_PARTIAL, SYNTHETIC_GEOMETRY_REPRODUCED, PREDICTIVE_VALIDATION_NOT_PERFORMED.**

This isolated research branch preserves the completed Gansten Kindle audit as its parent and adds:
- `GANSTEN_RECONCILIATION_REPORT.md`: selected Gansten × Lilly × Ptolemy comparison and method distinctions.
- `GANSTEN_LILLY_PTOLEMY_CROSSWALK.csv`: 12 keyed source-comparison records with unresolved historical differences.
- `geometry_reference.py`: restricted, frozen-coordinate sphere formulas including an independent vector position-circle solver.
- `test_geometry_reference.py`: nine numerical tests, including all quadrant inversions and both geographic hemispheres where defined.
- `run_verification.py`: repeatable random synthetic parity tests; no biographies or charts are used.
- `VERIFICATION.json`: prior execution results (nine tests; 6,000 Regiomontanian pole/vector comparisons).
- `SOURCE_PROVENANCE.json`: exact parent and historical-audit checkpoint references.

Run from this directory: `python3 -m unittest -v test_geometry_reference && python3 run_verification.py`.

**Nonclaims and restrictions:** These checks do not establish historical authorship, source-glyph collation, current software-engine parity, ephemeris correctness, or predictive validity in humans. The restricted Placidean under-pole formula is not a complete global algorithm. Do not merge it into production calculations or evaluate known biographies until models, birth-data provenance and comparison scoring are frozen. No copyrighted source text is reproduced.
