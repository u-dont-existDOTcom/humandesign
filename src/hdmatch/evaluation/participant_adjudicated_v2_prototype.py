"""Small owner-development interaction probe for the participant-adjudicated v2 path.

This module is intentionally development-only: it uses a deterministic proposer and
synthetic source provenance, while every persisted decision crosses the frozen v2 core.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from hdmatch.evaluation.participant_adjudicated_v2 import (
    EpisodeFactV2,
    EpisodeV2,
    LifePatternsRecordV2,
    ParticipantAdjudicationV2,
    PatternEvidenceLinkV2,
    PatternProposalV2,
    SemanticCallbackProvenanceV2,
    SourceProvenanceV2,
    TheoryBlindSemanticCallbacksV2,
    build_adapter_projection_v2,
    freeze_life_patterns_record_v2,
    validate_life_patterns_record_v2,
)

_CONTRACT_SHA = "a" * 64
_ARCHIVE_SHA = "b" * 64
_CALLBACKS = TheoryBlindSemanticCallbacksV2(
    provenance=SemanticCallbackProvenanceV2(
        validator_id="owner-prototype-theory-blind-double",
        validator_version="1",
        validator_sha256="f" * 64,
    ),
    asserts_real_world_nonoccurrence=lambda fact: fact.proposition.startswith("NONOCCURRENCE:"),
    grounding_supports_current_proposition=lambda proposal, _link, facts: bool(facts)
    and proposal.proposition in {
        "I prepare before complex work.",
        "I plan before complex work.",
    },
)


def _source(source_id: str, digest: str) -> SourceProvenanceV2:
    return SourceProvenanceV2(
        source_provenance_id=source_id,
        source_record_id=f"prototype-{source_id}",
        locator=f"development:{source_id}",
        content_sha256=digest * 64,
        exact_text_available=True,
    )


@dataclass
class OwnerPrototypeSessionV2:
    """One bounded episode-to-adjudication interaction for owner testing."""

    record: LifePatternsRecordV2
    unsupported_fact_ids: set[str] = field(default_factory=set)
    _proposal_revision: int = 0

    @classmethod
    def synthetic(cls) -> OwnerPrototypeSessionV2:
        fact = EpisodeFactV2(
            fact_id="FACT-1",
            fact_lineage_id="LINEAGE-1",
            revision_index=0,
            episode_id="EP-1",
            assertion_type="positive_occurrence",
            actor="participant",
            proposition="The participant made a checklist before complex work.",
            source_provenance_ids=("SRC-EPISODE",),
        )
        episode = EpisodeV2(
            episode_id="EP-1",
            neutral_summary="A bounded planning episode.",
            source_provenance_ids=("SRC-EPISODE",),
            fact_ids=(fact.fact_id,),
        )
        return cls(
            LifePatternsRecordV2(
                contract_sha256=_CONTRACT_SHA,
                source_archive_sha256=_ARCHIVE_SHA,
                source_provenance=(
                    _source("SRC-EPISODE", "c"),
                    _source("SRC-PARTICIPANT", "d"),
                    _source("SRC-CORRECTION", "e"),
                ),
                episodes=(episode,),
                episode_facts=(fact,),
            )
        )

    def review_fact(
        self, fact_id: str, action: str, corrected_proposition: str | None = None
    ) -> None:
        """Accept, append a participant correction, or mark a proposed fact unsupported."""
        fact = next(row for row in self.record.episode_facts if row.fact_id == fact_id)
        if action == "accept":
            return
        if action == "not-supported":
            self.unsupported_fact_ids.add(fact_id)
            return
        if action != "correct" or not corrected_proposition:
            raise ValueError("action must be accept, correct, or not-supported")
        correction = fact.model_copy(
            update={
                "fact_id": f"{fact.fact_id}-R1",
                "revision_index": fact.revision_index + 1,
                "proposition": corrected_proposition,
                "supersedes_fact_id": fact.fact_id,
                "participant_correction_provenance_ids": ("SRC-CORRECTION",),
            }
        )
        episodes = tuple(
            episode.model_copy(update={"fact_ids": episode.fact_ids + (correction.fact_id,)})
            if episode.episode_id == correction.episode_id
            else episode
            for episode in self.record.episodes
        )
        self.record = self.record.model_copy(
            update={
                "episode_facts": self.record.episode_facts + (correction,),
                "episodes": episodes,
            }
        )

    def propose_pattern(
        self, wording: str = "I prepare before complex work."
    ) -> PatternProposalV2:
        current = tuple(
            row
            for row in self.record.episode_facts
            if row.fact_id not in self.unsupported_fact_ids
        )
        if not current:
            raise ValueError("a usable accepted fact is required before proposing a pattern")
        proposal_id = f"PROPOSAL-{self._proposal_revision}"
        # A refinement reuses the original preproposal anchor; it must not promote
        # postproposal evidence into preproposal evidence.
        link_id = "LINK-0" if self._proposal_revision else "LINK-0"
        proposal = PatternProposalV2(
            proposal_id=proposal_id,
            pattern_thread_id="THREAD-1",
            revision_index=self._proposal_revision,
            proposition=wording,
            question_text=f"Does this fit your experience: {wording}",
            evidence_link_ids=(link_id,),
            grounding_evidence_link_ids=(link_id,),
            previous_proposal_id=(
                f"PROPOSAL-{self._proposal_revision - 1}"
                if self._proposal_revision
                else None
            ),
        )
        link = PatternEvidenceLinkV2(
            evidence_link_id=link_id,
            proposal_id=proposal_id,
            episode_id=current[0].episode_id,
            fact_ids=(current[-1].fact_id,),
            role="preproposal_anchor",
            acquisition_phase="pre_first_proposal",
        )
        self.record = self.record.model_copy(
            update={
                "pattern_proposals": self.record.pattern_proposals + (proposal,),
                "pattern_evidence_links": (
                    self.record.pattern_evidence_links
                    if self._proposal_revision
                    else self.record.pattern_evidence_links + (link,)
                ),
            }
        )
        return proposal

    def adjudicate(self, decision: str, wording: str | None = None) -> None:
        proposal = self.record.pattern_proposals[-1]
        self.record = self.record.model_copy(
            update={
                "participant_adjudications": self.record.participant_adjudications
                + (
                    ParticipantAdjudicationV2(
                        adjudication_id=f"ADJ-{proposal.revision_index}",
                        proposal_id=proposal.proposal_id,
                        decision=decision,  # type: ignore[arg-type]
                        participant_response_provenance_ids=("SRC-PARTICIPANT",),
                        participant_approved_wording=wording,
                    ),
                )
            }
        )

    def refine_once(self, wording: str) -> PatternProposalV2:
        if self.record.participant_adjudications[-1].decision != "revise":
            raise ValueError("refinement requires a revise decision")
        self._proposal_revision += 1
        return self.propose_pattern(wording)

    def result(self) -> dict[str, object]:
        validate_life_patterns_record_v2(self.record, callbacks=_CALLBACKS)
        freeze = freeze_life_patterns_record_v2(self.record, callbacks=_CALLBACKS)
        projection = build_adapter_projection_v2(freeze, callbacks=_CALLBACKS)
        resolved = (
            freeze.payload.resolved_patterns[-1]
            if freeze.payload.resolved_patterns
            else None
        )
        return {
            "status": resolved.status if resolved else "provisional",
            "wording": resolved.participant_approved_wording if resolved else None,
            "scope_note": resolved.scope_note if resolved else None,
            "exception_note": resolved.exception_note if resolved else None,
            "evidence_fact_ids": tuple(row.fact.fact_id for row in projection.episode_facts),
            "freeze_payload_sha256": freeze.freeze_payload_sha256,
        }


def run_synthetic_owner_demo() -> list[str]:
    """Return a human-readable interaction transcript for local owner testing."""
    session = OwnerPrototypeSessionV2.synthetic()
    lines = [
        "Episode: A bounded planning episode.",
        "Proposed fact: The participant made a checklist before complex work.",
    ]
    session.review_fact("FACT-1", "correct", "The participant wrote a plan before complex work.")
    lines.append("Fact review: corrected (append-only revision created).")
    session.propose_pattern()
    lines.append(
        "Candidate question: Does this fit your experience: I prepare before complex work."
    )
    session.adjudicate("revise", "I plan before complex work.")
    session.refine_once("I plan before complex work.")
    session.adjudicate("accept", "I plan before complex work.")
    lines.append("Adjudication: accepted — I plan before complex work.")
    lines.append(f"Result: {session.result()['status']} (participant-adjudicated)")
    return lines


if __name__ == "__main__":
    print("\n".join(run_synthetic_owner_demo()))
