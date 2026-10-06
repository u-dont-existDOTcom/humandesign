from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'apps/life-patterns-participant/participant/app.py';s=p.read_text()
def rep(old,new):
 global s
 assert s.count(old)==1,(old[:70],s.count(old))
 s=s.replace(old,new,1)
rep('from .validation_diagnostics import safe_validation_diagnostic','from .validation_diagnostics import safe_validation_diagnostic\nfrom .review_timing import review_guidance\nfrom .fast_review import PROTOCOL, source_revision')
rep('    public_origin: str = ""','    public_origin: str = ""\n    fast_review_enabled: bool = False')
rep('            live_enabled=os.environ.get("PARTICIPANT_LIVE_ENABLED") == "1",','            live_enabled=os.environ.get("PARTICIPANT_LIVE_ENABLED") == "1",\n            fast_review_enabled=os.environ.get("PARTICIPANT_FAST_REVIEW_ENABLED") == "1",')
rep('    candidate_record: dict\n\n\nclass GptReviewAnswer', '    candidate_record: dict\n    review_protocol: Literal["legacy-v1", "fast-batch-v1"] = "legacy-v1"\n\n\nclass GptReviewAnswer')
rep('class GptReviewControl(Body):','''class BatchAnswer(Body):
    clarification_id: str = Field(pattern=r"^Q-[a-f0-9]{32}$")
    answer_text: str = Field(default="", max_length=20000)
    skipped: bool = False


class GptBatchAnswers(Body):
    batch_id: str = Field(pattern=r"^B-[a-f0-9]{32}$")
    operation_id: str = Field(min_length=16, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    answers: list[BatchAnswer] = Field(min_length=1, max_length=3)


class GptReviewControl(Body):''')
rep('class WorkerHeartbeat(Body):\n    claim_id: str = Field(pattern=r"^L-[a-f0-9]{32}$")','class WorkerHeartbeat(Body):\n    claim_id: str = Field(pattern=r"^L-[a-f0-9]{32}$")\n    review_stage: str | None = Field(default=None, max_length=40)')
rep('        "clarification_needed", "ready", "error", "paused", "stopped", "resource_limited"','        "queued", "clarification_needed", "ready", "error", "paused", "stopped", "resource_limited"')
rep('    clarification: WorkerClarification | None = None','    clarification: WorkerClarification | None = None\n    clarifications: list[WorkerClarification] | None = Field(default=None, min_length=1, max_length=3)')
a=s.index('        recommended_check_after_seconds = 0\n',s.index('    def review_public('));b=s.index('        return {',a)
s=s[:a]+s[b:]
rep('            "recommended_check_after_seconds": recommended_check_after_seconds,','''            **review_guidance(payload),
            "review_protocol": payload.get("review_protocol", "legacy-v1"),
            "batch_id": payload.get("pending_batch_id") if status == "clarification_needed" else None,
            "clarifications": payload.get("pending_clarifications") if status == "clarification_needed" else None,
            "final_review_completed": status == "ready",
''')
rep('        candidate = body.candidate_record\n        validate_review_candidate(candidate)','''        candidate = body.candidate_record
        if body.review_protocol == PROTOCOL and not settings.fast_review_enabled:
            raise HTTPException(409, "Fast review is not enabled; retain the source and try later.")
        validate_review_candidate(candidate)''')
rep('            maximum_jobs=settings.maximum_sessions,','            maximum_jobs=settings.maximum_sessions,\n            review_protocol=body.review_protocol,')
marker='    @app.post("/api/gpt/reviews/{review_id}/control")'
rep(marker,'''    @app.post("/api/gpt/reviews/{review_id}/clarification-batches")
    def gpt_review_batch(request: Request, review_id: str, body: GptBatchAnswers):
        gpt_submitter(request)
        for answer in body.answers:
            if target_exposure(answer.answer_text):
                raise ValueError("Omit birth/chart information from clarification answers.")
        return review_public(store.add_gpt_review_batch_answers(
            review_id, body.batch_id, [answer.model_dump() for answer in body.answers], body.operation_id
        ))

'''+marker)
rep('            "schema": "life-patterns-review-worker-job-v1",','            "schema": "life-patterns-review-worker-job-v1",\n            "review_protocol": payload.get("review_protocol", "legacy-v1"),\n            "review_stage": payload.get("review_stage"),')
rep('        return store.renew_gpt_review(review_id, body.claim_id)','        return store.renew_gpt_review(review_id, body.claim_id, review_stage=body.review_stage)')
a=s.index('        clarification = body.clarification.model_dump()');b=s.index('        payload = store.complete_gpt_review(',a)
s=s[:a]+'''        clarification = body.clarification.model_dump() if body.clarification else None
        clarifications = [q.model_dump() for q in body.clarifications] if body.clarifications else None
        fast = queued.get("review_protocol") == PROTOCOL
        if fast and body.receipt.get("source_revision") != source_revision(
            queued["candidate_sha256"], queued.get("clarification_history", [])
        ):
            raise HTTPException(409, "The worker result refers to a stale source revision.")
        if body.status == "clarification_needed":
            if not clarification:
                raise ValueError("Clarification-needed results require one question.")
            questions = clarifications or [clarification]
            if questions[0] != clarification or (not fast and len(questions) > 1):
                raise ValueError("The batch does not match the review protocol.")
            pinned = store.instrument(queued.get("instrument_version", version))
            routes = {row["id"]: row for row in bank(pinned)["questions"]}
            for question in questions:
                route = routes.get(question["route_id"])
                if route is None:
                    raise ValueError("Worker returned an unknown survey route.")
                if question["route_type"] == "canonical" and question["question_text"] != route["question"]:
                    raise ValueError("Canonical worker question does not match the frozen bank.")
                if target_exposure(question["question_text"]):
                    raise ValueError("Birth/chart questions are not permitted.")
            if not body.worker_state or body.worker_state.get("phase") != "awaiting_answer":
                raise ValueError("Clarification results require the saved awaiting-answer state.")
            if fast:
                private = (body.worker_state.get("fast_review") or {}).get("pending_questions")
                if private:
                    from .fast_review import public_question
                    if [public_question(q) for q in private] != questions:
                        raise ValueError("Public batch differs from the saved approved questions.")
        elif clarification is not None or clarifications:
            raise ValueError("Only clarification-needed results may include a question.")
        if body.status == "ready":
            if not body.worker_state or body.worker_state.get("phase") != "review":
                raise ValueError("Ready results require a worker state at independent neutral review.")
            if fast and not (
                body.receipt.get("final_review_completed") is True
                and (body.worker_state.get("fast_review") or {}).get("final_review_completed") is True
                and body.worker_state.get("gpt_review_answers_processed") == len(queued.get("clarification_history", []))
            ):
                raise ValueError("Fast triage alone cannot complete a full review.")
        if body.status == "queued" and not (
            fast and body.worker_state and body.worker_state.get("phase") == "ready"
            and (body.worker_state.get("fast_review") or {}).get("stage") == "final_synthesis"
            and body.receipt.get("next_stage") == "final_synthesis"
        ):
            raise ValueError("Invalid saved stage transition.")
''' +s[b:]
rep('            clarification=clarification,\n            error=body.error,','            clarification=clarification,\n            clarifications=clarifications,\n            error=body.error,')
# The existing health response has a stable enabled field; add capability beside it.
needle='"gpt_review_queue_enabled":'
pos=s.index(needle);end=s.index('\n',pos)
s=s[:end]+ '\n            "fast_review_enabled": settings.fast_review_enabled,\n            "review_protocols": ["legacy-v1"] + ([PROTOCOL] if settings.fast_review_enabled else []),' +s[end:]
p.write_text(s)

p=root/'apps/life-patterns-participant/scripts/gpt_review_worker.py';s=p.read_text()
rep('def run_review(\n', 'def run_legacy_review(\n')
marker='\n\nclass EncryptedOutbox:'
rep(marker,'''\n\ndef run_review(job: dict, provider=None, authority_dir: Path | None = None, progress=None):
    from participant.fast_review import PROTOCOL, run_fast_review
    if job.get("review_protocol") != PROTOCOL:
        return run_legacy_review(job, provider=provider, authority_dir=authority_dir)
    with tempfile.TemporaryDirectory(prefix="life-patterns-fast-authority-") as folder:
        root = authority_dir or authority_copy(Path(folder))
        instrument = job.get("instrument") or load_instrument(root)
        local_store = Store(Path(folder)/"instrument.sqlite3", Fernet.generate_key().decode())
        version = local_store.pin_instrument(instrument)
        if job.get("instrument_version") not in {None, version}:
            raise RuntimeError("review_instrument_hash_mismatch")
        def legacy(prepared, provider):
            return run_legacy_review(prepared, provider=provider, authority_dir=root)
        return run_fast_review(job, provider or CodexCliProvider(), instrument, version, legacy, progress)
''' +marker)
rep('    last_lease = time.monotonic()\n\n    def heartbeat():','''    last_lease = time.monotonic()
    current_stage = {"value": job.get("review_stage")}

    def progress(stage):
        current_stage["value"] = stage
        try:
            http_json("POST", base_url + f"/api/review-worker/jobs/{job['review_id']}/heartbeat",
                      worker_token, {"claim_id": job["claim_id"], "review_stage": stage})
        except TransportError as exc:
            if exc.status in {401, 409}:
                stop.set()
                raise

    def heartbeat():''')
rep('                    {"claim_id": job["claim_id"]},','                    {"claim_id": job["claim_id"], "review_stage": current_stage["value"]},')
rep('            job, provider=CodexCliProvider(stop_event=stop), authority_dir=authority_dir','            job, provider=CodexCliProvider(stop_event=stop), authority_dir=authority_dir, progress=progress')
# Attach source fence to operational errors as well; no source text in receipts.
rep('    if stop.is_set():\n        return True\n    outbox.save(','''    if stop.is_set():
        return True
    clarifications = None
    if job.get("review_protocol") == "fast-batch-v1":
        from participant.fast_review import source_revision, public_question
        receipt["source_revision"] = source_revision(job["candidate_sha256"], job.get("clarification_history", []))
        if result_status == "clarification_needed" and worker_state:
            pending = (worker_state.get("fast_review") or {}).get("pending_questions") or []
            if pending:
                clarifications = [public_question(q) for q in pending]
    outbox.save(''')
rep('                "clarification": clarification,\n                "error": error,','                "clarification": clarification,\n                "clarifications": clarifications,\n                "error": error,')
rep('                    clarification=None,\n                    error="worker_result_rejected_by_server",','                    clarification=None,\n                    clarifications=None,\n                    error="worker_result_rejected_by_server",')
# Preserve fast source revision in fallback error reporting.
rep('                        "paid_api": False,\n                        "error_code": "worker_result_rejected_by_server",','                        "paid_api": False,\n                        "source_revision": failed["receipt"].get("source_revision"),\n                        "error_code": "worker_result_rejected_by_server",')
p.write_text(s)
print('APP_AND_WORKER_PATCHED')
