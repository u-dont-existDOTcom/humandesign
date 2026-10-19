#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve source-specific phrases without cropping.
"""Exact pinned Zi Wei Volume II source auxiliary star lists & five bureau grids.

The transmitted raw source has original Chinese entries with separate proof
offsets and SHA. The source's five tabular bureau grids are preserved with
byte-equivalent original formatting, never interpreted as 30 verified birth
day/star/palace placements or actual-human outcomes.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
P = B.parents[1]
INDEX = P / "CHINESE_SOURCE_AUDIT_INDEX_V6.json"
PREVIOUS = P / "batches/ChineseAstro-04/ZIWEI_VOLUME2_LIFE_BODY_TAXONOMY_SOURCE_NOTES_V1.json"
SOURCE_EXPECTED_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
SOURCE_EXPECTED_BYTES = 106736
OLDID = 1963110
LAST_B04_ANCHOR = "以上自紫微至辅弼一十八星俱南北斗正曜"
EXCLUDED_AUX = "魁钺天马亦是吉星俱不入正曜"
BUREAU_LABELS = ("水二局", "木三局", "金四局", "土五局", "火六局")
AUX_GLOSSES = (
    "The transmitted list gives Kui and Yue stars a Fire classification.",
    "Tian Ma is assigned Fire, outside the preceding eighteen regular stars.",
    "Qing Yang is listed as Metal and an old Northern-Dipper penalty/punishment star.",
    "Tuo Luo is listed as Metal and a Northern-Dipper assisting star marked Ji.",
    "Huo Xing is Fire and a Southern-Dipper assistant.",
    "Ling Xing is Fire and a Southern-Dipper assistant.",
    "Tian Kong and Di Jie are both assigned Fire.",
    "Tian Shang and Tian Shi are listed as Water.",
    "Hua Lu is classified Earth and said to favor meeting Lu Cun.",
    "Hua Quan is classified Wood and said to favor meeting Ju Men and Wu Qu.",
    "Hua Ke is classified Water and said to favor meeting Kui/Yue.",
    "Hua Ji is classified Water and textually identified as Ji Du/Ketu.",
    "Hong Luan and Tian Xi are classified Water.",
    "Sui Jun is classified Fire.",
    "Bo Shi is Water, linked rhetorically with cleverness.",
    "Li Shi is Fire, associated with rank/power imagery.",
    "Qing Long is Wood, linked rhetorically with joy.",
    "Da/Xiao Hao are Fire, with claims about money loss/estate depletion.",
    "Jiang Jun is Wood, with martial and social-fit symbolism.",
    "Zou Shu is Metal, linked rhetorically with status/fortune.",
    "Fei Lian is Fire, with a solitude claim.",
    "Xi Shen is Fire, with joy symbolism.",
    "Fu Bing is Fire, with oral dispute/accusation symbolism.",
    "Bing Fu has an old illness claim but no quoted elemental assignment.",
    "Guan Fu is assigned a juridical allegation; distinguish 官府 from 官符.",
    "Sang Men has the Wood label.",
    "Diao Ke has the Fire label.",
    "Bai Hu has the Metal label.",
    "Guan Fu (官符) has the Fire label; keep separate from preceding 官府.",
)
BUREAU_POEM_GLOSSES = (
    "Water-two bureau verse starts first and second day at Chou and Yin and states forward steps; no full natal time engine.",
    "Wood-three bureau verse begins day1 at Dragon/Chen, day2 at Ox/Chou and gives reversal/forward sequences.",
    "Metal-four bureau verse gives day1 Pig/Hai and day2 Dragon/Chen starts, with forward/back movement.",
    "Earth-five bureau verse gives day1 Horse/Wu and day2 Pig/Hai and exceptions for selected days.",
    "Fire-six bureau verse mentions day2 Horse/Wu and day4 Dragon/Chen with alternating complex movements.",
)


def sha(x):
    return hashlib.sha256(x).hexdigest()


def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8"))


def save(file, value):
    Path(file).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze(raw_file):
    raw = Path(raw_file).read_bytes()
    assert len(raw) == SOURCE_EXPECTED_BYTES
    assert sha(raw) == SOURCE_EXPECTED_SHA
    text = raw.decode("utf-8")
    original = load(PREVIOUS)
    idx = load(INDEX)
    assert idx["sum_source_annotations"] == 315
    assert idx["systems"][0]["accepted_source_annotations"] == 154
    assert idx["systems"][1]["next_id"] == "ZWD-R0162"
    assert original["records"][-1]["id"] == "ZWD-R0161"
    assert original["records"][-1]["original_chinese_anchor"] == LAST_B04_ANCHOR
    start = text.index(LAST_B04_ANCHOR) + len(LAST_B04_ANCHOR)
    assert start > 3800
    segment = text[start:]
    intro = segment.find(EXCLUDED_AUX)
    assert 0 <= intro < 20
    poems = list(re.finditer(r"<poem>(.*?)</poem>", segment, re.S))
    assert len(poems) >= 6
    aux_lines = [line.strip() for line in poems[0].group(1).splitlines() if line.strip()]
    assert len(aux_lines) == len(AUX_GLOSSES) == 29
    poems_bureaus = poems[1:6]
    diagram_spans = []
    for i, (poem, label) in enumerate(zip(poems_bureaus, BUREAU_LABELS, strict=True)):
        next_poem_start = poems[i + 2].start() if i + 2 < len(poems) else len(segment)
        between = segment[poem.end() : next_poem_start]
        dm = re.search(r"<nowiki>(.*?)</nowiki>", between, re.S)
        assert dm is not None, (label, i)
        diagram_start = start + poem.end() + dm.start()
        diagram_end = start + poem.end() + dm.end()
        grid = text[diagram_start:diagram_end]
        assert label in grid, (label, grid[:90])
        assert grid.startswith("<nowiki>") and grid.endswith("</nowiki>")
        assert len(grid) > 550
        diagram_spans.append(
            {
                "bureau": label,
                "original_codepoint_start": diagram_start,
                "original_codepoint_end": diagram_end,
                "original_utf8_sha256": sha(grid.encode("utf-8")),
                "original_utf8_bytes": len(grid.encode("utf-8")),
                "diagram_content": grid,
                "source_day_to_palace_original_diagram_interpretation_verified": False,
            }
        )
    excerpt_end = diagram_spans[-1]["original_codepoint_end"]
    excerpt = text[start:excerpt_end]
    assert len(excerpt) > 6000
    (B / "SOURCE_1963110_AUXILIARY_AND_BUREAU_EXCERPT.txt").write_text(excerpt, encoding="utf-8")
    digest = sha(excerpt.encode("utf-8"))

    items = [
        (
            "auxiliary_status",
            EXCLUDED_AUX,
            "Kui/Yue and Tian Ma are called auspicious but excluded from the preceding eighteen regular stars.",
            None,
        )
    ]
    items.extend(
        ("aux_star", name, gloss, None) for name, gloss in zip(aux_lines, AUX_GLOSSES, strict=True)
    )
    for poem, label, gloss, _diagram in zip(
        poems_bureaus, BUREAU_LABELS, BUREAU_POEM_GLOSSES, diagram_spans, strict=True
    ):
        words = poem.group(1).strip()
        items.append(("bureau_poem", words, gloss, label))
        items.append(
            (
                "bureau_original_grid",
                label,
                f"Original diagram headed {label} is preserved exactly but not mechanically decoded.",
                label,
            )
        )
    assert len(items) == 1 + 29 + 5 * 2 == 40
    notes = []
    receipts = []
    for n, (kind, anchor, gloss, bureau) in enumerate(items):
        pos = text.find(anchor, start, excerpt_end)
        assert pos >= start, (kind, anchor)
        rid = f"ZWD-R{162 + n:04d}"
        token_sha = sha(anchor.encode("utf-8"))
        grid = next((g for g in diagram_spans if g["bureau"] == bureau), None)
        note = {
            "id": rid,
            "source": "ZWDS-CLASSIC-01",
            "locator": "紫微斗數全書/卷二 original oldid1963110 after regular 18-star classification",
            "source_revision_id": OLDID,
            "source_original_verbatim_chinese_anchor": anchor,
            "source_type": kind,
            "elemental_bureau_id": bureau,
            "source_historical_meaning_not_personal_result": gloss,
            "source_original_full_revision_sha256": SOURCE_EXPECTED_SHA,
            "original_full_source_character_offset": pos,
            "original_full_source_utf8_byte_offset": len(text[:pos].encode("utf-8")),
            "original_excerpt_relative_character_offset": pos - start,
            "original_quote_utf8_SHA256": token_sha,
            "source_original_bureau_grid_full_utf8_SHA256": grid["original_utf8_sha256"]
            if kind == "bureau_original_grid"
            else None,
            "source_original_early_print_authenticity_verified": False,
            "source_traditional_day_to_palace_bureau_engine_verified": False,
            "source_original_good_illness_crime_wealth_omens_personal_accuracy": False,
            "source_full_lunisolar_leapmonth_birth_engine_verified": False,
            "independently_validated_real_human_prediction": False,
            "runtime_promoted": False,
        }
        notes.append(note)
        receipts.append(
            {
                "id": rid,
                "full_original_source_sha256": SOURCE_EXPECTED_SHA,
                "original_codepoint_offset": pos,
                "relative_excerpt_codepoint_offset": pos - start,
                "verbatim_chinese": anchor,
                "utf8_quote_sha256": token_sha,
                "original_full_source_byte_offset": note["original_full_source_utf8_byte_offset"],
                "source_type": kind,
                "original_daygrid_full_sha256": note[
                    "source_original_bureau_grid_full_utf8_SHA256"
                ],
            }
        )
    assert [r["id"] for r in notes] == [f"ZWD-R{i:04d}" for i in range(162, 202)]
    assert sum(r["source_type"] == "aux_star" for r in notes) == 29
    assert sum(r["source_type"] == "bureau_poem" for r in notes) == 5
    assert sum(r["source_type"] == "bureau_original_grid" for r in notes) == 5

    result = {
        "schema": "ZWDS_VOLUME_II_AUXILIARY_29_STARS_FIVE_BUREAU_SOURCE_DIAGRAMS_V1",
        "batch": "ChineseAstro-07",
        "pinned_original_volume2_raw_oldid": OLDID,
        "pinned_original_volume2_full_raw_SHA256": SOURCE_EXPECTED_SHA,
        "pinned_original_volume2_full_raw_bytes": SOURCE_EXPECTED_BYTES,
        "original_text_segment_absolute_start_codepoint": start,
        "original_text_segment_absolute_end_codepoint": excerpt_end,
        "full_original_excerpt_SHA256": digest,
        "original_source_excerpt_bytes": len(excerpt.encode("utf-8")),
        "original_18_regular_stars_source_boundary_preserved": True,
        "original_auxiliary_star_source_lines": 29,
        "five_original_elemental_bureau_poems": 5,
        "five_original_unparsed_bureau_day_grid_diagrams": 5,
        "source_historical_annotation_count": len(notes),
        "first_id": "ZWD-R0162",
        "last_id": "ZWD-R0201",
        "next_id": "ZWD-R0202",
        "earliest_original_woodblock_attribution_verified": False,
        "separate_independent_classical_Chinese_expert_review": False,
        "original_diagrams_decode_consistency_verified": False,
        "original_lunisolar_year_to_birth_date_hour_verified": False,
        "independent_real_person_predictions_validated": 0,
        "runtime_promotions": 0,
        "record_rows": notes,
    }
    proof = {
        "schema": "ZWDS_VOLUME_II_RAW_1963110_AUX_STARS_FIVE_BUREAU_WITNESS_V1",
        "batch": "ChineseAstro-07",
        "whole_raw_original_SHA256": SOURCE_EXPECTED_SHA,
        "raw_source_revision_id": OLDID,
        "excerpt_SHA256": digest,
        "excerpt_start_codepoint": start,
        "excerpt_end_codepoint": excerpt_end,
        "original_anchor_count": 40,
        "diagram_count": 5,
        "all_original_chinese_source_anchors_matched": True,
        "original_visual_tables_not_calendar_chart_engine": True,
        "actual_people_predictions_validated": 0,
        "runtime_promotions": 0,
        "diagram_reversible_witnesses": diagram_spans,
        "quote_receipts": receipts,
    }
    save(B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json", result)
    save(B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json", proof)
    print(
        json.dumps(
            {
                "new_ZWD_source_notes": len(notes),
                "auxiliary_lines": 29,
                "bureau_poems": 5,
                "original_grids": 5,
                "excerpt_start": start,
                "excerpt_end": excerpt_end,
                "excerpt_sha256": digest,
                "notes_sha256": sha(
                    (B / "ZIWEI_VOLUME2_AUX_STARS_FIVE_BUREAU_40_SOURCE_NOTES_V1.json").read_bytes()
                ),
                "witness_sha256": sha(
                    (B / "SOURCE_1963110_AUXILIARY_BUREAU_WITNESS_V1.json").read_bytes()
                ),
                "next": "ZWD-R0202",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-pinned-wikitext", type=Path, required=True)
    freeze(parser.parse_args().full_pinned_wikitext)
