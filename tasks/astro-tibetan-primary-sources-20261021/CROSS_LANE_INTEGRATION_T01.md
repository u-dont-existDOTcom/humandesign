# Tibetan astrology T01 — integration with Western, Chinese and Jyotish research

Status: **SOURCE AUDIT OPEN — NO PREDICTIVE MODEL PROMOTION — NO HUMAN VALIDATION** (21 October 2026).

## Authority and scope

Owner request (verbatim): "ok then start reading everything you need that's free plus these, in turns, to merge into the other readings we are doing for astro system".

This is a **new independent source family/lane**, not a substitute for Lilly/Ptolemy, BaZi/Zi Wei, Jyotish or the existing HumanDesign human-validation requirements. The existing umbrella mission remains OPEN: reconstruct algorithms, preregister/freeze predictions, independently score blinded human responses against matched decoys and non-astrology baselines, preserve misses and null results. Historical annotations do not establish predictive accuracy.

Research inputs: user's three locally read books (Dorje 2001, Cornu English 1997, Henning 2007); open-access Janson 2014 (first-pass online read); Erlewine 2008 author-hosted free PDF catalog located, full text not yet retrieved. The complete Tibetan original of White Beryl has **not** been read. English versified Moonbeams appears inside Dorje. File hashes/page counts and statuses: `SOURCE_CATALOG_V1.json`; 20 currently verified-against-available-English source annotations: `batches/T01/SOURCE_NOTES_T01.json`. All user-supplied PDF bytes remain outside version control; only derived annotations are committed.

## Material classes and proposed crosswalk

| Tibetan technique/source family | Main comparison and overlapping inputs | Human test outcome class | Separation rule |
|---|---|---|---|
| 60-year animal/element birth year | Chinese BaZi year pillar / 12-animal system | Broad trait, life timing | Shared traditional signs are not independent corroboration; add increment relative to fixed BaZi baseline. |
| Four birth time divisions and element contrasts (White Beryl/Moonbeams) | BaZi Four Pillars, Zi Wei lunar month/day/hour | Traits, lifespan stages, family claims | Distinct rule algebra but partially identical birth input. Freeze sex-specific and calendar conventions and document dependence. |
| Mewa numeric square, parkha trigrams, five personal forces | Tibetan extension of Chinese numerology and elemental divination | Traits, stressors, preferences, annual obstacles | Test as distinct feature ablations, including broad year-sign-only control and conventional covariates. |
| Parent-element coincidence, children predictions | Lilly fifth house, Ptolemy children, Jyotish putra, Zi Wei children palace | Objective number/timing of births (when observed, not lifetime-incomplete) | Exact alternative outcomes (“five OR ten”) and culturally evaluative “useful child” cannot be credited as precise hits. No prospective prediction of high-stakes reproductive decisions. |
| Marriage compatibility and obstacle years | Western 7th house/transits, Jyotish marriage, Zi Wei spouse palace | Relationship chronology and partner attributes | Separate compatibility from predicted event timing; two people’s charts calculated independently, blinded pair baseline. |
| Lunar mansions and planet positions under Kālacakra | Indian Jyotish nakshatra/planetary calculations; Western astronomical positions | Planetary interpretation and timed events | Shared sky positions and inherited Indic methods must not count as independent sources of prediction. |
| Phugpa/Tsurphu astronomical calendars | Chinese lunar and astronomical date engine, Indian Kālacakra, modern ephemerides | **Calculation parity first**, later human predictions | Keep full branch/epoch, sunrise/daybreak, intercalation and tropical/sidereal policies as separate preregistered candidates. |
| Divination-hour, omen and ritual response | Horary/electional versus natal Western methods; Chinese divination | Consult-time predictions only | Divination place/time, family data, ritual amendments, and observer behavior are extra inputs. This arm is NOT pure birth-chart-to-personality. |
| Geomancy and sa-dag/Earth Lords | Chinese fengshui and Bon landscape rites | Geographic/household claims | Separate entirely until exact measurable predicates exist. |
| Doctrinal spirituality, karma, rebirth and Buddhist symbolism | Vedic doctrine; survey spiritual-experience and awe domains | Mostly doctrinal, NOT a demonstrated psychometric predictor | Do not infer that an individual will experience awakening or synchronicities unless an explicit testable natal rule is actually sourced. |

## Important newly demonstrated method boundaries

1. Dorje's English treatment of the Mar-ston fixed natal method counts **136 pebbles** (4 + 1 + 2 + 5 + 100 + 24) and explicitly uses the birth year, month, day, hour as well as query-time and parental inputs. This is not reducible to a zodiac-year profile. See Dorje printed pp.140–144, especially Charts 4.1–4.7 and Moonbeams ff.20a–23a.
2. A clear source-level family claim is that wood+fire parental destiny elements can yield five **or** ten children, while wood+wood yields two with the qualification that only one is “useful.” This is retained as historical source wording, **not** scored as an unambiguous verified hit. Dorje p.176, White Beryl ff.224b–225a.
3. Several competing even/odd classifications of signs, elements and trigrams occur **inside** White Beryl's own presentation of distinct traditions. They are not safely collapsible into a single table. Dorje pp.172–174.
4. Cornu's worked horoscope requires a birth-time conversion from civil/local solar/Greenwich time as well as month, day and year mapping; old numerical ephemeris/ayanāṃśa policies must be validated against Henning and modern astronomy rather than copied into the prediction runtime. Cornu pp.216–223.
5. Henning clearly distinguishes a reasonably accurate **mean** synodic month from inaccurate epoch positions and competing Phugpa/Tsurphu results. Validate calendar astronomy separately from natal interpretation. Henning pp.7, 9, 11, 14, 20, 23; Janson 2014 §1 and Table 1.

## Minimal test contract, pre-registration, and warnings

- Version all variants before deriving a participant's predictions. A single flattering narrative across variants is prohibited.
- Explicitly declare all input fields and whether the rule can be computed from **birth data alone**. Do not mine parental data, an interview, or divination observations after seeing the answer key.
- Freeze participant birth input, chart computation and all predicted questionnaire response probabilities before opening real responses; keep a separate final untouched cohort.
- Compare at least (a) random/matched birth decoys; (b) non-astrology trait and chronology baselines; (c) Tibetan without shared Chinese/Indian features, as a preregistered ablation; (d) competing calendrical traditions only if originally specified.
- Preserve factor correlations, rules from the same inherited tradition and multiple descriptions of the same claim under dependency caps. Historically copied claims are not repeated confirmations.
- The proposed crosswalk is **architectural interpretation written for this research**, not an assertion that a Tibetan classic provides modern survey-item predictions.
- Do not use medical, relationship-safety or reproductive guidance based on divination.

## Next safe reading and computational work

1. Read Dorje **all of printed pp.138–192** systematically, matching natal diagrams and Moonbeams verses to exact rules, then marriage pp.192–224 and obstacles pp.224–260. Preserve both the text and printed plate image/table and the original folio citation.
2. Read Cornu Chapters 4–10 including mewa/parkha, five forces, day-hour, and horoscope interpretations; record contradictions and incomplete table definitions. Verify Cornu's 1950 worked example by independent chronology and astronomical calculation.
3. Read Henning Chapter I fully then Chs. II–VI and Appendix I; implement only after a versioned, independent calculation specification and benchmark receipts; test Phugpa versus Tsurphu with an unchanged synthetic calendar case suite.
4. Retrieve/read author-hosted Erlewine free PDF and check against earlier primary translations (not an independent tradition by itself). Read Janson's full arXiv treatment, including appendices, and locate reliable Tibetan original witnesses for White Beryl, Moonbeams, Phugpa manuals.
5. Expand TIB-R0021+ source notes; do not alter Lilly/Ptolemy, BaZi/Zi Wei or Jyotish accepted indices on this branch. Integrate only through a reviewed cross-lane merge preserving all prior accepted notes/counts unchanged. No blind human evaluation until model freeze and clean human partition are independently verified.

**No new scientific claim is established by this first pass.** It is a source-grounded research and test-design advance. The parent request remains OPEN.
