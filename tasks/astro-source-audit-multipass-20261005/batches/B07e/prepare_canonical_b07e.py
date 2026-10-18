#!/usr/bin/env python3
"""Guarded append of original first-edition printed CL friend-type source."""

import hashlib
import json
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
INDEX = ROOT / "tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
PROGRESS = ROOT / "state/ASTROLOGY_SOURCE_STUDY_PROGRESS_20261017.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261018_B07e_FRIEND_QUALITY.md"
CHINESE = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V1.json"
BACK = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261018.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


for p in (LATEST, RECEIPT, BACK / "INDEX_BEFORE_B07e.json"):
    assert not p.exists(), f"Duplicate or interrupted original source admission: {p}"
i = read(INDEX)
a = read(B / "ACCEPTANCE.json")
r = read(B / "RULES.json")
w = read(B / "ORIGINAL_SOURCE_WITNESS.json")
m = read(B / "SOURCE_TO_RECORD_MAP.json")
limits = read(B / "UNRESOLVED_SOURCE_LIMITS.json")
z = read(B / "SOURCE_RELEASE_RECEIPT_20261018.json")
chinese = read(CHINESE)

assert i["records_count"] == a["prior_lilly"] == 9862
assert i["read_numbered_chapters"] == list(range(1, 150))
assert i["batches"][-1]["id"] == "B07d"
assert i["next"]["chapter"] == "CL"
assert i["next"]["printed_chapter_numeral"] == "CL"
assert i["next"]["pdf_page"] == 670
assert i["empirical_validations"] == i["runtime_promotions"] == 0
assert not any(x["id"] == "B07e" for x in i["batches"])
assert r["record_count"] == a["new_historical_annotations"] == 64
assert [x["record_number"] for x in r["rules"]] == list(range(9863, 9927))
assert [x["id"] for x in r["rules"] if x["role"] == "next_chapter_navigation"] == ["R9925", "R9926"]
assert r["substantive"] == a["substantive"] == 62
assert a["numbered_chapters_added"] == 1
assert a["lilly_if_published"] == 9926 and a["combined_if_published"] == 10992
assert w["body_pdf_frames"] == [670, 671]
assert w["following_printed_CLI_heading_pdf"] == 671
assert len(m["source_groups"]) == m["source_group_count"] == 6
assert not limits["real_person_trustworthiness_or_demographic_inference_authorized"]
assert not limits["friendship_quality_original_operator_complete"]
assert r["empirical_validations"] == a["empirical_validations"] == 0
assert r["runtime_promotions"] == a["runtime_promotions"] == 0
assert all(not x["runtime_model_promoted"] for x in r["rules"])
assert sha(B / "RULES.json") == a["rules_sha256"] == z["accepted_rules_sha256"]
assert z["crc_passed"] and z["sha256_passed"] and z["extraction_passed"]
assert z["replayed_tests"] == 20 and sha(z["archive_path"]) == z["archive_sha256"]
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
for old, name in (
    (INDEX, "INDEX_BEFORE_B07e.json"),
    (CURRENT, "CURRENT_BEFORE_B07e.md"),
    (PROGRESS, "PROGRESS_BEFORE_B07e.md"),
):
    (BACK / name).write_bytes(old.read_bytes())

i["batches"].append(
    {
        "id": "B07e",
        "path": "batches/B07e/RULES.json",
        "records_count": 64,
        "sha256": a["rules_sha256"],
        "scope": (
            "Original first-edition William Lilly printed CHAP CL "
            "Quality of Friends starts after divider middle PDF670/"
            "printed636, ends upper PDF671/printed637 BEFORE "
            "independent printed CLI on concord of two nativities. "
            "Six reversible photo/source groups, 62 substantive "
            "historical clauses and two next-numbered navigation "
            "R9863-R9926. Friend type allegedly identified from "
            "first/eleventh occupants, their rulers or intercepted "
            "sign; period Saturn elder/trades/stigma, Jupiter clergy/"
            "legal/nobles, Mars military/red hair, Sun monarchy/"
            "administration, Venus arts/women/gaming, Mercury "
            "scholarship/commerce, Moon maritime/matrons/general "
            "people. Internal Constancy source: fixed sign eleventh "
            "supposedly fixed friends, movable changed, common mixed, "
            "plus 11th lord aspect and unclear Venus own-house clause. "
            "All occupational, gender, status, physical appearances "
            "and moral type labels are historical prejudicial "
            "classifications, no actual person inference validated. "
            "CLI requires TWO charts, not a continuation of "
            "single-nativity friend quality. No production "
            "source rules promoted."
        ),
    }
)
i["records_count"] = 9926
i["read_numbered_chapters"].append(150)
i["status"] = "BOOK_III_CL_FRIEND_QUALITY_NEXT_CLI_TWO_NATIVITY_CONCORD"
i["next"] = {
    "pdf_page": 671,
    "printed_page": 637,
    "chapter": "CLI",
    "printed_chapter_numeral": "CLI",
    "heading": "Whether there may be Concord or Unity betwixt two",
    "include_opening_paragraph": True,
    "extracted": False,
    "boundary_image_read": True,
    "position": (
        "Printed CHAP CLI Whether there may be Concord "
        "or Unity betwixt two begins after divider "
        "in original PDF671/printed637 upper-middle, "
        "after the closing CL constancy-of-friends text. "
        "It immediately requires comparing BOTH "
        "persons' Nativities and continues on original "
        "PDF672 onward. Verify exact following separately "
        "printed heading before complete extraction."
    ),
    "research_scope": (
        "Two-person natal compatibility and mutual friendship/"
        "contention, ascendant and its rulers, occupants, "
        "receiving aspects and natural planetary friendships/"
        "enmities, temporal constancy and conflict. "
        "Two independently calculated charts and "
        "predeclared dyad outcomes needed for validation; "
        "do not infer actual relationship ethics or risk."
    ),
}
i["current_state"] = str(LATEST.relative_to(ROOT))
i["chapter_CL_friend_types_acceptance_note"] = (
    "B07e source R9863-R9926, 64 historical source notes, "
    "six photo groups PDF670-673 SHA/bytes and 20 "
    "portable archive extracted test replays. "
    "Source friend-class occupation/appearance/morality "
    "not human claims, friendship constancy separate, "
    "next CLI explicitly requires two nativities. "
    "Chinese 72 original source notes separate."
)
assert i["records_count"] == sum(x["records_count"] for x in i["batches"]) == 9926
assert i["read_numbered_chapters"] == list(range(1, 151))
INDEX.write_text(json.dumps(i, ensure_ascii=False, indent=2) + "\n")

review = (B / "ORIGINAL_SOURCE_REVIEW_20261018.md").read_text()
LATEST.write_text(
    "# Lilly first-edition printed CL friend-type source documented\n\n"
    + review
    + "\nAfter authenticated GitHub publication "
    + "9,926 Lilly +1,066 Ptolemy=10,992 historical "
    + "source notes; 20 photo/ZIP replay tests pass, "
    + "zero human friend type/constancy or actual "
    + "pairwise compatibility validations, no model promotion.\n"
)
PROGRESS.write_text(
    "# Original Lilly through printed CL Quality of Friends — 2026-10-18\n\n"
    "After verified publication **10,992 historical source "
    "records** (9,926 Lilly +1,066 Ptolemy), source "
    "original PDF671/894 (**75.1% scanned physical page "
    "position only, not computational/research completion**). "
    "B07e 64 source-only friend type and constancy "
    "qualifiers, including period seven planetary "
    "social categories and fixed/movable/common signs. "
    "No actual human friend occupation/appearance/trust "
    "data, source runtime promotions zero. NEXT printed "
    "CLI on concord of TWO birth charts from PDF671 "
    "onward. Chinese BaZi46 / ZiWei26 original "
    "sources separately indexed.\n\n---\n\n" + (BACK / "PROGRESS_BEFORE_B07e.md").read_text()
)
CURRENT.write_text(
    "# Lilly CL friend types documented, two-nativity concord source next\n\n"
    "2026-10-18 Africa/Dakar UTC+0. Original B07e "
    "source R9863-R9926 prepared, GitHub publication pending. "
    "After verified push 9,926 Lilly +1,066 Ptolemy "
    "=10,992 historical notes; 20 first edition "
    "source and ZIP extraction tests pass. "
    "No actual human friendships/careers/reputation "
    "verified and no model promotions. "
    "NEXT printed CLI two-person concord PDF671 onward. "
    "Chinese BaZi 46 + Zi Wei26 sources separate.\n\n---\n\n"
    + (BACK / "CURRENT_BEFORE_B07e.md").read_text()
)
receipt = {
    "batch": "B07e",
    "status": "GUARDED_CL_HISTORIC_FRIEND_QUALITY_PENDING_GITHUB",
    "previous_index_git_blob": old_blob,
    "prior_index_sha256": sha(BACK / "INDEX_BEFORE_B07e.json"),
    "updated_index_sha256": sha(INDEX),
    "latest_sha256": sha(LATEST),
    "progress_sha256": sha(PROGRESS),
    "current_sha256": sha(CURRENT),
    "rules_sha256": sha(B / "RULES.json"),
    "archive_sha256": z["archive_sha256"],
    "lilly_if_published": 9926,
    "ptolemy_retained": 1066,
    "combined_if_published": 10992,
    "separate_chinese_source_notes": 72,
    "new_numbered_chapters": 1,
    "empirical_validations": 0,
    "runtime_promotions": 0,
    "remote_published": False,
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
