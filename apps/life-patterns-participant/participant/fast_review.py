"""Live adapter for the Pro-reviewed first-clarification stage.

The frozen full Engine remains the final evidence authority. No fast-path outcome
alone can authorize freeze/submission. All state is stored in the encrypted queue.
"""

from __future__ import annotations

import copy
from collections.abc import Callable

from .domain import Plan, import_record, new_state, utc, validate_plan
from .shadow_triage import privacy_safe_case_summary, run_shadow_fast_spec_path
from .store import canonical, digest
from .question_policy import activate

PROTOCOL = "fast-batch-v1"


def source_revision(candidate_sha256: str, history: list[dict]) -> str:
    """Private revision binding; never put this digest in public diagnostics."""
    return digest(canonical({"candidate": candidate_sha256, "history": history}))


def public_question(question: dict) -> dict:
    return {
        "route_id": question["route_id"],
        "route_type": question["route_type"],
        "question_text": question["text"],
        "antecedent_turn_ids": question.get("antecedent_turn_ids", []),
    }


class ProgressProvider:
    def __init__(self, provider, callback: Callable[[str], None] | None, *, fast: bool):
        self.provider, self.callback, self.fast = provider, callback, fast
        self.count = 0

    def __getattr__(self, name):
        return getattr(self.provider, name)

    def call(self, system, payload, schema, model, effort):
        self.count += 1
        if self.fast and self.count > 16:
            raise RuntimeError("fast_review_call_budget_exhausted")
        name = schema.__name__
        stage = None
        if "Admission" in name:
            stage = "gap_admission" if self.fast else "final_admission"
        elif "MatchAudit" in name:
            stage = "omission_audit"
        elif "Question" in name:
            stage = "question_render"
        elif not self.fast:
            stage = "final_synthesis"
        if stage and self.callback:
            self.callback(stage)
        return self.provider.call(system, payload, schema, model, effort)


def _source_state(job: dict, instrument: dict, version: str) -> dict:
    history = job.get("clarification_history") or []
    prior = job.get("worker_state")
    if prior is None:
        if history:
            raise RuntimeError("fast_history_without_saved_state")
        state = new_state(version, job["model"], job["effort"])
        activate(state)
        import_record(
            state,
            job["candidate_record"],
            "prior_json",
            instrument,
            job["candidate_record"].get("collection_mode", "unknown"),
        )
        state.update(
            consent=True, consented_at=utc(), phase="ready", gpt_review_answers_processed=0
        )
        state["fast_review"] = {
            "protocol": PROTOCOL,
            "stage": "triage",
            "pending_questions": [],
            "source_revision": source_revision(job["candidate_sha256"], []),
            "deferred_audit_pending": False,
            "final_review_completed": False,
        }
        return state
    state = copy.deepcopy(prior)
    activate(state)
    meta = state.get("fast_review") or {}
    if meta.get("protocol") != PROTOCOL or state.get("instrument_version") != version:
        raise RuntimeError("fast_review_saved_state_version_mismatch")
    processed = int(state.get("gpt_review_answers_processed", 0))
    if processed > len(history) or meta.get("source_revision") != source_revision(
        job["candidate_sha256"], history[:processed]
    ):
        raise RuntimeError("fast_review_source_revision_mismatch")
    incoming = history[processed:]
    if not incoming:
        return state
    pending = meta.get("pending_questions") or []
    if state["phase"] != "awaiting_answer" or not (1 <= len(incoming) <= len(pending)):
        raise RuntimeError("fast_review_batch_history_mismatch")
    # The queue has already bound IDs/order atomically. Verify exact saved wording
    # again at the model boundary, including partial-batch early reconciliation.
    for index, item in enumerate(incoming):
        question = pending[index]
        if (
            item.get("question_text") != question["text"]
            or item.get("route_id") != question["route_id"]
        ):
            raise RuntimeError("fast_review_answer_question_mismatch")
        tid = f"review-answer-{processed + index + 1:04d}"
        if any(turn["turn_id"] == tid for turn in state["turns"]):
            raise RuntimeError("fast_review_duplicate_answer")
        skipped = item.get("answer_status") == "skipped"
        state["turns"].append(
            {
                "turn_id": tid,
                "sequence": len(state["turns"]) + 1,
                "turn_source": "import-fast-review-clarification",
                "canonical_question_id": question["route_id"],
                "route_type": question["route_type"],
                "id_basis": "server_admitted_question",
                "question_wording_status": "server_admitted_exact",
                "question_text": question["text"],
                "answer_text": None if skipped else item["answer_text"],
                "answer_status": "skipped" if skipped else "unassessed",
                "antecedent_turn_ids": question.get("antecedent_turn_ids", []),
                "conditions": [],
                "corrections": [],
                "process_feedback": [],
                "correction_of": None,
                "recorded_at": utc(),
            }
        )
        if skipped:
            state["dispositions"][tid] = {
                "turn_id": tid,
                "status": "skipped",
                "reason": "Participant explicitly skipped.",
            }
    state.update(gpt_review_answers_processed=len(history), phase="ready", pending_question=None)
    meta.update(
        pending_questions=[],
        stage="triage",
        source_revision=source_revision(job["candidate_sha256"], history),
        final_review_completed=False,
    )
    # No old proposed question or cached audit is applied to this newer source.
    meta["deferred_audit_pending"] = True
    return state


def run_fast_review(
    job: dict,
    provider,
    instrument: dict,
    version: str,
    legacy_run: Callable,
    progress: Callable[[str], None] | None = None,
):
    history = job.get("clarification_history") or []
    prior = job.get("worker_state") or {}
    prior_meta = prior.get("fast_review") or {}
    revision = source_revision(job["candidate_sha256"], history)
    # After full synthesis starts, preserve the Engine's own evidence/clarification
    # continuation mechanics. Existing legacy jobs never enter this adapter.
    if prior_meta.get("stage") == "legacy_continuation":
        processed = int(prior.get("gpt_review_answers_processed", 0))
        if processed > len(history) or prior_meta.get("source_revision") != source_revision(
            job["candidate_sha256"], history[:processed]
        ):
            raise RuntimeError("fast_review_source_revision_mismatch")
        if progress:
            progress("final_synthesis")
        wrapped = ProgressProvider(provider, progress, fast=False)
        status, receipt, state, question = legacy_run(job, provider=wrapped)
        if state:
            meta = state.setdefault("fast_review", copy.deepcopy(prior_meta))
            meta.update(source_revision=revision, final_review_completed=status == "ready")
            meta["pending_questions"] = []
        receipt.update(
            review_protocol=PROTOCOL,
            source_revision=revision,
            final_review_completed=status == "ready",
        )
        return status, receipt, state, question
    state = _source_state(job, instrument, version)
    meta = state["fast_review"]
    if meta["stage"] == "final_synthesis":
        if meta["source_revision"] != revision or meta.get("deferred_audit_pending"):
            raise RuntimeError("final_synthesis_source_not_reconciled")
        if progress:
            progress("final_synthesis")
        wrapped = ProgressProvider(provider, progress, fast=False)
        prepared = dict(job, worker_state=state)
        status, receipt, saved, question = legacy_run(prepared, provider=wrapped)
        if saved:
            saved["fast_review"].update(
                stage="legacy_continuation",
                source_revision=revision,
                final_review_completed=status == "ready",
            )
        receipt.update(
            review_protocol=PROTOCOL,
            source_revision=revision,
            final_review_completed=status == "ready",
        )
        return status, receipt, saved, question
    if progress:
        progress("initial_triage" if not history else "reconciliation")
    result = run_shadow_fast_spec_path(
        state,
        instrument,
        ProgressProvider(provider, progress, fast=True),
        model=job["model"],
        effort=job["effort"],
    )
    summary = privacy_safe_case_summary("review", state, result)
    receipt = {
        "route": "subscription-authenticated local Codex CLI",
        "model": job["model"],
        "effort": job["effort"],
        "instrument_version": version,
        "question_policy": state["question_policy"],
        "paid_api": False,
        "production_backend": False,
        "review_protocol": PROTOCOL,
        "round": job.get("round", 0),
        "source_revision": revision,
        "semantic_calls": summary["semantic_calls"],
        "finished_at": utc(),
        "final_review_completed": False,
        "triage_outcome": summary["shadow_outcome"],
    }
    meta.update(
        source_revision=revision,
        deferred_audit_pending=summary["match_audit_pending"],
        final_review_completed=False,
    )
    if summary["ready_question_route_ids"]:
        questions = [
            result["final_questions"][rid].model_dump()
            for rid in summary["ready_question_route_ids"]
        ]
        for question in questions:
            validate_plan(
                Plan(
                    action="ask",
                    dispositions=[],
                    evidence=[],
                    question=question,
                    control_quote=None,
                    addressed_routes=[],
                    source_review_complete=False,
                    reason="fast_admitted_question",
                ),
                state,
                instrument,
                [],
            )
        state.update(phase="awaiting_answer", pending_question=questions[0])
        meta["pending_questions"] = questions
        return "clarification_needed", receipt, state, public_question(questions[0])
    # A genuine no-question result continues into full evidence coding. Any
    # unresolved fast result falls back to the unchanged full reviewer, NOT ready.
    meta.update(stage="final_synthesis", pending_questions=[], deferred_audit_pending=False)
    meta["full_review_fallback_reason"] = summary["shadow_outcome"]
    state.update(phase="ready", pending_question=None)
    receipt["next_stage"] = "final_synthesis"
    return "queued", receipt, state, None
