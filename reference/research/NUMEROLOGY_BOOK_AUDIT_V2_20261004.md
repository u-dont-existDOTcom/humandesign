# Numerology book audit V2 — four sources, separate methods

Date: 2026-10-04. Source scope: the four supplied books, plus immutable inherited CHEIRO_CHALDEAN_V1 and DECOZ_CURRENT_V1 snapshots. **Methodology first; no owner-history fitting.** The exact source-specification freeze is established by `numerology_v2_20261004/freeze_manifest.json`, not by a passing test or an earlier candidate heading.

## Result

The four books have now been inventoried through their final chapters, worked examples and appendices. Their important differences are not a few extra interpretive keywords. They change which name counts, what a consonant sum means, how intermediate numbers are reduced, when years change, how letters progress through a life, and how relationship claims are constructed.

The resulting separate systems are **CAMPBELL_YOUR_DAYS_V1**, **JORDAN_ROMANCE_NAME_V1**, **JAVANE_BUNKER_DIVINE_TRIANGLE_V1**, and an additive **CHEIRO_CHALDEAN_V2**. CHEIRO_CHALDEAN_V1 and DECOZ_CURRENT_V1 are preserved unchanged. No hybrid or average is introduced.

A source inventory can be complete while its author leaves some operations ambiguous. Those branches are part of the frozen specification. They are not a reserve of rules to choose after seeing an outcome. The specifications are historical-source models, not validated causal descriptions or recommendations.

## 1. Exact supplied editions and coverage

| Source | Actual inspected identity | Complete coverage and limitation |
|---|---|---|
| Cheiro, *When Were You Born?* | Kessinger reprint scan; attachment identifies2005/ISBN9780766193727. Interior confirms title/author but does not independently date the reprint. Internet Archive digitization notice2022 |140 PDF pages; body1–122, fifteen chapters, five affinity plates, monthly descriptions, colours/stones and back matter. Printed page+12=PDF page |
| Florence Campbell, *Your Days Are Numbered* |23rd printing1985; copyright1931, renewal1958; ISBN0875164226 |260 OCR-text leaves in ZIP; body1–246 including the final astrology addendum. **No page images**, so typographic/layout uncertainties cannot be visually certified. Printed page+12=leaf |
| Juno Jordan, *Numerology: The Romance in Your Name* |**Eleventh printing2003**, not the1978 date in the upload filename; copyright1965, transfer1988; ISBN0875162274 |388 PDF pages; all24 chapters and autobiography. Body1–347 and349–362; printed page+20=PDF page. The autobiography itself mentions1979 |
| Javane & Bunker, *Numerology and the Divine Triangle* |EPUB metadata2020-07-06; textcopyright1979, illustrations1980; printISBN9780914918103, EPUBISBN9781507301159 |All26 spine documents, native page anchorsi–viii/1–266, calculation diagrams, full example tables, every1–78 personal and temporary entry, Appendix and bibliography |

Input hashes and chapter-by-chapter coverage are recorded in `source_coverage.json`. Source pixels were used for calculation diagrams and tables where available. Raw books and full transcripts are not redistributed in this public repository.

## 2. What was genuinely new

### Cheiro: a real relationship-method addition, not another year clock

*When Were You Born?* distinguishes **mental/numerical sympathy** from **physical birth-period affinity**. It supplies four elemental triangles, a specific central/opposite affinity for each period, mixed-element rules, and monthly exceptions. Same birth-number sympathy alone is not its full romantic-affinity claim. Its fixed period dates and unweighted seven-day cusp language must not be replaced by modern solar-longitude calculations. Its chapter headed February covers January21–February18; a month-heading shortcut is wrong.

This justifies CHEIRO_CHALDEAN_V2 as an explicit addition. It does **not** alter V1's name table, componentwise compounds, contextual public/private name rule, or year-plus-digit-sum periodicity. The source also does not provide a new Personal Year, name-change waiting period or marriage-date probability. Provenance: Cheiro pp.1–97 and98–108; full delta C2-01–C2-15.

### Campbell: different constructs, unusual letters and a late astrology layer

Campbell's **Quiescent Self** is the privately imagined self at rest, expressly not outward Personality. Impression is a separate, not uniquely calculable construct. Her Expression is Ability, while Destiny is the date-derived Life Path. These labels cannot be mapped mechanically to Jordan or Decoz.

Her literal table gives **K11/V22**, while compact examples and Inclusion use their2/4 roots; transit durations explicitly remain2/4 years. The master-reduction tensions are retained as branches. She also has an unusual Ruling Passion calculation: subtract2 from the frequency of5 before finding the maximum. Her Planes classify individual letters, not Jordan's numeric groups.

Her three life Cycles turn near the1 Personal Year nearest or following ages28/56, with a progressed-Moon rationale; that is not Decoz's Period-Cycle duration formula. Her Personal Year is calendar-based with multiple onset/overlap qualifications. Matching Essence and Personal Year can be an **overload warning**, not automatically corroborating good fortune.

The final page adds specific astrology-to-number-position correspondences, including Soul–Moon, Expression–Ascendant and Path–Sun. That is a real qualitative hybrid layer, but supplies no quantitative fusion algorithm. Provenance: Campbell pp.16–17,27–42,136–178,179–207,231–246; full spec C01–C38.

### Jordan: different master arithmetic, Planes and intraday timing

Jordan **reduces11 and22**, retaining their qualitative background rather than treating them as arithmetic stopping points. She counts **only AEIOU as vowels**: Y and W stay consonants regardless of pronunciation. Her Planes use numeric classes, followed by a separate plane-count interpretation layer, including zero and raw-count refinements.

She includes Balance of Force, intervals among major positions, four Challenges, the Habit Challenge/Point of Security, all birth-name components progressing concurrently, and a Race Consciousness age layer. Her day method goes beyond Personal Day: it divides the day into **three eight-hour periods** using date-derived Pinnacles and Challenges. This is nominal timing resolution, not evidence of accuracy at that resolution.

Her birth-name permanence is clear, but a changed name can channel existing ability. Legalization is not the symbolic trigger, and no numerical activation lag is stated. Several printed timing examples have incompatible age/display conventions; they are not quietly repaired. Provenance: Jordan pp.7–8,63–75,110,145–203,207–297,312–337; full spec J01–J33 plus reconciliation J-A18.

### Javane/Bunker: two alphabets and an entirely different life-timing mechanism

Core names use cyclic1–9 values and **straight full-name sums**. The Divine Triangle instead uses **unreduced alphabetical positions A1–Z26**, first/middle names only, sequentially, with **nine years per letter regardless of its value**. Surnames enter the natal core but not that letter sequence. This is not another implementation of simultaneous Transit/Essence tapes.

The Life Lesson adds the actual month, actual day and one digit-sum of the year. Masters include **11,22,33,44**. Personal Years run **birthday-to-birthday**, subdivided into three four-month periods. A minor Personal Month layer is supplied; a Personal Day formula is not.

The Triangle has27-year stages, explicit major/minor experience-age formulas, and an alert-after81 continuation using21-year lines. It generates72 labelled experience entries in the first81 years, **not72 distinct events or independent predictions**. The source supplies all78 personal and78 temporary interpretations and45 Life-Lesson-root pair descriptions. A remaining missing digit can be supplied by a core number, Power Number or actual adopted-name vibration; this differs from fixed natal-deficiency accounts. Provenance: Javane/Bunker pp.14–108,120–264; full spec JB01–JB19.

## 3. Cross-system comparison matrix

The Decoz column is the unchanged2026-10-03 project snapshot, not a claim to have re-audited a new Decoz book. The Cheiro column distinguishes inherited V1 and the present V2 additions.

| Dimension | Cheiro V1/V2 | Decoz current V1 | Campbell V1 | Jordan V1 | Javane/Bunker V1 |
|---|---|---|---|---|---|
| Birth name |Not an immutable dominant Name Number in V1; actual context matters |Full birth name remains core |Full birth name remains natal basis |Full birth name remains original pattern |Full birth name remains core/Destiny |
| Current/use name |Primary Name Number for the relevant public/private/trade context |Minor Expression/Heart/Personality and current-name Planes |External development/opportunity angle, nickname context |Vehicle for existing capabilities; signature/nickname context |Some modification; can supply missing vibration |
| Legal name |Relevant only through actual name context |Not automatically the everyday introduction name |Legal act not a specified switch |Legalization generally unnecessary for symbolic effect |No independent legal-trigger formula |
| Claimed name-change magnitude |Meaningful active-name change; exact effect/lag not quantified |Minor relative to core **does not mean negligible**; genuine adopted change claimed meaningful |Potentially large external change; natal basis persists |Potentially useful opportunity, not creation of absent talent |Limited/changeable expression overlay; natal Destiny persists |
| Claimed activation time |No new WWYB lag |Inherited gradual6months–2years/self-identification claim |Better part of a year; not a precise day count |No fixed lag supplied |No fixed lag supplied |
| Letter mapping |Chaldean1–8, no9letters |Cyclic1–9 |Cyclic positions with literalK11/V22 and compact alternatives |Cyclic1–9 |Cyclic1–9core; ordinal1–26Triangle |
| Vowels/Y/W |No vowel/consonant core subdivision |Ycontext-dependent;Wconsonant |Yphonetic;Wafter another vowel in one sound |AEIOUonly;Y/Wconsonants |Yparticular sound/syllable rules;WafterD/Gexamples |
| Reduction/compounds |Part roots combined; distinct10–52meanings |Componentwise; retain generating doubles |Componentwise; master-intermediate branches |Componentwise, **always reduce**, preserve full chain |Straight name sums;1–78bank; totals>78digit-summed |
| Masters / special numbers |No Western master arithmetic;4/8exceptions |11/22/33;13/14/16/19debts;powerdigitsseparate |11/22;13/14/16/19TestingNumbers |11/22qualitative roots2/4;16/19special |11/22/33/44; compound-specific karmic statements, not one imported closed list |
| Core hierarchy |Birth day primary for everyday/material matters; name, period, year separate |Life Path highest single core; Expression, Heart, Personality, Birthday |Soul/Ability/Path functional triad; Birthday modifier; Quiescent separate |Destiny/BirthForce/Heart/Personality/Reality, then refinements |LifeLesson/Soul/Outer/Destiny; LifeLesson leads career/compatibility; Power later |
| Forecasting layers |Lucky-date/compound-date methods, ages/ordinalyears, recurrence;V2physicalaffinity |Periods/Pinnacles/Challenges, three role-transits, Essence, PY/PM/PD, Duality, AgeDigit |Cycles/Pinnacles/threeChallenges, each birth-component tape, Essence, universal/personal calendar layers |Pinnacles/fourChallenges, each birth-component tape, Essence, calendar layers, RC, intraday |Triangle stages/letters/major-minor ages, birthdayPY, four-month periods, PM; no importedEssence/Pinnacles |
| Annual boundary |No commonPYclock |CalendarPY; birthdayTransits/Essence |CalendarPY with explicit overlap/lag qualifications; birthdaylettertapes |CalendarPY; birthdaylettertapes with printed indexing conflicts |BirthdayPY; calendar-month refinement can straddle birthday |
| Relationships |Number harmony;V2mental+physical triangles/opposites/exceptions |Whole core profile, cycles, relationship forecasts |Soul-first, elements/parity, differentExpressions; cycles/lacks; business rules differ |Whole core/cross-position comparison, Planes/traits/alltiming |45LifeLesson-root pair entries; individual temporary marriage/partnership layers |
| Finest nominal timing |Day selection and age/yearrecurrence |Personal Day |Personal Day |Eight-hour blocks |Month minor; four-month periods and agepoints |
| Spiritual/occult integration |Planet numbers, birth periods, affinities, occult compounds |Inherited symbolic/karmic framework |Reincarnation, vowel/numberplanets, Tarot motifs, late qualitativeastrology |Divine purpose, reincarnation,16Tower; no fullastrologicalengine |Full1–78Tarot/astrology synthesis and geometric/theologicalframework |
| Source completeness |Book of Numbers inherited; supplied WWYB fully inventoried |Inherited framework/inventory; not newly source-completed here |Full provided text includingp246; nofacsimile; explicitly incomplete letter-combinationknowledge |Full supplied book/autobiography; conflicting timingexamplespreserved |Full EPUB, allpersonal/temporarybanks,Appendix and diagrams |
| Unresolved issues |Cusps, differingdate/friendlists, mentalharmony scope |Exact full interpretive banks/operational weights not supplied by this audit |K/V/master arithmetic, cycles/endpoints, lack/excess interpretation,OCRlimits |Ageindexing/endpoints, intermediatecompoundpriority, thresholds/conditionalclaims |Vowel/edge-date rules, anticipation/masteractivation,22/77correspondences, after81branch |

## 4. Incompatible outputs — do not average

**Arithmetic and timing disagreements can be demonstrated without inspecting anyone's history.** A second distinction is necessary: different constructs are not automatically contradictory claims about the same target.

| Contrast | Reproducible difference | Consequence |
|---|---|---|
| Same spelling with Y/W |Jordan excludes both from Heart; Campbell and Javane/Bunker admit different conditional uses |Soul/Heart and consonant totals can differ for the same name; fix pronunciation first |
| Same compound44 |Jordan/Cheiro reduce8; Campbell reduces8; Javane/Bunker retains44; Decoz's frozen44is not a master |Different special-status predictions, not a consensus “master44” |
| Campbell's own K/V branches |KIRK gives literal40/4 versus compact22 |Even within one book, the final-master status is unresolved; preserve both branches |
| Same full-name input |Jordan/Freda Mary Norton uses7+3+6=16/7; straight-sum arithmetic retains79 before the JB>78rule |Different compound histories despite sometimes equal final roots |
| Same birthdate11/12/1940 |JB LifeLesson11+12+14=37/1; Jordan BirthForce2+3+5=10/1 |Equal root does not establish equal method or equal compound interpretation |
| Same target day before a late-year birthday |Calendar-year methods have changedPY inJanuary; JB still uses the preceding birthday year |Conflicting current-year interpretations for much of the civil year |
| Same person's name-based age |Concurrent full-name tapes versus sequential given-name-only nine-year lines |Different active letters, compounds and predicted transition ages |
| Compound43 when generated in the relevant layer |Cheiro's43is an upheaval/failure warning; JB43/7ThreeCups emphasizes abundance/celebration |Opposing source expectations; do not choose the author after the outcome |
| Remaining missing digit |JB permits Power/core/name compensation; Campbell preserves the natal weak link despite mitigation |Different assertions about a currently missing/compensated quality |
| Within one JB system |General9warns against new starts, but27/9AceWands explicitly favours births/marriages/business starts |A root-only forecast is not the full author model; retain specificcompoundcontext |

**Do not mislabel adjacent differences as logical contradictions.** Campbell's private Quiescent Self versus Jordan's public Personality measures different proposed constructs. Campbell's Essence=PY overload warning is not the negation of every favourable major-number echo in Jordan. Jordan's within-chart3-to6interval strain and Cheiro's general3/6/9harmony operate in different relation types. Cheiro's birth-period elements and Campbell's number-derived elements have different inputs. Their matching principles differ, but a direct pair-level disagreement requires applying both complete methods to the same frozen inputs.

## 5. Earlier assumptions that need correction

“Pythagorean numerology” is not one stable algorithm. Decoz was an implementation choice, not a universal rule. The other three authors cannot be imported into DECOZ_CURRENT_V1 simply because their vocabulary overlaps.

The earlier suggestion that Cheiro's missing book would only add descriptive richness was too narrow for **relationship analysis**: it supplies a distinct mental/physical affinity method. It does not add another year-periodicity formula.

“Current-name influence is Minor” is a hierarchy statement, not proof that an author claims little practical effect. Conversely, legal registration alone does not make a name the active current-use input.

Raw totals53/90 should not be called Cheiro's combined compounds for the previously discussed name variants. The already-corrected component-root method remains authoritative. **2008 is moderately consequential, not top-major.**2018remainsmajor and2029prospective. The old retrodiction's UNKNOWN2008 sentence is stale; its descriptive background-year tally must not be rebranded a specificity estimate. No new fit or significance calculation was performed here.

This audit's own errors were also corrected: the JB Sagittarius wheel was initially misread and is **not** inconsistent; a Jordan consonant trace is19→10→1, not raw10; two Elizabeth tape fixtures initially miscopied the finalletter. `SOURCE_RECONCILIATION.md` has precedence over those exact candidate-spec statements. An audit must not preserve a false criticism simply because it was already written.

## 6. Reproducibility, freeze and what remains missing

The arithmetic reference and tests reproduce75 source/synthetic branch fixtures plus all68rows of the Cayce annual/four-month table, **272 numerical entries**.23test methods pass. That is engineering/source arithmetic evidence, not evidence that the books predict human events. Expected source constants were recorded separately from the calculation functions. There was no untouched participant test, no independent predictive score and no owner-history optimization.

The freeze binds four per-system specifications, their reconciliation, the ambiguity registry, source coverage, arithmetic reference, fixtures, comparison and method registry. It freezes the author-specific rules **and the set of unresolved alternatives**. A later experiment must choose or propagate those alternatives before outcomes. It cannot silently add omitted interpretations to rescue a miss.

Remaining limitations are specific:

- Campbell's supplied source lacks original page images; a facsimile could settle OCR/layout doubts, but must create a logged source correction rather than an unversioned rule.
- Some books genuinely omit normalization details, decision weights, exact onset conventions and selectors for positive/adverse manifestations. Campbell explicitly says the event-letter interpretation is incomplete. Another general book cannot fill these gaps while retaining this system ID.
- Decoz remains the inherited frozen framework. This four-book audit does not supply its complete81Duality interpretation bank or all operational relationship mappings. A full Decoz empirical arm must freeze the exact official implementation/interpretation resources it uses; a Personal-Year-only substitute is not admitted.
- Cross-family check: **not run** because the authorized remote Claude route was platform-blocked. Source checks and arithmetic tests are reported, not relabelled independent model review. No high-stakes personal recommendation or empirical-superiority claim is made.

## 7. Consequence for future owner analysis

Yes, these books materially change **how a fair analysis should be constructed**. They require separate author-specific charts, complete relevant timing layers, explicit name roles and pronunciation masks, and source-branch flags. CheiroV2 changes the relationship-method scope; Campbell/Jordan/JB add genuinely different competing models. They do not establish which is more accurate for the owner, and they do not retrospectively validate an attractive match.

The next document, `EMPIRICAL_COMPARISON_DESIGN.md`, is authored only after the source freeze. It describes a full-system, cross-person/prospective comparison with independently rated targets, observed negative periods, equal attention to false alarms and misses, and no rule creep. It is a design, not a launched trial or a result.

### Reading map

`numerology_method_registry_v2_20261004.json` is the machine entry point. The four named per-system Markdown files contain the full page-level formulas, all major interpretation-bank inventories and author-specific caveats. `SOURCE_RECONCILIATION.md` controls the few corrected statements. `ambiguities.json` and `source_coverage.json` distinguish inventoried uncertainty from missing source. `freeze_manifest.json` supplies exact identities. `formula_fixtures.json`, the Python reference and tests provide reproducible arithmetic. `independent_review.md` states the actual review boundary.
