"""Auditable partial Zi Wei NaYin five-phase bureau lookup.

Source: frozen Wikisource Volume II oldid1963110, not an original Ming imprint.
This is a rule transcription/parity test, NOT a complete civil-date natal
decoder, independently validated 14-star chart, or predictive astrology model.
Two source spelling errors require *opt-in* documented emendations.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from ziwei_source_mechanics import BRANCHES, STEMS, palace_stem_from_yin

SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "batches/ChineseAstro-07/SOURCE_ORIGINAL_ZIWEI_VOL2_1963110_RAW.txt"
)
SOURCE_SHA256 = "1e255c6ae99e6f89ae124ab342554ef1347fc8e68fb8908cba7290d1a38cbb72"
POEM_HEADING = "'''六十花甲子纳音歌'''"
HAN_STEMS = "甲乙丙丁戊己庚辛壬癸"
HAN_BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
PHASE_TO_BUREAU = {"水": ("Water", 2), "木": ("Wood", 3),
                   "金": ("Metal", 4), "土": ("Earth", 5),
                   "火": ("Fire", 6)}

# Only these whole-couplet emendations are supported, not global replacement.
# Witnesses are later textual witnesses, not ancient edition authentication.
DOCUMENTED_EMENDATIONS = {
    "甲戊乙亥山头火": "甲戌乙亥山头火",  # 戊 -> 戌 in first branch
    "戊戌已亥平地木": "戊戌己亥平地木",  # 已 -> 己 in second stem
}
COLLATION_URLS = (
    "https://www.shidianguji.com/zh/book/HY1439/chapter/1m70sj2411nvn",
    "https://m.gushiwen.cn/guwen/bookv_46fc9880f58c.aspx",
    "https://ctext.org/wiki.pl?chapter=466438&if=gb",
)


@dataclass(frozen=True)
class BureauResult:
    """Status preserves the difference between original and emended text."""

    year_stem: str
    life_palace: str
    palace_stem: str
    phase: str | None
    bureau_number: int | None
    source_status: str  # direct | emended_later_witness | unresolved_source


def original_couplets() -> tuple[str, ...]:
    """Read 30 exact seven-character source couplets; fail on source drift."""
    blob = SOURCE_PATH.read_bytes()
    if sha256(blob).hexdigest() != SOURCE_SHA256:
        raise ValueError("Pinned original source SHA256 changed")
    source = blob.decode("utf-8")
    if source.count(POEM_HEADING) != 1:
        raise ValueError("Original NaYin heading absent or ambiguous")
    poem = source.split(POEM_HEADING, 1)[1].split("<poem>", 1)[1].split("</poem>", 1)[0]
    tokens = tuple(c.strip() for c in poem.replace("\n", "").replace("。", "，").split("，") if c.strip())
    if len(tokens) != 30 or any(len(c) != 7 for c in tokens):
        raise ValueError("Original NaYin poem segmentation changed")
    return tokens


def table(*, documented_emendations: bool = False) -> dict[tuple[str, str], tuple[str, int, str]]:
    """Return accepted pillar->(phase, bureau, provenance), excluding corrupt tokens.

    When documented_emendations=False, the original text's two malformed
    tokens are omitted (58 valid sexagenary pairs); never infer their values.
    """
    result: dict[tuple[str, str], tuple[str, int, str]] = {}
    tokens = original_couplets()
    if set(tokens) & set(DOCUMENTED_EMENDATIONS) != set(DOCUMENTED_EMENDATIONS):
        raise ValueError("Expected exact malformed oldid1963110 couplets absent")
    expected = {(HAN_STEMS[i % 10], HAN_BRANCHES[i % 12]) for i in range(60)}
    invalid: set[str] = set()
    for original in tokens:
        corrected = DOCUMENTED_EMENDATIONS.get(original, original) if documented_emendations else original
        phase = corrected[-1]
        if phase not in PHASE_TO_BUREAU:
            raise ValueError("Unknown NaYin phase")
        name, bureau = PHASE_TO_BUREAU[phase]
        for index, pair in enumerate((corrected[:2], corrected[2:4])):
            key = (pair[0], pair[1])
            if key not in expected:
                invalid.add(pair)
                continue
            if key in result:
                raise ValueError("Duplicate original sexagenary label")
            # Only the changed two-character PILLAR needs an emendation;
            # its valid neighboring pillar is attested directly by oldid.
            raw_pair = original[2 * index : 2 * index + 2]
            status = "emended_later_witness" if pair != raw_pair else "direct"
            result[key] = (name, bureau, status)
    if documented_emendations:
        if invalid or set(result) != expected:
            raise ValueError("Documented corrections failed 60-cycle closure")
    elif invalid != {"甲戊", "已亥"} or len(result) != 58:
        raise ValueError("Unexpected source corruptions in uncorrected text")
    return result


def life_palace_bureau(
    birth_year_stem: str, life_palace_branch: str, *, documented_emendations: bool = False
) -> BureauResult:
    """Lookup requires independently provided year stem and Life palace.

    It does not infer birth year, local time, lunar month or leap-month rules.
    Default preserves unresolved entries rather than silently normalizing.
    """
    if birth_year_stem not in STEMS or life_palace_branch not in BRANCHES:
        raise ValueError("Year stem and Life-palace branch must be canonical")
    stem = palace_stem_from_yin(birth_year_stem, life_palace_branch)
    key = (HAN_STEMS[STEMS.index(stem)], HAN_BRANCHES[BRANCHES.index(life_palace_branch)])
    item = table(documented_emendations=documented_emendations).get(key)
    if item is None:
        return BureauResult(birth_year_stem, life_palace_branch, stem, None, None, "unresolved_source")
    return BureauResult(birth_year_stem, life_palace_branch, stem, *item)


ENGINE_SCOPE = {
    "rule_transcription": True,
    "year_stem_and_life_palace_inputs_required": True,
    "uncorrected_year_stem_palace_paths": 116,
    "documented_emendation_year_stem_palace_paths": 120,
    "independent_original_imprint_authentication": False,
    "lunar_calendar_converted": False,
    "14_star_chart_parity_verified": False,
    "human_predictive_tests": 0,
    "runtime_promotions": 0,
}
