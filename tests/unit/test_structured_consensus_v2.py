from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from hdmatch.evaluation.automated_annotation_calibration import AutomatedCodingPassReceipt
from hdmatch.evaluation.structured_annotation_v2 import StructuredAnnotationResponseV2
from hdmatch.evaluation.structured_consensus_v2 import build_structured_consensus_v2
from hdmatch.evaluation.validated_automated_pass_v2 import (
    ValidatedStructuredAutomatedPassArtifactV2,
    ValidatedStructuredAutomatedPassPayloadV2,
)
from hdmatch.experiments.canonical import canonical_json_bytes, sha256_json

NOW = datetime(2026, 9, 4, 13, 20, tzinfo=UTC)


def _response(
    value: str | tuple[str, ...],
    *,
    relation: str = "single",
    note: str | None = None,
    context: tuple[str, ...] = (),
) -> StructuredAnnotationResponseV2:
    values = (value,) if isinstance(value, str) else value
    return StructuredAnnotationResponseV2(
        task_id="TASK-A",
        freeze_id="BPF-0123456789ABCDEF0123",
        freeze_sha256="0" * 64,
        ontology_artifact_id="LPO-0123456789ABCDEF0123",
        ontology_sha256="1" * 64,
        procedure_id="LPSP-0123456789ABCDEF0123",
        procedure_sha256="2" * 64,
        episode_id="EP-A",
        observable_id="OBS-A",
        state="observed",
        coded_values=values,
        value_relation=relation,  # type: ignore[arg-type]
        supporting_source_turn_ids=("TURN-A",),
        context_qualifiers=context,
        annotation_note=note,
    )


def _bytes(response: StructuredAnnotationResponseV2) -> bytes:
    return canonical_json_bytes(response) + b"\n"


def _validated(pass_id: str, data: bytes) -> ValidatedStructuredAutomatedPassArtifactV2:
    output_sha = hashlib.sha256(data).hexdigest()
    pass_receipt = AutomatedCodingPassReceipt(
        pass_id=pass_id,
        corpus_sha256="3" * 64,
        codebook_sha256="4" * 64,
        coding_procedure_sha256="2" * 64,
        prompt_sha256="5" * 64,
        model_identity="STRUCTURAL-MODEL",
        model_version="STRUCTURAL-VERSION",
        output_sha256=output_sha,
        created_at_utc=NOW,
    )
    payload = ValidatedStructuredAutomatedPassPayloadV2(
        automated_pass=pass_receipt,
        task_set_sha256="6" * 64,
        raw_output_sha256="7" * 64,
        normalized_output_sha256=output_sha,
        normalization_implementation_sha256="8" * 64,
        expected_unit_count=1,
        validated_unit_count=1,
        created_at_utc=NOW,
    )
    digest = sha256_json(payload)
    return ValidatedStructuredAutomatedPassArtifactV2(
        artifact_id=f"LPVP-{digest[:20].upper()}",
        artifact_sha256=digest,
        payload=payload,
    )


def _entry(pass_id: str, response: StructuredAnnotationResponseV2):
    data = _bytes(response)
    return (_validated(pass_id, data), data)


def test_two_of_three_identical_semantic_responses_form_majority() -> None:
    consensus = build_structured_consensus_v2(
        (
            _entry("PASS-1", _response("VALUE_A")),
            _entry("PASS-2", _response("VALUE_A", note="Different non-substantive note")),
            _entry("PASS-3", _response("VALUE_B")),
        )
    )
    unit = consensus.payload.units[0]
    assert unit.status == "majority"
    assert unit.agreeing_pass_ids == ("PASS-1", "PASS-2")
    assert unit.dissenting_pass_ids == ("PASS-3",)
    assert unit.consensus_response is not None
    assert unit.consensus_response.coded_values == ("VALUE_A",)
    assert unit.consensus_response.annotation_note is None
    assert consensus.payload.majority_units == 1


def test_unordered_multiple_and_set_like_metadata_are_semantically_normalized() -> None:
    consensus = build_structured_consensus_v2(
        (
            _entry(
                "PASS-1",
                _response(
                    ("VALUE_A", "VALUE_B"),
                    relation="unordered_multiple",
                    context=("CTX-B", "CTX-A"),
                ),
            ),
            _entry(
                "PASS-2",
                _response(
                    ("VALUE_B", "VALUE_A"),
                    relation="unordered_multiple",
                    context=("CTX-A", "CTX-B"),
                ),
            ),
            _entry(
                "PASS-3",
                _response(
                    ("VALUE_A", "VALUE_B"),
                    relation="unordered_multiple",
                    context=("CTX-A", "CTX-B"),
                ),
            ),
        )
    )
    unit = consensus.payload.units[0]
    assert unit.status == "unanimous"
    assert consensus.payload.unanimous_units == 1


def test_ordered_sequence_difference_is_not_erased() -> None:
    consensus = build_structured_consensus_v2(
        (
            _entry("PASS-1", _response(("VALUE_A", "VALUE_B"), relation="ordered_sequence")),
            _entry("PASS-2", _response(("VALUE_A", "VALUE_B"), relation="ordered_sequence")),
            _entry("PASS-3", _response(("VALUE_B", "VALUE_A"), relation="ordered_sequence")),
        )
    )
    assert consensus.payload.units[0].status == "majority"


def test_no_strict_majority_remains_unresolved() -> None:
    consensus = build_structured_consensus_v2(
        (
            _entry("PASS-1", _response("VALUE_A")),
            _entry("PASS-2", _response("VALUE_B")),
            _entry("PASS-3", _response("VALUE_C")),
        )
    )
    unit = consensus.payload.units[0]
    assert unit.status == "unresolved"
    assert unit.consensus_response is None
    assert unit.agreeing_pass_ids == ()
    assert unit.dissenting_pass_ids == ("PASS-1", "PASS-2", "PASS-3")
    assert consensus.payload.unresolved_units == 1
