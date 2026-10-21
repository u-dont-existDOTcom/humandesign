#!/usr/bin/env python3
"""Exact transmitted Zi Wei Volume II final four palace sections; no human forecast."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-chinese-primary-sources-20261017"
RAW = T / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
PREVIOUS = T / "CHINESE_SOURCE_AUDIT_INDEX_V23.json"
WEST = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
RAW_SHA = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
OLD_SHA = "0bc5836d92c332a458a7d4a74dbb25488705344aa38df256dc721c6c5a673a0e"
WEST_SHA = "c3233591a5ce1199e52b1a7e00e09f0dff45538733211b0acb3e9a5dc02851c8"
SEGMENTS = (
    ("Career", "官禄", "===九官禄===", 44429, 45743, 38,
     "fa97eb2aa98e9a8d87ca2ed754268d558f6a399a836a47ab1d86b6480aa7e97a"),
    ("Estate", "田宅", "===十田宅===", 45743, 46678, 24,
     "ccc5e2f6cf55e772c37c7f2f78e78d6b0d7ffb66bf529aaf74e7d6ba0a631efb"),
    ("Fortune", "福德", "===十一福德===", 46678, 47640, 28,
     "d67acacd1d8e4ca1150267f6c8e955447f4f096d78637ae34e76c4c5e64e356c"),
    ("Parents", "父母", "===十二父母===", 47640, 48890, 33,
     "80d8ed7db08ea75b48f1a728cb4b2cd4c1641a4bec063efe1bd7f93235bf9c04"),
)
CONTINUATIONS = {
    "Career": {5:"WuQu", 12:"JuMen", 14:"TianXiang"},
    "Estate": {5:"WuQu"},
    "Fortune": {4:"TaiYang", 6:"WuQu", 15:"QiSha"},
    "Parents": {7:"TianJi", 9:"TaiYang", 19:"TianLiang"},
}
CAREER_POEM_LABELS = {28,30,32,34,36}
CAREER_POEM_VERSES = {29,31,33,35,37}
SOURCE_CLAIM_FLAGS = ("刑", "克", "死", "贫", "富", "官", "贵", "家", "父", "母", "寿", "祸", "病", "妇", "女", "子")


def hash_bytes(blob: bytes) -> str:
    return sha256(blob).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(name: str, obj: object) -> None:
    (B / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_quote(txt: str, cp: int, raw: bytes, s: str) -> dict:
    enc = txt.encode("utf-8")
    bp = len(s[:cp].encode("utf-8"))
    if s[cp:cp+len(txt)] != txt or raw[bp:bp+len(enc)] != enc:
        raise ValueError("Source quote at codepoint does not equal original UTF8 bytes")
    return {"quote": txt, "sha256": hash_bytes(enc),
            "codepoint": cp, "UTF8_byte_offset": bp, "UTF8_bytes": len(enc)}


def main() -> None:
    raw = RAW.read_bytes()
    if (len(raw),hash_bytes(raw)) != (106736,RAW_SHA):
        raise ValueError("Pinned online Volume II raw UTF8 changed")
    if hash_bytes(PREVIOUS.read_bytes()) != OLD_SHA or hash_bytes(WEST.read_bytes()) != WEST_SHA:
        raise ValueError("Previous Chinese or inherited Western source snapshot drift")
    old = load(PREVIOUS)
    if old["sum_source_annotations"] != 1146 or [
        (x["accepted_source_annotations"], x["next_id"]) for x in old["systems"]
    ] != [(210,"BZI-R0211"),(936,"ZWD-R0937")]:
        raise ValueError("V23 original Chinese historical frontier not accepted")
    if old["accepted_batches"][-1]["id"] != "ChineseAstro-23SRC-Servants":
        raise ValueError("Latest previously accepted Zi Wei source is not Servants")
    s = raw.decode("utf-8")
    if len(s) != 48890 or SEGMENTS[0][3] != 44429 or SEGMENTS[-1][4] != len(s):
        raise ValueError("Expected full original online Volume II codepoint coverage changed")
    if any(SEGMENTS[i][4] != SEGMENTS[i+1][3] for i in range(len(SEGMENTS)-1)):
        raise ValueError("Four original section source spans are not contiguous")
    excerpt = s[44429:48890]
    (B / "SOURCE_1963110_FINAL_FOUR_EXACT_EXCERPT.txt").write_bytes(excerpt.encode("utf-8"))
    records: list[dict] = []
    section_summaries: list[dict] = []
    packaging: list[dict] = []
    verse_markup: list[dict] = []
    for tag, native, title, begin, end, expected, expected_sha in SEGMENTS:
        part = s[begin:end]
        if not part.startswith(title) or hash_bytes(part.encode("utf-8")) != expected_sha:
            raise ValueError("Original source section title or segment SHA drift: " + tag)
        cursor = begin
        count = 0
        local_verse_marks = []
        line_classes: dict[str,int] = {}
        for rawline in part.splitlines(keepends=True):
            quoted = rawline.strip()
            cp = cursor + (rawline.index(quoted) if quoted else 0)
            cursor += len(rawline)
            if not quoted:
                continue
            if quoted in ("<poem>", "</poem>"):
                mark = {"source_palace": tag, **make_quote(quoted,cp,raw,s)}
                local_verse_marks.append(mark)
                verse_markup.append(mark)
                continue
            if quoted == "</onlyinclude>" or quoted.startswith("{{footer|"):
                if tag != "Parents":
                    raise ValueError("Non-source Wikitext footer appeared in a nonfinal palace")
                packaging.append({"kind":"SITE_WRAPPER_NOT_HISTORIC_ASTROLOGY",
                                  "source_palace":tag, **make_quote(quoted,cp,raw,s)})
                continue
            original_line_index = count
            count += 1
            if original_line_index == 0:
                kind, group = "ORIGINAL_PALACE_HEADING", tag
            elif tag == "Career" and original_line_index in CAREER_POEM_LABELS:
                kind, group = "ORIGINAL_POEM_TITLE_NOT_NATAL_RULE", "CareerPoem"
            elif tag == "Career" and original_line_index in CAREER_POEM_VERSES:
                kind, group = "ORIGINAL_HISTORIC_CAREER_VERSE", "CareerPoem"
            elif tag == "Parents" and original_line_index in (1,2,3,4):
                kind, group = "ORIGINAL_PARENTAL_SOURCE_METHOD_PREAMBLE", "ParentsMethod"
            elif original_line_index in CONTINUATIONS[tag]:
                kind, group = ("ORIGINAL_CONTINUED_PRIOR_PROFILE_LINE",
                               CONTINUATIONS[tag][original_line_index])
            else:
                kind, group = "ORIGINAL_HISTORICAL_STAR_CONDITION_LINE", tag
            line_classes[kind] = line_classes.get(kind,0) + 1
            note = {
                "id": f"ZWD-R{937+len(records):04d}",
                "source": "ZWDS-CLASSIC-01",
                "batch": "ChineseAstro-24SRC-FinalPalaces",
                "source_oldid": 1963110,
                "source_full_SHA256": RAW_SHA,
                "source_palace": tag,
                "source_palace_native": native,
                "original_source_line_index": original_line_index,
                "source_kind": kind,
                "original_continuation_group": group,
                "original_exact_Chinese_Wikitext_quote": quoted,
                "original_quote_SHA256": hash_bytes(quoted.encode("utf-8")),
                "original_quote_UTF8_bytes": len(quoted.encode("utf-8")),
                "original_absolute_codepoint_offset": cp,
                "original_UTF8_byte_offset": len(s[:cp].encode("utf-8")),
                "source_excerpt_relative_codepoint_offset": cp - 44429,
                "historical_social_family_status_mortality_claim": any(w in quoted for w in SOURCE_CLAIM_FLAGS),
                "ancient_Ming_printing_authenticated": False,
                "independent_human_blind_forecasts_validated": 0,
                "runtime_astrology_promotions": 0,
            }
            witness = make_quote(quoted,cp,raw,s)
            if (witness["sha256"] != note["original_quote_SHA256"] or
                witness["UTF8_byte_offset"] != note["original_UTF8_byte_offset"]):
                raise ValueError("Independent source quote witness disagrees")
            if not (begin <= cp < cp + len(quoted) <= end):
                raise ValueError("Source quote lies outside palace original text")
            records.append(note)
        if cursor != end or count != expected:
            raise ValueError(f"Source {tag} physical lines/boundaries count {count} expected {expected}")
        if [x["quote"] for x in local_verse_marks] != ["<poem>", "</poem>"]:
            raise ValueError("Original opening/closing verse delimiters not preserved")
        section_summaries.append({
            "source_palace": tag, "source_palace_native": native,
            "original_heading": title, "original_start_codepoint": begin,
            "original_end_codepoint_exclusive": end,
            "original_segment_SHA256": expected_sha,
            "historical_original_line_count": count,
            "original_line_kinds": line_classes,
            "poem_tag_offsets": [x["codepoint"] for x in local_verse_marks],
        })
    if len(records) != 123 or records[0]["id"] != "ZWD-R0937" or records[-1]["id"] != "ZWD-R1059":
        raise ValueError("Historical source contiguous IDs through Wikitext end mismatched")
    if len(packaging) != 2:
        raise ValueError("Exactly two nonhistorical Wikitext footer wrappers expected")
    if packaging[0]["quote"] != "</onlyinclude>" or not packaging[1]["quote"].startswith("{{footer|"):
        raise ValueError("Source closing wrapper must remain unmodified but uncounted")
    if len(verse_markup) != 8:
        raise ValueError("Four original section poem-open/close marker pairs expected")
    if sum(sct["historical_original_line_count"] for sct in section_summaries) != 123:
        raise ValueError("Four source sections not exhaustively captured")
    data = {
        "schema": "CHINESE_V24_FINAL_FOUR_ZIWEI_VOLUME_II_ONLINE_SOURCE_ONLY_V1",
        "batch": "ChineseAstro-24SRC-FinalPalaces",
        "original_online_Wikitext_oldid": 1963110,
        "original_full_online_volume_SHA256": RAW_SHA,
        "original_full_online_volume_UTF8_bytes": len(raw),
        "excerpt_source_codepoint_span": [44429,48890],
        "excerpt_SHA256": hash_bytes(excerpt.encode("utf-8")),
        "excerpt_UTF8_bytes": len(excerpt.encode("utf-8")),
        "source_sections": section_summaries,
        "nonhistorical_Wikitext_footer_records_preserved_not_counted": packaging,
        "source_poem_markup_records": verse_markup,
        "source_literal_ancient_content_lines": 123,
        "source_nonhistorical_site_footer_lines": 2,
        "new_documentary_records": 123,
        "first_record_id": "ZWD-R0937",
        "last_record_id": "ZWD-R1059",
        "next_documentary_id": "ZWD-R1060",
        "source_online_volume_II_end_reached": True,
        "all_online_volume_II_twelve_palace_source_lines_documented_subject_to_prior_accepted_indexes": True,
        "independently_authenticated_early_original_printing": False,
        "complete_original_critical_work_collated": False,
        "full_Chinese_natal_calendar_engine_verified": False,
        "real_human_predictive_validations": 0,
        "runtime_astrological_promotions": 0,
        "records": records,
    }
    notes = B / "ZIWEI_FINAL_FOUR_123_SOURCE_NOTES_V1.json"
    save(notes.name, data)
    witness = B / "SOURCE_FINAL_FOUR_123_EXACT_OFFSET_WITNESS_V1.json"
    save(witness.name, {
        "schema": "CHINESE_V24_FINAL_FOUR_CP_UTF8_SHA_SOURCE_WITNESS",
        "original_full_Wikitext_SHA256": RAW_SHA,
        "source_excerpt_SHA256": data["excerpt_SHA256"],
        "source_excerpt_codepoints": [44429,48890],
        "source_poem_markup": verse_markup,
        "source_footer_metadata_not_historical_records": packaging,
        "quoted_original_records": [
            {"id": row["id"], "source_palace": row["source_palace"],
             "absolute_codepoint": row["original_absolute_codepoint_offset"],
             "absolute_UTF8_byte_offset": row["original_UTF8_byte_offset"],
             "quote_SHA256": row["original_quote_SHA256"],
             "quote_UTF8_bytes": row["original_quote_UTF8_bytes"]} for row in records
        ],
        "real_human_blind_forecasts": 0,
    })
    save("ACCEPTANCE.json", {
        "batch": "ChineseAstro-24SRC-FinalPalaces",
        "previous_index_V23_SHA256": OLD_SHA,
        "Chinese_before": 1146,
        "BaZi_unchanged": 210,
        "ZiWei_before": 936,
        "new_original_historical_text_notes": 123,
        "Chinese_after_if_accepted": 1269,
        "ZiWei_after_if_accepted": 1059,
        "first_id": "ZWD-R0937",
        "last_id": "ZWD-R1059",
        "next_id": "ZWD-R1060",
        "next_BaZi": "BZI-R0211",
        "source_full_online_volume_sha256": RAW_SHA,
        "source_note_sha256": hash_bytes(notes.read_bytes()),
        "source_witness_sha256": hash_bytes(witness.read_bytes()),
        "source_excerpt_sha256": data["excerpt_SHA256"],
        "Wikitext_footer_markup_not_counted": True,
        "original_early_printed_book_authenticated": False,
        "human_blind_predictive_validations": 0,
        "runtime_astrological_promotions": 0,
    })
    print(json.dumps({
        "batch": data["batch"],
        "historical_text_lines": len(records),
        "sections": [(x["source_palace"],x["historical_original_line_count"]) for x in section_summaries],
        "site_footer_nonhistorical": len(packaging),
        "next_id": data["next_documentary_id"],
        "source_excerpt_sha256": data["excerpt_SHA256"],
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
