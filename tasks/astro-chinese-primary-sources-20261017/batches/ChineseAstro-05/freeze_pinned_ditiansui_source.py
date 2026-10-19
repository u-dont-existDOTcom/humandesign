#!/usr/bin/env python3
# ruff: noqa: E501  # Preserve complete English source glosses and exact quotes.
"""Extract first six pinned Di Tian Sui primary-text sections without chart claims.

All quoted Chinese is extracted VERBATIM from exactly revision-hashed source
Wikisource Wikitext. English working meanings are conservative and not an
authenticated old printed edition or independent philological translation.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parent
MANIFEST = B / "DITIAN_SUI_PINNED_SOURCE_MANIFEST_V1.json"
NOTES = B / "BAZI_DITIAN_SUI_SIX_SECTIONS_55_SOURCE_NOTES_V1.json"
WITNESS = B / "SOURCE_REVISION_ANCHOR_WITNESS_V1.json"
CHAPTERS = ["01", "02", "03", "06", "09", "10"]
CHAPTER_NAMES = {
    "01": "通天論",
    "02": "天干論",
    "03": "地支論",
    "06": "格局論",
    "09": "歲運論",
    "10": "體用論",
}
VERSE_GLOSSES = {
    "01": [
        "Introduces three constituent origins as a framework for reading the source's cosmology.",
        "Historical five-phase partiality and wholeness are said to affect auspicious judgments.",
        "Links the human figure with heaven and earth and claims harmony matters.",
        "Calls for understanding favorable and adverse mechanisms rather than literal labels.",
        "Emphasizes qi's advancement and retreat and the need to weigh context.",
        "Proposes examining Heavenly Stem and Earthly Branch combinations to interpret life.",
        "Classifies five yang and five yin stems, with Bing and Gui described as archetypal.",
        "Distinguishes original yin and yang stems' relationship to qi and prevailing momentum.",
    ],
    "02": [
        "Jia Wood is compared with a tall tree and conditioned by heat, moisture and season.",
        "Yi Wood is described as flexible, with conditional fire, tree-support and weather effects.",
        "Bing Fire is described as powerful but differently affected by Metal, Earth and Water.",
        "Ding Fire is milder, with Yi/Ren interactions and seasonal vulnerabilities.",
        "Wu Earth is weighty, prefers moisture in heat, and has branch-clash cautions.",
        "Ji Earth is low/moist soil, whose Fire/Metal and support interactions differ.",
        "Geng Metal is hard, conditional on moisture, Water, Fire and Wood relations.",
        "Xin Metal is softer, with moisture/warmth and accumulated Earth restrictions.",
        "Ren Water is wide-moving, interacting with Metal and Gui and transformed context.",
        "Gui Water is subtle, with a stated Wu combination and actual Fire-root qualification.",
    ],
    "03": [
        "The traditional six yang branches are characterized as rapid and moving.",
        "The six yin branches are described as steadier and longer-acting.",
        "Separates birth, storehouse and defeat places, and qualifies the value of clashes.",
        "Says a branch clash generally matters more than punishment or harm claims.",
        "Discusses concealed clashes and meetings versus overt relationships.",
        "A clash's effects depend on comparative strength, not merely occurrence.",
        "Specifically warns against rigid application of yin/yang life-and-death stages.",
        "Pure heavenly-stem qi still requires adequate earthly-branch bearing.",
        "Three earthly-component structures require covering Heavenly Stem conditions.",
        "Male/yang place is associated with strength with dependent luck-period handling.",
        "Female/yin place is associated with strength with dependent luck-period handling.",
        "Earthly-branch nourishment to day stem may be cut by a clash if day stem is weak.",
        "A strong supporting earthly branch should remain undisturbed in the source model.",
        "Chart vertical elements are said to benefit from compatible relations.",
        "Chart lateral elements are said to benefit from shared intent.",
        "Beginnings/endings and movement across luck phases condition conclusions.",
    ],
    "06": [
        "Differentiates wealth, officer, resource and output chart pattern structures.",
        "Warns not to rigidly elevate remote pattern devices or mixed seasonal categories.",
        "Official and killing-star combinations may be acceptable or unacceptable by condition.",
        "The officer versus hurting-officer relationship depends on actual chart context.",
    ],
    "09": [
        "Distinguishes decade luck and annual influence, asking which wins clash or harmony.",
        "The section asks what constitutes a conflict/battle between luck and year.",
        "The section asks what counts as a branch clash between luck and year.",
        "The section introduces combinations called harmony with direction dependent on favor.",
        "The section distinguishes amity/accord from clash and transformation.",
    ],
    "10": [
        "Warns that body/function (ti/yong) has multiple valid analytical referents, with balancing.",
    ],
}
SOURCE_CAVEATS = {
    "01": "Cosmological historical source claims; no independent human fate tests or lunar calendar.",
    "02": "Ten-stem ecological metaphors are conditional traditional claims, not measured personality.",
    "03": "Branch clash/life-stage interpretations explicitly depend on context, not fixed fatal events.",
    "06": "Month branch, relative strength and other charts conditions must be established separately.",
    "09": "Luck-year interactions are examples, not full chronological prediction without chart parity.",
    "10": "Text differentiates ti/yong by context; no universal static model is licensed.",
}
COMMENTARY = [
    (
        "01",
        "日干為天元，地支為地元，支中所為人元",
        "Distinguishes day stem as heavenly source, branch as earthly source and hidden branch factors as human source.",
        "Requires an independently calculated chart's day stem and branches.",
    ),
    (
        "01",
        "甲，丙，戊，庚，壬，為陽",
        "Explicitly lists Jia, Bing, Wu, Geng and Ren as Yang Heavenly Stems.",
        "This is a formal original-stem enumeration.",
    ),
    (
        "01",
        "乙，丁，己，辛，癸，為陰",
        "Explicitly lists Yi, Ding, Ji, Xin and Gui as Yin Heavenly Stems.",
        "This is a formal original-stem enumeration.",
    ),
    (
        "03",
        "寅申巳亥，四生也",
        "Names Yin, Shen, Si and Hai as the four birth/growth branches.",
        "Source patterns require a validated sexagenary chart.",
    ),
    (
        "03",
        "辰戌丑未，四庫也",
        "Names Chen, Xu, Chou and Wei as four storage branches.",
        "Text treats storehouses differently from four birth branches.",
    ),
    (
        "03",
        "子午卯酉，四敗也",
        "Names Zi, Wu, Mao and You as the four defeat branches.",
        "The verse explicitly says effects of clash may vary.",
    ),
    (
        "03",
        "若專執生死推斷，則誤矣",
        "Warns that predicting rigidly from life/death stages alone is erroneous.",
        "Source explicitly critiques an overgeneralized fatalistic diagnostic rule.",
    ),
    (
        "06",
        "格之真者，月支之神，透於天干也",
        "States that a genuine pattern has a month-branch influence visible among Heavenly Stems.",
        "Requires independently validated month pillar and visible branch-hidden factors.",
    ),
    (
        "06",
        "傷官旺，財神輕，有比劫而可見官",
        "Conditional case where strong Hurting Officer with weak Wealth and a rival can meet Officer.",
        "Do not generalize as a favorable outcome for every Hurting Officer–Officer combination.",
    ),
    (
        "09",
        "大運譬如所歷之地",
        "Compares decade luck movement to places traversed.",
        "An analogy about source interpretation, not a real geography forecast.",
    ),
    (
        "09",
        "太歲譬如所遇之人",
        "Compares annual influence to a person encountered.",
        "Historical metaphor only; no real person or actual encounter established.",
    ),
]
assert sum(map(len, VERSE_GLOSSES.values())) == 44
assert len(COMMENTARY) == 11
assert set(VERSE_GLOSSES) == set(CHAPTERS)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def save(file: Path, value):
    file.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def freeze(raw_dir: Path):
    manifests = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert set(manifests) == set(CHAPTERS)
    source_text = {}
    chapter_verses = {}
    for section in CHAPTERS:
        md = manifests[section]
        raw = (raw_dir / md["frozen_local_name"]).read_bytes()
        assert len(raw) == md["source_bytes"]
        assert sha(raw) == md["full_source_sha256"]
        source_text[section] = raw.decode("utf-8")
        verse = re.findall(r"\{\{\+\|([^}]*)\}\}", source_text[section])
        assert len(verse) == len(VERSE_GLOSSES[section]), (section, len(verse))
        chapter_verses[section] = verse
        assert CHAPTER_NAMES[section] in source_text[section]
    specimens = []
    for section in CHAPTERS:
        for i, original in enumerate(chapter_verses[section]):
            specimens.append(
                (
                    section,
                    original,
                    f"verse_{i + 1:02d}",
                    VERSE_GLOSSES[section][i],
                    "Conditional historical pattern depending on natal stems, branches and source-specific dates.",
                    SOURCE_CAVEATS[section],
                    "ORIGINAL_VERSE",
                )
            )
    for section, original, interpretation, scope in COMMENTARY:
        specimens.append(
            (
                section,
                original,
                "commentary_"
                + str(sum(x[0] == section for x in specimens if x[-1] == "COMMENTARY") + 1).zfill(
                    2
                ),
                interpretation,
                scope,
                SOURCE_CAVEATS[section],
                "COMMENTARY_PROSE",
            )
        )
    assert len(specimens) == 55
    notes = []
    receipts = []
    for i, (chapter, original, _kind, interpretation, precondition, caveat, text_type) in enumerate(
        specimens
    ):
        meta = manifests[chapter]
        text = source_text[chapter]
        assert original in text, (chapter, original)
        start = text.index(original)
        assert text.count(original) >= 1
        rid = f"BZI-R{i + 47:04d}"
        anchor_sha = sha(original.encode("utf-8"))
        record = {
            "id": rid,
            "source": "BZI-DITIAN-SUI-WIKISOURCE-V1",
            "locator": f"滴天髓/{chapter} {CHAPTER_NAMES[chapter]}",
            "chapter_code": chapter,
            "source_wikisource_oldid": meta["revision_id"],
            "original_chinese_anchor": original,
            "working_English_historical_gloss": interpretation,
            "text_layer": "TRANSMITTED_VERSE"
            if text_type == "ORIGINAL_VERSE"
            else "TRANSMITTED_COMMENTARY_UNDATED",
            "source_precondition": precondition,
            "uncertainty_or_exception": caveat,
            "raw_anchor_char_offset": start,
            "raw_anchor_utf8_byte_offset": len(text[:start].encode("utf-8")),
            "raw_anchor_utf8_sha256": anchor_sha,
            "full_pinned_chapter_sha256": meta["full_source_sha256"],
            "original_quote_directly_matched": True,
            "verified_authentic_Ming_witness": False,
            "verified_author_identification": False,
            "full_BaZi_calendar_engine_verified": False,
            "independent_real_person_predictive_validation": False,
            "runtime_model_promoted": False,
        }
        notes.append(record)
        receipts.append(
            {
                "record_id": rid,
                "chapter_code": chapter,
                "oldid": meta["revision_id"],
                "full_raw_page_sha256": meta["full_source_sha256"],
                "raw_byte_count": meta["source_bytes"],
                "exact_chinese_quote": original,
                "raw_char_offset": start,
                "raw_utf8_byte_offset": record["raw_anchor_utf8_byte_offset"],
                "exact_quote_sha256": anchor_sha,
                "source_layer": record["text_layer"],
            }
        )
    assert [r["id"] for r in notes] == [f"BZI-R{i:04d}" for i in range(47, 102)]
    source = {
        "schema": "BAZI_DITIAN_SUI_SIX_PINNED_CHAPTERS_55_NOTES_SOURCE_ONLY_V1",
        "batch": "ChineseAstro-05",
        "source": "Di Tian Sui 滴天髓 transmitted Chinese Wikisource",
        "source_author_or_commentary_attribution_certified": False,
        "original_print_edition_verified": False,
        "source_manifest_sha256": sha(MANIFEST.read_bytes()),
        "chapter_codes": CHAPTERS,
        "chapter_pinned_revisions": {k: v["revision_id"] for k, v in manifests.items()},
        "chapter_source_hashes": {k: v["full_source_sha256"] for k, v in manifests.items()},
        "verse_quote_count": 44,
        "commentary_exact_quote_count": 11,
        "source_only_annotation_count": 55,
        "first_id": "BZI-R0047",
        "last_id": "BZI-R0101",
        "next_id": "BZI-R0102",
        "warning": "Transmitted online annotations blend historical layers; source English glosses are provisional and non-expert. No birth calendar or human evaluation.",
        "human_predictive_validations": 0,
        "runtime_promotions": 0,
        "records": notes,
    }
    witness = {
        "schema": "BAZI_DITIAN_SUI_SIX_RAW_PAGE_EXACT_QUOTE_WITNESS_V1",
        "batch": "ChineseAstro-05",
        "source_manifest_sha256": sha(MANIFEST.read_bytes()),
        "frozen_page_metadata": manifests,
        "exact_chinese_source_anchor_matches": len(receipts),
        "verses": 44,
        "commentary_snippets": 11,
        "source_authenticity_early_print_not_established": True,
        "independent_classical_Chinese_expert_translation_review": False,
        "lunar_solar_term_calendar_not_verified": True,
        "human_predictive_validations": 0,
        "runtime_promotions": 0,
        "anchor_proofs": receipts,
    }
    save(NOTES, source)
    save(WITNESS, witness)
    print(
        json.dumps(
            {
                "records": len(notes),
                "verses": 44,
                "commentary": 11,
                "next": source["next_id"],
                "notes_sha256": sha(NOTES.read_bytes()),
                "witness_sha256": sha(WITNESS.read_bytes()),
                "all_pinned_source_hashes_match": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, required=True)
    freeze(parser.parse_args().raw_dir)
