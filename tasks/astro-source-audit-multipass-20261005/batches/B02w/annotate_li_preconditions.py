"""Guarded editorial decomposition of LI source-first compound conditions.

Requires source-first draft currently unannotated. Saves exact pre-edit bytes.
This does NOT certify or empirically execute horary rules.
"""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
SRC=B/"SOURCE_FIRST_CLAUSES_DRAFT.json"
BACK=B/"recovery/SOURCE_FIRST_CLAUSES_before_precondition_annotation_20261015.json"
assert not BACK.exists(),"Previously annotated; inspect source and backup."
raw=SRC.read_bytes()
doc=json.loads(raw)
assert len(doc["rows"])==42
terms={
 "contest_querent_significator_assignment":["In the opening adversary question, assign to querent: ascendant lord; Moon; and the planet FROM which Moon separated."],
 "contest_opponent_significator_assignment":["Assign to defendant: seventh house; seventh lord; and planet TO which Moon applies. Printed clause physically crosses original pages400→401."],
 "contest_strength_and_fortunes_comparison":["Consider the respective significators' angular status, strength and companion planets before the outcome comparison."],
 "contest_infortunes_first_fortunes_seventh":["Unfortunate planet(s) in ASC AND fortunate planet(s) in seventh; outcome author attributes to adversary."],
 "contest_seventh_lord_in_asc_querent_victory":["Seventh house lord in ascendant; victory is ascribed to querent."],
 "safe_return_strong_first_with_benefic":["Ascendant lord strong AND with a good planet AND well disposed; safe return authorial claim."],
 "safe_return_seventh_fortunate_even_if_first_weak":["Seventh house and its lord fortunate even when first is not; source claims eventual return WITH losses/obstacles."],
 "safe_return_moon_applying_to_benefic":["Moon applies to a good planet; Moon's own condition must also be observed."],
 "safe_return_malefics_eighth_fear":["Malefic planet(s) in eighth; adverse alternatives fear/terror/death."],
 "safe_return_saturn_vs_mars_node_injury":["Saturn category=bruises/ruins; Mars OR printed node-like glyph category=weapon wounds."],
 "war_safe_return_first_lord_good_or_good_in_asc":["First lord with a good planet OR itself good OR benefic planet in first; any one is printed as a safe-return testimony."],
 "war_sun_with_first_lord_not_go_burning":["Sun with ascendant lord at any part of the chart; source advises no departure and attributes this to burning."],
 "war_seventh_lord_benefic_first_lord_malefic_impeded_no_death":["Seventh lord with benefic AND ascendant lord with malefic; source says impediment yet no death."],
 "war_malefic_with_first_benefic_in_first_loss_wound_not_death":["Malefic with first lord AND benefic in first; source predicts loss/wounds but explicitly excludes death."],
 "war_saturn_in_first_or_with_lord_avoid_journey":["Saturn in first OR with first lord; the author advises against travel."],
 "war_malefic_first_saturn_first_wood_stone_wounds":["Malefic with first lord AND Saturn in first OR Saturn with first lord (grouping requires care); original wood/stone consequence crosses PDF401→402."],
 "war_mars_node_malefic_first_grievous_wound":["Mars OR South Node in first or with first lord; OR malefics in first or with lord. Clause contains alternative groups, not necessarily all required."],
 "war_malefic_eighth_mortality_fear":["Malefic planet in eighth; author raises death as feared outcome."],
 "war_sun_seventh_or_eighth_bad_to_go":["Sun with seventh lord OR Sun in eighth; terminal 'so of tenth and seventh' remains ambiguous."],
 "war_result_first_seventh_assignments":["First house/lord denote querent; seventh house/lord denote opposing party in this subsection."],
 "war_result_benefic_first_malefic_seventh_strong_first":["Good planets in first AND evil in seventh AND first lord well conditioned AND seventh lord ill."],
 "war_result_malefic_first_benefic_seventh_converse_loss":["Malefic with ascendant lord AND malefic in first AND seventh lord well conditioned AND benefic in seventh."],
 "war_result_both_lords_first_benefics_second_cusp":["First AND seventh lords in ascendant; benefics casting benevolent aspects to SECOND-HOUSE CUSP, on the ascendant lord's behalf."],
 "war_result_same_condition_victory_or_reconciliation":["Inherits preceding both-lords-ASC and benefic-to-second-cusp conditions; outcomes victory OR potential reconciliation."],
 "war_result_both_lords_first_benefic_first_malefic_seventh_both_loss":["Both first and seventh lords in ASC; benefics on ascendant side and malefics on seventh side; both suffer, querent better at end."],
 "war_result_seventh_lord_in_asc_actor_fortune":["Seventh lord in ASC in war-outcome subsection; 'fortune of Actors' referent unresolved."],
 "war_side_houses_querent_marginal":["Printed margin classes houses 10/11/12/1/2/3 as querent's party."],
 "war_side_houses_opponent_marginal":["Printed margin classes houses 9/8/7/6/5/4 as quesited's party."],
 "war_death_querent_eighth_ruler_disposition":["First lord in eighth OR first lord conjoined with eighth lord OR eighth lord in first."],
 "war_death_opponent_seventh_second_disposition":["Seventh lord in second OR with second lord OR second lord in seventh OR with seventh lord."]
}
seen=set()
for r in doc["rows"]:
 if r["kind"] in terms:
  assert r["preconditions"]==[],r["kind"]
  r["preconditions"]=terms[r["kind"]]
  seen.add(r["kind"])
assert seen==set(terms)
for r in doc["rows"]:
 if r["role"]=="conditional":
  assert r["preconditions"],r["kind"]
for r in doc["rows"]:
 if r["role"]=="converse":
  assert not r["preconditions"],r["kind"]
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
SRC.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"annotated_kinds":len(terms),"records":len(doc["rows"]),
"frozen_sha256":hashlib.sha256(raw).hexdigest(),
"current_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
"accepted":False},indent=2))
