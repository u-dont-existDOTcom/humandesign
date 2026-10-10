# Independent source findings: Lilly, Book II, XXVIII

Status: source-only candidate supplied to the supervising reader for reconciliation. No HumanDesign repository files were edited. No participant records, model files or outcome collections were accessed. The source is the 894-page Wellcome witness already supplied by the parent, SHA256 `2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b`.

## What was actually read

I inspected original WHOLE-PAGE images for PDF211 through PDF222, each rendered at scale1.5, and inspected an additional scale3 whole-page image of PDF211 for the chart. Existing page text211–222 was used alongside the images. No crop, new OCR, modern ephemeris reconstruction, or predictive test was performed. Reading PDF222 established the next chapter boundary; it did not extract XXIX rules.

Literal printed folios observed: PDF211177;212178;213179;214180;215181;216182;217183;218184;219185;220186;221187;222188. The last digit on PDF216 is worn but visually reads2; its OCR186 reading is false. PDF214's folio is damaged but reads180. These are visual readings, not an unverified assumption that every source page equalsPDF−34.

## Exact section boundary

The tradesman prelude and chart are on PDF211/printed177, before the literal chapter heading. **CHAP. XXVIII. If the Querent shall be Rich or Poore.** begins PDF212/printed178. Its concluding text finishes on PDF221/printed187 with the cross-reference “see page71.” A horizontal rule then introduces **Of the third House, viz. Of Brethren, Sisters, Kindred, short Journeys.** A full third-house preamble follows on that same page. The literal XXIX heading begins PDF222/printed188.

The next unread source point is therefore **PDF221, below the rule, third-house heading and preamble**, followed by XXIX onPDF222. Counting all ofPDF221 as second-house material would silently absorb or skip the third-house preamble.

## Chapter architecture and rule inventory

The54 local candidate records are in `XXVIII_CANDIDATE_RULES.json`; its `C` IDs are placeholders for root assignment. Its structure follows the prior batch's record shape while adding precise passage boundaries, observed folios and optional worked values.

| Source pages | Function | Candidate coverage |
|---|---|---|
|211|Case prelude, four questions and chart|Retrospective context; printed date/time,12 cusps,7 planets, Fortune, nodes|
|212|Motion examination, dignity-table method, Saturn tally|All7 motion rows; source cross-references; Saturn6−14=−8|
|213|Jupiter, Mars, Sun and Venus tallies|Each component and total; unscored Jupiter–Mars square qualification|
|214|Mercury, Moon and Fortune; net summary|18−5=13;12−7=5; Fortune3−5=−2; beyond-five-degree cusp attribution|
|215|Net-score instruction; antiscia; first wealth reasoning|All7 antiscia/contra pairs; whole-figure and wealth conditions|
|216|Wealth conclusion, marriage qualification and means|Ordered lunar transfer; Fortune terms; labor/ease qualification; turned eighth|
|217–218 top|Informant confirmation and timing|Reported wife money/land and trade; two timing routes; friend help; reason/art qualification|
|218–220|General hindrance/perfection insertion|Malefic chains, reception exceptions, beneficial interruption, translation/collection and direction|
|220–221 top|Persistence, antiscia cautions, friends|Explicit competence definition; Saturn contra-antiscion; historical caution about solar men|

## Chart and numeric readings pinned to the original

The chart center reads **16.Iuly1634,11H0A.M.** Mercury is the day-lord glyph and the Sun the hour glyph. No Gregorian/Julian or UTC conversion is attempted. The compact final central aspect shorthand remains unpromoted because some symbols are not securely resolved.

|Body/point|Printed longitude|
|---|---|
|Saturn|Sagittarius15°19′, retrograde|
|Jupiter|Cancer17°31′|
|Mars|Libra16°12′|
|Sun|Leo3°10′|
|Venus|Leo25°34′|
|Mercury|Leo17°45′|
|Moon|Leo19°07′|
|Fortune|Scorpio0°10′|
|North node|Virgo22°12′|
|South node|Pisces22°12′|

Cusps1–12: Libra14°13′;Scorpio6°35′;Sagittarius7°12′;Capricorn19°00′;Aquarius26°35′;Pisces23°09′;Aries14°13′;Taurus6°35′;Gemini7°12′;Cancer19°00′;Leo26°35′;Virgo23°09′.

PDF212 diurnal motions: Saturn2′ slow;Jupiter13′ swift, compared with4′59″ mean;Mars35′ swift, compared with31′27″ mean;Sun57′00″ slow;Venus1°13′ very swift;Mercury1°44′ more swift;Moon11°54′ slow. The Saturn entry is an unsigned daily-motion magnitude with a separate retrograde status.

The net strength totals onPDF214 agree arithmetically with the listed components: Saturn−8,Jupiter+20,Mars+9,Sun+8,Venus+18,Mercury+13,Moon+5,Fortune−2. Component rows are retained inJSON. The source does not debit Jupiter's platick Mars square numerically.

Antiscia/contra-antiscia,PDF215: Saturn14°41′Capricorn/Cancer;Jupiter12°29′Gemini/Sagittarius;Mars13°48′Pisces/Virgo;Sun26°50′Taurus/Scorpio;Venus4°26′Taurus/Scorpio;Mercury12°15′Taurus/Scorpio;Moon10°53′Taurus/Scorpio.

The chart numbers support these bounded differences, for the root's calculation reconciliation: Mars−Ascendant1°59′;Venus−Moon6°27′;second cusp−Fortune6°25′;eleventh cusp−Venus1°01′;Jupiter−Saturn contra-antiscion2°50′. These differences do not by themselves establish the author's timing scale, an astronomical ephemeris, or predictive accuracy.

## Important OCR repairs

1. **PDF216 and217: Mercury, not Jupiter.** The Moon separates from a sextile ofMars, then conjunction ofMercury, and applies to conjunction ofVenus; the transferred virtues areMercury andMars. Their exact printed longitudes also fit the stated order. Jupiter is a separate testimony.
2. **PDF216: Fortune, not Venus**, is in a fixed sign and Mars's terms. Venus inLeo is not the referent of that terms clause.
3. **PDF212: Mars35′**, not38′. Its stated mean is31′27″. Jupiter's mean is4′59″, not the OCR4′57″.
4. **PDF211:16July**, not6July. Figure second cusp isScorpio6°35′, and Fortune isScorpio0°10′.
5. **PDF217 folio183**, not185; **PDF216 folio182**, not186. Word and glyph damage must not be treated as genuine author errors.
6. **PDF219 abscission clause: perfect conjunction** with an evil planet; the geometry matters to the stated interruption.

## Contradictions, qualifications and unresolved formalization

### A clear source counting discrepancy

PDF217 explicitly says **five** planets are swift. PDF212 identifies onlyJupiter,Mars,Venus andMercury as swift;Saturn,Sun andMoon are slow. Preserve the five claim and the four-row count separately. There is no image support for silently repairing either statement.

### An explicit cusp exception

PDF214 knowingly assignsFortune to the second even though it is more than five degrees from that cusp. The chart yields6°25′. This defeats an unqualified claim that Lilly always uses a strict5° cutoff here. The passage calls first-house signification absurd but gives no general replacement threshold. It is a recorded case decision, not permission to invent a6°25′ universal orb.

### Reception syntax that remains unresolved

PDF219's paragraph starts **“If the Planet who receives the Lord of the Ascendant”** and later says the planet, if free from misfortunes, is **“neither receiving or received”**, yet perfects easily. The original page contains both expressions. They might use “receives” in distinct contact/reception senses, but that is an interpretation; do not silently emend the source or export this as a fully specified machine predicate.

The following paragraph, beginning **“If the Planet to whom the Lord of the Ascendant”**, omits a syntactically expected joined/contact verb. Its chain reading is recoverable in context but should remain editor-normalized and provisional. EarlierPDF218 pronouns in the nested ill-disposed-Infortune route likewise need a declared relation mapping rather than hidden assumptions.

### The ordered reception and obstruction qualifications

Do not reducePDF218–220 to either “reception always saves” or “malefics always prevent.” The insertion requires all of these distinctions:

- An ill-disposed evil contact without reception prevents the matter, including a chain through another planet.
- Reception can rescue an unfortunate retrograde, combust or cadent contact, with weariness and solicitation; no reception gives failure.
- An unimpeded intermediary connected to a benefic still fails when the benefic contacts an impedited malefic that does not receive the relevant prior planet.
- Interception **before the harmful conjunction** may remove the malefic harm and permit completion. This is contextually different from an Abscissor that destroys a useful perfection.
- Hard-aspect reception with ill disposition profits nothing, and still less if the received planet is impedited.
- Sextile/trine reception favors success; a well-disposed receiver can succeed by any aspect, including square/opposition.
- Applying sextile/trine may succeed without reception. Separation is explicitly excluded.
- Joining an unimpeded Fortune perfects.
- Translation to an impedited Infortune fails unless that Infortune is again received; the sentence leaves the next receiving agent unspecified.
- A collector that is an Infortune **or** unfortunate must receive **both** significators; reception of only one is insufficient.
- Querent significator entering the thing's house or conjunction with its lord indicates the querent going toward the thing. The inverse placement/application indicates the thing coming to the querent, with the Moon/other-aspect reservation retained. Direction is not an unconditional guarantee of success.

### Other source distinctions, not forced contradictions

- Jupiter has no numeric debit in the tally but its platickMars square is qualitatively harmful. LaterSaturn contra-antiscion affliction is another testimony. “Strong” and “wholly untroubled” are not interchangeable.
- The first synthesis says no violent affliction. A platick square described as some detriment need not logically contradict that narrower statement.
- Fortune is numerically weak yet has fixed-sign/Mars-term testimony. Do not discard either consideration or invent a new combined score.
- Mars promises acquisition through its office while remaining a peregrine Infortune that brings care and obstruction. Own industry, relative ease compared with expectation, and remaining labor can all coexist.
- “No planet in the second” does not excludeFortune, which is a calculated point.
- Antiscia are little used because none meets an exact material cusp/planet, yet the author uses a **near contra-antiscion**. These are different categories, and no universal exact or near cutoff follows.
- Venus near the eleventh brings helpful friends; solar men are specifically cautioned against because of theSun's aspect toFortune/second cusp. The latter is not a retraction about every friend.
- The concluding paragraph says “two things” without an unambiguous enumerated pair. Do not manufacture two observed confirmations from it.

## Actual case confirmation scope

PDF211 says Lilly has seen experience of his judgment: an author-level retrospective assurance. PDF216 says the man has acquired an estate/competent fortune with labor and care “to the day hereof.” PDF217 explicitly says the man reports wife-derived **money and land**, and says the trading has been very good. The Ascendant–Mars passage also states he had a portion with his wife around the two-year interval.

The later **about1640** trade/reputation/friends cluster is stated as Lilly's earlier judgment, without an equally specific separately documented1640 result in this scoped chapter. The second-cusp/fixed-sign paragraph predicts durable competence and explains rich as not falling into poverty; it supplies no full-life observation. The kin, servant, and solar-friend passages are judgments/cautions, not explicit outcome confirmations.

Every reported confirmation remains one selected historical case, transmitted by the author and sometimes explicitly by the subject through the author. It is neither untouched validation nor independent evidence for every extracted rule. The separate statement callingJupiter in the tenth certain and infallible is Lilly's general claim, not an empirical certification.

## Handoff files

- `XXVIII_CANDIDATE_RULES.json`:54 normalized records, precise page and passage anchors, local candidate IDs.
- `XXVIII_NUMERIC_TABLES.json`:chart, motion table, all planetary score components, antiscia pairs.
- `READING_RECEIPT.json`:actual viewed pages, source hash, rendering method, scope and evidence limits.
- Whole-page images `p211.png` through `p222.png` and `p211-high.png`:scratch reading aids, not publication payloads.

The parent owns integration, canonical numbering, numeric reference checks, final independent claim reconciliation and publication. These files freeze this source reader's findings without changing any old batch.
