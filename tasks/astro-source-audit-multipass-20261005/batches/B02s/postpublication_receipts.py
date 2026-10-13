"""Post-publication receipt: independently check two nonforce refs and actual owner Downloads.
Never modify accepted ZIP/source bytes; published historical batch is source-only.
"""
from pathlib import Path
import json,hashlib,subprocess
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
SHA="6b23d863487baef1a6c499581924464d75e10a9a"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
 p=B/name
 assert not p.exists(),("Receipt already exists; no blind overwrite",p)
 p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
def command(args):return subprocess.check_output(args,text=True).strip()
assert command(["git","-C",str(ROOT),"rev-parse","HEAD"])==SHA
remote=command(["git","-C",str(ROOT),"ls-remote","--heads","origin",
 "research/six-rule-life-timing-20261001","research/lilly-marriage-b02s-20261013"])
lines=[line.split() for line in remote.splitlines() if line.strip()]
assert len(lines)==2 and all(line[0]==SHA for line in lines),lines
index=json.loads((ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json").read_text())
assert index["records_count"]==2137 and index["next"]["chapter"]=="L"
assert index["batches"][-1]["id"]=="B02s"
a=json.loads((B/"ACCEPTANCE.json").read_text())
packet=json.loads((B/"PACKET_USABILITY.json").read_text())
m=json.loads((B/"DELIVERABLES_MANIFEST.json").read_text())
assert a["accepted"] and a["new_documentary_units"]==217
assert a["focused_source_tests"]==281 and packet["extracted_tests_run"]==281
assert packet["actual_extraction"] and packet["payload_hashes_verified"]==138
local=json.loads((B/"DELIVERY_RECEIPT.json").read_text())
assert local["all_destination_hashes_match_exact_published_manifest"]==True
assert len(local["files"])==len(m["files"])==3
owner_dir=Path(command(["xdg-user-dir","DOWNLOAD"]))
assert owner_dir.is_dir()
files=[]
for expected in m["files"]:
 filename=expected["filename"]
 dst=owner_dir/filename
 assert dst.is_file() and dst.stat().st_size==expected["bytes"] and sha(dst)==expected["sha256"]
 assert next(x for x in local["files"] if x["filename"]==filename)["hash_matched"]
 files.append({**expected,"destination_verified":True})
pub={
 "batch":"B02s","canonical_repository":"u-dont-existDOTcom/humandesign",
 "source_branch":"research/lilly-marriage-b02s-20261013",
 "canonical_research_branch":"research/six-rule-life-timing-20261001",
 "previous_canonical_head":"ca391542e44dc82a19dcb4aa505ffca212d6259c",
 "accepted_content_head":SHA,"nonforce_fast_forward_to_both_branches_verified":True,
 "canonical_record_count":2137,"retained_ptolemy":1066,"combined":3203,
 "new_source_records":217,"documentary_only":True,
 "source_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "focused_source_tests":281,"extracted_source_tests":281,
 "zip_payload_files_verified":138,
 "global_ci_unit_integration":"396 passed, 4 skipped",
 "global_ci_lint":"FAIL: 61 Ruff errors (same count seen on prior accepted research branch; no all-green claim)",
 "predictive_or_clinical_validation":False,
 "independent_initial_review_windows":2,"informed_changed_review_windows":2,
 "blind_final_after_controller_corrections":False,
 "archive_sha256":packet["sha256"],
 "source_artifact_frozen":True}
save("PUBLICATION_RECEIPT.json",pub)
delivery={
 "batch":"B02s","method":"OS-designated Downloads, actual post-publication bytes verified",
 "destination":"xdg-user-dir DOWNLOAD on owner computer",
 "actual_destination_matches_manifest":True,
 "files":files,
 "archive_actual_extraction_verified":True,
 "extracted_tests_replayed":281,
 "historical_source_only":True,
 "absolute_local_owner_paths_omitted_for_public_repo":True
}
# replace the private-path local receipt with the reviewed public-safe representation.
(B/"DELIVERY_RECEIPT.json").write_text(json.dumps(delivery,indent=2,ensure_ascii=False)+"\n")
closeout=(
 "# Lilly Chapter XLIX — accepted source audit and verified owner delivery\n\n"
 "B02s original 1647 source spans PDF336/printed302 below the divider through PDF353/printed319 "
 "above the Chapter L divider. The two initial overlapping original-page reviews and two informed "
 "changed-item reviews identified, qualified or corrected historic text interpretations, including "
 "directions of planetary application, received conjunctions, claimed intentions, reported coercion "
 "versus consent, and explicit denials of false allegations. The two informed reports retain "
 "their earlier REPAIR_REQUIRED verdicts: the final controller fixes were not checked by a fresh "
 "third blind evaluator. This is documentary fidelity research, not a successful astrology forecast.\n\n"
 "**217** new source-only reference units **R1921–R2137**. Cumulative **2,137 Lilly** plus "
 "**1,066 Ptolemy = 3,203 combined**. **68** retained source uncertainties; **zero** "
 "independently authenticated couples, prospective predictions, clinical outcomes or production promotions. "
 "281/281 distinct source regressions pass; the frozen 138-payload-file ZIP passed CRC, original "
 "bytes/manifest verification, extraction and all 281 replayed tests. Both nonforce GitHub branches "
 "were read back at content commit **"+SHA+"**. Three named deliverables are present in OS Downloads "
 "and match their published SHA-256 values; see PUBLICATION_RECEIPT.json and DELIVERY_RECEIPT.json.\n\n"
 "The whole-repository CI unit/integration step passed (396 passed, 4 skipped), but repository-wide "
 "Ruff lint still reports 61 errors; this is not an all-green CI claim. No unrelated lint repair "
 "was introduced into the historical source research batch.\n\n"
 "Next source study: Chapter L, *Of Servants fled, Beasts strayed, and things lost*, opening "
 "original PDF353 printed319 **below** divider, then PDF354 onward; next provisional record "
 "**R2138** only after reconfirming live accepted index. Multi-author historical source audit remains OPEN. "
 "The accepted ZIP retains its pre-publication checkpoint bytes; later receipts supersede delivery "
 "status without altering the ZIP itself.\n")
(B/"PUBLISHED_CLOSEOUT.md").write_text(closeout)
(B/"LESSON_DISPOSITION.md").write_text(
 "# B02s lesson disposition\n\n"
 "- Historical source wording, original-volume errata and handwritten marginalia stay separate.\n"
 "- Avoid blame inversion in claims about sexual conduct: distinguish deceived from culpable, "
 "preserve explicit denial and nonconsensual branches. These are documentary source distinctions, "
 "not validated assessments of people.\n"
 "- One printed scope-extension sentence near a chapter end requires its own unit when source "
 "completeness is the owner's outcome.\n"
 "- Maintain both independent first-pass review windows and informed follow-up provenance; "
 "do not mislabel the latter as blind evidence.\n"
 "- Existing Universal Development Architecture source-provenance rules already cover these; "
 "no new universal promotion required.\n")
state=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261013_B02s.md"
s=state.read_text()
assert "Post-publication delivery verified" not in s
state.write_text(s+"\n**Post-publication delivery verified:** Nonforce source/canonical push, accepted content "
 +SHA+". 138-file ZIP extraction and 281 tests replayed, all three owner Downloads files exact SHA-256 "
 "matches. See B02s/PUBLICATION_RECEIPT.json, B02s/DELIVERY_RECEIPT.json, "
 "B02s/PUBLISHED_CLOSEOUT.md. Historical source-only; parent study OPEN.\n")
print(json.dumps({"refs_checked":2,"canonical_lilly":2137,"combined":3203,
 "payload_verified":138,"delivered":3,"byte_match":True,"all_green_global_ci":False}))
