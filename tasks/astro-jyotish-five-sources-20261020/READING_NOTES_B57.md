# B57 — Ārūḍha calculation is not one agreed source algorithm

2026-10-22 UTC. **Documentary source analysis, not human astrology validation.** This continues committed B56 and independently reads the user's original uploaded Sanjay Rath *Jaimini Upadeśa Sūtra* course, Lesson 18, indexed PDF pages 377–385, against two accessible online Sanskrit source layers: *Bṛhat Parāśara Horā Śāstra* Chapter 29 vv1–11 and a posted Sanskrit/English translation of the Venkateśa commentary on Jaimini's sutras. The latter's physical manuscript and *Parāśara*'s critical archetype have **not** been independently inspected. The historical user-uploaded Portuguese Parāśara Ch29 previously appeared in B27's structural map, but its full lines were not freshly readable here; do not claim new Portuguese source collation.

## 1. Shared counting procedure, divergent exceptional padas

Rath PDF377–381 and the displayed BPHS 29.2 count inclusively from each sign or house to its lord, then count the same number of signs onward from the lord. BPHS 29.4–5 explicitly prohibit the ordinary result falling in its own or opposing sign and yield **fourth** for lord placed fourth or tenth, and **tenth** for lord placed first or seventh. Rath's detailed rider and ready-reckoner agree. Twelve symbolic placements (for Aries as source) give the following relative results:

| Lord's relative house | Raw count | Rath / BPHS29 | Venkateśa local |
|---:|---:|---:|---:|
| 1 | 1 | 10 | 1 |
| 2 | 3 | 3 | 3 |
| 3 | 5 | 5 | 5 |
| 4 | 7 | 4 | 7 |
| 5 | 9 | 9 | 9 |
| 6 | 11 | 11 | 11 |
| 7 | 1 | 10 | 1 |
| 8 | 3 | 3 | 3 |
| 9 | 5 | 5 | 5 |
| 10 | 7 | 4 | **unresolved** |
| 11 | 9 | 9 | 9 |
| 12 | 11 | 11 | 11 |

The apparently paradoxical row for **lord in fourth** is supported by an entirely different *Venkateśa* commentary reading: its Sanskrit on `स्वस्थे दाराः` gives **seventh** as the arudha in that case; on `सुतस्थे जन्म` it gives original **lagna itself** for the lord in seventh. An older *Vṛddha Kārikā* verse quoted in the same commentary allows original lagna as pada when its ruler is in lagna or seventh. Thus the result is not simply Rath's calculation with a different numbering offset. The commentary also offers *alternative kāraka* interpretations of both sutras, rather than establishing a universally binding and uncontested local rule. Its text as inspected does **not** explicitly explain the lord-in-tenth case, so the diagnostic version **abstains** instead of inventing a rule. Source context: [Venkateśa own/seventh kārikā](https://jaiminicommentary.wordpress.com/2010/02/02/sutra-1-1-30/), [Venkateśa two exception sutras in 2010 archive](https://jaiminicommentary.wordpress.com/2010/02/), [BPHS Ch29 Sanskrit and gloss](https://enjoylearningsanskrit.com/scriptures/parashara/chapter-29/).

This finding is significant for future software: *source selection changes the astronomical chart features before any predictive weights are considered*. Tests of one school's exceptional placement cannot be marketed as tests of every Jaimini recension. No actual sky or person was evaluated.

## 2. Stronger co-lord versus multiple padas

Rath PDF378 says Scorpio and Aquarius may have a pair of lords and yield **two possible bhāva ārūḍhas**, with a stronger one dominating. BPHS 29.7's Sanskrit `द्विनाथद्विभयोरेवं ... सबलावधि` invokes strength when handling dual ownership. This does not authorize selecting whichever lord fits a known biography. Our source variant module retains two tagged candidates and leaves `dominant_lord=null` until a school-specific strength algorithm has been frozen. Whether multiple placements co-activate and what probability mass either should receive remain **unresolved**.

## 3. Planetary *graha* ārūḍha has an origin ambiguity

Rath PDF378 and the Sanskrit commentary accompanying `यावदीशाश्रयं पदमृक्षाणां` distinguish a planet's *graha ārūḍha* from a house's *bhāva ārūḍha*: count signs from a planet to an owned sign, then continue that count from the **owned sign**, producing a derived sign. In a source-only example Sun in Aries with Leo owned by Sun yields distance five and derived Sagittarius. A modern English gloss below BPHS 29.6 instead says advance the second count **from the planet itself**: this literally gives Leo in the example and algebraically collapses every case to its owned sign. Because this English paraphrase is an editorial gloss, it is NOT sufficient to allege a separate ancient Sanskrit recension. Record the source-layer mistake risk and never silently change the origin. No rule in the quoted bhāva rider automatically supplies a graha rider.

## 4. Exact degrees are a modern method dispute, not fixed by sign verse

Rath PDF379 explicitly contrasts the claimed received usage of carrying over the original longitude in sign with his own recommendation **30° minus original longitude**, while disapproving a third exact mirror-of-longitude approach. His example Aries 9°50′, Mars in Gemini gives the same **Leo** sign in both, but Leo 9°50′ under one and Leo 20°10′ under the other. The cited BPHS29.2 and its exception sutras define **signs**, not exact degree projection. For source input exactly 0° the proposed complement equals 30° (a sign boundary), so the diagnostic code abstains instead of silently reducing it to zero.

## 5. Outcome vocabulary and ethics

Rath distinguishes manifested image, social title, degree of public recognition and the actual underlying state: a title or possession is not automatically personal competence or wealth. BPHS29.8–10 adds historic claims about the *means* of acquisition and differentiates mixed, benefic and adverse influences. These must not become modern criminal accusations or be collapsed with amount of income. This work does not score those historical claims, nor infer anyone's character from a chart.

## Verification and evidentiary classification

`arudha_source_variants_B57.py` plus `test_arudha_source_variants_B57.py`: **31** symbolic source-version and boundary tests passed on clean standard-library Python. Tests enumerate all twelve sign placements, preserve unselected co-lords, expose the planetary starting-point mismatch, and distinguish exact longitude alternatives. Every diagnostic is `score_allowed=false`; no ephemeris, full critical printed Sanskrit, respondent or known birth data. `ARUDHA_SOURCE_VARIANT_MATRIX_B57.json` has **eight** source-criticism records and 12-case table. These are NOT new de-duplicated original five-book source annotations: accepted registry remains **432**, with **zero** independent prospective human prediction successes and **zero** promoted production rules.

**Next executable:** Try an independently photographed/printed BPHS29 recension and original Portuguese Ch29 lines; study Rath Lesson17–18 source original Sanskrit, then continue under-read source passages of the five original books, especially positively and negatively specified career/wealth/relationship targets. Keep unresolved alternative algorithms as abstentions rather than forecast decisions. Do not touch other astrology branches, questionnaire, participant data or model.
