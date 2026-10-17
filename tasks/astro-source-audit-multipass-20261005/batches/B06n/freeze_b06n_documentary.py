#!/usr/bin/env python3
"""Freeze 1647 Lilly marriage death-order source as unsupported historical text."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = j("SOURCE_FIRST_AUTHORING_20261017.json")
assert author["batch"] == "B06n"
assert author["printed_chapter"] == "CXXXVI"
assert author["body_pdf_frames"] == [633, 634]
assert author["following_printed"] == "CXXXVII"
assert len(author["groups"]) == 6
assert not author["human_mortality_predicted"]

rules, reverse = [], []
for number, group in enumerate(author["groups"], 1):
    span = f"B06n-S{number:03d}"
    assert group["source_span"] == span
    assert set(group["original_pdf_frames"]) <= {633, 634}
    ids = []
    for clause in group["clauses"]:
        no = 8344 + len(rules)
        rid = f"R{no}"
        assert clause["id"] == rid
        assert len(clause["original_anchor_not_diplomatic"]) >= 6
        assert len(clause["historical_only_meaning"]) >= 45
        assert not clause["actual_human_death_order_validated"]
        assert not clause["person_mortality_illness_or_abuse_prediction_authorized"]
        assert not clause["runtime_promoted"]
        rules.append(
            {
                "id": rid,
                "record_number": no,
                "batch": "B06n",
                "source_span": span,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": clause["role"],
                "anchor_not_diplomatic": clause["original_anchor_not_diplomatic"],
                "historical_only_meaning": clause["historical_only_meaning"],
                "source_qualification": clause["qualification"],
                "historical_documentary_accepted": True,
                "independent_spousal_mortality_accuracy_validated": False,
                "independent_spousal_illness_accuracy_validated": False,
                "independent_pair_survival_order_validated": False,
                "real_human_danger_or_abuse_label_authorized": False,
                "medical_lifespan_forecast_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": span,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["group_name"],
            "mapped_record_ids": ids,
        }
    )
assert len(rules) == 54
assert [x["record_number"] for x in rules] == list(range(8344, 8398))
assert [x["id"] for x in rules if x["role"] == "next_chapter_navigation"] == ["R8396", "R8397"]
images = {}
for frame in (633, 634):
    p = B / "evidence" / f"pdf_1647-{frame}.jpg"
    raw = p.read_bytes()
    assert len(raw) > 150000 and raw[:2] == bytes.fromhex("ffd8")
    images[str(frame)] = {
        "file": str(p.relative_to(B)),
        "sha256": sha(p),
        "bytes": len(raw),
        "printed_folio": str(frame - 34),
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06n",
        "source": "William Lilly Christian Astrology 1647 original Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [633, 634],
        "following_printed_CXXXVII_heading_pdf": 634,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06n",
        "source_groups": reverse,
        "source_group_count": 6,
        "record_count": 54,
        "substantive": 52,
        "navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06n",
        "issues": [
            (
                "This historical chapter on purported death order is not evidence "
                "that natal charts forecast lifespan, mortality, physical danger "
                "or medical illness."
            ),
            (
                "No patient-level, birth-certificate, mortality registry or "
                "preregistered time-to-event studies are available; mortality and "
                "spouse-abuse forecasts are prohibited."
            ),
            (
                "The initial source says spouse significators in cadent houses "
                "ESPECIALLY second house, even though second is not cadent; "
                "preserve exact original anomaly."
            ),
            (
                "A poor seventh ruler can allegedly signal either wife death OR "
                "prolonged illness, two non-equivalent outcomes and post-hoc "
                "flexibility."
            ),
            (
                "Moon conjoined exactly ONE companion uses relative strength "
                "comparison in opposite branches; without reliable astronomical "
                "dignity grading no direction can be determined."
            ),
            (
                "Moon separated from Mars AND applying Venus in Occidental part is "
                "one compound rule; wife count and death order are different "
                "outcomes."
            ),
            (
                "Moon Venus conjunct Saturn in seventh combines spouse death and "
                "difficulty marrying; neither is an independently verified "
                "forecast."
            ),
            (
                "Venus fourth with Mars and Saturn harsh aspects is separate from "
                "further Venus movable-sign qualification that adds multiple wives "
                "and all dying first."
            ),
            (
                "Moon seventh in malefic ill aspects includes explicit Jupiter OR "
                "Venus beneficial support exception, not a universal Moon-seventh "
                "fatality prediction."
            ),
            (
                "Venus occidental of Sun plus peregrine plus malefic conjunction "
                "OR hard square/opposition carries no objective definition of "
                "short lifespan."
            ),
            (
                "Venus conjunct Mars twelfth is used for morally charged husband "
                "misconduct, NOT to predict wife death; no actual abuse "
                "classification."
            ),
            (
                "Peregrine malefics with dominion in seventh is a possible "
                "historical internal dignity conflict; expert text/source review "
                "needed."
            ),
            (
                "Lilly sometimes shifts targets from one wife to multiple wives or "
                "alleged enemies, further weakening falsifiability."
            ),
            (
                "The next printed CXXXVII on Women's Marriage starts middle "
                "PDF634; not part of first-death chapter."
            ),
            (
                "Selective original-source paraphrase only; original page-anchored "
                "photos do not validate human forecasts or constitute full "
                "diplomatic transcription."
            ),
        ],
        "real_person_lifespan_danger_or_illness_predictions_authorized": False,
        "independent_mortality_prediction_validations": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06n",
        "status": "ORIGINAL_1647_MARRIAGE_DEATH_ORDER_HISTORICAL_ONLY",
        "printed_chapter": "CXXXVI",
        "editorial_chapter": "CXXXVII",
        "record_count": 54,
        "first_record": "R8344",
        "last_record": "R8397",
        "substantive": 52,
        "following_navigation": 2,
        "source_groups": 6,
        "body_original_pdf_frames": [633, 634],
        "next_heading_pdf": 634,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "real_mortality_accuracy_validations": 0,
        "runtime_promotions": 0,
        "rules": rules,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06n",
        "status": "SOURCE_ONLY_MORTALITY_HISTORICAL_LOCALLY_FROZEN",
        "prior_lilly": 8343,
        "new_historical_annotations": 54,
        "lilly_if_published": 8397,
        "ptolemy_retained": 1066,
        "combined_if_published": 9463,
        "substantive": 52,
        "navigation": 2,
        "source_groups": 6,
        "new_numbered_chapters": 1,
        "next_printed_chapter": "CXXXVII",
        "next_original_pdf": 634,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "empirical_validations": 0,
        "real_person_mortality_forecasts_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06n 1647 first-death order source 54 historic notes R8344–R8397; no human forecasts")
