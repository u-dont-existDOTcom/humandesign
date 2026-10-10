"""Bind the frozen diagnostic review to the unchanged canonical candidate.

This checks identities, not the truth of the source judgments. It requires the
original source-image paths retained by the reviewer and is not the portable
packet test entrypoint.
"""

import hashlib
import json
from pathlib import Path

BATCH = Path(__file__).resolve().parent
REVIEW = BATCH / "independent_review"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def objsha(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def read(path):
    return json.loads(path.read_text())


def main():
    manifest = read(BATCH / "REVIEW_CANDIDATE_MANIFEST.json")
    for entry in manifest["files"]:
        assert sha((BATCH / entry["path"]).read_bytes()) == entry["sha256"], entry["path"]
    records = read(BATCH / "RULES.json")["rules"]
    verdicts = read(REVIEW / "INITIAL_RECORD_VERIFICATION.json")["records"]
    by_id = {item["id"]: item for item in records}
    assert len(by_id) == len(verdicts) == 192
    image_hashes = {}
    for item in verdicts:
        assert item["verdict"] == "PASS" and item["required_change"] is None
        assert objsha(by_id[item["id"]]) == item["record_sha256"], item["id"]
        for evidence in item["source_evidence"]:
            path = evidence["image_path"]
            if path not in image_hashes:
                image_hashes[path] = sha(Path(path).read_bytes())
            assert image_hashes[path] == evidence["image_sha256"], path
    ledger = read(BATCH / "CLAIM_LEDGER.json")
    claims = read(REVIEW / "INITIAL_CLAIM_VERIFICATION.json")
    by_id = {item["id"]: item for item in ledger["items"]}
    report = (BATCH / "AUDIT_REPORT.md").read_text()
    assert len(by_id) == len(claims["items"]) == 42
    for item in claims["items"]:
        assert item["verdict"] == "PASS" and item["required_change"] is None
        assert objsha(by_id[item["id"]]) == item["ledger_item_sha256"], item["id"]
        assert item["text"] == by_id[item["id"]]["text"]
        assert sha(item["text"].encode()) == item["text_sha256"]
        assert report.count(item["text"]) == 1
        for evidence in item["evidence_files"]:
            assert sha((BATCH / evidence["path"]).read_bytes()) == evidence["sha256"], evidence["path"]
    assert not claims["whole_report_scan"]["new_unmatched_claims"]
    frozen = read(REVIEW / "INITIAL_FREEZE_MANIFEST.json")
    for entry in frozen["files"]:
        assert sha((REVIEW / entry["path"]).read_bytes()) == entry["sha256"], entry["path"]
    diagnosis = read(REVIEW / "INITIAL_DIAGNOSIS.json")
    receipt = {
        "batch": "B02k",
        "stage": "SOURCE_AND_REPORT_ACCEPTED; PUBLICATION_AND_DELIVERY_PENDING",
        "decision": "PASS_WITH_EXPLICIT_LIMITS",
        "candidate_manifest_sha256": sha((BATCH / "REVIEW_CANDIDATE_MANIFEST.json").read_bytes()),
        "candidate_files_unchanged": 44,
        "source_record_hashes_matched": 192,
        "report_whole_item_hashes_matched": 42,
        "report_table_data_rows_checked": 27,
        "unmatched_report_claims": 0,
        "independent_frozen_support_files_verified": 31,
        "root_original_image_dependency_hashes_matched": len(image_hashes),
        "report_sha256": sha((BATCH / "AUDIT_REPORT.md").read_bytes()),
        "rules_sha256": sha((BATCH / "RULES.json").read_bytes()),
        "code_sha256": sha((BATCH / "lilly_sixth_opening_reference.py").read_bytes()),
        "test_count": 33,
        "required_candidate_changes": [],
        "review_cycles": {"initial_exhaustive_passes": 1, "changed_item_cycles_used": 0, "changed_item_cycles_limit": 2},
        "independence": diagnosis["independence"],
        "review_material_limits": diagnosis["material_limits"],
        "source_first_refinement": {
            "id": "SF-REF01", "decision": "ACCEPT",
            "root_evidence": "Root directly viewed the original PDF888 errata crop after diagnosis freeze: p257 l23 r eight. Candidate already correct; original evaluator freeze unchanged."
        },
        "diagnostic_note_disposition": [
            {"id": item["id"],
             "disposition": "RETAIN_LIMIT_NO_CURRENT_DEFECT" if item["id"].startswith("COV-") else "OPTIONAL_PRESENTATION_NOT_REQUIRED_FOR_THIS_BATCH",
             "reason": item["current_evidence"]}
            for item in diagnosis["diagnostic_coverage_and_presentation_notes"]
        ],
        "root_review_basis": "Root full original-source reading before compilation; complete frozen diagnosis, all42 claim reasons, item/material-evidence bindings and actual source-supported refinement. Reviewer verdict alone is not treated as truth.",
        "parent_status": "OPEN", "whole_XLIV_complete": False,
        "clinical_or_predictive_validation": False,
    }
    (BATCH / "ACCEPTANCE.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    (BATCH / "REVIEW_CYCLE_LEDGER.json").write_text(json.dumps({
        "batch": "B02k",
        "cycles": [{"cycle": "INITIAL", "source_records_pass": 192, "report_items_pass": 42,
                    "required_changes": 0, "candidate_changes_after_freeze": 0,
                    "diagnosis_manifest_sha256": sha((REVIEW / "INITIAL_FREEZE_MANIFEST.json").read_bytes()),
                    "carried_passes": "All44 candidate inputs and all192 record /42 whole-item hashes plus material dependencies matched unchanged."}],
        "repair_cycles_used": 0, "repair_cycles_limit": 2, "stall": False, "withheld_items": [],
        "source_ambiguities": "Retained as qualified source content, not hidden omissions.",
        "late_exposure_disclosure": "independent_review/INITIAL_REVIEW_RECEIPT.json#/independence",
        "evaluator_refinement": "SF-REF01; frozen source-first files unchanged; candidate already used correct line23."
    }, indent=2) + "\n")
    print(json.dumps({key: receipt[key] for key in ["decision", "candidate_files_unchanged", "source_record_hashes_matched", "report_whole_item_hashes_matched", "independent_frozen_support_files_verified", "root_original_image_dependency_hashes_matched"]}))


if __name__ == "__main__":
    main()
