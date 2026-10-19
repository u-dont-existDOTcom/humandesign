#!/usr/bin/env python3
"""Portable original Di Tian Sui 55-note source packet: 321 regression tests."""
import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
P="tasks/astro-chinese-primary-sources-20261017"
REL=P+"/batches/ChineseAstro-05/"
WEST="tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
NAME="Astrology-DiTianSui-BaZi-55-Pinned-Chinese-Sources-B05-20261019.zip"


def sha(f):
    return hashlib.sha256(Path(f).read_bytes()).hexdigest()


def load(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def downloads():
    p=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
    return Path(p.stdout.strip() if p.returncode==0 and p.stdout.strip()
                else str(Path.home()/"Téléchargements"))


notes=load(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json")
witness=load(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json")
source=load(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json")
v4=B/"recovery"/"CHINESE_V4_BEFORE_05.json"
v4=v4 if v4.exists() else ROOT/P/"CHINESE_SOURCE_AUDIT_INDEX_V4.json"
prev=load(v4)
assert prev["sum_source_annotations"]==207
assert prev["systems"][0]["accepted_source_annotations"]==46
assert prev["systems"][1]["accepted_source_annotations"]==161
assert prev["systems"][0]["next_id"]=="BZI-R0047"
assert notes["source_only_annotation_count"]==55
assert notes["first_id"]=="BZI-R0047" and notes["last_id"]=="BZI-R0101"
assert witness["exact_chinese_source_anchor_matches"]==55
assert notes["source_manifest_sha256"]==witness["source_manifest_sha256"]==(
    sha(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json")
)
assert set(source)==set(notes["chapter_codes"])
assert all(row["original_quote_directly_matched"] for row in notes["records"])
assert all(not row["runtime_model_promoted"] for row in notes["records"])
assert load(ROOT/WEST)["records_count"]==12472

paths=[
    P+"/CHINESE_SOURCE_AUDIT_INDEX_V1.json",
    P+"/CHINESE_SOURCE_AUDIT_INDEX_V2.json",
    P+"/CHINESE_SOURCE_AUDIT_INDEX_V3.json",
    P+"/SOURCE_MANIFEST_V1.json",
    P+"/bazi/BAZI_SOURCE_FIRST_RULES_V1.json",
    P+"/bazi/bazi_source_mechanics.py",
    P+"/bazi/ditiansui_historical_conventions.py",
    P+"/ziwei/ZIWEI_SOURCE_FIRST_RULES_V1.json",
    P+"/ziwei/ziwei_source_mechanics.py",
    P+"/ziwei/quan_shu_vol2_placements.py",
    P+"/ziwei/quan_shu_vol2_aux_placements.py",
    P+"/ziwei/quan_shu_vol2_life_body_taxonomy.py",
    P+"/batches/ChineseAstro-02/ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json",
    P+"/batches/ChineseAstro-02/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    P+"/batches/ChineseAstro-02/test_ziwei_volume2_source.py",
    P+"/batches/ChineseAstro-03/ZIWEI_VOLUME2_AUXILIARY_45_SOURCE_NOTES_V1.json",
    P+"/batches/ChineseAstro-03/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    P+"/batches/ChineseAstro-03/test_chinese_source_03.py",
    P+"/batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json",
    P+"/batches/ChineseAstro-04/SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    P+"/batches/ChineseAstro-04/test_chinese04_source_and_mechanics.py",
    P+"/tests/test_chinese_source_mechanics.py",
]+[REL+n for n in (
    "DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json",
    "BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json",
    "SOURCE_REVISION_ANCHOR_WITNESS_V1.json",
    "ORIGINAL_BAZI_SOURCE_REVIEW_20261019.md",
    "CONTINUATION_HANDOFF_ACCEPTED_20261019.md",
    "freeze_pinned_ditiansui_source.py",
    "test_chinese05_ditiansui_sources.py",
    "build_chinese_05_release.py",
    "prepare_chinese_05_index_v5.py",
)]
files={name:ROOT/name for name in paths}
files[P+"/CHINESE_SOURCE_AUDIT_INDEX_V4.json"]=v4
files[WEST]=ROOT/WEST
assert all(p.is_file() for p in files.values()),[
    name for name,p in files.items() if not p.is_file()
]
manifest={
    "batch":"ChineseAstro-05",
    "source":"Di Tian Sui transmitted Wikisource chapters 01/02/03/06/09/10",
    "six_frozen_source_revision_hashes":{
        key:value["full_source_sha256"] for key,value in source.items()
    },
    "source_quoted_original_chinese_passages":55,
    "source_original_verses":44,
    "source_transmitted_commentary":11,
    "prior_chinese_historical_notes":207,
    "new_BaZi_source_notes":55,
    "total_BaZi_if_accepted":101,
    "ZiWei_retained":161,
    "total_chinese_if_accepted":262,
    "Lilly_Western_historical_source_unchanged":12472,
    "true_early_print_author_verified":False,
    "full_astrological_year_month_day_hour_calendar_engine_verified":False,
    "real_human_predictive_validations":0,
    "runtime_promotions":0,
    "members":{
        name:{"sha256":sha(p),"bytes":p.stat().st_size} for name,p in files.items()
    },
}
folder=downloads()
folder.mkdir(parents=True,exist_ok=True)
archive=folder/NAME
with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,file in files.items():
        z.write(file,"ChineseAstro-05-root/"+name)
    z.writestr("ChineseAstro-05-root/RELEASE_MANIFEST.json",
               json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")

tests=[
    (REL,"test_chinese05_ditiansui_sources.py",72),
    (P+"/batches/ChineseAstro-04/","test_chinese04_source_and_mechanics.py",89),
    (P+"/batches/ChineseAstro-03/","test_chinese_source_03.py",68),
    (P+"/batches/ChineseAstro-02/","test_ziwei_volume2_source.py",54),
    (P+"/tests/","test_chinese_source_mechanics.py",38),
]
ran=[]
with zipfile.ZipFile(archive) as z,tempfile.TemporaryDirectory() as td:
    assert z.testzip() is None
    z.extractall(td)
    root=Path(td)/"ChineseAstro-05-root"
    assert load(root/"RELEASE_MANIFEST.json")==manifest
    for name,meta in manifest["members"].items():
        f=root/name
        assert f.stat().st_size==meta["bytes"]
        assert sha(f)==meta["sha256"]
    for directory,pattern,expected in tests:
        p=subprocess.run(
            ["python3","-m","unittest","discover","-s",str(root/directory),
             "-p",pattern,"-q"],
            capture_output=True,text=True,timeout=90,
        )
        assert p.returncode==0,p.stdout+"\n"+p.stderr
        m=re.search(r"Ran (\d+) tests",p.stderr)
        assert m and int(m.group(1))==expected,p.stderr
        assert "skipped" not in p.stderr
        ran.append(expected)
assert sum(ran)==321
receipt={
    "batch":"ChineseAstro-05",
    "status":"SIX_PINNED_DITIAN_SUI_SOURCES_55_QUOTES_321_ARCHIVE_REPLAY_PASS",
    "filename":NAME,
    "archive_sha256":sha(archive),
    "archive_bytes":archive.stat().st_size,
    "member_count":len(files),
    "CRC_passed":True,
    "member_sha256_and_exact_bytes_passed":True,
    "independent_archive_extract_passed":True,
    "new_BaZi_source_tests":72,
    "Chinese04_retained":89,
    "Chinese03_retained":68,
    "Chinese02_retained":54,
    "prior_Chn_mechanics_retained":38,
    "total_portable_test_replays":321,
    "source_manifest_sha256":sha(B/"DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json"),
    "55_notes_sha256":sha(B/"BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json"),
    "source_quote_witness_sha256":sha(B/"SOURCE_REVISION_ANCHOR_WITNESS_V1.json"),
    "prior_chinese_V4_index_sha256":sha(v4),
    "western_Lilly_count_retained":12472,
    "human_predictive_validations":0,
    "runtime_promotions":0,
    "remote_published":False,
}
(B/"SOURCE_RELEASE_RECEIPT_20261019.json").write_text(
    json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
)
print(json.dumps(receipt,indent=2))
