"""Deterministic local ZIP delivery: unbranded rater forms separate from key.

Only researcher-authored fictional materials are included. Never add real
volunteer ratings, DOB, or private profile information. Zips created with
fixed metadata so hashes remain reproducible across re-runs to a NEW path.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parent
DOWNLOAD_DIR=Path.home()/"Téléchargements"
RATER_ZIP="Anonymous-Message-Style-Review-Packets-G39-20261025.zip"
RESEARCH_ZIP="Gene-Keys-G39-Researcher-Scoring-Evidence-20261025.zip"
MANIFEST=ROOT/"GENEKEYS_G39_DELIVERY_MANIFEST_V1.json"

RESEARCH_FILES=(
 "GENEKEYS_G39_BLIND_MESSAGE_MANIPULATION_REVIEW_20261025.md",
 "GENEKEYS_G39_CONTINUATION_20261025.md",
 "GENEKEYS_G39_RESEARCHER_GUIDE.md",
 "GENEKEYS_G39_RESEARCHER_ONLY_ITEM_KEY_V1.json",
 "GENEKEYS_G39_SYNTHETIC_RATER_GRADER_RECEIPT_V1.json",
 "GENEKEYS_G39_ACTUAL_BRAVE_OFFLINE_BROWSER_SMOKE_V1.json",
 "GENEKEYS_G39_STIMULUS_WORDING_CONFOUND_PREFLIGHT_V1.json",
 "GENEKEYS_G39_PUBLIC_RATER_INSTRUCTIONS.txt",
 "genekeys_g39_blind_rating_packets.py",
 "genekeys_g39_rate_blind_packets.py",
 "genekeys_g39_mock_rater_controls.py",
 "genekeys_g39_stimulus_preflight.py",
 "genekeys_g39_browser_smoke.cjs",
 "genekeys_g39_deliver_separated_packages.py",
 "test_genekeys_g39_blind_manipulation.py",
 "GENEKEYS_G38_SIX_LINE_MESSAGE_BANK_DRAFT_V1.json",
 "GENEKEYS_G37_SIX_LINE_SOURCE_TESTABILITY_V1.json",
 "GENEKEYS_G38_LINE_STYLE_STUDY_CONTRACT_DRAFT_V1.json",
 "genekeys_g38_synthetic_line_preference.py",
)


def stable_entry(archive:ZipFile,arcname:str,data:bytes)->None:
    info=ZipInfo(arcname,date_time=(2026,10,25,0,0,0))
    info.compress_type=ZIP_DEFLATED
    info.external_attr=(0o644<<16)
    info.create_system=3
    archive.writestr(info,data,compress_type=ZIP_DEFLATED,compresslevel=9)


def rater_members()->dict[str,bytes]:
    items={"README_FOR_RATERS.txt":
           (ROOT/"GENEKEYS_G39_PUBLIC_RATER_INSTRUCTIONS.txt").read_bytes()}
    for p in sorted((ROOT/"GENEKEYS_G39_ANONYMOUS_RATER_HTML").glob("*.html")):
        items["RATER_FORMS/"+p.name]=p.read_bytes()
    if len(items)!=7:
        raise ValueError("expected six blinded forms plus public instructions")
    if any("KEY" in name or "RESEARCHER" in name for name in items):
        raise AssertionError("research truth must not enter public ZIP")
    for name,data in items.items():
        if (b"source_line" in data or b"Gene Keys" in data
            or b"Human Design" in data):
            raise AssertionError("public rater archive contains source identity or truth")
    return items


def researcher_members()->dict[str,bytes]:
    items={name:(ROOT/name).read_bytes() for name in RESEARCH_FILES}
    html_dir=ROOT/"GENEKEYS_G39_ANONYMOUS_RATER_HTML"
    for p in sorted(html_dir.glob("*.html")):
        items["GENEKEYS_G39_ANONYMOUS_RATER_HTML/"+p.name]=p.read_bytes()
    if len(items)!=len(RESEARCH_FILES)+6:
        raise ValueError("research receipt missing a source or browser form")
    return items


def write_sealed_zip(path:Path,members:dict[str,bytes])->dict:
    if path.exists():
        raise FileExistsError("Refuse to overwrite existing accepted G39 delivery")
    with ZipFile(path,"x",ZIP_DEFLATED) as archive:
        for name in sorted(members):
            stable_entry(archive,name,members[name])
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("corrupt rater/researcher ZIP")
        if sorted(archive.namelist())!=sorted(members):
            raise ValueError("unexpected package membership")
        for name in members:
            if archive.read(name)!=members[name]:
                raise ValueError("package extract mismatch")
    return {
      "zip_basename":path.name,
      "byte_length":path.stat().st_size,
      "sha256":sha256(path.read_bytes()).hexdigest(),
      "member_count":len(members),
      "member_names":sorted(members),
      "no_actual_human_reviewer_or_natal_data":True,
    }


def main():
    if not DOWNLOAD_DIR.is_dir():
        raise FileNotFoundError("owner local French Downloads directory unavailable")
    if MANIFEST.exists():
        raise FileExistsError("manifest already published; do not replace")
    rater=write_sealed_zip(DOWNLOAD_DIR/RATER_ZIP,rater_members())
    research=write_sealed_zip(DOWNLOAD_DIR/RESEARCH_ZIP,researcher_members())
    if any("RESEARCHER_ONLY_ITEM_KEY" in n for n in rater["member_names"]):
        raise AssertionError("secret research mapping leaked in rater ZIP")
    if not any("RESEARCHER_ONLY_ITEM_KEY" in n for n in research["member_names"]):
        raise AssertionError("researcher ZIP cannot grade without source key")
    body={
        "schema":"HUMANDESIGN_G39_TWO_PACKAGE_OWNER_DELIVERY_V1",
        "date":"2026-10-25",
        "source_worktree_parent_commit":"40ac0e2aa07f992843180c51bf923d9baf05125d",
        "user_local_delivery_not_sandbox":True,
        "absolute_private_owner_home_directory_not_recorded":True,
        "rater_archive":rater,
        "researcher_archive":research,
        "reviewer_packet_contains_no_source_key":True,
        "researcher_key_public_repo_visibility_may_limit_adversarial_blinding":True,
        "no_rater_forms_sent_to_people":True,
        "no_real_human_manipulation_ratings":True,
        "no_real_natal_predictions":True,
        "production_modified":False,
    }
    MANIFEST.write_text(json.dumps(body,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("RATER_ZIP",RATER_ZIP,rater["member_count"],rater["byte_length"],
          rater["sha256"])
    print("RESEARCHER_ZIP",RESEARCH_ZIP,research["member_count"],
          research["byte_length"],research["sha256"])


if __name__=="__main__":
    main()
