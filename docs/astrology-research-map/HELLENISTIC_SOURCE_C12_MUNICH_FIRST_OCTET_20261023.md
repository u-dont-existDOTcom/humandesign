# Hellenistic source C12 — Munich Paulus monomoiria first eight degrees, four triplicities and duplicated Venus

**23 October 2026 · source-critical research only. Human predictive validations: 0.** Continue from C11; no Gansten Kindle extraction, biographies, production scorer changes, or full-manuscript copy.

## What was actually checked

Directly visually inspected the Bayerische Staatsbibliothek original manuscript **Cod. graec. 170**, handwritten **page 65**, digital image **00081** of the 274-image public IIIF manuscript. This early-modern manuscript contains the Paulus text with scholia and figures (catalogued by Pinakes). The handwritten numerical table and image regions were examined at original resolution and enlarged through IIIF; no OCR and no image redistribution to Git. Source locator is retained in [the machine witness](PAULUS_C12_MUNICH_FIRST_OCTET_SOURCE_WITNESS_V1.json).

The **four printed headings are the four trigons**, each listing **three zodiac signs**, rather than a separate chart for Aries, Taurus, Gemini and Cancer:

| Column | Zodiac glyph grouping | First sign named in C11 |
|---|---|---|
| 1: fire | Aries, Leo, Sagittarius | Aries |
| 2: earth | Taurus, Virgo, Capricorn | Taurus |
| 3: air | Gemini, Libra, Aquarius | Gemini |
| 4: water | Cancer, Scorpio, Pisces | Cancer |

C11 was observationally right about the first sign in each column, but incomplete about the **three-sign grouping**. The table is therefore relevant to **Paulus's triplicity monomoiria** rather than being four unrelated single-sign tables. A separate by-sign monomoiria calculation exists in Paulus ch5 and must not be substituted for this chart. The adjacent handwritten pages 64 and 66 were already opened in C11.

## First-eight-degree manuscript visual transcription

The eight Greek degree labels run **α, β, γ, δ, ε, ϛ, ζ, η**. Each is accompanied by a drawn planetary glyph. The reading below is a **manual same-image glyph identification**, cross-checked against repeated graphic forms elsewhere within the chart: solar slanted circle, Jupiter's curved multistroke, Venus's loop and stem, lunar crescent, hooked Saturn, ornate Mercury, and crossed Mars. There has **not** been a blind second palaeographic reading. All claims are bounded to degrees 1–8.

| Trigon | MS 1–8 source reading (normalized planetary names) |
|---|---|
| Fire | Sun, Jupiter, Venus, Moon, Saturn, Mercury, **Venus**, Mars |
| Earth | Venus, Moon, Saturn, Mercury, **Venus**, Mars, Sun, Jupiter |
| Air | Saturn, Mercury, Venus, Mars, Sun, Jupiter, **Venus**, Moon |
| Water | Venus, Mars, Sun, Jupiter, **Venus**, Moon, Saturn, Mercury |

The first pair of fire **Sun/Jupiter** and earth **Venus/Moon** matches the *diurnal* rather than *nocturnal* trigon ruler order in the Greek source. **Sect is consequently inferred, not certified by an independently transcribed manuscript rubric.** The page's accompanying small Greek scholia have not yet been accurately collated.

## Source-mechanism finding: second Venus retained

The opening eight values in **each of four trigons** agree with a simple traversal of four **diurnal pairs** in order fire→earth→air→water (rotated to the current trigon), *without* applying the narrative instruction to omit a planet that has already appeared. The planet **Venus occurs twice** because it is in both earth and water diurnal pair lists. In other words:

- Manuscript first eight: **eight pair-slots, seven distinct planets**.
- Existing C05 narrative reconstruction: **seven distinct planets**, skipping Venus's later appearance.
- Greenbaum's corrected printed day canon: another **seven-planet cycle**, not an exact copy of the manuscript's first eight.

This is a **positive observation about one sixteenth-century manuscript's visible table**, and a possible textual corruption or alternate computation. It is **not** evidence that the ancient author himself prescribed an eightfold cycle or that an eightfold cycle should be used for natal results. In particular, do not generate manuscript values for degrees 9–30 from an assumed period eight merely because the first octet fits the simple hypothesis. Handwritten layout beyond the first octet may have irregular or amended entries.

## Comparison limited to nine relevant disputes, rather than claiming 34 resolved

Compared each of the 32 manually read first-octet values to the two **previously frozen** sources: C05 narrative sevenfold allocation and C04 Greenbaum corrected printed daytime canon. Of the historic **34/120** narrative-versus-corrected-table discordances, **nine** are in the inspected first eight degrees:

| Trigon | Previously disputed degrees within 1–8 | Handwritten result |
|---|---|---|
| Air | 3, 4, 5, 6 | All four agree with narrative, not corrected printed table |
| Water | 1, 2, 3, 4 | All four agree with narrative, not corrected printed table |
| Water | 8 | Manuscript **Mercury**; C05 narrative **Venus**; Greenbaum printed **Mars** — **matches neither** |

Therefore **8/9 of directly inspected disputed cells match the narrative**, **0/9 match the corrected printed canon**, **1/9 matches neither**. These are **within-manuscript textual agreements only**, not a canon-wide win, not independent validation of the underlying astrology, and not resolution of the remaining **25 of 34** disputed positions. The fourth-column degree-eight disagreement is deliberately preserved as a negative case. **C12 historical-source suite: 86/86 PASS** (77 prior + nine new source fidelity tests), with **no independently blinded human evaluations**.

No selection was made using any birth chart or someone's known life.

## Reproducibility and next steps

[Machine-readable first-octet witness](PAULUS_C12_MUNICH_FIRST_OCTET_SOURCE_WITNESS_V1.json) stores 32 image-anchored tentative glyph assignments, all four sign triplets, dates/IIIF locators and explicit unread-status controls. [Source-only comparison](paulus_munich_first_octet_c12.py) rejects degrees greater than 8, and calculates exactly the nine relevant cells without extrapolation. [Regression tests](test_hellenistic_c12_munich_first_octet.py) assert exact witness values and forbid unintended full-table or human-model promotion.

**Next:** individually read manuscript degrees **9–30** in all four trigon columns, retain glyph uncertainty and handwritten corrections, and determine whether entries past the first octet preserve the same pattern or switch; inspect the associated Greek scholia/rubric and Boer's 1958/1962 critical apparatus for family/version linkage. Find the original authenticated P.Oxy. 4277 image separately; the previous C05 papyrus by-sign comparison remains **1/3**, with its two negative outcomes retained.

## C13 supersession notice — full-page inspection supersedes only C12's '25 unread' boundary

The C12 first-octet observation remains preserved unchanged, but **do not generalize its eight-slot pattern**: C13 directly inspected manuscript degrees 9–30 as well. In the resulting 120-position image-based registry, **119 labels are tentatively identified, earth degree 28 remains indeterminate**. Source evidence contradicts a simple eight-position repetition for **water degrees 9–30** and earth degrees 29–30. All 34 previously disputed narrative-versus-corrected-table cells have now been compared within *this one manuscript*: **11 narrative-only, 1 corrected-only, 22 neither**. This is not a decision that either version is original/authentic, and does not change model scoring. See [C13 research report](HELLENISTIC_SOURCE_C13_MUNICH_120_IMAGE_COLLATION_20261023.md) and [C13 recorded glyphs](PAULUS_C13_MUNICH_120_POSITION_IMAGE_TRANSCRIPTION_V1.json).
