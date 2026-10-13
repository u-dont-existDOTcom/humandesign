"""After canonical push, verify both GitHub heads + source data and owner Downloads.

Do NOT change accepted ZIP, report or handoff bytes.
"""
from pathlib import Path
import json,hashlib,subprocess,shutil
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
OUT=B.parent/"deliverables"
ORIGINAL_ACCEPTED_COMMIT="fcb1f525ba32ff344a68be102abb3985c92298e0"
def rd(n):return json.loads((B/n).read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):return subprocess.check_output(args,text=True).strip()
manifest=rd("DELIVERABLES_MANIFEST.json")
accept=rd("ACCEPTANCE.json")
packet=rd("PACKET_USABILITY.json")
state=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert len(manifest["files"])==3
assert accept["accepted"] and accept["new_documentary_units"]==267
assert packet["actual_extraction"] and packet["payload_hashes_verified"]==110
assert packet["extracted_tests_run"]==314
assert state["records_count"]==2572 and state["next"]["chapter"]=="L"
assert state["next"]["pdf_page"]==381
assert not accept["chapter_L_complete"]
remote=run(["git","-C",str(ROOT),"ls-remote","--heads","origin",
            "research/lilly-thief-and-goods-b02u-20261013",
            "research/six-rule-life-timing-20261001"])
rows=[line.split() for line in remote.splitlines() if line.strip()]
assert len(rows)==2 and all(q[0]==ORIGINAL_ACCEPTED_COMMIT for q in rows),rows
assert run(["git","-C",str(ROOT),"rev-parse","HEAD"])==ORIGINAL_ACCEPTED_COMMIT
directory=Path(run(["xdg-user-dir","DOWNLOAD"]))
assert directory.is_dir() and directory.is_absolute()
for entry in manifest["files"]:
    src=OUT/entry["filename"];dst=directory/entry["filename"]
    assert src.is_file() and src.stat().st_size==entry["bytes"] and H(src)==entry["sha256"]
    if dst.exists():
        assert dst.is_file() and dst.stat().st_size==entry["bytes"] and H(dst)==entry["sha256"],"Nonmatching existing owner file: "+str(dst)
    else:
        shutil.copy2(src,dst)
    assert dst.is_file() and dst.stat().st_size==entry["bytes"] and H(dst)==entry["sha256"]
d={
 "batch":"B02u","destination":"Owner OS-designated Downloads, exact destination SHA-256 verified",
 "actual_destination_hashes_match_published_manifest":True,
 "files":[{**entry,"exact_owner_downloads_hash_verified":True} for entry in manifest["files"]],
 "archive_sha256":packet["sha256"],
 "extracted_documentary_tests_replayed":314,
 "owner_absolute_path_intentionally_omitted":True,
 "no_clinical_criminal_or_predictive_validation":True}
assert not (B/"DELIVERY_RECEIPT.json").exists()
(B/"DELIVERY_RECEIPT.json").write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
pub={
 "batch":"B02u",
 "canonical_repository":"u-dont-existDOTcom/humandesign",
 "canonical_branch":"research/six-rule-life-timing-20261001",
 "source_branch":"research/lilly-thief-and-goods-b02u-20261013",
 "source_accepted_content_commit":ORIGINAL_ACCEPTED_COMMIT,
 "nonforce_both_remote_heads_checked":True,
 "exact_remote_heads":[q[0] for q in rows],
 "accepted_documentary_records_added":267,
 "cumulative_lilly":2572,"retained_ptolemy":1066,"combined":3638,
 "chapter_l_complete":False,
 "original_1647_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "original_page_images_verified":20,
 "independent_source_image_first_review_windows":5,
 "initial_material_errors_detected_and_repaired":True,
 "final_blind_after_controller_repairs":False,
 "uncertainties_retained":119,
 "original_tables_diplomatic_cell_completeness":False,
 "focused_and_extracted_source_tests":314,
 "archive_payload_file_count":110,
 "owner_downloads_files_exact_hashes_verified":3,
 "historical_documentary_only":True,
 "independently_validated_thieves_or_crimes":0,
 "empirically_validated_predictions":0
}
assert not (B/"PUBLICATION_RECEIPT.json").exists()
(B/"PUBLICATION_RECEIPT.json").write_text(json.dumps(pub,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"published_content_head":ORIGINAL_ACCEPTED_COMMIT,
 "lilly":2572,"combined":3638,"files_delivered":3,
 "actual_SHA256_matches":True,"archive_replay_tests":314,
 "chapter_L_complete":False,
 "owner_download_directory":str(directory)}))
