"""Second fresh source window A, source-bound corrections; no admission/promotion."""
import json,shutil,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
raw=Path.home()/"ai-source-review/b02t-phase1-recheck-a-20261013/review.stdout"
assert raw.exists()
snap=B/"recovery/before_second_fresh_A"
assert not (snap/"PHASE1_RULES_DRAFT.json").exists(),"Already ran"
snap.mkdir(parents=True,exist_ok=True)
for f in ("PHASE1_RULES_DRAFT.json","ERRATA_COLLATION.json","UNRESOLVED.json"):
 shutil.copy2(B/f,snap/f)
d=json.loads((B/"PHASE1_RULES_DRAFT.json").read_text());rs={x["record_number"]:x for x in d["rules"]}
assert len(rs)==162 and sorted(rs)==list(range(2138,2300))
def fix(n,s=None,limit=None):
 r=rs[n]
 if s is not None:r["source_statement"]=s
 if limit:r["exceptions_and_evidence_limits"].append(limit)
fix(2139,limit="Original p320 printed margin 'This principally concerns Cattle strayed' restricts some adjoining applications; do not universalize to every inanimate missing object.")
fix(2142,"Moon-house lord separated from twelfth/eighth/sixth lord and applying to the DEGREE OF SECOND HOUSE, whatever the aspect, gives HOPE to find the thing again.", "This is hope, not assured recovery.")
fix(2146,"If Moon and ascendant lord occupy the SAME quarter, and have not more than ONE SIGN between them, Lilly places the missing thing in the loser's house OR ABOUT IT.", "One whole sign is original separation scale, not a degree-only measurement.")
fix(2147,"If Moon and first-house lord are separated MORE THAN 30 and LESS THAN 70 DEGREES, Lilly says the thing is in the owner's TOWN.", "The same-quarter premise is not expressly repeated for this sentence; treat its inheritance as unresolved.")
fix(2151,"Ascendant lord separating from JUPITER or in Jupiter's house is assigned to FASTING/ABSTINENCY, care in household government, ordering laws or some TRUST placed in a person who then carried the thing away or mislaid it.", "The printed Abbey/Nunnery marginal comment is authorial/contextual testimony, not verified venue.")
fix(2153,"Ascendant lord separating from SUN or in Sun's house is attributed to a king, hunting, recreation, master of the family OR a gentleman.","Keep master of family and gentleman separately; not just public authority.")
fix(2155,"The LORD OF THE ASCENDANT separating from MERCURY is attributed to writing, sending or dictating letters, or GOING ON A MESSAGE.", "No Mercury-house alternative is printed; preserve that asymmetry.")
fix(2157,"If a missing BEAST is queried rather than a thing without life, Lilly says the place/state significations are AS those for lifeless things, PLUS inquiry whether the animal fled on its own, another drove it away, whether it lives, and, if dead, the cause.", "Not instead of inert-goods scheme; animal adds questions and remains a separate evidence class.")
fix(2160,"Only when Moon's house lord has NOT separated from another planet, but ANOTHER planet separates from it, Lilly says someone TOOK the beast and fled away.", "Do not substitute later 'driven away' wording for this passage or omit the first nonseparation.")
fix(2161,"After neither the Moon-house lord nor second-house lord demonstrates the stated separation, Lilly judges the beast STILL IN ITS PLACE OR NEAR IT and says it has NOT fled.", "Both ruler checks must precede this conclusion.")
fix(2165,"If neither Moon nor her lord applies to the stated eighth-from-Moon targets, the source says take signification from THE LORD OF THE EIGHTH HOUSE after same manner.", "Whether this final eighth-house lord is radical or again counted from Moon is UNSPECIFIED in this printed sentence; do not assert radical.")
fix(2168,"Moon by CONJUNCTION ☌, SQUARE □ or OPPOSITION ☍ to the presumed thief signifier, OR the lord of Moon's house/term, the second lord, PART OF FORTUNE ⊗ OR ITS LORD are listed as further parties in the alleged thief-contact conditions.", "Elliptical original coordination; do not fabricate individual Moon aspects to every listed lord or omit glyphs and Part-of-Fortune lord.")
fix(2169,"If the source's named thief-contact constellations are absent Lilly says IT IS NOT STOLEN, EXCEPT an infortune in ascendant or second, or unhappy Moon-house/term ruler, Part of Fortune OR ITS LORD, ASCENDANT LORD OR SECOND LORD; these instead SIGNIFY LOSING.", "Extent of the exception and whether term means the term or its lord are unresolved; it is not real exonerating proof.")
fix(2173,"When Moon is INJURED by lord of sixth/eighth/twelfth, Lilly alleges an ill holder unwilling to yield the lost goods, CHIEFLY if the INFORTUNE regards ASCENDANT OR ASCENDANT LORD.", "The extra infortune's object is first house/its lord, NOT Moon; historical accusation uncorroborated.")
fix(2180,"Moon in Aries ♈, Leo ♌ or Sagittarius ♐ is interpreted as PLACE OF FIRE; Moon OR HER DISPOSITOR in MOVABLE signs means a place NEWLY BROKEN UP.", "Limit to PDF357 text; new-peopled/new-built/hills are a later PDF358 clause recorded under R2194.")
fix(2181,"Moon WITHIN THIRTY DEGREES of ASCENDANT LORD means missing thing WITH THE LOSER OR NEAR HIM; more than THIRTY DEGREES is FAR OFF.", "No quadrant prerequisite printed here; printed marginal scope is Strayed; both branches are untested claims.")
fix(2183,"MOON OR HER DISPOSITOR applying to LORD OF EIGHTH, OR TO EIGHTH HOUSE FROM MOON, is called DEAD OR WILL DIE SHORTLY in the printed missing-thing source context.", "Do not infer radical eighth, add a living-beast restriction not printed in this line, or call it merely near death.")
fix(2189,"LORD OF SIXTH in SIXTH OR TWELFTH is alleged to mean beasts are IN A POUND.", "Do not replace pound with administrative 'official custody' here; separate justice/officer clause appears later.")
fix(2193,"The printed 'Behold the Signe where the Moon is' paragraph, marginally 'This concerns GOODS IMMOVABLE', gives fiery signs places with current/former fire and airy signs windows, garrets/open places; a STAR on the later EARTHLY-sign Moon clause refers to 'This hath relation to BEASTS STRAYED'.", "Scope margin for goods immovable applies to heading/early paragraph; source star relates beast context to earthy clause; star's further reach uncertain.")
fix(2194,"MOON OR MOON'S HOUSE LORD in a MOVABLE sign indicates NEW PEOPLED or NEW BUILT place, HILLS, OR in some places LEVEL GROUNDS.", "Do not add newly broken-up from preceding printed page; exact star-mark scope remains unresolved.")
fix(2195,"Moon in FIXED sign is placed in PLAIN/CHAMPION COUNTRY; in COMMON sign in a place of MUCH WATER, ACCORDING TO NATURE OF PLACE WHERE THING WAS LOST OR MISSING.", "Earlier fixed-sign low/hiding classification follows on PDF359, not precedes this passage.")
fix(2202,limit="Printed 'and/or' coordination and an IMPLIED death conclusion are uncertain; do not normalize silently.")
fix(2204,limit="Printed here says 'kept close', not specifically a formal 'pound' as extra assertion.")
fix(2269,limit="Source explicitly calls the holder a 'trusty body, which keepeth the same' and 'would faine restore' rather than guaranteed actual return.")
fix(2270,"If the same FORTUNE APPLY TO ASCENDANT OR BEHOLD IT, OR THE MOON BEHOLD ASCENDANT, Lilly says a FAITHFUL person WILL RESTORE the property.", "Three printed alternatives, distinct from merely wanting to return property; old author claim.")
fix(2271,"Moon IN ASCENDANT indicates EAST under the original lost-goods place heading.", "The print says 'in the east &c.', not relative-to-owner in this sentence.")
fix(2275,limit="Return rule includes Moon applying to its own DISPOSITOR. Do not add unstated 'relevant degrees' targets.")
fix(2279,limit="Printed 'The place where the thing is that is lost' concerns location AT TIME OF THE QUESTION.")
fix(2268,limit="Duplicate explanatory echo of the 'judge the contrary' clause R2143 across several preceding constellations; preserve source sentence only once at final integration.")
e=json.loads((B/"ERRATA_COLLATION.json").read_text())
for v in e["entries"]:
 if v["printed_page"]==330:
  v.update(original_erratum="p 330 l 6 r or",replacement="or",
           body_target_proved=True,
           note="Printed p330 'for according to probability' near three-day return/news is partially blotted; same-volume erratum directs 'or'. Keep source body separate; source's 'or' changes explanation to alternative.")
(B/"ERRATA_COLLATION.json").write_text(json.dumps(e,ensure_ascii=False,indent=2)+"\n")
d["rules"]=list(rs.values())
d["status"]="SOURCE_CORRECTED_AFTER_FRESH_READBACK_A_B_PENDING"
(B/"PHASE1_RULES_DRAFT.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"reader":"A","source_units":len(rs),"source_claims_corrected":29,"erratum330":"or","accepted":False}))
