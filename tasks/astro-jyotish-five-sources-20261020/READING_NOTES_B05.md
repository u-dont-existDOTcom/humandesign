# JYOT B05 — Jaimini computational variants and birth-time sensitivity (2026-10-21)

**New batch:** 20 source-located technical notes in `SOURCE_CANDIDATES_B05.json` across Sanjay Rath's *A Course on Jaimini Maharsi's Upadesa Sutra* and the supplied Portuguese BPHS. These are **source texts and computations**, not evidence of astrological predictive accuracy.

## What is textually stable and what is not

Rath **PDF355** prints Jaimini Sutra **1.1.4** and interprets primary *argala* as influence of planets in **2nd, 4th and 11th** from a sign/planet (order in the sutra is fourth, second, eleventh). In **PDF361**, the blockage places are **12th, 10th and 3rd**, respectively, matching the same structural account in the BPHS Portuguese translation **line2659**. However, Rath's explanatory insider/outsider psychological terminology and his relative strength interpretations are **modern commentary**, not direct verse wording.

Rath **PDF377** prints Sutra **1.1.30**, the basic Arudha count: count zodiacal signs from a sign to its lord, then the same count forward from the lord to the provisional Arudha. **PDF379–381** prints Sutras **1.1.31–32**, exceptions when provisional reflected signs coincide with the reference sign or its seventh, using a tenth-sign adjustment. Arithmetic must use precisely documented inclusive counting and special cases.

**Consequential unresolved fork:** Rath's illustration **PDF379** keeps the final *sign* the same but presents two possible precise Arudha *degrees*. With Aries Ascendant **9°50′**, source-rule sign count leads to Leo: he reports **Leo 9°50′** under one convention and **Leo 20°10′** under his own reflection convention. The modern commentator explicitly encourages readers to compare them, without a blinded comparative test. These choices can change fine-grained D9/D60-derived conclusions even when the sign stays fixed. Record as **separate frozen computational branches**, not a silent numerical correction.

The same Rath volume's Arudha Table64 **PDF382** labels Upapada as the twelfth-house pada **A12 / UL**. The **BPHS Portuguese editorial note** line2625 proposes an alternate 12th/2nd base by ascending odd/even signs. Note: the alternative is expressly an editor's interpretive note; it must not automatically supersede Jaimini's sutra or become the only modern implementation.

## A highly sensitive special Ascendant: Prāṇapada

Rath, lessons20 and22, **PDF415–418, PDF452–453**, discusses sunrise-based special ascendants; the supplied BPHS Portuguese text **lines524, 530, 536** gives structurally comparable cycles.

Assuming the Sun-reference longitude and sunrise are locally fixed, Rath's rates are:

| Special Lagna | Change per hour | Change per minute |
|---|---:|---:|
| Bhava Lagna | 15° | 0.25° |
| Hora Lagna | 30° | 0.5° |
| Ghatika Lagna | 75° | 1.25° |
| Prāṇapada | **300°** | **5°** |

Rath's **PDF453** formula is equivalent to `Pranapada = (Konarka + 300 × elapsed_hours_since_sunrise) mod 360` for the described convention. Its local time derivative is **300°/hour = 5°/minute = 5 arcminutes/second**. A **30° zodiacal sign is traversed in 6 minutes**, and the arc size of a **D60 segment, 0.5°, is traversed in 6 seconds**. This makes a highly exact recorded birth time and correct local sunrise necessary to claim fine-grained Prāṇapada state as unique. It says nothing about whether the formula predicts any human trait.

**Arithmetic reproduction of the book's example:** Konarka **190°09′13″**, birth elapsed **20h56m48s**. Calculated longitude is **354°09′13″**, matching the example printed at PDF453 exactly. This checks *only the multiplication and modulo arithmetic*, not astronomical ephemeris provenance, the correct traditional method or empirical forecasts.

Rath specifically describes civil-day rollover for births after midnight (PDF453). At minimum, any deterministic engine should propagate birth-time uncertainty through local-date sunrise choice and no longer claim a single sensitive state when the uncertainty covers several candidate signs/divisions.

## Varnada differences and unverified examples

Rath **PDF423–425** describes a **sign-count** Varnada method and also explicitly documents a **degree-based alternative** used by other astrologers. BPHS Portuguese **lines552–570** conveys sign/parity counts and a dasha timing scheme. Those are version forks, not grounds to silently choose whichever birth chart looks more accurate.

The Portuguese BPHS **line564** assigns both the 3rd and 11th from Varnada to longevity of **older siblings**, an apparent internal duplication where a younger/older distinction might have been intended. It must stay **uncorrected in source attribution** until an original-language collation. Line570 asserts that Bhava/Hora special ascendants are common to all places, even though preceding formulas start at **sunrise** and ordinary sunrise varies by date/place. This may be compression or mistranslation; do not infer location invariance from this wording alone.

Rath **PDF473** gives his practical timing of love marriage/childbirth from third of Prāṇapada and the dasha/antardasha/pratyantardasha hierarchy. The same paragraph says **arranged and love marriages** differ in interpretation. This is a modern explanatory model using mostly known cases, not a verified universal deterministic ancient rule.

Rath also makes high-stakes claims in **PDF454** about conception viability and neonatal life, and literal hemispheric brain-function claims in his **PDF382** commentary. Preserve them as examples of historical/modern beliefs **not established by medical or neuroscientific evidence**. No clinical advice, predictions of miscarriage or mental diagnoses may be derived from them.

## Status and next continuation

This reader's five source-only batches now hold **113 research entries** (B01 24, B02 10, B03 37, B04 22, B05 20). A new model variant becomes relevant only if it has exact mathematical implementation, data-independent rule choice, fixed response mapping and ethically appropriate prospective outcome evidence. None has been promoted or evaluated.

Next: compare exact Sanskrit printed sutras and calculators for Arudha, Varnada and Pranapada; continue reading remaining house/planet-specific source chapters to discover distinct candidate targets. Do not overwrite other astrology reader's Western/Chinese registries, questionnaire, participant answers or model.
