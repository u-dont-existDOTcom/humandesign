#!/usr/bin/env python3
"""Only after independent archive/source tests: append original Lilly B07bd notes.

Fail closed on modified parent/foreign source indexes, already-open recovery,
missing original-photos, zero-human-outcome audit, or archive checksum mismatch.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
TASK = ROOT / "tasks/astro-source-audit-multipass-20261005"
INDEX = TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA = ROOT / "tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bd_MARRIAGE.md"
RECOVERY = B / "recovery"
RECEIPT = B / "CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH = "research/astro-b07bd-clxxxi-marriage-source-20261020"
SOURCE_FILE = B / "ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json"
RULE_FILE = B / "RULES.json"
SOURCE_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"

def read(p):
    return json.loads(p.read_text(encoding="utf-8"))

def sha(p):
    return sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def require_repository_file_untouched(p):
    relative = str(p.relative_to(ROOT))
    old = git("rev-parse", "HEAD:" + relative)
    new = git("hash-object", str(p))
    if old != new:
        raise ValueError("Refuse modified accepted repository file " + relative)

def main():
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("Source acceptance attempted outside intended isolated branch")
    if RECOVERY.exists() or RECEIPT.exists() or LATEST.exists():
        raise ValueError("Interrupted previous acceptance; reconcile rather than restart")
    index=read(INDEX)
    china=read(CHINA)
    source=read(SOURCE_FILE)
    rules=read(RULE_FILE)
    acceptance=read(B/"ACCEPTANCE.json")
    release=read(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if index["records_count"] != 13044 or index["batches"][-1]["id"]!="B07bc":
        raise ValueError("Parent accepted index no longer ends with B07bc")
    if index["read_numbered_chapters"] != list(range(1,181)):
        raise ValueError("Parent numbered original-source chapter list changed")
    if index["read_headed_units_count"] != 96 or index["partial_numbered_chapters"] != []:
        raise ValueError("Parent original-source headed-unit frontier changed")
    if (index["next"]["chapter"],index["next"]["pdf_page"],index["next"]["printed_page"]) != (
        "CLXXXI",788,754
    ):
        raise ValueError("Parent next-original marriage chapter not at correct physical divider")
    if index["empirical_validations"] or index["runtime_promotions"]:
        raise ValueError("Historic source does not add measured human outcomes")
    if index["source_sha256"]!=SOURCE_SHA or len(index["batches"])!=0 and sum(
        b["records_count"] for b in index["batches"]
    )!=13044:
        raise ValueError("Parent original source index checksum/count drift")
    if china["sum_source_annotations"]!=355 or sha(CHINA)!=acceptance["Chinese_V7_index_sha256"]:
        raise ValueError("Parent separate Chinese V7 source SHA drift")
    if len(source["all_source_records"])!=57 or len(rules["rules"])!=57:
        raise ValueError("57 original marriage source-only notes expected")
    if [r["id"] for r in rules["rules"]] != [f"R{n}" for n in range(13045,13102)]:
        raise ValueError("Nonconsecutive Lilly source annotation IDs")
    if source["all_source_records"]!=rules["rules"] or source["next_R"]!="R13102":
        raise ValueError("Source index and rule bundle disagree")
    if (acceptance["Lilly_before"],acceptance["Lilly_after_if_accepted"],
        acceptance["Western_after_if_accepted"])!=(13044,13101,14167):
        raise ValueError("Expected historical source counts changed")
    if (sha(SOURCE_FILE),sha(RULE_FILE))!=(acceptance["source_notes_sha256"],
                                           acceptance["rules_sha256"]):
        raise ValueError("Source notes/RULES not accepted exact SHA")
    if not release["ZIP_CRC_verified"] or not release["member_SHA256_and_bytes_verified"]:
        raise ValueError("Portable source evidence archive not independently verified")
    if (release["independently_extracted_standalone_original_tests_executed"],
        release["independently_extracted_actual_offline_tests_passed"],
        release["independently_extracted_optional_SWE_tests_skipped"])!=(19,17,2):
        raise ValueError("Independent extracted portable tests incomplete")
    archive=Path(release["archive_path_on_owner_machine"])
    if not archive.is_file() or sha(archive)!=release["archive_sha256"]:
        raise ValueError("Portable original source archive SHA drift")
    from build_b07bd_marriage_source import photo_witnesses
    if photo_witnesses()!=source["four_original_folio_photographs"]:
        raise ValueError("Original eight photographic witnesses changed")

    for p in (
        INDEX,CHINA,
        TASK/"batches/B07bc/RULES.json",
        TASK/"batches/B07bc/ORIGINAL_1647_1659_SICKNESSE_SERVANTS_SOURCE_V1.json",
        TASK/"batches/B07bb/evidence/1647_original-788.jpg",
        TASK/"batches/B07bc/evidence/1659_original_djvu_783.jpg",
    ):
        require_repository_file_untouched(p)

    for row in source["all_source_records"]:
        if row["real_human_behavioral_prediction_validation_count"] or row["runtime_astrological_model_promoted"]:
            raise ValueError("Cannot promote editorial predictions as human validated results")
    RECOVERY.mkdir(exist_ok=False)
    for p,name in ((INDEX,"LILLY_INDEX_BEFORE_B07bd.json"),
                   (CURRENT,"CURRENT_BEFORE_B07bd.md"),
                   (CHINA,"CHINESE_V7_BEFORE_B07bd.json")):
        (RECOVERY/name).write_bytes(p.read_bytes())

    index["batches"].append({
        "id":"B07bd",
        "path":"batches/B07bd/RULES.json",
        "records_count":57,
        "sha256":sha(RULE_FILE),
        "scope":(
            "Original first 1647 and independent 1659 printed CLXXXI seventh-house "
            "Marriage folios754-757/PDF788-791: 57 source-only R13045-R13101; "
            "prediction of late marriage after29, exactly two wives and two sweethearts; "
            "contrary one-marriage astrological testimony; spouse features, wealth, "
            "east/west geography and terms-vs-months time ambiguity. Mercury/Venus "
            "Cazimi source nominal17arcmin vs modern SWIEPH73-76arcmin under explicit "
            "unverified 1616 Julian-clock assumptions. Known merchant, no independent "
            "marriage records or human predictive success; next CLXXXII Children below "
            "folio757 physical divider."
        )
    })
    index["records_count"]=13101
    index["status"]="BOOK_III_CLXXXI_MARRIAGE_PHYSICAL_SOURCE_COVERED_NEXT_CLXXXII_CHILDREN"
    index["read_numbered_chapters"].append(181)
    index["read_headed_units_count"]=97
    index["completed_original_source_units_with_uncertainty"].append({
        "printed_chapter":"CLXXXI",
        "editorial_ordinal":181,
        "heading":"Of Marriage",
        "physical_source_start_pdf":788,
        "accepted_through_pdf":791,
        "printed_folios":[754,755,756,757],
        "source_batch":"B07bd",
        "historical_start":"R13045",
        "historical_end":"R13101",
        "complete":True,
        "physical_source_span_covered":True,
        "two_original_printed_edition_images_sha_verified":True,
        "whole_1659_source_binary_sha_verified":False,
        "full_expert_diplomatic_source_critical_edition_finished":False,
        "original_marriage_predictions_known_to_author_and_not_blind":True,
        "verified_real_merchant_marital_history":False,
        "original_venus_cazimi_at_17arcmin_source":True,
        "modern_Sun_Venus_separation_far_beyond_17arcmin_under_hypothetical_UT":True,
        "original_meridian_historical_UT_and_birthplace_verified":False,
        "independent_person_predictive_accuracy_validated":0,
        "production_rules_promoted":False
    })
    index["next"]={
        "pdf_page":791,"printed_page":757,
        "chapter":"CLXXXII",
        "printed_chapter_numeral":"CLXXXII",
        "editorial_source_sequence_ordinal":182,
        "heading":"Of Children",
        "include_opening_paragraph":True,
        "extracted":False,
        "boundary_image_read":True,
        "position":(
            "1647 first printed757/PDF791, below physical divider from CLXXXI "
            "Marriage after only first two lines on this page. Full children text "
            "not extracted by B07bd, next source record R13102."
        ),
        "research_scope":(
            "Source-only fifth-house children case about known merchant, "
            "number/sex/birth/relationship claims not empirically validated."
        )
    }
    index["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07bd_MARRIAGE.md"
    index["chapter_CLXXXI_original_specific_numerical_outcome_caution"] = (
        "Lilly original 1647/1659 known merchant marriage source predicts only two "
        "wives/two sweethearts and marriage after age29, spouse appearances, inheritance "
        "and opposing wife origins; nothing is independently biographically verified "
        "or a blinded predictive success. Claimed Venus in Cazimi is at 17arcmin "
        "original printed exact whole-minute border, but differs >73arcmin from "
        "SWIEPH under one explicitly uncertain true-Julian UT hypothesis. This "
        "is a source/chart input inconsistency, not evidence about a real wife."
    )
    if (index["records_count"] != sum(b["records_count"] for b in index["batches"])
        or index["read_numbered_chapters"] != list(range(1,182))
        or index["empirical_validations"] or index["runtime_promotions"]):
        raise ValueError("Proposed accepted source index inconsistent")
    INDEX.write_text(json.dumps(index,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

    headline=(
        "# Original Lilly 1647/1659 CLXXXI Marriage — physically source covered B07bd\n\n"
        "**57 historical source-only notes R13045–R13101** from original printed754–757/"
        "PDF788–791 and separate 1659 printed edition DjVu783–786, with eight "
        "SHA/byte-verified original page images. These document an already-known "
        "merchant's *claimed* marriage after29, exactly two wives/two sweethearts, "
        "two spouse descriptions and contrasting origin/estate predictions. "
        "No independent biography, marriage certificate, human outcomes or "
        "prognostic success verified. Original Venus Cazimi asserted at a "
        "printed17′ Sun-Venus spacing versus modern true SWIEPH approx75′ "
        "for an explicitly unverified 1616 Julian/UT assumption; not resolved. "
        "**13,101 Lilly +1,066 Ptolemy=14,167 Western** accepted historical "
        "annotations, separate unchanged V7 Chinese355; independently accepted "
        "Chinese V9 BaZi210+ZiWei220 (430) on its own branch. "
        "Next Lilly **R13102**, Chapter **CLXXXII Of Children**, original "
        "printed757/PDF791 below physical divider. Real-human blind prediction "
        "validations **0**, astrology runtime promotions **0**.\n\n"
    )
    CURRENT.write_text(headline+"## Previous accepted historical checkpoint retained\n\n"+
                       CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(headline+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
                      encoding="utf-8")
    receipt={
        "batch":"B07bd",
        "status":"GUARDED_ORIGINAL_CLXXXI_57_NOTES_PREPARED_REMOTE_ACCEPTANCE_PENDING",
        "Lilly_before":13044,"Lilly_after":13101,"Ptolemy_retained":1066,
        "Western_after":14167,"separate_Chinese_V7_retained":355,
        "separate_Chinese_V9_source_total_in_other_branch":430,
        "new_historical_source_annotations":57,
        "new_8_source_photo_witnesses_verified":True,
        "original_martial_life_outcomes_independently_verified":False,
        "next_R":"R13102","next_original_pdf":791,"next_printed_chapter":"CLXXXII",
        "old_index_sha256":sha(RECOVERY/"LILLY_INDEX_BEFORE_B07bd.json"),
        "new_index_sha256":sha(INDEX),
        "source_notes_sha256":acceptance["source_notes_sha256"],
        "rules_sha256":acceptance["rules_sha256"],
        "archive_sha256":release["archive_sha256"],
        "portable_offline_tests_passed":17,
        "portable_optional_swieph_skipped":2,
        "Chinese_V7_sha256":sha(CHINA),
        "real_human_predictive_validations":0,
        "runtime_astrological_promotions":0
    }
    RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
