# Jyotish five-book reading lane: first source-critical pass (JYOT B01)

**Date:** 2026-10-20 (UTC). **Owner goal:** incorporate five newly uploaded Jyotish books into the ongoing, methodologically blinded astrology research, **in parallel** with the existing Western, Chinese, and previously opened Jyotish source readers. This branch adds one *new* source lane only: it does not amend the accepted Lilly index, Chinese ledger, astrological scoring engine, participant answers or questionnaire.

**Evidence status:** inventory 5/5, initial 24 locatable **source-only** candidates; no source-critical Sanskrit collation, no human predictions run, no empirical verification, no model promotion. These totals must not be added to historical Lilly/Ptolemy/Chinese record counts.

## Raw-source custody and text quality

The public repository stores a structured source manifest (SHA-256, bytes, page counts, exact filename, translation/editor status), bounded paraphrases, research records and cross-source comparisons. The original 106+ MB of uploaded modern editions/translations are **not uploaded** to this public branch because permission to redistribute them is unestablished; Rath's copyright page specifically reserves reproduction rights (PDF p4). The source material remains in the initiating chat's uploaded files. Future workers must not mistake the manifest for permanent access to the raw bytes.

- **Sarvarth Chintamani**, Vyankatesh Sharma, J.N. Bhasin English translation, Ranjan Publications; 374-page noisy scan. Translator says explicitly that Rahu/Ketu aspects are missing from the author's work and that his team supplied them in notes (PDF p4, introductory note ¶4). His proposed adjustment of Lahiri ayanamsa appears in ¶6 and continues PDF p5. Neither is an original-source planetary aspect/ayanamsa rule.
- **Brihat Parashara Hora Shastra**, Portuguese text by André Kerr, translated from English, 5,941 lines. Physical bytes are **Windows-1252/cp1252**, not UTF-8 (UTF-8 decoding introduces ~20,901 replacement characters). Historical-date and original-author assertions in the modern foreword are not independently verified. Portuguese source has visible technical omissions.
- **Jaimini Maharsi's Upadesa Sutra**, Sanjay Rath Volume 1, 520-page scan. Copyright p4, preface p11: Rath reports four public-domain adhyayas of an alleged original eight and treats Jaimini/Parashara as a unified school. That is **Rath's lineage/interpretive assertion**, not demonstrated agreement of every technical variant. Many examples are retrospectively known cases.
- **Jataka Parijata**, Vaidyanatha Dikshita, V. Subramanya Sastri translation/commentary, 1,094-page scanned compilation. Publisher's note PDF pp2–3 discusses a 1932 edition and textual interpolation; the original author in Adhyaya I sloka 3 (PDF p8/printed p2) expressly says that this work abridges **Saravali**. It cannot be counted as a fully independent witness for matching verses.
- **Saravali**, Kalyana Varma, 150-page searchable English summary, 55 chapters; explicit translator and critical Sanskrit source not yet verified in this supplied compilation. Intro chapter (PDF p5) places it as an expansion of Varahamihira's brief teaching. Detailed multi-planet conjunctions appear in chapter 20 (PDF pp40–43).

## First consequential substantive result: spirituality is a real classical prediction domain

Earlier questionnaire design discussions raised omitted spiritual experience and awe. These texts substantiate a **narrower** source-backed domain of *religious initiation, renunciation, spiritual/ascetic vocation, teachers, discipline and philosophical/religious orientation*. They do **not** by themselves establish source-backed precise predictions about subjective synchronicities, surprise, revelations or sense of wonder; those require a separate targeted source search before questionnaire mappings are claimed to be astrology-derived.

**Traceable lines:**

1. *Saravali* ch20 slokas 1–6 (PDF pp40–41) lists specific strong multi-planet conjunctions associated with renunciation/asceticism. This is not a generic "all spiritual people have a special chart" claim. It requires parsing exact participating planets, strength, conjunction semantics and competing yogas; extreme conjunctions also create severe coverage/prevalence limits.
2. *Saravali* ch20 sloka 21 (PDF p42) distinguishes an **aspiration to enter a religious order** from **actual initiation** when the asceticism-producing planet is combust or otherwise aspected; slokas 22–29 provide further Moon/Saturn and disposition configurations; sloka 37 (PDF p43) gives Raja-Yoga interaction. These are conditional and potentially in tension. Reject a positive-only keyword extraction.
3. *Jataka Parijata* Adhyaya XV slokas 17–18 (PDF pp914–915) includes a three-strong-planets/strong-tenth-house-lord ascetic condition and subcases. Sloka 40 (PDF p922) gives a separate asceticism condition involving Saturn and an isolated/weak ascendant lord. Slokas 41–42 (PDF p923) include Moon in a Saturn decanate/amsa and a non-fulfilment distinction when yoga-producing planets are obscured or defeated. The later Sastri note explains a philosophical interpretation: keep note separate from verse text.
4. The *BPHS* Portuguese section "Yogas de Vocação Espiritual" (text begins line 5509) says four or more strong planets in one house can indicate ascetic vocation. This cross-resonance is **textual/traditional overlap**, not three independent successful predictions or a reproducible quantitative rule.
5. *BPHS* "O Uso dos 16 Divisionais" (line 650) assigns **D20** to religious sense and **D24** to learning, **D12** to parents, **D10** to status/profession, etc. *Sarvarth Chintamani* ninth-house opening (PDF p195/ch7 slokas 1–2) lists *guru*, compassion, *tapas*, charity and prospects in the same house domain. The domain crosswalk is not itself evidence of predictive accuracy.
6. Rath, *Jaimini* lesson 15 (PDF p289), explicitly gives **both seven- and eight-chara-karaka computational schemes** and argues for the eight-planet scheme for living beings; his planet-by-planet **atmakaraka spiritual lessons** (e.g., PDF pp304–306) are modern exposition. Do not present either his scheme-selection rationale or his spiritual prescriptions as literal, unambiguous ancient sutras. A chart calculated under a different charakaraka scheme is a separate frozen model variant.

## Mechanism conflicts/quality defects (do not silently correct)

| ID | Supplied-source observation | Correct disposition |
|---|---|---|
| Q01 | BPHS Portuguese "Categorias das casas" line 702 enumerates the 10th house as both kendra/angle and apoklima/cadent, excluding the ordinary ninth in the cadent list. | Text is internally contradictory. Freeze no categorical rule from this rendering; collate source against Sanskrit/reliable editions. |
| Q02 | BPHS Portuguese "Trimshamsamsa (D-30)" line 629 supplies **five** angular intervals 5,5,8,7,5 degrees, but **four** ruler names Mars, Saturn, Mercury, Venus. | Mark fifth-ruler enumeration **missing**, not algorithmically inferable from this text. Saravali ch3 sloka 15 (PDF p6) independently gives five names including Jupiter as the third; treat as **cross-edition repair hypothesis**, not silently replace Portuguese text. |
| Q03 | Sarvarth Chintamani Bhasin introductory note PDF pp4–5 explicitly supplies Rahu/Ketu aspects not present in original and recommends a shifted Lahiri ayanamsa. | Two **translator-origin** additions; separate author-source and translator model variants. |
| Q04 | Saravali ch20 sloka21 says aspects of another planet can prevent initiation, while neighboring ch20 slokas22–29 use aspects in initiation yogas. | Unresolved scope/precedence. Requires exact source-language logical interpretation, not a blanket aspect cancellation. |
| Q05 | Jataka Parijata first-book author sloka3 declares dependence on Saravali, and editor notes quotations from older works and interpolations (PDF p3). | Assign text-transmission dependency edges; do not multiply classical "witnesses" as if independent. |
| Q06 | Rath derives seven/eight charakaraka scheme selection from his modern interpretation and cites BPHS 34.1–2 at PDF p289. | Freeze branch variants rather than declaring one historically/empirically proven. |
| Q07 | Saravali PDF includes English-only adapted sloka paragraphs without shown original Sanskrit, and Jataka/Sarvarth scans have frequent OCR damage. | Textual page reads support exploration; precise verse semantics and astrology-calculation adoption require authoritative images and textual comparison. |

## Provisional survey/model implications — separate from evidence

- Candidate survey dimensions justified by sources: **formal spiritual initiation/renunciation; intensity of voluntary discipline/tapas; periods of public role followed by withdrawal; teacher/guru/mentorship orientation; pilgrimage/religious practice; education/learning orientation**. Questions must refer to actual behaviors/occurrences and exclude normative labeling. These are **candidate domains, not authorized questionnaire additions**.
- Do not equate Buddhist attainment, mystical experience, religious institution membership, voluntary solitude, dissatisfaction with life, and ordinary spirituality; ancient rules often predict **observable ascetic occupations or obligations**, not subjective sudden insights.
- Do not score an individual's known autobiography against selected rules to optimize the variant. Existing respondents/cases and the cited Sri Aurobindo example are **development/illustrative only**; retain untouched participants, birth-time uncertainty and matched decoys.
- Do not build D20/D24/D60 etc. from text unless the exact subdivision algorithms, ayanamsa, boundary convention, chart/timezone, house model and conflicting transmitted variants are specified and tests protect every boundary.
- Avoid double-counting Saravali/JP/BPHS formula families as three independent pieces of predictive evidence; count predictions per genuine person and unique prediction with dependency structure.

## Next autonomous reading queue for this branch

1. Directly inspect all of Saravali chapter20 slokas 1–37, chart exceptions, ch32 ninth and ch34 house domains; annotate predicates and scope line-by-line, including **negative** cases.
2. Inspect Jataka Parijata Adhyaya XV slokas 15–42 in page images; map exact overlap/differences from Saravali without attributing Sastri commentary to Vaidyanatha.
3. Inspect BPHS Portuguese spiritual-vocation paragraph range plus D1/D9/D20/D24 and Chara Dasha sections; flag every garbled list, confirm against an independently sourced original Sanskrit or reliable critical translation before adding to engine.
4. Inspect Sarvarth Chintamani chapters on 5th/9th/10th house, philosophical/religious practice, marriage, parental outcomes and dasha. Separate Bhasin notes from original slokas; physically verify Sanskrit wherever scans disagree.
5. Inspect Rath lesson15 charakaraka, lesson17 Argala, lesson18 Arudha and lessons20–22 special ascendants/Pranapada; compare sutra text and his interpretation to other independent schools.
6. Derive a versioned, **frozen and testable** candidate model crosswalk only after textual collation; then run preregistered genuinely blinded forward/reverse tests. Report every miss and all unmatched outcomes.

**Current status: OPEN.** First-pass 24 records are inventory/reading candidates only. The other astrology reader's Western and Chinese work and accepted indices remain untouched.
