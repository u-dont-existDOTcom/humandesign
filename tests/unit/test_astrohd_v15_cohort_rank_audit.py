"""Cohort six-rule identity matrix with exact permutation and false-positive controls."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

TASK = Path(__file__).resolve().parents[2] / "tasks/astrohd-v15-structural-null-20261015"
sys.path.insert(0, str(TASK))
spec = importlib.util.spec_from_file_location("cohort_rank_audit", TASK / "cohort_rank_audit.py")
assert spec and spec.loader
cohort = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cohort)

DOMAIN_IDS = (
    "insight_translation",
    "retreat_privacy",
    "romantic_attachment",
    "persuasion_strategy",
    "recognition_entry",
)


def row(pid: str, *, supported: str | None, mask: int, consent: bool = True) -> dict:
    profile = {name: "unknown" for name in DOMAIN_IDS}
    if supported:
        profile[supported] = "supported"
    return {
        "pseudonym": pid,
        "consent_to_analysis": consent,
        "chart_known_to_question_coder": False,
        "neutral_profile": profile,
        "chart_six_bit_mask": mask,
    }


def test_matched_cohort_exact_permutation_beats_chart_only_baseline():
    data = [
        row("P1", supported="insight_translation", mask=1),
        row("P2", supported="retreat_privacy", mask=2),
        row("P3", supported="recognition_entry", mask=16),
    ]
    result = cohort.evaluate(data)
    assert result["score_matrix_rows_profile_columns_chart"] == [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    assert [r["rank_best"] for r in result["true_chart_ranks"]] == [1, 1, 1]
    assert result["group_null"]["method"] == "EXACT_ALL_N_FACTORIAL_LABEL_PERMUTATIONS"
    assert result["group_null"]["n_assignments_evaluated"] == 6
    assert result["group_null"]["one_sided_p_ge_observed_including_ties"] == pytest.approx(1 / 6)
    assert result["all_positive_chart_only_control"]["group_permutation_p"] == 1.0
    assert result["no_calibrated_probabilities_claimed"]


def test_known_model_full_signature_nonnegative_requires_structural_disclosure():
    data = [
        row("A", supported="insight_translation", mask=63),
        row("B", supported="insight_translation", mask=0),
    ]
    result = cohort.evaluate(data)
    assert result["true_chart_ranks"][0]["rank_best"] == 1
    assert result["true_chart_ranks"][0]["target_first_structurally_guaranteed"] is True
    assert result["true_chart_ranks"][1]["target_first_structurally_guaranteed"] is False


def test_missing_evidence_preserved_not_laundered_to_success():
    data = [
        row("A", supported="insight_translation", mask=1),
        row("B", supported=None, mask=2),
    ]
    result = cohort.evaluate(data)
    assert result["true_chart_ranks"][1]["status"] == "UNSCORABLE_NO_INFORMATION"
    assert result["true_chart_ranks"][1]["rank_best"] is None
    assert result["group_null"]["status"] == "NOT_CALCULATED_UNSCORABLE_PARTICIPANT_PRESERVED"


@pytest.mark.parametrize(
    "change,match",
    [
        ({"consent_to_analysis": False}, "consent"),
        ({"chart_known_to_question_coder": True}, "leaked"),
        ({"chart_six_bit_mask": 64}, "mask"),
        ({"chart_six_bit_mask": True}, "mask"),
        ({"pseudonym": "P1"}, "Repeated"),
        ({"birth_date": "SYNTHETIC"}, "five declared"),
    ],
)
def test_invalid_consent_leakage_mask_or_duplicate_id_fail_closed(change, match):
    data = [
        row("P1", supported="insight_translation", mask=1),
        row("P2", supported="retreat_privacy", mask=2),
    ]
    data[1].update(change)
    with pytest.raises(ValueError, match=match):
        cohort.evaluate(data)


def test_large_panel_uses_reproducible_seeded_null_not_unlabeled_exact_p():
    rows = [
        row(f"P{i}", supported=DOMAIN_IDS[i % len(DOMAIN_IDS)], mask=(1 << (i % 6)))
        for i in range(9)
    ]
    a = cohort.evaluate(rows)
    b = cohort.evaluate(rows)
    assert a["group_null"] == b["group_null"]
    assert a["group_null"]["method"] == "SEEDED_RANDOM_CHART_LABEL_PERMUTATION_MONTE_CARLO"
    assert a["group_null"]["n_assignments_evaluated"] == 20_000
    assert 0 < a["group_null"]["one_sided_p_ge_observed_including_ties"] <= 1


def test_insufficient_participant_count_is_rejected():
    with pytest.raises(ValueError, match="2 to 100"):
        cohort.evaluate([row("P1", supported="insight_translation", mask=1)])


def test_cli_private_cohort_fixture_and_permissions(tmp_path):
    import json
    import os
    import stat
    import subprocess
    import sys

    root = TASK.parents[1]
    input_path = tmp_path / "synthetic-pairs.json"
    output_path = tmp_path / "result.json"
    entries = [
        row("P1", supported="insight_translation", mask=1),
        row("P2", supported="retreat_privacy", mask=2),
        row("P3", supported="recognition_entry", mask=16),
    ]
    input_path.write_text(
        json.dumps(
            {
                "schema": "astrohd-v15-consenting-cohort-v1",
                "records": entries,
            }
        )
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(TASK / "cohort_rank_audit.py"),
            "--private-cohort-json",
            str(input_path),
            "--private-output-json",
            str(output_path),
        ],
        cwd=root,
        env={**os.environ, "PYTHONPATH": str(root / "src")},
        check=True,
        capture_output=True,
        text=True,
    )
    assert "private_report_written" in proc.stdout
    out = json.loads(output_path.read_text())
    assert out["group_null"]["one_sided_p_ge_observed_including_ties"] == pytest.approx(1 / 6)
    assert out["preexisting_prospective_freeze_receipts_verified_by_this_script"] is False
    assert stat.S_IMODE(output_path.stat().st_mode) == 0o600
