"""Advance audit-progress mirrors after the source batch, preserving historical artifacts."""
from pathlib import Path
import json
import subprocess

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
T = ROOT / "tasks/astro-source-audit-multipass-20261005"
BASE = "ce054e8334bd23b56c962e68f27d2005eeb002c7"
subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT, check=True)
current = json.loads((T / "CURRENT_PASS.json").read_text())
assert (current["counts"]["source_records"], current["counts"]["ptolemy_read_sections"]) == (708, 48), "Already advanced or conflicting checkpoint; inspect before rerun"
rules = json.loads((B / "RULES.json").read_text())
assert rules["records_count"] == len(rules["records"]) == 37
coverage = json.loads((B / "SECTION_COVERAGE.json").read_text())
next_range = "Full English II.3 from PDF153/printed129 through final city-foundation paragraphs and note1 on PDF185/printed161; stop before II.4 heading (note2 belongs to II.4)."
current.update(completed="Source intake; full English Ptolemy Books I/III/IV including both endings and II.1-II.2; B01n archive restored and progress mirrors synchronized", current="B01o English II.1-II.2 complete; previous timing recovery resolved; parent audit OPEN", next_batch="B01p", next_range=next_range, next_actor="Next authorized source-audit continuation; no further restoration or upload needed", last_verified_unit="II.2 final paragraph and explanatory note on PDF151/printed127; next II.3 start/end headings located only", source_rule_records=745)
current["counts"].update(ptolemy_read_sections=50, ptolemy_unread_sections=11, source_records=745, isolated_definition_tests=550, ptolemy_book_II_read_sections=2, general_context_glossary_entries=5, retained_historical_region_portraits=6)
current["counting_note"] = "745 Ptolemy source records; no independent human observations or predictive successes.550 source-reference tests plus34 methodology tests; actual latest execution is recorded in batches/B01o/VERIFICATION.json."
current["latest_reports"] = ["batches/B01o/REPORT.md", "batches/B01o/VERIFICATION.json", "batches/B01o/B01n_RECOVERY_VERIFICATION.json"]
current["secondary_progress_mirrors"] = {"status":"SYNCHRONIZED_THROUGH_B01o", "paths":["PASS_PLAN.json", "SECTION_DISCOVERY.json"], "explanation":"Both mirrors now contain all completed English sections through II.2; B01n ordinary artifacts have been restored hash-identically.", "action":"No recovery rerun needed; continue first unread unit."}
current["archive_storage"] = "Original B01n archive parts retained unchanged. All21 member files now materialized as ordinary inspectable files with matching digests."
current["stop_admission"] = {"parent_status":"OPEN", "remaining_gap":"Eleven BookII chapters, other supplied books, full cross-source reconciliation, compilation and evaluation.", "next_action":next_range, "authority":"Owner-authorized multi-pass source audit and current continuation.", "executed_this_increment":"Restored21-member timing archive, refreshed lagged mirrors, ran recovered559-check suite; read/extracted37 new source records with25 new checks and saved first-unread boundary.", "delivery_boundary":"Completed source-reading batch under the existing owner-approved multiple-pass contract; parent remains OPEN and no unattended execution is claimed."}
plan = json.loads((T / "PASS_PLAN.json").read_text())
for p in plan["passes"]:
    if p["id"] == "P2": p["status"] = "PTOLEMY_61_INDEXED;50_ENGLISH_SECTIONS_READ_MAPPED"
    elif p["id"] == "P3": p["status"] = "ENGLISH_I_III_IV_AND_II1_II2_COMPLETE;745_RECORDS;REMAINDER_OPEN"
    elif p["id"] == "P4": p["status"] = "550_SOURCE_REFERENCE_CHECKS_PLUS34_METHODOLOGY;TWENTY_TARGETED_COMPARISONS;LATEST_EXECUTION_IN_B01o_VERIFICATION"
first = plan["batches"][0]
assert first["id"] == "B01" and not any(x["id"] == "B01o" for x in first["completed_subbatches"])
first["next"] = next_range
first["completed_subbatches"].append({"id":"B01o", "scope":"Full English II.1-II.2 and relevant English notes; B01n lossless restoration and mirror reconciliation", "source_records":37, "new_predictions":0, "tests":25, "test_scope":"Context-bound glossary/taxonomy retrieval, source attribution, unknown handling, scope and artifact integrity; no population or personal prediction.", "targeted_cross_source_comparisons":0})
d = json.loads((T / "SECTION_DISCOVERY.json").read_text())
assert d["read_sections_count"] == 48
for sec in coverage["sections"]:
    chapter = int(sec["chapter"].split(".")[1])
    row = next(x for x in d["sections"] if x["book"] == "II" and x["chapter"] == chapter)
    assert row["status"] == "INDEXED_NOT_READ"
    row.update(status="READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE", locator_status="ENGLISH_TEXT_AND_RELEVANT_NOTES_IMAGE_VERIFIED", rule_ids=sec["record_ids"], english_pdf_pages=sec["english_pdf_pages"], reading_receipt="batches/B01o/READING_RECEIPT.json", boundary=sec["boundary"])
for chapter in (3,4):
    row = next(x for x in d["sections"] if x["book"] == "II" and x["chapter"] == chapter)
    row["locator_status"] = "HEADING_LOCATED_ONLY_NOT_CHAPTER_READ"
d.update(read_sections_count=50, indexed_unread_count=11, body_locators_warning="Full English Books I/III/IV and II.1-II.2 read/extracted;11 BookII chapters remain. II.3 begins153 and continues through city-foundation paragraphs and note1 on185 before II.4; located only.")
assert sum(x["status"] == "READ_EXTRACTED_BOUNDED_ENGLISH_SCOPE" for x in d["sections"]) == 50
state_path = ROOT / "state/ASTROLOGY_SOURCE_AUDIT_CURRENT.md"
old = state_path.read_text()
preserved = old[old.index("## B01n source controls"):old.index("## Next reading")]
new = """# Current astrology source audit

**Parent OPEN. Full English Books I (24/24), III (14/14), IV (10/10), and II.1-II.2 are read/extracted.**50/61 Ptolemy sections and745 source records;11 BookII chapters and other sources remain. No personal forecasts, fitted-rule changes, or runtime promotion.

## Current recovery — completed work must not be repeated
- `tasks/astro-source-audit-multipass-20261005/CURRENT_PASS.json`, `PASS_PLAN.json` and `SECTION_DISCOVERY.json` are synchronized through B01o.
- Current `batches/B01o/REPORT.md`, `RULES.json`, `GENERAL_CONTEXT_TABLES.json`, reading/coverage receipts and `VERIFICATION.json` contain37 new records and25 bounded checks.
- `batches/B01o/B01n_RECOVERY_VERIFICATION.json` closes the previous access-limited recovery:21 archive members verified,19 missing ordinary files materialized hash-identically, both progress mirrors refreshed,559 cumulative source/reference and methodology checks freshly passed on the host.
- B01n source files are now directly inspectable beside the original lossless archive. Its old report and test receipt remain historical unchanged records; do not rerun its mirror script after this newer checkpoint.
- The final cumulative run is in B01o verification. The550 source-test inventory plus34 methodology checks must not be called the whole application suite or predictive validation.

## B01o source controls
II.1 preserves two independent organizing axes: whole countries/cities and greater-periodic/lesser-occasional circumstances. The city reading has a separately attributed variant; qualitative priority has no supplied numerical score. Regional familiarity and time-specific configurations are particularly considered, not a complete two-variable algorithm.

Robbins's local glossary distinguishes climes (latitude-defined regions), proper regions (examples: planetary domiciles in I.17 and terms), transits (zodiacal passage), parallels (north/south latitude), and angles (east/west position here). Do not substitute natal angles, declination aspects, or natal houses merely because a technical word matches.

II.2's six historical portraits remain attributed claims, not modern population/personality/clinical classifiers. Probable Posidonius dependence is editorial and unverified here. Named Egyptians/Chaldaeans and alternative explanations of frankness belong to Anonymous as reported by Robbins, not the unnamed main-text clause. Local situation/height/lowness/adjacency and plain/sea/soil examples qualify the broad framing. The explicit generally-but-not-every-individual clause supplies no measured prevalence or post-hoc exemption rule.

""" + preserved + """## Next reading
**B01p: full English II.3**, PDF153/printed129 through the city-foundation conclusion and note1 on PDF185/printed161. Stop before II.4 heading; note2 on185 belongs to II.4. Boundaries located only, complete chapter not read. Inspect tables visually and preserve original place names, layered rulerships, and source qualifications. No new upload is needed; no unattended work is claimed after delivery.
"""
assert preserved in new
for name, obj in [("CURRENT_PASS.json",current),("PASS_PLAN.json",plan),("SECTION_DISCOVERY.json",d)]:
    (T/name).write_text(json.dumps(obj,indent=2)+"\n")
state_path.write_text(new)
print("Progress advanced:50/61 sections,745 records; B01n restoration resolved; preserved prior source controls.")
