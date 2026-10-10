"""Rebuild the B02l canonical inventory from the two frozen source-reader files.

This compiler preserves documentary clauses. It is not a diagnostic rule engine.
"""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re

BATCH = Path(__file__).resolve().parent
TASK = BATCH.parent.parent
SOURCE_ID = "LILLY1647_WELLCOME_B30338724"
SOURCE_SHA = "2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
SCOPE = ("XLIV continuation: DARIOT Abridged heading and complete italic introduction "
         "on PDF292/printed258 through the full upper bridge ending Judgments of this House "
         "on PDF302/printed268; every intervening unnumbered section included. Stop above "
         "the divider before Hermes Trismegistus upon the first Decumbiture of the Sick. "
         "Chapter XLIV remains incomplete.")


def read(name):
    return json.loads((BATCH / name).read_text(encoding="utf-8"))


def write(name, data):
    (BATCH / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(name):
    return hashlib.sha256((BATCH / name).read_bytes()).hexdigest()


def referenced_locals(texts, mapping):
    """Resolve explicit local tokens and same-prefix inclusive ranges only."""
    result = set()
    for text in texts:
        for first, last in re.findall(r"([AB]\d{3})[-–]([AB]\d{3})", text):
            if first[0] == last[0]:
                result.update(f"{first[0]}{n:03d}" for n in range(int(first[1:]), int(last[1:]) + 1))
        result.update(re.findall(r"\b[AB]\d{3}\b", text))
    return sorted(result.intersection(mapping))


def compile_data():
    raw = [(label, row) for label in ("a", "b")
           for row in read(f"source_readers/source_{label}/source_records.json")]
    before = read("RETAINED_LILLY_INDEX_BEFORE.json")
    assert before["records_count"] == 1549
    first = before["records_count"] + 1
    mapping = {row["local_id"]: f"LI.1647.II.XLIV.R{first+i}" for i, (_, row) in enumerate(raw)}
    assert len(raw) == len(mapping) == 101
    issues = []
    for label in ("a", "b"):
        for original in read(f"source_readers/source_{label}/SOURCE_ISSUES.json")["issues"]:
            local_ids = original.get("records", original.get("local_ids", []))
            issue = {
                "id": original["issue_id"], "source_reader": label.upper(),
                "category": original.get("type", original.get("category")),
                "pdf_pages": original.get("pages", original.get("pdf_pages", [])),
                "local_ids": local_ids, "record_ids": [mapping[x] for x in local_ids],
                "observation": original["observation"], "disposition": original["disposition"],
                "source_resolved": original["issue_id"] in {"SA-I06", "B-SI-10"},
                "reader_observation_unchanged": copy.deepcopy(original),
            }
            issue["status"] = "SOURCE_READING_RESOLVED" if issue["source_resolved"] else "LIMIT_RETAINED"
            if issue["id"] == "SA-I06":
                issue["resolution"] = "The fixed-sign class is stated with three illustrative examples introduced by as in; no fourth glyph is inserted and Scorpio is not declared excluded from the class."
            if issue["id"] == "B-SI-10":
                issue["resolution"] = "Original PDF299 visibly includes the sextile glyph with square and opposition of Mars. B-SI-11 separately retains the sentence's twelfth-house grammar limit."
            issues.append(issue)
    for number, local, page, category, finding in [
        (1, "A025", 295, "node_glyphs", "The two glyphs after Scorpio are South Node and North Node. SA-I04 separately retains the unresolved reach of with over Leo/Scorpio; identifying the glyphs does not settle that grammar."),
        (2, "A047", 297, "planet_glyph", "The opening fever-cause planet on PDF297 is Mars, continuing the preceding Mars sequence."),
        (3, "A027", 295, "errata_body_agreement", "The original errata at PDF888 specify usually at printed261 line23; the corresponding body text already reads usually."),
        (4, "A045", 296, "errata_body_agreement", "The original errata at PDF888 specify returning at printed262 line33; the corresponding body text already reads returning."),
    ]:
        issues.append({"id": f"ROOT-SR{number:02d}", "source_reader": "ROOT",
                       "category": category, "pdf_pages": [page] + ([888] if number > 2 else []),
                       "local_ids": [local], "record_ids": [mapping[local]],
                       "observation": finding, "disposition": "Retain the verified source reading; no conjectural emendation.",
                       "source_resolved": True, "status": "SOURCE_READING_RESOLVED"})
    issue_links = {key: [] for key in mapping}
    for issue in issues:
        for local in issue["local_ids"]:
            issue_links[local].append(issue["id"])
    rules = []
    amendments = []
    for label, source in raw:
        row = copy.deepcopy(source)
        local = row["local_id"]
        if local == "A011":
            # IF-01: original PDF294/printed260 visibly prints the plural.
            # Amend the canonical copy; preserve the frozen producer file.
            changes = []
            for field, index in (("proposition", None), ("conditions", 1), ("uncertainties", 0)):
                before_text = row[field] if index is None else row[field][index]
                after_text, n = re.subn(r"principal ([Ss])ignificator\b", r"principal \1ignificators", before_text)
                assert n == 1
                if index is None:
                    row[field] = after_text
                else:
                    row[field][index] = after_text
                changes.append({"source_field": field if index is None else f"{field}[{index}]",
                                "before": before_text, "after": after_text})
            amendments.append({"finding_id": "IF-01", "record_id": mapping[local], "local_id": local,
                "original_pdf_page": 294, "printed_page": 260,
                "source_anchor": "or from the principall Significators in the Figure",
                "reason": "The printed source names plural Significators. Restore grammatical number in the canonical fields and their duplicates; the repeated-from ambiguity remains unresolved. No all-of-group or voting rule is inferred.",
                "changes": changes, "frozen_reader_file_modified": False})
        dependencies = referenced_locals(row["dependencies"], mapping)
        rules.append({
            "id": mapping[local], "local_id": local, "title": row["proposition"], "kind": row["kind"],
            "source_locator": {"source_id": SOURCE_ID, "source_sha256": SOURCE_SHA, "book": "II",
                "section_key": "II.XLIV.Dariot_continuation", "source_section": row["section"],
                "pdf_pages": row["pdf_pages"], "printed_sequence_expected": row["printed_pages"],
                "visible_printed_labels": [str(p) for p in row["printed_pages"]],
                "passage_anchor": row["source_anchor"],
                "anchor_note": "Locating wording with long-s, line breaks, spacing and astrological glyph names normalized; not a diplomatic full transcription. Original page images govern."},
            "genre": "historical_horary_source", "statement_type": "editor_normalized_paraphrase",
            "source_attribution": row["attribution"], "source_statement": row["proposition"],
            "prerequisites": [{"source_clauses": row["conditions"], "executable": False,
                               "logic_policy": "Retain explicit AND/OR/negative/modal wording and source dependencies; unresolved syntax is not compiled to a single Boolean predicate."}],
            "consequent": row["outcomes"], "exceptions_and_modifiers": row["exceptions"],
            "qualifications_and_limits": row["exceptions"] + row["uncertainties"],
            "conventions": {"calendar_time_basis": "No dated figure in this span; no calendar convention inferred.",
                            "astrological_terms": "Earlier definitions remain dependencies; no modern clinical mapping.",
                            "duplicate_roles": "Repeated roles may name the same planet; no independence or vote count inferred."},
            "bridge_to_implementation": {"status": "DOCUMENTARY_ONLY", "note": row["implementation_note"],
                "bounded_helpers": "Separate reference helpers only for B031 time-origin selection, B032 angular offsets, and B041-B042 unsynthesized timing options."},
            "source_fields": row, "source_reader": label.upper(), "unresolved_ids": issue_links[local],
            "runtime_status": "REFERENCE_ONLY_NOT_PROMOTED", "independent_evidence_unit": False, "case_id": None,
            "related_record_ids": [mapping[x] for x in dependencies if x != local],
            "dependency_text_preserved": row["dependencies"],
            "external_dependency_references": [t for t in row["dependencies"] if not re.fullmatch(r"[AB]\d{3}", t)],
        })
    write("RECORD_ID_MAP.json", mapping)
    write("ROOT_SOURCE_CORRECTIONS.json", {"canonical_record_amendments": amendments, "frozen_reader_files_unchanged": True,
        "note": "The listed source-adjudicated amendment changes only the canonical copy; all frozen producer files remain unchanged. Other source-detail resolutions are tracked in UNRESOLVED and TEXTUAL_CHECKS. A reader's informal chat summary called the A043 actor Jupiter; its frozen record and the source correctly say Saturn. That chat typo is not canonical data."})
    write("RULES.json", {"schema_version": 1, "batch": "B02l", "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA, "status": "SOURCE_ONLY_NOT_RUNTIME_OR_VALIDATION", "scope": SCOPE,
        "records_count": len(rules), "general_records_count": len(rules), "worked_example_records_count": 0,
        "rules": rules})
    groups = [
        ("DARIOT Abridged: complete italic introduction", "A", 1, 1),
        ("If the Party be sicke", "A", 2, 8),
        ("Cause of the Disease inward or outward", "A", 9, 21),
        ("Of the qualitie and nature of the Disease", "A", 22, 54),
        ("Right or left side and member", "B", 1, 6),
        ("Body, mind, or both", "B", 7, 24),
        ("Unheaded natal, mundane and luminary callbacks", "B", 25, 29),
        ("Crisis or critical days", "B", 30, 37),
        ("Recovery timing and the complete practical/Hermes bridge", "B", 38, 47),
    ]
    bylocal = {r["local_id"]: r for r in rules}
    sections = []
    for i, (title, prefix, start, stop) in enumerate(groups, 1):
        ids = [f"{prefix}{n:03d}" for n in range(start, stop+1)]
        pages = sorted({p for x in ids for p in bylocal[x]["source_locator"]["pdf_pages"]})
        sections.append({"id": f"S{i:02d}", "title": title, "pdf_pages": pages,
                         "printed_pages": [p-34 for p in pages], "local_ids": ids,
                         "record_ids": [mapping[x] for x in ids],
                         "status": "ORIGINAL_IMAGES_READ_AND_EXTRACTED", "known_substantive_omissions": []})
    next_passage = {"pdf_page": 302, "printed_page": 268, "chapter": "XLIV",
        "heading": "Hermes Trismegistus upon the first Decumbiture of the Sick.",
        "include_opening_paragraph": True,
        "opening_anchor": "The heavenly Rayes or Influences proceeding and emitted from the seven Planets",
        "position": "Below the horizontal divider on PDF302. Include the heading and complete opening paragraph, then continue on PDF303. The entire preceding upper bridge is complete.",
        "extracted": False, "boundary_image_read": True}
    write("SECTION_COVERAGE.json", {"batch": "B02l", "scope": SCOPE,
        "admitted_pdf_pages": list(range(292, 303)), "section_unit_count": len(sections),
        "count_semantics": "Nine editorial coverage units, not nine numbered chapters. Fine-grained reader units are retained separately and are not added to the record total.",
        "sections": sections, "whole_chapter_complete": False, "book_complete": False, "next": next_passage})
    write("UNRESOLVED.json", {"batch": "B02l", "register_entries_count": len(issues),
        "retained_limit_or_anomaly_entries_count": sum(not i["source_resolved"] for i in issues),
        "source_resolved_entries_count": sum(i["source_resolved"] for i in issues),
        "count_semantics": "Typed observations, not source-error counts. Thirty-eight producer issue observations are preserved; two are resolved readings. Four additional root glyph/errata resolutions are separately typed. A resolved glyph can coexist with an unresolved grammatical attachment in a linked entry.",
        "items": issues})
    ptolemy_bytes = (TASK / "PTOLEMY_ENGLISH_EXTRACTION_INDEX_V1.json").read_bytes()
    ptolemy = json.loads(ptolemy_bytes)
    (BATCH / "RETAINED_PTOLEMY_INDEX_SNAPSHOT.json").write_bytes(ptolemy_bytes)
    pcount = sum(b["records_count"] for b in ptolemy["source_batches"])
    assert pcount == ptolemy["source_records"] == sum(b["records"] for b in ptolemy["books"].values()) == 1066
    write("PTOLEMY_COUNT_RECEIPT.json", {"status": "RECOMPUTED_RETAINED_INDEX_COUNT",
        "retained_records": pcount, "retained_batch_count": len(ptolemy["source_batches"]),
        "snapshot_sha256": digest("RETAINED_PTOLEMY_INDEX_SNAPSHOT.json"),
        "new_ptolemy_source_reading_this_batch": False,
        "method": "Sum retained index source_batches records_count and compare with its source_records and sum of book records. No new audit of every Ptolemy source row claimed."})
    last = first + len(rules) - 1
    counts = {"batch": "B02l", "new_source_records": len(rules), "first_record_number": first,
        "last_record_number": last, "previous_lilly_records": before["records_count"],
        "cumulative_lilly_records": last, "retained_ptolemy_records": pcount,
        "combined_lilly_ptolemy_records": last+pcount,
        "general_methodological_illustrative_records": len(rules), "worked_narrative_records": 0,
        "dated_enquiries": 0, "worked_horoscope_figures": 0, "independently_verified_clinical_outcomes": 0,
        "source_record_independence_not_claimed": True, "coverage_units": len(sections), "admitted_pdf_pages": 11,
        "typed_register_entries": len(issues),
        "retained_limits_and_anomalies": sum(not i["source_resolved"] for i in issues),
        "source_resolved_register_entries": sum(i["source_resolved"] for i in issues),
        "kind_counts": dict(Counter(r["kind"] for r in rules)),
        "retained_callback_records_not_added_to_count": 4,
        "whole_XLIV_complete": False, "runtime_promotions": 0, "predictive_accuracy_evaluated": False}
    write("COUNTS.json", counts)
    index = copy.deepcopy(before)
    index["status"] = "BOOK_I_COMPLETE_BOOK_II_THROUGH_XLIII_COMPLETE_XLIV_THROUGH_DARIOT_READ_OTHER_SECTIONS_OPEN"
    index["records_count"] = last
    index["batches"].append({"id": "B02l", "path": "batches/B02l/RULES.json", "records_count": len(rules),
                              "sha256": digest("RULES.json"), "scope": SCOPE})
    index["next"] = next_passage
    index["partial_numbered_chapters"] = [{"chapter": 44, "label": "XLIV", "batches": ["B02k", "B02l"],
        "scope": "Sixth-house opening and continuation through Dariot/Lilly practical bridge; Hermes and following XLIV material remain open."}]
    index["current_state"] = "state/ASTROLOGY_SOURCE_AUDIT_LATEST_20261010_B02l.md"
    write("LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json", index)
    (TASK / "LILLY_SOURCE_EXTRACTION_INDEX_V1.json").write_bytes((BATCH / "LILLY_SOURCE_EXTRACTION_INDEX_SNAPSHOT.json").read_bytes())
    old_rules = json.loads((BATCH.parent / "B02k" / "RULES.json").read_text())["rules"]
    retained = [r for r in old_rules if int(r["id"].rsplit("R", 1)[1]) in (1359, 1360, 1361, 1438)]
    assert len(retained) == 4
    write("RETAINED_SOURCE_EXCERPTS.json", {"not_new_records": True, "records": retained,
        "original_pages_re_read_this_turn": [277, 283],
        "comparison_scope": "Local time-origin hierarchies and timing-unit discretion; no global rule override."})
    print(json.dumps(counts))


if __name__ == "__main__":
    compile_data()
