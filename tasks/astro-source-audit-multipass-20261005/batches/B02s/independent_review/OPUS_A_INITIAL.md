# Lilly, *Christian Astrology* (1647), Ch. XLIX "Of Marriage": review of RULES.json batch B02s

I read the 11 source images first and wrote my own reconstruction before opening RULES.json. I opened PDF338 a second time to confirm two readings.

**Overall result:** 38 issues, 14 of them major. The single biggest problem is coverage: RULES.json covers only PDF336–345 (`"range": [336, 345]`), while the chapter runs to PDF353. I had no images for PDF346–353, so that part is unreviewed.

**Conventions:** I have written the long s as "s". Symbols (☽ Moon, ⊙ Sun, ♀ Venus, ♂ Mars, ♄ Saturn, ♃ Jupiter, ☋ South Node, ☌ conjunction, □ square, ☍ opposition, △ trine, ✱ sextile) are as printed. "Ch." means chapter, "MS" means handwritten, "L1"/"L7" mean the Lord of the 1st/7th house, and "p." is the printed page number.

## 1. Reconstruction of printed pp. 302–311 (made before reading RULES.json)

| PDF / page | Content and order |
|---|---|
| 336 / 302 | Ch. XLVIII aphorisms 40–43 sit above the divider and are out of scope. Below it: **"CHAP. XLIX. Of Marriage."** The opening paragraph assigns significators and gives application rules (Lord of ascendant or ☽ applying to the Lord of the 7th: "many petitions, solicitations and prayers"; by □/☍ with reception: "slownesse, labour and travell"). It runs on to p.303 ("great good will of the man or woman quesited after… △ or ✱"). The handwritten "Gadbury saith… try your Rules" note is MS, not print. |
| 337 / 303 | **"Aphorismes of ALKINDUS touching MARRIAGE."**, with a printed margin note: "* Or, if the Lord of the seventh apply to the Lord of the ascendant." Five aphorisms follow. Then the heading **"Of Marriage, whether it shall take effect or no?"**, which runs on to p.304. |
| 338 / 304 | The rest of that section: "unwillingly be consented", "the ☽ in the tenth", "great encouragement". Then the heading **"Of Marriage."** with the man's and woman's significators. A printed marginal heading **"It shall be."** introduces five numbered testimonies. A margin note reads "* Viz. one in the Termes, the other in the Triplicity…". The text runs on to p.305 ("Dig-/nities"). |
| 339 / 305 | Margin heading **"Which love most, or desire it most."** Frustration, helpers by house, and "promised by ☌ □ or ☍". Then the heading **"What shall be the occasion of hindring the Marriage."**, running on to p.306. |
| 340 / 306 | Hindrances by the lords of the 2nd–12th houses. |
| 341 / 307 | The note on who will assist, and "I have herein dealt very candidly". Headings **"Whether a man shall Marry."**, **"The time of Marriage."** and **"How many Husbands a woman shall have."** There is a handwritten change at "seventh and/⊙ ? ♂". |
| 342 / 308 | Headings **"From what part one shall Marry."**, **"What manner of person he or she is."** (with an MS Gadbury note beside it), **"Whether man or woman be more noble."** and **"Who shall be Master of the two."** |
| 343 / 309 | Headings **"Whether she be rich or not."**, **"Whether the MARRIAGE be Legitimate."** and **"How they shall agree after Marriage."**, then an unnumbered italic heading **"Disagree."** |
| 344 / 310 | Headings **"Who shall be the cause of their Strife, or the authour of their Good."** and **"That the Marriage shall be broken, and the cause thereof."** |
| 345 / 311 | Two Moon aphorisms, with the margin note "An Arabick Aphorisme, not overmuch to be credited without consent of other Significators". Headings **"Whether a Man or his Wife shall dye first…"** and **"Which of the two shall live longest."**, which continues on p.312 (unreviewed). |

**Errata page entries for pp. 302–319:**
- "p 305 l 22 dele ☌"
- "p 306 l 26 r undertaken"
- "p 307 l 28 r for ⊙ and ♂"
- "p 312 l 17 r it is no good"
- "p 315 l 7 r ☋"
- "p 315 l 10 r seventh"

There are no errata for pp. 302–304 or 308–311.

## 2. Issues

### Major

**01 · R1937 (and R1938's exception) · Negation, involving consent**
- **Source:** p.304, "it will **unwillingly** be consented unto by the party desired". I confirmed this on the second view.
- **Problem:** The record says "willingly". The errata page has no entry for p.304. The printed word does contradict p.303 ("great good will"), so it may well be a misprint, but the volume never corrects it.
- **Fix:** Record the printed "unwillingly". Add a flag that it conflicts with p.303 and that "willingly" would be an editorial repair, not an original-volume erratum. Rewrite R1938's "contrasts willing completion" on the same basis.

**02 · R1940 · Wrong house**
- **Source:** p.304, "also the ☽ in the **tenth** signifieth the same". Confirmed twice.
- **Problem:** The record says "Moon in seventh".
- **Fix:** Change it to "Moon in the tenth". Keep the separate clauses as they are: ☽ applying to ♀ "but by mediation of Friends", and the ⊙–♀ application "especially when ⊙ hath dignity in the seventh, idem".

**03 · R1961 · Conflicts with the original-volume erratum**
- **Source:** p.305, "Marriages promised by ☌ □ or ☍, note performance with much adoe". The errata page says "p 305 l 22 dele ☌".
- **Line number:** This is the only ☌ on p.305. It sits on text line 23 by my count, so the erratum's line number is one off (its figure is partly unclear).
- **Problem:** The record keeps the conjunction as a laborious aspect.
- **Fix:** "Promised by □ or ☍: much ado; △ or ✱: easy; with Reception: best of all." Cite the erratum.

**04 · R1930 · Added qualifier**
- **Source:** p.303, "When the Lord of the ascendant doth apply to the Lord of the 7th house, * it's an argument the Marriage shall be performed". No aspect type is given.
- **Problem:** The record adds "by trine or sextile".
- **Fix:** Remove "by trine or sextile". Keep the margin alternative (Lord of the 7th applying to the Lord of the ascendant).

**05 · R1932 · "and" turned into "or", and the wrong planet as referent**
- **Source:** p.303, "if ♀ doe behold the ⊙, **and** the ⊙ have any dignity in the ascendant, **and** behold the Lord of his house, viz. of the Signe wherein he is".
- **Problem:** The record says "ascendant dignity **or** aspect to ascendant lord". The source requires all three conditions together, and the planet the Sun must behold is its own dispositor, not the ascendant lord.
- **Fix:** Require all three conditions, and name the third as "⊙ beholds his own dispositor".

**06 · R1933 · Premise reversed**
- **Source:** p.303, "if the Planet applying, and he to whom he doth apply, be both cadent… especially if their Lords doe not behold them". The source assumes an application exists.
- **Problem:** The record says "not regarding each other".
- **Fix:** "Applying planet and the planet it applies to both cadent, especially if unbeheld by their dispositors: good hopes at first, then by dallying… no Marriage."

**07 · R1949 · Statement has no source**
- **Problem:** Nothing in the source matches "Sun or Venus in angular exchange…".
- **What the source actually says at this point:** p.304 "the * Signifiers in interchangeable Dignities", with the margin note "Viz. one in the Termes, the other in the Triplicity of the Significator, or the like". This continues on p.305: "the ☽ in the seventh giving vertue to the Lord of the ascendant, or Lord of the seventh."
- **Fix:** Replace the record with these two clauses and set its locator to PDF338–339.

**08 · R1992 · Wrong planets, lost conditions, word meaning reversed**
- **Source:** p.308, "and for the woman, judge by the Planet the ⊙ beholdeth; ⊙ in △ or ✱ of ♄, wise and painfull; ⊙ aspecting ♃, honest".
- **Problem:** The record says "Moon with Mars… painful traits". It has the wrong luminary and the wrong planet, and drops the △/✱ condition, the word "wise", and the "for the woman" condition. "Painfull" here means painstaking or diligent, not "painful". The record's "pleasant" has been imported from the ☽–♀ clause.
- **Fix:** Restore the source wording and conditions.

**09 · R2018 · Wrong meaning and an invented aspect**
- **Source:** p.310, "☽ in □ of good Planets, by dead men; ☽ in ☌ of good Planets, promises good by their owne industry and labour".
- **Problem:** The record reads "square/opposition shows harder gain or quarrels". The source never mentions opposition here, and it drops the ☌ clause.
- **Fix:** △/✱ with good planets: gifts from Friends. □: by dead men. ☌: good by their own industry.

**10 · R2028 · Wrong sign, misreading the glyph**
- **Source:** p.311, "the ☽ being in the twelve first degrees of **♑**". The glyph matches "first minute of ♑" and the "♈ ♋ ♎ ♑" list on the same page, and differs from ♍ in "♊ ♍ ♐ ♓".
- **Problem:** The record says Virgo. It also garbles the outcomes: the source has "shall lose her before marriage, or dye within six moneths, or live in discord with her", for someone "Espoused to a Wife".
- **Fix:** Correct the sign to Capricorn and restore the three outcomes. Keep the margin caution.

**11 · R2013 · Premise changed**
- **Source:** p.310, "an Infortune in the tenth…: In the fourth, either a Divorcement or a willingnesse to it, or hinderance in Dowry". The condition is a malefic *placed in* the 4th.
- **Problem:** The record says "Fourth ruler affliction" and drops "a Divorcement".
- **Fix:** Restore the placement condition and the divorce alternative.

**12 · R1967 · Allegations turned into possible facts (sexuality claims)**
- **Source:** p.306, "(if either party have any;) or if a Batchelour propounds, **perhaps it's objected**, he either is not capable of getting a Child, or that he hath had a Bastard, or **is scandalized about such a thing**, or that **it's feared** the party will be wanton, or given to luxury… vary your rule, and it serves if a woman propound".
- **Problem:** The record states "possible infertility, earlier child out of wedlock". It drops the "objected", "scandalized" and "feared" framing, the "if either party have any" condition, the bachelor condition and the rule for when a woman proposes. "Luxury" here (17th-century usage) means lechery, so "pleasure and luxuries" is a mistranslation.
- **Fix:** Keep these as objections and rumours recorded by the source, and restore the dropped conditions.

**13 · R1963 · Wrong mechanism**
- **Source:** p.305, "consider what **evill** Planet… doth hinder the Reception… or who frustrates their aspect, or prohibits them, or interjects his Rayes betwixt the Significators".
- **Problem:** The record substitutes "transferring light", which elsewhere in this chapter is a mechanism that *helps* the marriage (R1939, R1956–60). It also drops "evill" and the section's opening premise ("although there seem great probability… yet you find just cause to judge, it shall not either really be acted…").
- **Fix:** Restore the source's mechanisms, the "evill" qualifier and the premise.

**14 · Batch-wide · Coverage gap**
- **Problem:** The claimed scope runs through PDF353, but the 112 records end at R2032 (p.311). Nothing covers the following:
  - The "Which of the two shall live longest." heading and its first sentence (p.311, continuing onto p.312).
  - All of PDF346–353 (printed pp.312–319).
  - The pages carrying errata p.312 l.17 ("it is no good") and p.315 l.7 and l.10 ("☋", "seventh").
- **Consequence:** I could not check for the sexuality or gender passages, the consent and force exceptions, or the warnings about false accusations that you asked about, if any of them fall in that range.

### Moderate

**15 · R1931**
- **Source:** p.303, "☽ doe apply unto ♀, and she strong, encreasing in her motion, and in some of her owne Dignities, and the ☽ likewise".
- **Problem:** The strength, increasing motion and dignity belong to ♀ first, and then to the ☽ "likewise". The record gives the motion to the Moon only.

**16 · R1934**
- **Source:** p.303, "if ☽ ⊙ ♀ and Lord of the seventh, and Lord of the ascendant be in angles… or if their Lords behold them".
- **Problem:** The record drops the named significators and the alternative about the dispositors beholding them. It also softens "shall" to "may".
- **What to keep:** The consent clause, "finished by the consent of all parties", should be kept close to verbatim.

**17 · R2009 and two missing clauses (page boundary)**
- **Missing from p.309:** "The Lord of the ascendant and Lord of the seventh in □ or ☍, Lord of the ☽ impedited beholding the ascendant". The record's locator lists PDF344 only.
- **Missing from p.310:** "♄ ♂ or ☋ in the ascendant, idem, if the question be asked by the man."

**18 · Missing headings**
- **Missing:**
  - p.304 "Of Marriage."
  - p.308 "What manner of person he or she is."
  - p.309 "How they shall agree after Marriage."
  - p.310 "Who shall be the cause of their Strife, or the authour of their Good."
  - p.311 "Which of the two shall live longest."
- **Consequence:** Because the p.310 heading is missing, R2011–R2019 are filed under "disagreement", including the positive "authour of their Good" material.

**19 · R2011**
- **Source:** p.310, "and be in the ascendant or seventh house".
- **Problem:** The record drops this placement condition.

**20 · R2017**
- **Source:** p.310, "if the ☽ doe aspect, or be in ☌". The rule for which partner suffers is limited by "if this ☌ be in the tenth or fourth".
- **Problem:** The record narrows the premise to a conjunction only and drops the 10th/4th limit.

**21 · R1964**
- **Source:** pp.305–306, "they break off on the Querent's behalf, Money… wanting on that side".
- **Problem:** The record drops which side lacks the money and imports "dowry". It also cites PDF340 only.

**22 · R1970 and R1971**
- **Source:** p.306, "Death will bereave the **querent**", "the **quesited** hath not a sufficient Portion", "the quesited's Kinred", "Journey… by the querent".
- **Problem:** The records drop the querent/quesited roles, and R1970 adds "inheritance".

**23 · R1996**
- **Source:** p.308, "A more assured way is… most potentiall in essentiall Dignities; if no such thing be, who is best placed in an angle".
- **Problem:** The order of priority (dignity first, angularity as the fallback) is lost. The extension "of two Companions, or any one else" is missing.

**24 · R1998**
- **Problem:** The outcome is missing. The source (pp.308–309) says "the querent shall be Master".

**25 · R2005**
- **Problem:** The negative qualifier "and they not Significators in the Question" (p.309) is hidden behind "stated signification conditions". The ☋ glyph is legible, so the record's "node-like glyph" hedge isn't needed.

**26 · R2007**
- **Problem:** The record drops the condition "if neither the Lord of the ascendant, or of the seventh be in angles", the qualifier "or strive for it", and the word "impedited" from "⊙ impedited, worst for the man", along with the ♀ and ☽ counterparts (p.309).

**27 · R2031**
- **Source:** p.311, "neer the **Lord of** the eighth".
- **Problem:** The record says "near eighth".

**28 · R2027**
- **Problem:** The record omits the degree range "between the seventeenth degree of ♐, and the first minute of ♑" and the alternative "depart from her Husband" (p.311).

**29 · Missing clause and omissions on p.305**
- **Missing clause:** "and so of the other Significators, for those that apply argue most love".
- **R1952 omissions:** "free from love" and "her Portion is knowne, or the mans".

### Minor

**30 · R1941 and R1948**
- **R1941:** "the other's house" stands in for "in the seventh"/"in the ascendant", and "or with the Lord thereof" is dropped.
- **R1948:** The premise "without the preceding simple aspect routes" is added. The source just lists this as the fifth testimony.

**31 · R1986 (glyph uncertainty)**
- **Problem:** The record matches the corrected reading from the errata entry for p.307 l.28, "for ⊙ and ♂", but doesn't say it relies on that erratum.
- **Not repaired:** The printed glyph between ⊙ and ♂ is obscured, and a handwritten note strikes "and" and adds "for". I have left this unrepaired. I also read "⊙ in ✱ or △" with moderate confidence only.

**32 · R2032**
- **Source:** p.311, "Tropick Signes, as ♈ ♋ ♎ ♑".
- **Problem:** These are the cardinal signs, so "tropical sign" is misleading. The qualifier "Usually I observe" is dropped.

**33 · R2020 and R2021**
- **R2020:** The heading reads "That the Marriage shall be broken", not "when".
- **R2021:** It drops the contrast "though at present it is very feasible", and its premise begins on p.310 (PDF344).

**34 · R2026**
- **Problem:** The source says "describe that Planet, and you may notifie the party". It does not say the person is identified by house.

**35 · R1965, R1966, R1968, R1974**
- **R1965:** The source has "some Journey", not "short".
- **R1966:** The source has "will settle no Estate", a refusal, not an "inability".
- **R1968:** "his Fathers Kinred" is dropped.
- **R1974:** "the querent shall never know by whom" and the fact that it is the querent who is slandered are both dropped.

**36 · Locator and metadata problems**
- **R1928:** The clause starts on p.302.
- **R1924:** "natural" is added.
- **R1935:** Its kind, "unheaded", contradicts its own text.
- **R1921:** I can see only aphorisms 40–43, so its description "forty-three general horary aphorisms" can't be checked.

**37 · R2003 (copy uncertainty)**
- **Source:** p.309 appears to read "and of **her** estate".
- **Problem:** The record silently normalises this to "man's estate" and adds a "turned-house scheme". The source says only "judge after the same manner".

**38 · R2006**
- **Source:** p.309, "☽ beholding her Dispositor, or Lord of the Exaltation…, idem".
- **Problem:** This is an independent testimony, not one that "strengthens" the first. The alternative about the Lord of the Exaltation is dropped.

## 3. Checks with no error found

- **Direction of lunar application:** No record reverses it. I checked R1922, R1923, R1928, R1946, R1980, R2001, R2010 and R2016.
- **Handwritten notes:** None of the handwritten material (the Gadbury notes, the "7th House" notes in the margins, the p.307 correction) has been imported into any record.
- **Margin cautions:** R2027 and R2028 correctly keep the margin note "not overmuch to be credited".
- **Records not named above:** I found no material error in them.

## 4. Counts and limitations

- **Records reviewed:** 112 (R1921–R2032).
- **Images inspected:** 11 (pdf-336 to pdf-345 and errata-888), with pdf-338 viewed twice.
- **Unreviewed:** PDF346–353 (printed pp.312–319, up to the divider before Ch. L). I was given no images for these pages and did not open any.
- **Reconstruction:** I made a full working transcription, but the table above is a condensed version.
- **Image identity:** I did not confirm that `source_images/` is byte-identical to the `evidence/` paths cited in RULES.json.
- **Errata line numbers:** These are off by about one line on p.305.
- **Scope of judgement:** All findings are about whether the records faithfully report the source text. None says anything about astrological validity.

FINDS_ERROR
