#!/usr/bin/env python3
"""Original William Lilly 1647 mining speculation as historical source only."""

import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent


def load(name):
    return json.loads((B / name).read_text())


def save(name, data):
    (B / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


a = load("SOURCE_FIRST_AUTHORING_20261017.json")
assert a["batch"] == "B06c"
assert a["printed_chapter"] == "CXXVII"
assert a["original_body_pdf_frames"] == [609]
assert len(a["groups"]) == 9
rows, reverse = [], []
for index, group in enumerate(a["groups"], 1):
    sid = f"B06c-S{index:03d}"
    assert group["source_span"] == sid
    assert set(group["original_pdf_frames"]) <= {609, 610}
    ids = []
    for claim in group["claims"]:
        no = 7549 + len(rows)
        rid = f"R{no}"
        assert claim["id"] == rid
        assert len(claim["anchor_not_diplomatic"]) >= 5
        assert len(claim["historical_meaning"]) >= 45
        assert not claim["actual_mining_investment_outcome_verified"]
        assert not claim["runtime_promoted"]
        rows.append(
            {
                "id": rid,
                "record_number": no,
                "source_span": sid,
                "original_pdf_frames": group["original_pdf_frames"],
                "role": claim["role"],
                "original_anchor_not_diplomatic": claim["anchor_not_diplomatic"],
                "historical_only_meaning": claim["historical_meaning"],
                "qualification": claim["source_qualification"],
                "historical_documentary_accepted": True,
                "independent_mining_finance_prediction_validated": False,
                "actual_ore_or_mineral_deposit_validated": False,
                "modern_legal_financial_or_mining_advice_authorized": False,
                "runtime_rule_promoted": False,
            }
        )
        ids.append(rid)
    reverse.append(
        {
            "source_span": sid,
            "original_pdf_frames": group["original_pdf_frames"],
            "source_group": group["subject"],
            "mapped_ids": ids,
        }
    )
assert len(rows) == 35
assert [r["record_number"] for r in rows] == list(range(7549, 7584))
assert [r["id"] for r in rows if r["role"] == "next_section_navigation"] == ["R7582", "R7583"]
images = {}
for n in [609, 610, 611, 612]:
    p = B / "evidence" / f"pdf_1647-{n}.jpg"
    raw = p.read_bytes()
    assert len(raw) > 150000 and raw[:2] == bytes.fromhex("ffd8")
    images[str(n)] = {
        "file": str(p.relative_to(B)),
        "bytes": len(raw),
        "sha256": sha(p),
        "printed_folio": str(n - 34),
        "role": "mining_chapter" if n == 609 else "following_sixth_house_context",
    }
save(
    "ORIGINAL_SOURCE_WITNESS.json",
    {
        "batch": "B06c",
        "source": "Lilly Christian Astrology 1647 first edition Wellcome b30338724",
        "original_volume_pdf_sha256": (
            "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
        ),
        "source_body_pdf_frame": 609,
        "following_unnumbered_sixth_house_start_frame": 610,
        "images": images,
    },
)
save(
    "SOURCE_TO_RECORD_MAP.json",
    {
        "batch": "B06c",
        "source_groups": reverse,
        "groups_count": 9,
        "record_count": 35,
        "substantive_records": 33,
        "following_section_navigation": 2,
    },
)
save(
    "UNRESOLVED_SOURCE_LIMITS.json",
    {
        "batch": "B06c",
        "issues": [
            (
                "Seventeenth-century mine/metal-wealth forecasts do not establish "
                "geology, property deposits, mining returns or sound investments."
            ),
            (
                "Saturn being fourth ruler OR fourth occupant is an original "
                "alternative, not two independent supporting observations."
            ),
            (
                "The strong Saturn wealth case requires essential dignity, "
                "directness, swiftness and a favorable contact to traditional "
                "benefics; do not simplify to Saturn in fourth alone."
            ),
            (
                "The author scales expected mineral profits by planetary potency, "
                "but provides neither a numerical forecast nor an objective economic "
                "baseline."
            ),
            (
                "Reception of fourth ruler by luminaries OR by their dispositor, "
                "with mutual reception, has complex conjunction/alternative scope "
                "and requires source-faithful coding."
            ),
            (
                "The Jupiter-in-fourth/Libra tin category and family inheritance "
                "outcome are two interpretations of one natal premise, not "
                "independent evidence."
            ),
            (
                "Saturn Aquarius in fourth plus Jupiter Libra, and Mars Leo in "
                "fourth plus Sun Aries, are compound sign configurations; both "
                "components must be retained."
            ),
            (
                "The final coal/lead ore branch requires Saturn in earth sign and "
                "good Sun/Mars/Mercury aspect and ambiguous fourth-house occupancy "
                "versus aspect condition."
            ),
            (
                "Source lists gold, silver, iron, tin, lead, coal, quarry stones as "
                "alternative mining outcomes, increasing retrospective fit "
                "flexibility."
            ),
            (
                "No independent mined samples, ore grades, capital investment "
                "returns, mine dates, historical commercial cases or matched decoy "
                "charts are provided."
            ),
            (
                "The following unnumbered sixth-house source on ailments begins "
                "original PDF610 and must be studied separately with stronger "
                "medical-risk guardrails."
            ),
            (
                "Original 1647 imagery, selective anchors and qualifications "
                "preserved; no complete diplomatic transcription or scientific proof "
                "of astrology."
            ),
        ],
        "economic_predictions_validated": 0,
        "investment_advice_authorized": False,
        "runtime_promotions": 0,
    },
)
save(
    "RULES.json",
    {
        "batch": "B06c",
        "status": "ORIGINAL_1647_MINING_WEALTH_HISTORICAL_ONLY",
        "printed_chapter": "CXXVII",
        "editorial_chapter": "CXXVIII",
        "record_count": 35,
        "first_record": "R7549",
        "last_record": "R7583",
        "substantive_historical_records": 33,
        "next_unnumbered_source_navigation": 2,
        "original_body_frame": 609,
        "next_unnumbered_sixth_house_frame": 610,
        "source_groups": 9,
        "diplomatic_transcription_complete": False,
        "empirical_validations": 0,
        "human_mining_outcomes_validated": 0,
        "runtime_promotions": 0,
        "rules": rows,
    },
)
save(
    "ACCEPTANCE.json",
    {
        "batch": "B06c",
        "status": "FIRST_EDITION_HISTORIC_SOURCE_LOCALLY_FROZEN",
        "previous_lilly": 7548,
        "new_historical_records": 35,
        "lilly_if_published": 7583,
        "ptolemy_retained": 1066,
        "combined_if_published": 8649,
        "substantive": 33,
        "navigation": 2,
        "source_groups": 9,
        "next_section": "UNNUMBERED_SIXTH_HOUSE_INFIRMITIES",
        "next_pdf_frame": 610,
        "rules_sha256": sha(B / "RULES.json"),
        "independent_mining_outcome_validations": 0,
        "empirical_validations": 0,
        "runtime_promotions": 0,
        "remote_published": False,
    },
)
print("B06c mining source 35 historical notes R7549-R7583, empirical zero")
