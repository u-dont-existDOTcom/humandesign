# Primary-directions aspect continuation checkpoint — 2026-10-24

**Owner intent:** Continue the empirical astrology primary-direction calculation engine, not more third-party bug hunting, and keep separate historical variants for eventual combined blinded tests.

**Status:** New aspect-projection research implementation ready. Root historical-engine and empirical goals remain OPEN.

## Changes completed in this branch

- Existing Swiss-verified natal ephemeris snapshot extended to retain each of seven classical planets' ecliptic longitude and latitude plus true obliquity of date.
- New aspect_points.py: distinct 60°/90°/120°/180° ecliptic ZERO-LATITUDE promissor rays (both mathematical ± branches except unique opposition) and independently reconstructed normalized semi-arc phase offsets. No right-ascensional aspect mislabeling.
- New aspect_timeline.py: zodiacal promissor rays supported by proportional semi-arcs, Placidean under-the-pole and Regiomontanian position circles, with body-retained or projected fixed significator β=0; and separate mundane semi-arc phase aspects only for proportional semi-arcs. Exact natal Asc/MC angle circles remain exact.
- CLI addition --profile with default body_conjunctions unchanged; --significator-projection explicit only for zodiacal. Unsupported method/latitude options fail closed.
- Synthetic official-SWIEPH four-output packet from two natal instants, provenance-hashed; 36 targeted regression/neighbor tests, ruff and mypy.
- Independent 600-aspect-ray frozen source comparison: 600/600 semi-arc, 600/600 Regiomontanian, 596/600 Placidean; four known AODO sign defect cases (all fully diagnosed), 0 unexplained. This is method-level, not historical-software/full-GUI certification.
- Historical source locators in README derive from the earlier audited purchased Gansten Kindle notes. No fresh text extraction, no verbatim reproduction or stronger attribution than the evidence.
- No participant data, birth-event fitting, time-based empirical predictions, questionnaire modifications, or production HD model changes.

## Follow-on research, without repeating completed steps

Highest-value next engineering stage: historically sourced aspects of the significator, traditional role-reversed converse algorithms, and exact latitude variants (Bianchini's inclined circle vs Morin's orbital correction) only when the primary printed witnesses support precise formulas. Keep normalized mundane, zodiacal and right-ascensional aspects separate. Subsequently check literal Lilly Naibod key tables, lunar secondary motion, terms/bounds and Lot of Fortune.

**Proof boundary:** Mathematical contacts or better engine parity ≠ predictive validity; account for expanded method/branch search-space in later preregistered forward-blind tests.

**Branch:** research/gansten-primary-directions-aspects-20261024
**Parent implementation branch:** research/gansten-primary-direction-timeline-20261024

Run CLI/test commands and research assumptions from README.md; inspect VERIFICATION.json for SHA/provenance.
