"""Participant check-back guidance. Pilot estimates are not completion promises."""

from __future__ import annotations

import math
import time

# Seconds from stage start. Broad ranges deliberately reflect limited pilot data.
# First batch: two 81-turn runs at 112/114s. Legacy initial full review: ~488s.
# Omission-only observed ~273s; rendering/review together ~25s. No SLA implied.
STAGES = {
    "initial_triage": ("Checking for useful clarifications", 60, 180, 180),
    "reconciliation": ("Rechecking your clarification answers", 60, 240, 180),
    "gap_admission": ("Independently checking proposed clarifications", 15, 90, 60),
    "question_render": ("Preparing and checking question wording", 15, 90, 60),
    "omission_audit": ("Checking for overlooked or conflicting answers", 120, 480, 300),
    "final_synthesis": ("Preparing the full evidence review", 300, 720, 600),
    "final_admission": ("Independently checking the evidence review", 60, 180, 180),
    "legacy_review": ("Reviewing the complete interview", 360, 720, 600),
    "legacy_followup": ("Reviewing a clarification answer", 60, 240, 180),
}


# Do not describe extrapolated integrated-stage ranges as measured quantiles.
ESTIMATE_BASIS = {
    "initial_triage": "limited pilot; two 81-turn first-batch runs around 112-114 seconds",
    "gap_admission": "limited pilot stage timings; broad planning range, not a deadline",
    "question_render": "limited pilot wording-stage timings; retries can take longer",
    "reconciliation": "provisional; informed by legacy follow-up timings, not calibrated batch timings",
    "omission_audit": "provisional; informed by a prior omission-audit run, not a calibrated distribution",
    "final_synthesis": "provisional; informed by legacy full-review timings, not a measured synthesis-only range",
    "final_admission": "provisional; informed by earlier independent-review timings",
    "legacy_review": "limited pilot; prior complete-review observation around eight minutes",
    "legacy_followup": "limited pilot; earlier follow-up observations around one to two minutes",
}


def review_guidance(payload: dict, *, now: float | None = None) -> dict:
    now = time.time() if now is None else now
    status = payload["status"]
    fast = payload.get("review_protocol") == "fast-batch-v1"
    default = (
        ("initial_triage" if not payload.get("round") else "reconciliation")
        if fast
        else ("legacy_review" if not payload.get("round") else "legacy_followup")
    )
    stage = payload.get("review_stage") or default
    if stage not in STAGES:
        stage = default
    label, lower, upper, check = STAGES[stage]
    cycle = float(payload.get("cycle_queued_at_unix") or payload.get("created_at_unix") or now)
    started = float(payload.get("stage_started_at_unix") or cycle)
    age = max(0, int(now - started))
    heartbeat = payload.get("worker_heartbeat_at_unix")
    heartbeat_age = max(0, int(now - float(heartbeat))) if heartbeat is not None else None
    waiting = status in {"queued", "processing"}
    overdue = waiting and status == "processing" and age > upper
    stale = status == "processing" and (heartbeat_age is None or heartbeat_age > 90)
    queue_delayed = status == "queued" and now - cycle > 180
    remaining = [max(0, lower - age), max(0, upper - age)] if status == "processing" else None
    recommended = 0
    note = ""
    if status == "queued":
        recommended = check if not queue_delayed else 300
        note = (
            "Your source is saved, but the reviewer has not started this stage. "
            "Queue time is not predictable; the pilot reviewer needs the researcher's computer online. "
            "Check again in about 5 minutes. Do not resubmit your record."
            if queue_delayed
            else "Your source is saved and queued. The estimate starts when the reviewer begins, "
            f"not when you submit. Check again in about {format_check(recommended)}."
        )
    elif status == "processing":
        if stale:
            recommended = 300
            note = (
                "Your source remains saved. The reviewer has not sent a recent heartbeat; "
                "completion time is currently unknown. Check again in about 5 minutes. "
                "Do not start a duplicate review."
            )
        elif overdue:
            recommended = 120
            note = (
                "This stage is taking longer than the pilot estimate, but the reviewer "
                "is still checking in. There is no reliable remaining-time estimate. "
                "Check again in about 2 minutes; do not resubmit."
            )
        else:
            recommended = max(30, int(check - age))
            note = (
                f"Provisional stage estimate: {format_range(lower, upper)} from its start. "
                f"Check again in about {format_check(recommended)}. "
                "This is a limited-pilot estimate, not a deadline; larger records can take longer."
            )
    elif status == "clarification_needed":
        note = (
            "Your clarification questions are ready. Answer them one at a time; "
            "there is no review wait between independent questions in this batch. "
            "After your answers are submitted, reconciliation and the full evidence review may follow."
        )
    elif status == "ready":
        note = "The full evidence review is ready for your confirmation. No further server wait is needed now."
    elif status in {"error", "resource_limited"}:
        note = (
            "The review is blocked, not still processing. Your source remains saved. "
            "Waiting alone will not fix this; use the same review's retry after the issue is resolved."
        )
    elif status == "paused":
        note = "The review is paused. Processing will resume only when you ask to resume it."
    elif status in {"stopped", "withdrawn"}:
        note = "This review is no longer processing."
    return {
        "review_stage": stage if waiting else status,
        "review_stage_label": label if waiting else status.replace("_", " "),
        "estimated_stage_seconds": {"low": lower, "high": upper} if waiting else None,
        "estimated_remaining_seconds": (
            {"low": remaining[0], "high": remaining[1]}
            if remaining is not None and not overdue and not stale
            else None
        ),
        "estimate_basis": ESTIMATE_BASIS[stage] if waiting else None,
        "stage_elapsed_seconds": age if status == "processing" else None,
        "worker_heartbeat_age_seconds": heartbeat_age if status == "processing" else None,
        "estimate_exceeded": bool(overdue),
        "worker_status_uncertain": bool(stale or queue_delayed),
        "recommended_check_after_seconds": recommended,
        "wait_guidance": note,
    }


def format_range(low: int, high: int) -> str:
    if low < 60:
        return f"{low}-{high} seconds"
    return f"{math.ceil(low / 60)}-{math.ceil(high / 60)} minutes"


def format_check(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} seconds"
    n = math.ceil(seconds / 60)
    return f"{n} minute" + ("s" if n != 1 else "")
