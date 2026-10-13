# Second-pass source-fidelity audit: Lilly 1647, Ch. XLIX, batch B02s (PDF336–345, printed pp. 302–311)

The batch still needs repair. Most of my first-review findings are fixed, but two high-severity errors remain:

- **R1992:** the man/woman direction is reversed.
- **R2010:** the repair deleted an original clause.

This is an informed check of the changed items, not a second blind first pass. I transcribed all 11 images before opening any JSON file or my earlier review. I did not edit any files.

## Scope
- **Images (11):** pdf-336 to pdf-345 (printed pp. 302–311) and errata-888, each viewed once.
- **Records (122):** R1921–R2034 plus R2108–R2115. Of these, 49 carry a repair tag, 8 are new insertions and 65 are unchanged drafts.
- **Also read:**
  - RULES_SOURCE_ORDER.json. It lists 216 IDs, and the 94 not in this file fall after p.311.
  - ERRATA_COLLATION.json.
  - INITIAL_INDEPENDENT_REVIEW.md.
- **Could not check:**
  - PDF346–353 (pp. 312–319, including p.317). I had no images for them.
  - Whether `source_images/` is byte-identical to the `evidence/` files the records cite.

## 1. What happened to my first-review findings

Of the 38 findings, 31 are CORRECTED, 5 are STILL_WRONG and 2 are partly UNVERIFIABLE.

**Not resolved:**

| # | Record | Status | Printed evidence |
|---|---|---|---|
| 08 | R1992 | **STILL_WRONG, HIGH** | The planets, aspect and "painfull" are now right. But the precondition "Question concerns characterization of the woman" describes the wrong person. p.308: "For the man, note the Planet the ☽ is with; as if with ♀, say **she** is faire… and for the woman, judge by the Planet the ⊙ beholdeth". p.304 adds "⊙, the naturall significator of men". So when a woman asks, the ⊙ rules describe the man. |
| 17 | R2009 / R2010 / R2114 | **STILL_WRONG: one HIGH regression, one MEDIUM** | The locator is fixed and the "♄ ♂ or ☋ in the ascendant, idem…" clause was added. But it was written over R2010, whose kind is still `disagreement_moon_fall`. The clause at p.310 ll.4–8 is now in no record: "the ☽ in her fall, or at □ or ☍ with ♄ or ♂, or any Retrograde Planet, if the ☽ then behold the ascendant, noteth brawling ever moved by the woman". R2010 still points to "the Moon affliction clause", which no longer exists. R2009 also leaves out ♄ (M1 below). |
| 15 | R1931 | **STILL_WRONG (partial), MEDIUM** | Venus's conditions are fixed. But p.303 "and the ☽ likewise" follows "strong, encreasing in her motion, and in some of her owne Dignities", and the record now applies only dignity to the Moon. |
| 26 | R2007 | **STILL_WRONG (partial), MEDIUM** | Three items were restored: "if neither… be in angles", "or strive for it" and "impedited". But the main clause on p.309 is gone: "The Lord of the seventh more weighty, and in an angle, she will be master, or strive for it". The "strive for it" hedge has been attached to the fallback, which the print gives as "shall be master". |
| 30 | R1941 (R1948 is fixed) | **STILL_WRONG, LOW** | The exception note says "'or with the Lord thereof' is preserved", but the statement itself leaves it out (p.304). |
| 14 | Batch scope | **CORRECTED in window; rest UNVERIFIABLE** | Scope is now [336,345], and R2033 covers the p.311 heading "Which of the two shall live longest." R2034's content after "Behold the Lord of the ascendant, and of the seventh, which / of" is on p.312, which I can't see. |
| 36 | R1921 (R1924, R1928 and R1935 are fixed) | **UNVERIFIABLE** | Only aphorisms 40–43 are visible, so "forty-three… aphorisms" can't be checked. |

**Corrected (with the printed phrase that confirms it):**
- **01 · R1937 / R1938:** p.304 l.2 "it will **unwillingly** be con-/sented". The errata page has no p.304 entry, and the record keeps the printed word and flags the conflict with p.303. Its kind label is stale (M9).
- **02 · R1940:** p.304 "the ☽ in the tenth signifieth the same".
- **03 · R1961:** p.305 "promised by ☌ □ or ☍" alongside the erratum "p 305 l 22 dele ☌". Both are kept.
- **04 · R1930:** No aspect type is added any more. The margin note "* Or, if the Lord of the seventh apply…" is kept. Its kind label is stale (M9).
- **05 · R1932:** "and the ⊙ have any dignity… and behold the Lord of his house, viz. of the Signe wherein he is".
- **06 · R1933:** The premise is restored. It does soften "no Marriage at all performed" to "may" (low).
- **07 · R1949:** "Signifiers in interchangeable Dignities", the margin note "Viz. one in the Termes…", and p.305 "☽ in the seventh giving vertue".
- **09 · R2018:** "☽ in □ of good Planets, by dead men; ☽ in ☌… owne industry".
- **10 · R2028:** p.311 "twelve first degrees of ♑" is now Capricorn, with all three outcomes and the margin caution. Its kind label is stale (M9).
- **11 · R2013:** "In the fourth, either a Divorcement or a willingnesse to it".
- **12 · R1967:** "perhaps it's objected… scandalized… it's feared".
- **13 · R1963:** "what evill Planet… frustrates… prohibits… interjects his Rayes".
- **16 · R1934:** The named significators, "or if their Lords behold them", and "consent of all parties" are all back.
- **18 · Headings:** R2108, R2112, R2113, R2115 and R2033 add the missing headings, and R2109 and R2110 add the margin headings.
- **The rest, all confirmed against the print:**
  - 19 · R2011
  - 20 · R2017
  - 21 · R1964
  - 22 · R1970 and R1971
  - 23 · R1996
  - 24 · R1998
  - 25 · R2005
  - 27 · R2031
  - 28 · R2027
  - 29 · R2111 and R1952's omissions (but see M3)
  - 31 · R1986: the erratum is now cited, and the obscured glyph is still flagged.
  - 32 · R2032
  - 33 · R2020 and R2021's "very feasible" (but see M2)
  - 34 · R2026
  - 35 · R1965, R1966, R1968 and R1974
  - 37 · R2003
  - 38 · R2006

## 2. Errors still open (HIGH and MEDIUM)

**HIGH**
- **H1 · Missing clause, deleted by the repair:**
  - **Source:** p.310 ll.4–8, "the ☽ in her fall, or at □ or ☍ with ♄ or ♂, or any Retrograde Planet, if the ☽ then behold the ascendant, noteth brawling ever moved by the woman".
  - **Fix:** Give this clause its own record, or put it back in R2010 and give the "♄ ♂ or ☋" clause a new ID.
  - **Also in R2010:** It should either tie "idem" back to this clause or mark it as ambiguous, rather than saying "querent or woman".
- **H2 · R1992:** The precondition should say "woman querent; the planet the ⊙ beholds describes the man". The statement's "Moon–Venus clause concerns the man" should become "a man's question describes the woman ('say she is faire')".

**MEDIUM** (the first review missed M1, M4, M5, M6 and M2; the repairs introduced M3)
- **M1 · R2009 and R2114 leave out Saturn.** The last line of p.309 reads "…beholding the ascendant, or ♄," with the catchword "♂". p.310 l.1 continues "♂ or a Retrograde or Combust Planet in the ascendant". Fix: add ♄.
- **M2 · R2021 misreads "heavy".** The print says "if he be a **heavy Planet**, and be hindered by □ or ☍ of an ill Planet, or be Cadent" (pp.310–311). The record has "heavily afflicted planet… etc." Fix: restore "heavy (ponderous) receiver" as its own condition and drop "etc.".
- **M3 · R1952's precondition turns "especially" into "or".** The print says "in the seventh, especially in one of his owne houses" (p.305 ll.6–7). The precondition reads "in seventh **or** own domicile". Fix: the 7th lord must be in the 7th, with "especially in own house" as an intensifier only.
- **M4 · R1945 misses part of the first testimony.** p.304 reads "It shall be, if the Lord of the ascendant **or ☽** be in the seventh". The bare "☽ in the seventh" branch is in no record; R1949's version carries an extra condition. Fix: add it.
- **M5 · R1991 narrows a general rule to one example.** The print says "For the man, note the Planet the ☽ is with; as if with ♀, say she is faire, slender and pleasant… and so of the rest" (p.308). The record keeps only Moon with Venus and "agreeable traits". Fix: restore the general rule, the man-asks condition and the three printed traits.
- **M6 · R2019 broadens a specific condition.** The print says "if the ☽ aspect ♄ or ♂… in angles, notes a probability of separation" (p.310). The record has "an afflicted Moon" and gives "in angles" to "related afflicted planets". Fix: restore "☽ aspecting ♄ or ♂", and flag that it's unclear what "in angles" refers to.
- **M7 · R1931:** Apply "and the ☽ likewise" to all three conditions, or flag its scope as ambiguous.
- **M8 · R2007:** Restore the 7th-lord clause ("she will be master, or strive for it") as the primary rule and the "neither in angles… shall be master" rule as the fallback.
- **M9 · Three record-kind labels still carry the removed misreadings:**
  - R1937 `quesited_willing`
  - R1930 `alkindus_sextile_trine`
  - R2028 `arabic_virgo_condition`

**LOW (grouped)**
- **Wording drift:**
  - R1940 says "Sun applying to Venus" where the print has "application of the ⊙ and ♀".
  - R1925 adds "natural".
  - R1967 changes "propounds" to "asks".
  - R1974 and R1927 soften "shall" to "may".
  - R1971 has "obstinate" for "busie-headed".
  - R1973 has "either" for "both".
- **Dropped phrases:**
  - R1934 drops "by the will of God".
  - R2001 drops "If the man aske".
- **Labels and sequencing:**
  - R2027 is labelled `natal`, which the print doesn't say.
  - R2109 is sequenced before R1944, but the print places it after.

## 3. Errata collation check
- **p.305 l.22 "dele ☌":** The errata text is confirmed, though the glyph is tiny. The only ☌ on p.305 is in "promised by ☌ □ or ☍", which sits on line 23 by my count. The target is certain from its content; the line number is off by one.
- **p.306 l.26 "r undertaken":** The errata text is confirmed. But the body line "Journey to be **undertaken** by the que-/rent" already reads "undertaken" in this copy. The uncorrected word is not visible here, so the collation shouldn't imply a different printed word. R1971 is consistent either way.
- **p.307 l.28 "r for ⊙ and ♂":** The errata text is confirmed. In the body, the glyph between ⊙ and ♂ is obscured, and a later owner has handwritten "for" over the printed "and". That handwriting is not part of the 1647 print. R1986 handles this correctly; it should read "⊙ and ♂", not "Sun/Mars".
- **p.312 l.17 "it is no good", p.315 l.7 "☋" and p.315 l.10 "seventh":** The errata text is confirmed (the ☋ is small but probable). The body pages are not supplied, so these body matches can't be checked. That includes the collation's "original_reading" quotes and its misprinted "215". The records that use these errata (R2040, R2062, R2064) are not in this file.
- **No errata for pp.302–304 or 308–311:** confirmed.

## 4. Checks on the points you listed

| Point | Result |
|---|---|
| Negation | Correct in R1953, R2016, R2005, R1933, R1966 and R2027. |
| Forced vs voluntary | Correct in R1937, R1928, R1934, R2013 and R1952. No passage about forced relations is printed on pp.302–311. |
| Free will | No passage on pp.302–311 is about free will. The nearest is "by the will of God… consent of all parties" (p.303); R1934 keeps the consent and drops "by the will of God" (LOW). |
| False accusation | R1967 and R1974 frame these correctly as objections, fears and slander. No false-accusation exception is printed on pp.302–311. |
| House and gender directions | The open items are H1, H2, M5 and M8. R1972, R1971, R1995, R2031, R2030 and R2017 are correct. |
| "unwillingly" (p.304) | Kept correctly; only the label is wrong (M9). |
| Love direction, p.305 vs p.317 | p.305 is kept correctly in R1950, R1951 and R2111. R2111's claim that p.317 contradicts it can't be checked and must not override p.305. |
| Capricorn glyph (p.311) | Correct in R2027, R2028 and R2032; only R2028's label is wrong (M9). |
| Timing from lunar aspects | Correct in R1980, R1981 (strong testimonies and swift significators), R2017 ("quickly") and R2028 ("six moneths"). |
| Missing clauses and headings | All headings are present. The missing clauses are H1, M1 and M4. |

## 5. Biggest remaining risk
The biggest risk is the man/woman direction of the descriptions. In machine-readable form, R1992 now says the ⊙ character rules describe the woman. And the one printed clause that pins disagreement on "the woman" (H1) was dropped while fixing another clause. Behind that, pp.312–319 can't be checked from these images, including the p.317 love-direction conflict and the body matches for the p.312 and p.315 errata.

**Final label: REPAIR_REQUIRED**
