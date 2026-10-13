"""Original-image errata collation after direct visual enlarged PDF888 readback."""
import json,shutil
from pathlib import Path
B=Path(__file__).resolve().parent
P=B/"ERRATA_COLLATION.json"
backup=B/"recovery/errata_before_direct_image_readback.json"
backup.parent.mkdir(exist_ok=True)
assert not backup.exists(),"Errata already visually reconciled; inspect instead"
shutil.copy2(P,backup)
D=json.loads(P.read_text())
e=D["original_printed_errata_entries"]
assert [x["printed_page"] for x in e]==[330,335,336,336]
# The enlarged ORIGINAL 1647 image reads 'Planet', not 'Planes',
# and singular 'vertue' in both adjacent line instructions.
e[1]["read"]="Planet"
e[1]["original_source_visual"]="p 335 l ult. r Planet"
e[1]["body_target_matched"]=False
e[2]["read"]="vertue";e[2]["original_source_visual"]="p 336 l 4 r vertue"
e[3]["read"]="vertue";e[3]["original_source_visual"]="l 9 r vertue"
e.append({"printed_page":337,"line":"28","read":"for ☉ and ♂",
 "original_source_visual":"p 337 l 28 r for ☉ and ♂",
 "body_context":"printed337 original PDF371; exact replacement and nearby glyph sequence need body read",
 "body_target_matched":False,"admission":"DRAFT_COLLATION_PENDING"})
D["corrected_against_exact_original_1647_errata_raster"]=True
D["original_visual_is_not_alternate_edition"]=True
D["number_of_entries_in_this_phase_not_already_B02t"]=4
D["p330_instruction_belongs_to_prior_accepted_batch"]=True
P.write_text(json.dumps(D,indent=2,ensure_ascii=False)+"\n")
print("DIRECT_SOURCE_ERRATA_VERIFIED",len(e),"INCLUDING_PREVIOUS_BATCH_P330",True)
