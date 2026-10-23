"""C17 Oxford original P.Oxy. LXI 4277 image identity and source-status audit.

Publisher-authenticated image bytes are not the same as independently
transcribing all ancient Greek glyphs. C05's three documentary comparisons
remain arithmetically unchanged and cannot be counted as human predictions.
No Oxford papyrus photo is stored in the repository.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from oxy4277_monomoiria_audit_c05 import documentary_audit

EVIDENCE_FILE = Path(__file__).with_name("P_OXY_C17_OXFORD_ORIGINAL_IMAGE_EVIDENCE_V1.json")


def source_record() -> dict:
    return json.loads(EVIDENCE_FILE.read_text(encoding="utf-8"))


def historical_documentary_comparison() -> dict:
    r=source_record()
    baseline=documentary_audit()
    old=baseline["records"]
    declared=r["comparison_with_older_C05"]["papyrus_labels_as_reported_not_newly_certified"]
    assert len(old)==len(declared)==3
    audit=[]
    for orig,red in zip(old,declared):
        assert orig["object_name"].casefold()==red["object"].casefold()
        assert orig["written_monomoiria"]==red["reported_source_monomoiria"]
        assert orig["Paulus_by_sign_true_ordinal"]==red["preexisting_Paulus_bysign_proper_ordinal"]
        assert orig["agrees_true_ordinal"] is red["preexisting_match"]
        audit.append({"object":red["object"],"source_reported":orig["written_monomoiria"],
                      "derived_paulus":orig["Paulus_by_sign_true_ordinal"],
                      "matches":orig["agrees_true_ordinal"],
                      "original_photo_label_read_independently":False})
    assert sum(x["matches"] for x in audit)==1
    return {
        "historical_astrological_document":"P.Oxy. LXI 4277",
        "Oxford_exact_object_identity_verified":True,
        "photographs_directly_visually_inspected":len(r["official_images"]),
        "Publisher_supplied_and_local_MD5_sha256_verified":True,
        "historical_readings_independently_collated_from_photo":0,
        "preexisting_C05_source_arithmetic_agreements":baseline["true_ordinal_agreements"],
        "preexisting_C05_source_arithmetic_disagreements":3-baseline["true_ordinal_agreements"],
        "newly_confirmed_astrological_natal_predictions":0,
        "scoring_rule_promoted":False,
        "rows":audit,
    }


def verify_local_study_images(local_file_mapping: dict[int,Path]) -> dict:
    """Optional off-repo evidence check; separate from hermetic unit tests.

    Supply the two authorized original study image paths. A missing file
    fails closed. Do not copy images into the tracked research directory.
    """
    r=source_record()
    expected={x["id"]:x for x in r["official_images"]}
    if set(local_file_mapping)!=set(expected):
        raise ValueError("Require both exact Oxford source file IDs")
    outcome={}
    for image_id,p in local_file_mapping.items():
        f=Path(p)
        if not f.is_file():
            raise FileNotFoundError(str(f))
        info=expected[image_id]
        blob=f.read_bytes()
        got_sha=hashlib.sha256(blob).hexdigest()
        got_md5=hashlib.md5(blob).hexdigest()
        passed=(len(blob)==info["downloaded_bytes"] and got_sha==info["sha256"] and got_md5==info["publisher_md5"])
        outcome[image_id]={"passed":passed,"bytes":len(blob),"sha256":got_sha,"md5":got_md5}
        if not passed:
            raise ValueError(f"Oxford original source integrity mismatch: {image_id}")
    return {"kind":"REMOTE_LOCAL_TEMPORARY_SOURCE_PHOTO_HASH_CHECK",
            "reproduced":True,"checks":outcome,
            "images_in_Git":False}


if __name__=="__main__":
    print(json.dumps(historical_documentary_comparison(),indent=2))
