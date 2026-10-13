"""Apply source-only high-severity corrections after fresh window B review."""
import json,shutil
from pathlib import Path
B=Path(__file__).resolve().parent
bk=B/"recovery/before_fresh_B"
assert not (bk/"PHASE1_RULES_DRAFT.json").exists(),"already applied"
bk.mkdir(parents=True,exist_ok=True)
shutil.copy2(B/"PHASE1_RULES_DRAFT.json",bk/"PHASE1_RULES_DRAFT.json")
D=json.loads((B/"PHASE1_RULES_DRAFT.json").read_text())
R={x["record_number"]:x for x in D["rules"]}
assert len(R)==162
def fix(n,s,lim="Original historical source only; no independent outcome evidence.",pages=None):
 x=R[n];x["source_statement"]=s;x["exceptions_and_evidence_limits"].append(lim)
 if pages:
  x["source_locator"]["pdf_pages"]=pages
  x["source_locator"]["printed_pages"]=[z-34 for z in pages]
  x["source_locator"]["page_images"]=[f"evidence/pdf-{z}.png" for z in pages]
fix(2200,"SIXTH LORD unfortunate by SATURN or MARS indicates missing beasts, CHIEFLY IF CADENT; alternatively the source says cattle DRIVEN AWAY OR STOLEN.","Cadency strengthens, not universally required. Alternative attachment of chiefly uncertain.")
fix(2202,"MOON applying to EIGHTH LORD OR EIGHTH HOUSE, or lunar-house lord applying to eighth, is alleged beast death; alternative BEAST SIGNIFICATOR IN EIGHTH AND SQUARE TO AN INFORTUNE IN FOURTH.","Source implies some outcomes without repeating them; four-house infortune prerequisite must remain.")
fix(2212,"Heading 'BEASTS STOLEN OR STRAYED' compares FIXED GOODS (stolen) with MOVABLE GOODS (departed themselves), using separation by MOON'S HOUSE LORD OR SECOND LORD.","Fixed or movable here qualifies the goods, not the zodiac signs.")
fix(2216,"SIXTH LORD in FIERY SIGN is read as EAST woods/burnt brush, BUT IF ANGULAR it gives CLOSES, POUND OR LOCK instead.","The 'but' yields a different outcome rather than additive simultaneous locations.")
fix(2217,"SIXTH LORD in EARTHY SIGN suggests SOUTH dry land; ANGULAR suggests pound/closes with mud wall; SUCCEDENT suggests enclosed fields on RIGHT HAND OF QUERENT.","Closes are enclosed fields, not a closer position.")
fix(2218,"SIXTH LORD in AIRY SIGN: PLAIN GROUND; ANGULAR means housed or pounded WEST; SUCCEDENT RIGHT WEST; CADENT LEFT AND GOING AWAY, STRAYING farther from rightful owner.","West is not explicitly attached to the cadent alternative.",[360,361])
fix(2219,"SIXTH LORD in WATERY SIGN points NORTH low ground; ANGULAR enclosed north, SUCCEDENT right north, CADENT on LEFT in COMMON near WATER/MEADOW or watering of cattle.","Water/meadow is cadent-specific.")
fix(2225,"CATTLE TO POUND: MOON IN TWELFTH signifies pound 'WHAT SIGNIFICATION SOEVER'; MOON UNFORTUNATE, or TWELFTH LORD AND PRINCIPAL SIGNIFICATOR unfortunate, likewise signifies pound or private close custody.","Printed scope of 'what signification soever' remains ambiguous.")
fix(2226,"SATURN in TWELFTH or in FIRST when querent comes to know, OR MOON IN TWELFTH, ANY OF THEM UNFORTUNATE, signifies LONG IN POUND.","Do not drop Moon or the 'unfortunate' qualification.")
fix(2227,"MARS ASPECTING SATURN OR MOON IN TWELFTH by CONJUNCTION, SQUARE OR OPPOSITION is alleged to mean beasts killed, dying or near starvation IN POUND.","Mars is the aspecting planet; not an independent Moon–Saturn branch.")
fix(2230,"ASCENDANT LORD in TWELFTH: though good, beasts remain SICK AND ILL IN POUND.","Do not convert to mere stay without illness.")
fix(2231,"ASCENDANT LORD IN EIGHTH: 'PROBABLE' beasts DIE in pound; principal SIGNIFICATOR RETROGRADE: source instead says they DIE.","Different modalities and significators, not proof of death.")
fix(2233,"Under 'WHETHER THE FUGITIVE SHALL BE TAKEN', the FIRST HOUSE, FIRST LORD AND SUN signify QUERENT; SEVENTH AND ITS LORD signify FUGITIVE OR THING ASKED FOR.","Moon is separately called fugitive's natural significatrix; not additional querent body.")
fix(2234,"FIRST LORD applying to SEVENTH LORD by CONJUNCTION, SEXTILE OR TRINE, OR first lord in seventh, signifies recovery of THINGS LOST OR FUGITIVE.","Both missing goods and fugitive are explicitly covered.")
fix(2236,"MOON NATURAL SIGNIFICATRIX OF FUGITIVE: Moon IN ASCENDANT or APPLYING to ASCENDANT LORD by GOOD ASPECT supports recovered/returning, in conjunction with the next source clause.","Moon application direction and shared outcome retained.",[362,363])
fix(2237,"SEVENTH LORD OR MOON separating from FORTUNES and IMMEDIATELY JOINING INFORTUNES is the third clause in source's RETURN/RECOVERY series.","Do not reassign this to separate capture without support.",[362,363])
fix(2242,"SEVENTH LORD JOINED TO INFORTUNE IN ANGLE: ON GOOD SEARCH fugitive TAKEN; IF BOTH NOT ANGULAR: DETAINED BUT NOT IMPRISONED.","Two alternatives, with explicit search and imprisonment qualifications.")
fix(2243,"FIRST LORD beholding infortune afflicting fugitive signifies DETAINED BY SOMEONE OWED MONEY OR SOMEONE DEMANDING MONEY BEFORE RELEASE.","Two different financial alternatives.")
fix(2248,"MOON separating from SEVENTH LORD and JOINING ASCENDANT OR FIRST LORD signals REPENTANCE AND SOMEONE SENT TO ENTREAT RETURN.","Opposite Moon separation from FIRST to SEVENTH is news, not this rule.")
fix(2250,"MOON JOINED to SATURN, MARS or DRAGON TAIL, OR to RETROGRADE PLANET, is alleged return after MISERY.","Original lists Dragon Tail expressly.")
fix(2251,"SEVENTH LORD BEHOLDING AN INFORTUNE FROM SEVENTH signifies fugitive held by someone WHO DEMANDS MONEY BEFORE RELEASE.","The word In-fortune spans PDF363–364; not benevolent Fortune.",[363,364])
fix(2252,"MOON SEPARATING FROM JUPITER OR VENUS is said to give QUICK FUGITIVE RETURN OR SUDDEN FINDING OF A LOST THING.","Both people and goods scope.")
fix(2253,"MOON ASPECTING HER OWN HOUSE by SEXTILE OR TRINE allegedly yields return in THREE DAYS OR NEWS within THREE DAYS, IF DISTANCE NOT TOO GREAT.","Original erratum p330 l6 says read OR, not for; lunar house not house ruler.")
fix(2254,"Under DISTANCE, separation of SEVENTH LORD and HOUR LORD by DEGREE gives hypothetical MILES to FUGITIVE OR LOST THING.","Alternative lunar distance calculation is preferred by author.")
D["rules"]=list(R.values());D["status"]="REVIEW_B_CORE_REPAIRED_PHASE1_UNACCEPTED"
(B/"PHASE1_RULES_DRAFT.json").write_text(json.dumps(D,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"repaired":24,"candidate_records":len(R),"source_only":True}))
