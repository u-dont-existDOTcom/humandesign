I found errors. Three would change how a rule gets applied, and two more are ambiguous passages the candidate states as settled without flagging them.

**What I inspected:**
- **Pages:** all 9 images: `source_images/pdf-330.png` to `pdf-337.png`, plus `source_images/errata-888.png`. The "888" comes only from that filename; I couldn't confirm the PDF page index myself.
- **Records:** all 69 units in `RULES.json` (R1852–R1920), all 35 entries in `UNRESOLVED.json`, plus `SECTION_COVERAGE.json`, `SOURCE_IDENTITY.json` and `ERRATA_COLLATION.json`.

**Independence caveat:** I had no way to list the directory. To find the image filenames I opened `SOURCE_IDENTITY.json`, `SECTION_COVERAGE.json`, `ERRATA_COLLATION.json` and the first unit (R1852) before reading the images. So I had already seen the producer's page plan and their errata conclusion. I transcribed all nine images before reading any of the other rule or aphorism text.

## What the images show
- **PDF330 / printed 296:** two closing lines of XLVII ("Master BOOKER … I forbeare."), a rule, then "CHAP. XLVIII. If a Servant shall get free from his Master?"
- **PDF331 / 297:** XLVIII ends; "Finis ſexæ Domus." (printed *sexæ*); a row of ornaments; "The Significations of the seventh House", with the topic list and the announcement of 43 aphorisms.
- **PDF332–336 / 298–302:** "Aphorismes and Considerations for better judging any Horary Question", numbered 1–43. All numbers are present, in order, once each. A rule follows, then "CHAP. XLIX. Of Marriage."
- **PDF337 / 303:** XLIX continues, then "Aphorismes of Alkindus". This page only marks the next boundary.
- **Handwriting in this copy:** "7th House" in the margins of 297, 299, 301 and 303, and a "Gadbury saith…" note beside the XLIX heading. U32 correctly treats these as non-authorial, and no unit relies on them.

## Material errors
- **F1 – R1907 (aphorism #31).**
  - **Source (PDF335/p301):** "if it be in going to **Warre**, you may feare the life of the Querent; if in a Journey, ill successe; if Marriage, an ill end of Wooing".
  - **Candidate:** "if **waning**, source warns for querent's life", with a precondition requiring a waning Moon.
  - **Problem:** this invents a lunar-phase condition and loses the war topic.
  - **Fix:** if the question is about going to war, fear for the querent's life; if a journey, ill success; if marriage, a bad end to the wooing. Also restore "seldome good end comes of a Question where the ☽ is impedited".
- **F2 – R1882 (#6).**
  - **Source (p298):** "unlesse **the ☽ and they** receive each other in the signification".
  - **Candidate:** "unless significators mutually receive one another".
  - **Problem:** the Moon is dropped, so the exception names the wrong party. U15 doesn't catch this.
  - **Fix:** the exception requires mutual reception between the Moon and Saturn/Mars. The point that cold and heat are symbolic ("neither of them is cold or dry") is correctly kept.
- **F3 – R1916 (#40) and U28.**
  - **Source (p302):** "an **unfortunate Planet** in the seventh … unlesse the same Planet be a Significator at the Birth".
  - **Candidate:** "a malefic" / "an infortune occupies seventh".
  - **Problem:** in these aphorisms "unfortunate" describes a planet's condition (afflicted): #3 "peregrine or unfortunate", #5, #41 "impedited or unfortunate". The candidate reads it that way in #3 and #41. Saturn and Mars are always called "Infortunes". Making it "malefic" changes which planets trigger the rule.
  - **Fix:** "an unfortunate (afflicted) planet in the seventh". The natal-significator exception itself is correct.

## Ambiguous passages stated as settled (moderate)
- **F4 – R1896 (#20) and U18.**
  - **Source:** p299 ends "House, Exaltation, Triplicity" with the cue word "**or**" printed at the foot of the page. But p300 opens "**and** Angles". This is the only one of the seven page joins in 296–303 where the cue word doesn't match the next page.
  - **Candidate:** asserts "AND angles" as firmly required, without noting this. U18 also says "near angles"; the source says "in … Angles".
  - **Fix:** keep "and Angles" as the page reading, record the "or" mismatch as unresolved, and change "near" to "in".
- **F5 – R1862 (Chapter XLVIII; no UNRESOLVED entry).**
  - **Source (p296):** "have no aspect to the ascendant, **or is in aspect with any Planet in an Angle**… then say, he shall be freed".
  - **Candidate:** presents this as a firm freedom configuration ("first lord aspect must exist").
  - **Problem:** that contradicts the next rule on p296–297 (R1865): "joyned to a Planet being in those angles, and that Planet be Direct, he shall not be delivered". The candidate itself (R1855/U03) treats "joined" as covering aspects, so the two rules collide.
  - **Fix:** quote the printed "or" and flag that it could be a separate option or a continuation of "no aspect … [n]or". Cross-reference R1865.

## Minor
- **F6 – R1892 (#16):** the source says "cast **not** any aspect unto them". The candidate silently reads this as positive and narrows "any aspect" to "favourable … aspects". The incomplete closing clause is correctly preserved (U17).
- **F7 – R1860:** both questions after "viz." are examples of the determinate question; the text doesn't contrast them with each other or define "absolute". U04 does keep the ambiguity open.
- **F8 – R1869:** after the new "or if he is entring combustion", it's open whether the four-angle location still applies. The candidate asserts it does.
- **F9 – R1912 (#36):** the source says "whether they be **both** Peregrine…". The precondition drops "both" (infortune and significator). U26 partly covers this.
- **F10 – softened or inflated wording (no reversals):**
  - **R1884:** "hope well" becomes "expect favourable result" (inflated).
  - **R1857:** "it's an argument he is as good as freed already" loses the hedge "an argument".
  - **R1902:** omits "let it be in what Signe it will". The 12° and 16′ thresholds themselves are correct.
  - **R1919:** omits "it seldome failes".
  - **R1895:** omits "beyond expression" and "but scornes to hurt him".
  - **R1889, R1899, R1906, R1881:** each omits a qualifying clause.
  - **R1887:** moves "good house" from the Moon to the planet it applies to.
  - **R1900:** narrows "joyned" to conjunction.
  - **R1872:** drops "&c." from the topic list.
  - **R1875:** drops "if well understood".
- **F11 – file bookkeeping:**
  - `SECTION_COVERAGE.json` record ranges for PDF332–336 are off by one against the candidate's own page locators. They should be 332: R1876–R1884; 333: R1885–R1896; 334: R1896–R1905; 335: R1905–R1915; 336: R1916–R1920.
  - `page_images` point to `evidence/`, which doesn't exist; the files are in `source_images/`.
  - "after CRYSIS" (`SECTION_COVERAGE.json`) and "XLIV" (as the physician-aphorism chapter, in R1875/U10) can't be checked from these pages.

## Checked and correct
- **Chapter XLVIII:**
  - The servant is the first house, its lord and the Moon; the master is the tenth house and its lord.
  - An exact contact "by degree and minute" means freed "easily, and in a short time".
  - A separation of "some few minutes" means as good as freed.
  - Then the Moon fallback, then the Sun fallback; the Sun's trigger correctly reads "neither … be separated".
  - Third/ninth house versus all four angles.
  - Direct versus retrograde.
  - Bodily conjunction, square or opposition from an ill planet.
- **Seventh-house intro:** the nine topics, the claimed difficulty, and "forty three" aphorisms meant for "the whole body of Astrology".
- **Aphorisms:**
  - #1: lord of the ascendant and of the hour of one nature or triplicity.
  - #3: ☋ in the tenth.
  - #7: Jupiter/Venus by trine or sextile, and in dignity.
  - #9: four signs (Cancer, Taurus, Sagittarius, Pisces).
  - #27: Saturn/Jupiter/Mars versus Venus/Mercury timing reversal.
  - #28: fixed, common, moveable signs.
  - #29: both Dragon's Head and Tail.
  - #32: Mercury in Sagittarius or Pisces.
  - #35: Moon conjunct Sun / combustion as the worst affliction.
  - #39: Part of Fortune (⊗) glyph.
  - #41: woman's death and debts kept as separate branches.
  - #42: Jupiter and Venus well dignified, with house examples.
  - #43: ☋.
- **Boundaries:** R1852, R1870–71 and R1920 all match the images.

## Errata page
There are no entries for printed pages 296–302; the nearest are "p 295 l 34 r atram" and "p 305 l 22 dele ☌". Entries for "p 330", "p 335" and "p 336" mean *printed* pages, not PDF330/335/336, and the candidate correctly doesn't apply them. The errata preface ("the literall and most observable are here met withall") supports calling the list selective. The scoping in `ERRATA_COLLATION.json` and U34 is correct.

## Limits
This rests on one scanned copy at the resolution supplied, with no other edition checked. Every unit records what the 1647 text says, not a tested or validated outcome; the candidate's "not verified" flags are appropriate.

**FINDS_ERROR**
