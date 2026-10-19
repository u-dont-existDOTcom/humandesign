#!/usr/bin/env python3
"""Guarded append-only Chinese V5 registry admission, 55 Di Tian Sui notes."""
import copy
import hashlib
import json
import subprocess
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
P=B.parents[1]
V4=P/"CHINESE_SOURCE_AUDIT_INDEX_V4.json"
V5=P/"CHINESE_SOURCE_AUDIT_INDEX_V5.json"
WEST=ROOT/"tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_CHINESE_SOURCE_AUDIT_LATEST_20261019_05.md"
RECOVERY=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261019.json"
BRANCH="research/astro-chinese-05-bazi-ditiansui-20261019"


def sha(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()


def downloads():
    p=subprocess.run(["xdg-user-dir","DOWNLOAD"],text=True,capture_output=True)
    return Path(p.stdout.strip() if p.returncode==0 and p.stdout.strip()
                else str(Path.home()/"Téléchargements"))


for p in (V5,RECEIPT,LATEST,RECOVERY/"CHINESE_V4_BEFORE_05.json"):
    assert not p.exists(),f"Possible interrupted admission, reconcile first: {p}"
assert git("branch","--show-current")==BRANCH
old=load(V4)
notes=load(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json")
witness=load(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
manifest=load(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json")
release=load(B/"SOURCE_RELEASE_RECEIPT_20261019.json")
western=load(WEST)
assert old["sum_source_annotations"]==207
assert old["accepted_batches"][-1]["id"]=="ChineseAstro-04"
assert old["systems"][0]["accepted_source_annotations"]==46
assert old["systems"][1]["accepted_source_annotations"]==161
assert old["systems"][0]["next_id"]=="BZI-R0047"
assert old["systems"][1]["next_id"]=="ZWD-R0162"
assert old["independently_validated_real_human_claims"]==old["runtime_promotions"]==0
assert notes["source_only_annotation_count"]==55
assert notes["first_id"]=="BZI-R0047"
assert notes["last_id"]=="BZI-R0101"
assert notes["next_id"]=="BZI-R0102"
assert notes["human_predictive_validations"]==notes["runtime_promotions"]==0
assert witness["exact_chinese_source_anchor_matches"]==55
assert witness["human_predictive_validations"]==witness["runtime_promotions"]==0
assert set(manifest)==set(("01","02","03","06","09","10"))
assert all(r["original_quote_directly_matched"] for r in notes["records"])
assert all(not r["runtime_model_promoted"] for r in notes["records"])
assert [r["id"] for r in notes["records"]]==[
    f"BZI-R{n:04d}" for n in range(47,102)
]
assert release["CRC_passed"] and release["member_sha256_and_exact_bytes_passed"]
assert release["independent_archive_extract_passed"]
assert release["total_portable_test_replays"]==321
assert sha(downloads()/release["filename"])==release["archive_sha256"]
assert sha(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json")==release["55_notes_sha256"]
assert sha(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json")==release["source_quote_witness_sha256"]
assert sha(V4)==release["prior_chinese_V4_index_sha256"]
assert western["records_count"]==release["western_Lilly_count_retained"]==12472
assert western["batches"][-1]["id"]=="B07w"
for f in (
    P/"CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    P/"CHINESE_SOURCE_AUDIT_INDEX_V2.json",
    P/"CHINESE_SOURCE_AUDIT_INDEX_V3.json",
    V4,
    P/"bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    P/"bazi/bazi_source_mechanics.py",
    P/"ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P/"ziwei/quan_shu_vol2_life_body_taxonomy.py",
    P/"batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json",
    WEST,
):
    relative=str(f.relative_to(ROOT))
    assert git("rev-parse","HEAD:"+relative)==git("hash-object",str(f)),relative

RECOVERY.mkdir(exist_ok=False)
for file,name in (
    (V4,"CHINESE_V4_BEFORE_05.json"),
    (CURRENT,"CHINESE_CURRENT_BEFORE_05.md"),
    (WEST,"WESTERN_LILLY_INDEX_BEFORE_CHINESE05.json"),
):
    (RECOVERY/name).write_bytes(file.read_bytes())

index=copy.deepcopy(old)
index["schema"]="ASTROLOGY_CHINESE_SOURCE_EXTRACTION_INDEX_V5"
index["status"]="BAZI_SIX_DITIAN_SUI_CHAPTERS_55_EXACT_SOURCE_QUOTES_DOCUMENTED"
index["as_of_utc"]="2026-10-19"
index["prior_index"]="CHINESE_SOURCE_AUDIT_INDEX_V4.json"
index["prior_index_sha256"]=sha(V4)
index["sum_source_annotations"]=262
index["original_chinese_source_anchors_checked_against_revision"]=190
index["accepted_batches"].append({
    "id":"ChineseAstro-05",
    "added_bazi_source_annotations":55,
    "added_ziwei_source_annotations":0,
    "start":"BZI-R0047",
    "end":"BZI-R0101",
    "path":"batches/ChineseAstro-05/BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json",
    "rules_sha256":sha(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json"),
    "witness_path":"batches/ChineseAstro-05/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    "witness_sha256":sha(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "source_manifest_path":"batches/ChineseAstro-05/DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json",
    "source_manifest_sha256":sha(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json"),
    "source_pinned_multiple_revision_ids":{
        k:v["revision_id"] for k,v in manifest.items()
    },
    "portable_tests_replayed":321,
    "independent_human_predictions_validated":0,
    "runtime_rules_promoted":0,
})
bz=index["systems"][0]
bz["accepted_source_annotations"]=101
bz["current_ids"]="BZI-R0001–BZI-R0101"
bz["next_id"]="BZI-R0102"
bz["current_batch"]="ChineseAstro-05"
bz["source_files"]=[
    "bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    "batches/ChineseAstro-05/BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json",
]
bz["chapter_coverage"]=(
    "46 historical Joey Yap 2005/2006 English claims plus 55 exact "
    "original Chinese phrase annotations from Di Tian Sui transmitted "
    "Wikisource chapters 01,02,03,06,09,10 with frozen six oldids and "
    "separate verse/commentary statuses. Author/early-imprint authenticity "
    "and complete BaZi lunisolar chart engine not yet verified."
)
index["separate_lilly_source_count_at_this_revision"]=12472
index["separate_ptolemy_source_count_at_this_revision"]=1066
index["full_ziwei_original_text_collation_finished"]=False
index["all_14_principal_stars_verified"]=False
index["ziwei_complete_natal_calendar_engine_verified"]=False
index["chinese_bazi_solar_term_engine_verified"]=False
index["independently_validated_real_human_claims"]=0
index["runtime_promotions"]=0
index["historical_glyph_and_translator_limits"]=(
    "Historical transmitted Di Tian Sui chapters are versioned online "
    "Chinese wikitext, not an authenticated early woodblock. Source "
    "verse and later commentary are separately labeled, English "
    "glosses are provisional; important context qualifiers expressly "
    "oppose rigid life/death-stage forecasts. Previous Zi Wei oldid "
    "1963110 with ambiguous 火玲 remains unaltered. No measured "
    "human predictive validity or full astrology calendar engine."
)
index["next"]=(
    "BaZi BZI-R0102 source-first Di Tian Sui chapters 04–05, 07–08 "
    "and subsequent sections; independently verify early original "
    "printed text and commentary strata. Zi Wei ZWD-R0162 original "
    "Volume II source bureau diagrams and calendar. Lilly original "
    "1647 CLXVI numerical measures remain unaccepted R12473. "
    "Separate actual ephemeris/calendar chart parity before real "
    "prospective blinded human testing."
)
assert sum(s["accepted_source_annotations"] for s in index["systems"])==262
assert [a["id"] for a in index["accepted_batches"]]==(
    [a["id"] for a in old["accepted_batches"]]+["ChineseAstro-05"]
)
V5.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

summary=(
    "# Chinese source-first progress: Di Tian Sui six original chapters (V5)\n\n"
    "Added **55 pinned exact original Chinese source excerpts BZI-R0047–BZI-R0101**, "
    "44 historical verses and 11 transmitted commentary excerpts from six "
    "separately SHA-pinned Wikisource raw chapters. Conditional chart "
    "interpretation and the original warning against rigid stage-of-death "
    "forecasts are documented; author and physical early edition are not "
    "independently verified. Chinese accepted **101 BaZi +161 Zi Wei =262 "
    "historical annotations**, prior Chinese V1–V4 byte-preserved. "
    "**321 source/mechanics regression tests replayed from independently "
    "extracted CRC/SHA-verified archive.** Western historical index unchanged "
    "**12,472 Lilly +1,066 Ptolemy=13,538**; original printed CLXVI numerical "
    "Lilly notes R12473 unaccepted. Next **BZI-R0102, ZWD-R0162**. "
    "No authenticated full Chinese/Western chart engine, no independent real "
    "people predictions and no runtime model promotions.\n\n"
)
prior_current=CURRENT.read_text(encoding="utf-8")
CURRENT.write_text(
    summary+"## Earlier accepted checkpoint preserved verbatim\n\n"+prior_current,
    encoding="utf-8"
)
LATEST.write_text(
    summary+(B/"ORIGINAL_BAZI_SOURCE_REVIEW_20261019.md").read_text(encoding="utf-8"),
    encoding="utf-8"
)
record={
    "batch":"ChineseAstro-05",
    "status":"PINNED_BAZI_SOURCE_INDEX_V5_PREPARED_REMOTE_PUBLISH_PENDING",
    "Chinese_before":207,
    "Chinese_after":262,
    "BaZi_before":46,
    "BaZi_after":101,
    "ZiWei_retained":161,
    "new_documented_source_notes":55,
    "prior_index_V4_sha256":sha(V4),
    "new_index_V5_sha256":sha(V5),
    "DiTianSui_original_notes_sha256":sha(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json"),
    "original_quote_witness_sha256":sha(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "original_chapter_manifest_sha256":sha(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json"),
    "archive_sha256":release["archive_sha256"],
    "portable_tests":321,
    "Western_Lilly_retained":12472,
    "Ptolemy_retained":1066,
    "next_BaZi":"BZI-R0102",
    "next_ZiWei":"ZWD-R0162",
    "human_predictions_validated":0,
    "runtime_promotions":0,
}
RECEIPT.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",
                   encoding="utf-8")
print(json.dumps(record,indent=2))
