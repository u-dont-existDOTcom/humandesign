#!/usr/bin/env python3
"""Freeze original 1647 Regiomontanus narrative: historical source only."""

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


a = j("SOURCE_FIRST_AUTHORING_20261017.json")
proc = j("REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json")
assert a["batch"] == proc["batch"] == "B06b"
assert a["printed_chapter"] == "CXXVI"
assert a["body_pdf_frames"] == [608, 609]
assert len(a["source_groups"]) == 10
assert proc["procedure_status"] == "SOURCE_RECONSTRUCTION_ONLY_NON_EXECUTABLE"
assert not proc["attributions_verified_against_original_regiomontanus"]
assert not proc["tests_and_limits"]["promote_to_runtime"]
assert proc["source_preconditions"]["day_geniture_required"]
assert proc["source_preconditions"]["sun_not_on_tenth_or_fourth_cusp"]
assert proc["arithmetic_template"]["house_increment_deg"] == 30
records, mapping = [], []
for i, group in enumerate(a["source_groups"], 1):
    sid = f"B06b-S{i:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {608, 609}
    refs = []
    for clause in group["clauses"]:
        number = 7503 + len(records)
        rid = f"R{number}"
        assert clause["id"] == rid
        assert len(clause["source_anchor_not_diplomatic"]) >= 10
        assert len(clause["historical_only_meaning"]) >= 40
        assert not (
            clause["independent_family_prediction_validated"]
            or clause["astronomical_chart_recovery_validated"]
            or clause["runtime_promoted"]
        )
        records.append(
            {
                "id": rid,
                "record_number": number,
                "batch": "B06b",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": clause["role"],
                "original_anchor_not_diplomatic": clause["source_anchor_not_diplomatic"],
                "historical_only_meaning": clause["historical_only_meaning"],
                "source_qualification": clause["qualification"],
                "historical_documentary_accepted": True,
                "independent_human_parental_affection_validated": False,
                "regiomontanus_original_independently_verified": False,
                "independent_father_birth_time_recovery_validated": False,
                "runtime_algorithm_promoted": False,
                "medical_legal_or_family_advice_authorized": False,
            }
        )
        refs.append(rid)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "original_passage": group["source_group"],
            "mapped_record_ids": refs,
        }
    )
assert len(records) == 46
assert [r["record_number"] for r in records] == list(range(7503, 7549))
assert [r["id"] for r in records if r["role"] == "next_chapter_navigation"] == ["R7547", "R7548"]
assert len({r["id"] for r in records}) == len(records)
images = {}
for n in range(608, 612):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "role": "chapter_body" if n in (608, 609) else "next_section_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06b",
        "source": "William Lilly Christian Astrology original 1647 Wellcome b30338724",
        "volume_source_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pdf_frames": [608, 609],
        "following_mines_chapter_CXXVII_frame": 609,
        "following_unnumbered_sixth_house_frame": 610,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06b",
        "source_groups": mapping,
        "record_count": 46,
        "source_group_count": 10,
        "substantive": 44,
        "next_chapter_navigation": 2,
        "historical_astronomical_procedure_file": "REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json",
        "historic_procedure_steps": len(proc["source_steps"]),
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06b",
        "issues": [
            (
                "Both the source's parent-affection claims and the father-chart "
                "reconstruction claim are unvalidated on real people."
            ),
            (
                "Do not confuse Sun and Moon as daytime father/mother in THIS "
                "chapter with Sun and Venus in the preceding parents' mutual "
                "agreement chapter."
            ),
            (
                "The source's daylight parent indicators, nighttime Saturn/Moon, "
                "first ruler versus literal Ascendant aspects, and reception are "
                "distinct relational conditions."
            ),
            (
                "Lilly's stronger-mother-affection branch explicitly requires "
                "Moon/Venus favorable aspect and lack of favorable Sun/Saturn "
                "counterpart; absence matters."
            ),
            (
                "The attribution Regiomontanus Problem 24 is a statement by Lilly; "
                "the original Regiomontanus mathematical proof is not separately "
                "inspected."
            ),
            (
                "The source explicitly limits its father figure technique to a "
                "diurnal geniture when Sun is not on tenth or fourth cusp, with no "
                "alternate implementation for excluded cases."
            ),
            (
                "Original Sun positional circle pole is not interchangeable with "
                "geographic latitude or ordinary oblique ascension at the local "
                "horizon."
            ),
            (
                "Right ascension of proposed Midheaven must remain distinct from "
                "original Sun oblique ascension; source subtracts 90 degrees then "
                "refers to house-specific poles and 30 degree increments."
            ),
            (
                "The inverse oblique ascension to ecliptic longitude step requires "
                "validated Regiomontanus pole tables or exact astronomical "
                "algorithm, missing from this source batch."
            ),
            (
                "Original reference 'Regiomontanus pag. 175' has not been resolved "
                "to a verified independent work/page; do not assume it refers to PDF "
                "page 175 of Lilly."
            ),
            (
                "The original recipe cannot infer a unique actual father birth "
                "date/time without external independent birth-time evidence; no "
                "proven father natal recovery."
            ),
            (
                "Lilly's 'used by excellent astrologians' is an uncorroborated "
                "authorial report, not blind validation."
            ),
            (
                "No human parent-child affection outcomes, actual father birth "
                "documents, ephemeris source-mode parity or timing control panels "
                "were inspected."
            ),
            (
                "Printed CXXVII about minerals/mines begins PDF609 after a divider, "
                "and an unnumbered sixth-house illness source begins PDF610. Do not "
                "absorb them into CXXVI."
            ),
            (
                "Full diplomatic first-edition transliteration, complete "
                "mathematical source proofs and independent scientific predictive "
                "validity remain open."
            ),
        ],
        "regiomontanus_math_status": proc["procedure_status"],
        "father_birth_time_recoveries_validated": 0,
        "human_relationship_validations": 0,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06b",
        "status": "FIRST_EDITION_ORIGINAL_PARENT_NATIVE_AND_REGIOMONTANUS_HISTORY",
        "printed_chapter": "CXXVI",
        "editorial_chapter": "CXXVII",
        "record_count": 46,
        "first_record": "R7503",
        "last_record": "R7548",
        "substantive_source_annotations": 44,
        "following_navigation": 2,
        "source_groups": 10,
        "body_pdf_frames": [608, 609],
        "next_heading_frame": 609,
        "full_diplomatic_transcription": False,
        "regiomontanus_procedure_executable": False,
        "regiomontanus_original_crosschecked": False,
        "empirical_validations": 0,
        "independent_father_birth_time_validations": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06b",
        "status": "FIRST_EDITION_SOURCE_ONLY_LOCALLY_FROZEN_PENDING_REMOTE",
        "previous_lilly": 7502,
        "new_historical_records": 46,
        "lilly_if_published": 7548,
        "ptolemy_retained": 1066,
        "combined_if_published": 8614,
        "substantive": 44,
        "navigation": 2,
        "source_groups": 10,
        "next_printed": "CXXVII",
        "next_pdf_frame": 609,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "regiomontanus_source_sha256": sha(B / "REGIOMONTANUS_HISTORICAL_PROCEDURE_V1.json"),
        "independent_father_datetime_recoveries": 0,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06b original source R7503-R7548 46 notes, no astronomical family validation")
