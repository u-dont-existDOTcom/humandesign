# Gansten / Lilly / Naibod timing checkpoint — 2026-10-24

## Parent goal (OPEN)

Accurately calculate historically distinct natal astrology systems and test their independently frozen predictions jointly in blinded human cohorts. This timing-table work advances mathematics and source provenance; it does NOT demonstrate prediction accuracy.

## Completed in this work package

- Located Lilly's Naibod conversion table in an accessible **2003 re-typeset copy** of Christian Astrology Book III, printed pp.713–715, corresponding to PDF zero-indexed pages 226–228. Visually checked degree and minute tables and both printed worked examples. The *1647 first-edition page images were not independently verified*. Beware falsely attributing the 2003 witness's numerical flaws to Lilly's original print.
- Added historical_naibod.py: strict, literal diagnostic lookup using 90 printed degree rows and 59 of 60 minute rows (27' missing), preserving source anomalies. The literal source table is not a continuous rate and is intentionally NOT a TimeKey.
- Two worked examples: 11°55' = **12y33d14h** exactly as source example; 19°52' arithmetic = **20y57d21h**, while final prose reports **22y57d21h**, a 2-year discrepancy in the 2003 witness. Multiple source-table anomalies are documented with no silent repair.
- Added two independently labeled continuous **diagnostic** keys: exactly 59'08" arc/year, and exact rational 360/365.25 degrees/year. Both remain distinct from the existing 1°/year and 360/365.2422 diagnostics, and neither is identified with Lilly's unverified literal printed table.
- Source digitization CSV, anomaly register and 75° key sensitivity examples, plus two synthetic Swiss-file outputs with the new keys. Legacy outputs and defaults unchanged.
- Recorded source PDF URL, source text status and SHA-256. No human life-event data were used. No production chart scorer changes.

## Assurance / status

61 relevant regression tests PASS. Ruff and mypy PASS. Tests cover source rows, missing cell, printed arithmetic, carry behavior, numerical timing rate contrast, original frozen outputs, role and aspect profiles, and Swiss-file provenance. Git branch and exact reproducibility manifest are recorded in VERIFICATION.json.

## Next safe research action

Independently inspect ORIGINAL printed 1647 or contemporary Lilly pages 713–715 to distinguish printing errors from modern transcription errors. If the original changes a value, retain the 2003 witness as a distinct record and update traceably. Separately implement Brahe's day-at-birth solar RA key and Placidus accumulated solar RA key with strict SWIEPH and clear UT/TT/calendar/meridian conventions. Neither timing method is completed here.

Keep historical attribution, numerical implementation correctness and actual empirical prediction power as SEPARATE validation states. Do not silently select the historical variant with the most attractive hindsight match.

**Research branch:** research/gansten-lilly-naibod-time-keys-20261024

**Parent state:** OPEN; bounded table-source subtask COMPLETE.
