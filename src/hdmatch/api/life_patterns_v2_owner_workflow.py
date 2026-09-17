"""Revision-bound operations for the existing participant-authoritative interview.

This module owns workflow state, not research semantics. Exact browser recovery remains
an unvalidated working checkpoint. There is no disk persistence of private narratives.
"""

from __future__ import annotations

import uuid
from copy import deepcopy
from threading import Lock
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_context import interview_context
from .life_patterns_v2_owner_conversation import ConversationMove
from .life_patterns_v2_owner_natural_flow import NaturalFlowRecoverabilitySession
from .life_patterns_v2_owner_persistent import _canonical_sha
from .life_patterns_v2_owner_recoverability import _open_domains

Phase = Literal["awaiting_answer", "synthesis_review", "advancing", "paused", "bounded", "complete"]
Kind = Literal[
    "answer", "advance", "adjudicate", "investigate", "pause", "resume", "annotate", "reconstruct"
]
PHASES = {"awaiting_answer", "synthesis_review", "advancing", "paused", "bounded", "complete"}
QUESTION_MOVES = {"follow_up", "request_contrast", "boundary_question"}


class InterviewOperation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    operation_id: str = Field(min_length=1, max_length=100)
    expected_revision: int = Field(ge=0)
    kind: Kind
    payload: dict[str, Any] = Field(default_factory=dict)


class WorkflowConflict(ValueError):
    """The client must reconcile its current revision before a different mutation."""


class WorkflowSession(NaturalFlowRecoverabilitySession):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.phase: str = "awaiting_answer"
        self.resume_phase: str = "awaiting_answer"
        self.revision = 0
        self._operation_lock = Lock()
        self._receipts: dict[str, dict[str, Any]] = {}
        self.coverage_aggregate: dict[str, dict[str, Any]] = {}
        self.legacy_patterns: list[dict[str, Any]] = []
        self.legacy_answer_memory: list[str] = []
        self.question_admissions: list[dict[str, Any]] = []
        self.pattern_notes: list[dict[str, Any]] = []
        self.direct_proposal_ids: list[str] = []
        self.inference_note = ""
        self._admission_sink: list[dict[str, Any]] = []

    def evidence_context(self) -> dict[str, Any]:
        # The practical interview's whole source archive, not a different latest-N
        # window per planner. No source is silently truncated into a stronger claim.
        return {
            "admission_sink": self._admission_sink,
            "conversation": [dict(row) for row in self.conversation],
            "operative_facts": [
                fact.model_dump(mode="json") for fact in self.core.operative_facts()
            ],
            "patterns": self.patterns(),
            "participant_corrections": deepcopy(self.pattern_notes),
            "legacy_answer_memory_planning_only": list(self.legacy_answer_memory),
            "coverage_planning_only": list(self.coverage_aggregate.values()),
            "meaning": "Only participant source text and operative evidence establish claims. Rejected, disputed, inferred and planning-only material is not established participant evidence.",
        }

    def patterns(self) -> list[dict[str, Any]]:
        proposals = {p.proposal_id: p for p in self.core.record.pattern_proposals}
        sources = {row.get("turn_id"): row.get("text", "") for row in self.conversation}
        links = {link.evidence_link_id: link for link in self.core.record.pattern_evidence_links}
        facts = {fact.fact_id: fact for fact in self.core.record.episode_facts}
        rows: list[dict[str, Any]] = []
        for adj in self.core.record.participant_adjudications:
            prop = proposals[adj.proposal_id]
            if adj.decision == "revise":
                continue
            evidence_sources: set[str] = set()
            for link_id in prop.evidence_link_ids:
                for fact_id in links[link_id].fact_ids:
                    evidence_sources.update(facts[fact_id].source_provenance_ids)
            notes = [n for n in self.pattern_notes if n["proposal_id"] == prop.proposal_id]
            rows.append(
                {
                    "proposal_id": prop.proposal_id,
                    "thread_id": prop.pattern_thread_id,
                    "status": "disputed"
                    if notes
                    else {"accept": "accepted", "reject": "rejected"}.get(
                        adj.decision, "unresolved"
                    ),
                    "wording": adj.participant_approved_wording or prop.proposition,
                    "origin": "direct_report"
                    if prop.proposal_id in self.direct_proposal_ids
                    or prop.question_text.startswith("Participant directly stated")
                    else "inference",
                    "scope_note": adj.scope_note,
                    "exception_note": adj.exception_note,
                    "sources": [
                        {
                            "source_id": sid,
                            "text": sources.get(
                                sid.removeprefix("SRC-"),
                                "Source preserved in the evidence archive.",
                            ),
                        }
                        for sid in sorted(evidence_sources)
                    ],
                    "corrections": deepcopy(notes),
                }
            )
        known = {r["wording"] for r in rows}
        for i, row in enumerate(self.legacy_patterns):
            if row.get("wording") and row["wording"] not in known:
                rows.append(
                    {
                        **row,
                        "proposal_id": f"legacy-{i}",
                        "origin": "legacy_recovery",
                        "status": "disputed"
                        if any(n["proposal_id"] == f"legacy-{i}" for n in self.pattern_notes)
                        else row.get("status", "unresolved"),
                        "sources": [],
                        "corrections": [
                            n for n in self.pattern_notes if n["proposal_id"] == f"legacy-{i}"
                        ],
                    }
                )
        return rows

    def view(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "revision": self.revision,
            "phase": self.phase,
            "resume_phase": self.resume_phase,
            "conversation": [dict(row) for row in self.conversation],
            "patterns": self.patterns(),
            "aggregate_coverage": deepcopy(self.coverage_aggregate),
            "pattern_active": self._draft_move is not None,
            "pattern_proposition": self._active_proposition() if self._draft_move else None,
            "inference_note": self.inference_note,
            "recovery_quality": self.recovery_quality,
            "question_admission_log": deepcopy(self.question_admissions),
        }

    def _merge_progress(self, result: dict[str, Any]) -> None:
        report = result.get("coverage")
        if isinstance(report, dict):
            for row in report.get("assessments", []):
                if isinstance(row, dict) and row.get("domain_id"):
                    # Current assessments supersede stale ones, including after corrections.
                    self.coverage_aggregate[str(row["domain_id"])] = deepcopy(row)

    def _record_direct_reported_pattern(self, **kwargs: Any) -> dict[str, Any]:
        result = super()._record_direct_reported_pattern(**kwargs)
        self.direct_proposal_ids.append(self.core.record.pattern_proposals[-1].proposal_id)
        return result

    def _create_pattern(self, move: ConversationMove) -> None:
        reviewer = getattr(self.model, "review_pattern_candidate", None)
        if callable(reviewer):
            review = reviewer(move=move, evidence_context=self.evidence_context())
            if review.get("decision") == "context_only":
                raise ValueError("No supported person-specific formulation in this candidate")
            self.inference_note = str(review.get("inference_added", ""))
            self._direct_context_safe = review.get("decision") == "direct"
        else:
            self._direct_context_safe = True
        super()._create_pattern(move)

    def _direct_report_source(
        self, move: ConversationMove
    ) -> tuple[str, str, tuple[str, ...]] | None:
        if not getattr(self, "_direct_context_safe", True):
            return None
        return super()._direct_report_source(move)

    def _admit_final_question(self, result: dict[str, Any]) -> dict[str, Any]:
        gate = getattr(self.model, "_admit_in_thread_question", None)
        if result.get("move_type") not in QUESTION_MOVES or not callable(gate):
            return result
        candidate = ConversationMove(reply=str(result["reply"]), move_type=result["move_type"])
        admitted = gate(
            candidate=candidate,
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation[:-1]),
        )
        stopped = admitted.move_type == "topic_complete"
        reply = (
            "I do not see another useful question for this point right now."
            if stopped
            else admitted.reply
        )
        if self.conversation and self.conversation[-1].get("role") == "assistant":
            self.conversation[-1] = {**self.conversation[-1], "text": reply}
        self.pending_boundary_question = admitted.move_type == "boundary_question"
        if admitted.move_type == "request_contrast":
            self.awaiting_new_episode = True
            self.current_episode_id = None
        elif self.core.record.episodes:
            self.current_episode_id = self.core.record.episodes[-1].episode_id
            self.awaiting_new_episode = False
        result.update(reply=reply, move_type=admitted.move_type)
        audit = getattr(self.model, "pop_question_admission", lambda _reply: None)(admitted.reply)
        if audit is not None:
            result["question_admission"] = audit
        if stopped:
            result["no_useful_question"] = True
            # The person still has authority over a pending inference; stopping questions
            # must not accept it, discard it, or falsely mark coverage sufficient.
            result["topic_complete"] = self._draft_move is None
        return result

    def _advance(self) -> dict[str, Any]:
        domains = _open_domains(list(self.coverage_aggregate.values()))
        if not domains:
            self.phase = "complete"
            return {"complete": True, "opening": None}
        planner = getattr(self.model, "plan_continuation_question", None)
        if not callable(planner):
            raise ValueError("The configured interviewer cannot select a next question.")
        plan: dict[str, Any] = planner(
            open_domains=domains,
            aggregate_coverage=list(self.coverage_aggregate.values()),
            completed_results=self.patterns(),
            answer_memory=self.legacy_answer_memory,
            recent_conversation=tuple(self.conversation),
            operative_facts=self.core.operative_facts(),
        )
        if plan.get("no_useful_question") or not plan.get("opening"):
            self.phase = "bounded"
            return {**plan, "complete": False, "no_useful_question": True}
        self.current_episode_id = None
        self.awaiting_new_episode = True
        self.pending_boundary_question = False
        self.boundary_answered = False
        self.pattern_focus_established = True
        self._topic_complete_ready = False
        self.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "assistant",
                "text": str(plan["opening"]),
            }
        )
        self.phase = "awaiting_answer"
        return {**plan, "complete": False}

    def _apply(self, request: InterviewOperation) -> dict[str, Any]:
        kind, data = request.kind, request.payload
        if kind == "pause":
            if self.phase != "paused":
                self.resume_phase = self.phase
                self.phase = "paused"
            return {"paused": True}
        if kind == "resume":
            if self.phase == "paused":
                self.phase = self.resume_phase
            return {"resumed": True}
        if kind == "annotate":
            text = str(data.get("message", "")).strip()
            proposal_id = str(data.get("proposal_id", ""))
            if (
                not text
                or len(text) > 8000
                or proposal_id not in {p["proposal_id"] for p in self.patterns()}
            ):
                raise ValueError(
                    "Choose a saved pattern and supply a correction (up to 8000 characters)."
                )
            # An append-only correction annotation is not a second adjudication of a
            # historically accepted proposal. No implicit re-acceptance is manufactured.
            self.pattern_notes.append(
                {
                    "note_id": uuid.uuid4().hex,
                    "proposal_id": proposal_id,
                    "text": text,
                    "recorded_revision": self.revision + 1,
                    "status": "participant_correction_pending_reassessment",
                }
            )
            return {"correction_saved": True}
        if self.phase == "paused":
            raise WorkflowConflict("Resume the interview before submitting another response.")
        if kind == "advance":
            if self.phase not in {"advancing", "bounded"}:
                raise WorkflowConflict("This interview is not awaiting a next-question operation.")
            return self._advance()
        if kind == "reconstruct":
            from .life_patterns_v2_owner_import_resume import (
                _rebuild_visible_transcript_working_ledger,
            )

            result = _rebuild_visible_transcript_working_ledger(self)
        elif kind == "answer":
            if self.phase not in {"awaiting_answer", "synthesis_review", "bounded"}:
                raise WorkflowConflict("The interview is not awaiting an answer.")
            message = str(data.get("message", "")).strip()
            if not message or len(message) > 8000:
                raise ValueError("Write a response of 1–8000 characters.")
            result = super().turn(message)
        elif kind == "investigate":
            if self._draft_move is None:
                raise WorkflowConflict("There is no current inference to investigate.")
            result = super().continue_pattern()
        elif kind == "adjudicate":
            if self._draft_move is None:
                raise WorkflowConflict("There is no current inference to judge.")
            result = super().adjudicate(PatternAdjudicationRequest.model_validate(data))
            self.phase = "advancing"
            self.inference_note = ""
            return result
        else:
            raise ValueError("Unsupported operation")
        result = self._admit_final_question(result)
        self._merge_progress(result)
        self.phase = (
            "synthesis_review"
            if self._draft_move is not None
            else "advancing"
            if result.get("direct_pattern_recorded")
            or result.get("topic_complete")
            or result.get("move_type") == "topic_complete"
            else "awaiting_answer"
        )
        return result

    def execute(self, request: InterviewOperation) -> dict[str, Any]:
        if not self._operation_lock.acquire(blocking=False):
            raise WorkflowConflict("An operation is still processing. Reconcile before retrying.")
        try:
            signature = _canonical_sha(request.model_dump(mode="json"))
            receipt = self._receipts.get(request.operation_id)
            if receipt is not None:
                if receipt["request_sha256"] != signature:
                    raise WorkflowConflict(
                        "An operation identity cannot be reused with different content."
                    )
                return {
                    **deepcopy(receipt["result"]),
                    "replayed": True,
                    "view": self.view(),
                    "snapshot": self.recovery_snapshot(),
                }
            if request.expected_revision != self.revision:
                raise WorkflowConflict(
                    "The interview has changed. Restore the latest saved revision first."
                )
            before = self.recovery_snapshot()
            self._admission_sink.clear()
            try:
                with interview_context(self.evidence_context):
                    result = self._apply(request)
                self.revision += 1
                if result.get("question_admission"):
                    self.question_admissions.append(
                        {"revision": self.revision, **result["question_admission"]}
                    )
                self._receipts[request.operation_id] = {
                    "request_sha256": signature,
                    "revision": self.revision,
                    "result": deepcopy(result),
                }
                while len(self._receipts) > 256:
                    del self._receipts[next(iter(self._receipts))]
                return {
                    **result,
                    "operation_id": request.operation_id,
                    "view": self.view(),
                    "snapshot": self.recovery_snapshot(),
                }
            except Exception:
                self.restore_recovery_snapshot(before)
                raise
        finally:
            self._operation_lock.release()

    def recovery_snapshot(self) -> dict[str, Any]:
        body = super().recovery_snapshot()
        body.pop("recovery_sha256", None)
        body["workflow"] = {
            "version": 1,
            "phase": self.phase,
            "resume_phase": self.resume_phase,
            "revision": self.revision,
            "receipts": deepcopy(self._receipts),
            "coverage_aggregate": deepcopy(self.coverage_aggregate),
            "legacy_patterns": deepcopy(self.legacy_patterns),
            "legacy_answer_memory": list(self.legacy_answer_memory),
            "question_admissions": deepcopy(self.question_admissions),
            "pattern_notes": deepcopy(self.pattern_notes),
            "direct_proposal_ids": list(self.direct_proposal_ids),
            "inference_note": self.inference_note,
        }
        body["recovery_sha256"] = _canonical_sha(body)
        return body

    def restore_recovery_snapshot(self, snapshot: dict[str, Any]) -> None:
        super().restore_recovery_snapshot(snapshot)
        workflow = snapshot.get("workflow")
        if isinstance(workflow, dict):
            if workflow.get("version") != 1 or workflow.get("phase") not in PHASES:
                raise ValueError("Unsupported workflow checkpoint; the original file is preserved.")
            self.phase = str(workflow["phase"])
            self.resume_phase = str(workflow.get("resume_phase", "awaiting_answer"))
            if self.resume_phase not in PHASES - {"paused"}:
                raise ValueError("Invalid resume phase")
            self.revision = int(workflow.get("revision", 0))
            self._receipts = deepcopy(workflow.get("receipts", {}))
            self.coverage_aggregate = deepcopy(workflow.get("coverage_aggregate", {}))
            self.legacy_patterns = deepcopy(workflow.get("legacy_patterns", []))
            self.legacy_answer_memory = list(workflow.get("legacy_answer_memory", []))
            self.question_admissions = deepcopy(workflow.get("question_admissions", []))
            self.pattern_notes = deepcopy(workflow.get("pattern_notes", []))
            self.direct_proposal_ids = list(workflow.get("direct_proposal_ids", []))
            self.inference_note = str(workflow.get("inference_note", ""))
        else:
            # Migrate only the runtime phase, never the evidence. A later unanswered
            # question wins over historical adjudications. Ambiguity remains answerable.
            last = next(
                (r for r in reversed(self.conversation) if r.get("role") == "assistant"), {}
            )
            last_proposal = (
                self.core.record.pattern_proposals[-1]
                if self.core.record.pattern_proposals
                else None
            )
            just_adjudicated = bool(
                last_proposal
                and self.core.record.participant_adjudications
                and last.get("text") == last_proposal.question_text
            )
            self.phase = (
                "synthesis_review"
                if self._draft_move
                else "advancing"
                if self._topic_complete_ready or just_adjudicated
                else "awaiting_answer"
            )
            self._merge_progress({"coverage": self._last_progress_report})

    def recovery_status(self) -> dict[str, Any]:
        return {**super().recovery_status(), "workflow_phase": self.phase, "view": self.view()}

    def read_committed(self) -> dict[str, Any]:
        if not self._operation_lock.acquire(blocking=False):
            raise WorkflowConflict("The current operation has not committed yet.")
        try:
            return {"view": self.view(), "snapshot": self.recovery_snapshot()}
        finally:
            self._operation_lock.release()
