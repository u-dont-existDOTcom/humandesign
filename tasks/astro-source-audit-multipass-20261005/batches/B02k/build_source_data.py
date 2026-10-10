"""Reproduce the canonical B02k source data from retained reader artifacts."""

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

BATCH = Path(__file__).parent
TASK = BATCH.parent.parent
SOURCE_ID = "LILLY1647_WELLCOME_B30338724"
SOURCE_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
SCOPE = ("Sixth-house heading and XLIV opening, PDF277/printed243 through the paragraph "
         "ending shew death on PDF292/printed258, immediately before DARIOT Abridged. "
         "All intervening unnumbered material included; XLIV continues beyond this batch.")


def read(name):
    return json.loads((BATCH / name).read_text(encoding="utf-8"))


def write(name, value):
    (BATCH / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(name):
    return hashlib.sha256((BATCH / name).read_bytes()).hexdigest()


def compile_data():
    readers = {reader: read(f"source_readers/{reader}/CANDIDATE_RULES.json") for reader in ("a", "b")}
    raw = [(reader.upper(), row) for reader, rows in readers.items() for row in rows]
    mapping = {row["id"]: f"LI.1647.II.XLIV.R{1358 + i}" for i, (_, row) in enumerate(raw)}
    assert len(mapping) == len(raw) == 192
    corrections = [{
        "id": "ROOT-C01", "local_id": "B075", "record_id": mapping["B075"],
        "source_pdf_page": 289, "printed_page": 255,
        "source_anchor": "and he be cleer of all misfortune",
        "original_candidate": readers["b"][74]["conditions"][1],
        "corrected_condition": "The ascendant lord is clear of all misfortune, OR not impeded especially by eighth OR sixth lord.",
        "reason": "The source says he after naming the ascendant lord. The reader candidate incorrectly made Moon the subject.",
        "stage": "Root full-span image comparison before independent candidate review",
        "original_reader_file_preserved": True,
    }, {
        "id": "ROOT-C02", "local_id": "B014", "record_id": mapping["B014"],
        "source_pdf_page": 284, "printed_page": 250,
        "source_anchor": "the Disease is not, or will be permanent",
        "original_candidate": readers["b"][13]["assertion"],
        "corrected_assertion": "With the stated benevolent-planet prerequisites, Lilly prints that one may safely judge 'the Disease is not, or will be permanent'. The wording is retained without inserting a second not.",
        "reason": "The candidate silently supplied not before be permanent. The original image lacks that second not; the possible scope of the earlier negative is an interpretation question.",
        "stage": "Root targeted original-image check during helper/report preparation, before independent candidate review",
        "original_reader_file_preserved": True,
    }]
    canonical_fields = {}
    for reader, original in raw:
        row = copy.deepcopy(original)
        if row["id"] == "B075":
            row["conditions"][1] = corrections[0]["corrected_condition"]
            row["condition_logic"]["expression"] = "Moon applies to L1 by trine/sextile AND (L1 clear of all misfortune OR L1 not impeded especially by L8/L6), preserving printed OR."
        if row["id"] == "B014":
            row["assertion"] = corrections[1]["corrected_assertion"]
            row["uncertainty"].append("U-ROOT01: Whether the earlier not has shared scope over will be permanent, or a word is absent, is not resolved here. No second not is inserted into the source wording.")
        canonical_fields[row["id"]] = row
    issues = []
    for reader in ("a", "b"):
        for item in read(f"source_readers/{reader}/UNRESOLVED.json"):
            issue = copy.deepcopy(item)
            issue["source_reader"] = reader.upper()
            ids = issue.get("candidate_ids", issue.get("affected_candidate_ids", []))
            issue["record_ids"] = [mapping[local] for local in ids]
            issue["reader_status"] = issue["status"]
            if issue["id"] == "U-A02":
                issue["status"] = "RESOLVED_TARGETED_SOURCE_CALLBACK"
                issue["resolution"] = "Root re-read original PDF153/printed119; retained R523 supplies the Saturn/Cancer cell. Other table cells are not silently imported."
            if issue["id"] == "U-B05":
                issue["status"] = "RESOLVED_REFERENCE_VALUE"
                issue["resolution"] = "Root re-read original PDF114/printed80: the stated mean is13d10m36s per24h. The separate analogy threshold is13d10m. The reference helper explicitly declares this same-work callback; source wording remains unchanged."
            if issue["id"] == "U-B14":
                issue["additional_limit"] = "Source degree labels do not supply minutes, seconds, modern-epoch coordinates or a uniquely specified ordinal-to-continuous-degree conversion."
            issue["source_resolved"] = issue["id"] in {"U-A02", "U-A18", "U-B05", "U-B18"}
            issues.append(issue)
    issues.append({"id": "U-ROOT01", "type": "source_negative_scope",
        "source_reader": "ROOT", "status": "RETAINED_WITHOUT_EMENDATION",
        "source_resolved": False, "reader_status": "IDENTIFIED_DURING_ROOT_IMAGE_CHECK",
        "candidate_ids": ["B014"], "record_ids": [mapping["B014"]],
        "pdf_pages": [284], "printed_pages": [250],
        "issue": "The source prints the Disease is not, or will be permanent. The earlier negative may have shared scope or the text may lack a word; neither interpretation is established in this batch.",
        "handling": "Preserve the phrase and its prerequisites. Do not insert a second not or turn the outcome into an executable duration predicate.",
        "source_anchor": "the Disease is not, or will be permanent"})
    issue_links = {local: [] for local in mapping}
    for issue in issues:
        for local in issue.get("candidate_ids", issue.get("affected_candidate_ids", [])):
            issue_links[local].append(issue["id"])
    rules = []
    for reader, original in raw:
        row = canonical_fields[original["id"]]
        pages = row["pdf_pages"]
        anchor = row["anchor"].split(";")[0].strip()
        lookup = row.get("lookup_key")
        title = (f"{lookup['namespace']} correspondence: {lookup['value']}" if lookup else anchor)
        rules.append({
            "id": mapping[row["id"]], "local_id": row["id"], "title": title,
            "kind": row["kind"],
            "source_locator": {"source_id": SOURCE_ID, "source_sha256": SOURCE_SHA,
                "book": "II", "section_key": "II.XLIV.opening", "pdf_pages": pages,
                "printed_sequence_expected": [page - 34 for page in pages],
                "visible_printed_labels": ["244" if page == 280 else str(page - 34) for page in pages],
                "passage_anchor": anchor,
                "anchor_note": "Locating phrase with long-s, spacing, and planet/sign glyph names normalized; not a diplomatic transcription. Table row identity is retained in source_fields.lookup_key."},
            "genre": "historical_horary_source", "statement_type": "editor_normalized_paraphrase",
            "source_attribution": row.get("attribution", "Lilly"),
            "source_statement": row["assertion"],
            "prerequisites": [{"source_clauses": row["conditions"], "condition_logic": row["condition_logic"], "executable": False}],
            "qualifications_and_limits": row["exceptions"] + row["uncertainty"],
            "source_fields": row, "source_reader": reader, "unresolved_ids": issue_links[row["id"]],
            "runtime_status": "REFERENCE_ONLY_NOT_PROMOTED", "independent_evidence_unit": False,
            "case_id": None, "related_record_ids": [mapping[key] for key in row["dependencies"] if key in mapping],
            "external_dependency_references": [key for key in row["dependencies"] if key not in mapping],
        })
    write("ROOT_SOURCE_CORRECTIONS.json", {"corrections": corrections, "originals_unchanged": True})
    write("RECORD_ID_MAP.json", mapping)
    write("RULES.json", {"schema_version": 1, "batch": "B02k", "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA, "status": "SOURCE_ONLY_NOT_RUNTIME_OR_VALIDATION", "scope": SCOPE,
        "records_count": len(rules), "general_records_count": len(rules), "worked_example_records_count": 0,
        "rules": rules})

    a = read("source_readers/a/SECTION_COVERAGE.json")["sections"]
    b = read("source_readers/b/SECTION_COVERAGE.json")["sections"]
    groups = [([a[i]], a[i]["title"]) for i in range(7)]
    groups += [([a[7], a[8]], "Whether the Disease will be long or short: seasons and planetary duration"),
               ([a[9], b[0]], "Signes of a long or short Sicknesse"),
               ([b[1]], b[1]["section"]), ([b[2]], b[2]["section"])]
    sections = []
    for i, (segments, title) in enumerate(groups, start=1):
        ids = [key for segment in segments for key in segment["candidate_ids"]]
        pages = sorted({page for key in ids for page in canonical_fields[key]["pdf_pages"]})
        sections.append({"id": f"S{i:02d}", "title": title, "pdf_pages": pages,
                         "record_ids": [mapping[key] for key in ids],
                         "status": "ORIGINAL_IMAGES_READ_AND_EXTRACTED",
                         "reader_segment_count": len(segments), "known_substantive_omissions": []})
    next_passage = {"pdf_page": 292, "printed_page": 258, "chapter": "XLIV",
        "heading": "DARIOT Abridged.", "include_opening_paragraph": True,
        "opening_anchor": "In regard I have ever affected Dariot his Method of judgment in sicknesses",
        "position": "Below the completed paragraph ending shew death. Include heading and full italic introduction, then continue on PDF293.",
        "extracted": False, "boundary_image_read": True}
    write("SECTION_COVERAGE.json", {"batch": "B02k", "scope": SCOPE,
        "admitted_pdf_pages": list(range(277, 293)), "section_unit_count": len(sections),
        "count_semantics": "Eleven coverage units, including one unheaded transition. Two reader segments of the same continuous duration discussion are joined; this is not a count of numbered chapters.",
        "sections": sections, "whole_chapter_complete": False, "book_complete": False, "next": next_passage})
    write("UNRESOLVED.json", {"batch": "B02k", "register_entries_count": len(issues),
        "retained_limit_or_anomaly_entries_count": sum(not item["source_resolved"] for item in issues),
        "source_resolved_entries_count": sum(item["source_resolved"] for item in issues),
        "count_semantics": "Typed register entries, not a count of source errors. Resolved callbacks/errata are separated from retained grammar, terminology, implementation, evidence and witness limits.",
        "issues": issues})

    namespaces = {key: {} for key in ("house", "sign", "planet", "retained_planet_sign", "historical_fixed_star")}
    for rule in rules:
        row = rule["source_fields"]
        if "lookup_key" in row:
            lookup = row["lookup_key"]
            namespaces[lookup["namespace"]][str(lookup["value"])] = {
                "record_id": rule["id"], "source_items": row["source_items"], "source_locator": rule["source_locator"]}
    namespaces["retained_planet_sign"]["Saturn|Cancer"] = {
        "record_id": "LI.1647.I.XIX.R523", "source_items": ["Reins", "Belly", "Secrets"],
        "source_pdf_page": 153, "printed_page": 119, "new_record": False,
        "provenance": "Retained source row, original image re-read; case and long-s normalized."}
    for name, sign, number, label, local in [
        ("Antares", "Sagittarius", 4, "in the fourth Sagittarius", "B108"),
        ("Lans/Lanx Australis", "Scorpio", 9, "about the ninth of Scorpio", "B108"),
        ("Palilicium", "Gemini", 4, "in four Gemini", "B108"),
        ("Caput Medusae", "Taurus", 20, "in twenty Taurus", "B108"),
        ("Pleiades", "Taurus", 24, "in 24 Taurus", "B118")]:
        namespaces["historical_fixed_star"][name] = {"record_id": mapping[local], "sign": sign,
            "source_degree_number": number, "source_degree_label_normalized": label,
            "minutes": None, "seconds": None, "modern_epoch_longitude": None,
            "ordinal_to_continuous_degree_convention": None, "nearness_threshold": None,
            "precision_note": "A historical degree label, not a modern exact coordinate; about remains in the Australis label."}
    write("REFERENCE_TABLES.json", {"batch": "B02k", "source_only": True, "clinical_mapping": False,
        "catalogue_counts": {"house": 12, "sign": 12, "planet": 7},
        "extra_retained_callback_cells": 1, "historical_star_labels": 5, "namespaces": namespaces})
    counts = {"batch": "B02k", "new_source_records": len(rules), "first_record_number": 1358,
        "last_record_number": 1549, "previous_lilly_records": 1357, "cumulative_lilly_records": 1549,
        "retained_ptolemy_records": 1066, "combined_lilly_ptolemy_records": 2615,
        "general_methodological_illustrative_records": len(rules), "worked_narrative_records": 0,
        "dated_enquiries": 0, "worked_horoscope_figures": 0, "independently_verified_clinical_outcomes": 0,
        "source_record_independence_not_claimed": True, "coverage_units": len(sections),
        "admitted_pdf_pages": 16, "catalogue_rows": 31, "typed_register_entries": len(issues),
        "retained_limits_and_anomalies": sum(not item["source_resolved"] for item in issues),
        "source_resolved_register_entries": sum(item["source_resolved"] for item in issues),
        "kind_counts": dict(Counter(rule["kind"] for rule in rules)),
        "retained_callback_records_not_added_to_count": 4,
        "whole_XLIV_complete": False, "runtime_promotions": 0, "predictive_accuracy_evaluated": False}
    write("COUNTS.json", counts)
    index = read("RETAINED_LILLY_INDEX_BEFORE.json")
    assert index["records_count"] == 1357
    index["status"] = "BOOK_I_COMPLETE_BOOK_II_THROUGH_XLIII_COMPLETE_XLIV_OPENING_READ_OTHER_SECTIONS_OPEN"
    index["records_count"] = 1549
    index["batches"].append({"id": "B02k", "path": "batches/B02k/RULES.json", "records_count": 192,
                             "sha256": digest("RULES.json"), "scope": SCOPE})
    index["next"] = next_passage
    index["partial_numbered_chapters"] = [{"chapter": 44, "label": "XLIV", "batch": "B02k", "scope": SCOPE}]
    index["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02k.md"
    write("LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json", index)
    (TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(counts, ensure_ascii=False))


if __name__ == "__main__":
    compile_data()
