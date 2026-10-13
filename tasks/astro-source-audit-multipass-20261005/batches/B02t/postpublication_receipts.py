"""Evidence-only post-publication readback, local Downloads hashes, and closeout.

Run ONLY after both source/canonical nonforce pushes and real owner Downloads
delivery. Do not leak owner filesystem paths into the repository.
"""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
def rd(n):return json.loads((B/n).read_text())
def hs(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def call(args):return subprocess.check_output(args,text=True).strip()
assert not (B/"PUBLICATION_RECEIPT.json").exists(),"Already published receipt; inspect instead"
actual=call(["git","-C",str(ROOT),"rev-parse","HEAD"])
lines=call(["git","-C",str(ROOT),"ls-remote","--heads","origin",
 "research/six-rule-life-timing-20261001",
 "research/lilly-fugitives-missing-goods-b02t-20261013"]).splitlines()
assert len(lines)==2
assert all(line.split()[0]==actual for line in lines)
idx=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
acc=rd("ACCEPTANCE.json")
pkt=rd("PACKET_USABILITY.json")
delivery_local=rd("DELIVERY_RECEIPT.json")
manifest=rd("DELIVERABLES_MANIFEST.json")
assert acc["accepted"] and acc["chapter_L_complete"] is False
assert idx["records_count"]==acc["lilly_after_if_integrated"]
assert idx["read_numbered_chapters"][-1]==49 and idx["next"]["chapter"]=="L" and idx["next"]["pdf_page"]==364
assert idx["batches"][-1]["id"]=="B02t"
assert hs(B/"RULES.json")==acc["rules_sha256"]
assert pkt["actual_extraction"] and pkt["crc_verified"] and pkt["identical_test_identities"]
assert pkt["extracted_tests_run"]==acc["focused_documentary_tests"]
assert delivery_local["all_destination_hashes_match_exact_published_manifest"]
assert len(manifest["files"])==len(delivery_local["files"])==3
downloads=Path(call(["xdg-user-dir","DOWNLOAD"]))
assert downloads.is_dir()
files=[]
for v in manifest["files"]:
 p=downloads/v["filename"]
 assert p.is_file() and p.stat().st_size==v["bytes"] and hs(p)==v["sha256"]
 files.append({**v,"verified_on_owner_downloads":True})
pub={
 "batch":"B02t","phase":"1_OF_CHAPTER_L",
 "repository":"u-dont-existDOTcom/humandesign",
 "canonical_branch":"research/six-rule-life-timing-20261001",
 "source_branch":"research/lilly-fugitives-missing-goods-b02t-20261013",
 "published_content_head":actual,
 "nonforce_fastforward_verified_by_two_remote_heads":True,
 "canonical_index_lilly":idx["records_count"],"retained_ptolemy":1066,
 "combined":idx["records_count"]+1066,
 "new_reference_only_units":acc["new_documentary_units"],
 "original_volume_sha256":acc["source_pdf_full_sha256"],
 "first_phase_original_pages":[353,364],
 "original_images_replayed":acc["source_replay_original_images"],
 "focused_distinct_documentary_tests":acc["focused_documentary_tests"],
 "zip_payload_hashes_verified":pkt["payload_hashes_verified"],
 "zip_actual_extraction":True,"zip_crc_verified":True,
 "zip_replayed_tests":pkt["extracted_tests_run"],
 "original_first_pass_review_windows":2,
 "post_correction_reader_windows":2,
 "none_of_reviews_are_human_prospective_predictive_tests":True,
 "new_independently_verified_cases":0,
 "whole_chapter_L_complete":False,
 "next_source":"PDF364 below Of a Thief and Theft; continue L until PDF400 above LI",
 "unresolved_source_uncertainty":acc["original_uncertainties_retained"],
 "owner_downloads_sha256_verified":True,
 "verified_archive_sha256":pkt["sha256"]}
(B/"PUBLICATION_RECEIPT.json").write_text(json.dumps(pub,indent=2)+"\n")
(B/"DELIVERY_RECEIPT.json").write_text(json.dumps({
 "batch":"B02t","destination":"OS Downloads (xdg-user-dir), path intentionally omitted",
 "files":files,"all_destination_hashes_match_exact_published_manifest":True,
 "replayed_extracted_documentary_tests":pkt["extracted_tests_run"],
 "public_safe_no_owner_absolute_paths":True,
 "not_clinical_or_predictive_validation":True},indent=2)+"\n")
close=(
 "# Chapter L Phase1 historical source batch — published closeout\n\n"
 f"**Accepted documentary source-only**, not a predictive or clinical claim. Original "
 f"William Lilly 1647 PDF353/printed319 BELOW Chapter XLIX divider to PDF364/printed330 "
 f"ABOVE the independent heading *Of a Thief and Theft*. "
 f"{acc['new_documentary_units']} historic source units R2138–{acc['last_id']}, "
 f"new cumulative Lilly **{idx['records_count']}**, retained Ptolemy **1,066**, "
 f"combined **{idx['records_count']+1066}**. Whole Chapter L **INCOMPLETE** "
 f"until original PDF400/printed366 ABOVE Chapter LI divider. "
 f"Two original-image-first reviews and two post-correction source-readback windows "
 f"are documented with provenance and source-specific uncertainty. "
 f"{acc['original_uncertainties_retained']} unresolved source limits retained. "
 f"Original entire 1647 scan SHA256 {acc['source_pdf_full_sha256']}. "
 f"{acc['source_replay_original_images']} original PNG witnesses re-rendered/pixel verified. "
 f"{acc['focused_documentary_tests']} focused regression tests passed; the frozen archive "
 f"passed CRC, manifest bytes/hash checks, actual extraction and all tests replayed. "
 f"Nonforce GitHub source/canonical branches verified at content commit {actual}. "
 f"All three file copies in OS Downloads have exact SHA256 matches. "
 f"No witnessed human/animal outcomes, clinical findings, theft proof, frozen forecast, "
 f"or runtime model promotion. Next: same original PDF364 BELOW Of a Thief and Theft; "
 f"continue through PDF400 above LI. Next source ID R{idx['records_count']+1} "
 f"after checking live source index. Multi-author historical study OPEN.\n")
(B/"PUBLISHED_CLOSEOUT.md").write_text(close)
state=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02t_PHASE1.md"
s=state.read_text()
assert "Post-publication verified" not in s
state.write_text(s+f"\n**Post-publication verified:** Original source-only ZIP, report and continuation "
 "were delivered into owner OS Downloads and SHA-256 checked; both GitHub branch heads "
 f"and remote source inventory read back as accepted at {actual}. "
 "Publication and delivery receipts in B02t/. The remaining Chapter L source is OPEN.\n")
print(json.dumps({"verified_lilly":idx["records_count"],
 "delivered_files":len(files),"verified_git_refs":2,"archive_replay":pkt["extracted_tests_run"],
 "all_chapter_L_complete":False}))
