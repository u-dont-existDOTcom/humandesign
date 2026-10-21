# JYOT B10 — Exact Aṣṭakavarga contributor-table reconciliation (2026-10-21)

## Evidence and scope

The original five uploaded files are available and their SHA-256 match the previously committed source manifest. This packet compares **printed secondary translations**, not a critical Sanskrit edition and **not predicted human outcomes**. Source A: `JYOT-SARAVALI-EN`, **PDF page 142, Chapter 53, slokas 2–8** (physically rendered and visually inspected). Source B: `JYOT-BPHS-KERR-PT`, Portuguese second-hand translation **plaintext lines 5267, 5299, 5305** (decoded CP1252), discussing the same Aṣṭakavarga system.

The complete source-only 7-target × 8-contributor offset transcription, computed totals and one discrepancy are in `ASHTAKAVARGA_B10_SOURCE_RECONCILIATION.json`. Count source signs inclusively: the contributor's occupied sign is relative **1**. All 56 contributor lists contain only distinct integer offsets 1–12. No natal chart or person's questionnaire data entered this comparison.

## 1. A notation inversion that can reverse scoring

- The uploaded English `Saravali` says **benefic dots/Bindus** in Chapter 53 and Chapter 54 and predicts greater auspiciousness when the target receives **more**.
- The Portuguese `BPHS` explicitly says in **line 5267** that **Karan (unfavorable)** places get `Bindu` (points), while favorable **Sthan** positions get `Rekha` (vertical strokes). Line **5305** specifies literal `Bindu = ponto (0)`, `Rekha = linha (1)`, and the polarity `Karan = inauspicious`, `Sthan = auspicious`.

This is **different marking conventions**, not yet a disagreement about which planetary positions are favorable. A cross-book software implementation must translate **meaning (favorable/unfavorable)**, not just equate the raw word `bindu`. Switching language/edition with the same symbol would incorrectly invert prediction direction.

## 2. A specific missing favorable position in one English source

The seven Saravali Chapter 53 target-table **favorable contributions** sum to:

| Target table | Count in uploaded Saravali |
|---|---:|
| Sun | 48 |
| Moon | 49 |
| Mars | 39 |
| Mercury | 54 |
| Jupiter | 56 |
| Venus | 52 |
| **Saturn** | **38** |
| **All seven** | **336** |

Compare Portuguese `BPHS` **line 5299**, the favorable (`Rekhaprad`) **Saturn** table. Instead of planet→relative-offset lists, that line groups the **contributors by relative sign**. On inversion, it agrees with every favorable position in Saravali Chapter 53 verse 8 **except one**: the ascendant as contributor in its **sixth** sign.

The Portuguese source states that at the **sixth** sign **every contributor except the Sun** is favorable; the uploaded English Saravali gives Saturn's ascendant offsets **1, 3, 4, 10, 11**—omitting **6**. That difference alone produces the Saturn **38 versus 39** and seven-target **336 versus 337** arithmetic.

**Disposition:** `POTENTIAL_ENGLISH_TRANSLATION_OR_TRANSMISSION_OMISSION`. The data artifact preserves Saravali's literal five offsets and a distinct, **proposed but unapplied**, ascendant-sixth addition derived from the Portuguese source. Neither text is silently corrected or proclaimed the original Sanskrit; original-language comparison and possibly further editions are needed before admitting a canonical engine rule.

This is particularly consequential because the Aṣṭakavarga tables are algorithmic: one missing contribution changes favorable-sign totals and potentially the classification of particular transit dates.

## 3. Separate table computation from event interpretation

- `Saravali` **Chapter 53.1**, PDF142, declares day-to-day transit uses. Chapter 53.9–10, **PDF143**, says more positive marks in the sign traversed by a planet lead to favorable outcomes. It separately modifies result size by exaltation/debilitation/own sign and whether the planet is early/middle/late in the sign.
- `Saravali` **Chapter 54.2–9**, **PDF143–144**, gives broad 0–8 **natal occupancy** result categories by planet, including historically alarming claims. These are not interchangeable with the transit claims without a stated additional assumption.
- Portuguese `BPHS` **line 5373** classifies **aggregate** (`Samudaya`) totals: above 30 favorable, 25–30 intermediate, below 25 unfavorable. These thresholds are explicitly for aggregate signs; do **not** apply them uncritically to an individual planet's 0–8 target table.
- `Saravali` Chapter 54.1, **PDF143**, describes 96 table cells, but calls both sets of intersecting lines 'horizontal'. The geometry implies perpendicular groups of lines, a probable editorial/layout error, not a verified Sanskrit correction.

The 7 target lists give a **deterministic historical feature extractor candidate**, which is cheaper to test than constructing another free-form personality reading. Nevertheless, interpreting the result requires precise question/event outcome definitions, realistic seasonal and calendar baselines, matched chart decoys, temporal dependence controls, and predeclared negative outcomes. None was implemented or scored here.

## Verification and next reading

`ASHTAKAVARGA_B10_SOURCE_RECONCILIATION.json` preserves the exact source-offset lists and a sign-centric transcription of the second book's Saturn contributions. The computation checked 7×8 maps and isolated a **single** mismatched coordinate (Saturn table, Lagna contributor, relative sign 6). No statement about human predictive power follows from this table consistency check.

Next: collate this precise coordinate against an independent Sanskrit Chapter 53 witness and Parashara's original-language schema, and broaden the source study to Navābha (whole-chart patterns), Dasha subperiod exceptions, planetary-state reversals, and non-personality outcomes. Preserve the branch's existing 153 historical source annotations, independent book rights and other reader's work.
