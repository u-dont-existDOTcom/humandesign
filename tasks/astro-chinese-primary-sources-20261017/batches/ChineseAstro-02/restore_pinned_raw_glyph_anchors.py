#!/usr/bin/env python3
"""Correct source anchors to exact simplified glyphs in pinned Wikisource wikitext.

The web viewer can transform glyphs to traditional; original pinned raw revision
is simplifed. Keep the former display rendering in a separate non-authoritative field.
"""

import json
from pathlib import Path

B = Path(__file__).resolve().parent
P = B / "ZIWEI_VOLUME2_PART_A_SOURCE_NOTES_V1.json"
obj = json.loads(P.read_text(encoding="utf-8"))

anchors = {
    "ZWD-R0027": "紫微天机逆行旁",
    "ZWD-R0028": "子时戌上起文昌",
    "ZWD-R0029": "文曲数从辰上起",
    "ZWD-R0030": "左辅正月起于辰",
    "ZWD-R0031": "右弼从戌宫逆转",
    "ZWD-R0032": "甲戊庚牛羊",
    "ZWD-R0033": "申子辰人马居寅",
    "ZWD-R0034": "甲生禄存在寅宫",
    "ZWD-R0035": "前安擎羊禄后安陀罗",
    "ZWD-R0036": "癸禄在子",
    "ZWD-R0037": "寅午戌人丑卯方",
    "ZWD-R0038": "甲廉破武阳为伴",
    "ZWD-R0039": "壬梁紫府武宿是",
    "ZWD-R0040": "亥上起子顺安劫",
    "ZWD-R0041": "逆向便是天空乡",
    "ZWD-R0042": "天伤安在奴仆宫",
    "ZWD-R0043": "天使安在疾厄宫",
    "ZWD-R0044": "阳男阴女顺推轮",
    "ZWD-R0045": "天刑星从酉上起正月",
    "ZWD-R0046": "天姚星从丑上起正月",
    "ZWD-R0047": "初一日加在左辅宫",
    "ZWD-R0048": "初一加右弼宫逆数",
    "ZWD-R0049": "哭逆巳兮虚顺未",
    "ZWD-R0050": "虚顺未",
    "ZWD-R0051": "龙池子顺辰",
}
sections = {
    "安南北斗諸星訣": "安南北斗诸星诀",
    "安文昌文曲星訣": "安文昌文曲星诀",
    "安左輔右弼星訣": "安左辅右弼星诀",
    "安天魁天鉞訣": "安天魁天钺诀",
    "安天馬星訣": "安天马星诀",
    "安祿存星訣": "安禄存星诀",
    "安擎羊陀羅二星訣": "安擎羊陀罗二星诀",
    "安火鈴二星訣": "安火铃二星诀",
    "安祿權科忌四星變化訣": "安禄权科忌四星变化诀",
    "天空地劫訣": "天空地劫诀",
    "安天傷天使訣": "安天伤天使诀",
    "安十二宮太歲殺祿訣": "安十二宫太岁杀禄诀",
    "安天刑天姚星訣": "安天刑天姚星诀",
    "安三台八座二星訣": "安三台八座二星诀",
    "安天哭天虛星訣": "安天哭天虚星诀",
    "安龍池鳳閣訣": "安龙池凤阁诀",
}
assert len(obj["records"]) == len(anchors) == 25
for row in obj["records"]:
    rid = row["id"]
    row["display_transliterated_traditional_anchor"] = row["original_chinese_anchor"]
    row["original_chinese_anchor"] = anchors[rid]
    prefix, head = row["locator"].split(":", 1)
    assert head in sections, head
    row["display_traditional_section"] = head
    row["locator"] = prefix + ":" + sections[head]
obj["witness_glyph_note"] = (
    "Pinned original revision is Simplified Chinese wikitext; earlier rendered "
    "Traditional conversion is preserved separately, and only exact "
    "raw-Simplified anchors count as witnessed source words."
)
P.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Updated", len(anchors), "raw-text quote anchors and", len(sections), "section headings")
