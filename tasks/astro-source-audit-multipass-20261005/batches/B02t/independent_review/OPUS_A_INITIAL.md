## Coverage
- **Images read (8):** `source_images/pdf-353.png` through `pdf-359.png` (printed pp. 319–325) and `errata-888.png`. I read all of them before opening the JSON. `pdf-352`, `pdf-360` and `pdf-364` are not in `source_images`.
- **Candidate units checked: 70 of 70** (R2138–R2207; the file's `source_count` is 70).
- I did not open the `PART*_SOURCE_DRAFT.json` files the records point to, and I made no modifications.
- I couldn't check the PDF's SHA256 because the full PDF wasn't supplied. The hash in the records matches the one in your brief.
- Quotes below turn long-s into s; otherwise the spelling is as printed.
- **Severity:** MAJOR changes which configuration triggers a rule, or what it concludes. MODERATE adds or drops a printed alternative, qualifier, unit, scope note or passage. Both count as material. MINOR is wording or metadata drift.

## Material findings: 7 MAJOR (F01–F07), 15 MODERATE (F08–F22)

**F01 · MAJOR · WRONG_HOUSE · sure.** PDF359: "if they be found in the second, **fift** or eleventh houses". R2205 says "second, **sixth** or eleventh". *Repair:* change sixth to fifth.

**F02 · MAJOR · 8TH-FROM-MOON LOST · sure.** PDF356 reads "the Lord of the eighth house **from her**" and "…**from the Moon**". Only as a last resort does it say "take the signification from the Lord of the eighth house". R2163 and R2164 both say "eighth-house lord", so R2165's fallback ends up pointing at the same planet. R2164 also drops "or it shall dye very shortly". *Repair:* in R2163 and R2164, write "lord of the 8th from the ☽"; add "or will die very shortly" to R2164.

**F03 · MAJOR · SIGNIFICATOR DROPPED · sure.** PDF358: "**☽ Or** her Dispositor applying to the Lord of the eighth, **or eighth house from the ☽**, it is dead or will dye shortly".
- R2183 keeps only the dispositor and drops "8th from ☽".
- It renders "will dye shortly" as "near-death".
- It also applies the rule to a "missing thing", against its own note not to treat lost objects as creatures that can die.

*Repair:* restate the printed rule.

**F04 · MAJOR · FALLBACK ORDER · sure.** PDF356: "behold … the Lord of the second house … and if you find **of these two** no separation, say that the Beast is still in his place".
- R2161 says "still in place" based on the ☽'s lord alone.
- Its note says the Lord of the 2nd (L2) fallback comes "later", when the ☽'s lord "cannot be assessed".
- In the print, L2 is checked first, whenever the ☽'s lord shows neither separation.

*Repair:* make R2161 require that neither lord shows separation, and place it after R2162.

**F05 · MAJOR · OUTCOME MISASSIGNED · the omission is sure; which clause the "if" belongs to is uncertain.** PDF357: "honest man that **will** restore it againe; if ♃ or ♀ have any aspect to the ascendant, or ☽ apply to the ascendant; **☽ in the ascendant, it is restored with trouble or paine**".
- R2175 drops "☽ in the ascendant" and attaches trouble/pain to the ♃/♀ clause.
- R2174 has "may return … finder" instead of "will restore".
- p.320's parallel ("if that Fortune apply to the ascendant … faithfull person will restore") suggests the "if" clause belongs with R2174.

*Repair:* R2175 = "☽ in the Ascendant → restored with trouble or pain"; move the "if" clause into R2174 and flag it as ambiguous.

**F06 · MAJOR · CONFLATION, "and" FOR "or" · sure.** PDF354: "if the Lord of the house of the ☽ do behold ☽; but if you finde these Constellations contrary, judge the contrary; if the ☽ be fortunate by … Fortunes … would faine restore …; **or** if that Fortune apply to the ascendant … faithfull person **will** restore".
- R2143 moves the "Lord of ☽'s house beholds ☽" hope clause into the restorer rule.
- It joins Fortune and Ascendant with "and", losing the difference between "would faine" and "will" restore.
- The contrary clause has no record.

*Repair:* split into three records and add the contrary rule.

**F07 · MAJOR · WRONG SIGNIFICATOR, GLYPHS DROPPED · sure.** PDF354: "if the **Lord of the house of the Moon** be in humane Signes … Signes of small Beasts, **as ♈ and ♑** … Also, look to the ☽". R2145 gives the small-beast signs to the ☽ and omits ♈ and ♑. The humane-sign clause has no record. *Repair:* add a record for the Lord of ☽'s house; R2145 keeps only ☽ in fire or water.

**F08 · MODERATE · UNIT NORMALISED · sure.** PDF354: "not between them more then **one Signe** … in the house of him that lost it". R2146 says "about thirty degrees" and "near-owner", and its note claims the degrees are printed. The print measures in signs here, then in degrees in the next clause. *Repair:* keep "one Signe" and "the loser's house".

**F09 · MODERATE · PASSAGE OMITTED · sure.** PDF356–357, under the margin "Not stolne.": "Lord of the house of the ☽ separating from any Planet … fled of its owne accord; … some other from him, it is driven away; the like … by the Lord of the second … abideth still, and is not stolen". No record covers it. *Repair:* add one citing [356, 357].

**F10 · MODERATE · ADDED TARGET · sure.** PDF357: "applying to the Lord of the ascendant, or to the degree of the second house". R2172 adds "second ruler". *Repair:* delete it.

**F11 · MODERATE · "CHIEFLY IF" MADE REQUIRED · sure.** PDF359: "the Beasts be lost, **chiefly if** the Lord of the sixt be cadent". R2200 says "…**and** cadent". *Repair:* make cadency a strengthener, not a condition.

**F12 · MODERATE · CONDITION DROPPED · sure.** PDF359: "□ to any infortune **in the fourth**". R2202 omits "in the fourth". *Repair:* add it.

**F13 · MODERATE · ALTERNATIVES DROPPED · sure.** PDF355 has "or in the house of" for ♃, ♂, ☉ and ♀. R2151–R2154 omit it. R2156 keeps it for ☽; ♄ and ☿ correctly have none. R2151 also drops "fast or abstinency" and adds "offices". *Repair:* add "or the Lord of the 1st in X's house" to each.

**F14 · MODERATE · GLYPHS LEFT UNREAD · sure.** PDF358: "☉ in the ascendant (unlesse in **♎ or ♒**) found". R2186 says "Aquarius-like/another glyph". *Repair:* name ♎ and ♒. Three other records flag glyphs that are clear on the page: ☉ (R2184), ♊ ♍ ♐ ♓ (R2197), △ (R2207).

**F15 · MODERATE · SIGN PRECISION AND PRECONDITION · sure (subject uncertain).** PDF357: "in ♋ ♏ or ♓ … Wels; ☽ in the **last face** of ♑ … Ships; **this must be when things are lost neer a Harbour**".
- R2179 writes "late Capricorn".
- It turns the harbour clause into part of the location instead of a precondition.
- It reduces ♋ ♏ ♓ to "watery signs".
- It adds "Moon or" as a subject; the print only implies the subject, so that point is uncertain.

*Repair:* keep "last face", the glyphs, and the harbour precondition.

**F16 · MODERATE · ADDED CLASS, CLAUSE DROPPED · sure.** PDF358: "in ♋ … Dennes … Rivolet, if ♒ or ♓ … Fish-ponds, in the **last moity** of ♑ … Ships, or … Wood-yard". R2192 adds "or other watery signs" and drops the ♑ clause, which hides the print's last-face (p.323) versus last-moiety (p.324) discrepancy. *Repair:* list the clauses as printed.

**F17 · MODERATE · PRINTED SCOPE NOTES OMITTED · sure.** None of these printed margins appears in any record (R2158 is the only record carrying a margin note):
- PDF354 "This principally concerns Cattle strayed", which governs R2139–R2143.
- PDF355 "This was Friarly Astrology … Abbey or Nunnery", which governs R2151.
- PDF358 "This concerns Goods immovable" and "\*This hath relation to Beasts strayed" (the asterisk is at "the Moon in earthly Signes"), which govern R2193–R2195.

*Repair:* attach each note to the records it governs.

**F18 · MODERATE · EXCEPTION MISSTATED · sure.** PDF356: "except there be **an Infortune in the ascendant or second** … ⊗ or **his Lord** … **these signifie losing**". R2169 blurs the placed infortune into "first/second … unfortunate", drops ⊗'s lord, and omits "signifie losing". *Repair:* restate it as printed.

**F19 · MODERATE · RELATION MISPARSED, CLAUSE OMITTED.** PDF356.
- **R2167 (sure):** makes the L1–thief contact mutual. The print reads "Lord of the ascendant to the Significator …, or the Signifier of the Theef apply to the Lord of the ascendant by □ or ☍".
- **R2168 (uncertain, the print is elliptical):** has the ☽ aspecting the lords of its house, term, the 2nd and ⊗. In the print those lords stand alongside the ☽ as parties to the thief contact.
- **Omitted (sure):** "if any Planet be in the ascendant, and give his power to the Signifier of the Theef, or the Signifier to him by □ or ☍".

*Repair:* keep the printed directions and add the omitted clause.

**F20 · MODERATE · TIMING LIMIT DROPPED · sure.** PDF354: "some hope … **during that aspect with the degree ascending**". R2141 omits the limit. *Repair:* add it.

**F21 · MODERATE · NARROWED READING · uncertain.** PDF359: "**for the most part** Lord of the twelft or sixt in the twelft or sixt … kept close". R2204 says "its own respective house" and drops the hedge. p.324's "sixt in the sixt or twelft" supports either lord in either house. *Repair:* use the printed wording.

**F22 · MODERATE · OTHER UNITS OMITTED · sure.** These printed clauses have no record:
- PDF354: "place of the Moon in the Figure … in the ascendant … east"
- PDF357: "☽ in aspect to her Dispositor, good"
- PDF357: "otherwise not" (dropped from R2170)
- PDF358: "Lord of the second in the eleventh or twelfth, farre off"
- PDF358: "Lord of the ascendant and Lord of the hour be one Planet … pound"
- PDF358: "Moon in watry Signes, where water is"

Seven headings also have no record:
- *The place where the thing is that is lost*
- *Whether it be alive*
- *Whether the thing missing be stolne, or fled of it selfe*
- *That the Beasts are lost*
- *Dead or alive*
- *In Pound or not*
- *That the Cattle shall be found againe*

The third matters most: R2166–R2169 sit under a general "thing missing" heading, not a cattle one.

## Minor (sure, not material)
- R2142 "predicts recovery" for "there is hope".
- R2149 quotes "thing" where the heading reads "things".
- R2159 should cite PDF355–356.
- R2157 drops "things not having life" and "cause of the death".
- R2173 drops "chiefly if the Infortune behold…", and its kind label says dispositor.
- R2180 "newly developed" for "newly broken up".
- R2181 narrows "the thing … with the Loser" to a beast.
- R2185 adds "rather than thief".
- R2189 adds "official custody".
- R2191 drops "common" from "common Fields".
- R2194 drops "levell grounds".
- R2199 "under water" for "in water, or under the earth".
- R2201 drops "or sold".
- R2207's kind label says "sextile" where the print has △.
- All 70 `page_images` point to `evidence/pdf-NNN.png`, which doesn't exist here; the originals are in `source_images/`.

## Uncertain (not counted as errors)
- R2147 assumes "in one quarter" for the 30–70° clause.
- R2170 reads "or second house" as the Lord of the 2nd.
- R2181 cites a "p326–327 rule" that is outside this window.

## Checked and faithful
- Separation direction is never reversed (R2159, R2160, R2182, R2201).
- "Twelfth from the ascendant" is kept (R2139).
- 12th-house custody stays separate from the 8th-house death rules (R2176).
- The 30° and 70° thresholds are kept (R2147).
- The fixed-sign contradiction with p.325 is flagged (R2195).
- The cattle versus dead-things scope is kept (R2158, R2197).
- No later handwriting appears in any record.
- No record claims a prediction worked.

## Errata (errata-888, printed pp. 319–330 only)
- "p 324 l 10 r the". The "324" is slightly blotted, so the page number is a probable reading.
- "p 330 l 6 r or". Page 330 is PDF364, outside this window.

No record cites or applies either correction. I couldn't identify which word on p.324 line 10 the correction targets, because that depends on whether the heading counts as a line. I've left the body text unchanged.

## Boundary
Chapter L begins on PDF353 below the printed rule. Window A ends at a complete sentence on PDF359, and the catchword "How" leads into PDF360. I couldn't check the PDF364 boundary above "Of a Thief and Theft" because that image isn't in this window.

**FINDS_ERROR**
