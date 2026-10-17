#!/usr/bin/env python3
"""Freeze Lilly original first-edition maternal chapter as history, not clinical advice."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def read(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


source = read("SOURCE_FIRST_AUTHORING_20261017.json")
assert source["batch"] == "B05x"
assert source["printed_chapter"] == "CXXII"
assert source["editorial_chapter"] == "CXXIII"
assert source["original_body_pdf_frames"] == [604, 605]
assert len(source["groups"]) == 11
rows, mapping = [], []
for n, group in enumerate(source["groups"], start=1):
    sid = f"B05x-S{n:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {604, 605, 606}
    ids = []
    for claim in group["claims"]:
        number = 7358 + len(rows)
        rid = f"R{number}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 12
        assert len(claim["historical_only_meaning"]) >= 45
        assert not claim["independent_human_mother_outcome_verified"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": number,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "printed_chapter": (
                    "CXXII"
                    if claim["role"] != "next_chapter_navigation"
                    else "CXXIII_NAVIGATION_ONLY"
                ),
                "role": claim["role"],
                "anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "meaning_historical_only": claim["historical_only_meaning"],
                "qualification": claim["qualification"],
                "historical_documentary_accepted": True,
                "independent_human_maternal_health_validated": False,
                "validated_maternal_wealth_or_ancestry": False,
                "reliable_human_birth_death_prediction": False,
                "clinical_or_moral_actions_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "passage_group": group["group"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 53
assert [r["record_number"] for r in rows] == list(range(7358, 7411))
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R7409", "R7410"]
assert len({r["id"] for r in rows}) == 53

images = {}
for n in (604, 605, 606):
    f = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = f.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(n)] = {
        "file": str(f.relative_to(B)),
        "sha256": sha(f),
        "bytes": len(data),
        "printed_folio": str(n - 34),
        "role": "mother_chapter_body" if n in (604, 605) else "next_chapter_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05x",
        "source": "William Lilly original Christian Astrology 1647, Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_frames": [604, 605],
        "next_printed_CXXIII_heading_frame": 606,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05x",
        "source_groups": mapping,
        "group_count": 11,
        "record_count": 53,
        "substantive_source_records": 51,
        "next_heading_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05x",
        "issues": [
            (
                "These original 1647 maternal source clauses are not verified human "
                "maternal lifespan, disease, childbirth, class or mortality "
                "observations."
            ),
            (
                "The mother's proposed indicators are tenth house, tenth ruler, "
                "Venus by day/Moon by night, and planets physically occupying tenth; "
                "mixing sect conditions is invalid."
            ),
            (
                "The original favorable mother branch depends on majority strength "
                "and good house/dignities, and explicitly on the mother's "
                "pre-existing family social position."
            ),
            (
                "The author's comparison of mother and father outcomes distinguishes "
                "finances, body and mind, which are not one observable variable."
            ),
            (
                "Sun/Moon Venus and malefic planet orientation and angular "
                "conditions contain multiple historic diagnostic alternatives; none "
                "is modern physiology."
            ),
            (
                "The oriental versus occidental description's grammatical subject is "
                "uncertain and must not create a deterministic rule about a mother's "
                "life versus estate."
            ),
            (
                "Conjunction with Saturn/Mars/Mercury in maternal-short-life "
                "passages has unknown glyph/operator scope; preserve source "
                "uncertainty."
            ),
            (
                "The old concepts of 'imposthumation' of matrix/reins, cholick, "
                "fevers and agues are premodern claims, not clinical diagnoses or "
                "disease causes."
            ),
            (
                "Multiple simultaneous alternative aspects and houses permit "
                "retrospective overfitting of maternal outcomes without "
                "preregistered rejection criteria."
            ),
            (
                "No independent participant/case histories, maternal death records, "
                "health outcomes, socioeconomic controls, births or time horizons "
                "are supplied."
            ),
            (
                "The succeeding printed CXXIII on childbirth labour starts at "
                "PDF606/printed572 and is separate from mother status/life chapter; "
                "do not absorb."
            ),
            (
                "No full diplomatic first-edition glyph-by-glyph transcription has "
                "been certified; selective original source anchors and uncertainties "
                "retained."
            ),
            (
                "None of these historic claims should be used for care, prediction "
                "of life or death, family accusation, fertility advice, or other "
                "high-stakes decisions."
            ),
        ],
        "original_diplomatic_transcription_complete": False,
        "independent_actual_person_validations": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B05x",
        "status": "FIRST_EDITION_MOTHER_MEDICAL_HISTORICAL_DOCUMENTARY_ONLY",
        "printed_chapter": "CXXII",
        "editorial_chapter": "CXXIII",
        "record_count": 53,
        "first_record": "R7358",
        "last_record": "R7410",
        "original_body_frames": [604, 605],
        "following_heading_frame": 606,
        "source_groups": 11,
        "substantive_historical_clauses": 51,
        "navigation_units": 2,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "medical_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B05x",
        "status": "LOCAL_DOCUMENTARY_FREEZE_PENDING_REMOTE",
        "previous_lilly": 7357,
        "new_source_records": 53,
        "lilly_if_published": 7410,
        "ptolemy_retained": 1066,
        "combined_if_published": 8476,
        "substantive": 51,
        "navigation": 2,
        "source_group_count": 11,
        "next_printed_chapter": "CXXIII",
        "next_original_pdf": 606,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "independent_human_mortality_validations": 0,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B05x original mother source: 53 historical annotations R7358-R7410")
