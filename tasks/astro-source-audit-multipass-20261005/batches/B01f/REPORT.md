# Astrology source audit: birth chapters and the first complete directions chapter

Date: 2026-10-06. Batches B01f and B01g. Source: Ptolemy, *Tetrabiblos*, F. E. Robbins translation, supplied 1964 reprint of the 1940 edition.

## Completed work

The scheduled English III.6–III.9 reading is complete. Work also continued through the entire III.10, including its worked directional calculations and closing qualification. This is source extraction and bounded arithmetic replay, not a personal reading, a medical forecast or a complete primary-directions engine.

| Scope | New source records |
|---|---:|
| III.6–III.9: historical birth classifications and conditional survival/rearing rules | 29 |
| III.10: selection, Fortune, prorogation, qualifications and worked examples | 34 |
| This pass | 63 |
| Cumulative with earlier batches | 227 |

Ptolemy now has **34 of 61 sections read**, with **27 unread**. Book I remains complete; Book III is 10/14. Book II is explicitly deferred to its general/mundane pass, not discarded. All Book IV remains pending.

Main text was read from the III.6 heading on PDF279/printed255 through the end of III.10 before III.11 on PDF331/printed307. Relevant English notes on facing pages were followed. Source images governed numerical ambiguities. The Greek was not independently translated and the full critical apparatus was not collated. Record counts are organizational units, not independent predictions.

## 1. The same zodiacal interval does not imply the same directional interval

III.10 explicitly rejects using ordinary ascensional times for every position. Rising, meridian, setting and intermediate positions require different measures (PDF311–319, printed287–295).

The author's worked example keeps the same two ecliptic points—the beginning of Aries and the beginning of Gemini—while changing the first point's position relative to the horizon and meridian. The rounded results are:

| Position of the starting point | Directed interval in equinoctial times |
|---|---:|
| Rising | 46 |
| At the Midheaven | 58 |
| Setting | 70 |
| Three ordinary hours west of the Midheaven | 64 |

These are not four estimates for the same chart position. They demonstrate why a fixed 60-degree ecliptic subtraction cannot substitute for the source's temporal geometry (PDF319–325, printed295–301).

The chapter assigns one equinoctial time to one solar year in this historical technique (PDF313/printed289). An equinoctial time here is a degree of equatorial rotation, not a day of secondary progression. Reproducing the arithmetic does not establish that the resulting number predicts a lifespan.

The new reference code replays the supplied signed distances and ordinary-hour magnitudes. It does not calculate actual natal coordinates, choose every directional arc or implement the full forecasting method.

## 2. A page-image check changed a numerical reading

Robbins gives more precise values in his notes. On PDF321/printed297, the original image reads **147 times 44 minutes**; the searchable text layer misreads the minutes as **14**. The same note gives the hour magnitude as **17 times 6 minutes 30 seconds**.

Using these finer inputs reproduces a rising interval of **45°05′** and a setting interval of **70°23′**, matching the values reported in the notes. These are kept as a separate commentary-precision track, not substituted silently for the author's rounded 46 and 70.

The later interpolation shortcut is explicitly approximate. The recorded examples give 62 when two ordinary hours from the Midheaven and 66 when two hours from setting; the shared midpoint is 64. They are different positions, not contradictory answers. Numerical tests preserve the direction and do not hide negative values with an absolute-value operation.

## 3. Fortune has an explicit convention in this edition

The adopted main text says to measure from Sun to Moon in following-sign order and project the same distance from the Ascendant, **both by day and by night** (PDF299–301, printed275–277).

The corresponding bounded calculation is:

`Fortune = (Ascendant + Moon − Sun) modulo 360`

The note reports other transmitted wording and the editor's objections. We retain that separate textual layer. A later source profile using a nocturnal reversal must identify it as a different convention, rather than treating the two formulas as interchangeable.

This calculation can subsequently support the inheritance and sibling-co-residence passages already extracted. It does not itself validate any of their interpretations.

## 4. An adverse contact is not the complete judgement

The chapter states that the listed destructive places do not inevitably produce that outcome. It then specifies prevention and competition conditions (PDF309, printed285).

Among them are benefic terms, qualifying benefic rays, the unequal following-degree limits of **12° for Jupiter and 8° for Venus**, bodily latitude mismatch, and the number and power of competing testimonies. Under-beams restrictions can exclude assistance as well as harm.

The 12°/8° values belong to this particular protective-ray condition; they are not a general instruction to use those numbers as universal aspect orbs. The helper tests only the directed-distance component after the other conditions have been established.

The latitude detail in III.9 has a different provenance: Robbins reports **Cardanus's interpretation** of an isosceles opposition as opposite equal latitudes as well as opposing longitudes (PDF290, printed266). That interpretation is retained as commentary, not promoted to an undisputed general definition.

## 5. Finding the encounter and judging its consequence are separate

After the numerical procedure, Ptolemy returns to assistance, affliction and temporal ingresses to distinguish the outcome (PDF329, printed305). An exact calculated encounter is not, by itself, a forecast of the kind or severity of an event.

The original topical familiarity still matters. The later treatment of divisions of time and ingresses remains a dependency for fuller implementation; it has not been read merely because this chapter refers to it.

## 6. The source itself permits past-event selection—with a research boundary

The end of III.10 discusses uncertain or competing rulers: calculate their encounters and either prefer those that agree most with past events for predicting the future, or retain all as equally powerful and judge degree (PDF329–331, printed305–307).

This is a source-authorized selection procedure, not an instruction to prohibit learning from known history. In this project, selecting a candidate using those past events is **development fitting**. Reproducing those same events is not independent validation; later untouched outcomes must remain separate. No existing fitted rule or personal birth time was changed in this pass.

## 7. Historically uncomfortable chapters remain in the coverage record

III.6–III.9 discuss sex at birth, multiple births, extraordinary births and children who are not reared. Their literal claims, inherited conditions and translator notes are preserved as historical source material, without converting them into modern identity or clinical classifiers.

Several methodological distinctions survive independently of those claims. III.8 says its opening adverse pattern also occurs in other nativities, so that pattern is explicitly insufficient by itself (PDF285/printed261). III.7 changes the subject from the native's birth to a mother's multiple pregnancies when the relevant angle changes from Ascendant to Midheaven (PDF283/printed259). III.9 includes exposure/abandonment as well as non-survival, and retains rescue and rearing-by-other-parents versus own-parents branches (PDF288–295, printed264–271).

Such distinctions cannot be replaced with one generic “bad birth” outcome. Missing support for a condition also remains unknown, not automatically false.

## Tests, preservation and continuation

**39 new reference and integrity checks pass locally.** They cover all four rounded worked examples, the finer commentary track, interpolation endpoints and direction, Fortune's day/night convention, seasonal-hour units, bounded ray distances, Cardanus's explicit geometry example, invalid inputs, and source-record/reading-receipt integrity. The accompanying integration verification records the run with the 142 earlier checks.

These tests do not certify a complete source interpretation, an independently translated Greek text, a complete chart engine or predictive validity. No Swiss Ephemeris calculation was required for this supplied-number replay. No new OCR run, external reviewer, personal prediction or runtime promotion occurred.

All previous source batches, retained astrology/numerology candidates and personal prediction freezes are preserved. Raw books, full extracted text and page images remain private and outside Git.

**Next: III.11–III.12**, from the III.11 heading on PDF331/printed307 to the end of III.12 before III.13 on PDF357/printed333. The next headings were located, but those chapters are not counted as read. This is a completed increment of the owner-authorized multi-pass audit, not completion of the whole corpus and not a background-work claim.
