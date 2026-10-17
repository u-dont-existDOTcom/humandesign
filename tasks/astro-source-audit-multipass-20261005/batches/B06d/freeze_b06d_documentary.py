#!/usr/bin/env python3
"""Freeze first-edition Lilly sixth-house medical history, not clinical predictions."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
NEXT_ID = 7584


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def save(name, item):
    (B / name).write_text(json.dumps(item, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


author = load("SOURCE_FIRST_AUTHORING_20261017.json")
tables = load("ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json")
assert author["batch"] == tables["batch"] == "B06d"
assert author["section"] == "UNNUMBERED_SIXTH_HOUSE_INFIRMITIES"
assert author["body_frames"] == list(range(610, 616))
assert author["next_heading_frame"] == 615
assert len(author["prose_groups"]) == 8
assert len(tables["planetary_rows"]) == 7
assert len(tables["zodiac_rows"]) == 12
assert [r["planet"] for r in tables["planetary_rows"]] == [
    "Saturn",
    "Jupiter",
    "Mars",
    "Sun",
    "Venus",
    "Mercury",
    "Moon",
]
assert [r["name"] for r in tables["zodiac_rows"]] == [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]
assert not tables["medical_evidence"] and not tables["clinical_use_authorized"]
assert [q["id"] for q in author["prose_groups"][-1]["claims"]] == ["R7694", "R7695"]
records, reverse = [], []


def append(record):
    no = NEXT_ID + len(records)
    rid = f"R{no}"
    assert record.get("id", rid) == rid
    record["id"] = rid
    record["record_number"] = no
    record["batch"] = "B06d"
    record["historical_documentary_accepted"] = True
    record["independent_human_health_accuracy_validated"] = False
    record["actual_disease_cause_verified"] = False
    record["clinical_diagnosis_or_treatment_authorized"] = False
    record["runtime_model_promoted"] = False
    records.append(record)
    return rid


def add_prose(group):
    mapped = []
    for claim in group["claims"]:
        assert not claim["independent_human_health_accuracy_validated"]
        assert not claim["runtime_promoted"]
        assert len(claim["anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_only_meaning"]) >= 42
        rid = append(
            {
                "id": claim["id"],
                "source_span": group["source_span"],
                "original_pdf_frames": group["source_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "historical_meaning_only": claim["historical_only_meaning"],
                "qualification": claim["qualification"],
                "source_list_items": [],
                "source_item_count": 0,
            }
        )
        mapped.append(rid)
    reverse.append(
        {
            "source_span": group["source_span"],
            "original_pdf_frames": group["source_pdf_frames"],
            "source_group": group["scope"],
            "mapped_record_ids": mapped,
        }
    )


for group in author["prose_groups"][:-1]:
    add_prose(group)
assert len(records) == 84
assert [x["record_number"] for x in records] == list(range(7584, 7668))

for row in tables["planetary_rows"]:
    sid = "B06d-PLANET-" + row["planet"].upper()
    mapped = []
    for role, field in (
        ("planet_body_region_cell", "body"),
        ("planet_historic_ailment_cell", "ailments"),
    ):
        assert row[field] and isinstance(row[field], list)
        mapped.append(
            append(
                {
                    "source_span": sid,
                    "original_pdf_frames": [row["pdf"]],
                    "role": role,
                    "planet": row["planet"],
                    "planet_glyph": row["glyph"],
                    "table_original_column": field,
                    "source_group": "Planet-associated original body/disease matrix",
                    "historical_meaning_only": (
                        "The original 1647 author assigns these named "
                        + field
                        + " to this planet; no clinical correspondence established."
                    ),
                    "qualification": "source_historical_medical_table",
                    "source_note": row["extra"],
                    "source_list_items": row[field],
                    "source_item_count": len(row[field]),
                }
            )
        )
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": [row["pdf"]],
            "source_group": "planet_mapped_body_and_historical_ailment_cells",
            "mapped_record_ids": mapped,
        }
    )

for row in tables["zodiac_rows"]:
    sid = "B06d-ZODIAC-" + row["name"].upper()
    items = row["body"] + row["conditions"]
    rid = append(
        {
            "source_span": sid,
            "original_pdf_frames": [row["pdf"]],
            "role": "zodiac_body_region_cell",
            "sign": row["name"],
            "sign_glyph": row["glyph"],
            "source_group": "One of the twelve sign/body region original rows",
            "historical_meaning_only": (
                "The source attributes bodily regions or historic ailments to "
                "this zodiac sign, not measured clinical or biological effects."
            ),
            "qualification": "historic_anatomical_symbolism",
            "source_note": row["uncertainty"],
            "body_parts": row["body"],
            "historic_conditions": row["conditions"],
            "source_list_items": items,
            "source_item_count": len(items),
        }
    )
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": [row["pdf"]],
            "source_group": "zodiac_source_body_regions_and_conditions",
            "mapped_record_ids": [rid],
        }
    )

assert len(records) == 110
assert [r["record_number"] for r in records[-26:]] == list(range(7668, 7694))
add_prose(author["prose_groups"][-1])
assert len(records) == 112
assert [r["record_number"] for r in records] == list(range(7584, 7696))
assert [r["id"] for r in records if r["role"] == "next_chapter_navigation"] == ["R7694", "R7695"]
assert len(reverse) == 27
assert len({r["id"] for r in records}) == len(records)
assert sum(r["role"] == "planet_body_region_cell" for r in records) == 7
assert sum(r["role"] == "planet_historic_ailment_cell" for r in records) == 7
assert sum(r["role"] == "zodiac_body_region_cell" for r in records) == 12
item_count = sum(r["source_item_count"] for r in records)
assert item_count == 150

images = {}
for n in range(610, 617):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    data = p.read_bytes()
    assert data[:2] == bytes.fromhex("ffd8") and len(data) > 150000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(data),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "source_role": "sixth_house_body" if n <= 615 else "next_eyes_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06d",
        "source": "William Lilly Christian Astrology 1647 original Wellcome b30338724",
        "volume_source_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "source_body_original_frames": [610, 611, 612, 613, 614, 615],
        "next_printed_CHAP_CXXVIII_begin_frame": 615,
        "next_printed_CHAP_CXXVIII_is_distinct": True,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06d",
        "source_groups": reverse,
        "source_group_count": len(reverse),
        "original_prose_passage_groups": 8,
        "planet_table_source_groups": 7,
        "zodiac_sign_source_groups": 12,
        "record_count": 112,
        "substantive_source_records": 110,
        "following_numbered_chapter_navigation": 2,
        "planet_body_region_cells": 7,
        "planet_historical_ailment_cells": 7,
        "zodiac_body_region_cells": 12,
        "total_semantic_source_list_items": item_count,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06d",
        "issues": [
            (
                "This is seventeenth-century "
                "source medicine. None of its natal illness, longevity, "
                "anatomy, psychiatric, speech, sight or fertility assertions "
                "are clinically validated or applicable to a real patient."
            ),
            (
                "The original five health significator categories and "
                "three factors must be considered together; selecting one "
                "after a medical history is seen is retrospective fitting."
            ),
            (
                "Lilly distinguishes a disease significator from the "
                "author or cause of an illness; the latter is a speculative "
                "astrological label, not verified medical causation."
            ),
            (
                "The author claims severity grows with two afflictions, "
                "exact aspects and angular malefics, but gives no clinical "
                "measurement or calibrated likelihood."
            ),
            (
                "A single source first-edition planet table is represented "
                "by two cells per planet (body parts and historical ailments); "
                "the 150 normalized list terms are NOT 150 independent cases."
            ),
            (
                "Saturn, Jupiter, Mars, Sun and Venus table cells begin in "
                "PDF613; Mercury and Moon begin in PDF614. Venus continues "
                "from the original PDF613 page bottom, not a second duplicate."
            ),
            (
                "Jupiter's margin refers to Wind, Stench or Putrefaction "
                "but its exact printing needs specialist verification; "
                "do not silently add reconstructed extra diagnosis terms."
            ),
            (
                "Mercury's historic word that appears to read Ptisick "
                "is uncertain in the original image and is not mapped "
                "to an established modern condition."
            ),
            (
                "The Aries zodiac row mixes head/face parts and historic "
                "conditions, whereas most other signs list body regions; "
                "those distinct semantic fields are retained."
            ),
            (
                "The gender-specific eye laterality for Moon and "
                "premodern labels involving reproduction, mental "
                "capacity, melancholy and humors are period beliefs "
                "and not biological or psychiatric facts."
            ),
            (
                "The 1647 source links whole-life health and mortality "
                "to positions of the Sun; no survival, disease incidence, "
                "or actual patient medical case data are provided."
            ),
            (
                "The original Sun–Moon negative aphorism has an "
                "uncertain aspect glyph; no operator is selected."
            ),
            (
                "Significators above versus below horizon and the "
                "source's house disease cross-reference do not "
                "provide a clinically verified anatomical method."
            ),
            (
                "Historical reference to second-part page245 "
                "is not fully diplomatically compared in this batch; "
                "reuse only as unverified bibliographic pointer."
            ),
            (
                "Several paths can allege both good health and illness "
                "in one chart, with flexible sign/house/planet selection. "
                "No preregistered priority or handling of contradiction."
            ),
            (
                "Source relies on classical humoral diseases, "
                "including many obsolete names; modern equivalences "
                "are not automatically assumed and require expertise."
            ),
            (
                "Original PDF615 first contains the ending of the "
                "unnumbered introduction, then a separate divider "
                "and printed CHAP CXXVIII on eye impairment. "
                "No eye-chapter substantive text is admitted here."
            ),
            (
                "No completed diplomatic transcription or independent "
                "paleographic verification of each historical term. "
                "Source images and selective qualified terms preserved."
            ),
            (
                "No person-level health advice, diagnostic inference, "
                "birth-time rectification, treatment plan, disability "
                "prediction or lifespan forecast is authorized."
            ),
        ],
        "source_terms_normalized_not_verified_human_predictions": item_count,
        "independent_human_clinical_validations": 0,
        "medical_or_treatment_inference_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06d",
        "status": "ORIGINAL_1647_SIXTH_HOUSE_MEDICAL_HISTORY_ONLY_LOCAL_FREEZE",
        "section": "UNNUMBERED_SIXTH_HOUSE_INFIRMITIES",
        "record_count": 112,
        "first_record": "R7584",
        "last_record": "R7695",
        "substantive_source_annotations": 110,
        "next_chapter_navigation": 2,
        "prose_source_annotations": 86,
        "planet_two_cell_records": 14,
        "zodiac_sign_cell_records": 12,
        "normalized_historical_table_items": item_count,
        "body_original_pdf_frames": [610, 611, 612, 613, 614, 615],
        "following_numbered_chapter": "CXXVIII",
        "following_chapter_start_pdf_frame": 615,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independent_human_health_forecasts_validated": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06d",
        "status": "FIRST_EDITION_ORIGINAL_DOCUMENTARY_LOCALLY_FROZEN_PENDING_REMOTE",
        "previous_lilly": 7583,
        "new_historical_source_annotations": 112,
        "lilly_if_published": 7695,
        "ptolemy_retained": 1066,
        "combined_if_published": 8761,
        "substantive": 110,
        "navigation": 2,
        "prose_source_records": 86,
        "structured_table_cells": 26,
        "normalized_source_items": item_count,
        "source_groups": len(reverse),
        "next_original_pdf_frame": 615,
        "next_printed_chapter": "CXXVIII",
        "numbered_chapters_added": 0,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
        "source_matrix_sha256": sha(B / "ORIGINAL_1647_PLANET_SIGN_MEDICAL_TABLES_20261017.json"),
        "empirical_validations": 0,
        "human_clinical_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print(
    "B06d 1647 medical historic source R7584–R7695, "
    "112 records / 150 table items / zero clinical outcomes"
)
