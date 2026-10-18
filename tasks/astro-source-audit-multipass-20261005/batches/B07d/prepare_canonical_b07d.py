#!/usr/bin/env python3
"""Guard original unnumbered eleventh-house friends source with unchanged chapter count."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07d_FRIENDS_INTRO.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def j(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07d.json"):
    assert not p.exists(), f"Duplicate or incomplete archival source admission: {p}"
i = j(INDEX)
a = j(B / "ACCEPTANCE.json")
r = j(B / "RULES.json")
w = j(B / "ORIGINAL_SOURCE_WITNESS.json")
m = j(B / "SOURCE_TO_RECORD_MAP.json")
limits = j(B / "UNRESOLVED_SOURCE_LIMITS.json")
guard = j(B / "FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json")
z = j(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = j(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 9777
assert i["read_numbered_chapters"] == list(range(1, 150))
assert i["batches"][-1]["id"] == "B07c"
assert i["next"]["chapter"] == "UNNUMBERED_ELEVENTH_HOUSE_FRIENDS"
assert i["next"]["pdf_page"] == 668
assert i["next"]["printed_chapter_numeral"] is None
assert i["next"]["following_printed_chapter_numeral"] == "CL"
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07d" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 85
assert [x["record_number"] for x in r["rules"]] == list(range(9778, 9863))
assert [x["id"] for x in r["rules"] if x["role"] == "next_numbered_navigation"] == [
    "R9861",
    "R9862",
]
assert r["substantive"] == a["substantive"] == 83
assert a["numbered_chapters_added"] == 0
assert a["lilly_if_published"] == 9862 and a["combined_if_published"] == 10928
assert w["unnumbered"] and w["body_original_pdf_frames"] == [668, 669, 670]
assert w["next_printed_CL_heading_frame"] == 670
assert len(m["source_groups"]) == m["source_group_count"] == 7
assert not limits["actual_person_trustworthiness_and_moral_classification_authorized"]
assert not limits["friendship_count_and_quality_scoring_engine"]
assert not guard["real_person_loyalty_morality_classification_authorized"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert sha(B / "FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json") == a["friendship_guard_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 25 and sha(z["archive_path"]) == z["archive_sha256"]
assert chinese["sum_source_annotations"] == 72
assert chinese["independently_validated_real_human_claims"] == chinese["runtime_promotions"] == 0

rel = str(INDEX.relative_to(ROOT))
assert subprocess.run(["git", "diff", "--quiet", "HEAD", "--", rel], cwd=ROOT).returncode == 0
old_blob = subprocess.check_output(["git", "rev-parse", "HEAD:" + rel], cwd=ROOT, text=True).strip()
assert (
    old_blob
    == subprocess.check_output(["git", "hash-object", str(INDEX)], cwd=ROOT, text=True).strip()
)
BACK.mkdir(exist_ok=True)
for src, name in (
    (INDEX, "INDEX_BEFORE_B07d.json"),
    (CURRENT, "CURRENT_BEFORE_B07d.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07d.md"),
):
    (BACK / name).write_bytes(src.read_bytes())

i["batches"].append(
    {
        "id": "B07d",
        "path": "batches/B07d/RULES.json",
        "records_count": 85,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original 1647 William Lilly substantive UNNUMBERED "
            "11th-house Friends introduction after printed CXLIX "
            "PDF668/printed634 mid-lower, continues PDF669 "
            "and its internal Speciall Rules extend into "
            "TOP PDF670/printed636, before separately numbered "
            "CHAP CL Quality of Friends on SAME page. "
            "7 photo-anchored reversible groups, 83 historical "
            "substantive qualified assertions plus two next "
            "chapter navigation R9778–R9862. Prioritized "
            "source eleventh occupants/aspects, first house "
            "planets, last eleventh lord/aspects. Strong "
            "Jupiter/Venus alleged many helpful sincere friends "
            "vs weakened mixed/moderate; strong Saturn/Mars "
            "alleged MANY insincere friends, weak FEW, South "
            "Node not as adverse as Mars, mixed luminaries/"
            "Mercury and strongest-planet arbitration. "
            "Internal six benefic source houses many friends, "
            "malefic twelfth/angles many enemies, Cancer "
            "rising friends hard, first/tenth ruler "
            "retrograde separation politics, individual "
            "11th-house planet claims, Moon known to many "
            "but fewer close friends. No actual human "
            "loyalty/morality/social accuracy nor runtime "
            "scoring promotion. Section UNNUMBERED so "
            "original printed chapter count unchanged."
        ),
    }
)
i["records_count"] = 9862
assert i["read_numbered_chapters"] == list(range(1, 150))
i["status"] = "BOOK_III_UNNUMBERED_ELEVENTH_FRIENDS_NEXT_PRINTED_CL"
i["next"] = {
    "pdf_page": 670,
    "printed_page": 636,
    "chapter": "CL",
    "printed_chapter_numeral": "CL",
    "heading": "Quality of Friends",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CL Quality of Friends begins "
        "AFTER a divider mid original PDF670/printed636. "
        "Previous UNNUMBERED eleventh-house Speciall "
        "Rules continue at TOP of SAME PDF670. "
        "Printed CL continues PDF671/printed637 "
        "and the next separately printed CHAP CLI "
        "Whether there may be Concord or Unity betwixt "
        "two starts later PDF671. Verify precise "
        "seam, do not merge these source units."
    ),
    "research_scope": (
        "Period planetary nature of close associates "
        "by first/eleventh occupants or rulers, "
        "social roles attributed to Saturn/Jupiter/"
        "Mars/Sun/Venus/Mercury/Moon; sign modalities "
        "allegedly indicate friendship constancy. "
        "Period social/gender/class stereotypes "
        "historical only and not real person labels."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["unnumbered_eleventh_house_acceptance_note"] = (
    "B07d R9778–R9862, 85 original source notes, "
    "PDF668–672 SHA/bytes and 25 ZIP test replays, "
    "unnumbered Speciall Rules continue TOP "
    "PDF670 before distinct printed CL. "
    "Count, reliability, helpfulness, enemy number "
    "and social esteem are separate targets, "
    "no verified humans or runtime promotions, "
    "Chinese 72 source notes separate."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9862
assert i["read_numbered_chapters"] == list(range(1, 150))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Original unnumbered eleventh-house friendship source documented\n\n"
    + review
    + "\nFollowing GitHub verified publication **9,862 Lilly "
    + "+1,066 Ptolemy=10,928 historical documentary notes**, "
    + "25 first-edition/portable archive tests pass, "
    + "no human friend count, faithfulness or relationship "
    + "predictions validated; zero promoted source rules.\n"
)
PROGRESS.write_text(
    "# Original Lilly through unnumbered eleventh-house friendship — 2026-10-18\n\n"
    "After remote verified acceptance **10,928 documentary "
    "historical records** (9,862 Lilly +1,066 Ptolemy). "
    "First-edition physical page position PDF670/894 "
    "(**74.9% scanned physical page order ONLY, not "
    "model/empirical completion**). B07d 85 historical "
    "source records distinguish friend number, sincerity, "
    "help, public acquaintances, enemy number, political "
    "favor and mixed cases. Unnumbered eleventh-house "
    "Speciall Rules continue on PDF670 before printed CL. "
    "No human loyalty/morality forecasting validated "
    "and no runtime source promotions. NEXT printed "
    "CL quality of friends PDF670–671, then CLI "
    "friendship concord on PDF671. Chinese BaZi46/"
    "Zi Wei26 source notes independent.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B07d.md").read_text()
)
CURRENT.write_text(
    "# Lilly eleventh-house friends unnumbered introduction documented; CL next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. B07d "
    "R9778–R9862 locally admitted pending remote "
    "publication; after authenticated GitHub readback "
    "9,862 Lilly +1,066 Ptolemy=10,928 "
    "historic source-only annotations. "
    "25 original/ZIP replays pass; no real person "
    "friendship/loyalty, support, public esteem "
    "or enemy counts validated and no scoring rule "
    "promotions. Section UNNUMBERED, chapter "
    "count unchanged. NEXT printed CL PDF670 "
    "then printed CLI PDF671. Chinese source "
    "BaZi46 + Zi Wei26 separately preserved.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07d.md").read_text()
)
receipt = {
    "batch": "B07d",
    "status": "GUARDED_UNNUMBERED_ELEVENTH_FRIENDS_PENDING_REMOTE",
    "prior_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07d.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "friendship_scope_guard_sha256": sha(B / "FRIENDSHIP_HISTORICAL_TARGET_GUARD_V1.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9862,
    "ptolemy_retained": 1066,
    "combined_if_published": 10928,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 0,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
