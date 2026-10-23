# Hellenistic source reading C04 — Greek Hephaistio, Paulus' monomoiria, and a 319 CE papyrus

2026-10-23 · Source-first exploration; no human predictive claims; this branch does not change the model or empirical test scoring.

## Purpose and recovery boundary

Continue C03 source audit. Examine a directly accessible Greek-language transcription for the open Hephaistio II.29/36 numerical questions, and anchor Paulus' chapter 32 *monomoiria by trigon* against the owner-owned Greenbaum scanned volume. Separately, find a historical chart document enabling objective arithmetic reconstruction **without** retrospectively using owner biography or scoring predictions about a living human.

All material was examined through authorized local source pages or openly hosted scholarly texts. No modern book, long passage, scan, or copyrighted edition was committed into this public research repo. The Amazon *Primary Directions* text was not accessed. Scientific status remains `SOURCE_ONLY_UNSCORED`.

## A. Greek source witness: better explanation of 360 / 365 / 375

### Source identity and limits

- Online Greek: [Eulogikon, Hephaestio, *Apotelesmatics* text](https://eulogikon.org/works/hephaestion-thebes-effects-tco-ab); original UTF-8 [Markdown delivery](https://eulogikon.org/works/hephaestion-thebes-effects-tco-ab.md), **905,747 bytes**, SHA-256 `2265293a6088920adbb487fe91ede7d275db21674da6b997fb98a9584a6c6d63` at retrieval on 23 October. The host metadata reports page-numbered ancient Greek lines with modern digitization. Its precise edition lineage has **not been independently established**; do not elevate this to a separate Greek manuscript or independent empirical confirmation of Schmidt.
- Owned facing-page English translation Robert H. Schmidt, *Apotelesmatics* II, 1998, SHA-256 `e1f11be1a21924345770d2a31766caa0e15a53274403c360057a3c4bc5221073`, visually audited English printed pp83–84 and 106–107 in C02.
- Later Vettius Valens **fifth-century addition** from Riley printed English PDF pp170–172, *different chronological/textual witness*; do not present as indisputably original Valens.
- Exact paired observations are in the machine-readable [Greek-versus-English numeral record](HEPHAISTIO_C04_GREEK_ENGLISH_NUMERIC_VARIANTS_V1.json).

### Chapter 29

The digitized Greek **Book II ch29, Eulogikon marker around printed Greek p201**, contains Saturn distributing **150 days** to Mercury (Greek `ρν`), in agreement with the Schmidt English number **150**. The much later Valens-addition English edition prints **140** for this subperiod. This supports a **source-level divergence, not an English-only transcription error**. No comparison with Hephaestio independent manuscript apparatus has yet resolved which ancient reading is earlier, more accurate or more historically representative.

Seven English subsidiary row sums previously established from visual scans **913, 365, 450, 569, 243, 606, 764** do not all equal each parent month count × 30 days (900, 360, 450, 570, 240, 600, 750). The Greek transcription reproduces the displayed child numbers. Translation agreement does not prove mathematical correctness.

### Chapter 36: explicit source-level correction

| Level | Saturn | Jupiter | Mars | Sun | Venus | Mercury | Moon | Sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Greek main annual allocation** | 85 | 34 | 42 | 54 | 22 | **52** | 71 | **360** |
| **Greek finer allocation headings** | 85 | 34 | 42 | 54 | 22 | **57** | **71** | **365** |
| **Schmidt English finer headings** | 85 | 34 | 42 | 54 | 22 | **57** | **81** | **375** |
| **Child-item sums in finer division** | 86 | 34 | 42 | 54 | 21 | 57 | 71 | **365** |

The online Greek **finer Moon heading** reads `οα` (**71**), whereas the Schmidt English printed fine heading reads **81**. Thus the headline **375-day** number is **specific to Schmidt's printed English witness**, not found in the checked online Greek header. The Greek internally has a **360 to 365 jump** and an unexplained reassignment of **five additional days to Mercury**; 365 total can *suggest* five Egyptian epagomenal days but no textual line yet proves this was intended, and individual Saturn and Venus subdivision totals still differ ±1 from their stated headings.

**Correct historical wording:** “The Greek transcription and printed English disagree in one Moon heading; main Greek annual totals 360, subsequent Greek fine headings total 365, subsequent English fine headings total 375; whether epagomenal days or textual corruption explains the remaining five-day change is unresolved.” **Incorrect:** “Hephaistio's authentic original specifies 375 days”, or “we have proven the ancient calendar used was 365”.

## B. Paulus monomoiria *by trigon* — first exact source-only computational register

- Owner's Greenbaum translation *Late Classical Astrology*, printed pp**66–69**, actual scanned PDF **pp82–85**, read from source images.
- Paulus *Introductory Matters* **ch32** instructs allocating each **individual degree** within one of four elemental triplicities cyclically among planetary rulers with sect-sensitive starts. Greenbaum provides an **editorially corrected daytime** 30-degree × 4-triplicity canon, printed p67. Day-mode column starting planets are: fire **Sun**, earth **Venus**, air **Saturn**, water **Mars**. The seven-planet cycle observable vertically is **Sun → Jupiter → Venus → Moon → Saturn → Mercury → Mars**.
- The extracted *nighttime* 30×4 canon is **NOT** available as a fully supported independent source in the owned truncated edition, and Greenbaum's notes warn of several inconsistent ancient tables (including corrected diurnal errors). **No nighttime canon implemented, intentionally.**
- The [pure source-only daytime lookup](paulus_monomoiria_source_c04.py) uses exact discrete degree integers 1–30, all 12 signs, four 30-entry elemental columns. `CANON` explicitly labels editorial reconstruction. It is neither 10°-decan dignities nor the unrelated *monomoiria by sign*.
- **Documented disagreement:** printed day canon assigns **Cancer degree 8 to Mars**, while a scholion in the same volume, printed p**69**, associates **Cancer degree 8 to Venus**. Its use of a different starting order is identified in Greenbaum's note. Preserve a **one-example variant** but do not invent an entire alternative nighttime table from one example. The edition itself offers comments on which rows need correction.

## C. Independent historical *document* check of Paulus' separate monomoiria *by sign*

**Not the same mechanism as B.** Original documentary study: **Dorian Gieseler Greenbaum and Alexander Jones (2017)**, [“P.Berl. 9825: An elaborate horoscope for 319 CE and its significance for Greek astronomical and astrological practice,” *ISAW Papers* 12](https://archive.nyu.edu/bitstream/2451/49543/4/Greenbaum%20and%20Jones%202017%20PBerl%209825%20ISAW%20Papers.pdf). Inspected actual PDF pp**13–14** (translation columns), p**31** (monomoiria description and textual reliability note). This article preserves a real ancient horoscope document's *computational attributions*. It does **not** provide verified biographical outcomes or statistically independent prospective natal tests.

Paulus **chapter 5** and paper p31 describe `monomoiria by sign`: degree 1 begins with the sign's *domicile ruler*, then each next degree follows `Saturn → Jupiter → Mars → Sun → Venus → Mercury → Moon` cyclically. An ecliptic longitude **3°43'** occupies the **fourth ordinal degree**, not third; the 1-based degree count is `floor(complete_degrees)+1`. This is key when matching ancient chart entries.

Created the [source-exact by-sign lookup](paulus_bysign_papyrus_c04.py), with an immutable seven-row original-paper comparison. Its output:

| Ancient object | Ancient zodiac longitude | Ruler on the surviving papyrus | Reconstructed ruler | Parity |
|---|---|---|---|---|
| Moon | Cancer 26° (minute unavailable in supplied translation) | Venus | Venus | Match with minute unspecified |
| Saturn | Aries 3°43' | Mercury | Mercury | Match |
| Mars | Scorpio 22°32' | Sun | Sun | Match |
| Venus | Libra 29°18' | Mercury | Mercury | Match |
| Mercury | Sagittarius 13°53' | **Mars** | **Saturn** | **Mismatch retained** |
| Ascending node | Scorpio 9°40' | Venus | Venus | Match |
| Descending node | Taurus 9°40' | Moon | Moon | Match |

**6 of 7 unambiguous checked rows agree, one does not.** This matches the authors' caution that **Mercury's monomoiria** in the transmitted chart is incorrect. For *Jupiter in Virgo 7°40'* the translation says “in its own monomoiria”, which is referentially ambiguous; the rule computes **Mercury** for this place but **we deliberately exclude Jupiter from the accuracy denominator** until text and commentary determine the intended referent. Another papyrus manuscript line for prenatal moon Taurus 20°30' has not been entered into this initial seven-row acceptance sample, but the function can deterministically compute **Sun** there.

The historical-match statistic is **reconstruction fidelity of an ancient worked astrological artifact**, not prediction of the person born in 319 CE. It must not increase the empirical project's claimed human hit rate. A wrong handwritten ancient entry stays a failure rather than silently “corrected”. Never tune a code branch after looking at any person's biography.

## D. Verification, status, and next reading

- [C04 Greek/English numeric variants](HEPHAISTIO_C04_GREEK_ENGLISH_NUMERIC_VARIANTS_V1.json)
- [Paulus by-trigon day table source code](paulus_monomoiria_source_c04.py), [by-sign papyrus evaluator](paulus_bysign_papyrus_c04.py)
- [C04 arithmetic tests](test_hellenistic_c04_sources.py) and [papyrus tests](test_hellenistic_papyrus_c04.py)
- Earlier C02 & C03 source tests retained unchanged.

A fresh **separate temporary-folder GitHub download**, not reusing old tool memory, executed all `test_hellenistic_*.py` tests with `python3 -m unittest discover -s ... -p 'test_hellenistic_*.py' -v`: **22/22 PASSED**. This includes 4 C02 table tests, 5 C03 day-rate tests, 7 C04 source/trigon tests and 6 C04 papyrus tests. No real person's questionnaire, event history, horoscope prediction, scoring model, or experimental accuracy was used.

**Still open:** secure Hephaistio's exact Greek textual provenance and secondary critical independent witness for II.29/36, determine five-day allocation in context, original by-trigon nocturnal variants and Paula chapter 33 traditional rectification with non-retrospective sample inputs, Greek `prosopon` own-face vs later face/decan lexical distinction, and restoration of Rhetorius p140 without misattribution. Human validation remains **0**.

**Resume exactly after this source read:** check whether original Greek ch36 explicitly mentions epagomenal days beyond extracted numbers; inspect manuscript apparatus or original critical edition. Separately, contrast by-sign and corrected by-trigon on neutral synthetic charts *without scoring events*. Continue substantive reading of Paulus ch33–37 from locally owned scanned pp68–77 and cross-compare other calculation examples. Do not redo the seven reconstructed papyrus rows or C02/C03 scans.
