# Tibetan source-study continuation after T53 — 21 October 2026

**Owner request verbatim:** "ok then start reading everything you need that's free plus these, in turns, to merge into the other readings we are doing for astro system". Subsequent owner instructions repeatedly "continue". Root outcome **OPEN**: source-study Tibetan + Western Lilly/Ptolemy + Indian Jyotish + Chinese BaZi/Zi Wei; build actual independently verified birth-date/planet/chart feature engines and freeze/score prospective blinded human predictions vs matched decoys and non-astrology controls. Completion requires scientific owner outcomes, not total historical notes or passes of synthetic tests.

## Accepted parent and new work

Predecessor accepted Tibetan T01–T50 branch: `research/astro-tibetan-t36-query-illness-20261021`, exact GitHub commit `18695e89dc9cda3dbe3643c1db966e25a7e31b8c`; **447** historical documentary source notes, independent ID checker/test green. New branch: `research/astro-tibetan-t51-cornu-janson-math-20261021`, created from exact predecessor. Exact current remote commit SHA MUST be retrieved again after this note and source/test commits, not inferred from this prose. Owner laptop worktree:
`/mnt/hdd/storage/joel/development-worktrees/humandesign/astro-tibetan-t51-cornu-20261021`.

Current documentary count **488**, new **41**: T51 Cornu 24 new notes TIB-R0448–0471 and T52 Janson 17 new TIB-R0472–0488; T53 = testable calculation subset, **0 additional historical notes**. All other accepted source notes T01–T50 preserved. Source PDF material not in repo.

New source files in `tasks/astro-tibetan-primary-sources-20261021/`:
- `batches/T51/CORNU_JUNGTSI_KARTSI_WORKED_24_NOTES_V1.json`, Cornu English *Tibetan Astrology*, PDF numbered spreads and printed chapter/figure anchors; user uploaded PDF witness SHA256 `8c7a7d8eb4f9d11793d02f1667979363cf520b02754365390f8e966a4452c472`.
- `batches/T52/JANSON_CALENDAR_17_SOURCE_NOTES_V1.json`, free Svante Janson `https://arxiv.org/html/1401.6285v1` §§5.2, A.2, E.1–E.4; this paper is modern mathematical reconstruction using Henning/Schuh and almanacs, NOT independent Tibetan primary translation.
- `batches/T53/tibetan_calendar_reference.py`, source-based **limited** working calendar-symbolic attributes. Derives year animal/power/life/body/fortune/spirit and mewa; Phugpa or Tsurphu month animals/elements/numerals; lunar-day attributes; selected integer-JDN calendar-day attributes; explicit leap-month indices under alternate epochs and policies; Cornu double-hour element once correct traditional hour animal is supplied. NOT a civil timestamp/date-to-Tibetan calendar date or a full astronomical or chart engine, and no human prediction validation.
- `batches/T53/CALCULATOR_SOURCE_PARITY_AND_1950_ERRATA_V1.json`, exact source rules, fixtures, unresolved input boundary, Cornu worked example time/angle issues.
- `verify_t51_t53_calendar.py` — runnable focused test with independent source Table23 all 60 year-body features, all 180 combined states, Cornu 1950 month/day/hour, Phugpa/Tsurphu 65-year 24-leap invariants, JDN 500-day and fail-closed policy input tests, and 1950 IANA timezone and 23°81′ source error. It imports but does NOT modify the previous `verify_global_source_registry.py` (447 prior IDs).
- `CROSS_LANE_INTEGRATION_T51_T53.md` — full cross-system summary and science boundaries; this handoff.

## Verification already performed (must reread exact final commit after publishing)

From task folder:
`python3 verify_t51_t53_calendar.py`
Actual output:
`T51–T53 PASS: 41 contiguous new documentary notes (TIB-R0448–0488), 60-year Table23 parity, 1950 Cornu birth year/month/day/hour, Phugpa/Tsurphu leap-policy 24/65, UTC/LMT and invalid DMS source boundaries, prior 447 notes unchanged; ZERO human predictive results.`
The generated test is source/internal engineering evidence only. Re-run on final remote GitHub fetched branch and verify no files outside Tibetan task tree changed.

## Scientific boundary and newly identified source problems

- **TIB-CONFLICT-010 (Cornu worked time):** Paris civil **1950-11-15 17:00 Europe/Paris** = **16:00 UTC** under historical zone. Local mean solar at longitude 2.3522°E = approximately **16:09:24.528**. Cornu English printed pp216–219 labels 16:00 “local solar,” 16:09 “GMT”: conflated/swapped; cannot treat 16:09 as unambiguous birth UTC golden.
- **TIB-CONFLICT-011 (Cornu DMS):** book prints 23°81′ for `(1950−285)×0.014 = 23.31°`; decimal correct is 23°18′36″; this is a notation correction *within Cornu's approximation*, not empirical verification of ayanāṃśa.
- Phugpa month1 **Dragon** vs Tsurphu month1 **Tiger**; leap indices Phugpa48/49 vs Tsurphu0/1; distinct policies. Gregorian civil year cannot substitute for actual Tibetan year label before Losar. Tsurphu daily mewa requires solstice reversal; leave UNKNOWN. Janson's theoretical "true" longitudes are not modern exact ephemeris.
- Cornu vs Erlewine Papme year-polarity vs native's sex conflict (prior T31) remains unresolved; do not fit model by an already-known person.
- BaZi/year signs, Chinese mewa/parkha and Indic nakshatras overlap source mechanisms: no double counting, only preregistered incremental tests. New user actual human validation: **zero**.

## NEXT executable work, no repetition

**Next historical note TIB-R0489.** Main owner gap remains: full traditional date/time and natal chart engine, source-complete readings, frozen blind human test.

1. Extend the limited Janson reference calculator with §§6–9 full mean/true Sun/Moon/weekday/dawn and local-day calculations (Phugpa and Tsurphu separately). Compare to published almanacs, Henning golden examples, and independently verified MIT open-source implementations (candidates `hnw/date-tibetan` and `dorjeduck/tibcal`, not yet imported or assumed correct). Preserve exact calendar policy, observer locale and historical timezone/DST provenance.
2. Complete Cornu remaining instructional/electional chapters beyond sampled pp33–120, Henning I–V and the rest of VI, free Erlewine and full Janson; obtain original Tibetan alternative manuscripts to resolve known source conflicts. Source uncertainty is not permission to invent formulas or select posthoc a favorable variant.
3. Once date calculation parity is independent and passed, compose Tibet-specific natal/annual features with shared Western/Jyotish/BaZi/ZiWei dependency caps, freeze testable rules, run blinded human prediction versus decoys and baselines with explicit misses.

All work in `humandesign`, no unrelated files edited. No copyrighted PDFs, private participant data, paid actions, medical/mortality/safety advice or live model promotions.
