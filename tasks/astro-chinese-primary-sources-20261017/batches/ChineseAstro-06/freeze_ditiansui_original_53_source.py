#!/usr/bin/env python3
# ruff: noqa: E501  # Original source/qualification sentences preserved.
"""Freeze exact 53 text anchors from six independently pinned Di Tian Sui pages.

The source raw revision is a *transmitted online document*, not an authenticated
early printing. The candidate English glosses are later interpretation; preserve
exact Chinese verse/commentary, source offset, byte hash, page and revision.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parent
PAGES = B / "DITIAN_SUI_ADDITIONAL_PINNED_PAGES_MANIFEST_V1.json"
CANDIDATES = B / "SOURCE_CANDIDATES_UNVERIFIED_V1.json"
NOTES = B / "BAZI_DITIAN_SUI_FORMATIONS_TRANSFORMATIONS_53_NOTES_V1.json"
WITNESS = B / "PINNED_DI_TIAN_SUI_SIX_PAGE_53_ANCHOR_WITNESS_V1.json"
PARTS = ("04", "05", "07", "08", "11", "12")
CONDITIONS = {
    "04": "Needs whole birth pillars, explicit seasonal qi, and separate luck period before any interpretive rule",
    "05": "Requires a complete natal four-pillar structure and strict distinction of 方 and 局",
    "07": "Requires independent chart verification of all three supported-source and month-command prerequisites",
    "08": "True versus apparent formation depends on hidden support and separately established birth/calendar data",
    "11": "The historical metaphors do not describe measured mental or physical health",
    "12": "The source itself forbids simply mapping one strong/weak element to a universal judgment",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze(source_dir: Path):
    manifest = load(PAGES)
    candidates = load(CANDIDATES)
    assert set(manifest) == set(PARTS)
    assert set(candidates["verse_glosses_by_section"]) == set(PARTS)
    original = {}
    titles = {}
    verses = {}
    for sec in PARTS:
        info = manifest[sec]
        raw = (source_dir / info["raw_file_local"]).read_bytes()
        assert len(raw) == info["source_bytes"], sec
        assert sha(raw) == info["source_sha256"], sec
        t = raw.decode("utf-8")
        original[sec] = t
        a = re.search(r"\{\{Novel\|滴天髓\|([^|]+)\|", t)
        assert a, sec
        titles[sec] = a.group(1)
        v = re.findall(r"\{\{\+\|([^}]*)\}\}", t)
        assert len(v) == info["verse_count"] == len(candidates["verse_glosses_by_section"][sec]), (
            sec
        )
        verses[sec] = v

    planned = []
    for sec in PARTS:
        for verse, gloss in zip(
            verses[sec], candidates["verse_glosses_by_section"][sec], strict=True
        ):
            planned.append((sec, verse, gloss, "TRANSMITTED_VERSE"))
    for item in candidates["commentary_quoted_source_candidates"]:
        sec = item["section"]
        assert sec in PARTS
        planned.append(
            (
                sec,
                item["original_chinese_anchor"],
                item["working_gloss"],
                "TRANSMITTED_COMMENTARY_UNDATED",
            )
        )
    assert len(planned) == 53
    assert sum(layer == "TRANSMITTED_VERSE" for _, _, _, layer in planned) == 15
    assert sum(layer == "TRANSMITTED_COMMENTARY_UNDATED" for _, _, _, layer in planned) == 38
    distinct = {(a, b) for a, b, _, _ in planned}
    assert len(distinct) == 53

    records = []
    proofs = []
    for n, (sec, anchor, gloss, layer) in enumerate(planned):
        raw = original[sec]
        info = manifest[sec]
        assert len(anchor) >= 4 and anchor in raw, (sec, anchor)
        if layer == "TRANSMITTED_COMMENTARY_UNDATED":
            assert not any(anchor == verse for verse in verses[sec]), anchor
        start = raw.index(anchor)
        real_byte_offset = len(raw[:start].encode("utf-8"))
        token_sha = sha(anchor.encode("utf-8"))
        rid = f"BZI-R{102 + n:04d}"
        record = {
            "id": rid,
            "source": "BZI-DITIAN-SUI-WIKISOURCE-PINNED-06",
            "locator": f"滴天髓/{sec} {titles[sec]}",
            "source_section": sec,
            "source_wikisource_oldid": info["wikisource_oldid"],
            "source_full_raw_chapter_sha256": info["source_sha256"],
            "text_layer": layer,
            "original_chinese_anchor_verbatim": anchor,
            "working_English_gloss_not_expert_translation": gloss,
            "source_precondition": CONDITIONS[sec],
            "uncertainty_or_exception": (
                "Historical verse/commentary, author and early physical edition unverified. "
                "Even if literal, not empirical human predictive validation."
            ),
            "source_character_offset": start,
            "source_UTF8_byte_offset": real_byte_offset,
            "original_anchor_UTF8_SHA256": token_sha,
            "original_quote_directly_matched": True,
            "source_original_early_print_verified": False,
            "source_author_verified": False,
            "source_full_four_pillars_calendar_implemented": False,
            "source_claims_about_actual_personality_or_morality_validated": False,
            "source_health_lifespan_or_wealth_prediction_validated": False,
            "independently_validated_real_human_accuracy": False,
            "runtime_promoted": False,
        }
        records.append(record)
        proofs.append(
            {
                "id": rid,
                "section": sec,
                "oldid": info["wikisource_oldid"],
                "whole_raw_source_SHA256": info["source_sha256"],
                "whole_raw_source_bytes": info["source_bytes"],
                "anchor_literal": anchor,
                "anchor_character_offset": start,
                "anchor_UTF8_byte_offset": real_byte_offset,
                "anchor_UTF8_SHA256": token_sha,
                "source_verse_or_commentary": layer,
            }
        )
    assert [r["id"] for r in records] == [f"BZI-R{i:04d}" for i in range(102, 155)]
    out = {
        "schema": "BAZI_DITIAN_SUI_FORMATIONS_FALSE_TRUE_TRANSFORMATIONS_53_SOURCE_NOTES_V1",
        "batch": "ChineseAstro-06",
        "source": "滴天髓 transmitted Chinese Wikisource online revisions",
        "source_physical_authorship_or_early_print_verified": False,
        "pinned_source_manifest_SHA256": sha(PAGES.read_bytes()),
        "pinned_pages": {
            s: {
                "oldid": manifest[s]["wikisource_oldid"],
                "full_raw_SHA256": manifest[s]["source_sha256"],
                "title": titles[s],
            }
            for s in PARTS
        },
        "first_id": "BZI-R0102",
        "last_id": "BZI-R0154",
        "next_id": "BZI-R0155",
        "source_annotations_added": len(records),
        "historical_original_verse_anchors": 15,
        "later_transmitted_commentary_anchor_quotes": 38,
        "source_historical_prognosis_morality_health_claims_are_documentation_only": True,
        "source_bazi_calendar_engine_verified": False,
        "source_historical_interpretation_empirical_reliability_verified": False,
        "independent_real_human_prediction_validations": 0,
        "runtime_promotions": 0,
        "records": records,
    }
    proof = {
        "schema": "BAZI_DITIAN_SUI_SIX_PAGES_53_SHA_OFFSET_WITNESSES_V1",
        "batch": "ChineseAstro-06",
        "original_source_manifest_SHA256": sha(PAGES.read_bytes()),
        "matched_independently_pinned_source_quotes": 53,
        "verse_quotes": 15,
        "commentary_quotes": 38,
        "source_is_original_diplomatic_early_witness": False,
        "independent_expert_Chinese_glosses_validated": False,
        "birthdate_true_solar_time_calculations_validated": False,
        "actual_real_person_outcome_validation_count": 0,
        "runtime_promotions": 0,
        "quote_receipts": proofs,
    }
    write(NOTES, out)
    write(WITNESS, proof)
    print(
        json.dumps(
            {
                "accepted_candidate_sources": len(records),
                "verse": 15,
                "commentary": 38,
                "earliest": records[0]["id"],
                "latest": records[-1]["id"],
                "next": out["next_id"],
                "source_manifest_SHA256": out["pinned_source_manifest_SHA256"],
                "notes_SHA256": sha(NOTES.read_bytes()),
                "witness_SHA256": sha(WITNESS.read_bytes()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-cache", type=Path, default=B / "evidence")
    freeze(parser.parse_args().raw_cache)
