# Lilly 1647 physician aphorisms (B02n, R1703–R1745): independent source-fidelity review

**Bottom line:** The count and the page boundaries are correct, and no record reverses the source's polarity. 6 records state something the print doesn't say (SOURCE_ERROR), 5 pick one reading of an ambiguous passage without saying so (UNRESOLVED), and 14 drop qualifiers. The most important finding comes from the errata page. Erratum p.285 l.11 "r therein" changes aphorism #33, and the record misses it.

## 1. What I read
- **Images:** all of PDF316, 317, 318, 319 and 320 (printed 282–286), at display resolution. I re-checked 318 and 319 for the lines the errata point to. I read the full errata page (`evidence/errata-888.png`), which was shown downscaled from 2217×3000 to 1478×2000.
- **Files:** all 14 listed in `MANIFEST.json`. That includes every field of all 43 records in `RULES.json`, plus `APHORISM_INDEX`, `SECTION_COVERAGE`, `UNRESOLVED`, `SOURCE_IDENTITY`, `SOURCE_IMAGE_MANIFEST`, `COUNTS` and `REQUEST.md`.
- I used Read only and edited nothing. My observations below come from the images, not from the producer's notes.

## 2. Count and boundary check
- **Start:** PDF316, below the rule after "…in danger of a Dropsie." The heading reads "Astrologicall APHORISMES beneficiall for PHYSICIANS." ✓
- **End:** #43 on PDF320, above the rule before "CHAP. XLV. A sick Doctor, what was his Disease? If curable?" The dated 1645 chart is correctly left out. ✓
- **43 items:** #1 has no printed number (it opens with a large initial "IN"). Numbers 2–43 are printed in order, with no gaps or duplicates. ✓
- **Items split across pages:**
  - #9: 316→317, breaking at "then | the Ascendant" ✓
  - #30: 318→319, breaking at "now | there," ✓
  - #42: 319→320, breaking at "if ♂ or the ☉, | it proceeds" ✓
  - The "20 If" at the foot of 317 is only a catchword; #20 starts on 318. ✓
- **Page fields:** the PDF page and printed page fields are right for all 43 records (the "282" on PDF316 is partly blurred). IDs run R1703–R1745 without gaps. The kind counts (26 method / 17 claim) match `COUNTS.json`.
- **Not verifiable from these pages:** the labels "chapter XLIV", "book II" and "printed chapter XLIV" in `source_attribution`. No chapter or book number is printed on PDF316–320; the only chapter number visible is XLV, after the section ends.
- **Locator typos:**
  - #15's anchor reads "in his Falls"; the print has "in his Fall,".
  - #41's anchor reads "Occidentally"; the print has "Occidentall,".

## 3. Verdict map (all 43)

| Verdict | Aphorisms |
|---|---|
| **PASS (18)** | 1, 2, 7, 11, 15, 17, 19, 22, 24, 25, 27, 28, 29, 35, 36, 38, 39, 42 |
| **MINOR_OMISSION (14)** | 3, 6, 9, 10, 14, 16, 21, 26, 30, 31, 32, 37, 40, 41 |
| **SOURCE_ERROR (6)** | 4, 5, 13, 18, 33, 43 |
| **UNRESOLVED (5)** | 8, 12, 20, 23, 34 |

How I applied the categories:
- **SOURCE_ERROR:** the record says something the print does not. That covers a changed subject, a changed modality, an added alternative, or a dropped restricting condition or whole clause.
- **MINOR_OMISSION:** the record drops a qualifier, intensifier or tail clause, or adds a small gloss, but the claim still points the same way.
- **UNRESOLVED:** the print is genuinely ambiguous and the record silently picks one reading or overstates what is printed.

## 4. SOURCE_ERROR details

**#4 (PDF316, p.282; R1706)**
- **Record:** "movable signs an ending or change relatively quickly"
- **Print:** "moveable ones shew an end one way or other quickly"
- **Defect:** "or change" is not printed. It blurs the print's own split, where common signs "vary the Disease" and movable signs show "an end". "Relatively" weakens "quickly". The record also drops "and whether it will terminate quickly, or endure long".
- **Repair:** "movable signs show an end one way or other quickly". Keep the existing exception about an end by either outcome.

**#5 (PDF316; R1707)**
- **Record:** "A physician first visiting in Saturn's planetary hour is said to face prolonged sickness or treatment and torment…"
- **Print:** "…his Patient shall either be long sick, or long in curing, and suffers much torment in his cure; nor shall he be cured…"
- **Defect:** the one who is long sick or long in curing is "his Patient", not the physician.
  - "Suffers much torment" most naturally continues with the patient as subject.
  - The tense shift from "shall" to "suffers" leaves a weaker reading where the physician suffers. Both readings should be recorded.
  - "Much" is also dropped.
- **Repair:** "his patient shall either be long sick or long in curing, and suffers much torment in his cure [subject most naturally the patient]; nor shall he be cured until almost both physician and patient despaired."

**#13 (PDF317, p.283; R1715)**
- **Record:** "said not necessarily to destroy". The exceptions add "not necessarily destructive … not necessarily helpful".
- **Print:** "The □ or ☍ of the Fortunes, as it destroyeth not, so neither doth the benevolent aspect of the Infortunes profit, unlesse that aspect be with Reception."
- **Defect:** the print's flat "destroyeth not" and "neither doth … profit" are weakened to "not necessarily", three times. Calling the claims "Asymmetric" misdescribes the printed "as … so neither" parallel. The record is right that reception attaches to "that aspect", meaning the infortunes' aspect.
- **Repair:** delete "necessarily" everywhere, and describe the two halves as parallel.

**#18 (PDF317; R1720)**
- **Record:** "Fear is prescribed when…"
- **Print:** "The Physitian may justly feare his Patient, when…"
- **Defect:**
  - "May justly fear" (fear is justified) becomes "prescribed" (fear is required). The physician and "his Patient" also drop out.
  - The exception quotes the house list as "eighth and seventh", but the print reads "eighth seventh", with no "and" and no comma.
  - The tenth-house handling is correct. Read literally, "the rest under" puts the tenth under the Earth; keep that as printed.
- **Repair:** use "the physician 'may justly feare his Patient' when…" and quote the house list exactly.

**#33 (PDF319, p.285; R1735)**
- **Record:** "together with an infortune at both times … unless a benefic casts favourable rays at one of those times." The prerequisites have no location condition.
- **Print:** "and both times there happens to be an Infortune, … unlesse a Fortune at one of those times cast thither his benevolent Beames."
- **Erratum:** "p 285 … l 11 r therein". Line 11 is exactly "ty, fourth, seventh, eighth or twelfth, and both times there happens to be".
- **Defect:** with the erratum applied, the infortune must be "therein" (in that natal house or place) at both times, and the fortune's rays must be cast "thither" (to that place). The record drops both location conditions, so its trigger is broader than the source: any infortune, anywhere.
- **Repair:** add "therein [errata 285/11; print 'there']" to the condition and "cast thither" to the exception. Note that the erratum applies.

**#43 (PDF320, p.286; R1745)**
- **Defect:** a whole clause is missing: "beware in the beginning of a sicknesse when the ☽ is thus unfortunated".
- **Also:**
  - For "in masculine Signes, Orientall and above the Earth", the record's capitalised AND makes all three a joint requirement. The list could also be read as separate aggravating factors; record both readings.
  - "Is said to make" turns the print's "when" into a cause.
- **Repair:** add the "beware…" clause, including its sickness-onset timing, to the statement and prerequisites.

## 5. UNRESOLVED details

**#8 (PDF316; R1710)**
- **Print:** "for the Urine was sometimes of the essence of the sick"
- **Record:** "invokes urine as sometimes part of the sick person's essence". This drops "was".
- **Readings:**
  - (a) In older English, "sometimes" could mean "formerly": the urine was once part of the sick body, which explains why it can represent the patient.
  - (b) The modern sense, "occasionally".
- This sense comes from my general knowledge of the language, not from anything in the directory.
- **Repair:** quote the clause including "was", and record both readings.

**#12 (PDF317; R1714)**
- **Record prerequisite:** "Both lights obscured or below Earth as the source states."
- **Print:** "…presence of the ☉ or ☽, so no safety, or hopes of recovery … when they are obscured or subterranean". The word "both" is not printed.
- **Readings:**
  - (a) Both lights: supported by the plural "they", by the light analogy, and by "if either of them be then afflicted" as a further aggravation.
  - (b) Either light: the antecedent of "they" is "☉ or ☽".
- **Also:** "no safety" is dropped.
- **Repair:** quote "they" instead of claiming "both" as printed, list both readings, and restore "no safety".

**#20 (PDF318, p.284; R1722)**
- **Print:** "…apply to the Lord of the ascendant, though under the earth, … the cure must needs be sooner if the application be above the Earth…"
- **Readings:** what is "under the earth" could be (a) the ascendant ruler, or (b) the Moon or the application itself.
- **Defect:** the record's prerequisite ("Target") chooses (a). Its own exception ("application even below Earth") implies (b), so the record contradicts itself. "Must needs" is weakened to "is said to be sooner still".
- **Repair:** record both readings, restore "must needs", and set the uncertainty flag to true.

**#23 (PDF318; R1725)**
- **Print:** "prolongs the Infirmity, and also signifieth Death, if the Lord of the fourth be an Infortune; of a benevolent expect the contrary."
- **Readings:**
  - (a) The "if" governs only "Death". The record imposes this one via its exception "Keep duration testimony distinct".
  - (b) The "if" governs both "prolongs" and "Death", so a benevolent reverses both.
- Erratum 284/14 lands on this line (§8).
- **Repair:** record both readings, cite the erratum, and set the uncertainty flag to true.

**#34 (PDF319; R1736)**
- **Print:** "is opposite to that of the Nativity, and is either the fourth, sixth, eighth, twelfth or seventh"
- **Defect:** an ascendant that is literally opposite can only be the natal seventh, yet the list also names the 4th, 6th, 8th and 12th. The record keeps both conditions joined but doesn't note the clash.
- **Readings:** (a) "opposite" is meant loosely ("contrary"); (b) the two clauses are alternatives despite "and".
- **Repair:** keep the printed grammar and add a note on the clash, alongside the existing note about "same".

## 6. MINOR_OMISSION details
- **#3 (316):** "if the tenth house or Lord thereof, his Physick is improper" has no verb. The record quietly fills in "misfortune of"; mark this as supplied from the parallel clause.
- **#6 (316):**
  - "partly disdaine or reject" loses "partly".
  - "his pains ill rewarded, and his person slighted" becomes "paying or respecting … poorly": "and" turns into "or", and the passives are pinned on the patient.
  - "shall find" becomes "produce", which implies cause.
  - The exception claiming "enters upon a cure" is a different event from "first visits" is interpretation; the print only uses different words.
- **#9 (316–317):** keeping "or" is correct. Two source facts are missing:
  - The closing "& sic in aliis, where no consent is", which restates only the consent condition.
  - #8 already assigns the ascendant to the sick person when urine is brought "whether the Querent come with consent or no". If "no Urine or consent" means either one missing, the urine-without-consent case is claimed by both #8 and #9; if it means neither, it isn't.
  - Record both facts without resolving the question.
- **#10 (317):** "for she is a generall Significatrix in all things" loses "in all things", and the reason is merged into the instruction. The opening "But", which contrasts with #9, is also lost.
- **#14 (317):** the certainty marker "without doubt the sick party will recover" is dropped. The ambiguity flags are otherwise good.
- **#16 (317):** "much feared" becomes "fear".
- **#21 (318):** "much affliction" loses "much". "So also doth the □ or ☍…" becomes a vague "likewise is adverse"; it should carry both claims (protracts the disease, much affliction).
- **#26 (318):** "shewes ill and much danger, and argues much distrust and fear" becomes "danger, distress and fear or distrust". "Much" is lost twice, "ill" (possibly an adjective on "danger") becomes "distress", and "and" becomes "or".
- **#30 (318–319):**
  - "easily", "much difficulty" and "much better" are weakened.
  - "now here, now there" is glossed as "movement between body parts", which the print doesn't say; quote it instead.
  - The reading depends on erratum 284/37 but doesn't cite it.
  - The tension with #4 is not noted (§9).
- **#31 (319):** "ever feare the ill positure…" becomes "examine", losing the stance of always fearing. Erratum 285/4 ("her" = the Moon's signification) is not cited.
- **#32 (319):** "goe on the more hardly" becomes "slower", which is not printed ("hardly" means with difficulty). "And" becomes "or".
- **#37 (319):** calling it the "Author's general rationale following a Sun-based prognosis" is an inference. It is numbered separately, with no "for" or "because" linking it to #36. "Candle" is dropped.
- **#40 (319):** "much encrease" becomes "aggravating", and "ill government and carelesnesse" becomes "careless or bad management".
- **#41 (319):** the closing "&c." is dropped, so the record no longer signals that the rule is open-ended.

**Systematic drift:**
- "Much" dropped: #5, 16, 21, 26, 30, 40.
- Certainty or necessity markers dropped: #14 ("without doubt"), #20 ("must needs"), #31 ("ever").
- "And" turned into "or": #2, 6, 26, 29, 32, 40.

## 7. Notes on passing records (ambiguities kept correctly)
- **#15:** "it's doubtfull the sick party will dye". (a) In older usage "doubtful" can mean feared, so death is feared. (b) "Uncertain", so death is not certain. The record keeps the word and makes no flat death rule ✓. Adding both readings would help.
- **#19:** "there's great fear of recovery". (a) Fear about recovery, i.e. recovery is in doubt. (b) The literal fear that he will recover, which jars with the context. A misprint can't be tested: the errata list has no entry for p.283. The record keeps the wording ✓.
- **Also kept correctly:** #14 "so affected"; #27 "Lord of the one and Dispositor of the other"; #28 "Animals", "both" and "so on the contrary" (3 explicit cases plus the contrary); #42 Saturn "Cold" only, not normalised to cold-and-dry.
- **Trivial wording in passing records:**
  - #2: "Disease or part" becomes "and".
  - #7: "shall" becomes "should".
  - #11: "(choose the relevant context)", though the print makes either time enough.
  - #29: "occult and not knowne" becomes "or".
  - #36: "usually" is labelled as timing; it is frequency.
- No wrong polarity anywhere. The case counts are correct in #11, 12, 14, 18, 21, 28, 29, 33, 34 and 36.

## 8. Errata on printed pages 282–286
The errata page has exactly these entries in range: "p 284 l 14 r if; l 37 dele semi-colon, p 285 l 4 r her, l 11 r therein". There are none for 282, 283 or 286; the list jumps from p 277 to p 284 and from p 285 to p 291.

The line numbers only make sense if the running head is not counted. Counting it would put each entry on a line with no plausible target.

| Entry | Line in this copy | Target | Effect on records |
|---|---|---|---|
| 284 l14 "r if" | #23: "if the Lord of the fourth be an Infortune; of a benevolent expect the con-" | The word isn't named. The first word already shows "if" in this copy, so the likely target is "of a benevolent" → "if a benevolent". I can't tell whether this copy was already corrected. | Meaning of #23 unchanged; not cited |
| 284 l37 "dele semi-colon" | #30: "…not without much difficulty[mark] re-" | Delete the mark → "not without much difficulty removeable" | Record follows the corrected sense; not cited |
| 285 l4 "r her" | #31: "mix[blotted]her signification" | "her" (the Moon's) | Consistent; not cited |
| 285 l11 "r therein" | #33: "both times there happens to be" | "there" → "therein" | **Material.** Missing (SOURCE_ERROR #33) |

Limits of this evidence:
- The errata give only page, line and replacement word; the target words are my inference.
- There is one copy, and the small type was read downscaled.
- The punctuation in "r if;" is uncertain.
- `errata-888.png` is listed in `MANIFEST.json` but not in `SOURCE_IMAGE_MANIFEST.json`, so I'm assuming it's the same copy.
- The preface says the list is selective ("the literall and most observable are here met withall"). The missing tenth house in #18 and "fear of recovery" in #19 are therefore not confirmed as correct just because no erratum lists them.
- PDF319 line 11 has a small superscript mark between "there" and "happens". It may be a reader's insertion mark; I couldn't resolve it.

## 9. Source facts missing from the rules
1. The "therein" erratum on #33 (material). Errata 284/14, 284/37 and 285/4 should be cited on #23, #30 and #31. These four mappings can replace the open item U18.
2. #4 and #30 conflict: "vary" belongs to common signs in #4 but to movable signs in #30 ("Moveable Signes easily cause the Disease to vary"), while #4's movable signs give "an end … quickly". Keep both; #4's added "or change" partly smooths over the conflict.
3. The #8/#9 overlap and #9's closing "where no consent is".
4. #43's "beware in the beginning of a sicknesse".
5. #1 has no printed number.
6. A later handwritten "6th House" sits beside the page number on PDF317 and PDF319. It isn't the author's text; record it in witness notes so it is never taken in as source text.
7. "Chapter XLIV" doesn't appear on any of these pages.

## 10. Weakest step
The weakest step is that `source_statement` is a free paraphrase with no line-by-line transcription behind it. Every defect type traces back to that:
- modality drift (#13, 14, 18, 20, 31)
- the changed subject in #5
- the added glosses in #4 and #30
- the dropped clauses in #43 and #9
- the deferred errata mapping (U18), which is how #33's "therein" was missed

A second problem: modern editorial cautions (#8, 9, 26, 40) sit in the same `exceptions_and_modifiers` field as exceptions that come from the source, so a reader can't tell them apart. Also, `APHORISM_INDEX` should flag textual uncertainty for #12, 20 and 23, plus an erratum marker for #30, 31 and 33.

## 11. What I did not verify
- Any SHA-256 hash; I had Read only.
- That the PNGs faithfully render the stated PDF, or that the errata page comes from the same copy.
- The Book II / Chapter XLIV labels, other copies or states, the 1659 edition, or Lilly's own sources.
- The older-English word senses (doubtful, sometimes, hardly); these come from my general knowledge, not from the directory.
- Fine glyphs: the mark at 318 l37, the blotted word at 319 l4, the mark at 319 l11, the punctuation of "r if;", and the "282" page number.
- The cumulative figures in `COUNTS.json`, which are out of scope.

I ran no tests and make no claim of medical or predictive validity. Nothing was merged, released or edited.