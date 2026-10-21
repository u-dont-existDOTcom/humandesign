# Tibetan astrology source and calendar research — T51–T53 (21 October 2026)

**Owner's root astrology project: OPEN.** This is source-documentary work and mathematical/engineering partial implementation. It is **not** demonstrated human predictive validity. Owner authorizes reading the free and three supplied Tibetan sources across turns, maintaining cross-system source separation and ultimately independently calculated, frozen forward/reverse blind tests against decoys and conventional controls. Work belongs in `humandesign`.

## Durable accepted parent, source coverage, and new evidence

- Accepted prior Tibetan checkpoint: `research/astro-tibetan-t36-query-illness-20261021`, exact commit `18695e89dc9cda3dbe3643c1db966e25a7e31b8c`, **447** original documentary annotations (TIB-R0001–0447). Eight-plus focused suites and global ID audit had passed on the owner laptop. No human blind tests.
- This pass adds **41 contiguous source annotations**: **T51** Cornu **24** (R0448–0471) and **T52** Janson **17** (R0472–0488). Cumulative documentary annotations: **488**. T53 adds no new historical claim count; it is code, source fixtures and checks. Existing registries and Western/Chinese/Jyotish file indexes remain unmodified.
- Cornu source witness: user-uploaded *Tibetan Astrology* (Hamish Gregor English), SHA256 `8c7a7d8eb4f9d11793d02f1667979363cf520b02754365390f8e966a4452c472`. Source reading examined modern Jungtsi/Naktsi and Kartsi method sections, five elements/personal forces, lunar mansions, double hours, and horoscope worked pages; important physical two-up PDF anchors T51. **This is not a claim that every Cornu page is exhausted.**
- Janson witness: *Tibetan calendar mathematics*, revised 2014, free author's scholarly article `https://arxiv.org/html/1401.6285v1`. Exact sections/equations 5.2–5.9, Appendix A.2 and E.1–E.4 read. This is a modern mathematical derivation **partly based on Henning and Schuh**, not independently translated original Tibetan prose and not independent corroboration of chart predictions. See T52 source notes.
- Source text/PDF bytes not copied into Git, only author-generated code, paraphrased annotations, tests and provenance.

## Newly executable source-derived calculation subset

Source code: `batches/T53/tibetan_calendar_reference.py`. Source-derived and tested inputs/outputs, with **no default calendar policy**:

| Calculator | Supported inputs | Outputs | Source/limitations |
|---|---|---|---|
| Tibetan year features | Explicit **Tibetan year-start label** (Gregorian year of Losar, not current Gregorian civil year by assumption) | Animal, Wood/Fire/Earth/Iron/Water power, five personal elemental aspects, masculine/feminine **year polarity**, natal central/life/power mewa | Janson E.1/Table23; no Losar discovery or birth-date conversion |
| Phugpa/Tsurphu month features | Year label, Tibetan month 1–12, explicitly selected calendar policy | Month animal, element, polarity and Tsurphu-specific month mewa | Janson E.2. **Phugpa month 1 = Dragon, Tsurphu month 1 = Tiger** |
| Phugpa/Tsurphu lunar-day features | Year label, Tibetan lunar month, tithi index 1–30, calendar policy | Lunar-day animal, element, trigram, mewa | Janson E.9–11; **lunar day ≠ civil calendar day**, can skip/repeat as civil date |
| Julian-day *calendar-day* attributes | Already resolved integer **JDN** and chosen calendar policy | Day animal/power/body/life/fortune/spirit, polarity, trigram, Phugpa mewa | Janson E.12–16. **Tsurphu daily mewa deliberately UNKNOWN** pending solar-solstice calculations; **JDN is not Julian Date/UTC timestamp**; no dawn resolver |
| Leap months | Tibetan year label, month, explicit Phugpa/Tsurphu policy and epoch | Intercalation index, leap flag, regular/leap true-month counts | Janson 5.2 and Appendix A.2, explicit Phugpa β* 61/55/0 at epoch806/1927/1987 and Tsurphu 59/14 at epoch1732/1852. Independent 65-year count invariant |
| Hour element from lunar day | Precomputed lunar-day element and **supplied traditional double-hour animal**, not raw civil time | Element following standard generating cycle, Hare first the son's element of day | Cornu printed pp115–116. Civil time/longitude, DST and Tibetan dawn boundaries still unimplemented |

**This is not a complete calendar or natal horoscope engine**: does not compute actual lunar/solar elongation, Julian day at the Tibetan local dawn, any Tibetan civil date from UTC, month-day skips/doubles, ayanāṃśa, zodiacal planetary positions, houses, or participant predictions. A correct partial calculation from already determined Tibetan dates can still be the wrong chart if the supplied date/time conversion is wrong. No astrology runtime model promotions were made.

### Source parity cases actually tested

Focused executable test: `verify_t51_t53_calendar.py`; includes previous `verify_global_source_registry.py` asserting 447 older IDs unchanged.

1. Cross-checked Janson 60-year Table23 body-element entries for every sexagenary position; checked 60-year elemental and 180-year combined mewa cycles with additional invariants.
2. Cornu 1950 Nov15 Paris worked year: Tibetan **Iron Tiger**; power Iron, life/body Wood, fortune Iron, spirit Water; central Mewa **5**, life **2**, power **8**.
3. Cornu same example Tibetan month **10 Water Ox**, lunar day **6 Wood Ox** with lunar-day mewa **3** (first day mewa **7**), and **Fire** hour element when the supplied traditional hour is Monkey. These are exact symbolic source matches; **the civil→Tibetan date and hour input have not yet been independently recomputed**.
4. Janson 1984 Tibetan **Wood Mouse**, natal 7; 1958 **Earth Dog** with natal6/life3/power9. Janson published Phugpa Losar table: 1984 Mar3, 1985 Feb20. Treat 1985 dates before Feb20 as belonging to the still-running 1984 Tibetan year under that published table, rather than selecting the Gregorian civil year.
5. All **24 Phugpa and 24 Tsurphu** leap-month placements per 65 Gregorian Tibetan-year labels, each named month 1–12 twice, with Phugpa leap ix48/49 and Tsurphu ix0/1. Checked that the 3 supported Phugpa epochs agree on leap placement and the 2 Tsurphu epochs agree internally; month counts have consistent one-month leap/regular separation.
6. Janson E.4 checked **500 consecutive known JDN values** for daily animal/element/trigram/mewa cycles and separated Phugpa from Tsurphu daily mewa. Janson gives 2007 Jan1 JDN2454102; a proleptic Gregorian date-to-integer identity is used only as a test, not as a Tibetan calendar-date conversion.
7. Invalid input/policy/cycle routes reject silently invented values: unknown epoch, 13th month, 31st lunar day, unspecified traditional double-hour, float birth year.

### Two newly recorded Cornu worked-example problems

Cornu's printed pp216–220 1950 example is useful as a source target, **not** a trusted UTC reference chart:

- Book's text calls subtracting 1 hour from Paris 17:00 civil time “local solar time = 16:00,” then adding ≈9 minutes longitude “GMT = 16:09.” Historical IANA `Europe/Paris` at **1950-11-15 17:00 is UTC+01:00**; actual **UTC = 16:00**. With Paris longitude 2.3522°E, **local mean solar = 16:09:24.528**, not GMT. This is an explicit distinction of clock systems; an apparent solar time would add a separately documented equation-of-time correction. The example time-source labels are swapped/conflated. No attempt to refit actual planetary positions using the mislabeled value.
- Book printed p220 (two-up scanned source) writes `(1950−285) × 0.014 = 23.31 = 23°81′`. The right-hand sexagesimal formatting is invalid (minutes ≥60): **23.31 decimal degrees = 23°18′36″**. This is a correction of notation/arithmetic inside Cornu's historical approximation, not a claim that the adopted 285 CE sidereal zero point or annual precession rate is physically correct.

These issues are registered as **TIB-CONFLICT-010** (historical UT/LMT labeling) and **TIB-CONFLICT-011** (invalid DMS), distinct from TIB-CONFLICT-001–009 in the earlier source lane. Correct source computations from other books should not silently override Cornu's documented wording.

## Cross-system implications for HumanDesign study

- **Inheritance/dependence:** The 12 animals, 60 year-pair cycles, five elements, animal-group fortune/life forces and some trigrams/nine squares overlap Chinese BaZi/GanZhi and related Chinese calendrical practices. The 27 lunar mansions and sidereal projection overlap Indian Jyotish. Shared input formulas do not count as independent natal predictions, and neither source has yet passed any blinded human outcome test.
- **Source variant pre-registration:** Phugpa and Tsurphu month-animal and month-element rules differ, so if we tested behavior retrospectively and chose the better fit we'd contaminate the test. Calendar variant must be fixed independently from observed personality data. Cornu versus Erlewine Papme year-polarity versus subject-sex switching remains another separate preregistered candidate (prior T31).
- **Features suitable for future natal arm:** birth-derived animal/element groups, mewa, trigram, planetary lunar mansions **only after** verified UTC↔local-day Tibetan calendar engine and source-specific horoscope map. Parent/household/consultation-time and funeral/ritual outcomes must remain separate question classes. Do not infer high-stakes health/relationship/mortality from astrological source statements.
- **Scientific gap:** Zero human participants tested prospectively, no held-out predictions scored, no false-positive/negative results established. Literature notes and a chart calculator's internal tests are *not* predictive success.

## Next most useful executable frontier

1. Independently implement Janson **Sections 6–9** (mean/“true” Sun/Moon positions, lunar/civil day association, skipped and repeated days), then run parity against existing named open-source reference calendar implementations (e.g., MIT implementations by hnw/date-tibetan and dorjeduck/tibcal **after verifying upstream code/versions**), almanac examples and Henning's printed numeric worked examples. Remain explicit about leap-month and dawn/longitude conventions.
2. Finish Cornu remaining interpretive/electional source chapters and Henning I–V; check historic local standard-time and apparent/mean-solar distinctions. Read the remainder of Erlewine free manual and Janson, including the full daily-attribute and original-source commentary.
3. Only after independent astronomical and calendar parity compute Tibetan natal feature sets for synthetic, then frozen untouched participants, with birth policy, calendar variant, day boundary, source rule weight, and non-astrology baseline fixed **before** answers.

Parent task remains OPEN. Source annotation continuation **TIB-R0489**. Entire work kept inside `humandesign` research branch; no purchase, deployment, raw human data, copyrighted PDFs, or model promotion.
