"""Prepare one guarded historical-source-only B02v canonical index update.

No Git push in this script. The predecessor index, accepted source packet,
byte hashes, original source scope and historical-only claim boundary are
validated before editing. The prior index bytes are frozen for recovery.
"""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[4]
B=Path(__file__).resolve().parent
INDEX=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
BACK=B/"recovery/LILLY_SOURCE_EXTRACTION_INDEX_BEFORE_B02v_CANONICAL_20261015.json"
REPORT=B/"CANONICAL_INTEGRATION_PREPARE_RECEIPT_U75_20261015.json"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02v_CHAPTER_L_COMPLETE.md"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
assert not BACK.exists() and not REPORT.exists(),"Already prepared; inspect existing state before retry"
assert not LATEST.exists(),"Latest source state already exists"
def sha(b):return hashlib.sha256(b).hexdigest()
def source(name):return (B/name).read_bytes()
raw=INDEX.read_bytes()
j=json.loads(raw)
old_blob_sha="d83d30b0b5496ee1d2e024878c6692fc27c60abe"
# git-object SHA-1 verified before this guarded transformation
import subprocess
g=subprocess.run(["git","hash-object",str(INDEX)],cwd=ROOT,capture_output=True,text=True,check=True)
assert g.stdout.strip()==old_blob_sha,(g.stdout.strip(),old_blob_sha)
assert j["source_id"]=="LILLY1647_WELLCOME_B30338724"
assert j["source_sha256"]=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert j["records_count"]==2572 and sum(x["records_count"] for x in j["batches"])==2572
assert j["batches"][-1]["id"]=="B02u"
assert not any(x["id"]=="B02v" for x in j["batches"])
assert j["read_numbered_chapters"]==list(range(1,50))
assert j["next"]["pdf_page"]==381 and j["next"]["chapter"]=="L"
assert j["runtime_promotions"]==j["empirical_validations"]==0
a=json.loads(source("ACCEPTANCE.json"))
rules=json.loads(source("RULES.json"))
unresolved=json.loads(source("UNRESOLVED.json"))
claim=json.loads(source("CLAIM_LEDGER.json"))
receipt=json.loads(source("independent_review/DOCUMENTARY_SOURCE_RELEASE_RECEIPT_U75_20261015.json"))
assert a["accepted"] and a["kind"]=="HISTORICAL_SOURCE_DOCUMENTARY_ONLY"
assert a["new_documentary_source_units"]==402
assert a["prior_accepted_lilly"]==2572 and a["uncertainties_retained"]==75
assert a["chapter_L_source_text_covered"] and not a["canonical_published"]
assert a["new_verified_predictive_cases"]==a["new_independently_authenticated_crimes"]==a["runtime_promotions"]==0
assert len(rules["rules"])==rules["record_count"]==402
assert [r["record_number"] for r in rules["rules"]]==list(range(2573,2975))
assert all(r["chapter"]=="L" for r in rules["rules"])
assert rules["documentary_accepted_locally"] and rules["whole_chapter_l_complete_at_documentary_source_level"]
assert not rules["accepted_as_empirical_astro_prediction"]
assert claim["empirical_predictive_outcomes"]==claim["runtime_promotions"]==0
assert len(unresolved["issues"])==75
hashes={
 "RULES.json":"rules_sha256","SOURCE_ORDER.json":"source_order_sha256",
 "UNRESOLVED.json":"unresolved_sha256","CLAIM_LEDGER.json":"claim_ledger_sha256",
 "AUDIT_REPORT.md":"audit_report_sha256",
}
for f,key in hashes.items():
    assert sha(source(f))==a[key],(f,key)
assert receipt["local_documentary_admission"]
assert receipt["accepted_documentary_source_records"]==402
assert receipt["number_original_source_images"]==21
assert receipt["archive_sha256"]==receipt["destination_sha256"]
assert sum(x["tests_run"] for x in receipt["actual_extracted_tests"].values())==109
assert all(x["exit_code"]==0 for x in receipt["actual_extracted_tests"].values())
archive=Path(receipt["destination_os_downloads"])
assert archive.is_file() and archive.stat().st_size==receipt["archive_size_bytes"]
assert sha(archive.read_bytes())==receipt["archive_sha256"]
old_current=CURRENT.read_bytes()
entry={
 "id":"B02v","path":"batches/B02v/RULES.json","records_count":402,
 "sha256":a["rules_sha256"],
 "scope":"Book II Chapter L final thief-house and theft sections; original PDF381 below thief-house heading through PDF400 above Chapter LI divider, 402 historical documentary source units, 75 retained textual issues, zero verified criminal or predictive cases."
}
j["batches"].append(entry)
j["records_count"]=2974
j["status"]="BOOK_I_COMPLETE_BOOK_II_THROUGH_L_DOCUMENTARY_SOURCE_ONLY_NEXT_LI_OPEN"
j["read_numbered_chapters"].append(50)
j["next"]={
 "pdf_page":400,"printed_page":366,"chapter":"LI",
 "heading":"Of Battell, Warre, or other Contentions",
 "include_opening_paragraph":True,
 "extracted":False,"boundary_image_read":True,
 "position":"Original PDF400 BELOW horizontal divider after Chapter L last capture clause; begin heading and first paragraph of Chapter LI without overlap."
}
j["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02v_CHAPTER_L_COMPLETE.md"
j["read_headed_units_count_note"]="Legacy cumulative headed-unit count is not recomputed here. B02v SOURCE_ORDER preserves 49 editorial section markers (48 printed-heading candidates and one prose lead-in); those have a narrower candidate definition."
j["chapter_L_source_acceptance_note"]="Documentary source intake only; 75 issue entries include repaired misreadings and still unresolved grammar/glyphs. Source-to-record map and bounded image audit are not independent word-for-word certification. No empirical validation, clinical use or real-person inference."
assert sum(x["records_count"] for x in j["batches"])==j["records_count"]==2974
assert len(j["read_numbered_chapters"])==50 and j["read_numbered_chapters"][-1]==50
body=r"""# Astrology source audit — William Lilly Chapter L documentary intake complete (B02v)

**2026-10-15 / Africa-Dakar UTC+0. Parent multi-author source study OPEN.**
Historical documentary/source-only acceptance, NOT a validated prediction model or verified claim about any person, crime, location, physical appearance, or medical outcome.

## Canonical accepted source inventory
- William Lilly, *Christian Astrology* (1647), original Wellcome b30338724, full PDF SHA256 \`2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b\`.
- Previous B02u accepted source R1–R2572 = **2,572** records. New B02v source R2573–R2974 = **402 historical documentary units**, locally source-accepted with **75 retained textual issue entries**, bringing Lilly to **2,974**.
- Retained Ptolemy English source: **1,066** records. Combined historical-source documentary units **4,040**. All source units are interpretations/references, not independent prediction cases.
- B02v physical scope: original PDF381/printed347 BELOW \`Of the house of the Thiefe, and the mark thereof\`; through PDF400/printed366 ABOVE Chapter LI divider. Exactly 20 original pages and original same-volume errata PDF888. No Chapter LI body included.

## Source integrity and qualified admission
- B02v \`ACCEPTANCE.json\`, \`RULES.json\`, \`SOURCE_ORDER.json\`, \`UNRESOLVED.json\`, \`CLAIM_LEDGER.json\` and \`AUDIT_REPORT.md\` are the accepted **documentary** files. \`RULES.json\` SHA256 **00e5e05c31a3f782983e7425cd4e4ab5ff2b9e7e9a2f8d9c7a55a03ffda2d409**.
- 20 original-page reverse maps have 420 normalized printed-source anchors referring to all 402 candidate IDs. 36 normalized direction-table rows checked. Ten higher-risk pages received additional image-first condition examination.
- Printed p360 line4 same-volume erratum remains unresolved; U01–U75 include earlier repaired errors and retained ambiguities. These uncertainties must be consulted when using historical text. No independent full diplomatic second transcription was claimed or required as a new owner gate.
- Release packet: **39,720,474 bytes**, ZIP SHA256 **c0834a95b3d14eabcd8f8c67721f1c321bc80f61ae760188b2c4f585d1a577ec**, in the owner's OS-designated Downloads folder as \`Astrology-Lilly-Chapter-L-Documentary-Source-Acceptance-20261015.zip\`. All 256 payload files, CRC, manifest SHA256, actual extraction and **109 source-only tests** verified. The archival admission originally marked canonical publication pending; verify post-publication receipt rather than treating that historic flag as current.
- **Empirical/source boundary:** zero independently authenticated crime cases, clinical validation, human chart predictions, runtime model promotions, or blinded forecast score changes.

## Continue the unfinished owner outcome
**Next original chapter:** William Lilly, Book II Chapter **LI**, *Of Battell, Warre, or other Contentions*. Start original PDF400/printed366 **BELOW** the horizontal divider following Chapter L's final clause. Reuse the verified original 1647 source and same-volume errata, preserve chapter boundaries, independent page-to-record source fidelity and historical authorial uncertainties. After Lilly, continue Valens, Phaladipika, and the owner's remaining astrology corpus.

This state file is part of the canonical index integration; later publication/readback receipts bind the actual Git refs. Retain B02u and historical B02v provisional snapshots intact.
"""
body=body.replace("\\`","`")
preface=r"""# Current astrology source audit — see latest authoritative chapter checkpoint

**CURRENT (2026-10-15):** Lilly Chapter L historical documentary source intake is locally accepted as B02v with 402 additional source units (R2573–R2974), 75 retained source issues; **2,974 Lilly + 1,066 retained Ptolemy = 4,040 total historical source units**. The owner’s multi-author study remains OPEN. Next: Chapter LI original PDF400/printed366 BELOW divider. Read \`state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261015_B02v_CHAPTER_L_COMPLETE.md\` and \`tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json\`. No empirical validation, criminal inference or runtime model promotion. Detailed material below this header describes the HISTORICAL B02a stage and is not current.

---

"""
preface=preface.replace("\\`","`")
BACK.parent.mkdir(parents=True,exist_ok=True)
BACK.write_bytes(raw)
INDEX.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n")
LATEST.parent.mkdir(parents=True,exist_ok=True)
LATEST.write_text(body)
CURRENT.write_text(preface+old_current.decode("utf-8"))
receipt_data={
 "status":"PREPARED_INDEX_AND_SOURCE_STATE_LOCALLY_NO_REMOTE_PUBLICATION_YET",
 "source_ref_before":"research/six-rule-life-timing-20261001",
 "predecessor_index_git_blob_sha1":old_blob_sha,
 "previous_index_sha256":sha(raw),
 "new_index_sha256":sha(INDEX.read_bytes()),
 "new_source_state_sha256":sha(LATEST.read_bytes()),
 "new_current_state_sha256":sha(CURRENT.read_bytes()),
 "accepted_source_rule_sha256":a["rules_sha256"],
 "accepted_source_release_zip_sha256":receipt["archive_sha256"],
 "batch":"B02v","new_documentary_units":402,
 "lilly_accepted_after_preparation":2974,"ptolemy_retained":1066,"combined":4040,
 "next_chapter":"LI","next_original_pdf_page":400,"next_boundary":"BELOW Chapter L divider",
 "predictive_validations_added":0,"canonical_published":False
}
REPORT.write_text(json.dumps(receipt_data,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(receipt_data,indent=2))
