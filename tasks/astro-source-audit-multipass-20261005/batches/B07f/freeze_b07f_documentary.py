#!/usr/bin/env python3
"""Freeze Lilly original 1647 CLI paired horoscopes source as unvalidated history."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def j(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, value):
    (B / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = j("SOURCE_FIRST_AUTHORING_20261018.json")
guard = j("DYAD_HISTORICAL_VALIDATION_GUARD_V1.json")
assert a["batch"] == "B07f"
assert a["printed_chapter"] == "CLI"
assert a["original_body_pdf_frames"] == [671, 672, 673]
assert a["next_section"] == "UNNUMBERED_TWELFTH_HOUSE_ENEMIES"
assert a["next_source_pdf"] == 673
assert a["following_separate_printed"] == "CLIII"
assert a["following_numbered_frame"] == 674
assert not a["printed_CLII_heading_observed"]
assert len(a["groups"]) == 8
assert guard["real_dyad_outcomes_validated"] == guard["runtime_promotions"] == 0
assert not guard["original_glyphs_fully_cross_collated"]

rows, mapdata = [], []
for index, group in enumerate(a["groups"], 1):
    sid = f"B07f-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {671, 672, 673, 674}
    ids = []
    for claim in group["claims"]:
        num = 9927 + len(rows)
        rid = f"R{num}"
        assert claim["id"] == rid
        assert len(claim["original_anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning_only"]) >= 38
        assert claim["source_only"]
        assert not claim["independent_real_dyadic_concord_validated"]
        assert not claim["person_relationship_safety_morality_inference_authorized"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": num,
                "batch": "B07f",
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "anchor_not_diplomatic": claim["original_anchor_not_diplomatic"],
                "historical_source_meaning_only": claim["historical_meaning_only"],
                "qualification": claim["qualification"],
                "documentary_source_accepted": True,
                "independent_real_mutual_affinity_validated": False,
                "independent_real_relationship_duration_validated": False,
                "independent_real_conflict_or_aggression_validated": False,
                "independent_real_asymmetric_affection_validated": False,
                "original_pairwise_chart_geometry_verified": False,
                "real_person_relationship_ethics_or_safety_claim_authorized": False,
                "runtime_model_promoted": False,
            }
        )
        ids.append(rid)
    mapdata.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["topic"],
            "mapped_record_ids": ids,
        }
    )
assert len(rows) == 93
assert [x["record_number"] for x in rows] == list(range(9927, 10020))
assert [
    x["id"]
    for x in rows
    if x["role"] in ("next_unnumbered_navigation", "later_numbered_navigation")
] == ["R10016", "R10017", "R10018", "R10019"]
assert len({x["id"] for x in rows}) == 93

images = {}
for n in range(671, 676):
    path = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 150000
    images[str(n)] = {
        "file": str(path.relative_to(B)),
        "sha256": sha(path),
        "bytes": len(raw),
        "printed_folio": str(n - 34),
        "source_role": (
            "pairwise_CLI_body" if n <= 673 else "following_twelfth_house_and_printed_CLIII_context"
        ),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B07f",
        "original_source": (
            "William Lilly Christian Astrology first edition 1647 Wellcome b30338724"
        ),
        "full_original_1647_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "original_body_pdf_frames": [671, 672, 673],
        "next_unnumbered_twelfth_house_pdf": 673,
        "following_printed_CLIII_pdf": 674,
        "original_intervening_CLII_heading_found": False,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B07f",
        "source_groups": mapdata,
        "source_group_count": 8,
        "record_count": 93,
        "substantive": 89,
        "navigation": 4,
        "validation_guard": "DYAD_HISTORICAL_VALIDATION_GUARD_V1.json",
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B07f",
        "issues": [
            (
                "This printed CLI requires comparing TWO complete independently "
                "calculated natal charts, not a single-person first/eleventh-house "
                "friend count, profession or relative social rank prediction."
            ),
            (
                "Original printed CLI body runs PDF671 lower through PDF673 upper, "
                "where a separate UNNUMBERED twelfth-house Enemies introduction "
                "begins after divider. Following printed CLIII on Enemies begins "
                "PDF674 without a separately observed CLII in studied pages."
            ),
            (
                "The natural 'friend/enemy' lists of planets are source-attributed "
                "and explicitly ASYMMETRIC: Mars calls Venus its friend but Venus "
                "does not reciprocate. A symmetric matrix would distort the source."
            ),
            (
                "Other printed planetary/nodal friendship rows use old glyphs, "
                "including a condensed lunar-node row with unresolved "
                "negative-group membership. Retain uncertainty; "
                "do not invent a complete authoritative friend graph."
            ),
            (
                "The four enumerated source modes of Ascendant-lord concord "
                "are same ruler, received by house/exaltation, conjunction, "
                "or sextile/trine. Failure of all is said to imply brief "
                "friendship, not necessarily lack of initial affection."
            ),
            (
                "Other alternate path uses interchange of Lights/Fortunes "
                "and planets occupying one another's natal places, with "
                "contradictory source strength and pejorative moral explanations."
            ),
            (
                "The text distinguishes mutual agreement, practical utility, "
                "pleasure, exclusive attachment, inconstant friendship, "
                "competitive rivalry, and a later separate question "
                "of which party feels more affection. None are synonyms."
            ),
            (
                "Several source phrases label people wicked, greedy, "
                "injurious or morally bad when malefics exchange positions "
                "or oppose. No actual person intent, crime, danger, "
                "abuse propensity or moral character can be inferred."
            ),
            (
                "The old most-sincere-friend test uses each Ascendant ruler "
                "and benefic/malefic occupants and a directional sinister "
                "sextile/trine; A-loves-B and B-loves-A are not symmetric."
            ),
            (
                "The final categorical claim about one person's Ascendant "
                "falling in the other's sixth/eighth/twelfth "
                "has no independently observed dyads or causal proof."
            ),
            (
                "Source exact orbs, house geometry, zodiac choice, "
                "planetary reception and old aspect operator semantics "
                "are not fully executable or source-cross-collated."
            ),
            (
                "No preregistered paired human charts, actual relationship "
                "history, outcome ages/durations, partner agreement "
                "measures, conflict records or matched baseline evaluated."
            ),
            (
                "The following unnumbered twelfth-house source concerns "
                "enemies and adversaries, separate from two-way CLI "
                "and following printed CLIII on quality of enemies."
            ),
            (
                "This is a photo-anchored historical paraphrase and reversible "
                "source map, not a full diplomatic seventeenth-century "
                "transcription or empirically validated compatibility scorer."
            ),
        ],
        "original_planet_friendship_glyphs_fully_verified": False,
        "original_CLII_printed_heading_found": False,
        "pairwise_affinity_scoring_engine_executable": False,
        "real_person_relationship_predictions_validated": 0,
        "real_person_relationship_risk_or_moral_inferences_authorized": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B07f",
        "status": "ORIGINAL_1647_CLI_TWO_NATIVITY_CONCORD_HISTORY_ONLY",
        "printed_chapter": "CLI",
        "record_count": 93,
        "first_record": "R9927",
        "last_record": "R10019",
        "substantive": 89,
        "following_navigation": 4,
        "source_groups": 8,
        "original_body_pdf_frames": [671, 672, 673],
        "next_unnumbered": "UNNUMBERED_TWELFTH_HOUSE_ENEMIES",
        "following_printed_chapter": "CLIII",
        "following_heading_pdf": 674,
        "intervening_original_CLII_observed": False,
        "empirical_validations": 0,
        "human_relationship_successes_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
write(
    "ACCEPTANCE.json",
    {
        "batch": "B07f",
        "status": "ORIGINAL_PRINTED_CLI_PAIRWISE_SOURCE_LOCALLY_FROZEN",
        "previous_lilly": 9926,
        "new_historical_annotations": 93,
        "lilly_if_published": 10019,
        "ptolemy_retained": 1066,
        "combined_if_published": 11085,
        "substantive": 89,
        "navigation": 4,
        "source_groups": 8,
        "numbered_chapters_added": 1,
        "next_source": "UNNUMBERED_TWELFTH_HOUSE_ENEMIES",
        "next_original_pdf": 673,
        "later_printed_chapter": "CLIII",
        "later_printed_pdf": 674,
        "rules_sha256": sha(B / "RULES.json"),
        "authoring_sha256": sha(B / "SOURCE_FIRST_AUTHORING_20261018.json"),
        "dyad_guard_sha256": sha(B / "DYAD_HISTORICAL_VALIDATION_GUARD_V1.json"),
        "empirical_validations": 0,
        "actual_human_dyad_accuracy_validated": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B07f original CLI dyadic comparison: 93 source notes R9927-R10019.")
