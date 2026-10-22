# B04 — directly reading the 1722 K'iche' calendar facsimile

**22 October 2026.** Source/algorithm research increment within `humandesign`'s cross-tradition astrology project. **Actual untouched human forward/reverse predictive validations remain zero.**

## What we inspected rather than repeating a later scholar

The University of Pennsylvania's Berendt–Brinton Collection **Ms. Coll. 700 Item 58** is a copy made by Carl/Karl Hermann Berendt in **1877** of an original K'iche' text dating to **1722**. The Foundation for the Advancement of Mesoamerican Studies (FAMSI) hosts **69** digitized image pages: [original facsimile landing](https://www.famsi.org/research/mltdp/item58/). We visually inspected and independently re-downloaded **26** representative scan images, verified their **26/26 SHA-256 checksums**, and committed **only** hashes, observations and page locator references. **No scanned originals or copyrighted full modern book were copied to public Git.**

The source-independent literary guide used here was the publisher-authorized **18-PDF-page opening chapter excerpt** of John M. Weeks, Frauke Sachse, and Christian M. Prager, *Maya Daykeeping: Three Calendars from Highland Guatemala* (University Press of Colorado 2009): [authorized introduction](https://upcolorado.com/media/acfupload/9780870819969.pdf), SHA-256 `07bba98f12a7b305628a549269a1e6313b7c6955825b54fbebb3aeff937bc944`. The preview contains **Table 1.1** showing 20 Kaqchikel/K'iche' spellings across 1685, 1722 and 1854, and **Table 1.2** containing 1722 month naming variants. It is **not the full scholarly volume**, especially not the complete 1722 source translation (printed pp.64–135).

## 1. Actual handwritten civil-date entries, now independently observed

The first [1722 daily calendar facsimile folio](https://www.famsi.org/research/mltdp/item58/ms_coll_700_item58_wk1_body0001.html) pairs the sacred day numeral and historic K'iche' name with the written civil date **Mayo 3**:

| Photographed source | Hand-read source-normalized claim | GMT 584283 date-only algorithm |
|---|---|---|
| body0001, 3 May 1722 | **9 Queh** | **9 KEJ** |
| body0001, 7 May 1722 | **13 Ba4/Batz** (old glyph spelling uncertain) | **13 B'ATZ'** |
| body0001, 8 May 1722 | **1 Ee** | **1 E** |
| body0002, 15 May 1722 | **8 Caok** | **8 KAWOQ** |
| body0002, 23 May 1722 | **3 Queh** | **3 KEJ** |
| body0002, 31 May 1722 | **11 4iquin** | **11 TZ'IKIN** |
| body0002, 1 June 1722 | **12 Ahmak** | **12 AJMAQ** |
| body0003, 12 June 1722 | **10 Queh** | **10 KEJ** |
| body0010, 19 November 1722 | **1 Queh** | **1 KEJ** |
| body0015, 2 March 1723 | **13 Tzi** | **13 TZ'I'** |
| body0017, 28 April 1723 | **5 Queh** | **5 KEJ** |
| body0018, 3 May 1723 | **10 Ee** | **10 E** |

All **30 manually selected dated rows** in the [primary-witness ledger](MAYA_1722_PRIMARY_FACSIMILE_HAND_READ_B04.json) agree under the preexisting source-declared reference converter. These are **30 entries from the same transmitted manuscript**, not 30 independent cultural attestations and not proof of astrology.

Two subtle arithmetic findings matter:

- The manuscript's **9 Queh / 3 May 1722** year anchor appears at **5 K'ayab'** in the *Lowland reference* 365-day Haab. Exactly **40 civil days later**, the **12 June 1722** manuscript records **10 Queh** and the lowland calculation reaches **0 Pop**. The sign stays *Queh* while its 1–13 coefficient rises by one: a 40-day displacement is **not a universal 40-day shift of the 260-day sign**. This checks the previous Garay/Xoyón Highland/Lowland offset hypothesis against a **hand-read historical copy**, without proving identical ritual year starts.
- Exactly 365 days later, **3 May 1723**, the original copy identifies **10 Ee**, not 9 Queh; the existing algorithm agrees, and the lowland Haab calendar returns to 5 K'ayab'. The 1723–1727 annual headings are visibly present later in body00018–body00022 but **not yet fully transcribed**.

The manuscript also contains a visible Spanish **6 December 1722** dated paragraph on [body0036](https://www.famsi.org/research/mltdp/item58/ms_coll_700_item58_wk1_body0036.html), and the following [body0037](https://www.famsi.org/research/mltdp/item58/ms_coll_700_item58_wk1_body0037.html) is marked **De otra mano** (another hand). The text therefore exhibits *at least a stated scribal distinction*; do not treat the whole 69-image copy as one continuously authored prognostication. These folios' original K'iche' clauses remain untranslated by this audit.

## 2. Discovery: the original manuscript's 5 × 52-day almanac layout

The [body0023 opening AHILABALZIH section](https://www.famsi.org/research/mltdp/item58/ms_coll_700_item58_wk1_body0023.html) groups **five separately named sacred days with the same numeral** next to a K'iche' interpretation paragraph. For example, the following are manual readings of the columns, using modern crosswalk forms to avoid claiming certainty about old diacritics:

| One handwritten group | Five day-name entries, all with the stated coefficient |
|---|---|
| 1 | Imox, Aj, Kan, No'j, Toj |
| 2 | Iq', I'x, Kame, Tijax, Tz'i' |
| 3 | Aq'ab'al, Tz'ikin, Kej, Kawoq, B'atz' |
| 4 | K'at, Ajmaq, Q'anil, Ajpu', E |

[Body0024](https://www.famsi.org/research/mltdp/item58/ms_coll_700_item58_wk1_body0024.html) continues groups **5–8**; body0025 continues **9–12**; and body0026 shows **13** and begins another series. We independently hand-read **13** such groups and compared them with a reference algorithm.

The hidden arithmetic is simple and consequential. Starting with a numbered sacred-calendar day, add **52** days four times. Since 52 is divisible by 13, **all five points have the same numeral**, while the associated **20 day names rotate**. For **1 Imox**, the five calendar positions are **1, 53, 105, 157, 209**, corresponding to **1 Imox, 1 Aj, 1 Kan, 1 No'j, 1 Toj**.

The mathematical extension enumerates **52 groups × 5 entries = 260 unique numbered day-name states**, with **each combination appearing exactly once**. The present document has physically checked **13 visible groups**, not every K'iche' sentence in all 52; the complete structural enumeration remains an **algorithmic extrapolation** and cannot yet claim whole-manuscript textual coverage.

This makes an important difference to the birth-survey plan: **the original source's textual unit may group multiple birth-day combinations rather than one of 20 independent personality signs.** But no K'iche' paragraph has yet been translated and definitively classified as *natal personality* rather than a ritual, auspicious-day, disease, or other divinatory statement. We must not invent a unified person-level rule simply because we can reproduce the structure.

The 5 × 52 structure also resembles some intervallic arrangements in **Dresden and Madrid almanacs**, which Aveni and Vail analyze in the previously read *Madrid Codex* chapters 6–8. This is a real **formal parallel** but does **not** prove exact glyph correspondence, direct copying, uniform meaning, or independent empirical validation. Keep ancient codices, 1722 colonial copy, living Momostenango and Zunil source versions separate.

## 3. Fresh birth-claim provenance: publisher excerpt, not the manuscript's group prose

The available 2009 publisher introduction clearly distinguishes **historic naming/character-by-birthday** (it cites colonial Francisco de Coto), **days favorable for activities**, and **source-specific interpreted divination**. Its printed pp.12–16 survey reported interpretations from Hernández Spina 1854, Bunzel, Edmonson, Schultze Jena and Tedlock.

This provides additional evidence that **some historic sources made natal ascriptions**; it does **not** transform every item in a 1722 almanac into a prenatal or personality statement. For example, the 1854 source's Toj natal association is pejorative, whereas the living Zunil daykeeper PDF characterizes Toj-born people positively as potential mediators and self-taught people. Preserve this as a historical discrepancy, *not* an objective fact about health, morality, sexuality, fate or any individual person. Existing Toj stigma quarantine stands.

The complete authorized *Maya Daykeeping* chapter 3 (1722 text, pp.64–135) and original translated 1722 AHILABALZIH interpretive clauses remain genuinely **unread** in their critical English edition; this is now the most relevant missing edition for this particular study, although not a prerequisite for other schools' first prospective human experiments.

## 4. Reproducibility and what was not done

New source-controlled artifacts:
- [SHA-pinned original-photo page register, 30 dated rows, 20 historic spelling pairs and 13 manually read interval groups](MAYA_1722_PRIMARY_FACSIMILE_HAND_READ_B04.json).
- [Pure five-by-52 calendar grouping reference](maya_1722_five_by_52_reference.py).
- [Photo/date/structural tests and negative controls](test_maya_1722_primary_folio_5x52.py).

The B03 film-date discrepancy **remains unresolved**. This 1722 evidence cannot determine what exact clock time the 2005 clip was recorded or whether modern birth-days turn over at sunrise, midnight or sunset. Likewise it is **not** a historical person-level evidence study; zero users, participants, or known friends' personal birth data were processed for B04. The existing GMT584283/584285 variants are not selected by personality fit.

**Bottom line:** We now have **direct original-copy visual evidence** for 1722/1723 continuous sacred-day arithmetic and for an independently visible five-by-52 grouping. This improves the *source-to-model* engineering map. It does **not** validate any natal trait, prove divine causation, or produce a prospective human predictive success. The untouched human test outcome remains **OPEN**.
