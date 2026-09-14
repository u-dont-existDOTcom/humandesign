"""Frozen open-world Life Patterns records with participant-adjudicated patterns.

This is the v2 participant-adjudicated path.  It deliberately lives beside the historical
fixed-codebook implementations: episode facts remain open text, while person-level recurrence
can enter an adapter projection only through a participant-accepted resolved pattern.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hdmatch.experiments.canonical import (
    canonical_json_bytes,
    load_json_bytes,
    sha256_json,
    write_new_bytes,
)

SHA256_PATTERN = r"^[0-9a-f]{64}$"
CONTRACT_SCHEMA_VERSION: Literal[
    "life-patterns-participant-adjudicated-neutral-contract-v2-candidate"
] = "life-patterns-participant-adjudicated-neutral-contract-v2-candidate"

EpisodeFactAssertionType = Literal[
    "positive_occurrence",
    "reported_appraisal_or_belief",
    "reported_outcome_or_resolution",
    "context",
    "temporal_relation",
    "admitted_absence",
]
AbsenceGateStatus = Literal["established", "not_established", "unclear"]
AbsenceEvidenceBasis = Literal["explicit_report_or_observation", "silence_or_missingness"]
AcquisitionPhase = Literal[
    "pre_first_proposal",
    "post_first_proposal",
    "timing_unclear",
]
PatternEvidenceRole = Literal[
    "preproposal_anchor",
    "preproposal_counterexample",
    "postproposal_scope_example",
    "postproposal_counterexample",
    "participant_added_exception",
]
ParticipantAdjudicationDecision = Literal["accept", "revise", "reject", "unresolved"]
ResolvedPatternStatus = Literal["accepted", "rejected", "unresolved"]
AdapterOperationKind = Literal["inspect", "aggregate", "count", "cluster", "score", "summarize"]
AdapterSemanticLevel = Literal["episode_fact", "person_level_pattern"]


class LifePatternsV2ValidationError(ValueError):
    """The record, freeze, projection, or adapter request violates the frozen v2 contract."""

    def __init__(self, findings: tuple[str, ...]) -> None:
        self.findings = findings
        super().__init__("; ".join(findings))


class LifePatternsV2Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, allow_inf_nan=False)


class SourceProvenanceV2(LifePatternsV2Model):
    source_provenance_id: str = Field(min_length=1)
    source_record_id: str = Field(min_length=1)
    locator: str = Field(min_length=1)
    content_sha256: str = Field(pattern=SHA256_PATTERN)
    exact_text_available: bool


class FactQualificationV2(LifePatternsV2Model):
    qualification_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)


class EpisodeUncertaintyNoteV2(LifePatternsV2Model):
    note_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)
    affects_fact_ids: tuple[str, ...] = ()


class EpisodeV2(LifePatternsV2Model):
    episode_id: str = Field(min_length=1)
    neutral_summary: str = Field(min_length=1)
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)
    fact_ids: tuple[str, ...] = Field(min_length=1)
    uncertainty_notes: tuple[EpisodeUncertaintyNoteV2, ...] = ()


class AbsenceAssessmentV2(LifePatternsV2Model):
    absence_assessment_id: str = Field(min_length=1)
    episode_id: str = Field(min_length=1)
    actor: str = Field(min_length=1)
    absent_proposition: str = Field(min_length=1)
    window_or_opportunity: str = Field(min_length=1)
    awareness: AbsenceGateStatus
    opportunity: AbsenceGateStatus
    reasonable_feasibility: AbsenceGateStatus
    established_nonoccurrence: AbsenceGateStatus
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)
    evidence_basis: AbsenceEvidenceBasis

    @model_validator(mode="after")
    def silence_is_not_nonoccurrence(self) -> Self:
        if (
            self.evidence_basis == "silence_or_missingness"
            and self.established_nonoccurrence == "established"
        ):
            raise ValueError("silence or missingness cannot establish nonoccurrence")
        return self

    @property
    def is_admitted(self) -> bool:
        return all(
            value == "established"
            for value in (
                self.awareness,
                self.opportunity,
                self.reasonable_feasibility,
                self.established_nonoccurrence,
            )
        )


class EpisodeFactV2(LifePatternsV2Model):
    fact_id: str = Field(min_length=1)
    fact_lineage_id: str = Field(min_length=1)
    revision_index: int = Field(ge=0)
    episode_id: str = Field(min_length=1)
    assertion_type: EpisodeFactAssertionType
    actor: str = Field(min_length=1)
    proposition: str = Field(min_length=1)
    source_provenance_ids: tuple[str, ...] = Field(min_length=1)
    qualification: FactQualificationV2 | None = None
    temporal_relation_provenance_ids: tuple[str, ...] = ()
    absence_assessment_id: str | None = None
    supersedes_fact_id: str | None = None
    participant_correction_provenance_ids: tuple[str, ...] = ()

    @model_validator(mode="after")
    def local_fact_contract_is_coherent(self) -> Self:
        if self.revision_index == 0 and (
            self.supersedes_fact_id is not None or self.participant_correction_provenance_ids
        ):
            raise ValueError("initial fact revision cannot be a participant correction")
        if self.revision_index > 0 and (
            self.supersedes_fact_id is None or not self.participant_correction_provenance_ids
        ):
            raise ValueError(
                "participant fact correction requires predecessor and exact correction provenance"
            )
        if self.assertion_type == "admitted_absence" and self.absence_assessment_id is None:
            raise ValueError("admitted absence fact requires an absence assessment")
        if self.assertion_type != "admitted_absence" and self.absence_assessment_id is not None:
            raise ValueError("only admitted absence facts may reference an absence assessment")
        if self.assertion_type == "temporal_relation" and not (
            self.temporal_relation_provenance_ids
        ):
            raise ValueError("temporal relation requires explicit source support")
        if self.assertion_type != "temporal_relation" and self.temporal_relation_provenance_ids:
            raise ValueError("only temporal relations may carry temporal-relation provenance")
        return self


class PatternProposalV2(LifePatternsV2Model):
    proposal_id: str = Field(min_length=1)
    pattern_thread_id: str = Field(min_length=1)
    revision_index: int = Field(ge=0)
    proposition: str = Field(min_length=1)
    question_text: str = Field(min_length=1)
    evidence_link_ids: tuple[str, ...] = Field(min_length=1)
    grounding_evidence_link_ids: tuple[str, ...] = Field(min_length=1)
    previous_proposal_id: str | None = None

    @model_validator(mode="after")
    def local_proposal_contract_is_coherent(self) -> Self:
        if not set(self.grounding_evidence_link_ids).issubset(self.evidence_link_ids):
            raise ValueError("proposal grounding links must be a subset of its evidence links")
        if self.revision_index == 0 and self.previous_proposal_id is not None:
            raise ValueError("first proposal cannot reference a previous proposal")
        if self.revision_index > 0 and self.previous_proposal_id is None:
            raise ValueError("revised proposal requires its immediate predecessor")
        return self


class PatternEvidenceLinkV2(LifePatternsV2Model):
    evidence_link_id: str = Field(min_length=1)
    proposal_id: str = Field(min_length=1)
    episode_id: str = Field(min_length=1)
    fact_ids: tuple[str, ...] = Field(min_length=1)
    role: PatternEvidenceRole
    acquisition_phase: AcquisitionPhase

    @model_validator(mode="after")
    def phase_cannot_be_promoted_by_role(self) -> Self:
        if self.role.startswith("preproposal_") and self.acquisition_phase != (
            "pre_first_proposal"
        ):
            raise ValueError("only pre-first-proposal evidence can have a preproposal role")
        if self.role.startswith("postproposal_") and self.acquisition_phase == (
            "pre_first_proposal"
        ):
            raise ValueError("pre-first-proposal evidence cannot have a postproposal role")
        return self


class ParticipantAdjudicationV2(LifePatternsV2Model):
    adjudication_id: str = Field(min_length=1)
    proposal_id: str = Field(min_length=1)
    decision: ParticipantAdjudicationDecision
    participant_response_provenance_ids: tuple[str, ...] = Field(min_length=1)
    participant_approved_wording: str | None = None
    scope_note: str | None = None
    exception_note: str | None = None
    counterexample_evidence_link_ids: tuple[str, ...] = ()
    retrieval_discrepancy_note: str | None = None

    @model_validator(mode="after")
    def participant_wording_is_present_when_required(self) -> Self:
        if (
            self.decision in {"accept", "revise"}
            and not (self.participant_approved_wording or "").strip()
        ):
            raise ValueError("accept and revise require participant-approved wording")
        return self


class ResolvedPatternV2(LifePatternsV2Model):
    pattern_thread_id: str = Field(min_length=1)
    status: ResolvedPatternStatus
    terminal_proposal_id: str = Field(min_length=1)
    supporting_preproposal_evidence_link_ids: tuple[str, ...]
    participant_response_provenance_ids: tuple[str, ...]
    participant_approved_wording: str | None = None
    scope_note: str | None = None
    exception_note: str | None = None


class SemanticCallbackProvenanceV2(LifePatternsV2Model):
    validator_id: str = Field(min_length=1)
    validator_version: str = Field(min_length=1)
    validator_sha256: str = Field(pattern=SHA256_PATTERN)
    target_theory_blind: Literal[True] = True


NonoccurrenceCallback = Callable[[EpisodeFactV2], bool]
GroundingCallback = Callable[
    [PatternProposalV2, PatternEvidenceLinkV2, tuple[EpisodeFactV2, ...]], bool
]


@dataclass(frozen=True)
class TheoryBlindSemanticCallbacksV2:
    """Required semantic checks whose decisions cannot be inferred from structural labels."""

    provenance: SemanticCallbackProvenanceV2
    asserts_real_world_nonoccurrence: NonoccurrenceCallback
    grounding_supports_current_proposition: GroundingCallback


class FactSemanticDecisionV2(LifePatternsV2Model):
    fact_id: str = Field(min_length=1)
    asserts_real_world_nonoccurrence: bool


class GroundingSemanticDecisionV2(LifePatternsV2Model):
    proposal_id: str = Field(min_length=1)
    evidence_link_id: str = Field(min_length=1)
    supports_current_proposition: bool


class SemanticValidationReceiptV2(LifePatternsV2Model):
    callback_provenance: SemanticCallbackProvenanceV2
    fact_decisions: tuple[FactSemanticDecisionV2, ...]
    grounding_decisions: tuple[GroundingSemanticDecisionV2, ...]


class LifePatternsRecordV2(LifePatternsV2Model):
    schema_version: Literal["life-patterns-participant-adjudicated-record-v2"] = (
        "life-patterns-participant-adjudicated-record-v2"
    )
    contract_schema_version: Literal[
        "life-patterns-participant-adjudicated-neutral-contract-v2-candidate"
    ] = CONTRACT_SCHEMA_VERSION
    contract_sha256: str = Field(pattern=SHA256_PATTERN)
    source_archive_sha256: str = Field(pattern=SHA256_PATTERN)
    source_provenance: tuple[SourceProvenanceV2, ...]
    episodes: tuple[EpisodeV2, ...]
    episode_facts: tuple[EpisodeFactV2, ...]
    absence_assessments: tuple[AbsenceAssessmentV2, ...] = ()
    pattern_proposals: tuple[PatternProposalV2, ...] = ()
    pattern_evidence_links: tuple[PatternEvidenceLinkV2, ...] = ()
    participant_adjudications: tuple[ParticipantAdjudicationV2, ...] = ()


class LifePatternsFreezePayloadV2(LifePatternsV2Model):
    schema_version: Literal["life-patterns-participant-adjudicated-freeze-payload-v2"] = (
        "life-patterns-participant-adjudicated-freeze-payload-v2"
    )
    contract_schema_version: Literal[
        "life-patterns-participant-adjudicated-neutral-contract-v2-candidate"
    ] = CONTRACT_SCHEMA_VERSION
    contract_sha256: str = Field(pattern=SHA256_PATTERN)
    source_archive_sha256: str = Field(pattern=SHA256_PATTERN)
    source_provenance: tuple[SourceProvenanceV2, ...]
    episodes: tuple[EpisodeV2, ...]
    episode_facts: tuple[EpisodeFactV2, ...]
    absence_assessments: tuple[AbsenceAssessmentV2, ...]
    pattern_proposals: tuple[PatternProposalV2, ...]
    pattern_evidence_links: tuple[PatternEvidenceLinkV2, ...]
    participant_adjudications: tuple[ParticipantAdjudicationV2, ...]
    resolved_patterns: tuple[ResolvedPatternV2, ...]
    semantic_validation: SemanticValidationReceiptV2


class LifePatternsFreezeEnvelopeV2(LifePatternsV2Model):
    schema_version: Literal["life-patterns-participant-adjudicated-freeze-v2"] = (
        "life-patterns-participant-adjudicated-freeze-v2"
    )
    payload: LifePatternsFreezePayloadV2
    freeze_payload_sha256: str = Field(pattern=SHA256_PATTERN)


class ProjectedEpisodeFactV2(LifePatternsV2Model):
    semantic_level: Literal["episode_only"] = "episode_only"
    fact: EpisodeFactV2


class ProjectedResolvedPatternV2(LifePatternsV2Model):
    semantic_level: Literal["participant_adjudicated_person_level_pattern"] = (
        "participant_adjudicated_person_level_pattern"
    )
    pattern: ResolvedPatternV2


class AdapterProjectionV2(LifePatternsV2Model):
    schema_version: Literal["life-patterns-participant-adjudicated-adapter-projection-v2"] = (
        "life-patterns-participant-adjudicated-adapter-projection-v2"
    )
    freeze_payload_sha256: str = Field(pattern=SHA256_PATTERN)
    contract_schema_version: Literal[
        "life-patterns-participant-adjudicated-neutral-contract-v2-candidate"
    ] = CONTRACT_SCHEMA_VERSION
    contract_sha256: str = Field(pattern=SHA256_PATTERN)
    source_archive_sha256: str = Field(pattern=SHA256_PATTERN)
    semantic_validation_provenance: SemanticCallbackProvenanceV2
    source_provenance: tuple[SourceProvenanceV2, ...]
    episode_facts: tuple[ProjectedEpisodeFactV2, ...]
    admitted_absence_assessments: tuple[AbsenceAssessmentV2, ...]
    accepted_patterns: tuple[ProjectedResolvedPatternV2, ...]
    operative_evidence_links: tuple[PatternEvidenceLinkV2, ...]


class AdapterOperationV2(LifePatternsV2Model):
    operation: AdapterOperationKind
    output_semantic_level: AdapterSemanticLevel
    episode_fact_ids: tuple[str, ...] = ()
    resolved_pattern_thread_ids: tuple[str, ...] = ()

    @model_validator(mode="after")
    def person_level_claims_use_only_resolved_patterns(self) -> Self:
        if self.output_semantic_level == "person_level_pattern":
            if self.episode_fact_ids:
                raise ValueError(
                    "episode facts cannot be aggregated into a person-level pattern claim"
                )
            if not self.resolved_pattern_thread_ids:
                raise ValueError(
                    "person-level pattern operation requires an accepted resolved pattern"
                )
        elif self.resolved_pattern_thread_ids:
            raise ValueError(
                "episode-level operation cannot relabel a resolved person-level pattern"
            )
        return self


class UnmeasuredNotRepresentedV2(LifePatternsV2Model):
    status: Literal["unmeasured/not_represented"] = "unmeasured/not_represented"
    distinction: str = Field(min_length=1)
    source_reread_permitted: Literal[False] = False


def _duplicates(values: tuple[str, ...]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)
    return duplicates


def _append_duplicate_errors(
    errors: list[str], *, label: str, identifiers: tuple[str, ...]
) -> None:
    for duplicate in sorted(_duplicates(identifiers)):
        errors.append(f"duplicate {label}: {duplicate}")


def _structure_errors(record: LifePatternsRecordV2) -> tuple[str, ...]:
    errors: list[str] = []
    _append_duplicate_errors(
        errors,
        label="source provenance id",
        identifiers=tuple(row.source_provenance_id for row in record.source_provenance),
    )
    _append_duplicate_errors(
        errors,
        label="episode id",
        identifiers=tuple(row.episode_id for row in record.episodes),
    )
    _append_duplicate_errors(
        errors,
        label="fact id",
        identifiers=tuple(row.fact_id for row in record.episode_facts),
    )
    _append_duplicate_errors(
        errors,
        label="absence assessment id",
        identifiers=tuple(row.absence_assessment_id for row in record.absence_assessments),
    )
    _append_duplicate_errors(
        errors,
        label="proposal id",
        identifiers=tuple(row.proposal_id for row in record.pattern_proposals),
    )
    _append_duplicate_errors(
        errors,
        label="evidence link id",
        identifiers=tuple(row.evidence_link_id for row in record.pattern_evidence_links),
    )
    _append_duplicate_errors(
        errors,
        label="adjudication id",
        identifiers=tuple(row.adjudication_id for row in record.participant_adjudications),
    )

    provenance = {row.source_provenance_id: row for row in record.source_provenance}
    episodes = {row.episode_id: row for row in record.episodes}
    facts = {row.fact_id: row for row in record.episode_facts}
    assessments = {row.absence_assessment_id: row for row in record.absence_assessments}
    proposals = {row.proposal_id: row for row in record.pattern_proposals}
    evidence_links = {row.evidence_link_id: row for row in record.pattern_evidence_links}
    adjudications = {row.proposal_id: row for row in record.participant_adjudications}

    def require_provenance(references: tuple[str, ...], owner: str) -> None:
        missing = sorted(set(references) - set(provenance))
        if missing:
            errors.append(f"{owner} references unknown source provenance: {','.join(missing)}")

    for episode in record.episodes:
        require_provenance(episode.source_provenance_ids, f"episode {episode.episode_id}")
        if len(episode.fact_ids) != len(set(episode.fact_ids)):
            errors.append(f"episode {episode.episode_id} repeats a fact id")
        for fact_id in episode.fact_ids:
            fact = facts.get(fact_id)
            if fact is None:
                errors.append(f"episode {episode.episode_id} references unknown fact {fact_id}")
            elif fact.episode_id != episode.episode_id:
                errors.append(f"episode {episode.episode_id} references fact from another episode")
        for note in episode.uncertainty_notes:
            require_provenance(
                note.source_provenance_ids,
                f"episode uncertainty note {note.note_id}",
            )
            for fact_id in note.affects_fact_ids:
                fact = facts.get(fact_id)
                if fact is None or fact.episode_id != episode.episode_id:
                    errors.append(
                        f"episode uncertainty note {note.note_id} references an invalid fact"
                    )
                elif fact.qualification is None:
                    errors.append(
                        f"episode-only uncertainty note {note.note_id} is insufficient for fact "
                        f"{fact_id}"
                    )
                elif fact.qualification.text != note.text or not set(
                    note.source_provenance_ids
                ).issubset(fact.qualification.source_provenance_ids):
                    errors.append(
                        f"fact {fact_id} does not preserve its source-bound uncertainty exactly"
                    )

    for assessment in record.absence_assessments:
        if assessment.episode_id not in episodes:
            errors.append(
                f"absence assessment {assessment.absence_assessment_id} references unknown episode"
            )
        require_provenance(
            assessment.source_provenance_ids,
            f"absence assessment {assessment.absence_assessment_id}",
        )

    for fact in record.episode_facts:
        owning_episode = episodes.get(fact.episode_id)
        if owning_episode is None:
            errors.append(f"fact {fact.fact_id} references unknown episode")
        elif fact.fact_id not in owning_episode.fact_ids:
            errors.append(f"fact {fact.fact_id} is absent from its episode fact list")
        require_provenance(fact.source_provenance_ids, f"fact {fact.fact_id}")
        require_provenance(
            fact.temporal_relation_provenance_ids,
            f"temporal relation {fact.fact_id}",
        )
        require_provenance(
            fact.participant_correction_provenance_ids,
            f"fact correction {fact.fact_id}",
        )
        if fact.qualification is not None:
            require_provenance(
                fact.qualification.source_provenance_ids,
                f"fact qualification {fact.qualification.qualification_id}",
            )
        if fact.absence_assessment_id is not None:
            linked_assessment = assessments.get(fact.absence_assessment_id)
            if linked_assessment is None:
                errors.append(f"fact {fact.fact_id} references unknown absence assessment")
            elif not linked_assessment.is_admitted:
                errors.append(f"fact {fact.fact_id} references a non-admitted absence assessment")
            elif (
                linked_assessment.episode_id != fact.episode_id
                or linked_assessment.actor != fact.actor
                or linked_assessment.absent_proposition != fact.proposition
            ):
                errors.append(f"fact {fact.fact_id} disagrees with its absence assessment")

    lineages: dict[str, list[EpisodeFactV2]] = {}
    for fact in record.episode_facts:
        lineages.setdefault(fact.fact_lineage_id, []).append(fact)
    for lineage_id, fact_rows in lineages.items():
        ordered_facts = sorted(fact_rows, key=lambda row: row.revision_index)
        indices = [row.revision_index for row in ordered_facts]
        if indices != list(range(len(ordered_facts))):
            errors.append(f"fact lineage {lineage_id} revisions are not contiguous and monotonic")
            continue
        children: dict[str, int] = {}
        for position, lineage_fact in enumerate(ordered_facts):
            if position == 0:
                continue
            predecessor_fact = ordered_facts[position - 1]
            if lineage_fact.supersedes_fact_id != predecessor_fact.fact_id:
                errors.append(
                    f"fact {lineage_fact.fact_id} does not supersede its immediate predecessor"
                )
            if lineage_fact.episode_id != predecessor_fact.episode_id:
                errors.append(f"fact lineage {lineage_id} crosses episode boundaries")
            if lineage_fact.supersedes_fact_id is not None:
                children[lineage_fact.supersedes_fact_id] = (
                    children.get(lineage_fact.supersedes_fact_id, 0) + 1
                )
        if any(count > 1 for count in children.values()):
            errors.append(f"fact lineage {lineage_id} branches")

    links_by_fact_and_thread: dict[tuple[str, str], AcquisitionPhase] = {}
    for link in record.pattern_evidence_links:
        introducing_proposal = proposals.get(link.proposal_id)
        linked_episode = episodes.get(link.episode_id)
        if introducing_proposal is None:
            errors.append(f"evidence link {link.evidence_link_id} references unknown proposal")
        if linked_episode is None:
            errors.append(f"evidence link {link.evidence_link_id} references unknown episode")
        for fact_id in link.fact_ids:
            fact = facts.get(fact_id)
            if fact is None:
                errors.append(f"evidence link {link.evidence_link_id} references unknown fact")
                continue
            if fact.episode_id != link.episode_id:
                errors.append(f"evidence link {link.evidence_link_id} crosses episode boundaries")
            if introducing_proposal is not None:
                key = (introducing_proposal.pattern_thread_id, fact_id)
                existing_phase = links_by_fact_and_thread.get(key)
                if existing_phase is not None and existing_phase != link.acquisition_phase:
                    errors.append(
                        f"evidence timing changed for fact {fact_id} in thread "
                        f"{introducing_proposal.pattern_thread_id}"
                    )
                links_by_fact_and_thread[key] = link.acquisition_phase

    proposals_by_thread: dict[str, list[PatternProposalV2]] = {}
    for proposal in record.pattern_proposals:
        proposals_by_thread.setdefault(proposal.pattern_thread_id, []).append(proposal)
    for thread_id, proposal_rows in proposals_by_thread.items():
        ordered_proposals = sorted(proposal_rows, key=lambda row: row.revision_index)
        indices = [row.revision_index for row in ordered_proposals]
        if indices != list(range(len(ordered_proposals))):
            errors.append(f"pattern thread {thread_id} revisions are not contiguous and monotonic")
            continue
        for position, thread_proposal in enumerate(ordered_proposals):
            if position > 0:
                predecessor_proposal = ordered_proposals[position - 1]
                if thread_proposal.previous_proposal_id != predecessor_proposal.proposal_id:
                    errors.append(
                        f"proposal {thread_proposal.proposal_id} does not reference its immediate "
                        "predecessor"
                    )
                prior_adjudication = adjudications.get(predecessor_proposal.proposal_id)
                if prior_adjudication is None or prior_adjudication.decision != "revise":
                    errors.append(
                        f"proposal {thread_proposal.proposal_id} lacks a prior revise adjudication"
                    )
                elif thread_proposal.proposition != prior_adjudication.participant_approved_wording:
                    errors.append(
                        f"proposal {thread_proposal.proposal_id} does not preserve participant "
                        "revision wording"
                    )
            for link_id in thread_proposal.evidence_link_ids:
                referenced_link = evidence_links.get(link_id)
                if referenced_link is None:
                    errors.append(
                        f"proposal {thread_proposal.proposal_id} references unknown evidence"
                    )
                    continue
                introducing = proposals.get(referenced_link.proposal_id)
                if introducing is None:
                    continue
                if (
                    introducing.pattern_thread_id != thread_id
                    or introducing.revision_index > thread_proposal.revision_index
                ):
                    errors.append(
                        f"proposal {thread_proposal.proposal_id} uses evidence outside its thread "
                        "history"
                    )
            if position == 0 and not any(
                evidence_links.get(link_id) is not None
                and evidence_links[link_id].role == "preproposal_anchor"
                and evidence_links[link_id].acquisition_phase == "pre_first_proposal"
                for link_id in thread_proposal.evidence_link_ids
            ):
                errors.append(
                    f"first proposal {thread_proposal.proposal_id} lacks a preproposal anchor"
                )

    adjudications_by_proposal: dict[str, list[ParticipantAdjudicationV2]] = {}
    for adjudication in record.participant_adjudications:
        adjudications_by_proposal.setdefault(adjudication.proposal_id, []).append(adjudication)
        adjudicated_proposal = proposals.get(adjudication.proposal_id)
        if adjudicated_proposal is None:
            errors.append(
                f"adjudication {adjudication.adjudication_id} references unknown proposal"
            )
        require_provenance(
            adjudication.participant_response_provenance_ids,
            f"adjudication {adjudication.adjudication_id}",
        )
        for link_id in adjudication.counterexample_evidence_link_ids:
            counterexample_link = evidence_links.get(link_id)
            if counterexample_link is None or "counterexample" not in counterexample_link.role:
                errors.append(
                    f"adjudication {adjudication.adjudication_id} has invalid counterexample "
                    "evidence"
                )
            elif adjudicated_proposal is not None:
                introducing = proposals.get(counterexample_link.proposal_id)
                if (
                    introducing is None
                    or introducing.pattern_thread_id != adjudicated_proposal.pattern_thread_id
                ):
                    errors.append(
                        f"adjudication {adjudication.adjudication_id} uses another thread's "
                        "evidence"
                    )
        if (
            adjudication.decision == "accept"
            and adjudicated_proposal is not None
            and adjudication.participant_approved_wording != adjudicated_proposal.proposition
        ):
            errors.append(
                f"accepted proposal {adjudicated_proposal.proposal_id} differs from "
                "participant-approved wording"
            )
    for proposal_id, adjudication_rows in adjudications_by_proposal.items():
        if len(adjudication_rows) > 1:
            errors.append(f"proposal {proposal_id} has multiple adjudications")

    return tuple(dict.fromkeys(errors))


def _current_fact_ids(record: LifePatternsRecordV2) -> set[str]:
    superseded = {
        fact.supersedes_fact_id
        for fact in record.episode_facts
        if fact.supersedes_fact_id is not None
    }
    return {fact.fact_id for fact in record.episode_facts if fact.fact_id not in superseded}


def _call_nonoccurrence_twice(callback: NonoccurrenceCallback, fact: EpisodeFactV2) -> bool:
    first = callback(fact)
    second = callback(fact)
    if type(first) is not bool or type(second) is not bool:  # noqa: E721
        raise LifePatternsV2ValidationError(
            (f"nonoccurrence callback returned a non-boolean for fact {fact.fact_id}",)
        )
    if first != second:
        raise LifePatternsV2ValidationError(
            (f"nonoccurrence callback was nondeterministic for fact {fact.fact_id}",)
        )
    return first


def _call_grounding_twice(
    callback: GroundingCallback,
    proposal: PatternProposalV2,
    link: PatternEvidenceLinkV2,
    facts: tuple[EpisodeFactV2, ...],
) -> bool:
    first = callback(proposal, link, facts)
    second = callback(proposal, link, facts)
    if type(first) is not bool or type(second) is not bool:  # noqa: E721
        raise LifePatternsV2ValidationError(
            (f"grounding callback returned a non-boolean for link {link.evidence_link_id}",)
        )
    if first != second:
        raise LifePatternsV2ValidationError(
            (f"grounding callback was nondeterministic for link {link.evidence_link_id}",)
        )
    return first


def _semantic_receipt(
    record: LifePatternsRecordV2,
    callbacks: TheoryBlindSemanticCallbacksV2,
) -> SemanticValidationReceiptV2:
    facts = {row.fact_id: row for row in record.episode_facts}
    links = {row.evidence_link_id: row for row in record.pattern_evidence_links}
    fact_decisions = tuple(
        FactSemanticDecisionV2(
            fact_id=fact.fact_id,
            asserts_real_world_nonoccurrence=_call_nonoccurrence_twice(
                callbacks.asserts_real_world_nonoccurrence, fact
            ),
        )
        for fact in sorted(record.episode_facts, key=lambda row: row.fact_id)
    )
    grounding_decisions: list[GroundingSemanticDecisionV2] = []
    for proposal in sorted(
        record.pattern_proposals,
        key=lambda row: (row.pattern_thread_id, row.revision_index, row.proposal_id),
    ):
        for link_id in sorted(proposal.grounding_evidence_link_ids):
            link = links[link_id]
            linked_facts = tuple(facts[fact_id] for fact_id in link.fact_ids)
            grounding_decisions.append(
                GroundingSemanticDecisionV2(
                    proposal_id=proposal.proposal_id,
                    evidence_link_id=link_id,
                    supports_current_proposition=_call_grounding_twice(
                        callbacks.grounding_supports_current_proposition,
                        proposal,
                        link,
                        linked_facts,
                    ),
                )
            )
    return SemanticValidationReceiptV2(
        callback_provenance=callbacks.provenance,
        fact_decisions=fact_decisions,
        grounding_decisions=tuple(grounding_decisions),
    )


def _semantic_errors(
    record: LifePatternsRecordV2,
    receipt: SemanticValidationReceiptV2,
) -> tuple[str, ...]:
    errors: list[str] = []
    fact_decisions = {row.fact_id: row for row in receipt.fact_decisions}
    grounding_decisions = {
        (row.proposal_id, row.evidence_link_id): row for row in receipt.grounding_decisions
    }
    links = {row.evidence_link_id: row for row in record.pattern_evidence_links}
    current_fact_ids = _current_fact_ids(record)

    for fact in record.episode_facts:
        establishes_nonoccurrence = fact_decisions[fact.fact_id].asserts_real_world_nonoccurrence
        if establishes_nonoccurrence and fact.assertion_type != "admitted_absence":
            errors.append(
                f"fact {fact.fact_id} establishes real-world nonoccurrence outside the "
                "absence route"
            )
        if fact.assertion_type == "admitted_absence" and not establishes_nonoccurrence:
            errors.append(
                f"fact {fact.fact_id} uses the absence route without a real-world "
                "nonoccurrence claim"
            )

    proposals_by_thread: dict[str, list[PatternProposalV2]] = {}
    for proposal in record.pattern_proposals:
        proposals_by_thread.setdefault(proposal.pattern_thread_id, []).append(proposal)
    for thread_id, rows in proposals_by_thread.items():
        terminal = max(rows, key=lambda row: row.revision_index)
        usable_grounding = False
        for link_id in terminal.grounding_evidence_link_ids:
            link = links[link_id]
            if any(fact_id not in current_fact_ids for fact_id in link.fact_ids):
                errors.append(
                    f"operative proposal {terminal.proposal_id} grounds through a superseded fact"
                )
                continue
            decision = grounding_decisions[(terminal.proposal_id, link_id)]
            if (
                link.role == "preproposal_anchor"
                and link.acquisition_phase == "pre_first_proposal"
                and decision.supports_current_proposition
            ):
                usable_grounding = True
        if not usable_grounding:
            errors.append(
                f"operative proposal {terminal.proposal_id} lacks semantic grounding for its "
                f"current proposition in thread {thread_id}"
            )
    return tuple(dict.fromkeys(errors))


def validate_life_patterns_record_v2(
    record: LifePatternsRecordV2,
    *,
    callbacks: TheoryBlindSemanticCallbacksV2,
) -> SemanticValidationReceiptV2:
    """Validate the complete record, including required target-theory-blind semantics."""

    structural = _structure_errors(record)
    if structural:
        raise LifePatternsV2ValidationError(structural)
    receipt = _semantic_receipt(record, callbacks)
    semantic = _semantic_errors(record, receipt)
    if semantic:
        raise LifePatternsV2ValidationError(semantic)
    return receipt


def _derive_resolved_patterns(
    record: LifePatternsRecordV2,
    receipt: SemanticValidationReceiptV2,
) -> tuple[ResolvedPatternV2, ...]:
    proposals_by_thread: dict[str, list[PatternProposalV2]] = {}
    adjudications = {row.proposal_id: row for row in record.participant_adjudications}
    links = {row.evidence_link_id: row for row in record.pattern_evidence_links}
    grounding_decisions = {
        (row.proposal_id, row.evidence_link_id): row.supports_current_proposition
        for row in receipt.grounding_decisions
    }
    current_fact_ids = _current_fact_ids(record)
    for proposal in record.pattern_proposals:
        proposals_by_thread.setdefault(proposal.pattern_thread_id, []).append(proposal)

    resolved: list[ResolvedPatternV2] = []
    for thread_id, rows in proposals_by_thread.items():
        terminal = max(rows, key=lambda row: row.revision_index)
        adjudication = adjudications.get(terminal.proposal_id)
        if adjudication is None or adjudication.decision in {"revise", "unresolved"}:
            status: ResolvedPatternStatus = "unresolved"
        elif adjudication.decision == "accept":
            status = "accepted"
        else:
            status = "rejected"
        supporting = tuple(
            link_id
            for link_id in terminal.grounding_evidence_link_ids
            if links[link_id].role == "preproposal_anchor"
            and links[link_id].acquisition_phase == "pre_first_proposal"
            and set(links[link_id].fact_ids).issubset(current_fact_ids)
            and grounding_decisions[(terminal.proposal_id, link_id)]
        )
        resolved.append(
            ResolvedPatternV2(
                pattern_thread_id=thread_id,
                status=status,
                terminal_proposal_id=terminal.proposal_id,
                supporting_preproposal_evidence_link_ids=supporting,
                participant_response_provenance_ids=(
                    adjudication.participant_response_provenance_ids
                    if adjudication is not None
                    else ()
                ),
                participant_approved_wording=(
                    adjudication.participant_approved_wording
                    if adjudication is not None and status == "accepted"
                    else None
                ),
                scope_note=(
                    adjudication.scope_note
                    if adjudication is not None and status == "accepted"
                    else None
                ),
                exception_note=(
                    adjudication.exception_note
                    if adjudication is not None and status == "accepted"
                    else None
                ),
            )
        )
    return tuple(sorted(resolved, key=lambda row: row.pattern_thread_id))


def freeze_life_patterns_record_v2(
    record: LifePatternsRecordV2,
    *,
    callbacks: TheoryBlindSemanticCallbacksV2,
) -> LifePatternsFreezeEnvelopeV2:
    """Validate and content-address one immutable audit-complete v2 freeze."""

    receipt = validate_life_patterns_record_v2(record, callbacks=callbacks)
    payload = LifePatternsFreezePayloadV2(
        contract_sha256=record.contract_sha256,
        source_archive_sha256=record.source_archive_sha256,
        source_provenance=tuple(
            sorted(record.source_provenance, key=lambda row: row.source_provenance_id)
        ),
        episodes=tuple(sorted(record.episodes, key=lambda row: row.episode_id)),
        episode_facts=tuple(
            sorted(
                record.episode_facts,
                key=lambda row: (row.fact_lineage_id, row.revision_index, row.fact_id),
            )
        ),
        absence_assessments=tuple(
            sorted(record.absence_assessments, key=lambda row: row.absence_assessment_id)
        ),
        pattern_proposals=tuple(
            sorted(
                record.pattern_proposals,
                key=lambda row: (row.pattern_thread_id, row.revision_index, row.proposal_id),
            )
        ),
        pattern_evidence_links=tuple(
            sorted(record.pattern_evidence_links, key=lambda row: row.evidence_link_id)
        ),
        participant_adjudications=tuple(
            sorted(record.participant_adjudications, key=lambda row: row.adjudication_id)
        ),
        resolved_patterns=_derive_resolved_patterns(record, receipt),
        semantic_validation=receipt,
    )
    return LifePatternsFreezeEnvelopeV2(
        payload=payload,
        freeze_payload_sha256=sha256_json(payload),
    )


def _record_from_payload(payload: LifePatternsFreezePayloadV2) -> LifePatternsRecordV2:
    return LifePatternsRecordV2(
        contract_sha256=payload.contract_sha256,
        source_archive_sha256=payload.source_archive_sha256,
        source_provenance=payload.source_provenance,
        episodes=payload.episodes,
        episode_facts=payload.episode_facts,
        absence_assessments=payload.absence_assessments,
        pattern_proposals=payload.pattern_proposals,
        pattern_evidence_links=payload.pattern_evidence_links,
        participant_adjudications=payload.participant_adjudications,
    )


def validate_life_patterns_freeze_v2(
    freeze: LifePatternsFreezeEnvelopeV2,
    *,
    callbacks: TheoryBlindSemanticCallbacksV2,
) -> None:
    """Verify bytes, derivations, and semantic callback decisions before projection."""

    if sha256_json(freeze.payload) != freeze.freeze_payload_sha256:
        raise LifePatternsV2ValidationError(("freeze payload hash does not match payload",))
    record = _record_from_payload(freeze.payload)
    receipt = validate_life_patterns_record_v2(record, callbacks=callbacks)
    if receipt != freeze.payload.semantic_validation:
        raise LifePatternsV2ValidationError(
            ("freeze semantic validation receipt does not match current callbacks",)
        )
    if _derive_resolved_patterns(record, receipt) != freeze.payload.resolved_patterns:
        raise LifePatternsV2ValidationError(("freeze resolved patterns are not derivable",))


def build_adapter_projection_v2(
    freeze: LifePatternsFreezeEnvelopeV2,
    *,
    callbacks: TheoryBlindSemanticCallbacksV2,
) -> AdapterProjectionV2:
    """Build the narrow no-reread projection after complete semantic revalidation."""

    validate_life_patterns_freeze_v2(freeze, callbacks=callbacks)
    payload = freeze.payload
    current_fact_ids = _current_fact_ids(_record_from_payload(payload))
    current_facts = tuple(
        fact for fact in payload.episode_facts if fact.fact_id in current_fact_ids
    )
    accepted = tuple(
        pattern for pattern in payload.resolved_patterns if pattern.status == "accepted"
    )
    proposals = {row.proposal_id: row for row in payload.pattern_proposals}
    adjudications = {row.proposal_id: row for row in payload.participant_adjudications}
    links = {row.evidence_link_id: row for row in payload.pattern_evidence_links}

    operative_link_ids: set[str] = set()
    for pattern in accepted:
        proposal = proposals[pattern.terminal_proposal_id]
        operative_link_ids.update(proposal.grounding_evidence_link_ids)
        adjudication = adjudications.get(pattern.terminal_proposal_id)
        if adjudication is not None:
            operative_link_ids.update(adjudication.counterexample_evidence_link_ids)
    for link_id in operative_link_ids:
        if not set(links[link_id].fact_ids).issubset(current_fact_ids):
            raise LifePatternsV2ValidationError(
                (f"operative evidence link {link_id} references a superseded fact",)
            )

    admitted_assessment_ids = {
        fact.absence_assessment_id
        for fact in current_facts
        if fact.absence_assessment_id is not None
    }
    admitted_assessments = tuple(
        assessment
        for assessment in payload.absence_assessments
        if assessment.absence_assessment_id in admitted_assessment_ids
    )

    used_provenance_ids: set[str] = set()
    for fact in current_facts:
        used_provenance_ids.update(fact.source_provenance_ids)
        used_provenance_ids.update(fact.participant_correction_provenance_ids)
        used_provenance_ids.update(fact.temporal_relation_provenance_ids)
        if fact.qualification is not None:
            used_provenance_ids.update(fact.qualification.source_provenance_ids)
    for assessment in admitted_assessments:
        used_provenance_ids.update(assessment.source_provenance_ids)
    for pattern in accepted:
        used_provenance_ids.update(pattern.participant_response_provenance_ids)

    return AdapterProjectionV2(
        freeze_payload_sha256=freeze.freeze_payload_sha256,
        contract_sha256=payload.contract_sha256,
        source_archive_sha256=payload.source_archive_sha256,
        semantic_validation_provenance=payload.semantic_validation.callback_provenance,
        source_provenance=tuple(
            row
            for row in payload.source_provenance
            if row.source_provenance_id in used_provenance_ids
        ),
        episode_facts=tuple(ProjectedEpisodeFactV2(fact=fact) for fact in current_facts),
        admitted_absence_assessments=admitted_assessments,
        accepted_patterns=tuple(
            ProjectedResolvedPatternV2(pattern=pattern) for pattern in accepted
        ),
        operative_evidence_links=tuple(links[link_id] for link_id in sorted(operative_link_ids)),
    )


def validate_adapter_operation_v2(
    projection: AdapterProjectionV2,
    operation: AdapterOperationV2,
) -> None:
    fact_ids = {row.fact.fact_id for row in projection.episode_facts}
    pattern_ids = {row.pattern.pattern_thread_id for row in projection.accepted_patterns}
    missing_facts = sorted(set(operation.episode_fact_ids) - fact_ids)
    missing_patterns = sorted(set(operation.resolved_pattern_thread_ids) - pattern_ids)
    errors: list[str] = []
    if missing_facts:
        errors.append(f"adapter requested unrepresented episode facts: {','.join(missing_facts)}")
    if missing_patterns:
        errors.append(
            f"adapter requested unrepresented accepted patterns: {','.join(missing_patterns)}"
        )
    if operation.operation != "inspect" and operation.episode_fact_ids:
        requested_facts = {
            row.fact.fact_id: row.fact
            for row in projection.episode_facts
            if row.fact.fact_id in operation.episode_fact_ids
        }
        if len({fact.episode_id for fact in requested_facts.values()}) > 1:
            errors.append("non-inspect episode-fact operations cannot cross episode boundaries")
    if errors:
        raise LifePatternsV2ValidationError(tuple(errors))


def person_level_pattern_or_unmeasured_v2(
    projection: AdapterProjectionV2,
    pattern_thread_id: str,
) -> ProjectedResolvedPatternV2 | UnmeasuredNotRepresentedV2:
    for pattern in projection.accepted_patterns:
        if pattern.pattern.pattern_thread_id == pattern_thread_id:
            return pattern
    return UnmeasuredNotRepresentedV2(distinction=pattern_thread_id)


def require_same_freeze_v2(*projections: AdapterProjectionV2) -> str:
    hashes = {projection.freeze_payload_sha256 for projection in projections}
    if len(hashes) != 1:
        raise LifePatternsV2ValidationError(
            ("all adapters in one comparison must consume the same freeze",)
        )
    if not hashes:
        raise LifePatternsV2ValidationError(("comparison requires at least one projection",))
    return next(iter(hashes))


def write_life_patterns_freeze_v2(
    path: str | Path,
    freeze: LifePatternsFreezeEnvelopeV2,
) -> Path:
    """Create, never replace, the canonical bytes of an immutable freeze."""

    return write_new_bytes(path, canonical_json_bytes(freeze))


def load_life_patterns_freeze_v2(
    path: str | Path,
    *,
    callbacks: TheoryBlindSemanticCallbacksV2,
) -> LifePatternsFreezeEnvelopeV2:
    value = load_json_bytes(path, require_canonical=True)
    freeze = LifePatternsFreezeEnvelopeV2.model_validate(value)
    validate_life_patterns_freeze_v2(freeze, callbacks=callbacks)
    return freeze
