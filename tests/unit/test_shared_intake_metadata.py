"""Private-file intake metadata tests using synthetic records only."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.participant.shared_intake_metadata import (
    SharedStudyIntakeMetadata,
    canonical_shared_intake_bytes,
    parse_shared_study_intake_metadata,
    write_shared_intake_metadata,
)

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate_shared_study_intake.py"


@pytest.fixture
def payload() -> dict:
    return {
        "participant_id_pseudonym": "P-SYNTHETIC-01",
        "study_id": "study-synthetic",
        "birth_input_sha256": "a" * 64,
        "collection_stage": "trusted_intake_before_interview",
        "recorded_at_utc": "2026-10-26T10:00:00+02:00",
        "source": "participant_self_report",
        "consent_to_pseudonymous_research_record": True,
        "selected_system_ids": ["study-arm-a", "study-arm-b"],
    }


def test_omission_stays_unknown_and_does_not_become_a_denial(payload: dict) -> None:
    record = SharedStudyIntakeMetadata.model_validate(payload)
    assert record.birth_quality.time_source == "unknown"
    assert record.birth_quality.stated_uncertainty_seconds is None
    assert record.birth_quality.reported_uncertainty_interval is None
    assert len(record.system_knowledge) == 2
    for knowledge in record.system_knowledge:
        assert knowledge.familiarity == "unknown"
        assert knowledge.own_profile_known == "unknown"
        assert knowledge.prior_personal_interpretation == "unknown"


@pytest.mark.parametrize("answer", ["yes", "no", "unsure", "prefer_not_to_say", "not_asked"])
def test_explicit_answers_remain_distinct(payload: dict, answer: str) -> None:
    payload["system_knowledge"] = [{
        "system_id": "study-arm-a", "own_profile_known": answer,
        "prior_personal_interpretation": answer,
    }]
    record = SharedStudyIntakeMetadata.model_validate(payload)
    assert record.system_knowledge[0].own_profile_known == answer
    assert record.system_knowledge[0].prior_personal_interpretation == answer
    assert record.system_knowledge[1].own_profile_known == "unknown"


def test_system_outside_selected_study_is_rejected(payload: dict) -> None:
    payload["system_knowledge"] = [{"system_id": "unselected-arm", "own_profile_known": "no"}]
    with pytest.raises(ValidationError, match="outside this study selection"):
        SharedStudyIntakeMetadata.model_validate(payload)


@pytest.mark.parametrize("where", ["selection", "answers"])
def test_duplicate_systems_are_rejected(payload: dict, where: str) -> None:
    if where == "selection":
        payload["selected_system_ids"] = ["study-arm-a", "study-arm-a"]
    else:
        payload["system_knowledge"] = [
            {"system_id": "study-arm-a"}, {"system_id": "study-arm-a"},
        ]
    with pytest.raises(ValidationError, match="duplicate"):
        SharedStudyIntakeMetadata.model_validate(payload)


@pytest.mark.parametrize("bad", [-1, "120", True, float("inf"), float("nan")])
def test_invalid_or_coerced_uncertainty_is_rejected(payload: dict, bad: object) -> None:
    payload["birth_quality"] = {"stated_uncertainty_seconds": bad}
    with pytest.raises(ValidationError):
        SharedStudyIntakeMetadata.model_validate(payload)


def test_reported_precision_and_asymmetric_interval_are_preserved(payload: dict) -> None:
    payload["birth_quality"] = {
        "time_source": "family_record",
        "stated_uncertainty_seconds": 90,
        "reported_uncertainty_interval": {
            "lower_offset_seconds": -30, "upper_offset_seconds": 90,
            "source": "source_record",
        },
    }
    record = SharedStudyIntakeMetadata.model_validate(payload)
    assert record.birth_quality.stated_uncertainty_seconds == 90
    assert record.birth_quality.reported_uncertainty_interval.lower_offset_seconds == -30
    assert record.birth_quality.reported_uncertainty_interval.upper_offset_seconds == 90
    only_precision = deepcopy(payload)
    del only_precision["birth_quality"]["reported_uncertainty_interval"]
    assert SharedStudyIntakeMetadata.model_validate(
        only_precision
    ).birth_quality.reported_uncertainty_interval is None


def test_reverse_uncertainty_bounds_are_rejected(payload: dict) -> None:
    payload["birth_quality"] = {"reported_uncertainty_interval": {
        "lower_offset_seconds": 60, "upper_offset_seconds": -60,
        "source": "participant_statement",
    }}
    with pytest.raises(ValidationError, match="ordered"):
        SharedStudyIntakeMetadata.model_validate(payload)


@pytest.mark.parametrize("bad", [False, "true", 1, None])
def test_consent_is_required_and_never_coerced(payload: dict, bad: object) -> None:
    payload["consent_to_pseudonymous_research_record"] = bad
    with pytest.raises(ValidationError):
        SharedStudyIntakeMetadata.model_validate(payload)


def test_missing_consent_is_not_fabricated(payload: dict) -> None:
    del payload["consent_to_pseudonymous_research_record"]
    with pytest.raises(ValidationError):
        SharedStudyIntakeMetadata.model_validate(payload)


def test_after_freeze_requires_link_without_modifying_linked_record(payload: dict) -> None:
    payload["collection_stage"] = "separate_post_freeze"
    with pytest.raises(ValidationError, match="frozen primary"):
        SharedStudyIntakeMetadata.model_validate(payload)
    payload["primary_record_sha256"] = "b" * 64
    record = SharedStudyIntakeMetadata.model_validate(payload)
    assert record.primary_record_sha256 == "b" * 64
    payload["collection_stage"] = "trusted_intake_before_interview"
    with pytest.raises(ValidationError, match="cannot claim"):
        SharedStudyIntakeMetadata.model_validate(payload)


@pytest.mark.parametrize("bad", ["2026-10-26T08:00:00", 1793000000, None])
def test_recording_timestamp_requires_explicit_timezone(payload: dict, bad: object) -> None:
    payload["recorded_at_utc"] = bad
    with pytest.raises(ValidationError):
        SharedStudyIntakeMetadata.model_validate(payload)


@pytest.mark.parametrize("field", ["birth", "local_datetime", "full_name", "email", "chart"])
def test_birth_identity_and_target_fields_are_forbidden(payload: dict, field: str) -> None:
    payload[field] = "DO-NOT-ECHO-PRIVATE-VALUE"
    with pytest.raises(ValidationError):
        SharedStudyIntakeMetadata.model_validate(payload)


def test_nested_profile_value_is_forbidden(payload: dict) -> None:
    payload["system_knowledge"] = [{"system_id": "study-arm-a", "profile_value": "hidden"}]
    with pytest.raises(ValidationError):
        SharedStudyIntakeMetadata.model_validate(payload)


def test_canonical_output_is_stable_and_utc(payload: dict) -> None:
    first = parse_shared_study_intake_metadata(json.dumps(payload))
    canonical = canonical_shared_intake_bytes(first)
    second = parse_shared_study_intake_metadata(canonical)
    assert canonical_shared_intake_bytes(second) == canonical
    assert b'"recorded_at_utc":"2026-10-26T08:00:00Z"' in canonical
    assert not canonical.endswith(b"\n")
    assert json.loads(canonical)["system_knowledge"][1]["familiarity"] == "unknown"


@pytest.mark.parametrize("raw", [
    '{"consent_to_pseudonymous_research_record":false,"consent_to_pseudonymous_research_record":true}',
    '{"birth_quality":{"stated_uncertainty_seconds":NaN}}',
    "[]",
])
def test_strict_json_rejects_ambiguous_or_nonfinite_input(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_shared_study_intake_metadata(raw)


def test_private_write_is_append_only(payload: dict, tmp_path: Path) -> None:
    record = SharedStudyIntakeMetadata.model_validate(payload)
    target = tmp_path / "metadata.json"
    write_shared_intake_metadata(target, record)
    frozen = target.read_bytes()
    with pytest.raises(FileExistsError):
        write_shared_intake_metadata(target, record)
    assert target.read_bytes() == frozen
    if os.name == "posix":
        assert stat.S_IMODE(target.stat().st_mode) == 0o600


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False, capture_output=True, text=True, env=env, timeout=20,
    )


def test_cli_validates_and_writes_without_modifying_input(payload: dict, tmp_path: Path) -> None:
    source = tmp_path / "input.json"
    target = tmp_path / "output.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    original = source.read_bytes()
    validate = run_cli(str(source))
    assert validate.returncode == 0, validate.stderr
    assert json.loads(validate.stdout)["written"] is False
    assert not target.exists()
    result = run_cli(str(source), "--output", str(target))
    assert result.returncode == 0, result.stderr
    assert source.read_bytes() == original
    assert json.loads(result.stdout)["canonical_sha256"] == sha256(target.read_bytes()).hexdigest()
    retry = run_cli(str(source), "--output", str(target))
    assert retry.returncode == 2
    assert target.read_bytes() == canonical_shared_intake_bytes(
        SharedStudyIntakeMetadata.model_validate(payload)
    )


def test_cli_errors_do_not_echo_private_values(payload: dict, tmp_path: Path) -> None:
    source = tmp_path / "invalid.json"
    payload["full_name"] = "DO-NOT-ECHO-PRIVATE-VALUE"
    source.write_text(json.dumps(payload), encoding="utf-8")
    result = run_cli(str(source))
    assert result.returncode == 2
    assert "DO-NOT-ECHO-PRIVATE-VALUE" not in result.stdout + result.stderr
    assert payload["participant_id_pseudonym"] not in result.stdout + result.stderr
    assert json.loads(result.stderr)["issues"][0]["field"] == "full_name"


def test_blank_template_cannot_pass_as_a_consented_record() -> None:
    template = ROOT / "reference/forward_blind/shared_study_intake_metadata_template_v1.json"
    with pytest.raises(ValidationError):
        parse_shared_study_intake_metadata(template.read_bytes())
