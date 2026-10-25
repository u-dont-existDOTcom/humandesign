# Argoli 1610 vs 1667 — descending and converse primary directions

**25 October 2026.** Owner's root research outcome: **OPEN**. The project seeks historically differentiated Western/Hellenistic/Jyotish/Chinese/other astrology systems and, eventually, separately frozen falsifiable chart predictions evaluated against genuinely untouched human outcomes and matched controls. This work is a historical-source and synthetic-method audit, **not evidence of predictive accuracy**.

## New original pages actually examined

The original 1610 *Tabulae primi mobilis*, Bavaria/Augsburg library scan `bsb11218073`, includes printed pp.43–48 (institutional IIIF leaves 55–60). The later 1667 Padua edition in the Michigan Internet Archive 107-leaf **excerpt** includes printed pp.31–34 (physical PDF leaves 44–47). Both are original print photographs, not modern OCR. All 10 complete page images are copied into `primary_witnesses/` with independent SHA-256 hashes; an additional source-aligned detail crop makes the later p.33 table error legible but is **not an independent printed witness**.

The separately published parent `argoli-aligned-1610-1667-20261025` proved 1610 chapter XIII (printed pp.39–41) corresponds to 1667 chapter XV (printed pp.29–30), including two exact examples and the 1667 p.30 discrepancy: **163°17′ − 119°55′ = 43°22′**, while that inspected 1667 printing gives **45°22′**.

## Further aligned chapters

| Original 1610 printing | Original 1667 printing | Observation |
| --- | --- | --- |
| Chapter XIV, p.43–44: `De directione significatoris ... parte caeli descendente` | Chapter XVI, p.31–32 | Both describe descending-half directions by *oblique descensions* |
| Chapter XV, p.45–46: `Quomodo significator ... per ascensiones` | Chapter XVII, p.32–33 | Both describe an alternate placement at the opposition, with reversed latitude, to compute via *oblique ascensions* |
| Chapter XVI, p.47: `De directione conversa` | **No separate matching heading** between Chapter XVII and the next profections heading on inspected p.33 | Cannot infer the converse method was absent throughout the later edition; relocation/omission is unresolved |
| Chapter XVII, p.48: `De profectionibus` | Profections chapter printed `Cap. XIIX` on p.33 | Printed numbering and contents differ; `XIIX` is retained as printed |

### Matched numerical examples

| Example | Calculation | Both editions' reported arc |
| --- | --- | --- |
| Sun to sextile of Mars via descending oblique coordinate | 381°20′ − 340°03′ (1610 p.44 / 1667 p.31) | **41°17′** |
| Sun to sextile of Jupiter via descending oblique coordinate | 387°01′ − 340°03′ (1610 p.44 / 1667 p.32) | **46°58′** |
| Sun to sextile of Mars using alternate opposite-point oblique ascensions | 201°20′ − 160°03′ (1610 p.46 / 1667 p.32) | **41°17′** |
| Sun to sextile of Jupiter using alternate opposite-point ascensions | 207°01′ − 160°03′ (1610 p.46 / 1667 p.33 prose) | **46°58′** |

The original descending example expresses 21°20′ with the instruction to **add a full 360° circle before subtraction**, equivalent to 381°20′. The two algorithms reproduce the same two source outcomes within each edition; the original author thereby provides a cross-method consistency check.

### A second distinct numerical misprint in the inspected 1667 copy

The table immediately above the profections heading on **1667 printed p.33** gives:

- first oblique ascension: **207°01′**;
- second oblique ascension **printed 106°03′**, while the preceding p.32 prose and original 1610 p.46 use **160°03′**;
- reported directional arc: **46°58′**.

The arithmetic with the printed table operand would instead give **100°58′**. The reported arc is consistent with **207°01′ − 160°03′ = 46°58′**, establishing an apparent transposition of the printed digits **160 → 106** in this 1667 table. This is separate from the earlier original 1667 p.30 **45°22′ vs 43°22′** error. **We have inspected only one physical 1667 prose copy for either error**; do not claim all copies or printings share them. Original readings remain unaltered in `SOURCE_METHOD_ALIGNMENT.json`.

## The author explicitly specifies converse direction in 1610

Original 1610 **p.47, Chapter XVI** defines converse directions in a separate small chapter. Its decisive distinction is *whose position circle is used*: in converse the ascensions/descensions are taken from the **promissor's circle of position**, **not the significator's**, as in a direct direction. For a converse contact to the Midheaven the author specifically directs subtraction of promissor(MC) right ascension **from** that of the significator. The chapter mentions the Part of Fortune and retrograde planets as contexts where converse may be considered; it is **not** an unqualified instruction to use converse for every natal planet.

This resolves an earlier source-documentation ambiguity: Argoli's **1610 printing explicitly describes a converse operation**, so we must not equate the term solely with dexter/sinister aspect-point placement or with the modern shortcut `360° − direct arc`. The subsequent 1667 aligned chapter sequence skips a *standalone converse title*, but no exhaustive 1667 search has been performed to establish whether the procedure was moved or omitted.

## Separate research operationalization — not an author-certified forecast

`src/hdmatch/astrology/argoli_1610_direction_conventions.py` provides exact integer wrapped source arithmetic. It additionally compares two *existing modern Regiomontanian* constructions:
- a direct geometry using the **significator's** position circle;
- a role-swapped geometry using the **promissor's** position circle, as suggested by the 1610 converse source.

The role-swapped result is compared against `360° − direct`. These agree only in restricted geometries; there is no universal identity. A seed-20261025 **500-case exploratory development** run found 355/500 cases differing by over 1° (198/500 by over 5°), median difference about 2.99°, maximum about 63.05°. These numbers were observed **before** the present source contract and cannot be called a new untouched holdout.

A separate seed-20261029 **400-case synthetic coordinate panel** was fixed in the source record, with the code and tests, before it was run. It is still **only a mathematical holdout**. Neither panel contains a person's birth data, life events, or behavioral questionnaires, and no statistic measures astrology's predictive skill. The source authorial formula may have more conditions than simply using the current geometry engine with two actors swapped.

## Next source and empirical frontier

The **1644 Argoli method chapter is still not accessible** through the attempted Gallica (403) or Google Books (429) routes, despite bibliographic evidence of multiple copies. The later 1667 provenance issue also needs a second independently photographed prose copy. A fuller source-authenticated direction rule must address latitude, promissor/angle roles, true 1610/1644/1667 variants, time key, and both parties' radix strength. No known participant or owner's personal life history can qualify as untouched human validation. The optional **separately labeled modern diagnostic** pilot can be pre-registered with an exact age-window and birth-time-uncertainty protocol without pretending this historical-source work is a mandatory precondition.
