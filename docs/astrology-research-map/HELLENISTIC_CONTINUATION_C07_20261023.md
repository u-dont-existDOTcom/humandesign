# Hellenistic source-research continuation checkpoint C07

23 October 2026 — **research still OPEN**, current human predictive validations **0**; isolated historical source-reading branch.

## Original task authority

Continue reading and comparing historical astrology books and source variants for eventual frozen, blinded empirical testing. Save all useful work in `humandesign`. The owner purchased Gansten *Primary Directions* as a separate Amazon ebook and is **not using Work mode to extract it**. No such extraction occurred. No human natal chart or biography was used to choose a reading; no predictions were frozen, evaluated, or promoted; no deployment, paid action, or change to other Jyotish/Chinese/Tibetan/Maya research lanes.

## Current source record

- Root reading report: [C07: Hephaistio's five-day manuscripts and Epitome IV](HELLENISTIC_SOURCE_C07_FIVEDAY_CALENDAR_MANUSCRIPTS_20261023.md) — includes source-grade comparison, exact edition/page references and chronology.
- Data witness 1: [main Book II.29/36 and P/P² Greek five-day/marginal register](HEPHAISTIO_C07_FIVEDAY_MANUSCRIPT_AND_CALENDAR_V1.json).
- Data witness 2: [Epitome IV 140/365 separate-recension register](HEPHAISTIO_C07_EPITOME_IV_INDEPENDENT_RECENSION_V1.json).
- Focused tests: [main five-day and 360/365 tests](test_hellenistic_c07_fiveday.py), [Epitome IV approximation and 365 tests](test_hellenistic_c07_epitome_iv.py).
- Prior checkpoints C01–C06 retain their historical results; current canonical cross-tradition source map entry remains `README.md`. No competing architecture map was created.

### What was newly READ and verified this turn

1. **Pingree Greek critical Volume I (1973)**, SHA256 `f2f803c457b7ba62df23f5c51d6f49ffff3644e17723c6673f5795298514ecae`: actual source Book II.29 at printed **p201** says include a five-day period alongside each year's twelve months, and later manuscript **P²** margin reinforces this; **P** is Parisinus graecus 2417, 13th century shortened text, **P²** is 14th-century corrector (Latin prefatio physical pp11–15). The Book II.36 p225 apparatus notes **P adds a 365-day reference** to its timing description, while editor still notes `νβ desid.` (expects Mercury 52 where edited fine heading prints 57). Not a separate ancient authorial confirmation.
2. **Pingree Greek Epitome IV Volume II (1974)**, 524-page research PDF, SHA256 `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a`, **80,704,330 bytes**, printed **pp240–242 and 264–265**, PDF pages **270–272 and 294–295**, actually rendered and visually checked. Epitome IV is a different but related *textual family* (critical preface Volume I pp XX–XXI), **not an independent astrologer**. The original Volume II itself has not been distributed.
3. **Three key corrections from Epitome IV**: section **37 p240** assigns **140 days** Saturn→Mercury whereas main Hephaistio II.29 assigns 150. Section 37 **p241** derives an approximately seven-day multiplier from Saturn's **30 months = 900 days** divided by total **129 months**. Its seven period-weight outputs `[210,84,105,133,56,140,175]` sum **903**, the +3 explained by rounding 900/129 to 7. It warns of corrupt numbers in its apparatus; do not promote “140 original authorial autograph” even though the later Valens appendix likewise gives 140. Section **37 p242** explicitly instructs including five days with each twelve-month year. Section **44 p264** explicitly states counting the year as **365 days**; prints headline periods `85,34,42,54,22,57,71` summing **365**. Main edited Hephaistio II.36 instead first gives `85,34,42,54,22,52,71` = 360. Epitome IV is therefore a genuine **365-day recensional procedure**, not merely an arithmetic guess.
4. **Main source-only numerical fit** of the seven II.29 child-subperiod sums: summed absolute error **42 days** under 360-day year vs exactly **263/12 = 21 11/12 days** under proportional 365-day-year assumptions. Mars and Sun remain incompatible with simple rounding; fit is NOT proof of which manuscript is correct. Epitome IV's explicitly approximate Saturn row differs from this general main recension (903 versus main original 913).

### Verifications

**45/45 deterministic source-only tests PASSED** after a clean isolated **GitHub sparse clone** of current research branch and a `python3 -m unittest discover -s ... -p 'test_hellenistic_*.py' -v` run, exit 0. C02–C06's 36 tests plus C07's 5 main-text and 4 Epitome IV tests. Initial GitHub anonymous API fetch was rate-limited (403), so the validated alternative was a fresh sparse Git clone, not a test run on contaminated older local files. This verifies recorded historical numerals/method implementations, **not astrology efficacy**. Production scoring and human-validation registers unchanged.

### Other source probes

- **Paulus**: independently verified bibliographic critical editions *Elementa apotelesmatica* (Ae. Boer 1958) and *Heliodori, ut dicitur, In Paulum Alexandrinum commentarium* (Ae. Boer 1962), needed to resolve the 34/120 Greenbaum corrected-day versus reconstructed Greek-prose conflict. No independent ancient night table was falsely claimed to have been read.
- **P.Oxy. LXI 4277**: Oxford portal search returned HTTP 403, so no authentic original papyrus image was read; C05's monomoiria 1/3 and C06's separate zodiacal-place text attestations remain untouched.
- No re-inspection of purchased Amazon Kindle *Primary Directions*, no new purchases.

## Exact next useful reading (no duplicate work)

1. Compare Epitoma IV and any alternative epitome 365-day algorithms *beyond just headline totals*, mapping how five epagomenal days are added vs distributed to child periods, including explicit ancient approximation and manuscript corrupt readings; preserve as named separate implementations, don't retrofit life histories.
2. Trace Boer 1958/1962 Greek tables and diagrams for Paulus and supposed Heliodorus/Olympiodorus commentary to classify the **34/120** narrative vs editorial day-canon disagreements; do not simply treat later reconstruction as an ancient manuscript.
3. Find securely attributed original papyrus/first-edition evidence for P.Oxy. 4277 and expand untouched **historical calculation** checks without optimizing to scribal matches.
4. Only once independent chart/rule arithmetic and contrary outcomes are frozen can prospective human tests (separately authorized empirical study) be considered; no score promotions from source restoration.

**One-line resume:** C07 already established Epitome IV 140, the explicit annual five-day instruction, and 365 year; resume by comparing epitome *detailed child-period allocations*, then Paul's table transmission. Do not repeat Vol I/II downloads or source location searches. Keep the root scientific outcome OPEN.
