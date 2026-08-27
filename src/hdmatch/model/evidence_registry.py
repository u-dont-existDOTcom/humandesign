"""Typed provenance registry for Mapping Library v2 candidate hypotheses."""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from hdmatch.model.rich_predicate import RichChartPredicate


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EvidenceClass(StrEnum):
    OFFICIAL_HD_PRIMARY = "official_hd_primary"
    INDEPENDENT_EMPIRICAL = "independent_empirical"
    HISTORICAL_SYSTEM_SOURCE = "historical_system_source"
    PARTICIPANT_DERIVED = "participant_derived"


class EmpiricalStatus(StrEnum):
    NO_INDEPENDENT_VALIDATION_RECORDED = "no_independent_validation_recorded"
    INDEPENDENT_SUPPORT_RECORDED = "independent_support_recorded"
    CONTRADICTORY_EVIDENCE_RECORDED = "contradictory_evidence_recorded"


class ConfirmatoryStatus(StrEnum):
    CANDIDATE_ONLY = "candidate_only"
    ELIGIBLE_FOR_FUTURE_FREEZE = "eligible_for_future_freeze"
    EXPLORATORY_ONLY = "exploratory_only"


class CandidateSource(_FrozenModel):
    class_: EvidenceClass
    publisher: str
    url: str
    source_claim_paraphrase: str


class CandidateClaim(_FrozenModel):
    candidate_id: str
    priority_basis: str
    predicate: RichChartPredicate
    source: CandidateSource
    construct: str
    proposed_observable: str
    question_design_notes: str
    empirical_status: EmpiricalStatus
    confirmatory_status: ConfirmatoryStatus


class EvidenceRegistry(_FrozenModel):
    schema_version: Literal["mapping-v2-candidate-claims-v1"]
    status: Literal["hypothesis_registry_not_scoring_library"]
    epistemic_note: str
    candidates: tuple[CandidateClaim, ...]

    @property
    def sha256(self) -> str:
        canonical = json.dumps(
            self.model_dump(mode="json", by_alias=True),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()


def load_evidence_registry(path: str | Path) -> EvidenceRegistry:
    source = Path(path)
    payload = json.loads(source.read_text(encoding="utf-8"))
    # JSON uses the natural key "class"; the model uses class_ because class is reserved.
    for candidate in payload.get("candidates", []):
        source_payload = candidate.get("source")
        if isinstance(source_payload, dict) and "class" in source_payload:
            source_payload["class_"] = source_payload.pop("class")
    return EvidenceRegistry.model_validate(payload)
