# JYOT B16–B17 — Broad house/strength, social opportunity and source-layer audit (2026-10-21)

**Owner goal:** read five newly supplied Jyotish books independently of the other long-running astrology reader. This pass uses the uploaded *Sārāvalī*, *Sarvārtha Cintāmaṇi*, and *Jātaka Pārijāta*, plus printed Sanskrit for two *Sārāvalī* points. All texts and SHA-256 are in SOURCE_MANIFEST. **New: 24 source-only candidates in `SOURCE_CANDIDATES_B16.json`; B17 is textual correction, not a new candidate count.** The passage’s traditional claim is not empirical evidence.

## 1. Strength of planets: source polarity is not unanimous

- *Sārāvalī* **5.2–4** (PDF11) prints **nine avasthā states** of a planet (exaltation, own/friendly sign, combustion, defeat and other conditions). The subsequent **27 Graha Samaya** calculation with a 27-fold lookup and a 540÷27 worked example appears in a paragraph expressly labeled **Notes** (PDF12), not those verses. It must be distinguished from Kalyāṇavarman’s own nine-state source.
- The same *Sārāvalī* **5.14** (PDF13) describes retrograde exaltation as failing to produce good results **according to some authorities**; **5.39** (PDF14) describes a retrograde benefic as powerful and a retrograde malefic as causing difficulties. The transmitted Sanskrit itself has alternative readings `फल(बल)` in v14, while v39 contains `वक्रिणस्तु महावीर्याः`; see [Sanskrit Chapter 5](https://www.csu-lucknow.edu.in/e-books/saravali/p6.html). Do not resolve these competing views using a participant’s story or simply choose the strongest-sounding rule.
- *Sarvārtha Cintāmaṇi* **9.4** (PDF222) gives a compound royal/status rule about three planets in friendly signs while retrograde, subject to remaining dignity conditions. Bhasin’s **Translator’s Note**, PDF223 (confirmed page image), generalizes retrogression as **always** strengthening. That sentence is a commentator’s inference, not the text of 9.4.

## 2. Social and political role predictions depend on unobserved opportunity

- *Sārāvalī* **35.2**, PDF95 (confirmed image) says a person from a ruling family becomes ruler with 3–4 strong exalted/mūlatrikoṇa planets, whereas 5–6 purportedly overcome nonroyal family origin. With only 1–2, the translation describes wealth comparable to a ruler but **not** political rule. These are **social-origin-contingent claims**, not isolated chart-to-rank predictions.
- **35.3** explicitly records Yavana, Jīvaśarma, and Kalyāṇavarman interpretations of strong natural malefics yielding respectively cruelty plus political power, courage without rulership, and regional office. The [Sanskrit Chapter35 vv2–3](https://www.csu-lucknow.edu.in/e-books/saravali/p36.html) confirms the disagreement. There is no empirically established winning source variant.
- **35.20–21** (PDF96) confines lunar Adhi Yoga to benefics in 6–8 from Moon **without** Sun/malefic interference. A parser selecting only “benefics near Moon” would miss indispensable textual exclusions.

## 3. Another consequential mistranslation: four aspects, not five/six

The uploaded English *Sārāvalī* **35.6** (PDF95) says an exalted-like Vargottama ascendant/Moon receives aspect from **five or six** planets (excluding Moon). Yet the published Sanskrit [Chapter35 verse6](https://www.csu-lucknow.edu.in/e-books/saravali/p36.html) says `चतुर्ग्रहैश्चन्द्रविवर्जितैः`: **four** planets excluding Moon; a separate verse11 says `चतुराद्यैः` “four and upwards.” This has **high relevance to prevalence**: four aspects may be much more common than five or six. We saved both literal versions in `SANSKRIT_RAJAYOGA_AND_RETROGRADE_VARIANTS_B17.json`. The rule is **not automatically corrected** in a model without a source-version choice.

## 4. Astronomy: all seven exalted vs a six-planet condition

*Sarvārtha Cintāmaṇi* Chapter9 verse3 (PDF222, physical image verified) contains **both** “all planets exalted” and a *different* condition about the Moon exalted at Lagna with six exalted planets. The **all-seven** case is physically impossible under normal geocentric astronomy because Sun must be in Aries and Mercury in Virgo (minimum 120° of longitude separation). **Six** is **not automatically impossible**, as the six may exclude Mercury. That six-planet antecedent would need a separate comprehensive ephemeris/feasibility check; a previous preliminary remark grouping it with seven was **corrected** explicitly.

*Sarvārtha* Ch9.13 (PDF224–225) describes debilitation cancellation producing a ruler; Bhasin’s separate Translator’s Note expresses doubt and proposes a **narrower Lagna** interpretation. That proposed change is editor-derived, not the literal original verse.

## 5. These books explicitly target different people and different times

- *Sārāvalī* Ch7 vv5–6, PDF16 assigns different proportions of success to choosing a matching planetary **year/month/weekday/hour** for an undertaking. The fractions are source-internal symbolic magnitudes, **not measured probabilities**. This concerns *timing an intentional action*, not birth-chart prediction of a person.
- *Sārāvalī* Ch8 PDF16–18 requires the time of **intercourse/conception**, potentially both parents' charts and external reproductive context, to forecast birth characteristics and gestational timing. These are **historically asserted high-stakes health/family claims**, not legitimate medical guidance and not recoverable from natal chart inputs alone.
- *Sārāvalī* **46.30–32**, PDF126, explicitly makes **female religious initiation** and **female Vedic/Vedānta scholarship** candidate chart domains, then discusses applying aspects to the husband.
- *Jātaka Pārijāta* Adhyāya XVI **v5**, PDF947/printed937 (physically confirmed), is a Sanskrit verse specifying the stronger of ascendant/Moon and distinct house targets for women’s fortune, children and married condition. **Above the verse**, Sastri’s **Notes** quote and interpret another authority to redirect predictions supposedly applicable only to men to the husband. The latter is **an editorial-source layer**, not Vaidyanātha’s own v5. It would be improper to rescue a failed person-level prediction by retrospectively transferring its outcome to an untested spouse.
- *Sarvārtha* Ch1 opening PDF7 likewise says natal principles can be used for horary judgments, but *modern experiments* must keep birth-derived forward prediction distinct from query-time reconstruction to prevent information leakage.

## Status and continuation

**24 new B16 source-located annotations; cumulative 181 + 24 = 205 documentary source records.** B15's four conjunction text repairs and B17's numerical disagreement memo are **separate critical comparisons**, not extra source rule counts. No model or questionnaire modification, no person-specific interpretation or predictive validation.

All report files remain under `tasks/astro-jyotish-five-sources-20261020/` on the independent source-reader branch; raw modern copyrighted translated books are not published in the public repository. **Next:** source-critical comparison of remaining chapters (including C15–19 nested conjunction precedence), Priṇḍa rule occupancy stages, and time-bounded evaluation designs after prior methods are frozen. Follow exact source paths and preserve missing outcomes.
