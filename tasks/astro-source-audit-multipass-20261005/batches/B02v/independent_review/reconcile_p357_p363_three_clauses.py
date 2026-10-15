"""Source-first correction of three literal clauses, without empirical promotion.

PDF391/printed357 supplies a recovery CONSEQUENT and timing qualifiers;
PDF397/printed363 uses plural significators and an ambiguous aspect subject.
Original component bytes are saved before editing.
"""
from pathlib import Path
import json, hashlib
B=Path(__file__).resolve().parents[1]
pairs=[
 ("PRODUCER_SOURCE_DRAFT_P391_392.json","recovery/producer_p391_392_pre_U56_20261014.json"),
 ("PRODUCER_SOURCE_DRAFT_P396_397.json","recovery/producer_p396_397_pre_U57_U58_20261014.json"),
]
state=[]
for src,dst in pairs:
 p=B/src;backup=B/dst
 assert not backup.exists(),"Previously applied; do not repeat: "+dst
 raw=p.read_bytes();doc=json.loads(raw)
 state.append((p,backup,raw,doc))
src1,backup1,raw1,a=state[0]
src2,backup2,raw2,b=state[1]
r1=next(x for x in a["units"] if x["local_id"]=="P391C011")
r2=next(x for x in b["units"] if x["local_id"]=="P396C038")
r3=next(x for x in b["units"] if x["local_id"]=="P396C044")
assert (r1["kind"],r2["kind"],r3["kind"])==(
 "applying_body_to_recovery_planet","knave_leaves_sign_lodging","remains_first_cadent_aspect_asc")
assert r1["pdf_pages"]==[391] and r2["pdf_pages"]==r3["pdf_pages"]==[397]
r1["kind"]="bodily_application_recovery_with_timing"
r1["source_statement"]="If the Moon or ascendant lord bodily applies to the planet denoting recovery, Lilly claims the stolen item will THEN be recovered; separate retrograde/direct application qualifiers address how soon."
r1["preconditions"]=["One of Moon or first-house lord applies bodily to the identified recovery planet, original printed p357."]
r1["exceptions_and_uncertainty"]=["The printed consequent explicitly predicts return, not timing alone; the retrograde/direct alternatives remain separate next records. No observed recovery is established."]
r2["kind"]="knave_significators_plural_change_sign"
r2["source_statement"]="Under 'Where the Knave is', the author uses plural 'the Significators' passing from one zodiac sign into another as one alternative assertion of changing lodgings; which/how many must cross is unspecified."
r2["preconditions"]=["Printed PDF397/363: 'if the Significators be going out of one Signe into another' (plural)."]
r2["exceptions_and_uncertainty"]=["Do not force a singular thief significator or assert ALL/ANY quantification absent from the sentence."]
r3["kind"]="remains_first_cadent_behold_asc_actor_unspecified"
r3["source_statement"]="Under 'He remaines', the ascendant lord is joined to a planet in a cadent house; the original additionally says 'and behold the ascendant', without unambiguously identifying which planetary subject beholds it."
r3["preconditions"]=["First-house lord joined to a planet in a cadent house; a beholding of the ascendant is also mentioned."]
r3["exceptions_and_uncertainty"]=["The aspect actor cannot be assigned uniquely to the cadent planet or first lord from the printed grammar. Consequent comes from the section heading, not an explicit following sentence."]
ledgerpath=B/"UNRESOLVED_DRAFT.json"
issues=json.loads(ledgerpath.read_text())
assert issues["retained_count"]==55 and len(issues["issues"])==55
assert not {"U56","U57","U58"}.intersection({x["id"] for x in issues["issues"]})
records=[
 ("U56","SOURCE_IMAGE_CORRECTION_RETAINED","PDF391/357 R2762 originally says bodily application yields recovery itself, with subsequent retrograde/direct timing. Producer recorded only timing; both meanings restored."),
 ("U57","SOURCE_IMAGE_CORRECTION_RETAINED","PDF397/363 R2895 says 'the Significators' in plural crossing zodiac sign, not a singular thief significator; threshold remains unstated."),
 ("U58","SOURCE_GRAMMATICAL_AMBIGUITY_RETAINED","PDF397/363 R2901 'and behold the ascendant' has no certain actor; previous producer assigned cadent planet alone, now source ambiguity explicit.")
]
for id,status,description in records:
 issues["issues"].append({"id":id,"status":status,"description":description})
issues["retained_count"]=len(issues["issues"])
for p,backup,raw,doc in state:
 backup.parent.mkdir(parents=True,exist_ok=True)
 backup.write_bytes(raw)
 p.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
ledgerpath.write_text(json.dumps(issues,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"revised":["R2762","R2895","R2901"],"issues":issues["retained_count"],"before_sha256":{p.name:hashlib.sha256(raw).hexdigest() for p,_,raw,_ in state},"accepted_new_records":0},indent=2))
