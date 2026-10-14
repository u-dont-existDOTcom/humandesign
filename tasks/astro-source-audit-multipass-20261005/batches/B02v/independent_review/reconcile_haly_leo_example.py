"""One-time source-image correction of p352-353 Haly / Leo / Venus example.

The 1647 printed original attributes this anecdote to Haly (a source Lilly
cites), NOT to Lilly's own experience. The ascending sign is Leo, NOT Libra.
Preserve exact pre-edit producer bytes; no empirical accuracy inferred.
"""
import hashlib
import json
from pathlib import Path

B=Path(__file__).resolve().parents[1]
src=B/"PRODUCER_SOURCE_DRAFT_P385_387.json"
backup=B/"recovery/producer_p385_387_before_20261014_haly_leo_source_correction.json"
assert not backup.exists(), "Previously corrected. Inspect existing backup."
original=src.read_bytes()
j=json.loads(original)
u={r["local_id"]:r for r in j["units"]}
start=u["P385C041"]
end=u["P385C042"]
assert start["pdf_pages"]==[386] and end["pdf_pages"]==[387]
assert start["kind"]=="reported_libra_venus_example_start"
assert end["kind"]=="reported_libra_venus_bed"
assert start["source_statement"]=="Lilly says he was once asked when Libra rose and Venus was in the ascendant; the result is explained on the following page."
start["kind"]="reported_haly_leo_venus_example_start"
start["source_statement"]="Lilly quotes Haly's report of a lost-object question with LEO ascending; the sentence continues on printed p353 with Venus in the ascendant."
start["preconditions"]=["Original PDF386/printed352: 'Haly saith, it was asked him one time when' plus Leo (♌) ascending; original PDF387/printed353: Venus (♀) therein."]
start["exceptions_and_uncertainty"]=["This is a quoted historical source's self-report, not an independent outcome. Leo is the printed sign glyph; Libra was an editorial misreading. Do not attribute the episode directly to Lilly."]
start["image_readback"]="Original PDF386/printed352 above catchword 'ing' and PDF387/printed353 continuation"
end["kind"]="reported_haly_leo_venus_bed"
end["source_statement"]="In the continuation of Haly's historical Leo-ascending, Venus-in-first question, Haly says the lost object lay under a bed, near a robe or covering, attributing the bed symbolism to Venus."
end["preconditions"]=["Leo (♌) rising and Venus (♀) within ascendant in the previous sentence; printed PDF386–387. The source explicitly attributes the report to Haly."]
end["exceptions_and_uncertainty"]=["No chart, dated question, or independently authenticated lost-object retrieval was supplied. Do not credit this as Lilly's personal test or evidence of success."]
end["image_readback"]="Original PDF387/printed353 starts 'ing and ♀ therein; and he saith, the thing was under a Bed'"

backup.parent.mkdir(exist_ok=True)
backup.write_bytes(original)
src.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
ledger=B/"UNRESOLVED_DRAFT.json"
l=json.loads(ledger.read_text())
assert l["retained_count"]==53
assert all(x["id"]!="U54" for x in l["issues"])
l["issues"].append({
    "id":"U54",
    "status":"SOURCE_IMAGE_CORRECTION_RETAINED",
    "description":"PDF386/printed352 and PDF387/printed353 worked lost-object report is explicitly attributed to HALY, with LEO ascending and VENUS in ascendant. P385C041/P385C042 (provisional R2674–R2675) previously misattributed to Lilly and read Leo as Libra; corrected both editorial records and froze prior producer bytes. No independent case authentication."
})
l["retained_count"]=len(l["issues"])
ledger.write_text(json.dumps(l,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"source_page_range":[386,387],"record_numbers":[2674,2675],
"old_sha256":hashlib.sha256(original).hexdigest(),"new_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),
"retained_issues":len(l["issues"]),"admitted_source_units":0},indent=2))
