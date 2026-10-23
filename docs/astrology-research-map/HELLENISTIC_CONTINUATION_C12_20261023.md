# Hellenistic astrology C12 — durable source continuation

**23 October 2026. Research objective: OPEN. Human predictive validations: 0.** Source-critical comparison only; no production scoring changes.

## Bootstrap and research state

Read live `u-dont-existDOTcom/universal-dev-architecture/AGENTS.md` and `LESSON-INDEX.md`, then `u-dont-existDOTcom/humandesign/AGENTS.md`. Read this checkpoint and the C12 report; do not redo C01–C11.

- **New isolated branch:** `research/astro-hellenistic-c12-munich-paulus-20261023`
- **Exact C11 base:** `fbd382beb7df52a5e857b8fdf3a58a4dae226792`, research branch `research/astro-hellenistic-c11-recension-20261023`.
- **Original research integration branch:** `research/astro-missing-book-audit-20261022`. Child branch not merged into production.
- **C12 evidence:** [report](HELLENISTIC_SOURCE_C12_MUNICH_FIRST_OCTET_20261023.md), [source register](PAULUS_C12_MUNICH_FIRST_OCTET_SOURCE_WITNESS_V1.json), [comparison module](paulus_munich_first_octet_c12.py), [nine source-only tests](test_hellenistic_c12_munich_first_octet.py).

## Actual new source evidence

Munich Bayerische Staatsbibliothek **Cod. graec. 170**, handwritten **p65** (digital image **00081**), is a sixteenth-century manuscript carrying Paulus and scholia, not a late-antique autograph. Examined original and magnified IIIF image; not redistributed.

The four table columns are **triplicities**, each listing three zodiac signs, rather than four independent signs:
Fire Aries/Leo/Sagittarius; earth Taurus/Virgo/Capricorn; air Gemini/Libra/Aquarius; water Cancer/Scorpio/Pisces. This clarifies the incomplete column-label description from C11.

The original **first eight degree glyphs** of each of the four columns were read, **32 manually observed source cells**. They follow four diurnal ruler pairs rotated to the current triplicity **without skipping Venus's second appearance**. Every first octet has **two Venus assignments** and seven distinct planets. This is a *manuscript observation* and does not establish a canonical eightfold system. Day designation is **inferred** from fire Sun/Jupiter and earth Venus/Moon; Greek rubric still needs independent exact reading.

Of 34 previously disputed Greenbaum corrected day versus C05 narrative cells, **9 occur in these first eight**. Eight visible cells match the narrative (air 3–6, water 1–4); **water 8** matches neither (manuscript Mercury, narrative Venus, Greenbaum Mars). All such counts are witness-specific, **not astrology's predictive validity**.

## Remaining source gaps and restrictions

- **25 of 34** previously disputed cells have **not** been individually re-read here. Do not extrapolate manuscript degrees 9–30 from the first octet; their patterns and possible scribal irregularities require their own image-based transcription.
- The tiny manuscript rubric about sect is not fully deciphered. Boer's 1958 Paulus and 1962 Heliodorus/Olympiodorus Greek diagrams/apparatus remain unread in this lane. P.Oxy. LXI 4277 original photograph remains unverified, with prior C05 **1/3** scholarly-text computational agreement and **two negative cases** retained.
- C11 corrected false-green C10 Sun→Sun to **83**, Sun subdivision total **531**, not 130 and 578. Main Saturn→Mercury **150**, Epitome literal **40**, derived **140** remain distinct. Epitome IV §44 365 parent /366 finer remains unresolved. Venus→Sun is **36 in both** main and Epitome, unlike the different-direction Sun→Venus **35**.
- No Gansten purchased Kindle extraction using Work; no biography-based fitting, human model promotion, scoring, or modifications to other traditions' cross-system maps.

**Next executable investigation:** Finish handwritten Munich table degrees 9–30 *by actual independent glyph reading*, verify sect/rubric in p64–66, then compare all 34 previously disputed cells to Boer 1958/1962 once the original Greek is available. Preserve ambiguity and textual negatives rather than selecting a variant by numeric closure or personal fit.

Exact test:
```sh
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```
**C12 verified test receipt: 86/86 PASS**, 77 retained + 9 new C12, command exit 0 from the isolated C12 worktree. **0 human predictions.**

**Resume one-liner:** C12 manuscript first-eight yields duplicated Venus and nine locally inspectable disputed cells (8 narrative, 1 neither); finish 9–30 and confirm sect without inventing a universal eight-cycle.

## C13 supersession notice — full-page inspection supersedes only C12's '25 unread' boundary

The C12 first-octet observation remains preserved unchanged, but **do not generalize its eight-slot pattern**: C13 directly inspected manuscript degrees 9–30 as well. In the resulting 120-position image-based registry, **119 labels are tentatively identified, earth degree 28 remains indeterminate**. Source evidence contradicts a simple eight-position repetition for **water degrees 9–30** and earth degrees 29–30. All 34 previously disputed narrative-versus-corrected-table cells have now been compared within *this one manuscript*: **11 narrative-only, 1 corrected-only, 22 neither**. This is not a decision that either version is original/authentic, and does not change model scoring. See [C13 research report](HELLENISTIC_SOURCE_C13_MUNICH_120_IMAGE_COLLATION_20261023.md) and [C13 recorded glyphs](PAULUS_C13_MUNICH_120_POSITION_IMAGE_TRANSCRIPTION_V1.json).
