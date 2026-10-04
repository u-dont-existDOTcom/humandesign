# CAMPBELL_YOUR_DAYS_V1 — supplied-book source specification

Status: SOURCE-AUDITED CANDIDATE pending the common freeze manifest. No owner-history fitting. This is a reconstruction of Campbell's historical claims, not a statement that numbers cause personality, illness, wealth or relationship outcomes. An unresolved source branch remains unresolved in this specification.

## C01. Exact source, pagination and coverage

Florence Campbell, *Your Days Are Numbered: A Manual of Numerology for Everybody*, DeVorss & Company, **23rd printing, 1985**, ISBN **0-87516-422-6**; copyright1931, renewed1958, as stated on supplied leaf6. The upload is a ZIP of **260 OCR-text leaves, not page images**. Body pp.1–246 correspond to leaf=printed page+12. Front matter occupies leaves1–12; leaf259 is blank; leaf260 is an unnumbered back cover. The last addendum is signed Florence Evylinn Campbell and must not be omitted. Input SHA256 `3c5a3e88456767f29a11dbbb13e8f8a0b679330787fc21cff42708a0f1fb0f96`.

Every supplied leaf was read, including examples, all31 birthday entries, alphabet/plane tables, temporal tables, final astrological addendum and back cover. There are **no available source pixels** with which to certify OCR/diagram layout. Table ambiguities are flagged, not silently visually certified. The derived Latin-letter plane table can be cross-checked against the author's detailed prose and Ford counts, but this is not a facsimile verification.

| Part / chapter | Printed pages | Entire layer covered |
|---|---:|---|
| I.1 Vibrations | 1–15 | Primary triad, constructive/negative/destructive aspects,11/22, general classification |
| I.2 Soul Urge | 16–26 | Exact alphabet, phonetic Y/W, component sums,11 distinct interpretations |
| I.3 Quiescent / Expression / Impression | 27–42 | Three different constructs, calculations and all11-entry banks |
| I.4 Life Path and birthdays | 43–69 | Component date arithmetic,11 Life Paths,31 separate days, chart examples |
| I.5 Name changes | 70–78 | Fixed versus changeable layers, selection sequence, examples, adoption/marriage/signatures, lag |
| I.6 Universal Year | 79–85 | Calendar arithmetic, transition overlap,11 entries |
| I.7 Universal Month | 86–88 | Addition and11 entries |
| I.8 Universal Day | 89–95 | Addition,9 entries plus11/22 qualifications, historical examples |
| I.9 Personal Year | 96–104 | Personal versus universal priority,11 entries and tides |
| I.10 Personal Month | 105–108 | Addition, September reinforcement,11 entries |
| I.11 Personal Day | 109–123 | Addition,11 entries, special activity-date catalogue |
| II.1 Symbolism | 127–132 | Geometric, cosmological, Tarot/number rationale |
| II.2 Alphabets | 133–135 | Language/environment-dependent alphabet rules |
| II.3 Inclusion | 136–143 | Frequency table, master safeguards, Ruling Passion |
| II.4 Karmic Lessons | 144–150 | Missing digits, nine meanings, compensation and timing |
| II.5 Subconscious | 151–155 | Distinct-count formula, seven entries3–9, crisis reactions |
| II.6 Planes | 156–163 | Four planes × three classes;26 letter-specific interpretations |
| II.7 Elements | 164–167 | Four trinities, dual6, transmutation and association table |
| II.8 Corner / Key / First Vowel | 168–178 | First-letter/first-name, squared Key, Eccentric Angle, sound classes, seven vowel planets |
| II.9 Cycles / Pinnacles | 179–195 | Three life stages, Moon/PY timing, four peaks, all11 meanings |
| II.10 Challenge | 196–207 | Two sub-Challenges plus main, subtraction,0–8 meanings and qualifications |
| II.11 Vocation | 208–213 | Seven-step whole-chart synthesis |
| II.12 Testing numbers / Triads / Correspondences | 214–222 |13/14/16/19, three triads, colour/music/gems/planet numbers |
| II.13 Associations | 223–230 | Within-chart comparison, romance, friendship, business, places |
| II.14 Immediate Period | 231–243 | Concurrent name tapes, Essence, dates, letter combinations, interaction warnings, full Ford example |
| Final words | 244–246 | Historical assertions and **late astrology integration** |

## C02. Primary hierarchy and what the labels mean [pp.2–5,31–39,43–50]

Three main influences: **Soul Urge / Ideality = motive, HOW; Expression / Ability = familiar capacities, WHAT; Life Path / Destiny = opportunity and new lesson, WHERE**. Birthday is a major modifier within the Path, especially its middle stage. Do not call Campbell's Expression her Destiny; here Destiny is the date-derived Life Path. The birth name gives the tools and accumulated experience; the date directs what must be learned. This differs from Jordan's description of Birth Force as already-given talents.

The consonant sum is **Quiescent Self**, the private fantasy/self-at-rest, explicitly **not what other people see**. Impression usually follows Expression, but **has no infallible computed number**; one is advised to consider the three major positions and actual presentation. Subconscious Self is a third different construct: habitual interpersonal/emergency response from distinct included digits, not the consonant total and not ability.

There is no universal numeric weighting of the triad. Functional priority changes with question: name choice begins with Path; vocation begins with Expression, then opportunity; marriage begins with Soul. No LifePath+Expression Maturity/Reality number or universal current-name Minor triad is supplied.

## C03. Exact alphabet and competing arithmetic modes [pp.13–17,31,68,75–77,137,143,232]

Ordinary alphabetic-cycle values are1=AJS,2=BT,3=CLU,4=DM,5=ENW,6=FOX,7=GPY,8=HQZ,9=IR, with **K explicitly11 and V explicitly22** in the primary letter table (p.16). K/V remain qualitatively masters when placed in compact Inclusion bins2/4. The transit table expressly gives **K two years, V four years** (p.232); neither is an11- or22-year transit.

Let `r` reduce to1–9; `m` reduce but stop at11/22. The author says never reduce11/22 as final Soul/Expression/Path results; masters behind a final may be reduced for addition but their influence retained (pp.13–14,137). Date examples retain a master component in the arithmetic (Washington2+22+4=28/1, p.44); name examples often write compact K2/V4 instead. These permissions **can change whether a final master appears**. Preserve:

- `literal_letter_branch`: K11,V22 in initial name sums; retain every source compound.
- `compact_letter_branch`: K2,V4 for arithmetic, master-letter flags retained.
- `master_component_retained` versus `master_component_root_for_addition` where the text permits both.

These are declared source tensions, not interchangeable hidden implementation defaults. A single name component **KIRK** gives literal40/4 versus compact22: both have the same digital root but only one final master. This is a method test, not a participant prediction.

For the name, sum and reduce **each component separately**, then combine component results. Store raw letter sum, component reduction chain, final generating sum and final result. Soul and Quiescent use the same component construction on their respective letters. **Expression must be independently recomputed from all letters**, not by adding Soul+Quiescent: that shortcut can create or erase a master (p.31 footnote,137). Never combine a favourable subset of components or Cycles just to manufacture11/22 (p.137).

Higher compounds matter as modifiers, not an author-complete1–78 table. Ten is reduced to1 while retaining its higher-cycle meaning (p.13). The special Testing Numbers13/14/16/19 have their own position-dependent rules below. No33/44 master-number family is declared.

## C04. Name roles and normalization [pp.17,70–78,133–135,193]

For the natal chart use every name given at birth. Later marriage/adoption/professional/spiritual-use changes are external angles of development, not deletion of natal Soul, Path or lessons. Nicknames and pet names show the response of the particular people using them. Signatures have a separate practical presentation function. There is no rule that a legal act alone activates a new dominant natal name. The text mentions baptism/record, but does not resolve every delayed-baptism versus original-naming case. Retain naming chronology rather than silently treating any later baptismal name as original.

The author permits adding a middle name or **initial** to a changed name (p.78); do not import Jordan's refusal to read initials into this rule. No precise expansion-versus-letter treatment for all initials, title prefixes, suffixes, apostrophes, hyphens or multiple surnames is provided. Nonletters have no values in the table, but compound-changing token boundaries must be explicit implementation assumptions or branches.

The native alphabet/environment matters (pp.133–135): chart people in their own language; an adopted-country alphabet is said to become applicable with an adopted name and environment. The supplied volume gives no complete alternative-script tables or universal transliteration algorithm. Do not transliterate non-Latin names as if Campbell specified the result. Diacritics and differing pronunciations remain explicit input uncertainties.

## C05. Vowel, consonant and sound rules [pp.16–17,170–178]

AEIOU are ordinary vowels. **W is a vowel only after another vowel and sounded as one with it**, such as AW/EW/OW. **Y is a vowel after another vowel when sounded as one (AY/EY/OY), or when no other vowel exists in the syllable.** Otherwise use the consonant class. Every syllable requires a vowel; source phonetic examples must not be overridden by a universal letter-only Y rule. A vowel mask must be fixed from the actual pronunciation before calculation, with multiple pronunciation branches preserved when uncertain. W cannot be the first vowel in this scheme because it follows another (p.177).

The separate First-Vowel layer uses long/positive, short/receptive and diphthong/dual sound classes. It is **not** a different name-letter numerical table. The author's examples use historical English pronunciations and even call some written combinations diphthongs that modern phonetics might analyse differently; do not silently modernize them or assign a sound from spelling alone.

## C06–C10. Reproducible chart calculations and interpretation inventories

| ID | Calculation | Source-specific function | Pages |
|---|---|---|---:|
| C06 Soul / Ideality | Componentwise vowel sums, final11/22 retained | Intent, attitudes, principles;11 entries1–9,11,22 | 16–26 |
| C07 Quiescent | Componentwise consonant sums | Private idealized fantasy when alone;11 entries | 27–31 |
| C08 Expression / Ability | Recompute componentwise using **all** letters | Capabilities/vocational tools;11 entries | 31–38 |
| C09 Impression | **No uniquely specified formula**; commonly Expression, with all3major positions considered | Observable presentation and chosen image;11 entries | 38–42 |
| C10 Life Path / Destiny | Reduce month, day, birth-year separately preserving11/22; combine, preserving finalmasters. Keep permitted intermediate-reduction branches | New lesson, opportunity, people/environment;11 entries | 43–50 |

Amelia Clare Bronn: Soul component roots7,6,6→19/1; Quiescent7,6,3→16/7; Expression5,3,9→17/8 (pp.17,27,31–32). Washington February22,1732:2+22+4=28/1. Hoover August10,1874:8+1+2=11 (p.44). These illustrate **component arithmetic**, not universal master handling at every intermediate step.

Eleven recurring themes do not replace the distinct banks:1independence/creation;2cooperation/reception;3expressive art/joy;4order/service/work;5freedom/experience/change;6love/duty/adjustment;7analysis/inner knowledge;8executive material power;9universal service/art;11vision/revelation;22practical universal mastery. For Soul these are wants; for Expression capabilities; for Path lessons/opportunities; for Quiescent imagined private situations; for Impression projected style. The constructive, negative and destructive banks are separately enumerated for all11 values pp.7–12. **No birth/name algorithm selects the aspect**: the text attributes it to conduct. Do not infer criminality or retrospective spiritual failure from a numerical match.

Interpretation-bank page keys: Soul1p18,2p19,3p20,4pp20–21,5pp21–22,6p22,7p23,8p24,9pp24–25,11pp25–26,22p26. Quiescent1–3p28,4pp28–29,5–7p29,8–11p30,22pp30–31. Expression1–2pp33–34,3p34,4pp34–35,5p35,6pp35–36,7p36,8pp36–37,9/11p37,22pp37–38. Impression1–2p39,3–6p40,7pp40–41,8/9/11p41,22pp41–42. Path1p44,2/3p45,4/5p46,6pp46–47,7p47,8/9p48,11/22p49.

## C11. All31 birthdays, not just their roots [pp.50–67]

Use raw day1–31 plus reduced/master result. Birthday is lifelong but most active in the middle Cycle; the rough28–56 statement (p.50) is refined by C25's1PY-boundary rule. Conditional claims below are authorial and not personal advice. Medical/physiognomic claims are catalogued but excluded from testing actionable health guidance.

| Day | Distinctive emphasis beyond root | Page(s) |
|---:|---|---:|
| 1 | Independent planning/reasoning, sensitivity and unused power; procrastination | 50 |
| 2 | Emotional/environmental sensitivity, affection, rhythm and music | 51 |
| 3 | Imaginative language, public expression, recovery from emotional crises, varied activity | 51 |
| 4 | Nature/home/duty, tireless practical work, rigidity and restrained affection | 51–52 |
| 5 | Adaptability, variety, scientific/legal possibilities, dislikes ties despite marriage recommendation | 52 |
| 6 | Need for appreciation/company, idealized changing affections, professional/artistic rather than mechanical | 52–53 |
| 7 | Specialization, intuition/analysis, deliberate waiting; discourages marriage in its Cycle | 53 |
| 8 | Large public/business organization; own leadership rather than equal partnership | 54 |
| 9 | Public/philanthropic/artistic reach, strong will; warns of marriage endings in its Cycle | 54 |
| 10 | Many simultaneous capacities, isolated responsibility, creative business and non-domestic hospitality | 55 |
| 11 | Master inspiration/drama, determination with fluctuation and extreme feeling | 55 |
| 12 | Magnetic speech/argument, design, need for intellectual occupation and finishing | 56 |
| 13 | Creative/restless1+3 behind disciplined4; stubbornness, practical construction and misunderstood feeling | 56 |
| 14 | Dual reasoning/prophetic tendencies, large business, change; early marriage favoured; risk-taking claim | 57 |
| 15 | Attraction/help, scientific professional capacity with musical expression, self-sacrifice without submission | 57 |
| 16 | Analytical reserve with home need, internal complications/procrastination, wants affection | 58 |
| 17 | Financial stewardship, independent leadership with subordinate partners, proof-seeking | 58–59 |
| 18 | Responsibility/public administration, change/travel, repeat efforts; warns of broken engagements | 59 |
| 19 | Broad1–9 span, independence, professions, personal adjustment and varied surroundings | 59–60 |
| 20 | Protected small-group/detail work, knowledge collection, family/country and ensemble music | 60 |
| 21 | Voice/art/literature/education; sensitivity and suspicious imagination affect marriage | 60–61 |
| 22 | Master intuition plus practical ideals, broad construction/public concerns, balance | 61–62 |
| 23 | Practical/technical interpersonal usefulness, sympathy, social self-sufficiency rather than art | 62 |
| 24 | Persistent activity with change, artistic/dramatic/business scope, magnified feelings, domesticity | 62–63 |
| 25 | Intuition/occult/art plus concealment and vacillation; needs concentration | 63 |
| 26 | Introspection, unfinished starts, art/diplomacy, domesticity; early marriage favoured | 64 |
| 27 | More material9, independent leadership/literature; strong marriage disposition but9Cycle warning | 64–65 |
| 28 | Affectionate, unconventional1, executive sacrifice/ambition, freedom and impermanence after ideals realized | 65 |
| 29 | 11-derived inspired leadership/unifying, emotional extremes and absorption in personal dreams | 65–66 |
| 30 | Fixed opinions, imagination, teaching/social management, loyalty with flirtation | 66 |
| 31 | Original practical/creative work, travel, early marriage/responsibility, enduring memory of help/injury | 66–67 |

Day27's marriage disposition and a9Cycle marriage-start warning are **different propositions**, not a typo to delete. High-risk financial/medical/supernatural prescriptions are not adopted as advice.

## C12. General classifications and triads [pp.14–15,32–33,217–218]

One={1,2,3}:personal/self-development; Many={4,5,6}:family/community, with7a separate bridge still concerned withmany; All={8,9,11,22}:universal. Retain the7bridge rather than forcing an undocumented three-bin score. Ford's example uses a classification display without resolving all general-case7 allocation details.

Within={1,3,5,7,9,11}, Without={2,4,6,8,22}; **1,6,22are dual**. Count underlying component/letter occurrences where the examples do so and keep final-position labels separate. Do not confuse this with modern psychometric introversion.

Triads: Mental/angular1/4/7; Emotional/triangular3/6/9; outward/curved2/5/8. These are **not** the Planes' individual-letter classification. Master membership in the three ordinary-digit triads is not separately specified.

## C13. Inclusion, intensification and Ruling Passion [pp.136–143]

Count every birth-name letter in its reduced1–9bin, while flagging K11/V22. Preserve totals and allnine counts; do not count the component roots in place of letters. Washington counts [2,1,0,0,5,2,3,1,2], total16. A full interpretation reads each excess/deficit in relation to main numbers, not a free tally of favourable hits.

RulingPassion: copy histogram; **subtract2from count5**, then report largest adjusted count(s). Ties are permitted: Washington5and7both3. It concerns enjoyable hobby/preoccupation, not Soul motivation. The source does not specify flooring a negative adjusted5count, or a required margin/minimum. Preserve negative arithmetic internally and do not invent a threshold.

**Ford discrepancy:** counts [0,0,0,1,2,2,1,1,2] give adjusted maxima6and9, yet p.242 says RulingPassion=None. Keep formula result{6,9} and printed-example None as an unresolved disagreement. No fitted tie-breaking rule.

Nine emphasis banks pp.141–143:1will/self;2tact/detail/feeling;3verbal/art expression;4concentration/work;5change/experience;6duty/adjustment;7analysis/spiritual enquiry;8finance/management;9humanitarian feeling. Except explicit>2sixes possibly cosmic responsibilities, no complete numeric threshold model for “many/few” is supplied. Qualitative K/V are not read simply as2/4 (p.143).

## C14. Karmic Lessons and echoes [pp.144–150,193,240]

Missing inclusion bins are lessons, distinct from Testing compounds13/14/16/19. A corresponding Soul/Expression appearance mitigates the karmic quality but leaves the weak link;11partly compensates absent2, not completely. Same missing digit appearing in a Cycle/Pinnacle/PY/PM/PD is a claimed activation of its lesson. Keep original missing set even when a chosen name supplies it; the author describes help in learning, not erasure of historical natal input.

Allnine lesson meanings:1initiative/decision;2detail/cooperation;3self-expression/confidence;4patient work/foundation;5adaptation/experience;6responsibility/relationship adjustment;7inquiry/faith;8material stewardship;9empathy/universal concern. The text's past-life blame, illness and criminality assertions are historical claims, not established personal facts or participant-labeling rules. No objective test determines whether a lesson has already been mastered.

## C15. Subconscious Self [pp.151–155]

`Subconscious=9-number_of_missing_bins=number_of_distinct_reduced_letter_values`.

Not Quiescent. It refers to unplanned/emergency interpersonal reactions. Interpretation entries are3(scattered confrontation),4(detail-bound),5(restless/disorganized),6(family-protective),7(reserved/prayerful),8(efficient organization),9(philosophical/generalized). The author says3is lowest found, not an arithmetic constraint: names with fewer distinct bins are possible. Return1/2with **interpretation unavailable**, not an invented3floor. Formula alone does not determine whether an individual is altruistic or safe in crises.

## C16. Exact Planes × subdivisions [pp.156–163,209,243]

**Count letter instances** in fourplanes and threeclasses; do not sum their numerical weights. Table reconstructed from p.157text plus detailed prose and Ford's example:

| Class | Mental | Physical | Emotional | Intuitional |
|---|---|---|---|---|
| Inspired | A | E | O R I Z | K |
| Dual | H J N P | W | B S T X | F Q U Y |
| Balanced | G L | D M | none | C V |

All26letters occur exactly once. Report fourrow totals, threeclass totals,12cells, counts/fractions of total letters; no need to reduce counts to Jordan-style PlanesII meanings because Campbell supplies no such forty-cell second system. Physical and Intuitional letters differ byindividualletter even at same numeric value; **numeric grouping is expressly insufficient** (p.157).

Ford: Mental2,Physical2,Emotional3,Intuitional2;Inspired4,Dual4,Balanced1 (p.243). Column dominance informs vocation and style. Balance/duality has its own meaning: inspired starters, dual continuers/variable, balanced constructive finishers (pp.158–159). No exact total-score weights are specified.

## C17. All26 letter-specific qualitative distinctions [pp.158–163]

| Letters | Individual distinctions within shared root |
|---|---|
| A/J/S | A directed inspired mind; J variable mental leadership; S emotional/self-related upheaval |
| B/K/T | B shy emotional need for protection; K inspired intuition/invention; T tense, spiritually seeking sacrifice |
| C/L/U | C intuitive balanced spontaneous giving; L mental balanced slower reason; U intuitive dual attraction, concealment and loss |
| D/M/V | D self-contained practical efficiency; M bounded inexpressive material order; V receptive practical master-building |
| E/N/W | E physical inspiration/science; N mental variable truth; W physical duality/sensory instability |
| F/O/X | F intuitive burden-bearing; O emotionally inspired protected inward accumulation; X dual sacrifice/adjustment |
| G/P/Y | G balanced analysis/understanding; P variable mental reserve; Y intuitive fork/choice/perception |
| H/Q/Z | H mental bridge/advancement with strain; Q powerful unstable intuition; Z emotional inspiration joining ideals with feeling |
| I/R | I intense emotional inspiration; R more selfless emotional understanding |

The source explicitly allows constructive/adverse alternatives; no a-priori algorithm chooses between them. Medical, criminality and psychosis assertions attached to letters remain excluded historical material, not diagnoses.

## C18. Elements and all association types [pp.164–167]

Fire={1,3,9};Earth={4,6,8};Air={5,6,11};Water={2,7,22}. **6is multivalued**: personal/material6Earth, transmuted devotional6Air; do not infer its “evolution” from later outcomes. Fire=feeling,Earth=body,Air=spirit,Water=mind. Each trinity proceeds personal→group→universal in the printedorder. To calculate name-element composition use numerical letters/components as the passage specifies; literalK/Vmust retainmasterelement rather than root-bin2/4.

| Pair | Declared relation |
|---|---|
| Fire–Fire | Excess force |
| Fire–Earth | Disciplinary |
| Fire–Air | Congenial |
| Fire–Water | Powerful steam **or** explosive |
| Earth–Earth | Slow/material |
| Earth–Air | Unadaptable |
| Earth–Water | Congenial |
| Air–Air | Superficial/unstable |
| Air–Water | Congenial |
| Water–Water | Static/introspective/unprogressive |

Pairs are symmetric in this association table. Directional “unlocking” is separate:Fire transmutesEarth;Air transmutesWater;FirecanunlockWaterthroughsteam;AircannotunlockEarth;sameelementintensifiesbutdoesnotunlock. The broad sentence “Air mixes with both” (p.166) does not resolve its conflict with explicitEarth–Airunadaptable (p.167); preserve the specific table and note the tension. This is materially different from Cheiro's same-element affinity claim.

## C19. Cornerstone [pp.168–169]

First letter of the first name: preserve its literal letter, number, plane/subclass and element. It is the claimed first influence, even prenatally when already named, with a material-life foundation function. Compare it to Expression and birthday; no standalone weighted formula. It is not the sum of all initials.

## C20. Key, squared relationship and Eccentric Angle [pp.168–170]

Key is the first-name total with compound/master history. Compare its element to the birthday element. Same element may reduce struggle without producing progress. **Squared** means the same actual number, not merely the same root: Ann11 with birthday11 is the example. Preserve raw Key and raw birthday to distinguish11 from29, even if both reduce11. Wording beyond that example does not authorize treating every equal root as squared.

Eccentric Angle=`m(Key_result+Birthday_result)`, keeping permitted reduction branches. Ann11+day11=22 (the author also allows4 “if Ann chooses”); James12/3+day4=7. This is a distinct approach-style number. A modern Rational Thought formula cannot replace it just because some roots agree. The squared relationship and Eccentric Angle are related but different features.

## C21. First Vowel, sound and planets [pp.170–178]

Find the first vowel under C05; classify its actual sound as positive/long, receptive/short, or dual/diphthong. Record pronunciation and the source's examples rather than guessing accent. Letter rulers: **A Mars; E Venus; I Saturn; O Jupiter; U Moon; W Sun; Y Mercury**. The p.172 footnote explicitly says this is not the same scale as number-to-planet correspondences. A=1 does not imply its ruler is Sun in this layer.

| Vowel | General character; sound refinements |
|---|---|
| A | Creative will/progress; short more poised/dreamy; dual fluctuating |
| E | Movement/invention; short persistent/studious or restless; dual confused |
| I | Intense feeling/repetition; short quiet or erratic; dual alternating expression |
| O | Concentration/attraction/slow decisions; short enduring; dual human understanding |
| U | Unusual receptivity/conservation/dreams; short conservative; dual reserved or over-free |
| Y | Perceptive choice; long and short need gentle reasoning; in a diphthong subordinate to the preceding vowel |
| W | Diphthong only, not a first vowel; physical duality with potentially difficult development |

Repetition/excess of vowels modifies interpretation but no numerical threshold is specified. Attached illness and physiological claims are catalogued and disabled. This separate first-vowel analysis must not modify C05's vowel-selection rule after outcomes are known.

## C22–C24. Universal and personal calendar arithmetic [pp.79–123,239–240]

Let `m` preserve masters and `r` return the ordinary root. Formula families:

- **C22 Universal Year**=`m(digit_sum(calendar_year))`; Universal Month=`m(UY+month_component)`; Universal Day=`m(UY+month_component+day_component)`.
- **C23 Personal Year**=`m(UY+birth_month_component+birth_day_component)`. Birth year is not included. Personal Year guides the individual within Universal background (pp.96–97).
- **C24 Personal Month**=`m(PY+calendar_month_component)`; Personal Day=`m(PY+month_component+day_component)`.

Month/day components are reduced from their calendar numbers, with masters retained or explicitly flagged under C03. November is given as2(or11) at p.86. The direct three-term day formula and Personal-Month-plus-day route both appear (pp.109–110). Intermediate master reduction can alter a generating compound or final master; retain the calculation route instead of silently treating all routes as identical.

Examples: 1931 UY5; May1931 UM1; February12,1931 UD1; July4,1776 UD5. Birthday August5 in1931 PY9. PY6 July PM13/4; PY6 February12 PD11 (read11 and2,p.109); PY6 July4 PD17/8. The book has no eight-hour day partition or Cheiro periodicity formula.

Each bank is position-specific: Universal Year pp.80–85; Universal Month87–88; Universal Day89–91 (nine roots plus11/22 qualifications); Personal Year98–103; Personal Month106–108; Personal Day110–123. Eleven-value theme index:1 start;2 collect/cooperate;3 express/socialize;4 work/order;5 expand/change;6 home/adjust;7 analyse/wait;8 manage/material progress;9 finish/universalize;11 vision/inner work;22 large constructive public service. Negative/destructive alternatives remain part of the claims, not always-positive predictions.

The statement that1910 was the last11 Universal Year and2009 the next (pp.84,95) was **checked, not rejected**: enumerating1910–2009 under the stated digit-sum method gives exactly those two years. A long gap alone is not evidence of an author error.

## C25. Boundaries, seasonal strength, tides and three Path Cycles [pp.50,79,104–106,179–180,193,233–240]

Calendar Personal Year starts **January1**, not the birthday (p.233), but is said to operate fully at the first1 Personal Month (p.240). September intensifies the current year and begins overlap with the next. The old influence weakens through December31 while the new one gains (pp.79,106); no quantitative overlap weights are supplied. If a1PY arrives inside a letter period, its change is most effective after that period ends. Which component governs the delay when concurrent tapes differ is not specified. Each month's influence is strongest **5th–25th** (p.240); that is not a change to its nominal calendar boundary.

Tides (p.104):1 in;2 out;3 in;4 out;5 in;6 out;7 far out;8 far in;9 in/out or cusp;11 out;22 in for humanity. Important-change Personal Years={1,5,9};7 or9 usually means loss;8 is materially expressive,9 emotionally expressive (p.240). This is the author's set, not an outcome-selected transition set.

**Three Path Cycles** have the values birth month, birthday and birth year, with masters retained. First change is associated with the progressed Moon's first return, described as about28years4months; second about56years8months. Numerical operational rule: the1 Personal Year **nearest, before or after, the28th/56th birthday**. Another passage says full effect waits for the next1PY when mid-nine-year section: preserve nearest-versus-next ambiguity (pp.179–180). Exact lunar return needs a progression convention/ephemeris not supplied here; do not assert a precise astronomical boundary from the approximate duration. January versus birthday within the selected year is also not fully specified. This is **not Decoz's36-minus-Life-Path, then27years scheme**.

## C26. All three Cycle-phase interpretations [pp.181–187]

Read the number as environment/opportunity under the fixed Path, and the phase as youth/middle/later. Each of the11 values has a dedicated entry:

| Value | General meaning and phase qualifications |
|---|---|
| 1 | Independence; youth can involve repression, later life continued activity |
| 2 | Reception/detail; youthful dependency, middle diplomacy, later collecting |
| 3 | Artistic/social expression; youth may overexpress, middle/later enjoyment |
| 4 | Work/construction; youth restriction, later work may be chosen rather than necessity |
| 5 | Freedom/travel; youth misuse risk, middle/later movement and variety |
| 6 | Family/duty; youth restriction, middle home, later protection; best marriage Cycle |
| 7 | Inner study/alone; youth misunderstanding, middle specialization, later philosophy; marriage discouraged |
| 8 | Business/power; childhood financial freedom can be premature, middle/later achievement |
| 9 | Universal completion; youth difficult, later impersonal service; new marriages said seldom to last |
| 11 | Inspiration/revelation; a child may express its2 aspect |
| 22 | Broad practical mastery and public leadership |

Timing is C25, not a further number cycle inferred from these meanings.

## C27. Four Pinnacles, timing and echoes [pp.187–195]

Using date components and the intermediate master branches in C03:
`P1=m(month+day)`; `P2=m(day+year)`; `P3=m(P1+P2)`; `P4=m(month+year)`.

`end1=36-LifePath`; `end2=end1+9`; `end3=end2+9`; fourth lasts through remaining life. The text does **not** demonstrate whether a master Life Path is reduced for the duration calculation: preserve36-11 versus36-2, and36-22 versus36-4. Washington LP1 gives35,44,53; Pinnacles=[6,8,5,6] (pp.190–191). Age ranges “1–35,35–44” and “lasts until44” do not resolve every inclusive-birthday convention. Record explicit operational choices or return both branches.

Cycles and Pinnacles are distinct, usually overlapping. Coincident changes are explicitly important (p.189). Pinnacle changes are said to occur at exact computed times, but full influence may await a1PY (p.193). Pinnacles describe **events, reactions and attainment**, not the Cycle's environment. Phases: first personal development; second obligations; third broader achievement; fourth retrospection/future. All11 number meanings are covered in pp.194–195.

Echoes have specified positions: a Soul match favours heart's desire; Expression match assists ability; Path match assists opportunity; an unlearned Karmic-Lesson match is difficult. There is no numerical stacking weight, impact scale or probability.

## C28. Two sub-Challenges and one lifelong main [pp.196–207]

Reduce all date masters before absolute subtraction:
`c1=abs(r(month)-r(day))`; `c2=abs(r(day)-r(year))`; `main=abs(c1-c2)`.

**No fourth Challenge** is supplied. Washington=[2,0,2]. First sub-Challenge covers first Cycle and part of second; second covers the rest of second into third; the main is lifelong. Exact independent subperiod ages are not supplied.

All0–8 meanings appear:1 assertion versus ego;2 sensitivity/cooperation;3 expression versus frivolity;4 work versus rigidity;5 freedom/letting-go versus impulse;6 ideals versus domination;7 repression/faith;8 material judgment;0 choice/all qualities. Nine never appears arithmetically. The author says only the individual can accurately identify whether the number is being under- or overworked (p.199); this is not an a-priori behavioural classifier.

The assertion that8 occurs only with0 needs scope: a **main8** requires its immediate subpair{0,8}, but a sub8 need not accompany another0. Counterexample date components1,9,2 yield8,7,1. Preserve the qualified correct statement and the overly broad wording rather than altering subtraction. Zero is not numerically9 despite the spiritual equation at p.207.

## C29. Testing Numbers, distinct from missing-digit lessons [pp.214–217]

13,14,16,19 are warning/testing compounds;13 is said not always to be listed. Keep generating position and compound route.

| Compound | Position-specific warning |
|---|---|
| 13/4 | Constructive work versus dalliance; not intrinsically evil |
| 14/5 | Change/freedom; Soul interruptions in feeling; Expression disappointment/rebalancing; Path learning to have, hold and let go |
| 16/7 | Faith/spiritual foundation; Soul broken ideals/alliances; Expression loss of position; Path repeated letting-go |
| 19/1 | Obligation/endurance; Soul life-secrets/confrontation; Expression possible loss at the finish; Path repayment of past burdens |

Special associations:14 Mars/Waters of Lethe;16 Uranus/Falling Tower;19 Saturn/Rising Sun. These are not the general number-to-planet table at p.221. The supplied source includes grave medical/death/past-life-blame assertions: they are historical claims, not participant advice. Arbitrary substring compounds do not automatically become dominant natal debts. No universal chart-position weight is provided.

## C30. Within-chart comparisons [pp.223–226]

Compare Soul–Expression, Soul–Path and Expression–Path by (1)elements; (2)same number, compatible parity, opposite parity; (3)higher/lower numerical value. Preserve dual1/6/22 qualifications without inventing an overriding parity rule.

Soul=Expression can overdo or stagnate. The author suggests using their **sum/Essence as a constructive Expression** (p.224): this is a counselling overlay, **not permission to rewrite the natal Expression from C08**. Same Soul=Path is easy but less stimulating; compatible parity supports growth; opposite parity frustrates. Same Expression=Path supports self-perfection; compatible parity is called most fortunate; opposite parity demands difficult adjustment.

Higher Soul than Expression means more ideas than outlet; higher Expression means less motivating desire. Higher Soul than Path means experiences must be transcended; a higher Path demands growth. Higher Expression than Path casts the person as teacher with a limited market; a higher Path than Expression supplies demanding opportunities and helpful associates. Position and direction matter; equality is not universally good or bad.

## C31. Romance, friendship, marriage timing and business [pp.223–229]

Calculate both full charts. Marriage begins with **Soul–Soul**, elements and parity; **ignore higher/lower numerical rank between people**. Same Soul brings mutual understanding with stagnation risk; complements provide stimulus; opposites are strongly discouraged, although the author immediately concedes adaptation exceptions. Different Expressions are preferred for variety. Compare both Paths and capacity to live with different opportunities; compare Karmic Lessons and mutual supply of missing qualities; then both Cycles, Pinnacles and Personal Years.

A9 Cycle/Pinnacle is said to risk ending a new union. Personal Years3/5 scatter;7 makes physical adjustment difficult;1 starts are usually kept at least their nine-year cycle;2/4 are secure;6 is best for marriage;8 strong/balanced. Cross-person ExpressionA=PathB is a teacher-to-pupil relation, with B potentially tiring of it. No weighted or calibrated compatibility score is supplied.

Friendship uses similar principles less strictly and may change with a new Pinnacle when Souls are irreconcilable. **Business instead prefers same Expression and different Soul, including opposite Souls**, for varied policy/reach. Same Soul and Expression can stagnate. A marriage rule must not silently become a business rule.

## C32. Name-change magnitude and activation [pp.4–5,70–78]

Natal Soul, Path and required lessons remain. Nevertheless, changed external circumstances/opportunities are claimed capable of transforming an entire life: this is not a negligible-effect claim. A genuine personal desire/impulse is required; an imposed change is not helpful. Establishment takes **the better part of a year** (p.78), not a sourced exact365days or immediate switch. Neither effect size nor legal-trigger formula is supplied.

Selection sequence: Path opportunity; existing abilities including Expression, Key and Cornerstone; current Cycles/Pinnacles; missing qualities; desires and changed context. Married/adopted names bring new ties, environment and adjustments. A name may expose an existing writing/public talent without creating it from nothing. Famous-name counterfactuals are not controlled evidence. The rare “wrongly named” exception has no independent test and cannot justify renaming merely because a reading misses.

## C33. Complete vocational procedure [pp.208–213]

Seven ordered considerations: (1)abilities—Expression/Corner/Key; (2)opportunities—Path and elements; (3)tendencies—Birthday, Planes, first vowel; (4)preferences—Soul/Ruling Passion; (5)possibilities—remaining Inclusion/Planes evidence; (6)present Cycles/Pinnacles/PY/UY; (7)barriers—lessons and Challenges. Disliking an occupation is not proof of absent capacity. Perfect fit among all parts is not expected. Authorial career recommendations are not modern job-selection validation.

## C34. Immediate Period: concurrent letter tapes [pp.231–238]

Every birth-name component has its **own concurrent tape**; do not merge multiple middle names. Each letter lasts its ordinary reduced value in years, including K2/V4. Component period is the sum of durations; repeat indefinitely. Start at birth, completed age0. For `t>=0`, let `u=t mod period`; select the first cumulative endpoint greater thanu. All initials operate together at birth.

Calendar PY/UY rows and birthday letter/Essence rows require a “turn” for correct alignment (p.233). This is a bookkeeping explanation, not a different calendar: calculate each row from its own actual date boundary.

**Eva Amy Downs**, born August12,1920: Eva=E5,V4,A1, period10; Amy=A1,M4,Y7, period12; Downs=D4,O6,W5,N5,S1, period21. Mechanically checked examples:

| Completed age | Letters | Sum | Ordinary root |
|---:|---|---:|---:|
| 0 | E/A/D | 10 | 1 |
| 1 | E/M/D | 13 | 4 |
| 4 | E/M/O | 15 | 6 |
| 5 | V/Y/O | 17 | 8 |
| 9 | A/Y/O | 14 | 5 |
| 12 | E/A/W | 11 | 2 |
| 17–18 | V/Y/N | 16 | 7 |
| 19 | A/Y/N | 13 | 4 |
| 20 | E/Y/S | 13 | 4 |
| 21 | E/Y/D | 16 | 7 |

The printed table's use of2 at age12 preserves an11/2 interpretation question. More importantly, the prose says her marriage at19 would occur with a7 Essence, while its own tape arithmetic gives13/4. The previous7 state occupies17–18. Retain the discrepancy; do not shift the tape to rescue the example. Both literal and compact name arithmetic give Expression7, while her vowel mask (including Y and W) gives Soul7, consistent with the prose. “Eva May” is an isolated textual name slip, not a second subject to substitute.

The instruction to write under1 (“first year”) at p.234 conflicts superficially with age0 wording, but pp.233/236 clearly explain that the first lived year is completed age0. Preserve label ambiguity without silently adding a whole year to every transit.

## C35. Essence, interpretation limits and equality warnings [pp.234–240]

Essence is the sum of active letter values; retain compound and master history. Interpret its own number, then letters/planes, main triad, current Cycle/Pinnacle and Personal Year. Some examples print compact master roots, so distinguish arithmetic11/22 from displayed2/4. Record both letter changes and Essence changes. Nine-year Personal Year recurrence does not make Essence nine-periodic; a joint tape's least common multiple is only a mathematical repeat period.

The author explicitly says **letter-combination knowledge is incomplete**, several volumes would be required, and the brief general table is not absolutely accurate (pp.231–232,238–239). She warns against precise prediction with only this introductory knowledge (p.238). This limitation belongs in a source-complete audit; missing combination meanings cannot be invented and called Campbell's.

**Essence=Personal Year can negativize/overload** rather than simply reinforce beneficially:

| Matched number | Claimed overload |
|---|---|
| 1 | Fruitless overactivity |
| 2 | Disappointment and health/financial stress |
| 3 | Scattered forces |
| 4 | Confining work |
| 5 | Misused freedom |
| 6 | Excess home responsibility |
| 7 | Excess introspection/stagnation |
| 8 | Physical/financial strain |
| 9 | Emotional strain/sacrifice |
| 11 | Mental/nervous strain |
| 22 | Shock warning |

All medical applications remain disabled. This interaction must be compared with other authors at the same positions and scope; it does not contradict every positive echo anywhere in a chart.

## C36. Complete short event-letter table [p.239]

| Domain | Letters and qualifications |
|---|---|
| Change/activity | A,E,N,W,T; T may change home |
| Lowered vitality | B,D,M; health prediction disabled |
| Emotion | I,R,S,U,X |
| Love/marriage | B,E,N,W,M,O,T; Z sometimes |
| Responsibility | F,J,O |
| Secrecy | G,P,Y,Z |
| Finance | G gain; H gain or strain; U loss; N,Q unspecified |
| Delay/accidents | I,R; safety advice disabled |
| Nerves | I,R,K; health prediction disabled |
| Travel | A,D,L,M,O,V,W,X |

Use the26 individual-letter Plane meanings from C17 and the source's combination caveat, not standalone binary guarantees. Eva's particular events are authorial worked readings, not a general age16/19 marriage formula.

## C37. Astrology, Tarot and disabled peripheral catalogue [pp.127–135,171–178,214–222,229–230,244–246]

The **late addendum at p.246 materially expands the method**. Compare planets by sign, house and aspect with these numerical positions:

| Numerology position | Astrological correspondence |
|---|---|
| Soul | Moon |
| Ability/Expression | Ascendant |
| Life Path | Sun |
| Cornerstone | Mercury |
| First Vowel | Venus |
| Birthday | Mars |
| Key | Jupiter |
| Karmic Lessons | Saturn |
| Challenge | Uranus |
| Quiescent | Neptune |

Pluto's place is explicitly unagreed. Examples: a weak Moon may be strengthened by Soul8 or10; a well-aspected Saturn may mitigate karmic numbers. No quantitative aspect strength, orbs, ephemeris, progression convention or combined score is supplied. Catalogue this as a qualitative hybrid layer, disabled for a numerology-only comparison and never imported into Cheiro/Decoz.

Separate **number-to-planet table**, p.221:1 Sun;2 Moon;3 Venus;4 Saturn;5 Mars;6 Jupiter;7 Mercury;8 Sun;9 collective aura/no individual planet;11 Neptune;22 Uranus. Do not conflate it with the vowel planets or position correspondences. Geometry/trinity/22-Tarot symbolism and16Tower/19Sun references are explicit; no complete1–78 Tarot system or Divine Triangle forecast appears here.

**Colour/music/gems, disabled:**1 red/C/ruby;2 orange/D/moonstone;3 yellow/E/topaz;4 green/F/emerald;5 green-blue/G/turquoise;6 indigo/A/pearl or sapphire;7 violet/B/amethyst or aquamarine;8 rose/upper-red/diamond;9 all colours/yellow-gold/opals;11 silver/platinum;22 red-gold/coral. The chromatic table pp.219–220 gives C red,C# red-orange,D orange,D# orange-yellow,E yellow,F yellow-green,F# green,G green-blue,G# blue,A indigo,A# purple,B violet. Earlier F=green versus chromatic F=yellow-green, and the isolated2/B versus D wording are discrepancies, not a quietly harmonized table. Wear Soul colour for relaxation, Expression for ability, Path for opportunity; play corresponding tones/chords. No complete rhythm/composition algorithm is supplied.

**Places/houses, disabled:** place Expression matching a person's Soul supports belonging; place Soul matching personal Expression supports a market; place Expression matching personal Path supplies experience, not necessarily comfort. Streets/houses relate to chosen purpose. No complete abbreviation/apartment/fraction algorithm. Special activity days p.123 include shopping1/2/3, home6, saving7, business deposits1/2/4/8/22, public appearances9, speculation5. They are historical catalogues, not financial guidance. The final instruction allows necessary acts on any day with an adjusted attitude: the preceding warnings must not be recast as absolute safety bans.

**Other claims inventoried:** past lives, Soul choice of birthdate/naming, alleged vibration physics, health/colour causes and ancient transmission. They provide the author's rationale, not controlled validation. Medical, disability/criminality character judgments and risky financial prescriptions are disabled. No causal truth is inferred merely because a formula is reproducible.

## C38. Explicit ambiguity register and implementation boundary

| ID | Unresolved issue or bounded correction |
|---|---|
| C-A01 | Literal K11/V22 versus compact name arithmetic |
| C-A02 | Intermediate masters retained versus reduced; changed final-master generation |
| C-A03 | Y/W pronunciation, multilingual input and diacritics |
| C-A04 | Birth versus delayed baptism/adoption chronology |
| C-A05 | Initials, hyphens, titles and unsupported normalization |
| C-A06 | Impression has no unique formula |
| C-A07 | Ford Ruling Passion None versus formula tie6/9 |
| C-A08 | Unspecified many/few thresholds; adjusted5 count may be negative |
| C-A09 | Subconscious1/2 possible arithmetically but not interpreted |
| C-A10 | Dual6 Earth/Air and unsupplied spiritual-level selector |
| C-A11 | Nearest versus next1PY at28/56; calendar/birthday placement |
| C-A12 | Exact progressed-Moon calculation not provided |
| C-A13 | Master-Life-Path Pinnacle duration and endpoint inclusivity |
| C-A14 | Challenge under/overworking and imprecise subperiod times |
| C-A15 | Broad8-only-with0 statement must be limited to the main8 relation |
| C-A16 | Essence master display and age19 worked-example discrepancy |
| C-A17 | Which letter end delays1PY; unweighted September overlap |
| C-A18 | Astrology overlay lacks weights/orbs and agreed Pluto mapping |
| C-A19 | Explicitly incomplete letter-combination interpretation |
| C-A20 | Special planet/colour scales and internal colour/music discrepancies |
| C-A21 | Eva Amy versus isolated Eva May textual slip |
| C-A22 | Name-change magnitude and “better part of a year” not numerically fixed |
| C-A23 | No objective constructive/negative/destructive branch selector |

Resolved check C-R01: the1910→2009 gap between11 Universal Years is correct under the stated formula; no “correction” is warranted.

A source-complete inventory is not a claim that every instruction has a single computable answer. Implement unambiguous mechanics with exact branches and return missing interpretations/inputs honestly. Do not fill gaps with Jordan, Decoz or Javane–Bunker. Later empirical coding may freeze a transparent operational convention, but cannot repair a miss from this version after outcomes are inspected.
