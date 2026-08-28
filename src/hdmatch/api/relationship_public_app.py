"""Public capture-safe FastAPI app for the relationship questionnaire pilot.

This deployment intentionally implements only the chart-blind capture layer:
one question at a time, pseudonymous sessions, pause/resume, review, and response
freeze. Raw responses are stored outside Git in a private persistent directory.
Classifier, fingerprint, and post-freeze Astro/HD reveal layers are added later
without changing the storage or deployment boundary.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from hdmatch.relationship.questionnaire import (
    RelationshipQuestion,
    RelationshipQuestionnaireSpec,
    load_relationship_questionnaire,
    select_next_capture_question,
)


class CreateSessionRequest(BaseModel):
    consent_to_store_responses: bool


class AnswerRequest(BaseModel):
    token: str = Field(min_length=16)
    question_id: str = Field(min_length=1)
    answer: str = Field(min_length=1, max_length=20000)


class FreezeRequest(BaseModel):
    token: str = Field(min_length=16)


class RelationshipFileStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self) -> tuple[dict[str, Any], str]:
        session_id = f"RR-{uuid.uuid4().hex[:16]}"
        token = secrets.token_urlsafe(32)
        now = datetime.now(UTC).isoformat()
        payload: dict[str, Any] = {
            "session_id": session_id,
            "token_sha256": hashlib.sha256(token.encode()).hexdigest(),
            "created_at": now,
            "updated_at": now,
            "status": "in_progress",
            "answers": [],
            "freeze_sha256": None,
        }
        self._write(payload)
        return payload, token

    def read(self, session_id: str, token: str) -> dict[str, Any]:
        path = self._path(session_id)
        if not path.exists():
            raise HTTPException(status_code=404, detail="session not found")
        payload = json.loads(path.read_text(encoding="utf-8"))
        supplied = hashlib.sha256(token.encode()).hexdigest()
        if not secrets.compare_digest(str(payload["token_sha256"]), supplied):
            raise HTTPException(status_code=403, detail="invalid resume token")
        return payload

    def save(self, payload: dict[str, Any]) -> None:
        payload["updated_at"] = datetime.now(UTC).isoformat()
        self._write(payload)

    def _path(self, session_id: str) -> Path:
        safe = "".join(ch for ch in session_id if ch.isalnum() or ch in "-_")
        if safe != session_id:
            raise HTTPException(status_code=400, detail="invalid session id")
        return self.root / f"{safe}.json"

    def _write(self, payload: dict[str, Any]) -> None:
        path = self._path(str(payload["session_id"]))
        temporary = path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)


def _public_question(question: RelationshipQuestion) -> dict[str, Any]:
    return {
        "id": question.id,
        "prompt": question.prompt,
        "probes": list(question.probes),
        "stage": question.stage,
    }


def _next_question(
    spec: RelationshipQuestionnaireSpec, payload: dict[str, Any]
) -> RelationshipQuestion | None:
    answered = tuple(str(item["question_id"]) for item in payload["answers"])
    # Phase-1 public capture deliberately asks the six frozen anchors only.
    # Adaptive follow-ups require the blind classifier to supply unresolved axes
    # and applicability flags; those are not guessed from keywords here.
    return select_next_capture_question(spec, answered_question_ids=answered)


def _freeze_digest(payload: dict[str, Any]) -> str:
    frozen = {
        "session_id": payload["session_id"],
        "answers": payload["answers"],
    }
    encoded = json.dumps(frozen, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def create_relationship_public_app_from_env() -> FastAPI:
    questionnaire_path = Path(
        os.environ.get(
            "HDMATCH_RELATIONSHIP_QUESTIONNAIRE",
            "reference/relationship/relationship_dynamic_questionnaire_v1.json",
        )
    )
    store_value = os.environ.get("HDMATCH_RELATIONSHIP_STORE", "").strip()
    if not store_value:
        raise RuntimeError(
            "HDMATCH_RELATIONSHIP_STORE is required; point it at a private persistent volume"
        )

    spec = load_relationship_questionnaire(questionnaire_path)
    store = RelationshipFileStore(Path(store_value))
    app = FastAPI(title="Relationship X-Ray Pilot", version="0.1.0")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    def home() -> str:
        return _HTML

    @app.post("/api/sessions")
    def create_session(request: CreateSessionRequest) -> dict[str, Any]:
        if not request.consent_to_store_responses:
            raise HTTPException(status_code=400, detail="consent is required")
        payload, token = store.create()
        question = _next_question(spec, payload)
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "next_question": _public_question(question) if question else None,
        }

    @app.get("/api/sessions/{session_id}")
    def get_session(session_id: str, token: str) -> dict[str, Any]:
        payload = store.read(session_id, token)
        question = None if payload["status"] == "frozen" else _next_question(spec, payload)
        return {
            "session_id": session_id,
            "status": payload["status"],
            "answers": payload["answers"],
            "next_question": _public_question(question) if question else None,
            "freeze_sha256": payload["freeze_sha256"],
        }

    @app.post("/api/sessions/{session_id}/answers")
    def submit_answer(session_id: str, request: AnswerRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        expected = _next_question(spec, payload)
        if expected is None:
            raise HTTPException(status_code=409, detail="core questionnaire is complete")
        if request.question_id != expected.id:
            raise HTTPException(status_code=409, detail="answer does not match next question")
        payload["answers"].append(
            {
                "question_id": request.question_id,
                "answer": request.answer.strip(),
                "answered_at": datetime.now(UTC).isoformat(),
            }
        )
        store.save(payload)
        next_question = _next_question(spec, payload)
        return {
            "accepted": True,
            "answered_count": len(payload["answers"]),
            "next_question": _public_question(next_question) if next_question else None,
            "ready_to_review": next_question is None,
        }

    @app.post("/api/sessions/{session_id}/freeze")
    def freeze(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] == "frozen":
            return {
                "status": "frozen",
                "freeze_sha256": payload["freeze_sha256"],
            }
        if _next_question(spec, payload) is not None:
            raise HTTPException(status_code=409, detail="complete core questions before freezing")
        payload["status"] = "frozen"
        payload["freeze_sha256"] = _freeze_digest(payload)
        payload["frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {
            "status": "frozen",
            "freeze_sha256": payload["freeze_sha256"],
        }

    return app


_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Relationship X-Ray</title>
<style>
body{font-family:system-ui,sans-serif;max-width:760px;margin:0 auto;padding:32px 20px;line-height:1.5}textarea{width:100%;min-height:180px;font:inherit;padding:12px;box-sizing:border-box}button{font:inherit;padding:10px 16px;margin-top:12px}small{color:#555}.hidden{display:none}.card{border:1px solid #ddd;border-radius:12px;padding:20px;margin-top:18px}.probe{margin:6px 0;color:#555}.answer{white-space:pre-wrap;background:#f6f6f6;padding:10px;border-radius:8px;margin:8px 0}
</style></head>
<body>
<h1>Relationship X-Ray</h1>
<p>Describe one important relationship in ordinary language. Your answers build a multidimensional relationship record before any astrology or Human Design result is shown.</p>
<div id="start" class="card"><label><input id="consent" type="checkbox"> I consent to storing these responses privately for this research session.</label><br><button onclick="begin()">Begin</button></div>
<div id="survey" class="card hidden"><div id="prompt"></div><div id="probes"></div><textarea id="answer" placeholder="Write as much context as you need."></textarea><button onclick="submitAnswer()">Save & continue</button><p><small>Your private resume token is stored only in this browser.</small></p></div>
<div id="review" class="card hidden"><h2>Review</h2><div id="answers"></div><button onclick="freezeSession()">Freeze my answers</button></div>
<div id="done" class="card hidden"><h2>Responses frozen</h2><p>Your answers are sealed for this pilot. The personalized fingerprint and blinded Astro/HD comparison are the next deployment layer.</p><p id="digest"></p></div>
<script>
let sessionId=localStorage.getItem('rr_session');let token=localStorage.getItem('rr_token');let current=null;
async function begin(){if(!document.getElementById('consent').checked)return alert('Consent is required.');const r=await fetch('/api/sessions',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({consent_to_store_responses:true})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not start');sessionId=d.session_id;token=d.resume_token;localStorage.setItem('rr_session',sessionId);localStorage.setItem('rr_token',token);showQuestion(d.next_question)}
function showQuestion(q){document.getElementById('start').classList.add('hidden');document.getElementById('review').classList.add('hidden');document.getElementById('survey').classList.remove('hidden');current=q;document.getElementById('prompt').innerHTML='<h2>'+escapeHtml(q.prompt)+'</h2>';document.getElementById('probes').innerHTML=q.probes.map(x=>'<div class="probe">'+escapeHtml(x)+'</div>').join('');document.getElementById('answer').value=''}
async function submitAnswer(){const text=document.getElementById('answer').value.trim();if(!text)return alert('Write an answer or explain what is unknown.');const r=await fetch('/api/sessions/'+sessionId+'/answers',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token,question_id:current.id,answer:text})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not save');if(d.next_question)showQuestion(d.next_question);else loadReview()}
async function loadReview(){const r=await fetch('/api/sessions/'+sessionId+'?token='+encodeURIComponent(token));const d=await r.json();document.getElementById('survey').classList.add('hidden');document.getElementById('review').classList.remove('hidden');document.getElementById('answers').innerHTML=d.answers.map((a,i)=>'<h3>'+(i+1)+'. '+escapeHtml(a.question_id)+'</h3><div class="answer">'+escapeHtml(a.answer)+'</div>').join('')}
async function freezeSession(){const r=await fetch('/api/sessions/'+sessionId+'/freeze',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not freeze');document.getElementById('review').classList.add('hidden');document.getElementById('done').classList.remove('hidden');document.getElementById('digest').textContent='Freeze receipt: '+d.freeze_sha256}
function escapeHtml(s){return String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
if(sessionId&&token){fetch('/api/sessions/'+sessionId+'?token='+encodeURIComponent(token)).then(r=>r.json()).then(d=>{if(d.status==='frozen'){document.getElementById('start').classList.add('hidden');document.getElementById('done').classList.remove('hidden');document.getElementById('digest').textContent='Freeze receipt: '+d.freeze_sha256}else if(d.next_question)showQuestion(d.next_question);else loadReview()}).catch(()=>{})}
</script></body></html>"""
