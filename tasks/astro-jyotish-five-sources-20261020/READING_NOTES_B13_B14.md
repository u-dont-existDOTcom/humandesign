# JYOT B13–B14 — Parāśara original Sanskrit fixes numbers and part of the reduction algorithm (2026-10-21)

**Research status:** Source-critical and computational *documentation* only. The other parallel astrology readers, production rule engine, survey, participant data and frozen models are untouched. Cumulative previously accepted source annotations remain **181**; B12–B14 are cross-edition checks, not additional real-human forecast successes.

## Numeric Piṇḍa Sādhana multipliers: Sanskrit 69.2–4

The user-uploaded Portuguese *Bṛhat Parāśara Horā Śāstra* **line 5326** contains contradictory sign and planetary multipliers in its own prose and parenthetical tables. Sanskrit **Chapter 69 verses 2–4**, checked against [TransLiteral's 2011 transcription](https://www.transliteral.org/pages/z110726085844/view), [Sanskrit Wikisource](https://sa.wikisource.org/wiki/बृहत्पाराशरहोराशास्त्रम्/अध्यायः_६९_(पिण्डसाधनाध्यायः)), [VedicPupil](https://vedicpupil.in/hi/library/books/brihat-parashara-hora-shastra/chapter-69) and [Enjoy Learning Sanskrit](https://enjoylearningsanskrit.com/scriptures/parashara/chapter-69/) clearly assigns:

| Sign | multiplier | Sign | multiplier |
|---|---:|---|---:|
| Aries | 7 | Libra | 7 |
| Taurus | 10 | Scorpio | 8 |
| Gemini | 8 | Sagittarius | 9 |
| Cancer | 4 | Capricorn | **5** |
| Leo | 10 | Aquarius | 11 |
| Virgo | **5** | Pisces | 12 |

Planetary multipliers: **Sun5, Moon5, Mars8, Mercury5, Jupiter10, Venus7, Saturn5**. Sanskrit 69.3 contains `मृगकन्ये च पञ्चभिः` (Capricorn and Virgo by five); 69.4 states respectively `दशाष्टनगसायकाः` (10,8,7,5) for Jupiter, Mars, Venus, Mercury, `पञ्च शेषग्रहाणां` (five for remaining planets).

This text **contradicts the Portuguese prose** Capricorn/Virgo=6; Mars=3; remaining Sun/Moon/Mercury/Saturn=6. The Portuguese *parenthetical* planet chart agrees with Sanskrit. The sign chart keeps Capricorn5 correctly but incorrectly gives Virgo6, and prints Scorpio twice in what should be Taurus and Scorpio positions. Some popular English BPHS websites share the *same contradictory paragraph*, apparently common transmission/copying; repetition does NOT create independent support for the errors.

**Additional translation pitfall:** One separate online Sanskrit-learning site renders the four graha multipliers in 69.4 as **daśā durations in years**. This is contradicted by the immediately preceding `grahamānam athocyate` (“now the planetary multipliers”), and the Piṇḍa calculation introduced in 69.1. Do not confuse numerical Pinda weights with dasha-year lengths.

The precise per-source discrepancies and all 12+7 numbers are saved in `SANSKRIT_PINDA_MULTIPLIER_RECONCILIATION_B13.json`. The available Sanskrit texts may share the same printed ancestor; **full manuscript-critical verification remains incomplete**.

## Stage one reductions: original Sanskrit Chapter 67

The same Sanskrit source tradition explicitly says in **67.4**: `त्रिकोणेषु च यन्न्यूनं तत्तुल्यं त्रिषु शोधयेत्`, meaning subtract the lowest of each zodiacal trine's three counts from **all three**; if any count in that trine is **zero**, do not reduce that trine. Chapter 67.5 says if all three are equal they become zero, consistent with subtraction.

Four disjoint trines (Aries Leo Sagittarius), (Taurus Virgo Capricorn), (Gemini Libra Aquarius), (Cancer Scorpio Pisces) are treated separately. This corrects a Portuguese textual ambiguity at **line5314**, which appears to instruct subtraction from only the largest. The source-based operation admits easy boundary tests:

- `[0,3,6]→[0,3,6]` because zero prevents reduction.
- `[2,3,6]→[0,1,4]`.
- `[4,4,4]→[0,0,0]`.
- `[3,7,3]→[0,4,0]`.

All four cases are verified arithmetic examples, **not horoscope tests**. They are recorded in `SANSKRIT_SHODHANA_STAGES_B14.json`.

## Stage two reductions: original Sanskrit Chapter 68 remains nontrivial

Original Sanskrit **68.1–6** says perform Ekādhipatya (shared planetary ruler) Shodhana **after** Trikona reductions and before Piṇḍa. Pair signs owned by Mars, Venus, Mercury, Jupiter, Saturn; Cancer and Leo have only one traditional ruler and are not paired for this step.

Some firm exceptions: if **both** paired signs contain planets, do not reduce; an unoccupied sign with value equal to its occupied partner loses its value. But the supplied English/Portuguese/Sanskrit modern glosses diverge about certain unequal-occupancy cases. Do **not** silently choose whether to set unoccupied value to the smaller number or subtract one number from the other, or how to prioritize overlapping equal/unequal conditions. These form explicitly unresolved clauses in B14 JSON.

Therefore this reader **has established the Sanskrit numbers and first reduction step**, not a full working Piṇḍa calculation. The earliest defensible next implementation is a versioned isolated source-arithmetic fixture that verifies those portions and fails closed on the unresolved Ekādhipatya branches. No authorized production astrological forecasts are possible from an underdetermined implementation.

## Previously fixed source-critical error remains relevant

`SANSKRIT_ASHTAKAVARGA_RECENSION_B12.json` and `READING_NOTES_B12.md`: a Sanskrit *Sārāvalī* printed text and Central Sanskrit University e-book clearly include the **Lagna sixth** favorable Saturn contribution omitted in the user's English translation. The literal uploaded values still sum to **336**, Sanskrit/Portuguese full readings to **337**. The last three Sanskrit chapters are arranged **Ashtakavarga contributions Ch52; non-human births Ch53; Ashtakavarga effects Ch54**, while the English uploaded last three are **Ch53 contributions; Ch54 effects; Ch55 nonhuman births**. The Effects chapter **does exist** in the older Sanskrit printing: earlier speculation that it was absent was incorrect.

## Next research

Independent manuscript/source-image review for the exact planet-occupancy cases in Chapter68; then implement any arithmetic under explicitly versioned source conventions. Continue broader, non-repetitive chapter coverage across all five uploaded books. Retain all errors, negative results and source boundaries. **Zero real-human predictive successes, zero model promotions.**
