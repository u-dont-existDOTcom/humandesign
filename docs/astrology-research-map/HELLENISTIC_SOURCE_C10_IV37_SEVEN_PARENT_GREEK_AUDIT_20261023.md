# Hellenistic primary-source C10 — Epitome IV §37 full seven-parent printed-edition arithmetic, uncertain glyphs retained

**23 October 2026** · **Source/edition research only.** No historical-person chart fitting, human validation, rule acceptance, horoscope scoring or copying of the Gansten Kindle ebook. C09 remains the valid full §44 finer-level audit; C10 extends §37 instead of repeating C08–C09 acquisition and correction work.

## Source actually examined

The same authorized local research PDF of David Pingree's edited Greek *Hephaestionis Thebani apotelesmaticorum epitomae quattuor*, vol. II (1974), file SHA-256 `6ee168a3a39d414620b7c820145c1ffe06dd437617bf79fdc6c9842f51c47f8a`, printed **pp240–241** (= PDF **pp270–271**). Original image-rendered pages were re-read at 360–600 dpi (not OCR); close-ups focused on numeral rows and their overbars. Neither these page images nor the PDF are deposited. This remains **one twentieth-century edited Greek witness**, not a collated independent ancient manuscript.

Pingree explicitly warns in p240 apparatus, applying through p241 line 14, that some numbers are corrupt (`numeri nonnulli corrupti`). Therefore source-number audit, numerical sum, plausible textual restoration and an algorithm chosen for actual charts are distinct tasks. No coherent §37 model is inferred from the following mismatches.

## Novel C10: all seven printed §37 parent rows mapped, without manufacturing exactness

Columns use **Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon** recipient order, independent of the order printed within each Greek sentence.

| Parent | Parent period | Printed edited values, normalized | 30-day-month total | Sum of printed values | Difference |
|---|---:|---|---:|---:|---:|
| Saturn | 30 months | 210,84,105,133,57,**40**,105 | 900 | **734** | −166 |
| Jupiter | 12 | 85,34,42,54,22,57,71 | 360 | **365** | +5 |
| Mars | 15 | 105,**52?**,52,66,28,70,87 | 450 | **460** preferred visual; **450** if alternative 42 | +10 or 0 |
| Sun | 19 | 104,52,64,83,30,80,118 | 570 | **531** | −39 |
| Venus | 8 | 57,22,28,36,15,38,17 | 240 | **213** | −27 |
| Mercury | 20 | 141,57,70,90,36,96,117 | 600 | **607** | +7 |
| Moon | 25 | 177,71,87,**?**,47,119,148 | 750 | **764 or 794** | +14 or +44 |

Numeral strings recorded above are **editorial printed-text readings**, NOT a proposed new coherent distribution. There are **two live numeral ambiguities** in this pass; the additional rows are provisional edition readings until separately collated, with Mercury's 90/96 signs especially deserving checking.

- **Mars→Jupiter**, p241 approx. l2: At 420/600-dpi enlargement the printed glyph looks more like **νβ = 52**, matching the visual form of Mars's own **νβ = 52** in that same line. C09 had not chosen between **μβ = 42** and **νβ = 52**. Choosing 52 makes the total **460**, not the nominal 450. Record **52 as the current printed-edition visual preference, 42 as an explicitly retained alternate**, but do not resolve manuscript-level authenticity from the numerically less convenient result. This is a **change in visual interpretation**, not a second independent Greek witness.
- **Moon→Sun**, p241 approx. l13: Close-up has a similar ambiguity between **ριε = 115** and **ρμε = 145**. Conservatively preserve **both**, totaling 764/794; do not claim one as established by an ancient copy or give the Moon one fabricated exact sum.

**C08/C09 controls remain intact:** §37 Saturn→Mercury literally printed **40**, while the separate 7× numerical approximation calculates **140**; main Hephaistio II.29 prints **150**. §44 primary sums **365**, its complete finer children sum **366**. The fact that some §37 numbers nearly equal 30-day period estimates is not a license to change others silently. Jupiter's +5 still has an independently attested five-day annual supplement explanation, but that does not rescue the other rows.

## Independent witness investigation status

1. **Æ. Boer 1958 Paulus:** bibliographically verified as *Pauli Alexandrini Elementa apotelesmatica / Eisagogika*, Greek/Latin edited work, xxvi + 181 pp., including Otto Neugebauer's astronomical interpretations. *The Greek Library* corpus v2.3.0 newly located a catalogue entry `tlg2053.tlg001.local001` citing Boer 1958, printed pp1–100, but **the text/diagram was not accessible during this C10 pass**. The bibliographic record is **not** a verified figure reading. The main unresolved **34/120** daytime narrative/Greenbaum cells are unchanged.
2. **Æ. Boer 1962 attributed Heliodorus commentary:** verified Greek edition with Neugebauer and Pingree. Reviews by **Dain (1963)** and **Mugler (1963)** explain the Vienna manuscript A basis and replacement of missing commentary on Paulus ch1–8 by Byzantine redaction. These are secondary edition-history notices, NOT a Greek Paulus ch32 table or independent monomoiria 120-cell collation. The 2017 Tolsa article identifies an Olympiodorus *recentiores* nocturnal tabulation near **p113 Boer**, but the actual Greek diagram remains unavailable/unverified here. Do not conflate day/nights.
3. **P.Oxy. LXI 4277:** Already examined via the *published scholarly reading* in C05, particularly **Cristian Tolsa (2017)**; this pass confirmed that published discussion but did not obtain a fully identified original papyrus image. Searching for the original image brought unrelated papyrus pictures; none was accepted. The existing C05 **1/3** Paulus by-sign source-arithmetic agreement and two documented failures remain **unaltered**, as do Tolsa's caution about inconsistent original calculations.
4. A later Zellmann-Rohrer paper (*Three Deluxe Horoscopes*) refers to photograph-level observations of P.Oxy. 4277; its newly located bibliographic/preview material is only a lead. No P.Oxy. 4277 photo was visibly inspected here, so the source status cannot be upgraded.

## Reproduction

The machine-readable [C10 register](HEPHAISTIO_C10_EPITOME_IV37_SOURCE_QUESTION_REGISTER_V1.json) separates source edition, page, numbered readings, candidate glyphs, explicit assumptions and evidence levels. [C10 tests](test_hellenistic_c10_epitome_iv37.py) check exact row values, both unresolved candidate sets, raw sum deviations, and unchanged anti-promotion controls. They do **not** certify literal manuscript authenticity.

```bash
python3 -m unittest discover -s docs/astrology-research-map -p 'test_hellenistic_*.py' -v
```

**C10 run: 67/67 historical-source tests PASSED**, from isolated worktree after one C10 test assertion fix. Previous C09 58/58 remain in the count; C10 adds nine source-only assertions. **Human predictive validations: 0**. No other traditions or production code modified.

## Next exact research steps

Find and inspect genuine **Boer 1958 Paulus ch2/ch32 original Greek diagram and its apparatus** and **Boer 1962 commentary** (section/pages around p113, Greek textual recension), then compare *each* of the 34 source/disagreement cells with controlled day/night and ordinal-degree indexing. Obtain authenticated **P.Oxy. Astr. 4277** image (not a similar-looking sample papyrus) and verify the same three single-degree labels from its original glyphs against Jones 1999/Tolsa 2017; preserve illegible cases as such. For §37, collate the two unresolved glyphs against a manuscript or independent critical edition, with full negative and alternate readings. Do not adjust rows or future human profiles to improve fit.

## C11 supersession note (added after original C10 commit)

The C10 Sun→Sun transcription `πν=130` was erroneous. Enlarged inspection of Pingree Epitome IV §37 p241 gives **`πγ=83`**; the seven Sun children now total **531**, not **578**. This source-text correction fixes a false-green C10 arithmetic test. The prior wrong assertion is preserved in Git history, not silently erased. C10 Venus→Sun **36** remains the edited Epitome reading and **also equals the main Greek Venus→Sun 36**. Main Greek **Sun→Venus 35** is the *opposite-direction* period, so no Venus Epitome total revision is admitted. See C11 full comparison and tests.
