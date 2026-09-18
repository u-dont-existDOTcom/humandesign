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
from .life_patterns_v2_owner_dialogue import ParticipantInput, RepairFrontier
from .life_patterns_v2_owner_natural_flow import NaturalFlowRecoverabilitySession
from .life_patterns_v2_owner_persistent import _canonical_sha
from .life_patterns_v2_owner_recoverability import _open_domains, _normalize_recoverability_coverage

Phase = Literal["awaiting_answer", "synthesis_review", "advancing", "paused", "bounded", "complete"]
Kind = Literal[
    "answer", "advance", "adjudicate", "investigate", "pause", "resume", "annotate", "reconstruct", "review_draft", "review_repair"
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
        self.model_calls: list[dict[str, Any]] = []
        self.input_routes: list[dict[str, Any]] = []
        self.process_turn_ids: set[str] = set()
        self.active_domain_id: str | None = None
        self.repair_pending = False
        self.formulation_reviews: list[dict[str, Any]] = []
        self.retired_drafts: list[dict[str, Any]] = []
        self._suppressed_formulation: str | None = None
        self.draft_needs_review = False
        self._reviewing_emission = False
        self.reported_summaries: list[dict[str, Any]] = []
        self._reported_summary_recorded = False
        self.continue_current_focus = False
        self.repair_frontier: dict[str, Any] | None = None
        self.repair_needs_review = False

    def evidence_context(self) -> dict[str, Any]:
        # The practical interview's whole source archive, not a different latest-N
        # window per planner. No source is silently truncated into a stronger claim.
        return {
            "admission_sink": self._admission_sink,
            "model_call_sink": self.model_calls,
            "active_domain_id": self.active_domain_id,
            "workflow_phase": self.phase,
            "continue_current_focus": self.continue_current_focus,
            "repair_frontier": deepcopy(self.repair_frontier),
            "repair_pending": self.repair_pending,
            "pending_inference": self._active_proposition() if self._draft_move else None,
            "evidence_conversation": self._evidence_conversation(),
            "legacy_coverage_planning_only": self._legacy_coverage(),
            "conversation": [dict(row) for row in (self.conversation[:-1] if self._reviewing_emission else self.conversation)],
            "operative_facts": [
                fact.model_dump(mode="json") for fact in self._planning_facts()
            ],
            "patterns": self.patterns(),
            "participant_corrections": deepcopy(self.pattern_notes),
            "legacy_answer_memory_planning_only": list(self.legacy_answer_memory),
            "coverage_planning_only": list(self.coverage_aggregate.values()),
            "meaning": "Only participant source text and operative evidence establish claims. Rejected, disputed, inferred and planning-only material is not established participant evidence.",
        }

    def _planning_facts(self) -> tuple[Any, ...]:
        excluded_sources = {f"SRC-{tid}" for tid in self.process_turn_ids}
        return tuple(f for f in self.core.operative_facts()
                     if not (set(f.source_provenance_ids) & excluded_sources))

    def _evidence_conversation(self) -> list[dict[str, str]]:
        routes = {r["turn_id"]: r for r in self.input_routes}
        rows = []
        for row in self.conversation:
            if row["turn_id"] in self.process_turn_ids:
                continue
            route = routes.get(row["turn_id"])
            text = "\n".join(route["evidence_quotes"]) if route else row["text"]
            rows.append({**row, "text": text})
        return rows

    def _legacy_coverage(self) -> list[dict[str, Any]]:
        # Planning memory is not a recovered scientific ledger or a coverage score.
        rows = []
        for pattern in self.legacy_patterns:
            for row in (pattern.get("coverage") or {}).get("assessments", []):
                if row.get("status") in {"partial", "sufficient"}:
                    rows.append({"domain_id": row["domain_id"], "status": row["status"],
                                 "reason": row.get("reason", ""), "source_available": False})
        return rows

    def coverage_report(self) -> dict[str, Any]:
        facts = self._planning_facts()
        assessor = getattr(self.model, "assess_required_coverage", None)
        raw = assessor(operative_facts=facts, recent_conversation=tuple(self._evidence_conversation())) if callable(assessor) else {}
        return _normalize_recoverability_coverage(raw, operative_facts=facts)

    def _participant_user_turn_count(self) -> int:
        return sum(r["role"] == "user" and r["turn_id"] not in self.process_turn_ids
                   for r in self.conversation)

    def _retire_draft(self, reason: str) -> None:
        if self._draft_move is not None:
            self.retired_drafts.append({"revision": self.revision + 1,
                                       "reason": reason,
                                       "draft": self._draft_move.model_dump(mode="json"),
                                       "adjudicated": False})
        self._draft_move = None
        self.inference_note = ""
        self.draft_needs_review = False

    def _append_reply(self, reply: str, move_type: str, **extra: Any) -> dict[str, Any]:
        self.conversation.append({"turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                                  "role": "assistant", "text": reply})
        return {"reply": reply, "move_type": move_type,
                "pattern_active": self._draft_move is not None,
                "pattern_proposition": self._active_proposition() if self._draft_move else None,
                "episode_count": len(self.core.record.episodes), **extra}

    def _emit_move(self, move: Any) -> dict[str, Any]:
        if move.move_type == "topic_complete":
            # Stopping questions is neither measurement sufficiency nor adjudication.
            return self._append_reply(
                "I do not see a useful further question about that interpretation. It remains unjudged."
                if self._draft_move else "We can leave this point here for now.",
                "follow_up" if self._draft_move else "topic_complete",
                no_useful_question=True, topic_complete=self._draft_move is None,
                skip_question_admission=True)
        if move.move_type == "surface_hypothesis":
            self._suppressed_formulation = None
            self._auto_recorded_direct_result = None
            self._reported_summary_recorded = False
            self._create_pattern(move)
            if self._suppressed_formulation:
                reason = self._suppressed_formulation
                return self._append_reply(
                    "That point is already recorded; I am not adding it again."
                    if reason == "duplicate" else "I do not have a supported new interpretation to add here.",
                    "follow_up" if self._draft_move else "topic_complete",
                    formulation_suppressed=reason, topic_complete=self._draft_move is None,
                    skip_question_admission=True)
            if self._reported_summary_recorded:
                return self._append_reply("Saved a summary of what you reported.", "reported_summary",
                                          reported_summary_recorded=True)
            if self._auto_recorded_direct_result is not None:
                result = dict(self._auto_recorded_direct_result)
                self._auto_recorded_direct_result = None
                result.update(self._append_reply("Saved that pattern from your own words.", "direct_pattern"))
                return result
            # A draft's reply must not falsely announce completion or claim it was saved.
            return self._append_reply("Does this possible connection fit your experience?", "surface_hypothesis")
        self.pending_boundary_question = move.move_type == "boundary_question"
        if move.move_type == "request_contrast":
            self.awaiting_new_episode = True
            self.current_episode_id = None
        return self._append_reply(move.reply, move.move_type)

    def _handle_answer(self, message: str) -> dict[str, Any]:
        router = getattr(self.model, "route_participant_turn", None)
        route = ParticipantInput.model_validate(router(message=message, evidence_context=self.evidence_context())) if callable(router) else ParticipantInput(
            kind="answer", evidence_quotes=[message], repair_reply="",
            withdraw_pending_inference=False, historical_process_turn_ids=[])
        route.check_source(message)
        known_user_ids = {r["turn_id"] for r in self.conversation if r["role"] == "user"}
        if not set(route.historical_process_turn_ids) <= known_user_ids:
            raise ValueError("Input routing cited an unknown historical source")
        self.process_turn_ids.update(route.historical_process_turn_ids)
        if route.kind in {"repair", "skip", "pause"}:
            turn_id = f"TURN-{uuid.uuid4().hex[:10].upper()}"
            self.conversation.append({"turn_id": turn_id, "role": "user", "text": message})
            self.input_routes.append({"turn_id": turn_id, **route.model_dump(mode="json")})
            self.process_turn_ids.add(turn_id)
            if route.kind == "pause":
                self.resume_phase, self.phase = self.phase, "paused"
                return self._append_reply("The interview is paused here.", "conversation_control", process_only=True)
            if route.kind == "skip":
                self._retire_draft("participant_deferred_topic_without_adjudication")
                self.phase = "advancing"
                self.repair_pending = False
                return self._append_reply("We can leave this topic open and move on.", "conversation_control", process_only=True)
            if route.withdraw_pending_inference:
                self._retire_draft("withdrawn_during_conversation_repair")
            assert route.repair_frontier is not None
            self._set_repair_frontier(route.repair_frontier)
            reply = route.repair_reply
            if route.repair_frontier.question:
                reply += "\n\n" + route.repair_frontier.question
            return self._append_reply(reply, "conversation_repair", process_only=True)

        self.repair_pending = route.kind == "mixed"
        self.repair_frontier = None
        self.continue_current_focus = False
        if route.withdraw_pending_inference:
            self._retire_draft("participant_corrected_unsupported_draft")
        if not self.pattern_focus_established:
            result = self._start_or_redirect_pattern(message)
            user = next(r for r in reversed(self.conversation) if r["role"] == "user")
            self.input_routes.append({"turn_id": user["turn_id"], **route.model_dump(mode="json")})
            return result
        turn_id = f"TURN-{uuid.uuid4().hex[:10].upper()}"
        self.conversation.append({"turn_id": turn_id, "role": "user", "text": message})
        self.input_routes.append({"turn_id": turn_id, **route.model_dump(mode="json")})
        if self.pending_boundary_question:
            self.boundary_answered = True
            self.pending_boundary_question = False
        extraction = self.model.extract_turn(
            message="\n".join(route.evidence_quotes), current_episode_id=self.current_episode_id,
            operative_facts=self._planning_facts(), recent_conversation=tuple(self._evidence_conversation()))
        self._apply_extraction(extraction=extraction, turn_id=turn_id, message=message,
                               start_new_episode=self.awaiting_new_episode or self.current_episode_id is None)
        move = self._plan_current_focus()
        # A draft grounded in superseded or quarantined facts cannot remain operative.
        if self._draft_move and not set(self._draft_move.evidence_fact_ids) <= {f.fact_id for f in self._planning_facts()}:
            self._retire_draft("source_corrected_or_quarantined")
        result = self._emit_move(move)
        if route.kind == "mixed":
            result["repair_acknowledgement"] = route.repair_reply
        return result

    def _set_repair_frontier(self, frontier: RepairFrontier) -> None:
        if frontier.next_action == "await_judgment" and self._draft_move is None:
            raise ValueError("Cannot await judgment of an absent inference")
        self.repair_frontier = frontier.model_dump(mode="json")
        self.repair_needs_review = False
        self.repair_pending = frontier.next_action != "continue_interview"
        self.continue_current_focus = frontier.next_action == "continue_interview"
        self.phase = ("advancing" if self.continue_current_focus else
                      "synthesis_review" if self._draft_move else "awaiting_answer")

    def _plan_current_focus(self) -> Any:
        kwargs: dict[str, Any] = {"current_episode_id": self.current_episode_id,
                                 "episodes": self.core.record.episodes,
                                 "operative_facts": self._planning_facts(),
                                 "recent_conversation": tuple(self.conversation)}
        refiner = getattr(self.model, "plan_refinement_turn", None)
        if self._draft_move and callable(refiner):
            return refiner(current_proposition=self._active_proposition(), refinement_mode="answer", **kwargs)
        return self.model.plan_turn(boundary_answered=self.boundary_answered, **kwargs)

    def _save_report_summary(self, move: ConversationMove) -> None:
        facts = {f.fact_id: f for f in self._planning_facts()}
        source_ids = sorted({sid for fid in move.evidence_fact_ids
                             for sid in (*facts[fid].source_provenance_ids,
                                         *facts[fid].participant_correction_provenance_ids)})
        sources = {"SRC-" + row["turn_id"]: row["text"] for row in self.conversation if row["role"] == "user"}
        if not source_ids or not all(sid in sources for sid in source_ids):
            self._suppressed_formulation = "summary_source_unavailable"
            return
        wording = str(move.hypothesis_proposition)
        self.reported_summaries.append({
            "summary_id": "SUMMARY-" + uuid.uuid4().hex,
            "wording": wording, "evidence_fact_ids": list(move.evidence_fact_ids),
            "source_provenance_ids": source_ids, "recorded_revision": self.revision + 1,
            "authorship": "model_summary_of_participant_reports", "participant_adjudicated": False})
        if self._draft_move and self._draft_move.hypothesis_proposition == wording:
            self._retire_draft("reclassified_as_source_summary_without_adjudication")
        self._reported_summary_recorded = True
        self.continue_current_focus = self._draft_move is None

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
        for summary in self.reported_summaries:
            notes = [n for n in self.pattern_notes if n["proposal_id"] == summary["summary_id"]]
            rows.append({"proposal_id": summary["summary_id"], "summary_id": summary["summary_id"],
                         "wording": summary["wording"], "origin": "source_summary",
                         "status": "disputed" if notes else "reported", "participant_adjudicated": False,
                         "sources": [{"source_id": sid, "text": sources.get(sid.removeprefix("SRC-"), "Source unavailable.")}
                                     for sid in summary["source_provenance_ids"]],
                         "corrections": deepcopy(notes)})
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
            "active_domain_id": self.active_domain_id,
            "repair_pending": self.repair_pending,
            "draft_needs_review": self.draft_needs_review,
            "repair_needs_review": self.repair_needs_review,
            "continue_current_focus": self.continue_current_focus,
            "repair_frontier": deepcopy(self.repair_frontier),
            "model_profile": getattr(self.model, "model_profile", lambda: {})(),
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
        wording = (move.hypothesis_proposition or "").strip()
        normalized = " ".join(wording.casefold().split())
        patterns = self.patterns()
        if any(" ".join(p["wording"].casefold().split()) == normalized for p in patterns):
            self._suppressed_formulation = "duplicate"
            return
        if not set(move.evidence_fact_ids) <= {f.fact_id for f in self._planning_facts()}:
            self._suppressed_formulation = "unsupported_source"
            return
        reviewer = getattr(self.model, "review_pattern_candidate", None)
        if callable(reviewer):
            review = reviewer(move=move, evidence_context=self.evidence_context())
            self.formulation_reviews.append({"revision": self.revision + 1,
                                             "candidate": wording, "review": deepcopy(review)})
            if review.get("decision") == "duplicate":
                if review.get("related_proposal_id") not in {p["proposal_id"] for p in patterns}:
                    raise ValueError("Duplicate review did not identify an existing pattern")
                self._suppressed_formulation = "duplicate"
                return
            if review.get("decision") == "context_only":
                self._suppressed_formulation = "unsupported_or_context_only"
                return
            if "inference_quote" in review and review.get("decision") == "inference":
                anchor = str(review.get("inference_quote", ""))
                if not anchor.strip() or anchor not in wording or not str(review.get("inference_added", "")).strip():
                    self._suppressed_formulation = "review_does_not_match_candidate"
                    return
            self.inference_note = str(review.get("inference_added", ""))
            self._direct_context_safe = review.get("decision") == "direct"
            if self._direct_context_safe and self._direct_report_source(move) is None:
                self._save_report_summary(move)
                self.draft_needs_review = False
                return
            if review.get("decision") not in {"direct", "inference"}:
                raise ValueError("The formulation review did not return a supported decision")
        else:
            self._direct_context_safe = True
        super()._create_pattern(move)
        self.draft_needs_review = False

    def _direct_report_source(
        self, move: ConversationMove
    ) -> tuple[str, str, tuple[str, ...]] | None:
        # Directness is original-source authorship plus semantic endorsement, not
        # whichever assertion label an extractor happened to choose.
        if not getattr(self, "_direct_context_safe", True):
            return None
        wording = (move.hypothesis_proposition or "").strip()
        ids = tuple(dict.fromkeys(move.evidence_fact_ids))
        facts = {f.fact_id: f for f in self._planning_facts()}
        if not wording or not ids or not set(ids) <= facts.keys():
            return None
        source_ids = {r.source_provenance_id for r in self.core.record.source_provenance}
        for row in reversed(self.conversation):
            source_id = "SRC-" + row["turn_id"]
            if row["role"] != "user" or wording not in row["text"] or source_id not in source_ids:
                continue
            if not all(source_id in facts[fid].source_provenance_ids for fid in ids):
                continue
            admitted = next((r for r in self.input_routes if r["turn_id"] == row["turn_id"]), None)
            if admitted and not any(wording in quote for quote in admitted["evidence_quotes"]):
                continue
            return wording, source_id, ids
        return None

    def _admit_final_question(self, result: dict[str, Any]) -> dict[str, Any]:
        gate = getattr(self.model, "_admit_in_thread_question", None)
        if result.get("skip_question_admission") or result.get("move_type") not in QUESTION_MOVES or not callable(gate):
            return result
        candidate = ConversationMove(reply=str(result["reply"]), move_type=result["move_type"])
        self._reviewing_emission = True
        try:
            admitted = gate(candidate=candidate, operative_facts=self._planning_facts(),
                            recent_conversation=tuple(self.conversation[:-1]))
        finally:
            self._reviewing_emission = False
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
        if self.continue_current_focus:
            self.continue_current_focus = False
            self.repair_pending = False
            self.repair_frontier = None
            result = self._admit_final_question(self._emit_move(self._plan_current_focus()))
            self._set_result_phase(result)
            return {**result, "complete": False}
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
            operative_facts=self._planning_facts(),
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
        self.active_domain_id = str(plan.get("primary_domain_id") or "") or None
        self.repair_pending = False
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
        if self.repair_needs_review and kind in {"answer", "advance", "adjudicate", "investigate"}:
            raise WorkflowConflict("The saved repair frontier must be recovered first.")
        if kind == "review_repair":
            if not self.repair_needs_review:
                return {"repair_checked": True}
            recover = getattr(self.model, "recover_repair_frontier", None)
            if not callable(recover):
                raise ValueError("The interviewer cannot recover the legacy repair frontier")
            frontier = RepairFrontier.model_validate(recover(evidence_context=self.evidence_context()))
            self._set_repair_frontier(frontier)
            if frontier.question and (not self.conversation or frontier.question not in self.conversation[-1]["text"]):
                return self._append_reply(frontier.question, "conversation_repair", process_only=True, repair_checked=True)
            return {"repair_checked": True}
        if self.draft_needs_review and kind in {"adjudicate", "investigate"}:
            raise WorkflowConflict("The restored draft must be checked before judgment. Refresh to continue safely.")
        if kind == "review_draft":
            if not self.draft_needs_review or self._draft_move is None:
                self.draft_needs_review = False
                return {"draft_checked": True}
            old = self._draft_move
            self._suppressed_formulation = None
            self._auto_recorded_direct_result = None
            self._reported_summary_recorded = False
            self._create_pattern(old)
            if self._suppressed_formulation:
                reason = self._suppressed_formulation
                self._retire_draft("restored_draft_" + reason)
                self.phase = "advancing"
                return self._append_reply(
                    "The restored draft was not a supported new interpretation. I have removed it without changing your saved patterns.",
                    "conversation_control", draft_checked=True)
            self.draft_needs_review = False
            self.phase = "synthesis_review" if self._draft_move else "advancing"
            return {"draft_checked": True}
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
            result = self._handle_answer(message)
            if result.get("process_only"):
                return result
        elif kind == "investigate":
            if self._draft_move is None:
                raise WorkflowConflict("There is no current inference to investigate.")
            self.conversation.append({"turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                                      "role": "user", "text": "Keep investigating."})
            self.process_turn_ids.add(self.conversation[-1]["turn_id"])
            refiner = getattr(self.model, "plan_refinement_turn", None)
            if not callable(refiner):
                raise ValueError("The configured interviewer does not support refinement")
            move = refiner(
                current_proposition=self._active_proposition(), refinement_mode="continue",
                current_episode_id=self.current_episode_id, episodes=self.core.record.episodes,
                operative_facts=self._planning_facts(), recent_conversation=tuple(self.conversation))
            result = self._emit_move(move)
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
        acknowledgement = result.pop("repair_acknowledgement", "")
        if acknowledgement:
            result["reply"] = acknowledgement + "\n\n" + result["reply"]
            self.conversation[-1]["text"] = result["reply"]
        # Pure feedback never reaches this coverage path.
        result = self._attach_periodic_progress(result, force=bool(result.get("direct_pattern_recorded") or result.get("pattern_active")))
        self._merge_progress(result)
        self._set_result_phase(result)
        return result

    def _set_result_phase(self, result: dict[str, Any]) -> None:
        self.phase = (
            "synthesis_review" if self._draft_move is not None else
            "advancing" if result.get("direct_pattern_recorded") or result.get("reported_summary_recorded")
            or result.get("topic_complete") or result.get("move_type") == "topic_complete"
            else "awaiting_answer")

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
            "semantic_policy_version": 4,
            "reported_summaries": deepcopy(self.reported_summaries),
            "active_domain_id": self.active_domain_id,
            "repair_pending": self.repair_pending,
            "draft_needs_review": self.draft_needs_review,
            "repair_needs_review": self.repair_needs_review,
            "continue_current_focus": self.continue_current_focus,
            "repair_frontier": deepcopy(self.repair_frontier),
            "input_routes": deepcopy(self.input_routes),
            "process_turn_ids": sorted(self.process_turn_ids),
            "formulation_reviews": deepcopy(self.formulation_reviews),
            "retired_drafts": deepcopy(self.retired_drafts),
            "model_calls": deepcopy(self.model_calls),
            "model_profile": getattr(self.model, "model_profile", lambda: {})(),
            "process_exclusion_policy": "Interview-process facts are excluded from current elicitation and proposals; original historical archive is preserved.",
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
            self.active_domain_id = workflow.get("active_domain_id")
            self.repair_pending = bool(workflow.get("repair_pending", False))
            self.input_routes = deepcopy(workflow.get("input_routes", []))
            self.process_turn_ids = set(workflow.get("process_turn_ids", []))
            self.formulation_reviews = deepcopy(workflow.get("formulation_reviews", []))
            self.retired_drafts = deepcopy(workflow.get("retired_drafts", []))
            self.model_calls = deepcopy(workflow.get("model_calls", []))
            self.reported_summaries = deepcopy(workflow.get("reported_summaries", []))
            self.continue_current_focus = bool(workflow.get("continue_current_focus", False))
            self.repair_frontier = deepcopy(workflow.get("repair_frontier"))
            self.repair_needs_review = bool(workflow.get("repair_needs_review", False)) or (
                workflow.get("semantic_policy_version", 1) < 4 and self.repair_pending
                and (self.resume_phase if self.phase == "paused" else self.phase)
                in {"awaiting_answer", "synthesis_review"})
            self.draft_needs_review = bool(self._draft_move) and (
                workflow.get("semantic_policy_version", 1) < 4 or bool(workflow.get("draft_needs_review")))
            if not self.active_domain_id:
                for receipt in reversed(list(self._receipts.values())):
                    domain = receipt.get("result", {}).get("primary_domain_id")
                    if domain:
                        self.active_domain_id = str(domain)
                        break
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
            self.draft_needs_review = self._draft_move is not None

    def recovery_status(self) -> dict[str, Any]:
        return {**super().recovery_status(), "workflow_phase": self.phase, "view": self.view()}

    def read_committed(self) -> dict[str, Any]:
        if not self._operation_lock.acquire(blocking=False):
            raise WorkflowConflict("The current operation has not committed yet.")
        try:
            return {"view": self.view(), "snapshot": self.recovery_snapshot()}
        finally:
            self._operation_lock.release()
