# CHEIRO_CHALDEAN_V2 — source specification and explicit V1 delta

Status: SOURCE-AUDITED CANDIDATE; not frozen until the common freeze manifest is issued. Scope: the supplied *When Were You Born?* plus unchanged CHEIRO_CHALDEAN_V1. This is a historical author's model, not an empirically established causal account or personal advice.

## Source identity and coverage

Cheiro, *When Were You Born? Your Future, Marriage, Character, Tendencies Clearly Shown and Described*. The supplied Kessinger Rare Reprints scan has 140 PDF pages. Body pagination is 1–122; PDF page = printed page + 12. Front matter is PDF 1–12; post-body material is PDF 135–140. Title/author are visible on PDF 3; Kessinger branding and ISBN barcode are on PDF 140. Attachment metadata identifies Whitefish, 2005, ISBN 9780766193727, but the inspected interior does not independently date that reprint; preserve the distinction. Internet Archive digitization notice says 2022 (PDF 2). Input SHA-256: `5044709ef15aebaa8f48db8d6d18a3eecd5e9eb8342007137c41d88664a6de12`.

All fifteen chapters, preface, five affinity diagrams, colour subsections, and back matter were inventoried. Plates I–V were visually checked; OCR is not authoritative for diagram labels. There is no name-calculation chapter, letter table, Tarot system, calendar Personal Year formula, or new year-recurrence generator in this supplied book. Its material addition is the explicit relationship/period interpretation layer, not a replacement arithmetic system.

| Chapter | Printed pages | Contents and disposition |
|---|---:|---|
| I January | 1–7 | Capricorn-period character, friendships, health, colours/stones; birthday notebook leaves |
| II February | 8–15 | Aquarius-period equivalent |
| III March | 16–22 | Pisces-period equivalent |
| IV April | 23–29 | Aries-period equivalent |
| V May | 30–36 | Taurus-period equivalent |
| VI June | 37–44 | Gemini-period equivalent |
| VII July | 45–51 | Cancer-period equivalent |
| VIII August | 52–58 | Leo-period equivalent; extra Number-1 friendship statement |
| IX September | 59–65 | Virgo-period equivalent |
| X October | 66–72 | Libra-period equivalent |
| XI November | 73–82 | Scorpio-period equivalent; qualitative age-development distinction |
| XII December | 83–92 | Sagittarius-period equivalent |
| XIII Numbers and birth dates | 93–97 | Digital roots, planet correspondences, mental versus physical sympathy |
| XIV Life's Triangles and Affinities | 98–108 | Four elements, same-element affinities, central/opposite affinities, mixed-element claims |
| XV Lucky colours | 109–122 | Root-specific colour/stone rules, nonidentical period windows, claims and exclusions |

## Immutable inheritance and delta boundary

CHEIRO_CHALDEAN_V1 remains exactly the 2026-10-03 registry and audit. Its birth-day priority, separate zodiac-period and birth-year layers, contextual use-name, componentwise name reduction, compounds, action-date method, periodicity and age/ordinal-year branches are inherited, not recalculated from another author.

New rule IDs C2-01 through C2-15 below are additive. They must not be used to repair a miss attributed to V1. In particular, the new physical-affinity method cannot be retroactively presented as an old number-only prediction.

## Reproducible rules

### C2-01 — Fixed birth-period lookup and heading trap [pp. 1, 8, 16, 23, 30, 37, 45, 52, 59, 66, 73, 83]

Classify by the explicit month/day interval, **not the chapter's month heading**. January 29 belongs to chapter II, headed February. This is a fixed civil-calendar lookup, not a modern ephemeris calculation of solar longitude; year, clock time and birthplace are not inputs to it.

| Period ID | Interval inclusive | Element | Central affinity |
|---|---|---|---|
| Capricorn | Dec 21–Jan 20 | Earth | Cancer |
| Aquarius | Jan 21–Feb 18 | Air | Leo |
| Pisces | Feb 19–Mar 20 | Water | Virgo |
| Aries | Mar 21–Apr 19 | Fire | Libra |
| Taurus | Apr 20–May 20 | Earth | Scorpio |
| Gemini | May 21–Jun 20 | Air | Sagittarius |
| Cancer | Jun 21–Jul 20 | Water | Capricorn |
| Leo | Jul 21–Aug 20 | Fire | Aquarius |
| Virgo | Aug 21–Sep 20 | Earth | Pisces |
| Libra | Sep 21–Oct 20 | Air | Aries |
| Scorpio | Oct 21–Nov 20 | Water | Taurus |
| Sagittarius | Nov 21–Dec 20 | Fire | Gemini |

### C2-02 — Seven-day boundary mixing [pp. 1, 5 and repeated birthday-notebook introductions]

The sign takes seven days to come to full strength and seven days at its close to decline; people in the transition participate in the preceding and commencing qualities. No weights, exact seven-day inclusivity convention, or algorithm for mixed compatibility is supplied. Store the nominal period and a boundary-ambiguity flag; preserve competing preceding/following-period interpretations without selecting the better fit. Do not turn this into a fourteen-day ephemeris cusp.

### C2-03 — Root and planetary correspondence [pp. 94–95]

`r(n)` repeatedly sums decimal digits until 1–9. For this chapter 11→2, with no master-number exception. Planet table: 1 Sun, 2 Moon, 3 Jupiter, 4 Uranus, 5 Mercury, 6 Venus, 7 Neptune, 8 Saturn, 9 Mars. The Sun's paired series is 1/4; the Moon's is 2/7. The mention of only nine basic numbers is about this root calculation; it does not silently repeal V1's separately sourced compound interpretations.

### C2-04 — Mental/numerical affinity [pp. 95–98]

For birth days `d1,d2`, set `a=r(d1), b=r(d2)`. The local rule is `mental_affinity = (a==b) OR (a in {1,2,4,7} AND b in {1,2,4,7})`. The initial same-root rule is independent of birth month. These numerical sympathies are specifically described as more mental than physical.

The V1 Book-of-Numbers 3/6/9 harmony family is a distinct inherited predicate. This book says the other numbers attract their own class; it does not supply a 3/6/9 mental-affinity exception. Preserve two labelled outputs for those pairs; do not silently change the predicate or call the texts fully identical.

### C2-05 — Same-element physical affinity [pp. 98–108, Plates I–V]

Fire={Aries,Leo,Sagittarius}; Water={Cancer,Scorpio,Pisces}; Air={Gemini,Libra,Aquarius}; Earth={Taurus,Virgo,Capricorn}. Births in the same triangle are physical affinities. Same-period membership is included by the broad rule; some monthly friend lists omit repeating the person's own period. These four groups are not name-number or Tarot triangles.

### C2-06 — Central/opposite affinity [p. 102; Plates II–V, pp. 101,103,105,107]

Use the opposite-period mapping in the table above. A line from an apex to its opposite side marks that apex's central affinity. It is not permission to add all three midpoint periods to every apex. The author calls it ordinarily equally strong although opposite in character. Record `physical_relation` as SAME_ELEMENT, CENTRAL_OPPOSITE, OTHER_BLEND, or FIRE_WATER_CONFLICT, with source exceptions retained.

### C2-07 — Joint mental and physical claim [pp. 96, 102, 108]

Keep the two components separate, then `joint_affinity = mental_affinity AND (same_element OR central_opposite)` for the nominal-period branch. The author makes categorical permanence/reunion claims for true affinities, strengthened by sympathetic numbers. This is a source claim, not a validated probability or safety judgment. Numerical sympathy alone must not be reported as full romantic affinity; no percentage, rank weight or marriage date is supplied.

### C2-08 — Other element pairs and direction [pp. 106–108]

Air–Water, Air–Earth and Air–Fire are favourable blends but not true affinities under the general mixed-element passage; Air is said to dominate mentally. Earth–Water is a materially productive blend. Fire–Earth is described as warming/productive. Fire–Water is explicitly incompatible, with separation and possible hostility predicted. Central-opposite pairs are specific exceptions to the generic mixed-element/non-affinity wording; retain the specificity and the textual tension rather than calling every mixed pair adverse. Directional Air dominance is not a symmetric trait.

### C2-09 — Monthly prose exceptions [friend passages pp. 3,10–11,18,24–25,33,40,47,54,61,68–69,78,88]

Keep both the general triangle output and these explicit chapter lists. Most agree with own element + opposite. Exceptions needing separate fields: Capricorn's prose extends the Taurus range to **the end of May** (p. 3), rather than May 20; Aquarius's prose extends September 21–October 20 **as a rule to November 20** (pp. 10–11); Leo additionally favours people born on 1/10/19/28 in any month (p. 54). The Taurus chapter points to Plate IV although the Earth plate is V. A citation error is not a new triangle. No precedence or quantitative way to reconcile prose exceptions with the general rule is given.

### C2-10 — Period-specific personality and life-course catalogue [pp. 1–89]

Each entry below is a compact inventory of the chapter's distinct themes, not a standalone diagnosis. Every chapter contains favourable and adverse manifestations. There is no chart-derived classifier for a person's higher/lower expression; observing the outcome and then assigning a level is prohibited in prediction.

| Period | Distinct character/occupation themes | Relationship/life-course assertions | Pages |
|---|---|---|---:|
| Capricorn | Independent organisational leadership; plain/direct speech; intellectual and public-service orientation; misunderstood ideals; worry or discouragement | Broad charity rather than individual giving; warm feelings behind cold presentation; opposition through unpopular causes | 1–4 |
| Aquarius | Sensitivity and loneliness; intuitive character reading; debate; public activity; able to manage others and make money for them | Deep but undemonstrative loyalty or antipathy; crisis can bring abilities into use; adverse-expression unreliability is not predictable from period alone | 8–12 |
| Pisces | Absorptive understanding; historical/travel interests; insecurity about dependency; loyalty in trusted work; artistic talents need encouragement | Financial promises can retreat after reflection; brooding or self-undervaluing; no computed event dates | 16–19 |
| Aries | Will, organisation, independence, executive determination; resistance to criticism | Domestic difficulty from lack of understanding despite need for affection; no fixed marriage-failure age | 23–26 |
| Taurus | Endurance, memory/literary aptitude, hosting, business intuition, sensory/affectional responsiveness; stubbornness | Early first marriage warned against; jealousy and environmental influence; important choices alone advised by author | 30–33 |
| Gemini | Duality, quickness, wit, diplomacy, changing interests; actors/lawyers/speakers; sustained will needed | Inconstancy despite intense feeling; changing subjective truths; generic claim, not a timed affair forecast | 37–41 |
| Cancer | Home attachment plus restlessness, saving anxiety, effort/business over gambling, imagination | Multiple homes/domestic trouble; sensitive and encouragement-seeking; warns against young marriage because nature changes | 45–48 |
| Leo | Generosity, loyalty, pride, determination, leadership, inspiring others; unanticipated money | Easily deceived despite honesty; craves love, loneliness without purposeful work; extra Number-1 friendship rule | 52–55 |
| Virgo | Analysis, discrimination, memory, finishing others' projects, taste/order, deference to law/status | Author posits opposed moral/sexual manifestations without an a-priori classifier; unhappy domestic conditions linked to distress | 59–62 |
| Libra | Balancing, intuition alongside demand for proof, law/research/medicine; speculative financial swings | Exacting analysis of affection and domestic dissatisfaction; broad friendships | 66–69 |
| Scorpio | Intensity, emotional persuasion, writing/drama, crisis composure, adaptability, procrastination | Qualitative shift near twenty described; double-life/parallel-home tendencies, sexuality versus ambition; both saintly and adverse branches allowed | 73–79 |
| Sagittarius | Executive speed, candour, work, enterprise, music and law/order; two moral classes | Men described as impulsive in marriage, women as sacrificing/conventional; these sexed historical claims are not generalized beyond the text; no numerical timing | 83–89 |

### C2-11 — Colour/stone apparatus [monthly sections and pp. 109–120; disabled]

Birth-root principal/accent colours are separate from monthly colours. Root 1: yellow/orange/gold, with 2/7 green/cream/white interchange; topaz/amber. 2: light green/cream/white, light rose/pink/blue accents; pearl/cat's-eye/moonstone. 3: mauve/violet/purple; amethyst. 4: grey/fawn/electric shades, minor yellow/green; sapphire. 5: silver-grey/glittering white and light shades; silver/platinum/diamond. 6: blue with wide accents except black/dark purple; turquoise/emerald. 7: 2's colours somewhat stronger, green/yellow foundation; moonstone/white stones/cat's-eye, avoid dark. 8: dark/serious greys/blues/browns/russets; dark stones/deep sapphire. 9: crimson/red, rose/pink accents, blue also favourable; ruby/garnet/bloodstone.

The local strengthening windows are intentionally not substituted for C2-01: 1 Jul28–Aug22; 2 Jun25–Jul20; 3 Feb21–Mar21 and Nov21–Dec21; 4 Jul22–Aug22 and Jan22–Feb13; 5 May23–Jun23 and Aug23–Sep23; 6 Apr24–May24 and Sep24–Oct24; 7 Jun25–Jul25; 8 Dec26–Jan26 (positive) and Jan27–Feb18 (negative); 9 Mar27–Apr18 and Oct27–Nov18. The Jan22–Feb13 wording was checked on printed p.115; do not silently repair it to 18. The p.112 footnote combines a seven-day sign adjustment with the first matching 1-date; no general formula generating every listed window follows from that example.

Monthly stone/colour and health subsections exist in every period chapter at the page spans above. They are peripheral catalogues, not activated optimization or treatment modules. Their differences from root colours are preserved as two layers, not harmonized by picking a preferred colour.

### C2-12 — Health/material claims and exclusions [pp. 4,11–12,18–19,25–26,33,40–41,47–48,54–55,61–62,69,78–79,88–89;109–122]

Inventory: period-specific illness/body-part claims, food/climate/rest prescriptions, alleged colour/stone effects, vibration analogy, claims of personal verification, and spiritual/planetary explanation. All are disabled for medical, financial, relationship-safety or other high-stakes advice. Astral numbers/astral colours are explicitly outside this book's treatment (p.109). The book does not supply a diagnostic test or controlled evidence for its causal assertions.

### C2-13 — Names and normalization not supplied here [whole-source inventory]

This addition has no separate birth-name/current/legal/married/spiritual/nickname theory, vowel/consonant subdivision, Y/W phonetic rule, punctuation rule, title normalization, or name-change activation lag. Carry the V1 contextual-name policy only with V1 provenance. Do not fill these blanks from Campbell/Jordan/Javane–Bunker/Decoz. There is no evidence here for a numeric legal-name switch or a specific waiting period.

Inherited letter table: 1=AIJQY; 2=BKR; 3=CGLS; 4=DMT; 5=EHNX; 6=UVW; 7=OZ; 8=FP; 9 has no assigned letters. Inherited name arithmetic: sum each genuinely separate used name part; retain each part's compound; reduce each to 1–9; add the roots; retain this new compound when it is at least 10; reduce again. Whole-string sums are not interchangeable compound labels. A hyphen's tokenization must be declared; this new book supplies no rule resolving it. The V1 record, rather than *When Were You Born?*, is the provenance of these inherited rules.

### C2-14 — Timing and recurrence not supplied here [whole-source inventory]

The recurring yearly item is a person's birth-period interval; that is not a Personal Year or event forecast. The author discusses young marriage and a rough age-twenty development claim, but provides no precise age threshold except that qualitative example, no calendar/birthday cycle stack, and no new event-seeded periodicity formula. V1 recurrence stays unchanged and independently labelled. Full-year event probabilities cannot be inferred from this book's title, *Your Future*.

### C2-15 — Frozen ambiguity branches and no rescue

A01: nominal period versus unspecified seven-day blends. A02: Plate I's Aquarius endpoint looks Feb19 while chapter II/Plate IV state Feb18. A03: Capricorn Taurus-range extension to end-May. A04: Aquarius friendship range extension to Nov20. A05: specific opposite affinities versus generic other-element non-affinity wording. A06: WWYB same-root/1-2-4-7 mental affinity versus V1's additional general 3-6-9 harmony predicate. A07: chapter references to wrong plate numbers. A08: colour-period windows differ from character-period windows. A09: qualitative higher/lower character branches lack a prospective selection function. A10: no weights for joint versus single affinity, no numerical measure of name-change magnitude. A11: reprint year is attachment metadata, not an inspected copyright statement.

Return identified branch alternatives and source flags; do not average them. A later operational choice is a separately hashed experiment setting fixed before outcome inspection. The authorial method itself remains a multivalued specification where the source is unresolved.

## Reproducibility examples (not owner outcomes)

Birthdays 11 and 25 yield 2 and 7: mental affinity true. Days 3 and 6: WWYB mental-affinity predicate false; V1 general 3/6/9 harmony true. Apr 5 and Aug 5: same Fire element, same numerical root 5, joint affinity true. Apr 5 and Oct 5: central-opposite physical affinity plus same root, joint affinity true. Apr 5 and Jul 5: same root mentally, Fire–Water conflict physically; no joint affinity. Jan29 maps to Aquarius even though the chapter heading is February. None of these checks tests whether the asserted relationship effects occur in people.

## New versus unchanged

Genuinely new: reproducible mental/physical distinction, four elemental triangles, twelve central-opposite mappings, mixed-element/directional rules, explicit permanence claims, monthly exception inventory and period-specific character/relationship cautions. Unchanged: V1 name table, name compounds, public/private name roles, year periodicity, all Decoz rules. No owner-history fit was used to reconstruct this specification.
