# Hellenistic primary-source C09 — complete printed §44 finer-row audit; partial §37 audit

**23 October 2026.** Source-critical arithmetic only; **0** human predictive validations. Built from C08 without repeating earlier acquisition or the Saturn→Mercury correction. Branch-bound, not merged into the production model.

## Material new direct-source result: all seven Epitome IV §44 finer rows

Examined enlarged pages **264–265** (PDF pages **294–295**) of David Pingree, *Hephaestionis Thebani apotelesmaticorum epitomae quattuor* II (1974). Authorized local study copy SHA-256: `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a`. The edition is the same witness used in C08, **not** an independent new ancient manuscript. No page images or substantial source text are distributed in this repo. Transcription and numerals refer to Pingree's **edited printed body** and its apparatus, not demonstrably to an autograph.

For comparisons, child values are normalized into **Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon** order regardless of the printed sentence order:

| Parent | Primary yearly days (§44 p264) | Printed finer allocation (same planet order) | Sum of finer children | Fine minus primary |
|---|---:|---|---:|---:|
| Saturn | 85 | 20, 8, 10, 13, 5, 14, 16 | 86 | +1 |
| Jupiter | 34 | 8, 3, 4, 5, 2, 5, 7 | 34 | 0 |
| Mars | 42 | 10, 4, 5, 5, 3, 7, 8 | 42 | 0 |
| Sun | 54 | 12, 5, 7, 8, 4, 8, 11 | 55 | +1 |
| Venus | 22 | 5, 2, 3, 3, 1, 4, 5 | 23 | +1 |
| Mercury | 57 | 13, 5, 9, 8, 3, 9, 11 | 58 | +1 |
| Moon | 71 | 16, 7, 8, 11, 4, 11, 11 | 68 | **−3** |
| **Total** | **365** | | **366** | **+1** |

Thus **five of seven** fine rows do not sum to their higher periods: Saturn, Sun, Venus, Mercury and Moon. The previous C08 subset of 3 problematic rows was accurate but incomplete; the new discrepancies are **Mercury 58 vs 57** and **Moon 68 vs 71**. Jupiter and Mars do sum correctly. Even summing all fine rows produces 366 rather than the printed parent total 365; this is a cross-row conservation failure, not simply a rounding convention. Arithmetic **reproduction of this faulty edition** is not proof of a valid historical implementation.

The same printed **Venus 23** fine heading (p265 line 8) conflicts with its primary allocation **22** (p264). Pingree's p265 apparatus specifically reads `legendum κβ` (editorial preference **22**) where the body gives `κγ` (**23**). This **editorial suggestion** does not by itself repair the seven printed children, which sum to 23. The p265 lower apparatus also appears to record a different manuscript-J numeral near the Saturn→Moon child, but that small glyph is held **tentative** pending independent verification; no manuscript-level arithmetic correction is inferred.

## Direct §37 comparison advanced, remaining uncertainty retained

The §37 period list on pp240–241 uses 30, 12, 15, 19, 8, 20, 25 months; the printed figures are **not** automatically a correct application of the chapter's sevenfold approximation. C08's exact Saturn row remains authoritative: `[210,84,105,133,57,40,105]` with literal **40** for Mercury, against **140** derived from the approximation. This correction is not undone.

- **Jupiter's 12-month row**, spanning pp240–241, reads in normalized order `[85,34,42,54,22,57,71]` and sums to **365**, versus 12 × 30 = **360**. Unlike arbitrary scribal discrepancy, **+5** corresponds to the separately printed five-day year supplement. Treat that as a source-consistent possibility, **not** evidence that all other rows use the same rule.
- **Venus's eight-month row**, p241, is preliminarily read in sentence order as `[Venus 15, Saturn 57, Jupiter 22, Mars 28, Sun 36, Mercury 38, Moon 17]`: total **213** rather than **240**. The Moon numeral resembles `ιζ` (17), but this row has **not** been collated against another image/manuscript; it is recorded as preliminary rather than used in an algorithm.
- **Mars's 15-month row**, p241, has six comparatively clear numbers and an ambiguous Jupiter recipient glyph. Reading that single figure as **42** yields **450**; reading it as **52** yields **460**. **Do not** choose 42 merely because 450 closes the expected 15 × 30 days. This is an open **Greek transcription question**, and is carried as a candidate set rather than a forced value.
- **Sun, Mercury, Moon** §37 rows are still **not** fully and independently resolved to printed numbers. No declaration of seven-row completeness is made for §37.

Pingree's p240 apparatus explicitly warns that numerals in this span are corrupt (`numeri nonnulli corrupti`). Distinguish **literal printed body**, **manuscript variant recorded by apparatus**, **editorial suggested correction**, and **modern derived arithmetic**. Do not turn a mathematically convenient reconstruction into a claimed source reading.

## Paulus 34/120 and documentary papyrus — specific verification state

**Boer lead identified but NOT yet a diagram comparison.** The correct editions to inspect are Æ. Boer, ed., *Pauli Alexandrini Elementa apotelesmatica/Eisagogika* (Leipzig: Teubner, **1958**; includes O. Neugebauer's astronomical interpretations), and Æ. Boer, ed., *Heliodori, ut dicitur, in Paulum Alexandrinum commentarium* (Leipzig: Teubner, **1962**; contributions O. Neugebauer and D. Pingree). Library/bibliographic records confirm these distinct editions (1958 is Paulus; 1962 is the attributed Heliodorus commentary). They were **not acquired or examined as facsimile Greek charts during C09**, and the preexisting **34/120 daytime monomoiria conflicts remain unresolved**. Greek source witness and later Greenbaum printed correction cannot yet be chosen as a winner.

**P.Oxy. LXI 4277:** Oxford's Oxyrhynchus images portal explicitly hosts scans of the EES's Oxford-held papyri, and A. Jones's published astronomical papyri provide the existing scholarly reading path. C09 did **not** retrieve/verify the specific papyrus 4277 image. The previous **1/3** agreement from *published textual reconstructions* survives, **not** new image-level parity. No stronger authenticity inference is permitted.

**Source trail** (catalog/context, not a claim of inspected manuscript plate):
- 1958 edition: De Gruyter Teubner bibliographic entry / academic catalogs for `Eisagogika / Elementa apotelesmatica`, ISBN 9783110280678.
- 1962 edition: Stanford catalog `Heliodori, ut dicitur, In Paulum Alexandrinum commentarium`; Google Books bibliographic record with Boer, Neugebauer and Pingree.
- Original papyrus collection: `https://oxyrhynchus.web.ox.ac.uk/images` and `https://www.sds.ox.ac.uk/oxyrhynchus-papyri`; **specific 4277 object not yet opened**.
- Earlier P.Oxy. comparison: `HELLENISTIC_SOURCE_C05_NIGHT_AND_SECOND_PAPYRUS_20261023.md`; C08 witness and report remain source-of-record for corrected §37 Saturn row.

## What was deliberately not done

No human biography consulted; no chart rescored, no human prediction counted, no input/extracted copy of the owner's Gansten Kindle ebook, no Greek source volume copied into Git, no production scorer changes, no cross-tradition map rewrite, no retrospective repair that maximizes fit. These critical-edition numbers must remain source witnesses.

**Next precise tasks:** Verify ambiguous §37 figures (especially Mars→Jupiter) against a separately printed/independently collated Greek witness; examine Boer 1958 and 1962 original §2/§32 tabular apparatus to adjudicate the 34 disagreement cells; find and visually read an authorized image of **P.Oxy. 4277** before changing papyrus reconstruction status. All historical human validation = **0**.

[Machine-readable C09 source witness](HEPHAISTIO_C09_FULL_FINE_PERIOD_AND_OPEN_GLYPHS_V1.json) · [C09 arithmetic and preservation tests](test_hellenistic_c09_greek_subperiods.py)
