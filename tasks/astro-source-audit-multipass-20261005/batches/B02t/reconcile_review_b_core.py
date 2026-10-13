"""Apply high-material original-source errors from fresh reviewer B once.
Existing ID continuity is preserved; no accepted index is edited.
"""
from pathlib import Path
import hashlib,json,shutil
B=Path(__file__).resolve().parent
report=B/"independent_review/OPUS_B_INITIAL.md"
assert hashlib.sha256(report.read_bytes()).hexdigest()=="20de3a61ac25b299d7de909710c05b10201884497e54e260c5b80487635fa455"
backup=B/"recovery"/"before_first_review_b"
assert not (backup/"PHASE1_RULES_DRAFT.json").exists(),"Already repaired B; inspect before trying again"
backup.mkdir(parents=True,exist_ok=True)
for n in ("PHASE1_RULES_DRAFT.json","COUNTS.json","UNRESOLVED.json","ERRATA_COLLATION.json",
          "AUDIT_REPORT.md","SECTION_COVERAGE.json","TEST_RUN_SUMMARY.json"):
 shutil.copy2(B/n,backup/n)
p=B/"PHASE1_RULES_DRAFT.json"
D=json.loads(p.read_text())
assert D["record_count"]==148 and len(D["rules"])==148
R={q["record_number"]:q for q in D["rules"]}
def fix(n,s,limit=None,pages=None,kind=None):
 x=R[n];x["source_statement"]=s
 if limit:x["exceptions_and_evidence_limits"]=[limit]
 if kind:x["source_record_kind"]=kind
 if pages:
  x["source_locator"]["pdf_pages"]=pages
  x["source_locator"]["printed_pages"]=[p-34 for p in pages]
  x["source_locator"]["page_images"]=[f"evidence/pdf-{p}.png" for p in pages]
def append(n,s):
 if s not in R[n]["exceptions_and_evidence_limits"]:R[n]["exceptions_and_evidence_limits"].append(s)
CORRECTIONS={
2233:("In 'Whether the Fugitive shall be taken', the QUERENT is signified by the ASCENDANT, its LORD and SUN; the FUGITIVE OR THING ASKED FOR by SEVENTH HOUSE and its LORD.",
       "Moon is the FUGITIVE's natural significatrix under a separate later heading; not in original querent list."),
2248:("MOON SEPARATING FROM ASCENDANT LORD and IMMEDIATELY JOINING SEVENTH LORD or SEVENTH HOUSE is said to produce NEWS of the fugitive.",
       "This first-to-seventh moon motion means NEWS, not the inverse seventh-to-first remorse/entreaty in R2239."),
2251:("SEVENTH LORD BEHOLDING AN INFORTUNE FROM THE SEVENTH is said to indicate fugitive found with someone TO WHOM MONEY MUST BE GIVEN before release.",
       "Original 'In-fortune' crosses physical PDF363–364. Not a FORTUNE beneficial aspect or proof of detention."),
2253:("MOON ASPECTING HER OWN HOUSE by SEXTILE OR TRINE allegedly brings fugitive RETURN in THREE DAYS; the alternate three-day NEWS clause is qualified by distance NOT TOO GREAT.",
       "Moon's OWN HOUSE, not automatically its lord. Original printed p330 l6 '[f]or' is subject to same-volume erratum 'read OR'."),
2227:("MARS ASPECTS SATURN OR the MOON IN TWELFTH by CONJUNCTION, SQUARE OR OPPOSITION: beasts supposedly killed in pound, die there or nearly starve.",
       "Mars must be the aspecting planet; no unrelated Moon–Saturn-only contact is offered."),
2226:("SATURN IN TWELFTH or FIRST when querent hears of cattle, OR MOON IN TWELFTH, ANY OF THEM UNFORTUNATE, predicts long impoundment.",
       "The qualifier 'any of them unfortunate' is essential for this branch; another Saturn four-house clause is separate."),
2225:("MOON IN TWELFTH suggests pound 'what signification soever'; an UNFORTUNATE MOON supplies another pound claim; TWELFTH LORD AND PRINCIPAL SIGNIFICATOR UNFORTUNATE suggests hidden/private custody.",
       "Three different source readings; no invented 'Moon afflicted by twelfth lord'. Scope of 'what signification soever' uncertain."),
2202:("Moon applying to LORD OF EIGHTH OR THE EIGHTH HOUSE, OR Moon-house lord applying to eighth, signifies death; beast's significator IN EIGHTH and SQUARE TO AN INFORTUNE IN FOURTH is another alleged mortality claim.",
       "Preserve eighth-house direct application, fourth-house malefic location, and unusual geometry."),
2200:("SIXTH LORD UNFORTUNATE by SATURN or MARS predicts beasts lost, driven away OR STOLEN, CHIEFLY IF the sixth lord is CADENT.",
       "Cadency intensifies but isn't a required prerequisite."),
2212:("Heading 'BEASTS STOLEN OR STRAYED' introduces a comparison of the type of GOODS, FIXED versus MOVABLE, alongside Moon-house/second-lord separation.",
       "It is the GOODS that are fixed/movable, not a zodiac-sign modality alone."),
2218:("For SIXTH LORD in AIRY signs: generally PLAIN GROUND; ANGULAR means POUND/HOUSE WESTWARD; SUCCEDENT means RIGHT HAND WESTWARD; CADENT means LEFT, GOING AWAY-WARD, straying FURTHER FROM RIGHT OWNER.",
       "Cadent clause continues PDF360–361 and has no general WEST assignment."),
2219:("For SIXTH LORD in WATERY sign: NORTH low ground; ANGULAR means CLOSE GROUND NORTH; SUCCEDENT means RIGHT HAND NORTH; CADENT means COMMON ON LEFT by WATER/MEADOWS/CATTLE WATERING.",
       "The watering/meadows detail belongs particularly to the CADENT option, not every watery sign."),
2217:("SIXTH LORD in EARTHY sign suggests DRY SOUTHERN land; if ANGULAR, in CLOSE/POUND with MUD WALL; if SUCCEDENT, ABOUT CLOSES ON RIGHT HAND OF QUERENT.",
       "CLOSES means enclosures/fields, not 'closer'; no additional cadent clause supplied."),
2216:("SIXTH LORD in FIERY sign suggests EAST, woods or burnt brush; BUT when ANGULAR the direction is replaced by CLOSES, POUND or UNDER LOCK.",
       "The original 'BUT' makes the angular branch an alternative rather than simple additive detail."),
2232:("SIXTH LORD beholding ASCENDANT LORD by SEXTILE/TRINE predicts return, SQUARE/OPPOSITION means stopped. The source also gives SIXTH LORD TO MOON OR MOON'S HOUSE LORD: good aspects mean had again; hard aspects mean stopped in some VILLAGE OR TOWN.",
       "Preserve both first-lord target and Moon/lunar-lord alternatives."),
2230:("ASCENDANT LORD in TWELFTH means cattle remain SICK AND ILL in the POUND EVEN IF otherwise good.",
       "Different from eighth-house probable death or retrograde stronger death readings."),
2231:("ASCENDANT LORD in EIGHTH makes it PROBABLE cattle die in pound; a PRINCIPAL SIGNIFICATOR RETROGRADE is another branch saying they DIE IN POUND.",
       "Preserve the uncertainty qualifier for eighth placement and separately stated retrograde branch."),
2197:("Common signs GEMINI, VIRGO, SAGITTARIUS, PISCES indicate INANIMATE/DEAD THINGS such as rings within HOUSE; LIVING beasts suggest watery grounds, pits, rushes or MARKETPLACE.",
       "All four sign glyphs legible in original. Do not interchange dead goods with livestock."),
2250:("Moon JOINED TO INFORTUNES SATURN, MARS OR DRAGON TAIL, OR A RETROGRADE PLANET suggests fugitive eventually comes again AFTER MISERY.",
       "Dragon Tail printed explicit, 'joined to' not a made-up NEXT application."),
2236:("Moon is the fugitive's NATURAL SIGNIFICATRIX; MOON IN ASCENDANT, OR MOON APPLYING to ASCENDANT LORD with GOOD aspect, is used to claim the person returns or is hindered until return.",
       "The aspect is applying; shared outcome also covers R2237."),
2237:("SEVENTH LORD OR MOON SEPARATING from FORTUNES and then immediately CONJOINING INFORTUNES also predicts fugitive RETURN/RECOVERY or SO HINDERED that return follows.",
       "This is a third source condition with shared outcome, not automatically CAPTURE."),
2242:("SEVENTH LORD joined to INFORTUNE in ANGLE predicts taken UPON GOOD SEARCH; if BOTH are NOT in an ANGLE, source says DETAINED BUT NOT IMPRISONED.",
       "Keep 'upon good search' and both-not-angle condition, not invented arrest in all positions."),
2204:("FOR THE MOST PART, sixth OR twelfth lord IN TWELFTH OR SIXTH predicts beasts KEPT CLOSE.",
       "Either lord in either printed house, source hedge preserved."),
2201:("Another planet SEPARATING FROM lunar house lord OR second lord indicates beast DRIVEN AWAY OR SOLD; if none of these separations, it is NOT FAR.",
       "Not only stolen: sold is an alternative, 'none' scope may cover adjacent source options."),
2203:("SIXTH/TWELFTH LORD in NINTH OR TENTH allegedly places cattle with JUSTICE/OFFICER, under LOCK or ordered to be KEPT SAFE.",
       "These are conditional 1647 custodial claims, no actual officer or animal."),
2215:("SIXTH LORD ANGULAR suggests SMALL-GROWTH animals in CLOSES/POUNDS/HOUSES; SUCCEDENT nearby PASTURE; CADENT in COMMON GOING AWAY.",
       "Keep small-growth, common and house-dependent alternatives."),
2224:("MOON-TERM LORD FIXED indicates plain land NEWLY TAKEN IN/near new building; MOVABLE new hills/land; COMMON wet marshy ditches and pits.",
       "Moon term lord not merely Moon, distinct from sixth lord terrain."),
2238:("MOON INCREASING IN LIGHT AND NUMBER means LONG SEARCH; decreasing indicates soon found with little labour.",
       "Both printed descriptors retained; historical timing only."),
2243:("ASCENDANT LORD beholding INFORTUNE affecting fugitive indicates someone who OWES THE FUGITIVE MONEY OR DEMANDS MONEY for release.",
       "Owed money and extorted money are different hypotheses; no factual allegation established."),
2249:("SEVENTH LORD COMBUST is interpreted as fugitive TAKEN OR FOUND, 'VOLENS NOLENS', whether willing or not.",
       "The original does not prove consent or lack of consent in a real case."),
2256:("For every degree in a MOVABLE sign, Lilly assigns SEVENTEEN HOUSES OR FURLONGS AT DISCRETION to presumed distance.",
       "Not a measured physical distance; 'at discretion' source hedge."),
2254:("The 'DISTANCE' subsection gives degrees between SEVENTH LORD and HOUR LORD as supposed miles for FUGITIVE OR THING LOST.",
       "This is the inferior first method compared with R2255."),
2255:("Lilly says the SEVENTH-LORD/HOUR-LORD distance method is LESS PERFECT than MOON-to-SIGNIFICATOR distance by aspect and signs, whether for FUGITIVE OR THING LOST.",
       "Method comparison is authorial, not tested."),
2258:("For each degree in a FIXED sign source assigns ONE FURLONG OR HOUSE to presumed distance of FUGITIVE OR THING LOST.",
       "Historical units and setting affect application."),
2259:("After historical sign-degree calculations the author qualifies location by TOWN VERSUS FIELDS and whether FUGITIVE OR THING LOST is inquired of.",
       "No GPS or precise modern distance inferred."),
2252:("MOON SEPARATING FROM JUPITER OR VENUS predicts quick return of a FUGITIVE OR a THING LOST suddenly FOUND.",
       "These are alternative subject matter, not separate successful cases."),
2234:("ASCENDANT LORD applying by CONJUNCTION/SEXTILE/TRINE to SEVENTH LORD or occupying SEVENTH is said to recover the THING LOST OR FUGITIVE.",
       "Different categories, one historical rule."),
2239:("MOON SEPARATING FROM SEVENTH LORD then joining ASCENDANT OR LORD THEREOF indicates fugitive feels SORRY and sends an intermediary to ENTREAT return.",
       "Reverse of R2248's first-to-seventh source NEWS rule."),
2229:("ASCENDANT LORD in MOVABLE SIGN and THIRD/NINTH/TENTH is said to show cattle escaping pound.",
       "Movable (cardinal) not the COMMON/mutable group."),
2207:("SIXTH OR TWELFTH lord TRINE SUN OUT OF ANGLES predicts recovery of cattle.",
       "Only a TRINE, no sextile.")
}
for n,(s,lim) in CORRECTIONS.items():fix(n,s,lim)
for n,pages in [(2251,[363,364]),(2218,[360,361]),(2236,[362,363]),(2237,[362,363])]:
 x=R[n];x["source_locator"].update(pdf_pages=pages,printed_pages=[p-34 for p in pages],page_images=[f"evidence/pdf-{p}.png" for p in pages])
R[2248]["source_record_kind"]="moon_first_to_seventh_news"
R[2207]["source_record_kind"]="recovered_beast_trine_sun"
R[2229]["source_record_kind"]="escape_asc_movable_houses"
append(2253,"Original volume erratum PDF888 printed p330 line6 says READ 'OR' (body is blotted 'for/or'); it changes NEWS versus explanatory relation and is held separately.")
D.update(status="CORRECTED_A_AND_B_UNACCEPTED")
p.write_text(json.dumps(D,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"corrected_original_records":len(CORRECTIONS),"source_units":len(D["rules"]),
 "original_1647_review_B_sha256":hashlib.sha256(report.read_bytes()).hexdigest()}))
