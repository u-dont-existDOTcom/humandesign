# Jyotish research B35 checkpoint — 2026-10-21

Branch: research/astro-jyotish-five-sources-reader-20261020 (draft PR136). Accepted source annotations: **407**, not observed horoscope successes.

B34: original Sanskrit Saravali Ch35.58 and Ch35.144 duplicate a royal yoga, modern English 35.57 and 35.143 conflict over Moon's house. Older printed Sanskrit preserves verses corrupted by CSU/Wikisource digital text.

B35: two more original source claims in SOURCE_CANDIDATES_B35.json; whole-sign geometry and six-exaltation subset enumeration in WHOLE_SIGN_GEOMETRIC_EMPTY_YOGAS_B35.json and READING_NOTES_B35.md. Sun H7/Mercury H2 requires 120 degrees, exceeding ~28-degree separation; Sun H4/Venus H1 needs 60 degrees, exceeding ~48-degree limit. Conditional to whole-sign, not all Bhava interpretations. Of seven six-planet exalted subsets only omission of Mercury is not excluded by these simple tests. No actual human horoscope was tested.

whole_sign_geometry_B35.py and test_whole_sign_geometry_B35.py are byte-identical to locally tested source, six unit tests passing. No model edits.

Next: source-critical and sky geometry checks on other unusual royal-yoga rules. Keep branch isolated, no raw copyrighted books publicly uploaded.
