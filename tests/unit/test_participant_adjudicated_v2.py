from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from hdmatch.evaluation.participant_adjudicated_v2 import (
    AbsenceAssessmentV2,
    AdapterOperationV2,
    EpisodeFactV2,
    EpisodeUncertaintyNoteV2,
    EpisodeV2,
    FactQualificationV2,
    LifePatternsRecordV2,
    LifePatternsV2ValidationError,
    ParticipantAdjudicationV2,
    PatternEvidenceLinkV2,
    PatternProposalV2,
    SemanticCallbackProvenanceV2,
    SourceProvenanceV2,
    TheoryBlindSemanticCallbacksV2,
    build_adapter_projection_v2,
    freeze_life_patterns_record_v2,
    load_life_patterns_freeze_v2,
    person_level_pattern_or_unmeasured_v2,
    require_same_freeze_v2,
    validate_adapter_operation_v2,
    validate_life_patterns_record_v2,
    write_life_patterns_freeze_v2,
)

CONTRACT_SHA = "a" * 64
ARCHIVE_SHA = "b" * 64


def _source(source_id: str, digest_char: str) -> SourceProvenanceV2:
    return SourceProvenanceV2(
        source_provenance_id=source_id,
        source_record_id=f"record-{source_id}",
        locator=f"segment:{source_id}",
        content_sha256=digest_char * 64,
        exact_text_available=True,
    )


SOURCES = (
    _source("SRC-EPISODE", "c"),
    _source("SRC-PARTICIPANT", "d"),
    _source("SRC-CORRECTION", "e"),
)


def _fact(
    fact_id: str = "FACT-0",
    *,
    lineage_id: str = "LINEAGE-1",
    revision_index: int = 0,
    episode_id: str = "EP-1",
    assertion_type: str = "positive_occurrence",
    proposition: str = "The participant made a checklist before complex work.",
    qualification: FactQualificationV2 | None = None,
    absence_assessment_id: str | None = None,
    supersedes_fact_id: str | None = None,
    correction_provenance: tuple[str, ...] = (),
) -> EpisodeFactV2:
    return EpisodeFactV2(
        fact_id=fact_id,
        fact_lineage_id=lineage_id,
        revision_index=revision_index,
        episode_id=episode_id,
        assertion_type=assertion_type,
        actor="participant",
        proposition=proposition,
        source_provenance_ids=("SRC-EPISODE",),
        qualification=qualification,
        absence_assessment_id=absence_assessment_id,
        supersedes_fact_id=supersedes_fact_id,
        participant_correction_provenance_ids=correction_provenance,
    )


def _episode(
    fact_ids: tuple[str, ...] = ("FACT-0",),
    *,
    episode_id: str = "EP-1",
    uncertainty_notes: tuple[EpisodeUncertaintyNoteV2, ...] = (),
) -> EpisodeV2:
    return EpisodeV2(
        episode_id=episode_id,
        neutral_summary="A bounded planning episode.",
        source_provenance_ids=("SRC-EPISODE",),
        fact_ids=fact_ids,
        uncertainty_notes=uncertainty_notes,
    )


def _proposal(
    proposal_id: str = "PROPOSAL-0",
    *,
    revision_index: int = 0,
    proposition: str = "I prepare before complex work.",
    evidence_link_ids: tuple[str, ...] = ("LINK-0",),
    grounding_link_ids: tuple[str, ...] = ("LINK-0",),
    previous_proposal_id: str | None = None,
) -> PatternProposalV2:
    return PatternProposalV2(
        proposal_id=proposal_id,
        pattern_thread_id="THREAD-1",
        revision_index=revision_index,
        proposition=proposition,
        question_text=f"Does this fit: {proposition}",
        evidence_link_ids=evidence_link_ids,
        grounding_evidence_link_ids=grounding_link_ids,
        previous_proposal_id=previous_proposal_id,
    )


def _link(
    link_id: str = "LINK-0",
    *,
    proposal_id: str = "PROPOSAL-0",
    fact_ids: tuple[str, ...] = ("FACT-0",),
    episode_id: str = "EP-1",
    role: str = "preproposal_anchor",
    phase: str = "pre_first_proposal",
) -> PatternEvidenceLinkV2:
    return PatternEvidenceLinkV2(
        evidence_link_id=link_id,
        proposal_id=proposal_id,
        episode_id=episode_id,
        fact_ids=fact_ids,
        role=role,
        acquisition_phase=phase,
    )


def _adjudication(
    adjudication_id: str = "ADJ-0",
    *,
    proposal_id: str = "PROPOSAL-0",
    decision: str = "accept",
    wording: str = "I prepare before complex work.",
) -> ParticipantAdjudicationV2:
    return ParticipantAdjudicationV2(
        adjudication_id=adjudication_id,
        proposal_id=proposal_id,
        decision=decision,
        participant_response_provenance_ids=("SRC-PARTICIPANT",),
        participant_approved_wording=wording,
    )


def _record(
    *,
    facts: tuple[EpisodeFactV2, ...] = (_fact(),),
    episodes: tuple[EpisodeV2, ...] | None = None,
    assessments: tuple[AbsenceAssessmentV2, ...] = (),
    proposals: tuple[PatternProposalV2, ...] = (),
    links: tuple[PatternEvidenceLinkV2, ...] = (),
    adjudications: tuple[ParticipantAdjudicationV2, ...] = (),
) -> LifePatternsRecordV2:
    if episodes is None:
        by_episode: dict[str, list[str]] = {}
        for fact in facts:
            by_episode.setdefault(fact.episode_id, []).append(fact.fact_id)
        episodes = tuple(
            _episode(tuple(fact_ids), episode_id=episode_id)
            for episode_id, fact_ids in sorted(by_episode.items())
        )
    return LifePatternsRecordV2(
        contract_sha256=CONTRACT_SHA,
        source_archive_sha256=ARCHIVE_SHA,
        source_provenance=SOURCES,
        episodes=episodes,
        episode_facts=facts,
        absence_assessments=assessments,
        pattern_proposals=proposals,
        pattern_evidence_links=links,
        participant_adjudications=adjudications,
    )


def _accepted_record(
    *,
    fact: EpisodeFactV2 | None = None,
    proposal: PatternProposalV2 | None = None,
    link: PatternEvidenceLinkV2 | None = None,
    adjudication: ParticipantAdjudicationV2 | None = None,
) -> LifePatternsRecordV2:
    selected_fact = fact or _fact()
    return _record(
        facts=(selected_fact,),
        proposals=(proposal or _proposal(),),
        links=(link or _link(fact_ids=(selected_fact.fact_id,)),),
        adjudications=(adjudication or _adjudication(),),
    )


def _callbacks(
    supported_propositions: frozenset[str] = frozenset({"I prepare before complex work."}),
) -> TheoryBlindSemanticCallbacksV2:
    return TheoryBlindSemanticCallbacksV2(
        provenance=SemanticCallbackProvenanceV2(
            validator_id="synthetic-theory-blind-validator",
            validator_version="1",
            validator_sha256="f" * 64,
        ),
        asserts_real_world_nonoccurrence=lambda fact: fact.proposition.startswith(
            "NONOCCURRENCE:"
        ),
        grounding_supports_current_proposition=(
            lambda proposal, _link, facts: proposal.proposition in supported_propositions
            and bool(facts)
        ),
    )


def test_t001_absence_route_requires_semantic_nonoccurrence_callback() -> None:
    mislabeled = _record(
        facts=(
            _fact(
                assertion_type="positive_occurrence",
                proposition="NONOCCURRENCE: no message was sent during the agreed window.",
            ),
        )
    )
    with pytest.raises(LifePatternsV2ValidationError, match="outside the absence route"):
        validate_life_patterns_record_v2(mislabeled, callbacks=_callbacks())

    appraisal = _record(
        facts=(
            _fact(
                assertion_type="reported_appraisal_or_belief",
                proposition="The participant believed no message had been sent.",
            ),
        )
    )
    validate_life_patterns_record_v2(appraisal, callbacks=_callbacks())

    assessment = AbsenceAssessmentV2(
        absence_assessment_id="ABS-1",
        episode_id="EP-1",
        actor="participant",
        absent_proposition="NONOCCURRENCE: no message was sent during the agreed window.",
        window_or_opportunity="The agreed response window.",
        awareness="established",
        opportunity="established",
        reasonable_feasibility="established",
        established_nonoccurrence="established",
        source_provenance_ids=("SRC-EPISODE",),
        evidence_basis="explicit_report_or_observation",
    )
    admitted = _record(
        facts=(
            _fact(
                assertion_type="admitted_absence",
                proposition=assessment.absent_proposition,
                absence_assessment_id=assessment.absence_assessment_id,
            ),
        ),
        assessments=(assessment,),
    )
    validate_life_patterns_record_v2(admitted, callbacks=_callbacks())


def test_t002_timing_is_immutable_across_pattern_revisions() -> None:
    later_fact = _fact(
        "FACT-LATER",
        lineage_id="LINEAGE-LATER",
        proposition="The participant later described a second planning example.",
    )
    post_link = _link(
        "LINK-POST",
        fact_ids=(later_fact.fact_id,),
        role="postproposal_scope_example",
        phase="post_first_proposal",
    )
    valid = _record(
        facts=(_fact(), later_fact),
        proposals=(
            _proposal(evidence_link_ids=("LINK-0", "LINK-POST")),
        ),
        links=(_link(), post_link),
        adjudications=(_adjudication(),),
    )
    validate_life_patterns_record_v2(valid, callbacks=_callbacks())

    with pytest.raises(ValidationError, match="frozen"):
        post_link.acquisition_phase = "pre_first_proposal"  # type: ignore[misc]

    promoted_copy = _link(
        "LINK-PROMOTED",
        fact_ids=(later_fact.fact_id,),
        role="preproposal_anchor",
        phase="pre_first_proposal",
    )
    invalid = valid.model_copy(
        update={
            "pattern_evidence_links": valid.pattern_evidence_links + (promoted_copy,),
            "pattern_proposals": (
                valid.pattern_proposals[0].model_copy(
                    update={
                        "evidence_link_ids": ("LINK-0", "LINK-POST", "LINK-PROMOTED")
                    }
                ),
            ),
        }
    )
    with pytest.raises(LifePatternsV2ValidationError, match="evidence timing changed"):
        validate_life_patterns_record_v2(invalid, callbacks=_callbacks())


def test_t003_terminal_revision_requires_semantic_current_proposition_grounding() -> None:
    first = _proposal()
    revision = _proposal(
        "PROPOSAL-1",
        revision_index=1,
        proposition="I plan before complex work.",
        previous_proposal_id=first.proposal_id,
    )
    record = _record(
        proposals=(first, revision),
        links=(_link(),),
        adjudications=(
            _adjudication(decision="revise", wording=revision.proposition),
            _adjudication(
                "ADJ-1",
                proposal_id=revision.proposal_id,
                wording=revision.proposition,
            ),
        ),
    )
    with pytest.raises(LifePatternsV2ValidationError, match="current proposition"):
        validate_life_patterns_record_v2(record, callbacks=_callbacks())

    validate_life_patterns_record_v2(
        record,
        callbacks=_callbacks(
            frozenset({"I prepare before complex work.", "I plan before complex work."})
        ),
    )


def test_t004_fact_corrections_are_append_only_unique_leafs() -> None:
    original = _fact()
    correction = _fact(
        "FACT-1",
        revision_index=1,
        proposition="The participant wrote a plan before complex work.",
        supersedes_fact_id=original.fact_id,
        correction_provenance=("SRC-CORRECTION",),
    )
    proposal = _proposal(proposition="I plan before complex work.")
    adjudication = _adjudication(wording=proposal.proposition)
    stale_grounding = _record(
        facts=(original, correction),
        proposals=(proposal,),
        links=(_link(fact_ids=(original.fact_id,)),),
        adjudications=(adjudication,),
    )
    callbacks = _callbacks(frozenset({proposal.proposition}))
    with pytest.raises(LifePatternsV2ValidationError, match="superseded fact"):
        validate_life_patterns_record_v2(stale_grounding, callbacks=callbacks)

    current_grounding = stale_grounding.model_copy(
        update={"pattern_evidence_links": (_link(fact_ids=(correction.fact_id,)),)}
    )
    freeze = freeze_life_patterns_record_v2(current_grounding, callbacks=callbacks)
    projection = build_adapter_projection_v2(freeze, callbacks=callbacks)
    assert [row.fact.fact_id for row in projection.episode_facts] == [correction.fact_id]

    branch = _fact(
        "FACT-BRANCH",
        revision_index=1,
        proposition="The participant made a schedule.",
        supersedes_fact_id=original.fact_id,
        correction_provenance=("SRC-CORRECTION",),
    )
    branching = _record(facts=(original, correction, branch))
    with pytest.raises(LifePatternsV2ValidationError, match="revisions|branches"):
        validate_life_patterns_record_v2(branching, callbacks=callbacks)

    with pytest.raises(ValidationError, match="frozen"):
        original.proposition = "Mutated in place."  # type: ignore[misc]


def test_t005_fact_qualification_survives_freeze_and_projection() -> None:
    qualification = FactQualificationV2(
        qualification_id="QUAL-1",
        text="The exact timing was uncertain.",
        source_provenance_ids=("SRC-EPISODE",),
    )
    fact = _fact(qualification=qualification)
    note = EpisodeUncertaintyNoteV2(
        note_id="NOTE-1",
        text=qualification.text,
        source_provenance_ids=("SRC-EPISODE",),
        affects_fact_ids=(fact.fact_id,),
    )
    record = _record(
        facts=(fact,),
        episodes=(_episode(uncertainty_notes=(note,)),),
    )
    freeze = freeze_life_patterns_record_v2(record, callbacks=_callbacks())
    projection = build_adapter_projection_v2(freeze, callbacks=_callbacks())
    assert projection.episode_facts[0].fact.qualification == qualification

    episode_only = _record(
        facts=(_fact(),),
        episodes=(_episode(uncertainty_notes=(note,)),),
    )
    with pytest.raises(LifePatternsV2ValidationError, match="episode-only uncertainty"):
        validate_life_patterns_record_v2(episode_only, callbacks=_callbacks())


def test_t006_adapter_firewall_rejects_episode_fact_person_level_aggregation() -> None:
    facts = (
        _fact(),
        _fact(
            "FACT-2",
            lineage_id="LINEAGE-2",
            episode_id="EP-2",
            proposition="The participant made another checklist.",
        ),
    )
    record = _record(facts=facts)
    projection = build_adapter_projection_v2(
        freeze_life_patterns_record_v2(record, callbacks=_callbacks()),
        callbacks=_callbacks(),
    )
    with pytest.raises(ValidationError, match="cannot be aggregated"):
        AdapterOperationV2(
            operation="aggregate",
            output_semantic_level="person_level_pattern",
            episode_fact_ids=("FACT-0", "FACT-2"),
        )
    missing = person_level_pattern_or_unmeasured_v2(projection, "THREAD-1")
    assert missing.status == "unmeasured/not_represented"
    assert missing.source_reread_permitted is False

    accepted_projection = build_adapter_projection_v2(
        freeze_life_patterns_record_v2(_accepted_record(), callbacks=_callbacks()),
        callbacks=_callbacks(),
    )
    operation = AdapterOperationV2(
        operation="inspect",
        output_semantic_level="person_level_pattern",
        resolved_pattern_thread_ids=("THREAD-1",),
    )
    validate_adapter_operation_v2(accepted_projection, operation)
    assert len(accepted_projection.accepted_patterns) == 1

    cross_episode_operation = AdapterOperationV2(
        operation="aggregate",
        output_semantic_level="episode_fact",
        episode_fact_ids=("FACT-0", "FACT-2"),
    )
    with pytest.raises(
        LifePatternsV2ValidationError,
        match="cannot cross episode boundaries",
    ):
        validate_adapter_operation_v2(projection, cross_episode_operation)


def test_freeze_is_deterministic_content_addressed_and_immutable(tmp_path: Path) -> None:
    record = _accepted_record()
    first = freeze_life_patterns_record_v2(record, callbacks=_callbacks())
    second = freeze_life_patterns_record_v2(record, callbacks=_callbacks())
    assert first == second

    changed_fact = _fact(proposition="The participant drafted a checklist before complex work.")
    changed = _accepted_record(fact=changed_fact)
    changed_freeze = freeze_life_patterns_record_v2(changed, callbacks=_callbacks())
    assert changed_freeze.freeze_payload_sha256 != first.freeze_payload_sha256

    path = tmp_path / "life-patterns.freeze.json"
    write_life_patterns_freeze_v2(path, first)
    assert load_life_patterns_freeze_v2(path, callbacks=_callbacks()) == first
    with pytest.raises(FileExistsError, match="immutable"):
        write_life_patterns_freeze_v2(path, first)


def test_projection_revalidates_callbacks_and_has_no_raw_narrative_escape() -> None:
    freeze = freeze_life_patterns_record_v2(_accepted_record(), callbacks=_callbacks())
    with pytest.raises(LifePatternsV2ValidationError, match="current proposition"):
        build_adapter_projection_v2(freeze, callbacks=_callbacks(frozenset()))

    projection = build_adapter_projection_v2(freeze, callbacks=_callbacks())
    dumped = projection.model_dump(mode="json")
    assert "episodes" not in dumped
    assert "neutral_summary" not in str(dumped)
    assert "source_resolver" not in str(dumped)
    assert require_same_freeze_v2(projection, projection) == freeze.freeze_payload_sha256


def test_regression_open_world_absence_and_temporal_rules_remain_fail_closed() -> None:
    open_world = _record(
        facts=(
            _fact(
                proposition=(
                    "The participant improvised a novel preparation ritual absent from every "
                    "optional vocabulary."
                )
            ),
        )
    )
    projection = build_adapter_projection_v2(
        freeze_life_patterns_record_v2(open_world, callbacks=_callbacks()),
        callbacks=_callbacks(),
    )
    assert projection.episode_facts[0].fact.proposition == open_world.episode_facts[0].proposition
    assert "other_specified" not in EpisodeFactV2.model_fields

    failed_absence = AbsenceAssessmentV2(
        absence_assessment_id="ABS-FAILED",
        episode_id="EP-1",
        actor="participant",
        absent_proposition="NONOCCURRENCE: no message was sent.",
        window_or_opportunity="The response window.",
        awareness="established",
        opportunity="unclear",
        reasonable_feasibility="established",
        established_nonoccurrence="established",
        source_provenance_ids=("SRC-EPISODE",),
        evidence_basis="explicit_report_or_observation",
    )
    invalid_negative = _record(
        facts=(
            _fact(
                assertion_type="admitted_absence",
                proposition=failed_absence.absent_proposition,
                absence_assessment_id=failed_absence.absence_assessment_id,
            ),
        ),
        assessments=(failed_absence,),
    )
    with pytest.raises(LifePatternsV2ValidationError, match="non-admitted absence"):
        validate_life_patterns_record_v2(invalid_negative, callbacks=_callbacks())

    positive_with_failed_absence = _record(assessments=(failed_absence,))
    positive_projection = build_adapter_projection_v2(
        freeze_life_patterns_record_v2(positive_with_failed_absence, callbacks=_callbacks()),
        callbacks=_callbacks(),
    )
    assert [row.fact.fact_id for row in positive_projection.episode_facts] == ["FACT-0"]
    assert positive_projection.admitted_absence_assessments == ()

    with pytest.raises(ValidationError, match="silence or missingness"):
        AbsenceAssessmentV2(
            **failed_absence.model_dump(exclude={"opportunity", "evidence_basis"}),
            opportunity="established",
            evidence_basis="silence_or_missingness",
        )
    with pytest.raises(ValidationError, match="temporal relation"):
        _fact(
            assertion_type="temporal_relation",
            proposition="The checklist came before the call.",
        )
    with pytest.raises(ValidationError, match="target_result"):
        LifePatternsRecordV2.model_validate(
            open_world.model_dump(mode="python") | {"target_result": "forbidden"}
        )
    with pytest.raises(ValidationError, match="completion_denominator"):
        LifePatternsRecordV2.model_validate(
            open_world.model_dump(mode="python") | {"completion_denominator": 1}
        )


def test_rejected_pattern_remains_auditable_but_cannot_enter_projection() -> None:
    rejected = _accepted_record(
        adjudication=_adjudication(decision="reject", wording="not applicable"),
    )
    freeze = freeze_life_patterns_record_v2(rejected, callbacks=_callbacks())
    assert freeze.payload.resolved_patterns[0].status == "rejected"
    assert freeze.payload.participant_adjudications[0].decision == "reject"

    projection = build_adapter_projection_v2(freeze, callbacks=_callbacks())
    assert projection.accepted_patterns == ()
    assert [row.fact.fact_id for row in projection.episode_facts] == ["FACT-0"]
