# Hale Denizden / Hatice Baysan — clean-room astrology + numerology first-pass freeze V2

**Status:** FROZEN_BEFORE_HALE_OUTCOME_REVEAL
**Freeze date:** 2026-10-03 UTC
**Supersedes:** the earlier same-day V1 freeze, before any Hale outcome/personality/history reveal. V1 remains in Git history but must not be scored.
**Hale-specific inputs used:** current name, birth name, birth date/time/place supplied by the user — and nothing else.

No prior Hale chats, Memory, survey/Life Patterns responses, biographies, personality descriptions, known events, or other Hale-specific project material were consulted before this freeze. The first-pass result was cross-checked by a blind Claude Opus review packet that contained calculations but no Hale outcomes, followed by one reconciliation round.

## 1. Method and provenance

### Birth instant

- Supplied local civil time: **1994-01-28 00:35, Istanbul, Turkey**
- Historical IANA zone: **Europe/Istanbul**
- Historical offset at that instant: **UTC+02:00**
- Resolved UTC: **1994-01-27 22:35:00Z**
- Turkey's 1994 summer-time transition occurred later, in March; modern UTC+03 was not assumed.
- Coordinate proxy: **41.0138429552247 N, 28.9496612548828 E**, Istanbul city point. Exact birth-facility coordinates were not supplied.

The birth time is user-supplied. Documentary source and actual time uncertainty are unknown. Therefore angle/house claims and angle-target timing events are conditional on the stated 00:35 time; no invented ±-minute confidence interval is assigned.

### Astronomy

- Swiss Ephemeris: **2.10.03**
- Required mode: **FLG_SWIEPH**, fail closed on Moshier fallback
- sepl_18.se1 SHA-256: **ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66**
- semo_18.se1 SHA-256: **1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7**
- HumanDesign/AstroHD base: **chat/v14-cross-rulebook-20260924 @ f4fa0b86593e895328a18d13ec90432c8cb99662**
- Calculation artifact: **CALCULATIONS.json**
- Generic project-domain inspection: **ASTRO_DOMAIN_VOTES.json**

### Astrology hierarchy used here

1. **Primary:** direct source-grounded traditional chart interpretation using the current Lilly / Hellenistic / Jyotish rule families, planetary significations, dignity/strength conditions, houses and exact geometry.
2. **Secondary corroboration:** the pre-existing target-blind project consensus map. Its ontology came from project behavioral research, so it is not treated as a complete generic Hale personality taxonomy.
3. **Tertiary fingerprint only:** Joel's target-fitted V1.4 six-rule subset. Hale scores **1/6**. It contributes no generic personality evidence.

For reproducibility, the entire current V1.4 registry was evaluated outcome-blind: **390 rules**. The raw feature vector contains 36 positive / 14 negative / 255 zero Lilly clauses; 18 positive / 0 negative / 30 zero Phaladeepika clauses; 4 positive / 0 negative / 19 zero Ptolemy clauses; and 4 positive / 0 negative / 10 zero Valens clauses. These counts are a feature inventory, **not** a personality score or evidence that the clauses are independent. The exact vector is frozen in `ASTRO_V14_FULL_RULE_VECTOR_CLEAN.json`.

The broader V1.4 rule library contains source-grounded strength clauses beyond the older source-native Lilly total. In particular it includes a frozen solar-visibility condition; this matters for Mercury, Venus and Mars below.

### Numerology hierarchy

V1 uses the frozen Pythagorean/Decoz-style convention:
- birth-name core profile from **Hatice Baysan**;
- current name **Hale Denizden** as a minor/current-name overlay only;
- Y treated as a consonant by the project freeze;
- first/middle/last name Transit roles preserved;
- with no middle name, Baysan supplies both Mental and Spiritual Transit, per the Decoz convention;
- Personal Years are calendar-linked; Transits/Essences run birthday-to-birthday;
- useful compounds, Master numbers and Karmic Debt compounds are preserved without treating them as scientific causal facts.

## 2. Exact natal chart

### Tropical / Western state

| Body | Tropical longitude | Regiomontanus house | Tropical whole-sign house | Lilly native total |
|---|---:|---:|---:|---:|
| Sun | 7.77° Aquarius | 3 | 4 | **-9** |
| Moon | 12.77° Leo | 10 | 10 | **0** |
| Mercury | 23.34° Aquarius | 4 | 4 | **+11** |
| Venus | 10.37° Aquarius | 3 | 4 | **0** |
| Mars | 29.82° Capricorn | 3 | 3 | **+9** |
| Jupiter | 13.13° Scorpio | 1 | 1 | **+11** |
| Saturn | 29.88° Aquarius | 4 | 4 | **+13** |

Other exact tropical positions used for geometry:
- Uranus **23.17° Capricorn**
- Neptune **21.47° Capricorn**
- Pluto **27.76° Scorpio**
- true North Node **0.64° Sagittarius**
- Ascendant **5.15° Scorpio**
- MC **12.21° Leo**

This is a **night chart**. Under the source framework, Moon/Venus/Mars are the nocturnal sect planets; Jupiter/Saturn are not sect-supported. The implementation does not invent a new negative sect score for them, so this is a qualifier rather than a subtraction from their Lilly totals.

### Lahiri sidereal / Jyotish state

| Body | Lahiri longitude | Whole-sign house |
|---|---:|---:|
| Sun | 13.99° Capricorn | 4 |
| Moon | 18.99° Cancer | 10 |
| Mercury | 29.56° Capricorn | 4 |
| Venus | 16.59° Capricorn | 4 |
| Mars | 6.04° Capricorn | 4 |
| Jupiter | 19.36° Libra | 1 |
| Saturn | 6.10° Aquarius | 5 |
| Ascendant | 11.37° Libra | 1 |

Mercury's 29.56° Capricorn position is close to the Lahiri sign boundary. That is **zodiac-convention sensitive**, not a few-minutes birth-time instability; Lahiri itself is frozen for this version.

### Source-strength pattern

The bounded Lilly source-native totals rank the seven traditional planets:

**Saturn +13 > Mercury +11 = Jupiter +11 > Mars +9 > Moon 0 = Venus 0 > Sun -9.**

That is not an empirical personality scale. It is useful here because it identifies which source-defined significators receive the most support under one historical rule family.

The broader V1.4 solar-visibility rule adds an important qualification:
- **Mercury:** -1 visibility; about 15.57° from Sun — under the beams.
- **Venus:** -1 visibility; 2.60° from Sun — within the usual Lilly combustion range.
- **Mars:** -1 visibility; 7.95° from Sun — within the usual Lilly combustion range.
- **Jupiter/Saturn:** +1 visibility.

These visibility flags do not rewrite the older Lilly native totals; they belong to a broader source-grounded rule layer and are kept separate.

### Tight natal geometry, frozen at <=3°

Body-body:
- Jupiter square Moon: **0.37°**
- Moon opposite Venus: **2.39°**
- Jupiter square Venus: **2.76°**
- Sun conjunct Venus: **2.60°**
- Mars sextile North Node: **0.82°**
- Saturn square North Node: **0.77°**
- Mars sextile Pluto: **2.06°**
- Saturn square Pluto: **2.12°**
- North Node conjunct Pluto: **2.88°**
- Uranus conjunct Neptune: **1.69°**

Angle-dependent:
- Moon conjunct MC: **0.56°**
- Venus opposite MC: **1.84°**
- Jupiter square MC: **0.93°**
- Sun square Ascendant: **2.62°**

For interpretation and later scoring, Moon/MC + Venus + Jupiter are treated as **one connected angular tension family**, not several independent hits. Sun is not folded into that family at the frozen 3° threshold.

### Joel-fitted six-rule fingerprint

Hale activates only:
- Phaladeepika Venus directional strength = **1**

The other five Joel-selected rules = 0, producing **1/6**.

The apparent Sun-Venus conjunction does not activate Joel's Lilly benefic-conjunction rule because V1.4 freezes that source condition to a **1° partile orb**; the actual conjunction is 2.60°. This fingerprint is reported only for comparison with the fitted Joel model.

## 3. Astrology-only first-pass predictions

**D = mostly date-stable planetary evidence. T = materially time/angle/house-sensitive.** These are predictions to score later, not known facts about Hale.

### A1 — Structured analysis and explanation should recur
**Prediction:** difficult or conflicting material should repeatedly elicit organized reasoning, interpretation, explanation, study, or practical problem-solving rather than purely impressionistic processing.

Why:
- Mercury is among the strongest Lilly planets (**+11**), direct and in the night-air triplicity.
- Mercury falls in the 4th house in Regiomontanus, tropical whole-sign and Lahiri whole-sign.
- The project-domain inspection independently gives positive votes for **complex_structure** and **insight_translation** in both Lilly and Jyotish arms.
- Counterweight: Mercury is under the beams in the broader V1.4 visibility rule.

**Status:** D/T. The reasoning signification is date-stable; the repeated 4th-house emphasis is time-sensitive.

### A2 — Effort is strongest when there is something concrete to master
**Prediction:** persistence, technical effort, craft, conflict-resolution or decisive action should be more evident in concrete consequential tasks than as uniformly high everyday energy.

Why:
- Mars is exalted in Capricorn in both tropical and Lahiri calculations.
- Mars is in the nocturnal sect and scores **+9** in the bounded Lilly native arm.
- Hellenistic and Jyotish testimony both support Mars strongly.
- Counterweights: Mars is within the traditional combustion range and is in Western 3rd-house territory rather than an angular house.

**Status:** primarily D; domain of expression is T.

### A3 — Structure, endurance and private foundations should be major organizing themes
**Prediction:** maintaining a durable private base, routines, boundaries or long-term structure should demand sustained attention. Strength here should not imply ease; burdens, limits, solitude or delayed gratification may be part of the same pattern.

Why:
- Saturn has the highest Lilly total (**+13**).
- Saturn is in its own sign Aquarius in both tropical and Lahiri zodiacs.
- Western systems place Saturn in the 4th; Lahiri whole-sign places it in the 5th.
- The generic map gives positive **sanctuary_sensory** support and positive/mixed **retreat_privacy** support.
- Counterweight: Saturn is contrary to the nocturnal sect.

**Status:** dignity theme D; private/home placement T.

### A4 — Public responsiveness is stronger than effortless solar command
**Prediction:** if Hale occupies visible roles, they should more often involve responding to people, changing expectations, care, audience or relational demands than uncomplicated command/status symbolism.

Why:
- Moon is in the 10th in all supplied house frameworks.
- Sidereal Moon is in its own sign Cancer and the Moon is in sect.
- At the stated time Moon is only **0.56° from the MC**.
- By contrast the tropical Sun is in detriment and its bounded Lilly total is **-9**.
- The project-domain map's only clear negative collapsed domain is **recognition_entry**, coming from the Lilly solar arm.

This is not a prediction of obscurity: the angular Moon is direct counterevidence to a simplistic "low visibility" reading.

**Status:** Moon/MC claim T; solar dignity D.

### A5 — Personal preferences, relationships and public obligations should periodically conflict
**Prediction:** affection, agreements, companionship, values or pleasure should sometimes require renegotiation because of competing obligations or visible responsibilities.

Why:
- Moon opposite Venus **2.39°**.
- Jupiter square Moon **0.37°**, Jupiter square Venus **2.76°**.
- At the stated time Venus opposes MC **1.84°** and Jupiter squares MC **0.93°**.
- Venus receives supportive nocturnal/Jyotish testimony but is cadent/peregrine in the bounded Lilly arm and combust in the broader visibility layer.

These contacts are one connected geometry family. They are not four independent confirmations.

**Status:** Moon/Venus/Jupiter body geometry mostly D; MC component T.

### A6 — Resource/achievement capacity is plausible, but overextension is a live counterprediction
**Prediction:** judgment, counsel, learning, resource management or shared responsibility may create opportunity, but taking on too much or allowing obligations to expand beyond preference should recur as a risk.

Why:
- Jupiter scores **+11**, is direct, in its term, and angular in the 1st.
- Jyotish places Jupiter in a kendra and trikona.
- The project-domain map gives positive **resource_motivation** support across Lilly and Jyotish.
- Counterweights: Jupiter is contrary to sect and tightly squares Moon/Venus/MC.

**Status:** D/T.

### A7 — Communication/local coordination should be an arena for initiative and disagreement
**Prediction:** messages, explanation, negotiation, local logistics or coordination should repeatedly become settings where Hale takes initiative, argues a position, solves problems or encounters friction.

Why:
- Mars is exalted and falls in Regiomontanus H3.
- Sun and Venus are also in Regiomontanus H3.
- The project map gives positive **persuasion_strategy** and **network_pathways** testimony.
- Whole-sign systems move Sun/Venus into H4, so this is not equally strong in every framework.

**Status:** T; lower confidence than A1-A5.

### A8 — Romance/affection is salient but should not be forced into "easy" or "difficult"
Venus is supported by night sect and Jyotish kendra/directional testimony, yet is combust, mixed in Lilly strength and entangled in the Moon/Jupiter hard-aspect family. The frozen prediction is **salience plus mixed conditions**, not relationship luck, relationship failure, or a specific attachment style.

### Preserved astrology nulls
The target-blind domain map supplies no affirmative Hale prediction for **emotion_permeability, role_projection, immediate_body_signal, autonomy_direction, consequential_effort, correction_threshold, value_tension**, and several other ontology dimensions. Missing testimony remains **null**, not contradiction and not an invitation to fill the gap narratively.

## 4. Numerology-only first-pass

### Core numbers — birth name Hatice Baysan

| Quantity | Frozen calculation | First-pass hypothesis |
|---|---:|---|
| Life Path | **7** | inquiry, examination, specialist depth, selective trust/private reflection |
| Birthday | **28/1** | initiative and preference for choosing one's direction |
| Attitude / Sun | **29 -> 11 -> 2** | cooperative, responsive or diplomatic first approach |
| Expression / Destiny | **9** | broad-purpose, interpretive or human/collective contribution |
| Soul Urge | **8** | motivation toward capability, resources, effectiveness or authority |
| Personality | **10/1** | outward presentation emphasizing independence |
| Maturity | **16/7** | increasing emphasis on reassessment, understanding and inner standards |

Useful calculation compounds preserved by the declared method include:
- HATICE Expression component **28/1**; BAYSAN Expression component **17/8**.
- HATICE Personality component **13/4**.
- Maturity **16/7**, conventionally labeled Karmic Debt 16 in this numerology school.

These labels are symbolic conventions, not moral claims or evidence that adversity is inevitable.

### Current-name overlay — Hale Denizden

This is a **minor/current-name overlay**, not a replacement for the birth-name profile:

- Minor Expression: **17/8**
- Minor Soul Urge: **7**
- Minor Personality: **19/1**
- HALE consonant component: **11**
- DENIZDEN vowel component reduces through **19/1**

Because the adoption/use date is unknown, no historical onset, current-name Transit timeline or retrospective relationship inference is assigned.

### Numerology predictions

**N1 — Private inquiry should be a real baseline.** Life Path 7 is the central date-derived prediction. Maturity returns to 7, and the current-name Soul Urge is also 7, but those are not three independent trials.

**N2 — The outward style should look more self-directed than the initial social approach.** Birthday 28/1 and Personality 1 predict initiative/independence, while Attitude 29/11/2 predicts a more cooperative or responsive first approach. This is an internal tension to test, not a reason to average everything into "balanced."

**N3 — Tangible effectiveness/resources should matter.** Soul Urge 8 predicts motivation toward capability, resources, authority or results; the current-name Expression 8 repeats the theme conditionally on current-name use.

**N4 — The broader expression should not be purely self-focused.** Expression 9 predicts interest in wider-purpose contribution, synthesis, completion or concerns extending beyond immediate self-interest. This can conflict with the 8 resource/authority motive.

**N5 — Structure/follow-through is the recurring Challenge theme.** Challenges are **0, 4, 4, 4**, with Main Challenge **4**. Because all derive from the same birth digits, the repeated 4 is one structural finding rather than three independent confirmations.

### Pinnacles

Using the frozen Decoz-style calculation:

- Pinnacle 1: **2**, birth through the age-29 boundary.
- Pinnacle 2: **6**, age 29 through the age-38 boundary — approximately **2023-01-28 through 2032-01-27**.
- Pinnacle 3: **8**, age 38 through the age-47 boundary — approximately **2032-01-28 through 2041-01-27**.
- Pinnacle 4: **6**, from age 47 onward.

First-pass chapter hypotheses:
- 2: cooperation/relationships/sensitivity.
- 6: responsibility, care/service, home or durable obligations.
- 8: resources, authority, achievement, management or tangible results.
- 6: return to responsibility/service themes.

### Period cycles

Period numbers are **1 -> 1 -> 5**.

Under the Decoz rule, the First Period ends in the first Personal Year 1 on or after the 27th birthday. For this birth date that is **calendar year 2024**; the second Period then lasts 27 years, to **2051**.

Because the first two Period numbers are both **1**, 2024 changes the **cycle stage** without adding a new numeric theme. It must not be counted as an independent "1 activation" on top of the Personal Year 1.

### Personal Years

Frozen calendar-year sequence:
- 2021 **7**
- 2022 **8**
- 2023 **9**
- 2024 **1**
- 2025 **2**
- 2026 **3**
- 2027 **4**
- 2028 **5**
- 2029 **6**
- 2030 **7**
- 2031 **8**
- 2032 **9**
- 2033 **1**
- 2034 **2**
- 2035 **3**
- 2036 **4**
- 2037 **5**
- 2038 **6**
- 2039 **7**
- 2040 **8**
- 2041 **9**

These supply a fixed sequence of symbolic emphases; they do not guarantee corresponding events.

### Birth-name Transits and Essences

Transits/Essences are birthday-to-birthday. With no middle name, Baysan supplies both Mental and Spiritual Transit, so those two channels are mechanically duplicated and cannot be treated as independent evidence.

Selected future-relevant chapters:
- **2023-01-28 to 2028-01-27:** H / N / N -> Essence **18/9**
- **2028-01-28 to 2030-01-27:** H / B / B -> **12/3**
- **2030-01-28 to 2031-01-27:** A / A / A -> **3**
- **2031-01-28 to 2033-01-27:** T / Y / Y -> **16/7**
- **2033-01-28 to 2038-01-27:** I / Y / Y -> **23/5**
- **2038-01-28 to 2040-01-27:** two successive configurations both yielding **11/2**
- **from 2040-01-28:** I / N / N -> **19/1** for the corresponding active-letter span

The full year-by-year sequence is preserved in CALCULATIONS.json.

## 5. Fused astrology + numerology first-pass

The explicit test is whether numerology adds useful information beyond astrology. Agreement is allowed to motivate later fused-model development; it is **not** evidence of improved accuracy until scored against outcomes and then tested on new cases.

### Independent convergence hypotheses

**F1 — Deep structured analysis.**
Astrology: Mercury is strongly supported in the Lilly/Jyotish frameworks, linked to complex structure and explanation, with Saturn adding sustained structure.
Numerology: Life Path 7 independently predicts inquiry/depth.
**Frozen fused prediction:** consequential or confusing problems should tend to evoke sustained analysis and explanation rather than only rapid intuition or superficial treatment.

**F2 — Agency/achievement should show more through competence than effortless prestige.**
Astrology: Mars, Saturn and Jupiter receive strong source support while the Sun is weak/mixed.
Numerology: Birthday/Personality 1 and Soul Urge 8 emphasize initiative and tangible effectiveness.
**Frozen fused prediction:** ambition/agency should be real, but leadership—if present—should more often appear through competence, planning, responsibility or problem-solving than through uncomplicated status-seeking.

**F3 — Privacy versus public responsibility should be observable.**
Astrology: strong Saturn/private-foundation symbolism conflicts with a Moon nearly on the MC.
Numerology: Life Path 7 favors private reflection, while 1/8 themes favor agency/results and Attitude 2 emphasizes responsiveness.
**Frozen fused prediction:** meaningful tension should exist between needing private mental space and being pulled into visible/interpersonal responsibility.

**F4 — The early-30s chapter should emphasize responsibility/foundation more than the prior Pinnacle chapter.**
Astrology: 4th/private-foundation symbolism is strong.
Numerology: Pinnacle changes 2 -> 6 at age 29 in 2023.
**Frozen fused hypothesis:** roughly 2023-2031 should be more responsibility/home/foundation/care/durable-obligation heavy than the preceding Pinnacle chapter. This is broad and must not be scored as a hit merely because ordinary adult responsibilities increased.

### Complementarity

- Astrology supplies **domain and conflict structure**: reasoning, effort, private foundations, public responsiveness, resource judgment, and a mixed relationship/public geometry.
- Numerology supplies **role distinctions**: inner motive, outward presentation, first approach, and long-term chapter/timing sequences.
- Astrology supplies exact geometrical timing; numerology supplies independent arithmetic cycles.
- The current-name overlay adds a use-name hypothesis astrology cannot generate, but it has no onset date.

### Contradictions that must survive scoring

1. Weak/mixed solar prestige testimony vs numerology's 1/8 autonomy/achievement emphasis.
2. Public/angular Moon vs Life Path 7 privacy.
3. Strong Saturn/Mars structure vs Attitude 2 cooperation/sensitivity.
4. Expression 9 wider-purpose symbolism vs Soul Urge 8 resource/authority motive.
5. Astrology supplies no affirmative **autonomy_direction** vote in the target-blind domain map, while numerology strongly predicts outward 1-style independence.
6. Venus is neither uniformly benefic nor uniformly debilitated across frameworks, so no fused relationship verdict is permitted.

### Double-counting controls

- Cross-tradition reuse of one planetary position is rule-system corroboration, not independent astronomical evidence.
- Moon/MC-Venus-Jupiter is one geometry family.
- Retrograde repeat passes of one transit aspect are one activation family.
- Expression, Soul Urge and Personality reuse the same name letters.
- Life Path, Pinnacles, Challenges, Periods and Personal Years reuse the same birth-date digits in different formulas.
- Saturn return around age 29 and numerology age-linked Pinnacle/Period transitions are age-driven clocks; proximity in 2023-2024 does not make them statistically independent.
- Ordinary symbolic correspondences such as "Saturn = structure" and "4 = structure" can create semantic convergence without independent empirical support.

## 6. Timing/progression methods frozen

Astrology:
1. Exact major transits using the current project timing generator and pinned Swiss files.
2. Secondary progressions using the project-frozen day-for-tropical-year convention.
3. Natal angles included only conditionally on the stated birth time/location.

Numerology:
1. Personal Years.
2. Pinnacles.
3. Period cycles.
4. Birth-name Transits.
5. Essences.

Not promoted into this first pass:
- **Vimshottari dasha:** not currently frozen/implemented as this branch's timing method.
- **Solar arcs / returns:** documented as exploratory/narrowing ideas but not supplied here with an equivalently frozen executable implementation.
- Human Design timing: outside this astrology + numerology first-pass request.

Exact transit/progression contacts are timing anchors, not proof of event type, outcome valence or causal effects.

## 7. Outcome-blind timing windows

The uniform project-native timing run now covers **2020-01-01 through 2041-12-31** using the same current `scripts/partner_future_pilot.py` logic and pinned Swiss files throughout.

- Full timing artifact: **PROJECT_TIMING_2020_2041.json**
- Exact events: **500 transits, 71 secondary-progressed contacts**
- Timing artifact SHA-256: **c069a70313831796d2ef537430d2e298a71eb6cac53f2d07f2aaf381e3ecfadb**
- Fixed window artifact: **TIMING_WINDOWS_V2.json**
- Window artifact SHA-256: **6cf81fe16b9332b07154936bbab7bdb9477ef13197406087dc1e365f5a40c5f2**

Repeated direct/retrograde hits of one moving-body/aspect/target pair are collapsed into one activation family for window interpretation. Jupiter-only activity cannot define a major window. Angle-target events are conditional on the supplied birth time.

### W1 — 2020-2024: dense restructuring, then responsibility/agency transition
**Evaluation status: retrospective-blind, not prospective.**

Astrology anchors:
- Saturn conjunct Mars: **2020-03 through 2020-12**.
- Uranus repeatedly squares Sun/Venus and later Moon/MC; Saturn activates Sun/Venus/Moon/MC/Jupiter through **2021-2022**.
- Saturn conjunct Mercury repeatedly **2022-04 through 2023-01**.
- Exact Saturn return: **2023-03-06**.
- Pluto conjunct Mars: five exact hits from **2023-03-14 through 2024-11-08**.
- Progressed Mars conjunct natal Mercury: **2024-02-16**.

Numerology anchors:
- Personal Years **6 -> 7 -> 8 -> 9 -> 1** from 2020 through 2024.
- Pinnacle **2 -> 6** at the age-29 boundary in **2023**.
- Essence enters **18/9** on the 2023 birthday.
- Period-stage transition occurs in **calendar year 2024**, but the Period number stays **1 -> 1**.

**Frozen prediction:** this interval should contain more restructuring of agency, values/relationships, public/private responsibility or durable obligations than an ordinary comparison period, with 2023-2024 especially emphasizing closure/consolidation followed by a new direction.

**Specificity caution:** Saturn return + age-linked Pinnacle/Period transitions occur around the same developmental age by construction. Their temporal proximity is not treated as three statistically independent confirmations.

### W2R — 2026-01-01 to 2026-10-02
**Evaluation status: retrospective-blind.**

Astrology anchors:
- Pluto square ASC in March/June — **time-sensitive**.
- Uranus square natal Saturn **2026-04-23**.
- Saturn sextile Mars/Sun/Venus and trine Moon/MC through spring-autumn.
- Progressed Moon square Mars and trine Saturn in late September.

Numerology:
- Personal Year **3**
- Pinnacle **6**
- Essence **18/9**

This elapsed portion must not later be called a prospective success.

### W2P — 2026-10-03 through 2027-12-31
**Evaluation status: prospective from this freeze.**

Astrology anchors:
- Progressed Mercury conjunct natal Mercury: **2026-10-21**.
- Pluto square ASC repeats through 2027 — **time-sensitive**.
- Saturn supports Venus, Mercury, Moon and MC.
- Uranus trine Sun in 2027.
- Progressed Moon conjunct ASC **2027-02-06**, then squares Sun, Venus, MC and Moon through August — angle contacts are time-sensitive.

Numerology:
- Personal Year **3 -> 4**
- Pinnacle **6**
- Essence **18/9**

**Frozen prediction T2:** late 2026 emphasizes expression/reframing/analysis; 2027 should require more structure, boundaries and practical commitment. The astrology is mixed rather than uniformly difficult: one identity/angle pressure family is accompanied by several supportive Saturn/Uranus contacts.

### W3 — 2028-2030: sustained direction/relationship/value reorganization
**Evaluation status: prospective.**

Astrology anchors:
- Pluto conjunct Sun: **2028-02 through 2029-01**.
- Saturn squares Mars, Sun and Venus and opposes ASC across 2028-2029.
- Saturn squares Moon/MC and opposes Jupiter in April 2029.
- Pluto conjunct Venus: five exact hits **2029-04 through 2030-12**.
- Uranus and Neptune provide simultaneous easier contacts to Sun/Venus/Moon/MC.
- Progressed Sun trine Jupiter: **2029-02-02**.

Numerology:
- Personal Years **5 -> 6 -> 7**
- Essence **12/3**, then **3**
- Pinnacle **6**

**Frozen prediction T3:** a prolonged redefinition of direction, agreements/relationships, values and visible responsibilities, combining pressure with openings rather than a single positive/negative story.

### W4 — 2031-2033: clearest pre-frozen cross-system phase transition
**Evaluation status: prospective.**

Astrology anchors:
- Pluto opposes Moon/MC repeatedly through 2031-early 2032; MC contacts are time-sensitive.
- Pluto squares Jupiter repeatedly **2031-03 through 2032-11**.
- Uranus trines Mercury and later Saturn.
- Progressed Mars conjunct natal Saturn: **2032-06-09**.
- Progressed Moon conjunct Mars and progressed Venus sextile Mars in 2033.

Numerology:
- Essence **16/7** through the 2031-2032 birthday years.
- Personal Years **8 -> 9 -> 1** across 2031-2033.
- Pinnacle **6 -> 8** at the age-38 boundary in **2032**.
- Essence changes to **23/5** in 2033.

**Frozen prediction T4:** a transition from responsibility/service toward authority/resources/achievement, passing through scrutiny/completion and then a restart/change phase. Public/emotional role and resource/authority decisions are the specified domains.

This is the strongest future window for testing whether numerology adds genuinely different timing information rather than merely restating the astrology.

### W5 — 2035-2037: visible accountability versus flexibility
**Evaluation status: prospective.**

Astrology anchors:
- Saturn opposes Mars, Sun and Venus, squares ASC, and conjoins MC/Moon in 2035.
- Saturn continues hard contacts to Jupiter/Mercury/Saturn through 2036-2037.
- Several progressed Moon contacts accompany the cycle.

Numerology:
- Pinnacle **8**
- Essence **23/5**
- Personal Years **3 -> 4 -> 5**

**Frozen prediction T5:** greater visible accountability/constraint should conflict with a simultaneous push for flexibility/change; durable arrangements should require revision rather than effortless continuation.

### W6 — 2040-2041: major redirection and chapter boundary
**Evaluation status: prospective.**

Astrology anchors:
- Uranus opposes Mars in 2040 and Sun repeatedly through 2041.
- Neptune opposes ASC — time-sensitive.
- Uranus squares ASC and later conjoins MC — time-sensitive.
- Uranus opposes Venus in 2041.
- Progressed Moon opposes ASC and later squares Sun/Venus/MC/Moon.

Numerology:
- Personal Years **8 -> 9**
- Essence **19/1**
- Pinnacle **8 -> 6** at the age-47 boundary in **2041**

**Frozen prediction T6:** substantial redirection of visibility/responsibility, combining completion of an achievement/authority chapter with renewed initiative and a return toward responsibility/service themes.

### Predeclared lower-signal comparison periods

To reduce selective storytelling, **2025, 2034, and 2038-2039** were not selected as major convergence windows by the V2 rule. They remain useful comparison periods rather than being retroactively upgraded after reveal.

## 8. Concise blinded-scoring claim set

### Astrology
- **A1:** consequential/difficult tasks repeatedly evoke structured reasoning, interpretation or explanation.
- **A2:** concrete difficult tasks evoke persistence/decisive effort; shadow risk is rigidity, conflict or overcontrol.
- **A3:** private base/home/foundations, boundaries and durable structure are recurring organizing concerns.
- **A4:** visible/public responsibility is salient, but effortless prestige/status is not predicted.
- **A5:** preferences/relationships periodically conflict with visible or shared obligations.
- **A6:** resource/judgment/learning roles create opportunities but can produce overextension.
- **A7:** communication/local coordination is a recurring arena for initiative and disagreement.
- **A8:** affection/relationship symbolism is salient but mixed, not uniformly easy or difficult.

### Numerology
- **N1:** strong private/investigative tendency (7) coexists with independent outward presentation (1).
- **N2:** tangible effectiveness/authority motive (8) coexists with broader-purpose Expression 9.
- **N3:** first approach is more cooperative/responsive (29/11/2) than the 1/8 profile alone predicts.
- **N4:** Main Challenge 4 predicts recurring structure/follow-through/foundation themes.
- **N5:** Pinnacle 6 from age 29-38 predicts a responsibility/home/service chapter; Pinnacle 8 from age 38-47 shifts toward authority/resources/achievement.
- **N6:** current-name overlay repeats 8/7/19->1, but no onset date or causal effect is claimed.

### Fusion
- **F1:** deep structured analysis is a cross-system convergence.
- **F2:** agency/achievement should manifest more through competence/responsibility than effortless prestige.
- **F3:** a meaningful privacy-versus-public-responsibility push-pull should be observable.
- **F4:** the 2023-2031 chapter should be more responsibility/foundation heavy than the preceding Pinnacle chapter.

### Timing
- **T1:** 2020-2024 — dense restructuring, then responsibility/agency transition. Retrospective-blind only.
- **T2:** late 2026-2027 — expression/reframing gives way to structure/boundaries. Prospective only from 2026-10-03 onward.
- **T3:** 2028-2030 — sustained direction/relationship/value/public-role reorganization.
- **T4:** 2031-2033 — authority/resource phase transition with scrutiny/completion then restart/change.
- **T5:** 2035-2037 — visible accountability/constraint versus flexibility.
- **T6:** 2040-2041 — major redirection plus Pinnacle 8->6 chapter boundary.

These windows may not be widened or moved after Hale outcome/history data are revealed.

## 9. Uncertainties and claim limits

- Birth time is accepted as supplied; source quality and true uncertainty are unknown.
- Istanbul city coordinates are a reproducible proxy, not an exact birth-facility location.
- Angle/house claims and angle-target timing dates are therefore conditional.
- The Moon is faster than the other traditional planets, so its exact degree is more time-sensitive even when its sign remains stable under modest uncertainty.
- Regiomontanus vs whole-sign disagreements are preserved rather than adjudicated by outcome fit.
- Lahiri is frozen; alternative ayanamshas are not tried after seeing Hale.
- Lilly fortitude totals are bounded source-native symbolic weights, not probabilities or validated effect sizes.
- V1.4 visibility qualifiers and V1.3b native totals are different rule layers and are not silently merged into a custom numerical score.
- Jyotish output here is a bounded positional/dignity rule-family reading, not complete Shadbala/dasha astrology.
- The outer-planet timing layer establishes exact geometry under the project protocol; the traditional natal source catalog does not itself establish psychological meanings for Uranus/Neptune/Pluto.
- Numerology is treated as a testable symbolic overlay, not a scientifically established causal mechanism.
- Karmic Debt/Master labels are conventional numerology terms, not moral judgments.
- No specific occupation, diagnosis, relationship outcome, religious belief, trauma history or known life event is predicted.
- No first-pass accuracy claim is made. Numerology has not yet been shown to improve astrology.

## 10. What counts as numerology improving astrology

After freeze, later evidence should be scored in three distinct arms:

1. **Astrology-only:** A1-A8 plus astrology timing/domain claims.
2. **Numerology-only:** N1-N6 and fixed numerical timing chapters.
3. **Fused:** ask whether the numerology information improves prediction beyond the astrology-only arm on predeclared dimensions/windows.

A fused model becomes scientifically more interesting only if numerology:
- repairs astrology misses or adds discriminating information that astrology did not already predict;
- does not merely restate the same broad symbolism;
- improves held-out or prospective performance;
- survives dependency controls and later untouched people/events.

Development fitting on Hale may occur after this freeze, but Hale then remains a development case for any fitted revision. Later untouched cases are required for generalization.

## 11. Reproducibility / evidence artifacts

Primary calculation/provenance:
- `PROTOCOL.json`
- `calculate_first_pass.py`
- `CALCULATIONS.json`
- `calculate_domain_votes.py`
- `ASTRO_DOMAIN_VOTES.json`
- `evaluate_full_v14_library_clean.py`
- `ASTRO_V14_FULL_RULE_VECTOR_CLEAN.json`

Timing:
- `generate_project_timing.py`
- `PROJECT_TIMING_2020_2041.json`
- `build_timing_windows_v2.py`
- `TIMING_WINDOWS_V2.json`

Independent review:
- `CROSS_FAMILY_REVIEW_PACKET.md`
- `CROSS_FAMILY_REVIEW_OUTPUT.md`
- `CROSS_FAMILY_RECONCILIATION_REVIEW.md`
- `CROSS_FAMILY_RECONCILIATION.md`

The V1 same-day freeze is retained only as superseded pre-reveal provenance. V2 is the sole record to use for later Hale comparison.

**Next methodological state:** Hale outcome/personality/history data may be compared only after the V2 freeze hash is recorded. Such evidence may score or motivate a later development revision, but it must not rewrite this first-pass record.
