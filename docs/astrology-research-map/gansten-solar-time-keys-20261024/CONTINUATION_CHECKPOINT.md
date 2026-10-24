# Gansten solar-RA time-key research continuation checkpoint

Date: 2026-10-24 UTC. Project owner objective (OPEN): accurately calculate historically differentiated Western primary directions and other astrology systems, then freeze candidate interpretations for a separate prospective blind human test with multiplicity controls. Source parity, software reproducibility and predictive validity are separate questions.

Previous baseline: original 1647 Lilly table source comparison (pp.713-715) on research/gansten-lilly-original-1647-correction-20261024, whose 22 year-column corrections and 19°52' worked example must NOT be overwritten or conflated with Naibod mean solar or Placidus variable solar keys.

New implementation:
- SolarRAEngine, direct verified Swiss RA at varying times, true solar midnight H_sun=180° root, Brahe birth-date fixed rate across enclosing true midnights, Placidus cumulative true-Sun RA inversion via bracketing and bisection.
- CLI --solar-time-key is explicit, mutually exclusive with --key, does NOT change prior defaults; works with conjunction, zodiacal/mundane ray and historically separated motion/role families.
- Oversample geometry to 125° before re-timing requested ages (0,100], preventing omission near age limit.
- Synthetic official-SWIEPH examples 2000-01-01 January and 3-season key sensitivity, all file provenance separately hashed. No user/third-party real natal data or event histories.
- Independent Swiss rise_trans lower transit check agrees within ~0.02s on six time points. Placidus inverse residual checks; 85 regression tests PASS; Ruff and mypy pass in 11 source files.
- One initially suspected role-record duplication was a TEST MATCH KEY ERROR: the correct key includes mathematical aspect offset branch (ray_offset_branch versus aspect_offset_branch depending schema). Prior geometric code did not generate duplicate records; fixed in the new test.
- Modern Swiss geocentric apparent true equator-of-date and UT/TT conventions are explicit; no claim the 1573 Brahe or 17th-century Placidus original authors used identical modern timing conventions.

Next owner-aligned action: independently check Brahe and Placidus original computational conventions; run method-specific tests across calendar boundaries and longitude/date extremes; complete original printed Lilly minute/day/hour photographic collation; then freeze interpretations and run *untouched* joint forward-blind human study. Do NOT choose favorable historical keys retrospectively or count geometrically duplicate contacts twice.

Research state: safe engineering package completed, overarching historically complete predictive framework OPEN. No production scorer/participant interview changed.

Branch: research/gansten-solar-brahe-placidus-20261024.
Parent commit: 832747511befe6646a5ad39d779f59bd1a333a27.
