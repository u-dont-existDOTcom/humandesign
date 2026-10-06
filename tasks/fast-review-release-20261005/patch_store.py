from pathlib import Path
p=Path(__file__).resolve().parents[2]/'apps/life-patterns-participant/participant/store.py'
s=p.read_text()
def rep(old,new):
 global s
 assert s.count(old)==1, (old[:70],s.count(old))
 s=s.replace(old,new,1)
rep('        maximum_jobs: int = 50,\n    ) -> tuple[str, dict, bool]:','        maximum_jobs: int = 50,\n        review_protocol: str = "legacy-v1",\n    ) -> tuple[str, dict, bool]:')
rep('                if payload["candidate_sha256"] != candidate_sha256:', '                if (payload["candidate_sha256"] != candidate_sha256\n                    or payload.get("review_protocol", "legacy-v1") != review_protocol):')
rep('                "status": "queued",\n                "instrument_version": instrument_version,','                "status": "queued",\n                "review_protocol": review_protocol,\n                "review_stage": "initial_triage" if review_protocol == "fast-batch-v1" else "legacy_review",\n                "instrument_version": instrument_version,')
rep('            payload["claim_attempts"] = int(payload.get("claim_attempts", 0)) + 1', '            payload["stage_started_at_unix"] = now\n            payload["claim_attempts"] = int(payload.get("claim_attempts", 0)) + 1')
rep('    def renew_gpt_review(self, review_id: str, claim_id: str, lease_seconds: int = 180) -> dict:', '    def renew_gpt_review(self, review_id: str, claim_id: str, lease_seconds: int = 180,\n                         review_stage: str | None = None) -> dict:')
rep('            self._require_review_claim(payload, claim_id, now)\n            payload.update(', '            self._require_review_claim(payload, claim_id, now)\n            if review_stage is not None:\n                from .review_timing import STAGES\n                if review_stage not in STAGES:\n                    raise ValueError("Unknown review stage.")\n                if payload.get("review_stage") != review_stage:\n                    payload["review_stage"] = review_stage\n                    payload["stage_started_at_unix"] = now\n            payload.update(')
rep('        clarification: dict | None = None,\n        error: str | None = None,', '        clarification: dict | None = None,\n        error: str | None = None,\n        clarifications: list[dict] | None = None,')
rep('        if status not in {\n            "clarification_needed",', '        if status not in {\n            "queued",\n            "clarification_needed",')
rep('                    "clarification": clarification,\n                    "error": error,', '                    "clarification": clarification,\n                    "clarifications": clarifications,\n                    "error": error,')
rep('            payload.update(status=status, updated_at_unix=now, error=error, lease_until=None)', '''            if payload.get("review_protocol") == "fast-batch-v1":
                from .fast_review import source_revision
                expected = source_revision(candidate_sha256, payload["clarification_history"])
                if receipt.get("source_revision") != expected:
                    raise Conflict("The worker result refers to a stale review source revision.")
            if status == "queued":
                if (payload.get("review_protocol") != "fast-batch-v1"
                    or receipt.get("next_stage") != "final_synthesis"):
                    raise ValueError("Only a fast-stage transition can requeue work.")
                payload.update(review_stage="final_synthesis", cycle_queued_at_unix=now)
            payload.update(status=status, updated_at_unix=now, error=error, lease_until=None)''')
rep('''                payload["pending_clarification"] = dict(clarification) | {
                    "clarification_id": "Q-" + secrets.token_hex(16)
                }
            else:
                payload["pending_clarification"] = None''', '''                questions = clarifications or [clarification]
                if not 1 <= len(questions) <= 3 or questions[0] != clarification:
                    raise ValueError("Invalid clarification batch.")
                pending = [dict(q) | {"clarification_id": "Q-" + secrets.token_hex(16)}
                           for q in questions]
                payload["pending_clarifications"] = pending
                payload["pending_batch_id"] = "B-" + secrets.token_hex(16)
                payload["pending_clarification"] = pending[0]
            else:
                payload["pending_clarification"] = None
                payload["pending_clarifications"] = []
                payload["pending_batch_id"] = None''')
# Legacy single answer remains compatible, but invalidates the rest of a fast batch.
rep('''                round=len(payload["clarification_history"]),
            )''', '''                round=len(payload["clarification_history"]),
                pending_clarifications=[], pending_batch_id=None,
                review_stage="reconciliation" if payload.get("review_protocol") == "fast-batch-v1" else "legacy_followup",
            )''')
marker='    def control_gpt_review(self, review_id: str, action: str, operation_id: str) -> dict:'
new='''    def add_gpt_review_batch_answers(self, review_id: str, batch_id: str,
                                     answers: list[dict], operation_id: str) -> dict:
        """Atomically accept an ordered prefix; invalidate any unasked remainder."""
        if not 1 <= len(answers) <= 3:
            raise ValueError("A batch needs one to three answers or explicit skips.")
        signature = digest(canonical({"batch": batch_id, "answers": answers}))
        now = time.time()
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT payload FROM gpt_review_jobs WHERE id=?", (review_id,)).fetchone()
            if not row:
                raise Missing("Unknown GPT review.")
            payload = self.decode(row[0])
            operations = payload.setdefault("operations", {})
            if operation_id in operations:
                if operations[operation_id] != signature:
                    raise Conflict("A batch operation ID was reused for different content.")
                db.commit()
                return payload
            pending = payload.get("pending_clarifications") or []
            if (payload["status"] != "clarification_needed"
                or payload.get("pending_batch_id") != batch_id
                or len(answers) > len(pending)):
                raise Conflict("This batch is stale or no longer awaiting answers.")
            for question, answer in zip(pending, answers):
                if question["clarification_id"] != answer["clarification_id"]:
                    raise Conflict("Answers must match the current batch in its original order.")
                text, skipped = answer.get("answer_text", ""), answer.get("skipped", False)
                if (not skipped and not text.strip()) or (skipped and text):
                    raise ValueError("Provide an exact answer or an explicit empty skip.")
            for question, answer in zip(pending, answers):
                skipped = answer.get("skipped", False)
                payload["clarification_history"].append(dict(question) | {
                    "answer_text": None if skipped else answer["answer_text"],
                    "answer_status": "skipped" if skipped else "answered",
                    "answered_at_unix": now,
                })
            operations[operation_id] = signature
            payload.update(status="queued", updated_at_unix=now, cycle_queued_at_unix=now,
                           review_stage="reconciliation", error=None,
                           pending_clarification=None, pending_clarifications=[], pending_batch_id=None,
                           round=len(payload["clarification_history"]))
            self._save_review(db, payload)
            db.commit()
        return payload

'''
rep(marker,new+marker)
rep('''                        pending_clarification=None,
                        claim_id=None,''','''                        pending_clarification=None,
                        pending_clarifications=[], pending_batch_id=None,
                        claim_id=None,''')
p.write_text(s)
print('STORE_PATCHED')
