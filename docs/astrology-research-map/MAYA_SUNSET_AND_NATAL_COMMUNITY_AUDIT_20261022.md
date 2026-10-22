# Maya sunset day-boundary and community natal-rule audit — source reading B02
22 October 2026 · **Current source and engineering evidence only; zero untouched human predictions tested**

## Exact new source checked

**Alejandro Garay and Igor Xoyón**, *Armonización de los calendarios mayas*, Guatemala Ministry of Culture and Sports, 2016, original Spanish PDF. Owner-machine reference PDF: **119 PDF pages**, SHA-256 `16950ebf88f4bb7f0e94315e516aefdf1e99ae3cc3652e78948a2da96454fdf2`; original retained privately, **not distributed through GitHub or the owner ZIP**. Original location: https://mcd.gob.gt/wp-content/uploads/2017/02/Armonizacion-Maya.pdf. Print pp. **39–44** (PDF pp. 43–48), print **58** (PDF p. 62), and print **86** (PDF p. 90) read against the owner's downloaded text-bearing copy.

Their thesis is that the sacred **Cholq’ij** count switches day **when darkness begins after sunset**, whereas the 365-day **Ab’** switches **at dawn** (distinct from Gregorian midnight). They support the proposal with Classic-period epigraphic discussion and early twentieth-century records of **Ixil** and **Jakaltek/Popti'** practice, alongside discussions with contemporary Guatemalan spiritual guides. This is a historically argued **interpretation** rather than an observation proving a single rule for every Maya community and birth-hour across history. The authors separately propose a **40-day Highland Ab' shift** from Classical Lowland Haab' yearly reckoning; none of this requires changing the original date-only Lowland `maya_calendar_reference.py`.

**Source-critical correction:** Print p. 58 says a Guatemalan council of Maya spiritual guides agreed with the proposed dawn/sunset distinction. On the same page **more than 90%** of a workshop supported the date **5 K’ayab’ for the yearbearer celebration**. That percentage is **not** a survey percentage for whether people agree with a sunset rollover; reports must not silently conflate these subjects.

Complementary scholarship: Cano Contreras et al., 2020, DOI `10.19130/iifl.ecm.2020.56.2.0007`, reports persistence and change in Highland practices; the modern communities/variants are **not interchangeable**. A demonstrated calculated day is not proof its birth-trait ascription is predictive.

## New historically grounded phase examples

Source paraphrases here are calendar entries rather than predictions about a person. All matched GMT584283 after the explicit **before/after observed sunset** phase adjustment; not all are independent field observations.

| Gregorian date | Before sunset (sacred day) | After sunset (sacred day) | Attestation, source locus |
|---|---|---|---|
| 1927-03-10 | 1 Kej [calculated] | **2 Q’anil** | Print p.43; Garay/Xoyón recount La Farge's Jacaltec/Popti' night ceremony |
| 1927-03-15 | 6 E [calculated] | **7 Aj** | Print p.43; La Farge historical night report |
| 1939-03-12 | **5 E** | **6 Aj** | Print p.44; author example of sacred and solar different rollover |
| 1939-11-26 | **4 B’atz’** | **5 E** | Print p.43; authors' pre-sunset correction and Lincoln's nocturnal Ixil report |
| 1940-11-25 | **5 Ajmaq** | **6 No’j** | Print p.43; correction and Lincoln's nocturnal Ixil report |
| 2015-02-21 | **3 E** | **4 Aj** [derived] | Print p.86; author's proposed year cycle and following-day schedule |
| 2015-04-02 | **4 E** | **5 Aj** | Print p.86; author provides this explicit before/after-sunset worked example |
| 2016-02-21 | **4 No’j** | **5 Tijax** [calculated] | Print pp.58/86; yearbearer 4 No’j and following sacred day; post-sunset sign extrapolated rather than independent field report |

All 14 explicit phase records are stored with their original status in [MAYA_SUNSET_BOUNDARY_SOURCE_WITNESSES_V1.json](MAYA_SUNSET_BOUNDARY_SOURCE_WITNESSES_V1.json). Earlier Tedlock **1975/1977** numbered day reports remain unchanged. An author presenting a calendar computation based on the same correlation is **not** an independent scientific validation of that computation. Three historical Tedlock matches and the new original documentary evidence increase confidence in a limited **date alignment**, not in birth-character prediction or current community consensus.

## Safe engineering extension: sensitivity, not false clock precision

The new helper `maya_sunset_boundary_sensitivity.py` accepts a **civil date**, declared GMT correlation and one of exactly three externally observed states: `before_sunset`, `after_sunset`, or `unknown`. It computes **only sacred day label/number** and its reference civil date. It never computes a physical sunset, date/timezone transition, Haab, Long Count, horoscope, clinical judgment or personality output.

- Before sunset: date-only reference result for same Gregorian civil date.
- After sunset: sacred-day reference from the **next Gregorian date**, without shifting solar Ab'/Haab'.
- Unknown: **both** candidate days, always `ABSTAIN`. This is not model permission to choose whichever birth-sign fits later answers.

Even with an externally observed before/after sunset, the function returns `eligible_to_score_human: false`: **local birth-day clock rule and historic continuity are not sufficiently verified to promote this as a current specific community birth-chart calculator**. A future birth-clock engine must use location, civil timezone/date-history, precise clock uncertainty and an independently adopted community-specific rule, frozen before responses.

## Two original K'iche' sources — a nontrivial conflict

New [20-day source-domain crosswalk](MAYA_MOMOSTENANGO_ZUNIL_NATAL_DOMAIN_CROSSWALK_V1.json) compares **Tedlock's Momostenango ethnography** (1992 revised, printed pp.110–126) with direct statements by the **Komon Tohil daykeepers of Zunil** (Smithsonian NMAI, *The Meaning of the Days in the Maya Sacred Calendar*, pp.1–3). They are **different communities and source types**. The record explicitly separates each named natal domain from a separate divination-for-a-question/ritual use.

Examples of substantial, test-relevant differences:

| Birth day | Momostenango birth association (Tedlock) | Zunil birth association (Komon Tohil) |
|---|---|---|
| **No’j** | Inventive thinking and problem-solving (p.122) | Prudence/temperament and occupational associations (p.2), **not an explicit natal creativity claim** |
| **Imox** | Pejorative emotional/mental attributes (p.126) | Work, intuitive capacity and **creativity** (p.2) |
| **E** | Historic lineage religious/midwifery roles and longevity (p.118) | Travel, sociability, generosity (p.1) |
| **Toj** | Illness/debt ascriptions (pp.115–116) | Mediation and self-directed learning (p.3) |
| **B’atz’** | Material, marriage and life success (p.117) | Similar generalized fortune, but teaching and interpersonal attributes added (p.1) |

These differences are not a ranking of communities' authenticity. Nor does a shared cultural origin make the separate traits correct, or make a universal homogenized “Maya horoscope” scientifically appropriate. Tedlock pp.127–131 expressly argues against replacing the contextual oral mnemonic and ritual practices with fixed, one-word symbols.

**Ethical boundary:** historically stigmatizing, sexual, health, mental illness, witchcraft, lifespan or harmful negative labels belong in source-critical historical metadata only. They are not diagnoses or proper forecasts for participants. An **unfrozen** experimental test should use consented, nonstigmatizing behavioral measures and preserve omitted classes.

## Noj creativity prediction — experimental design and practicality

Retain the **single-source Momostenango-only** candidate `MAYA-MOMO-NOJ-DIVERGENT-THINKING-DRAFT-01`. A brief laboratory **divergent-thinking** task can be a plausible proxy for the original broader creative/innovative thinking description, **not a direct equivalence**. Before any confirmatory study, choose a known task and language-appropriate independent scoring rubric, preselect one score (e.g., blind-rated applicable originality with fluency safeguards), independent raters and reliability thresholds, and a truly concealed pre-response date-group assignment. Record education, fluency/language, age, birth-time source and opportunity as covariates. Lock all exclusion rules, controls, test direction and false-positive family before learning responses.

An ordinary random sample puts approximately **5%** in Noj (one of 20 day signs). A simplified two-group normal approximation, at two-sided alpha=0.05 and 80% power, unequal prevalence 1/20, with **no attrition or multiple-testing adjustment**, needs approximately:

| Assumed standardized effect (Noj vs other days) | Unscreened respondents needed |
|---|---:|
| 0.5 (large) | 661 |
| 0.4 | 1,033 |
| 0.3 (moderate) | 1,836 |
| 0.2 (small) | 4,131 |

These are planning *hypotheticals*; there is **no measured Maya trait effect size**. The formulas assume independent participants, equal conditional outcome variances, and valid mapping. A tiny self-selected cohort, even if 10/10 subjects match narratives, is not a prospective confirmation. Enrichment/balanced recruitment could cut **completed task** counts but still requires screening enough births; screening must occur without exposing subject predictions or outcomes.

The real parent outcome remains **OPEN** and should not depend on recruiting thousands of people for this one tentative school-specific construct. A mechanically mature independent natal chart hypothesis may be the more practical first untouched human test. Keep the Noj track as an explicitly budgeted side experiment until the clock and construct validity are settled.

## Reproducibility and audit scope

The 2016 paper is not a zero-bias ground-truth authority: it argues from history, interpreted glyphs, other researchers' readings, and practitioner consultations. The new **date-phase matches are engineering/source-regression checks**, and all known source ambiguities remain. No original glyphed codex has been independently deciphered here. No user or other participant's birth data were inspected.

**Tests:** 46 pre-existing map-source checks + **10** sunset-specific and **5** cross-community checks = **61/61** focused tests on the current branch. Calendar data + source/metadata tests do not establish any prospective human predictive result.

**Empirical score:** human forward-blind validations **0**; accepted natal model promotions **0**. The single canonical source-to-human research workflow remains unchanged.
