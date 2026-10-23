# Hephaistio II time-lord reading C02 — calendars, transmitted arithmetic and competing predictions

**23 October C04 Greek-source correction:** The previous 360/365/**375** arithmetic labels in this C02 audit are *accurate for the printed Schmidt English witness* but **do not all appear in the Eulogikon Greek transcription**. [C04 side-by-side numeric register](HEPHAISTIO_C04_GREEK_ENGLISH_NUMERIC_VARIANTS_V1.json) establishes Greek finer **Moon 71** vs English **Moon 81**; Greek fine headline sum **365** vs English sum **375**; Greek primary sum **360** persists, and the finer Mercury **57** differs from initial **52**. Schmidt English 150 and online Greek 150 agree on Saturn→Mercury; the later Valens appendix still gives 140. No proof yet of epagomenal intention or an independent Greek manuscript, and no numeric source was silently changed. Read [C04 report](HELLENISTIC_SOURCE_C04_GREEK_PAULUS_PAPYRUS_20261023.md) before interpreting this file.


**Source-critical correction, 23 October C03:** The previous paraphrase of Schmidt's footnote that *Ptolemy used 2½ days per sign* is **not Ptolemy's main critically chosen reading** in Robbins's Tetrabiblos IV.10 printed p453. Robbins prints **2⅓ days per sign**, and notes a distinct **2½** reading in two manuscripts; additionally his main months count assigns **28 days per sign**. Hephaistio II.28 retains **2½**, while Paulus I.31 gives **1 day/sign**. Read [C03](HELLENISTIC_SOURCE_INTEGRITY_C03_20261023.md) and the [variant register](HELLENISTIC_SOURCE_C03_VARIANTS_V1.json) before implementing calendar calculations. This correction does not alter the ch29/ch36 numerical witness or Saturn→Mars contrast.


23 October 2026 · Source-first audit · Experimental branch · **No runtime model or human predictive claim admitted**

**Machine witness and test:** [Numeric 129-month and 360/365/375-day tables](HEPHAISTIO_II_TIMELORD_NUMERICAL_WITNESS_V1.json), [four stdlib tests](test_hellenistic_period_witness.py), and [six separately gated candidate mechanisms](HELLENISTIC_C01_C02_SOURCE_CANDIDATES_V1.json). Tests passed 4/4 from a clean authenticated-free repository download; they check arithmetic only.\n\n### Firmicus Latin critically checked: English “eleven months” is erroneous

**This resolves one discrepancy described below.** The public-domain **Kroll–Skutsch Latin** text of Firmicus *Mathesis* VI.33.1 (Teubner printed p190) explicitly says `totam X annorum ac IX mensium`, and VI.34.1 (printed p193) independently says `anni X et menses IX`. Both mean **ten years and nine months**, consistent with seven periods totaling 129 months. [Digitized Latin VI, chapter 33–34](https://penelope.uchicago.edu/thayer/l/roman/texts/Firmicus_Maternus/Mathesis/6%2A.html), current page contents directly checked against sections, **not** based on search snippets alone. Thus Bram's English “ten years and eleven months” at PDF pp230–231 is a **published English translation/printing error**, not evidence of a substantive original Latin 131-month variant. The web transcriber acknowledges possible transcription mistakes; independent identical numerals at two separate sections substantially support this conclusion; a physical Teubner scan remains an optional further check rather than a blocking prerequisite.

**Also checked in the same Latin original**, VI.33.5 (printed p191): Saturn assigning fifteen months to Mars yields a **favorable** period by mutual mitigation of contrary powers. This **corroborates the direction of Bram's English Saturn→Mars**, independent of that English printing error, and sharpens the *actual* source disagreement with Hephaistio's **harmful daytime**, comparatively less harmful nighttime passage. It does **not** establish predictive validity or remove the need to match exact period/sect qualifiers.

**Correction of subsequent text in this file:** every reference below to an unresolved Firmicus “10y11m/10y9m source mismatch” means a **Bram-English printing mismatch now resolved against the Latin**. The original Latin cycle length is **nine months beyond ten years**, not eleven. Keep this correction attached when quoting or promoting any dependent source record.

## Reading completed in this pass

Book: Hephaistio of Thebes, *Apotelesmatics* II, Robert H. Schmidt English (1998), SHA-256 `e1f11be1a21924345770d2a31766caa0e15a53274403c360057a3c4bc5221073`. Read **printed pages 80–107, especially ch27–36**, from owned 59-leaf scanned PDF (one facing book leaf per left/right half). Pdf pages **47, 48, 59 were rendered and visually inspected**, in addition to both-half text extraction, to establish that material numeric discrepancies are **present in the printed source** rather than merely OCR output. Other chapter pages extracted as text and compared selectively. No copyrighted whole-book content has been stored in this public repository.

Cross witnesses:
- Vettius Valens, *Anthologies*, Riley translation, source SHA-256 `1abcb8f24a6b649c8e1c66ab0c398f99e8128c09000c7c8cca863a7c3a32ec6b`, PDF **pp170–172** explicitly labeled **“A Fifth-Century Addition”** in Riley. This is a *later appendix*, **not** a secure independent statement by second-century Valens.
- Firmicus Maternus, *Mathesis* VI.33–40, Jean Rhys Bram translation, SHA-256 `0249e8702f15ef1c7220df7eed800340d0953d6b5c01b793a4407f4c44abef70`, PDF **pp230–236** (book printed pp226–232). Contents independently checked in preceding local inventory. Read relevant pairs and baseline cycle, not an exhaustive all-verse Latin critical comparison.
- The Dorotheus Dykes `Carmen` printed IV.1–, PDF pp215–223 provides annual lord, profection, solar return and monthly methods, but those need literal two-system algorithm separation.

## What these texts *actually* specify

| Witness | Fixed-source method or provision | Remaining hard ambiguity |
|---|---|---|
| Hephaistio **II.27** printed 80–82 | Annual projection: each elapsed year advances the Ascendant to another sign; consider ruler's sect, phase, dignity, natal aspects and year's return/transits separately. | Epoch and exact annual clock rule must not be borrowed silently from modern practice. |
| Hephaistio **II.28** printed 82–83 | Months: start from the annual sign and advance **one zodiacal sign per month**; days: advance **one sign per 2½ days** from the monthly sign; compare planets within or aspecting target sign. Schmidt's **fn217**, printed p83, says Paulus uses **one sign per day** and Ptolemy **one per 2½ days**. | The 30-day ideal month, birthday boundary, annual year length, interpolation and traditional day-time divisions must be specified before computation; this is not an empirical claim about a given subject. |
| Hephaistio **II.29** printed 83–85 | A decade/time lord period of **10 years 9 months = 129 months**, distributed across Saturn 30, Jupiter 12, Mars 15, Sun 19, Venus 8, Mercury 20, Moon 25. Starting point normally the well-placed **sect luminary**, with conditional substitution if ineffective. Allocates smaller times in numeric tables. | Tables contain arithmetic discrepancies (below); whether to use proportional rounding, intercalary days, textual emendations or another method is **unresolved**. |
| Hephaistio **II.30–36** printed 85–105 | Detailed conditional predictions for each planetary lord and the recipient of distributed smaller time; **sect, phase, angularity, sign domicile and malefic/benefic testimony often reverse or qualify results**. | One unrestricted planet-pair → “good/bad” scoring rule would distort the source. **Outcome-specific, mutually exclusive predicates** are required. |
| Hephaistio **end II.36** printed 106–107 | Gives a **360-day** main daily year division 85/34/42/54/22/52/71 and a separate finer table, then mentions *alternative* division from the year's sign lord and explicitly notes the different procedures do not agree well. Schmidt **fn259** suggests a resemblance to Valens' releasing, which is his comparison, not the Hephaistio source proving common descent. | Which printed numbers belong to the 360-day vs 365-day procedure? The finer-day tables have internal inconsistent headers. Must **NOT** mix methods or resolve after comparing owner life history. |
| Firmicus **Mathesis VI.33–40** | Recites same seven baseline **129-month** subperiods, with its own full sequence of planet→planet results. Bram's English VI.33/34 inaccurately says *ten years and eleven months* at two points; independently checked Latin VI.33/34 explicitly reads `X annorum ac IX mensium` / `anni X et menses IX` (**ten years, nine months**), consistent with the original 129-month period. | **RESOLVED:** English Bram printing error; Latin source says 10y9m twice. Do not reopen 131-month interpretation based solely on that English mismatch. |
| Valens **later “Fifth-Century Addition”**, Riley **p170–172** | Exposes two competing constructions: approximately weight-proportional subperiod days from total **129**, and repeated **129-day** daily cycles within the current planet's monthly allocation. Later commentary **criticizes the proportional approximation** and prefers the repeating short-cycle calculation; also adjusts intercalary days. | A source-critical *fifth-century textual stratum*, not securely an original Valens recommendation. It cannot be counted as an independent period-efficacy confirmation against Hephaistio. |

## Numerically audited printed discrepancies

Full seven-column readings, exact source page, computed totals and discrepancies are captured in the **machine-readable [period witness register](HEPHAISTIO_II_TIMELORD_NUMERICAL_WITNESS_V1.json)**. They are **source observations, not corrected canonical periods**.

**II.29, printed pp83–84, seven 129-month subsidiary rows.** For each given parent planet, compare declared number of calendar-months ×30 with all seven printed subordinate-day allocations. The resulting totals and differences:

| Parent | 360-day convention would give | Sum of printed allocations | Difference |
|---|---:|---:|---:|
| Saturn | 900 | 913 | **+13** |
| Jupiter | 360 | 365 | **+5** |
| Mars | 450 | 450 | 0 |
| Sun | 570 | 569 | −1 |
| Venus | 240 | 243 | +3 |
| Mercury | 600 | 606 | **+6** |
| Moon | 750 | 764 | **+14** |

Printed **II.29** uses `150` days for Saturn→Mercury; **Riley's separate fifth-century appendix**, PDF p170, gives `140` for that subperiod. This exact **10-day textual/numeric variant** reduces the 913-row to 903 (still +3 vs 900). Several residual discrepancies could represent accumulated per-subdivision rounding, intercalations, different period definitions or corrupt source transmission. The record cannot identify which from arithmetic alone. The comment in II.29 explicitly derives 900 days for Saturn's 30 months and an approximate factor of 7; some other listed row totals differ too much to be explained by rounding each of seven subgroups to the nearest integer alone.

**II.36, printed p106: three different numeric levels.** The opening yearly allocation **85+34+42+54+22+52+71 = 360**. Within its printed fine-division introduction, Hermes has **57** and the Moon **81**, despite the opening **52** and **71**. The fine-divisions' **individual seven-item sums**, in planet order Saturn/Jupiter/Mars/Sun/Venus/Mercury/Moon, are **86,34,42,54,21,57,71**, whose combined total is **365**—not the stated 360, and not the stated alternative 57+81 header in the Moon case. For example Moon's 14+16+7+8+11+4+11 = **71**, despite its local heading `81`.

**Interpretation:** A 360-vs-365 calendrical mixing hypothesis is now *worth checking*, but the sums do not prove that all errors arose from that mechanism. Some numbers could be simple transcription/printing defects, intentionally approximate divisions, or mixed calendar conventions. **Source variants retained, no silent correction**. This is a significant **ENGINEERING_INADMISSIBLE_PENDING_SOURCE_RESOLUTION** gate for any exact chronological claims from this particular table.

## Important *opposite predictions*: Saturn→Mars

The two texts make materially different conditional predictions for the same directional parent→recipient pair, and cannot both be reduced to one supportive “traditional rule”:

- **Hephaistio II.30**, printed p**86–87** (PDF 49L–49R), says Saturn/Kronos distributing months or days **to Mars/Ares in a day nativity is harmful**, with setbacks, difficulties, loss and often dangerous travel; **in a night nativity** the result becomes **less severe and eventually relatively successful**, although not carefree. This is a **sect-dependent reversal**.
- **Firmicus *Mathesis* VI.33 §5**, printed p**226** (PDF 230), gives Saturn→Mars **a favorable period in general**, explaining that opposed malefic powers counteract one another. In the relevant English paragraph this positive rule is **not explicitly scoped by sect**, although section introductory paragraphs require respecting natal condition generally.
- Firmicus VI.33 §4–5 and Hephaistio II.30 both discuss recipients in a 129-month cycle; nevertheless exact timing granularity (month vs month/day), antecedent natal conditions, alternative time lord selection and language-era translation differences must be held constant before calling the outputs direct contradictions for a defined chart. **A genuine source disagreement candidate is identified, not a final historical contradiction solved.**
- **Test construction:** choose **never-tested** chart periods with identical sect, lord, recipient and definitions; freeze both source-specific predicted directions **independently**, capture a predeclared adverse vs favorable objective observation or **abstain** if contextual qualifiers prevent deciding. Do not allow the model to select whichever text matches the person's biography.

## Scientific/source status

**COMPLETE THIS PASS:** audited and visually checked numeric subperiod tables, compared a later Valens appendix, inspected Firmicus VI.33–40 and isolated one clear conditional competing Saturn→Mars prediction. Preserved separate chapter classes, source provenance and unverified calendar interpretation.

**NOT COMPLETE:** Greek critical editions, Hephaistio source-table variants and 360/365 calendar resolution; **Firmicus's relevant Latin cycle wording and Latin Saturn→Mars direction WERE checked**, actual software chart-period implementations; untouched forward-blind human tests; confirmation of any astrological efficacy. These are **not** requirements for recording or exploring other historically clear concepts, but are requirements for *declaring this exact table calibrated*.

**Next concrete research read:** compare sources for the 129-month construction and sunrise/birthday intercalation; audit Hephaistio's 360/365 numerals in an original-language or second translation; then freeze two competing *computable* Saturn→Mars sequences on synthetic neutral charts before any person-specific evaluation. Independently read image-only Paulus/Hephaistio I and their sect/day methods with page anchors as needed. Amazon Gansten book is **not** extracted or a blocker.
