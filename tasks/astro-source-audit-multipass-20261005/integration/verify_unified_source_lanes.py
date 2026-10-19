#!/usr/bin/env python3
"""Verify exact independent Western/Chinese historical source merge snapshot.

This check reads Git objects at a pinned merge commit, so later rightful
source-count increases do not invalidate historical acceptance tests.
"""

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FILE = HERE / "CROSS_LANE_MERGE_RECEIPT_20261019.json"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def verify():
    receipt = json.loads(FILE.read_text(encoding="utf-8"))
    merge = receipt["merge_commit"]
    parents = git("rev-list", "--parents", "-n", "1", merge).decode().strip().split()
    assert len(parents) == 3 and parents[0] == merge
    assert parents[1] == receipt["Chinese_V7_source_parent"]
    assert parents[2] == receipt["Lilly_B07am_source_parent"]
    for path, expected in receipt["source_file_sha256_at_merge"].items():
        original = git("show", f"{merge}:{path}")
        assert hashlib.sha256(original).hexdigest() == expected, (path, expected)
    west = json.loads(
        git(
            "show",
            f"{merge}:tasks/astro-source-audit-multipass-20261005/LILLY_SOURCE_EXTRACTION_INDEX_V1.json",
        )
    )
    china = json.loads(
        git(
            "show",
            f"{merge}:tasks/astro-chinese-primary-sources-20261017/CHINESE_SOURCE_AUDIT_INDEX_V7.json",
        )
    )
    assert west["records_count"] == 12625
    assert west["batches"][-1]["id"] == "B07am"
    assert west["next"]["pdf_page"] == 755
    assert west["next"]["chapter"] == "CLXVII"
    assert china["sum_source_annotations"] == 355
    assert [s["accepted_source_annotations"] for s in china["systems"]] == [154, 201]
    assert china["systems"][0]["next_id"] == "BZI-R0155"
    assert china["systems"][1]["next_id"] == "ZWD-R0202"
    assert receipt["western_historical_Lilly"] == 12625
    assert receipt["western_historical_Ptolemy"] == 1066
    assert receipt["western_historical_total"] == 13691
    assert receipt["chinese_historical_total"] == 355
    assert west["empirical_validations"] == west["runtime_promotions"] == 0
    assert china["independently_validated_real_human_claims"] == china["runtime_promotions"] == 0
    assert receipt["actual_human_outcome_predictions_validated"] == 0
    assert receipt["runtime_astrology_model_promotions"] == 0
    assert receipt["all_original_historical_source_index_files_unchanged_in_merge"]
    assert receipt["root_owner_outcome_status"] == "OPEN"
    print(
        json.dumps(
            {
                "merge_sha": merge,
                "provenance_files": len(receipt["source_file_sha256_at_merge"]),
                "lilly": west["records_count"],
                "ptolemy": 1066,
                "western": receipt["western_historical_total"],
                "chinese": china["sum_source_annotations"],
                "source_both_parent_edges_verified": True,
                "human_predictions_validated": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    verify()
