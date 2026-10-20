#!/usr/bin/env python3
"""Guarded append-only original Lilly CLXXXII Children records after source proof.

Refuse changed B07bd baseline, other source lane, source photograph SHA,
ZIP CRC and cold replay, any existing interrupted mutable recovery directory.
"""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import subprocess

B=Path(__file__).resolve().parent
ROOT=B.parents[3]
TASK=ROOT/"tasks/astro-source-audit-multipass-20261005"
INDEX=TASK/"LILLY_SOURCE_EXTRACTION_INDEX_V1.json"
CHINA=ROOT/"tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json"
CURRENT=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
LATEST=ROOT/"state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07be_CHILDREN.md"
SNAPSHOT=B/"recovery"
RECEIPT=B/"CANONICAL_PREPARE_RECEIPT_20261020.json"
BRANCH="research/astro-b07be-clxxxii-children-source-20261020"
CHINESE_SHA="bb73f28bf74a1ccb3a0a0e76b91c45f647128733047b8145094f28c9a4ae9d84"
FULL_ORIGINAL_1647_SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"

def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def sh(p):return sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def require_original_tracked(p):
    relative=str(p.relative_to(ROOT))
    if git("rev-parse","HEAD:"+relative)!=git("hash-object",str(p)):
        raise ValueError("Accepted original tracked file altered: "+relative)

def main():
    if git("branch","--show-current")!=BRANCH:
        raise ValueError("Not on isolated original Children source branch")
    if any(p.exists() for p in (SNAPSHOT,RECEIPT,LATEST)):
        raise ValueError("Already partially admitted: recovery review required")
    old=rd(INDEX)
    source=rd(B/"ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json")
    rules=rd(B/"RULES.json")
    accept=rd(B/"ACCEPTANCE.json")
    release=rd(B/"SOURCE_RELEASE_RECEIPT_PROVISIONAL_20261020.json")
    if (old["records_count"],old["batches"][-1]["id"],
            old["next"]["chapter"],old["next"]["pdf_page"],old["next"]["printed_page"])!=(
        13101,"B07bd","CLXXXII",791,757
    ):
        raise ValueError("Required last verified B07bd old source frontier changed")
    if old["read_numbered_chapters"]!=list(range(1,182)) or old["read_headed_units_count"]!=97:
        raise ValueError("Previous original source numbered/headed chapter index changed")
    if old["partial_numbered_chapters"]!=[]:
        raise ValueError("Parent source still marks incompletely reviewed chapters")
    if old["source_sha256"]!=FULL_ORIGINAL_1647_SHA:
        raise ValueError("Original Lilly Wellcome PDF SHA root mismatch")
    if old["empirical_validations"] or old["runtime_promotions"]:
        raise ValueError("Do not falsely count source notes as blind human predictions")
    if sh(CHINA)!=CHINESE_SHA or rd(CHINA)["sum_source_annotations"]!=355:
        raise ValueError("Independent Chinese V7 accepted source changed")
    if len(source["records"])!=len(rules["rules"])!=30 or rules["rules"]!=source["records"]:
        raise ValueError("Expected 30 original period Children source annotations")
    if [r["id"] for r in rules["rules"]]!=[f"R{i}" for i in range(13102,13132)]:
        raise ValueError("Historical source annotation IDs not sequential")
    if (accept["Lilly_before"],accept["Lilly_after_if_accepted"],
        accept["Western_after_if_accepted"],accept["next_R"])!=(
            13101,13131,14197,"R13132"
    ):
        raise ValueError("Original next count or chapter not as source dossier")
    if (sh(B/"ORIGINAL_1647_1659_CLXXXII_CHILDREN_SOURCE_V1.json"),
        sh(B/"RULES.json"))!=(accept["source_sha256"],accept["rules_sha256"]):
        raise ValueError("Original Children source dossier content edited after tests")
    if not release["ZIP_CRC_verified"] or not release["exact_member_SHA256_and_bytes_verified"]:
        raise ValueError("Cold portable archive CRC and original hashes not validated")
    if (release["independent_cold_extracted_tests"],release["independent_cold_extracted_green"])!=(14,14):
        raise ValueError("Cold portable test suite not completely replayed")
    archive=Path(release["full_archive_path_on_owner_computer"])
    if not archive.is_file() or sh(archive)!=release["archive_SHA256"]:
        raise ValueError("Cold portable evidence archive checksum drift")
    from build_b07be_children_source import photo_proof
    if photo_proof()!=source["source_photo_witnesses"]:
        raise ValueError("Independently original photographed folio SHA changed")

    for f in (
        INDEX,CHINA,
        TASK/"batches/B07bd/RULES.json",
        TASK/"batches/B07bd/ORIGINAL_CLXXXI_1647_1659_MARRIAGE_SOURCE_V1.json",
        TASK/"batches/B07bd/evidence/1647-original-folio757-iiif.jpg",
        TASK/"batches/B07bd/evidence/1659-original-folio757-thumb.jpg",
        TASK/"batches/B07bd/next_children_1647_photo_prefetch/1647-original-folio758-iiif.jpg",
    ):
        require_original_tracked(f)

    if any(r["actual_child_counts_or_sexes_independently_confirmed"]
           or r["allowed_for_medicine_parenting_reproductive_advice"]
           or r["runtime_astrological_rule_promoted"] for r in source["records"]):
        raise ValueError("Source-only reproductive claims cannot become clinical/empirical")
    SNAPSHOT.mkdir(exist_ok=False)
    for path,name in (
        (INDEX,"LILLY_INDEX_BEFORE_B07be.json"),
        (CURRENT,"CURRENT_BEFORE_B07be.md"),
        (CHINA,"CHINESE_V7_BEFORE_B07be.json"),
    ):
        (SNAPSHOT/name).write_bytes(path.read_bytes())

    old["batches"].append({
        "id":"B07be",
        "path":"batches/B07be/RULES.json",
        "records_count":30,
        "sha256":sh(B/"RULES.json"),
        "scope":(
            "Original first 1647 + separately typeset 1659 short Children CLXXXII "
            "on printed folio757/PDF791 with separate next original CLXXXIII Travels "
            "physical heading printed758/PDF792. 30 historical source-only "
            "R13102–R13131: old negative Mercury combustion/Gemini barren and "
            "Jupiter twelfth arguments overruled by Moon/aspects, tentative "
            "four-child count then reductions and contradictory male/female "
            "survival conjectures, sibling harmony and Venus child preferment. "
            "No actual merchant children record verified, no medicine, no real "
            "human predictive success, zero astrological runtime promotion."
        )
    })
    old["records_count"]=13131
    old["status"]="BOOK_III_CLXXXII_CHILDREN_PHYSICAL_SOURCE_COVERED_NEXT_CLXXXIII_TRAVELS"
    old["read_numbered_chapters"].append(182)
    old["read_headed_units_count"]=98
    old["completed_original_source_units_with_uncertainty"].append({
        "printed_chapter":"CLXXXII",
        "editorial_ordinal":182,
        "heading":"Of Children",
        "physical_source_start_pdf":791,
        "accepted_through_pdf":792,
        "printed_folios":[757,758],
        "children_substantive_original_folios":[757],
        "next_travels_source_heading_original_folio":758,
        "source_batch":"B07be",
        "historical_start":"R13102",
        "historical_end":"R13131",
        "complete":True,
        "physical_original_source_span_covered":True,
        "original_1647_1659_two_printings_pageSHA_checked":True,
        "original_Astro_glyphs_complete_expert_critical_edition":False,
        "original_no_issue_negative_overridden_by_positive_children":True,
        "original_four_children_are_tentative_not_undisputed_final_count":True,
        "original_Moon_Mars_positive_then_mortality_negative_reused":True,
        "real_merchant_children_count_birth_certificates_unverified":True,
        "medical_or_child_health_accuracy_unverified":True,
        "blind_real_human_predictive_tests":0,
        "runtime_astrological_promotions":0,
    })
    old["next"]={
        "pdf_page":792,"printed_page":758,
        "chapter":"CLXXXIII",
        "printed_chapter_numeral":"CLXXXIII",
        "editorial_source_sequence_ordinal":183,
        "heading":"Of Travels",
        "include_opening_paragraph":True,
        "extracted":False,
        "boundary_image_read":True,
        "position":(
            "1647 original printed758/PDF792 begins new ninth-house CLXXXIII Travels "
            "with a side note already claiming known travel to Barbary and Holland. "
            "Neither side note nor first prose paragraph is semantically scored in "
            "B07be, next R13132. Earlier original source photos p758 and p759 already prefetched."
        ),
        "research_scope":(
            "Original eighteenth-century (1647) historical merchant long-distance "
            "travel interpretations; existing marginal 'thrice beyond Sea' source is "
            "already-known retrospective, not a blinded astrological prediction."
        ),
    }
    old["current_state"]="state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261020_B07be_CHILDREN.md"
    old["chapter_CLXXXII_children_source_conflicting_count_and_survival"] = (
        "17th-century author's own known-merchant fifth-house example first asserts "
        "combustion and barren Gemini contraindicate issue, then overrides it to "
        "predict children. Interim 'probability of four' is qualified by two claimed "
        "lost children and two/three female possibilities; the Moon–Mars sextile is "
        "used as both favorable for fertility and negative child mortality testimony. "
        "No independent children register, survival or gender record; no medical "
        "validity or production astrology rule."
    )
    if (old["records_count"]!=sum(x["records_count"] for x in old["batches"])
        or old["read_numbered_chapters"]!=list(range(1,183))
        or old["empirical_validations"] or old["runtime_promotions"]):
        raise ValueError("New original index invariants failed")
    wr(INDEX,old)
    summary=(
        "# Original Lilly 1647 and 1659 CLXXXII Children — single-folio source covered B07be\n\n"
        "**30 original source-only R13102–R13131** document original printed757/"
        "PDF791 Children CLXXXII and *only the separate CLXXXIII Travels physical "
        "heading* on original printed758/PDF792, with four exact SHA verified "
        "1647/1659 printed source page images. Original historical source first "
        "cites barren Gemini, combust Mercury and obstructed Jupiter to "
        "suggest no children, then overrides these with Moon/aspects to predict "
        "children. It calls four a probability, removes two through supposed "
        "astrological adverse conditions, and conjectures sex and survival "
        "with internal conflicting signals. **No real merchant children or "
        "mortality outcomes independently verified.** The separate next "
        "Travels marginal note already recounts prior journeys; do not score "
        "it as a chart-derived forecast. **13,131 Lilly +1,066 Ptolemy = "
        "14,197 Western historical annotations**, independent accepted Chinese "
        "V9 **430** in its separate branch (aggregate original source counts "
        "14,627). Next source **R13132 CLXXXIII Travels**, original PDF792/"
        "printed758. No empirical human predictive successes, no medically "
        "supported historical claims and zero astrology runtime promotions.\n\n"
    )
    CURRENT.write_text(summary+"## Previous accepted historical checkpoint retained\n\n"+
                       CURRENT.read_text(encoding="utf-8"),encoding="utf-8")
    LATEST.write_text(summary+(B/"ORIGINAL_SOURCE_REVIEW_20261020.md").read_text(encoding="utf-8"),
                      encoding="utf-8")
    receipt={
        "batch":"B07be",
        "status":"GUARDED_ORIGINAL_1647_1659_CHILDREN_30_ADMITTED_LOCALLY_REMOTE_PENDING",
        "Lilly_before":13101,"Lilly_after":13131,"Ptolemy_retained":1066,
        "Western_after":14197,"Chinese_V7_frozen":355,
        "Chinese_V9_distinct_accepted_branch":430,
        "new_source_only_annotations":30,
        "four_original_page_images_exact_SHA_verified":True,
        "first_R":"R13102","last_R":"R13131","next_R":"R13132",
        "next_original_chapter":"CLXXXIII Of Travels",
        "next_original_pdf_frame":792,
        "old_index_sha256":sh(SNAPSHOT/"LILLY_INDEX_BEFORE_B07be.json"),
        "new_index_sha256":sh(INDEX),
        "original_source_notes_sha256":accept["source_sha256"],
        "original_rules_sha256":accept["rules_sha256"],
        "portable_archive_sha256":release["archive_SHA256"],
        "independent_cold_offline_tests":14,
        "original_CLAIMS_are_not_biographical_outcomes":True,
        "genuine_human_forecasts_validated":0,
        "astrology_runtime_promotions":0,
    }
    wr(RECEIPT,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
