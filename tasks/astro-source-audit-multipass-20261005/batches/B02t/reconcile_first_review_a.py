"""Source-limited corrections from FIRST independent original-image reader A.
This does not accept, publish or claim the historical predictions work.
Must run once before reviewer B reconciliation; keeps a complete original draft.
"""
from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parent
Q=B/"independent_review"/"OPUS_A_INITIAL.md"
assert Q.is_file() and hashlib.sha256(Q.read_bytes()).hexdigest()=="e30df2b3ce3e6f1b2088919fbb04cce899f392f532fae14944f43e44d719a6fc"
BACK=B/"recovery"/"pre_first_review"
assert not (BACK/"PHASE1_RULES_DRAFT.json").exists(),"Already reconciled A"
BACK.mkdir(parents=True,exist_ok=True)
for n in ["PHASE1_RULES_DRAFT.json","UNRESOLVED.json","COUNTS.json","ERRATA_COLLATION.json",
          "SECTION_COVERAGE.json","AUDIT_REPORT.md","SOURCE_FIRST_NOTES.md","TEST_RUN_SUMMARY.json"]:
  shutil.copy2(B/n,BACK/n)
d=json.loads((B/"PHASE1_RULES_DRAFT.json").read_text())
R={r["record_number"]:r for r in d["rules"]}
assert len(R)==129 and min(R)==2138 and max(R)==2266
def fix(n,statement=None,limit=None,kind=None,pages=None):
 r=R[n]
 if statement is not None:r["source_statement"]=statement
 if limit is not None:r["exceptions_and_evidence_limits"]=[limit]
 if kind is not None:r["source_record_kind"]=kind
 if pages is not None:
  r["source_locator"]["pdf_pages"]=pages
  r["source_locator"]["printed_pages"]=[x-34 for x in pages]
  r["source_locator"]["page_images"]=[f"evidence/pdf-{x}.png" for x in pages]
def qual(n,s):
 if s not in R[n]["exceptions_and_evidence_limits"]:R[n]["exceptions_and_evidence_limits"].append(s)
def insert(kind,statement,pages,precondition,limit,after):
 assert kind not in {r["source_record_kind"] for r in R.values()},kind
 n=max(R)+1
 q=json.loads(json.dumps(R[2139]))
 q.update(id=f"LI.1647.II.L.PHASE1.R{n}",record_number=n,
    source_record_kind=kind,source_statement=statement,
    preconditions=[precondition],exceptions_and_evidence_limits=[limit],
    source_draft_part="INDEPENDENT_A_MISSING_SOURCE_UNIT",
    source_review_inserted=True,source_order_after=after)
 q["source_locator"]={"pdf_pages":pages,"printed_pages":[p-34 for p in pages],
   "page_images":[f"evidence/pdf-{p}.png" for p in pages],
   "source_statement_is_verbatim":False}
 R[n]=q
 return n
fix(2141,
 "If the lord of the Moon's domicile is in the third, or in sextile to ascendant, Lilly offers hope of finding the missing property DURING THAT ASPECT WITH THE ASCENDING DEGREE.",
 "The hope claim is limited to the aspect's operative period with the ascending degree; not an outcome guarantee.")
fix(2143,
 "The lord of the Moon's own house beholding the Moon is one source hope of return; the next printed sentence says that when these configurations are found CONTRARY, the judgment is likewise contrary.",
 "Moon's domicile lord must behold Moon; contrary aspect/configuration yields a separately adverse judgment, not an honest-finder person-type.")
fix(2145,
 "Separately from the Moon-house ruler's human/animal signs, Lilly interprets the MOON placed in a fiery or watery sign as indicating a place with fire or water.",
 "Only the Moon's own fiery or watery placement in this sentence; small-beast signs ♈ and ♑ belong to the ruler of Moon's house in a separate clause.")
fix(2146,
 "If Moon and ascendant lord occupy the same quarter and have not more than ONE SIGN between them, the missing thing is said to be IN THE HOUSE of the person who lost it.",
 "Preserve one whole Sign as original distance unit, not a generic one-to-30-degree computation; source says the loser's house, not vague proximity.")
fix(2151,
 "First-house lord separating from JUPITER, OR being in Jupiter's house, is associated with business, justice, governance, a fast/abstinency or caring for important affairs when the property was lost.",
 "These are source's hypothetical circumstances and alternatives, not verified reasons or real officials. Original printed marginal critique about Friarly astrology/Abbey/Nunnery is separate testimony.")
for n,planet,words in [(2152,"Mars","fear, sudden passion, anger, fire, enemies or quarrels"),
                        (2153,"Sun","a king/great person, hunt, pastime or authority"),
                        (2154,"Venus","drink, cards, dice, music, tavern or time with women")]:
 fix(n,f"The ascendant lord separating from {planet.upper()}, OR situated in the house of {planet}, is associated by Lilly with {words} as possible original circumstances of the loss.",
     f"The required prior separating planet or first lord in {planet}'s house is explicit; these are unconfirmed alternatives, not reliable causes.")
fix(2157,
 "For a lost living BEAST instead of things not having life, Lilly introduces separate questions whether it fled voluntarily, was driven/taken, survives or died, and if dead the supposed cause.",
 "This is a source scope change from inanimate goods to beasts; no observed death or cause established.")
fix(2161,
 "Only AFTER checking both the Moon's house lord AND the second-house lord for the specified separating relation, if neither shows separation, Lilly says the beast still remains where it was.",
 "R2162 is the second-lord fallback; no-separation conclusion requires failure of BOTH comparisons, not Moon-house lord alone.")
fix(2162,
 "If Moon's domicile lord exhibits no relevant separation, ALSO inspect the second-house lord in the SAME manner; the latter is the next prescribed check BEFORE calling the beast still in place.",
 "Source fallback order: lunar domicile lord -> second-house lord -> combined nonseparation inference. R2161 states the final conclusion.")
fix(2163,
 "If the Moon applies to the LORD OF THE EIGHTH HOUSE COUNTED FROM THE MOON, Lilly says the missing beast is dead.",
 "The eighth FROM Moon is not the radical eighth house; animal death is unverified historic assertion.")
fix(2164,
 "If the Moon's domicile ruler applies to the LORD OF THE EIGHTH FROM THE MOON, the beast is said to be dead OR TO DIE VERY SHORTLY.",
 "Retain from-Moon derived house and the printed soon-to-die alternative, not near-death or source-independent medical evidence.")
fix(2165,
 "When Moon and her house lord do not make the preceding contacts with the eighth FROM Moon, Lilly instructs a LAST resort using the LORD OF THE RADICAL EIGHTH HOUSE.",
 "A genuine different fallback significator; do not replace both prior Moon-derived eighth lords with radical eighth.")
fix(2167,
 "An application from ASCENDANT LORD to the alleged thief significator is one source theft claim; ALTERNATIVELY, the thief significator APPLYING to ascendant lord BY SQUARE OR OPPOSITION is another.",
 "Asymmetrical source directions: specific square/opposition is printed for thief-to-first contact, not automatically for both.")
fix(2168,
 "The source lists Moon and lords of her house, term and second, and the Part-of-Fortune-like body, in possible contacts WITH THE ALLEGED THIEF SIGNIFICATOR; it does not say Moon directly aspects every listed lord.",
 "Printed grammar is elliptical; preserve the list as candidates in the alleged thief-contact test and retain ambiguity rather than inventing extra Moon aspects.")
fix(2169,
 "Absence of theft contacts suggests no theft, EXCEPT that an INFORTUNE IN ASCENDANT OR SECOND, or the Moon-house/term lord, Part of Fortune OR ITS OWN LORD unfortunate, are explicitly said to signify LOSS/LOSING.",
 "Author's negative conclusion has exceptions and can still mean LOSING (not independently proven theft); preserve Part-of-Fortune lord.")
fix(2172,
 "Moon's domicile ruler separating from sixth/eighth/twelfth lord and then applying to the FIRST HOUSE LORD OR THE DEGREE/CUSP OF SECOND is an alleged favourable sign.",
 "The print does not name an application to second-house RULER here; do not insert it as a third option.")
fix(2173,
 "If the Moon is afflicted by rulers of sixth/eighth/twelfth, particularly when an infortune beholds her under the named configuration, Lilly suspects goods retained by a harmful person.",
 "The especially-if infortune aspect qualifies intensity; allegations of dishonesty have no real evidentiary basis.")
fix(2174,
 "Moon's favourable relation to Jupiter or Venus suggests an HONEST FINDER WHO WILL RESTORE GOODS; the printed conditional may also attach fortunate Jupiter/Venus aspecting the ascendant or Moon applying to ascendant to this helpful-returner branch.",
 "Preserve the source's strong WILL wording as AUTHORIAL claim. Attachment of the next if clause is ambiguous and is not proof of actual honesty.")
fix(2175,
 "MOON IN THE ASCENDANT is specifically said to signify that the lost thing is RESTORED WITH TROUBLE OR PAIN.",
 "Do not attach the trouble/pain outcome only to Jupiter/Venus aspect or Moon applying to ascendant; source has Moon IN first.")
fix(2179,
 "If the relevant lunar house lord is in Cancer, Scorpio or Pisces, Lilly suggests wells/water; if Moon occupies the LAST FACE of Capricorn, he suggests ships, BUT ONLY WHEN goods went missing near a harbour.",
 "Sign glyphs ♋ ♏ ♓ and last-face ♑ are source-explicit; the antecedent house-lord/Moon subject is potentially unclear. Harbour is a precondition not a guaranteed location.")
fix(2180,
 "Moon in a fiery sign is read as near fire. In a separate clause, Moon or Moon-house ruler in MOVABLE sign signifies new-PEOPLED place, new houses, hills or LEVEL/NEWLY BROKEN-UP ground.",
 "Do not reduce 'broken up/newly peopled' to a validated geographical fact.")
fix(2181,
 "Within the relevant quarter, Moon/ascendant-lord separation under the source's degree threshold is taken to indicate THE MISSING THING near its owner, with greater separation implying farther.",
 "Source wording refers to the lost thing, not necessarily a living beast. Competing quarter schemes remain unverified.")
fix(2183,
 "For a missing LIVING beast, the MOON OR HER DOMICILE LORD applying to the radical eighth lord OR TO THE EIGHTH FROM THE MOON is claimed to signify it is dead OR WILL DIE SHORTLY.",
 "Four printed candidate contact routes must not be compressed into one. This is not an inanimate object's 'death' or modern animal prognosis.")
fix(2184,
 "MOON in ascendant, OR Moon in TRINE to the lord of ascendant, OR Moon in TRINE to the SUN, is offered as a favourable recovery reading.",
 "The Sun glyph is readable on PDF358, not a speculative unidentified planet.")
fix(2185,
 "Second-house lord in ninth or tenth indicates missing goods may be in the querent's house or with a familiar friend, without establishing a thief.",
 "No positive independent evidence that any particular acquaintance possesses the goods; separate the second lord in 11th/12th far-away clause.")
fix(2186,
 "SUN in ascendant is interpreted as finding lost goods, EXCEPT when the original source says SUN in LIBRA ♎ or AQUARIUS ♒.",
 "These two zodiac exception glyphs are legible; historical source claim only.")
fix(2191,
 "Moon in common signs points to rushy grounds; Moon angular to CLOSES/GROUNDS, succedent to nearby closes at owner's RIGHT HAND, and cadent to COMMON FIELDS.",
 "The word common in common fields is source-explicit; placements are alternatives with distinct labels.")
fix(2192,
 "Moon in CANCER ♋ is read as a den or water-beast place or little rivulet; AQUARIUS ♒ or PISCES ♓ as watery/fishing places or near fishponds; Moon in LAST MOIETY OF CAPRICORN ♑ as ships, wood or a wood-yard.",
 "Do not add generic 'other watery signs'. The p323 last-FACE versus p324 last-MOIETY Capricorn wording is a visible cross-page discrepancy.")
fix(2193,
 "Fiery Moon sign suggests former/current fire; airy signs many windows, garrets or open places; earthly signs mud/clay or earthen walls, separately labelled 'This concerns Goods immovable' in printed marginal text.",
 "A star-marked sentence following concerns beasts strayed, not all immutable goods. Elemental symbolism is not observed navigation.")
fix(2194,
 "Moon OR lord of her own domicile in MOVABLE signs indicates new people, recently built houses, hills or newly broken-up LEVEL ground; the printed star note says the linked part has relation to BEASTS STRAYED.",
 "Do not omit source margin switch from immovable goods to beasts; no identified real site.")
fix(2195,
 "Moon in FIXED sign is interpreted as plain country/champion; Moon in COMMON sign as place of much water, according to whether the thing lost was movable or live.",
 "Printed marginal context concerns beasts strayed for part of the passage; the earlier source also uses fixed signs to mean low hiding places, a retained disagreement.")
fix(2197,
 "If the relevant significator falls in a common sign GEMINI ♊, VIRGO ♍, SAGITTARIUS ♐ OR PISCES ♓, inanimate 'dead things' such as rings are said to be WITHIN HOUSE, while living beasts/cattle are assigned watery ditches, rushes, pits or a market-place.",
 "All four original zodiac glyphs are legible. Source explicitly separates dead things from quick/living things.")
fix(2199,
 "Movable signs are read as HIGH places, ceilings or roofs; watery signs as IN WATER OR UNDER THE EARTH, pavement or foundations.",
 "Do not convert the watery rule to merely 'under water'. These are source-place conjectures.")
fix(2200,
 "Sixth-house lord unfortunate through Saturn or Mars is interpreted as beasts lost or cattle driven away or stolen, CHIEFLY IF the sixth lord is CADENT.",
 "Cadency strengthens rather than is an unconditional requirement; no actual evidence of theft.")
fix(2201,
 "Any planet separating from Moon's house lord or second-house lord is treated as beasts taken, driven away OR SOLD; absence of both separations suggests beasts not far away.",
 "Preserve from/to direction, alternatives sold/driven away and no-separation fallback.")
fix(2202,
 "Moon applying to LORD OF EIGHTH OR TO EIGHTH HOUSE, or Moon-house lord applying to eighth, is said to imply beast death. Another branch puts beast's significator IN EIGHTH AND SQUARE TO AN INFORTUNE IN FOURTH.",
 "Moon application to eighth HOUSE is an independent alternative. 'In fourth' modifies the ill planet. Apparent geometry tension is source uncertainty, not to be repaired.")
fix(2203,
 "Sixth/twelfth lord in ninth or tenth supposedly puts strayed cattle with a JUSTICE OR OFFICER, under LOCK or ordered to be kept safe.",
 "Retain custody alternatives; not real detention evidence.")
fix(2204,
 "FOR THE MOST PART, the lord of TWELFTH OR SIXTH IN TWELFTH OR SIXTH indicates cattle KEPT CLOSE in an enclosure.",
 "Do not limit to each lord's own respective house; printed 'for the most part' makes it a hedged reading.")
fix(2205,
 "Sixth-house lord fortunate by Jupiter or Venus, AND found in the SECOND, FIFTH OR ELEVENTH houses, gives Lilly's prediction that cattle shall be recovered.",
 "FIFTH, not sixth; source uses ambiguous 'they be found' for the beneficiary/animal placement. Conditional conjunction and authorial scope retained.")
fix(2207,
 "Sixth OR twelfth lord IN TRINE △ TO SUN ☉ OUT OF ANGLES is separately said to favour finding cattle.",
 "The printed aspect is a trine, NOT a sextile; both sixth/twelfth house lords named.",
 "recovered_beast_trine_sun")
d["status"]="CORRECTED_AFTER_INDEPENDENT_A_SOURCE_ONLY_NOT_ACCEPTED"
(B/"PHASE1_RULES_DRAFT.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
a=[]
def add(kind,s,p,pre,lim,after):
 n=insert(kind,s,p,pre,lim,after);a.append(n);return n
add("moon_house_lord_human_small_beast",
 "MOON'S HOUSE LORD in a HUMAN sign points to a place frequented by people, while that lord in small-beast signs ARIES ♈ or CAPRICORN ♑ points to small-animal locations.",
 [354],"Moon domicile lord (not Moon) occupies the sign type under discussion.",
 "Original glyphs and actual location unverified.",2145)
add("moon_house_lord_contrary",
 "If the Moon-house-lord aspects/constellations named for return are FOUND CONTRARY, Lilly says judge the OPPOSITE instead of hopeful return.",
 [354],"Those immediately preceding configurations fail or reverse.","Negative branch is not automatic proof someone stole property.",2143)
add("fortune_would_fain_restore",
 "Moon fortunate by Jupiter or Venus is said to mean a holder who WOULD FAIN RESTORE the thing.",
 [354],"Moon is positively configured to one or both Fortunes.","Desire to restore is distinguished from actual action; no verified owner.",2143)
add("fortune_asc_will_restore",
 "If THAT Fortune applies to the ascendant, Lilly says a faithful person WILL RESTORE the missing thing.",
 [354],"A Fortune aspecting Moon must apply further to ascendant as prescribed.","Source-based claimed completion is not empirically verified.",2143)
add("moon_asc_east",
 "Moon in ASCENDANT under the p320 missing-goods place heading indicates location to the EAST of the owner.",
 [354],"Moon physically in first house; compare distinct Moon house-quarter rules.",
 "Do not apply universally to a different animal/fugitive question.",2144)
add("beast_repeat_separation_nonstolen",
 "The printed 'Not stolne' continued clause on PDF356–357 repeats that Moon-house lord SEPARATING from another implies self-straying, the reverse implies another driving/taking it, and a parallel SECOND LORD check with neither gives that it ABIDETH STILL, not stolen.",
 [356,357],"Keep the lunar-house-lord/second-lord and both separation directions.",
 "This is a later restatement/qualification of earlier beast rule, not an independently witnessed case.",2169)
add("planet_in_asc_thief_transfer",
 "If ANY PLANET in ASCENDANT gives its power to the presumed thief significator, OR the latter to it by SQUARE OR OPPOSITION, Lilly offers a separate alleged theft testimony.",
 [356],"An actual occupant of ascendant and specified directed transfer/aspect.",
 "Not a generic theft diagnosis or evidence any person stole the goods.",2168)
add("moon_applies_to_own_dispositor_good",
 "Moon in ASPECT to HER DISPOSITOR is separately called a GOOD return/recovery condition.",
 [357],"Moon must regard its own house ruler.","One historical source rule with no observed return.",2170)
add("moon_recovery_otherwise_not",
 "After named beneficial Moon applications to owner/goods lords or their relevant degrees, the printed passage gives an OTHERWISE NOT outcome.",
 [357],"Those listed Moon application/house conjunction conditions absent.",
 "Source's no-recovery branch cannot be silently dropped, nor turned into certain impossibility.",2170)
add("second_lord_eleven_twelve_far",
 "SECOND LORD in ELEVENTH or TWELFTH is interpreted as the missing thing FAR OFF.",
 [358],"Second-house lord specifically occupies 11th or 12th house.",
 "Different from second lord ninth/tenth near-owner clause; geographical inference unverified.",2185)
add("same_first_and_hour_lord_impounded",
 "If ASCENDANT LORD and LORD OF THE HOUR are ONE AND THE SAME PLANET, Lilly treats missing cattle as truly IN THE POUND.",
 [358],"Identical planet holds ascendant lord and hour lord roles.",
 "Applies to strayed beasts in pound/enclosure context, not owner money.",2189)
add("moon_watery_place",
 "Moon IN WATERY SIGNS is read as a place with WATER or near waters.",
 [358],"Moon (not its domicile ruler) occupies a watery sign in indicated passage.",
 "Part of old place classification, not a real site observation.",2193)
for kind,page,after,desc in [
 ("place_where_missing_heading",354,2144,"Printed heading 'The place where the thing is that is lost' introduces directions and place signatures."),
 ("whether_beast_alive_heading",356,2162,"Printed heading 'Whether it be alive' introduces Moon/eighth-derived death comparisons."),
 ("whether_missing_stolen_or_fled_heading",356,2165,"Printed heading 'Whether the thing missing be stolne, or fled of itselfe' opens a non-cattle-only theft discriminant."),
 ("that_beasts_lost_heading",359,2199,"Printed heading 'That the Beasts are lost' begins sixth-lord unfortunate clause."),
 ("dead_or_alive_beast_heading",359,2201,"Printed heading 'Dead or alive' introduces Moon/eighth death interpretations."),
 ("in_pound_or_not_heading",359,2202,"Printed heading 'In Pound or not' introduces custody/justice and sixth/twelfth lord judgments."),
 ("cattle_found_again_heading",359,2204,"Printed heading 'That the Cattle shall be found againe' introduces fortunate sixth-lord, lunar-term and sun-trine recovery claims.")]:
 add(kind,desc,[page],"Structural printed section boundary, before the following rules.","No independent animal, theft or lost-goods observation.",after)
d["rules"]=list(R.values())
d["record_count"]=len(R)
d["provisional_end"]=f"R{max(R)}"
(B/"PHASE1_RULES_DRAFT.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"window":"A","record_updates":"source-constrained","new_units":len(a),"new_total":len(d["rules"]),"last":max(R),
 "review_sha256":hashlib.sha256(Q.read_bytes()).hexdigest()}))
