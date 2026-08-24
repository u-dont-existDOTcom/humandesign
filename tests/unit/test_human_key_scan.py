from __future__ import annotations

from pathlib import Path

import pytest

from hdmatch.experiments.canonical import canonical_json_bytes, write_new_canonical_json
from hdmatch.human.workflow import (
    _ANSWER_KEY_SCAN_MAX_BYTES,
    _assert_no_human_answer_keys,
)


def _answer_key_payload() -> dict[str, object]:
    return {
        "schema_version": "human-cohort-answer-key-v1",
        "cohort": "validation",
        "protocol_sha256": "a" * 64,
        "blind_input_sha256": "b" * 64,
        "true_candidate_ids": {"P-001": "candidate-7"},
    }


@pytest.mark.parametrize(
    "filename",
    (
        "HUMAN-ANSWER-KEY.JSON",
        "renamed.payload",
        "cohort-key.Txt.BAK",
    ),
)
def test_answer_key_scan_detects_renamed_and_case_varied_text_files(
    tmp_path: Path,
    filename: str,
) -> None:
    write_new_canonical_json(tmp_path / filename, _answer_key_payload())

    with pytest.raises(RuntimeError, match="1 plaintext human answer key file"):
        _assert_no_human_answer_keys(tmp_path)


def test_answer_key_scan_detects_obvious_schema_less_nested_key_structure(
    tmp_path: Path,
) -> None:
    payload = _answer_key_payload()
    payload.pop("schema_version")
    write_new_canonical_json(tmp_path / "unlabeled.data", {"archive": payload})

    with pytest.raises(RuntimeError, match="1 plaintext human answer key file"):
        _assert_no_human_answer_keys(tmp_path)


def test_answer_key_scan_ignores_non_key_json_and_binary_marker_text(tmp_path: Path) -> None:
    write_new_canonical_json(
        tmp_path / "not-a-key.json",
        {
            "protocol_sha256": "a" * 64,
            "true_candidate_ids": {"example": "not sufficient without cohort binding"},
        },
    )
    (tmp_path / "binary.data").write_bytes(
        b"\x89PNG\x00human-cohort-answer-key-v1\x00true_candidate_ids"
    )
    (tmp_path / "source-example.txt").write_text(
        'The literal "human-cohort-answer-key-v1" is documentation, not JSON.',
        encoding="utf-8",
    )

    _assert_no_human_answer_keys(tmp_path)


def test_answer_key_scan_skips_metadata_caches_virtualenvs_and_large_files(
    tmp_path: Path,
) -> None:
    for directory_name in (".git", ".pytest_cache", ".VENV", "node_modules"):
        directory = tmp_path / directory_name
        directory.mkdir()
        write_new_canonical_json(directory / "hidden-key.data", _answer_key_payload())

    custom_environment = tmp_path / "python-environment"
    custom_environment.mkdir()
    (custom_environment / "pyvenv.cfg").write_text("home = /example\n", encoding="utf-8")
    write_new_canonical_json(custom_environment / "hidden-key.data", _answer_key_payload())

    large_payload = _answer_key_payload()
    large_payload["padding"] = "x" * _ANSWER_KEY_SCAN_MAX_BYTES
    large_bytes = canonical_json_bytes(large_payload)
    assert len(large_bytes) > _ANSWER_KEY_SCAN_MAX_BYTES
    (tmp_path / "large-key.data").write_bytes(large_bytes)

    _assert_no_human_answer_keys(tmp_path)
