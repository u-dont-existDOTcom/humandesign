#!/usr/bin/env python3
"""Freeze original 1647 Lilly 'Whether the Native shall be Rich' as source history.

Does NOT validate any actual human economic outcome or promote runtime rules.
"""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text(encoding="utf-8"))


def write(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hash_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


source = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert source["batch"] == "B05n"
assert source["printed_chapter"] == "CXIIII"
assert source["editorial_chapter"] == "CXV"
assert source["body_pdf_frames"] == [587, 588]
assert len(source["source_groups"]) == 12
mapping = []
records = []
for index, group in enumerate(source["source_groups"], 1):
    sid = f"B05n-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["pdf_pages"]) <= {587, 588, 589}
    group_ids = []
    for claim in group["claims"]:
        number = 6854 + len(records)
        expected = f"R{number}"
        assert claim["id"] == expected
        assert len(claim["anchor_not_diplomatic"]) >= 7
        assert len(claim["historical_only_meaning"]) >= 55
        assert not (claim["human_financial_prediction_validated"] or claim["runtime_promoted"])
        record = {
            "id": expected,
            "record_number": number,
            "batch": "B05n",
            "source_span": sid,
            "original_pdf_frames": group["pdf_pages"],
            "role": claim["role"],
            "printed_chapter": (
                "CXIIII" if claim["role"] != "next_chapter_navigation" else "CXV_NAVIGATION_ONLY"
            ),
            "editorial_chapter": (
                "CXV" if claim["role"] != "next_chapter_navigation" else "CXVI_NAVIGATION_ONLY"
            ),
            "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
            "historical_source_interpretation": claim["historical_only_meaning"],
            "source_qualification": claim["source_qualification"],
            "historical_documentary_accepted": True,
            "full_diplomatic_transcription": False,
            "independent_economic_outcome_validated": False,
            "tested_wealth_prediction_success": False,
            "financial_advice_authorized": False,
            "runtime_model_promoted": False,
        }
        records.append(record)
        group_ids.append(expected)
    mapping.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["pdf_pages"],
            "passage_group": group["source_topic"],
            "mapped_record_ids": group_ids,
        }
    )
assert len(records) == 57
assert [r["record_number"] for r in records] == list(range(6854, 6911))
nav = [r for r in records if r["role"] == "next_chapter_navigation"]
assert len(nav) == 2
assert [r["id"] for r in nav] == ["R6909", "R6910"]
assert len(mapping) == 12 and len({r["id"] for r in records}) == len(records)

images = {}
folio = {587: "553", 588: "554", 589: "555", 590: "556", 591: "557"}
for n in range(587, 592):
    path = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = path.read_bytes()
    assert raw[:2] == bytes.fromhex("ffd8") and len(raw) > 200000
    images[str(n)] = {
        "pdf_frame": n,
        "path": str(path.relative_to(B)),
        "sha256": hash_file(path),
        "bytes": len(raw),
        "original_printed_folio": folio[n],
        "role": ("chapter_body" if n in (587, 588) else "following_source_context"),
    }
write(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B05n",
        "source": "William Lilly, Christian Astrology 1647 original edition, Wellcome b30338724",
        "full_1647_source_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "body_pages": [587, 588],
        "next_heading_pdf_frame": 588,
        "first_following_chapter": "CXV",
        "following_chapter_has_tables": True,
        "printed_folio_sequence": [folio[n] for n in range(587, 592)],
        "original_source_in_scan_order": True,
        "images": images,
    },
)
write(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B05n",
        "source_groups": mapping,
        "source_group_count": 12,
        "record_count": 57,
        "substantive_claim_count": 55,
        "following_chapter_navigation": 2,
    },
)
write(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B05n",
        "issues": [
            (
                "The chapter inherits second-house, Part of Fortune, intercepted-sign "
                "and Jupiter significators from the unnumbered prior section; these are "
                "not independent new source trials."
            ),
            (
                "Angular placement of all or the greater part plus essential dignity is "
                "a conjunction of tests, not a standalone effect of any one planet."
            ),
            (
                "The relationship between moderately fortified significators and "
                "Regulus/Spica/Fortunes in good houses has ambiguous grammatical scope; "
                "the manuscript does not specify an orb or precise outcome operator."
            ),
            (
                "The phrase 'and so the contrary' following several poverty cases does "
                "not define which combined signs or counterfactuals reverse which "
                "forecast; do not invent an inverse decoder."
            ),
            (
                "Severe poverty wording for a King and multi-branch ruin claims is not "
                "measured economic probability or longitudinal event evidence."
            ),
            (
                "The precise moon/Mars/Saturn angular sentence needs expert "
                "operator-scope review; combining or separating the angular roles "
                "changes the rule substantially."
            ),
            (
                "The glyph in the poverty clause after 'place of the' and the following "
                "glyph (possibly an astrological point/node) are not securely "
                "identified; these were deliberately left unresolved."
            ),
            (
                "The referents 'they cadent' and 'Lord thereof' in the "
                "oppressive-malefic poverty cluster are grammatically uncertain; do not "
                "infer a deterministic medical/financial claim."
            ),
            (
                "Moon/Jupiter first-versus-second-house wealth configurations are true "
                "alternatives and their domicile/dignity requirements may attach only "
                "to the second case."
            ),
            (
                "Sun-Moon trine requires solar exaltation and the absence of "
                "Saturn/Mars affliction; record as a compound condition and maintain "
                "missing-data states."
            ),
            (
                "Eighth-house inheritance testimony has three distinct conditional "
                "patterns involving sect, benefic aspect, house-ruler dignity, Fortune "
                "ruler and Ascendant-ruler aspects; none is real-world inheritance "
                "evidence."
            ),
            (
                "Astrological essential dignities, house geometry, partile aspects and "
                "fixed-star conjunctions require independent reproducible ephemeris and "
                "an explicit freeze before prospective trials."
            ),
            (
                "No stated time window, income/wealth units, age, country, class, "
                "inheritance rate or person-level outcome calibration is given by "
                "Lilly; all empirical performance remains unmeasured."
            ),
            (
                "The original first-edition scans were directly checked; claims are "
                "selective paraphrases, not exhaustive diplomatic transcription or "
                "paleographic proof."
            ),
            (
                "The following CHAP CXV starts on the same PDF588 and should receive "
                "its own detailed planet-person-matter mappings and later sign/house "
                "tables; never subsume its contents here."
            ),
            (
                "No medical, financial, legal, relationship safety or personality "
                "decisions may be based on these unsupported historical claims."
            ),
        ],
        "source_documentary_only": True,
        "independent_human_outcomes_validated": 0,
        "diplomatic_transcription_complete": False,
        "runtime_promotions": 0,
    },
)
write(
    "RULES.json",
    {
        "batch": "B05n",
        "status": "FIRST_EDITION_DOCUMENTARY_HISTORICAL_LOCALLY_ADMITTED",
        "original_printed_chapter": "CXIIII",
        "editorial_chapter": "CXV",
        "record_count": 57,
        "first_record": "R6854",
        "last_record": "R6910",
        "source_passages": 12,
        "substantive_historical_units": 55,
        "following_chapter_navigation_units": 2,
        "body_original_pdf_pages": [587, 588],
        "following_heading_pdf_page": 588,
        "full_diplomatic_transcription": False,
        "empirical_validations": 0,
        "independently_successful_economic_predictions": 0,
        "runtime_promotions": 0,
        "rules": records,
    },
)
accepted = {
    "batch": "B05n",
    "status": "LOCALLY_VERIFIED_HISTORICAL_ONLY_PENDING_PUBLISH",
    "previous_lilly": 6853,
    "new_source_annotations": 57,
    "lilly_if_published": 6910,
    "ptolemy_retained": 1066,
    "combined_if_published": 7976,
    "substantive": 55,
    "navigation": 2,
    "source_image_frames": [587, 588, 589, 590, 591],
    "source_body_original_pdf_frames": [587, 588],
    "following_printed_chapter": "CXV",
    "following_editorial_chapter": "CXVI",
    "following_heading_pdf_frame": 588,
    "original_to_record_group_count": 12,
    "rules_sha256": hash_file(B / "RULES.json"),
    "authoring_sha256": hash_file(B / "SOURCE_FIRST_AUTHORING_20261017.json"),
    "empirical_validations": 0,
    "economic_outcomes_validated": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
write("ACCEPTANCE.json", accepted)
print(json.dumps(accepted, indent=2))
