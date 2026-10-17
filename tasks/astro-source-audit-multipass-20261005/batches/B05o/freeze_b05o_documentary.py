#!/usr/bin/env python3
"""Original-source Lilly wealth-origin chapter: historical text, not prediction proof."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, data):
    (B / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


logic = j("SOURCE_FIRST_LOGIC_AUTHORING_20261017.json")
matrix = j("SOURCE_FIRST_CLASSIFICATION_MATRIX_20261017.json")
assert logic["batch"] == matrix["batch"] == "B05o"
assert logic["printed_chapter"] == matrix["chapter_original_printed"] == "CXV"
assert logic["body_original_pdf_frames"] == list(range(588, 595))
assert len(logic["groups"]) == 9
assert len(matrix["planets"]) == 7
assert len(matrix["elements"]) == 4
assert len(matrix["planetary_natures"]) == 6
assert [r["no"] for r in matrix["houses"]] == list(range(1, 13))
rows, reverse = [], []


def add(sid, page_list, kind, label, items=None, extra=None, anchor=None, meaning=None):
    no = 6911 + len(rows)
    key = f"R{no}"
    assert set(page_list) <= set(range(588, 595))
    record = {
        "id": key,
        "record_number": no,
        "batch": "B05o",
        "source_span": sid,
        "original_pdf_frames": page_list,
        "role": kind,
        "source_label": label,
        "original_anchor_not_diplomatic": anchor,
        "meaning_historical_only": meaning,
        "source_items_normalized_not_diplomatic": items or [],
        "source_item_count": len(items or []),
        "source_metadata": extra or {},
        "historical_documentary_accepted": True,
        "full_diplomatic_transcription": False,
        "independently_validated_human_financial_result": False,
        "validated_person_occupational_or_moral_inference": False,
        "clinical_or_economic_action_authorized": False,
        "promoted_as_executable_runtime_rule": False,
    }
    rows.append(record)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": page_list,
            "source_role": kind,
            "record_id": key,
            "number_of_source_items": len(items or []),
        }
    )


def add_logic(groups):
    for group in groups:
        for c in group["claims"]:
            add(
                sid=f"{group['source_span']}-{c['id']}",
                page_list=group["original_pdf_frames"],
                kind=c["role"],
                label=group["source_group"],
                extra={"authoring_claim_id": c["id"], "qualification": c["qualification"]},
                anchor=c["anchor_not_diplomatic"],
                meaning=c["meaning_historical_only"],
            )


# First original CXV heading and the numbered four source dimensions.
add_logic(logic["groups"][:3])
# Seven original planet labels, each with distinct matters and persons cells.
for planet in matrix["planets"]:
    name = planet["name"]
    for aspect in ("matters", "persons"):
        words = planet["source_cells"][aspect]
        assert words and len(set(words)) == len(words)
        add(
            sid=f"B05o-PL-{name.upper()}-{aspect.upper()}",
            page_list=[planet["pdf_page"]],
            kind=f"planet_{aspect}_cell",
            label=f"{name}: original planet table {aspect}",
            items=words,
            extra={
                "planet": name,
                "cell_type": aspect,
                "cross_reference": planet.get("source_cross_reference"),
            },
            meaning=(
                "Period 1647 matter/person stereotypes attributed to the named "
                "planet as possible estate/loss sources; not an independently "
                "verified classification of actual people or occupations."
            ),
        )
# Then the original sign and house classification introductions.
add_logic(logic["groups"][3:4])
for element in matrix["elements"]:
    add(
        sid=f"B05o-ELEMENT-{element['name'].upper()}",
        page_list=[element["pdf_page"]],
        kind="zodiac_element_cell",
        label=f"{element['name']} sign grouping: means of wealth",
        items=element["items"],
        extra={"element": element["name"]},
        meaning="Traditional sign-element source attribution, not a modern causal inference.",
    )
for nature in matrix["planetary_natures"]:
    add(
        sid=f"B05o-NATURE-{nature['name'].upper()}",
        page_list=[nature["pdf_page"]],
        kind="planetary_sign_nature_cell",
        label=f"{nature['name']} zodiacal/planetary nature category",
        items=nature["items"],
        extra={"nature": nature["name"]},
        meaning="Traditional sign or planetary nature attribution, not observed finance.",
    )
for house in matrix["houses"]:
    add(
        sid=f"B05o-HOUSE-{house['no']:02d}",
        page_list=[house["pdf_page"]],
        kind="house_classification_cell",
        label=f"House {house['no']}: person, matter and source categories",
        items=house["items"],
        extra={"house": house["no"]},
        meaning="Original source categorization for a natal house; no validation on people.",
    )
# Finally Lilly's combination rules and the NEXT chapter navigation.
add_logic(logic["groups"][4:])
assert len(rows) == 84
assert [r["record_number"] for r in rows] == list(range(6911, 6995))
assert sum(r["role"].startswith("planet_") and r["role"].endswith("_cell") for r in rows) == 14
assert sum(r["role"] == "zodiac_element_cell" for r in rows) == 4
assert sum(r["role"] == "planetary_sign_nature_cell" for r in rows) == 6
assert sum(r["role"] == "house_classification_cell" for r in rows) == 12
assert [r["id"] for r in rows if r["role"] == "next_chapter_navigation"] == ["R6993", "R6994"]
assert sum(r["source_item_count"] for r in rows) == 316
assert len({r["id"] for r in rows}) == 84
assert len({r["source_span"] for r in rows}) == 84

images = {}
original_folios = {
    588: "554",
    589: "555",
    590: "556",
    591: "557",
    592: "558",
    593: "559",
    594: "561",
    595: "561",
    596: "562",
}
for n in range(588, 597):
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 200000
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "original_printed_folio": original_folios[n],
        "role": ("chapter_body" if n <= 594 else "next_chapter_context"),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05o",
        "source": "Wellcome b30338724, first edition William Lilly 1647",
        "full_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "original_chapter_pdf_frames": list(range(588, 595)),
        "following_printed_chapter_CXVI_heading_pdf": 594,
        "folio_note": (
            "PDF594 original folio visibly reads 561 after PDF593 printed559; "
            "PDF595 is also printed561, a duplicated folio. Text and "
            "source-image sequence are continuous; never reorder by folio."
        ),
        "source_page_sequence_contiguous": True,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05o",
        "record_count": 84,
        "source_groups": reverse,
        "planet_person_matter_cells": 14,
        "zodiac_element_cells": 4,
        "planetary_nature_cells": 6,
        "house_cells": 12,
        "free_prose_or_navigation_claims": 48,
        "normalized_item_count": 316,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05o",
        "historical_only": True,
        "issues": [
            (
                "The 316 matrix items are normalized interpretations of original "
                "source terms, not separate empirical observations, direct quotations "
                "or a full diplomatic transcription."
            ),
            (
                "The 1647 author groups planet-associated persons and occupations "
                "using era-specific class, religion, gender, criminality and morality "
                "stereotypes. Those are not legitimate classifications of any living "
                "person."
            ),
            (
                "The seven planetary person/matter cells and the separate six "
                "sign-related planetary-nature classes are different tables. Do not "
                "merge or mistake absence of a lunar sign-nature row for omitted lunar "
                "person/matter entries."
            ),
            (
                "Exact sign and house calculations, zodiac elements, partile aspect "
                "thresholds and planet dignities must be frozen with astronomy and "
                "17th-century calendar assumptions before any future human test."
            ),
            (
                "Planet, sign, house and partile aspect are different dimensions of "
                "the source method, not four independently corroborating observational "
                "studies."
            ),
            (
                "The source explicitly acknowledges rare all-favorable natal "
                "testimonies, frequent mixtures, losses despite strong general wealth "
                "configurations and gains despite strong unfavorable configurations; "
                "no ad hoc rescues allowed in prospective tests."
            ),
            (
                "The example of the third house assigning potential loss to a "
                "brother/kinsman is not independently observed and cannot justify a "
                "claim about a person's relatives."
            ),
            (
                "The author refers to the condition in which ancestors left a person "
                "as a baseline; real tests must compare against socioeconomic origins "
                "and mobility without astrology."
            ),
            (
                "Period age, birthplace, social hierarchy, vocation, gender, trade and "
                "access to property are confounders. They must not be treated as "
                "astrological causal results."
            ),
            (
                "The time-varying source claims have no quantitative event-date "
                "precision, net-worth thresholds, or outcome windows and cannot be "
                "used for actual investment decisions."
            ),
            (
                "Some historical spelling and printed glyphs remain subject to "
                "independent specialist transcription; all item lists carry "
                "normalized-not-diplomatic flags."
            ),
            (
                "Following printed CHAP CXVI starts on original PDF594. It concerns "
                "lawful or unlawful means of wealth, and its substantive clauses are "
                "not included as if they belonged to printed CXV."
            ),
            (
                "Source-first claim and matrix preservation does not create an "
                "executable validated astrological model or make 316 correct "
                "predictions."
            ),
        ],
        "empirical_validations": 0,
        "independent_human_financial_outcomes": 0,
        "clinical_or_moral_advice_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B05o",
        "status": "ORIGINAL_1647_HISTORICAL_SOURCE_LOCALLY_ADMITTED_ONLY",
        "original_printed_chapter": "CXV",
        "editorial_chapter": "CXVI",
        "record_count": 84,
        "first_record": "R6911",
        "last_record": "R6994",
        "source_body_pdf_frames": list(range(588, 595)),
        "next_heading_frame": 594,
        "planet_cells": 14,
        "zodiac_element_cells": 4,
        "planetary_sign_nature_cells": 6,
        "house_cells": 12,
        "substantive_prose_claims": 46,
        "next_chapter_navigation_units": 2,
        "source_normalized_items": 316,
        "original_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independently_verified_wealth_outcomes": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
accept = {
    "batch": "B05o",
    "status": "SOURCE_FIRST_HISTORICAL_LOCALLY_FROZEN_PENDING_REMOTE",
    "previous_lilly": 6910,
    "new_source_annotations": 84,
    "lilly_if_published": 6994,
    "ptolemy_retained": 1066,
    "combined_if_published": 8060,
    "source_groups": 84,
    "logic_annotations": 48,
    "structured_source_cells": 36,
    "normalized_cell_items": 316,
    "substantive_annotations": 82,
    "next_heading_navigation": 2,
    "original_pdf_witnesses": list(range(588, 597)),
    "following_printed_chapter": "CXVI",
    "following_heading_original_pdf": 594,
    "rules_sha256": sha(B / "RULES.json"),
    "source_logic_sha256": sha(B / "SOURCE_FIRST_LOGIC_AUTHORING_20261017.json"),
    "source_matrix_sha256": sha(B / "SOURCE_FIRST_CLASSIFICATION_MATRIX_20261017.json"),
    "empirical_validations": 0,
    "human_wealth_accuracy_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
write("ACCEPTANCE.json", accept)
print(json.dumps(accept, indent=2))
