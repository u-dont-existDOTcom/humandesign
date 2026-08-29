"""Public capture-safe FastAPI app for the relationship questionnaire pilot.

The participant UI keeps six broad relationship domains for navigation, but each
domain contains several narrow response fields. Every field has an explicit
certainty/status choice so mixed, context-dependent, unknown, and not-applicable
states are preserved instead of being forced into one narrative blob.

Raw responses remain on private persistent storage outside Git. Frozen legacy
single-textarea sessions remain immutable and may receive a separately frozen
guided clarification addendum.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, cast

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field

from hdmatch.relationship.questionnaire import (
    RelationshipQuestion,
    RelationshipQuestionnaireSpec,
    load_relationship_questionnaire,
    question_by_id,
    select_next_capture_question,
)

FieldStatus = Literal["clear", "mixed", "context_dependent", "unknown", "not_applicable"]


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class GuidedField(_FrozenModel):
    id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    placeholder: str = ""
    clarification_prompt: str = Field(min_length=1)


class GuidedQuestion(_FrozenModel):
    title: str = Field(min_length=1)
    intro: str = Field(min_length=1)
    fields: tuple[GuidedField, ...]


class GuidedRegistry(_FrozenModel):
    schema_version: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    status_options: tuple[FieldStatus, ...]
    questions: dict[str, GuidedQuestion]


class CreateSessionRequest(BaseModel):
    consent_to_store_responses: bool


class GuidedFieldAnswerRequest(BaseModel):
    field_id: str = Field(min_length=1)
    status: FieldStatus
    answer: str = Field(default="", max_length=12000)
    clarification: str = Field(default="", max_length=12000)


class AnswerRequest(BaseModel):
    token: str = Field(min_length=16)
    question_id: str = Field(min_length=1)
    field_answers: tuple[GuidedFieldAnswerRequest, ...]


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
            "format_version": "guided-fields-v1",
            "token_sha256": hashlib.sha256(token.encode()).hexdigest(),
            "created_at": now,
            "updated_at": now,
            "status": "in_progress",
            "answers": [],
            "freeze_sha256": None,
            "clarification_addendum": None,
        }
        self._write(payload)
        return payload, token

    def read(self, session_id: str, token: str) -> dict[str, Any]:
        payload = self.read_private(session_id)
        supplied = hashlib.sha256(token.encode()).hexdigest()
        if not secrets.compare_digest(str(payload["token_sha256"]), supplied):
            raise HTTPException(status_code=403, detail="invalid resume token")
        return payload

    def read_private(self, session_id: str) -> dict[str, Any]:
        """Load a private session for server-side credential workflows only."""

        path = self._path(session_id)
        if not path.exists():
            raise HTTPException(status_code=404, detail="session not found")
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))

    def private_records(self) -> tuple[dict[str, Any], ...]:
        """Return well-formed private records without exposing them through an API route."""

        records: list[dict[str, Any]] = []
        for path in sorted(self.root.glob("RR-*.json")):
            try:
                raw: Any = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError, UnicodeError):
                continue
            if not isinstance(raw, dict):
                continue
            session_id = raw.get("session_id")
            if not isinstance(session_id, str) or self._path(session_id) != path:
                continue
            records.append(cast(dict[str, Any], raw))
        return tuple(records)

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


def _load_guided_registry(path: Path, spec: RelationshipQuestionnaireSpec) -> GuidedRegistry:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    registry = GuidedRegistry.model_validate(raw)
    if set(registry.questions) != set(spec.core_question_ids):
        raise ValueError("guided field registry must contain exactly the six core questions")
    expected_statuses = {"clear", "mixed", "context_dependent", "unknown", "not_applicable"}
    if set(registry.status_options) != expected_statuses:
        raise ValueError("guided field registry has unexpected status options")
    for question_id, question in registry.questions.items():
        ids = [item.id for item in question.fields]
        if not ids or len(ids) != len(set(ids)):
            raise ValueError(f"guided field ids must be nonempty and unique: {question_id}")
    return registry


def _public_question(
    question: RelationshipQuestion, registry: GuidedRegistry
) -> dict[str, Any]:
    guided = registry.questions[question.id]
    return {
        "id": question.id,
        "title": guided.title,
        "intro": guided.intro,
        "stage": question.stage,
        "fields": [item.model_dump() for item in guided.fields],
    }


def _answered_ids(answers: list[dict[str, Any]]) -> tuple[str, ...]:
    return tuple(str(item["question_id"]) for item in answers)


def _next_question(
    spec: RelationshipQuestionnaireSpec, answers: list[dict[str, Any]]
) -> RelationshipQuestion | None:
    # The public capture layer asks the six core domains. Semantic adaptive
    # follow-ups remain classifier-driven and are not guessed from keywords.
    return select_next_capture_question(spec, answered_question_ids=_answered_ids(answers))


def _legacy_session(payload: dict[str, Any]) -> bool:
    answers = payload.get("answers", [])
    return bool(answers) and any("answer" in item and "fields" not in item for item in answers)


def _clean_field_answers(
    question: GuidedQuestion, supplied: tuple[GuidedFieldAnswerRequest, ...]
) -> list[dict[str, str]]:
    expected = [item.id for item in question.fields]
    provided = [item.field_id for item in supplied]
    if len(provided) != len(set(provided)) or set(provided) != set(expected):
        raise HTTPException(
            status_code=422,
            detail="submit exactly one response for every field in this domain",
        )
    by_id = {item.field_id: item for item in supplied}
    cleaned: list[dict[str, str]] = []
    for field in question.fields:
        item = by_id[field.id]
        answer = item.answer.strip()
        clarification = item.clarification.strip()
        if item.status in {"clear", "mixed", "context_dependent"} and not answer:
            raise HTTPException(
                status_code=422,
                detail=f"{field.id}: write an answer or mark it unknown/not applicable",
            )
        if item.status in {"mixed", "context_dependent"} and not clarification:
            raise HTTPException(
                status_code=422,
                detail=f"{field.id}: clarify what is mixed or what changes by context/time",
            )
        cleaned.append(
            {
                "field_id": field.id,
                "status": item.status,
                "answer": answer,
                "clarification": clarification,
            }
        )
    return cleaned


def _replace_answer(
    answers: list[dict[str, Any]], question_id: str, replacement: dict[str, Any]
) -> None:
    for index, item in enumerate(answers):
        if item["question_id"] == question_id:
            answers[index] = replacement
            return
    raise HTTPException(status_code=404, detail="answer not found")


def _freeze_digest(payload: dict[str, Any]) -> str:
    frozen = {"session_id": payload["session_id"], "answers": payload["answers"]}
    encoded = json.dumps(frozen, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def _addendum_digest(parent_freeze: str, answers: list[dict[str, Any]]) -> str:
    frozen = {"parent_freeze_sha256": parent_freeze, "answers": answers}
    encoded = json.dumps(frozen, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def _answer_record(question_id: str, fields: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "fields": fields,
        "answered_at": datetime.now(UTC).isoformat(),
    }


def create_relationship_public_app_from_env() -> FastAPI:
    questionnaire_path = Path(
        os.environ.get(
            "HDMATCH_RELATIONSHIP_QUESTIONNAIRE",
            "reference/relationship/relationship_dynamic_questionnaire_v1.json",
        )
    )
    guided_path = Path(
        os.environ.get(
            "HDMATCH_RELATIONSHIP_GUIDED_FIELDS",
            "reference/relationship/relationship_guided_response_fields_v1.json",
        )
    )
    store_value = os.environ.get("HDMATCH_RELATIONSHIP_STORE", "").strip()
    if not store_value:
        raise RuntimeError(
            "HDMATCH_RELATIONSHIP_STORE is required; point it at a private persistent volume"
        )

    spec = load_relationship_questionnaire(questionnaire_path)
    guided = _load_guided_registry(guided_path, spec)
    store = RelationshipFileStore(Path(store_value))
    app = FastAPI(title="Relationship X-Ray Pilot", version="0.2.0")

    def public_state(payload: dict[str, Any]) -> dict[str, Any]:
        question = None
        if payload["status"] == "in_progress":
            question = _next_question(spec, payload["answers"])
        addendum = payload.get("clarification_addendum")
        addendum_next = None
        if addendum and addendum.get("status") == "in_progress":
            addendum_next = _next_question(spec, addendum["answers"])
        return {
            "session_id": payload["session_id"],
            "status": payload["status"],
            "legacy_format": _legacy_session(payload),
            "answers": payload["answers"],
            "next_question": _public_question(question, guided) if question else None,
            "freeze_sha256": payload.get("freeze_sha256"),
            "can_start_clarification": (
                payload["status"] == "frozen"
                and _legacy_session(payload)
                and addendum is None
            ),
            "clarification_addendum": addendum,
            "clarification_next_question": (
                _public_question(addendum_next, guided) if addendum_next else None
            ),
        }

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    def home() -> str:
        return _HTML

    @app.get("/api/questions/{question_id}")
    def get_question_definition(question_id: str) -> dict[str, Any]:
        if question_id not in guided.questions:
            raise HTTPException(status_code=404, detail="unknown guided question")
        return _public_question(question_by_id(spec, question_id), guided)

    @app.post("/api/sessions")
    def create_session(request: CreateSessionRequest) -> dict[str, Any]:
        if not request.consent_to_store_responses:
            raise HTTPException(status_code=400, detail="consent is required")
        payload, token = store.create()
        state = public_state(payload)
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "next_question": state["next_question"],
        }

    @app.get("/api/sessions/{session_id}")
    def get_session(session_id: str, token: str) -> dict[str, Any]:
        return public_state(store.read(session_id, token))

    @app.post("/api/sessions/{session_id}/answers")
    def submit_answer(session_id: str, request: AnswerRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        expected = _next_question(spec, payload["answers"])
        if expected is None:
            raise HTTPException(status_code=409, detail="core questionnaire is complete")
        if request.question_id != expected.id:
            raise HTTPException(status_code=409, detail="answer does not match next question")
        fields = _clean_field_answers(guided.questions[expected.id], request.field_answers)
        payload["answers"].append(_answer_record(expected.id, fields))
        store.save(payload)
        state = public_state(payload)
        return {
            "accepted": True,
            "answered_count": len(payload["answers"]),
            "next_question": state["next_question"],
            "ready_to_review": state["next_question"] is None,
        }

    @app.put("/api/sessions/{session_id}/answers/{question_id}")
    def edit_answer(
        session_id: str, question_id: str, request: AnswerRequest
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "in_progress":
            raise HTTPException(status_code=409, detail="frozen answers cannot be edited")
        if request.question_id != question_id:
            raise HTTPException(status_code=422, detail="question id mismatch")
        if question_id not in guided.questions:
            raise HTTPException(status_code=404, detail="unknown guided question")
        fields = _clean_field_answers(guided.questions[question_id], request.field_answers)
        _replace_answer(payload["answers"], question_id, _answer_record(question_id, fields))
        store.save(payload)
        return {"accepted": True}

    @app.post("/api/sessions/{session_id}/freeze")
    def freeze(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] == "frozen":
            return {"status": "frozen", "freeze_sha256": payload["freeze_sha256"]}
        if _next_question(spec, payload["answers"]) is not None:
            raise HTTPException(status_code=409, detail="complete core questions before freezing")
        payload["status"] = "frozen"
        payload["freeze_sha256"] = _freeze_digest(payload)
        payload["frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {"status": "frozen", "freeze_sha256": payload["freeze_sha256"]}

    @app.post("/api/sessions/{session_id}/clarification")
    def start_clarification(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "frozen" or not _legacy_session(payload):
            raise HTTPException(
                status_code=409,
                detail="clarification addendum is only for frozen legacy-format sessions",
            )
        if payload.get("clarification_addendum") is None:
            payload["clarification_addendum"] = {
                "status": "in_progress",
                "parent_freeze_sha256": payload["freeze_sha256"],
                "started_at": datetime.now(UTC).isoformat(),
                "answers": [],
                "freeze_sha256": None,
            }
            store.save(payload)
        state = public_state(payload)
        return {
            "status": payload["clarification_addendum"]["status"],
            "next_question": state["clarification_next_question"],
        }

    @app.post("/api/sessions/{session_id}/clarification/answers")
    def submit_clarification_answer(
        session_id: str, request: AnswerRequest
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("clarification_addendum")
        if not addendum or addendum.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="clarification addendum is not active")
        expected = _next_question(spec, addendum["answers"])
        if expected is None or request.question_id != expected.id:
            raise HTTPException(status_code=409, detail="answer does not match next clarification")
        fields = _clean_field_answers(guided.questions[expected.id], request.field_answers)
        addendum["answers"].append(_answer_record(expected.id, fields))
        store.save(payload)
        next_question = _next_question(spec, addendum["answers"])
        return {
            "accepted": True,
            "next_question": _public_question(next_question, guided) if next_question else None,
            "ready_to_review": next_question is None,
        }

    @app.put("/api/sessions/{session_id}/clarification/answers/{question_id}")
    def edit_clarification_answer(
        session_id: str, question_id: str, request: AnswerRequest
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("clarification_addendum")
        if not addendum or addendum.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="clarification addendum is not active")
        if request.question_id != question_id or question_id not in guided.questions:
            raise HTTPException(status_code=422, detail="question id mismatch")
        fields = _clean_field_answers(guided.questions[question_id], request.field_answers)
        _replace_answer(addendum["answers"], question_id, _answer_record(question_id, fields))
        store.save(payload)
        return {"accepted": True}

    @app.post("/api/sessions/{session_id}/clarification/freeze")
    def freeze_clarification(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("clarification_addendum")
        if not addendum:
            raise HTTPException(status_code=409, detail="no clarification addendum")
        if addendum.get("status") == "frozen":
            return {"status": "frozen", "freeze_sha256": addendum["freeze_sha256"]}
        if _next_question(spec, addendum["answers"]) is not None:
            raise HTTPException(status_code=409, detail="complete clarification fields first")
        addendum["status"] = "frozen"
        addendum["freeze_sha256"] = _addendum_digest(
            str(addendum["parent_freeze_sha256"]), addendum["answers"]
        )
        addendum["frozen_at"] = datetime.now(UTC).isoformat()
        store.save(payload)
        return {"status": "frozen", "freeze_sha256": addendum["freeze_sha256"]}

    return app


_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Relationship X-Ray</title>
<style>
body{font-family:system-ui,sans-serif;max-width:850px;margin:0 auto;padding:32px 20px;line-height:1.5;color:#181818}
button,select,textarea{font:inherit}button{padding:10px 16px;margin:8px 8px 0 0;cursor:pointer}textarea{width:100%;min-height:100px;padding:10px;box-sizing:border-box}.hidden{display:none}.card{border:1px solid #ddd;border-radius:12px;padding:20px;margin-top:18px}.field{border-top:1px solid #e7e7e7;padding:18px 0}.field:first-of-type{border-top:0}.field label{font-weight:650;display:block;margin-bottom:8px}.field select{padding:7px;min-width:210px}.hint{color:#666;font-size:.93rem;margin:6px 0 10px}.clarify{background:#fff8e8;border-left:3px solid #d79d26;padding:10px;margin-top:10px}.answer{white-space:pre-wrap;background:#f6f6f6;padding:10px;border-radius:8px;margin:6px 0}.status{font-size:.9rem;font-weight:650}.uncertain{background:#fff8e8}.unknown{background:#f2f2f2}.progress{font-size:.9rem;color:#666}.review-field{margin:8px 0 14px}.receipt{font-family:ui-monospace,monospace;overflow-wrap:anywhere}
</style></head>
<body>
<h1>Relationship X-Ray</h1>
<p>Describe one important relationship before any astrology or Human Design result is shown. Each section has separate answer fields so you do not have to remember a list of unrelated questions inside one text box.</p>
<div id="start" class="card"><label><input id="consent" type="checkbox"> I consent to storing these responses privately for this research session.</label><br><button onclick="begin()">Begin</button></div>
<div id="survey" class="card hidden"><div class="progress" id="modeLabel"></div><h2 id="title"></h2><p id="intro"></p><div id="fields"></div><button onclick="submitDomain()" id="saveButton">Save & continue</button><button onclick="cancelEdit()" id="cancelEditButton" class="hidden">Cancel edit</button><p><small>Your private resume token is stored only in this browser.</small></p></div>
<div id="review" class="card hidden"><h2 id="reviewTitle">Review before freezing</h2><p id="ambiguity"></p><div id="answers"></div><button onclick="freezeCurrent()">Freeze these answers</button></div>
<div id="done" class="card hidden"><h2>Responses frozen</h2><p id="doneText">Your answers are sealed for this pilot.</p><p class="receipt" id="digest"></p><button id="clarifyLegacy" class="hidden" onclick="startClarification()">Add structured clarification</button></div>
<script>
let sessionId=localStorage.getItem('rr_session');let token=localStorage.getItem('rr_token');let current=null;let mode='main';let editing=false;let state=null;let questionDefinitions={};
const statuses=[['','Choose one…'],['clear','Clear enough'],['mixed','Mixed / both'],['context_dependent','Depends on context or time'],['unknown','I don\'t know'],['not_applicable','Not applicable']];
async function begin(){if(!document.getElementById('consent').checked)return alert('Consent is required.');const r=await fetch('/api/sessions',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({consent_to_store_responses:true})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not start');sessionId=d.session_id;token=d.resume_token;localStorage.setItem('rr_session',sessionId);localStorage.setItem('rr_token',token);mode='main';showQuestion(d.next_question)}
function showQuestion(q,existing=null){document.getElementById('start').classList.add('hidden');document.getElementById('review').classList.add('hidden');document.getElementById('done').classList.add('hidden');document.getElementById('survey').classList.remove('hidden');current=q;questionDefinitions[q.id]=q;document.getElementById('modeLabel').textContent=(mode==='clarification'?'Clarification addendum · ':'')+q.title;document.getElementById('title').textContent=q.title;document.getElementById('intro').textContent=q.intro;document.getElementById('fields').innerHTML=q.fields.map(f=>fieldHtml(f,existing)).join('');document.getElementById('saveButton').textContent=editing?'Save changes':'Save & continue';document.getElementById('cancelEditButton').classList.toggle('hidden',!editing);q.fields.forEach(f=>toggleClarification(f.id))}
function fieldHtml(f,existing){const old=existing&&existing.fields?existing.fields.find(x=>x.field_id===f.id):null;const st=old?old.status:'';const ans=old?old.answer:'';const cl=old?old.clarification:'';return '<div class="field" id="wrap_'+f.id+'"><label>'+escapeHtml(f.label)+'</label><div class="hint">'+escapeHtml(f.placeholder)+'</div><select id="status_'+f.id+'" onchange="toggleClarification(\''+f.id+'\')">'+statuses.map(x=>'<option value="'+x[0]+'" '+(x[0]===st?'selected':'')+'>'+escapeHtml(x[1])+'</option>').join('')+'</select><textarea id="answer_'+f.id+'" placeholder="Your answer">'+escapeHtml(ans)+'</textarea><div id="clarify_'+f.id+'" class="clarify hidden"><div class="hint">'+escapeHtml(f.clarification_prompt)+'</div><textarea id="clarification_'+f.id+'" placeholder="Clarify the difference or context">'+escapeHtml(cl)+'</textarea></div></div>'}
function toggleClarification(id){const st=document.getElementById('status_'+id).value;const box=document.getElementById('clarify_'+id);box.classList.toggle('hidden',!(st==='mixed'||st==='context_dependent'));document.getElementById('wrap_'+id).classList.toggle('uncertain',st==='mixed'||st==='context_dependent');document.getElementById('wrap_'+id).classList.toggle('unknown',st==='unknown'||st==='not_applicable')}
function collectFields(){return current.fields.map(f=>({field_id:f.id,status:document.getElementById('status_'+f.id).value,answer:document.getElementById('answer_'+f.id).value.trim(),clarification:document.getElementById('clarification_'+f.id)?document.getElementById('clarification_'+f.id).value.trim():''}))}
async function submitDomain(){const fields=collectFields();if(fields.some(x=>!x.status))return alert('Choose a status for every field.');for(const x of fields){if(['clear','mixed','context_dependent'].includes(x.status)&&!x.answer)return alert('Write an answer for each clear/mixed/context-dependent field, or mark it unknown/not applicable.');if(['mixed','context_dependent'].includes(x.status)&&!x.clarification)return alert('Please clarify every field marked mixed or context-dependent.')}const base='/api/sessions/'+sessionId+(mode==='clarification'?'/clarification':'')+'/answers';const url=editing?base+'/'+encodeURIComponent(current.id):base;const r=await fetch(url,{method:editing?'PUT':'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token,question_id:current.id,field_answers:fields})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not save');if(editing){editing=false;return loadReview()}if(d.next_question)showQuestion(d.next_question);else loadReview()}
async function loadState(){const r=await fetch('/api/sessions/'+sessionId+'?token='+encodeURIComponent(token));const d=await r.json();if(!r.ok)throw new Error(d.detail||'Could not load session');state=d;return d}
async function loadReview(){const d=await loadState();document.getElementById('survey').classList.add('hidden');document.getElementById('done').classList.add('hidden');document.getElementById('review').classList.remove('hidden');const list=mode==='clarification'?d.clarification_addendum.answers:d.answers;document.getElementById('reviewTitle').textContent=mode==='clarification'?'Review clarification addendum':'Review before freezing';let mixed=0,unknown=0;for(const a of list){if(a.fields)for(const f of a.fields){if(f.status==='mixed'||f.status==='context_dependent')mixed++;if(f.status==='unknown')unknown++}}document.getElementById('ambiguity').textContent=(mixed?'You explicitly marked '+mixed+' field(s) mixed/context-dependent; their clarification text will be preserved. ':'')+(unknown?unknown+' field(s) remain genuinely unknown, which is allowed. ':'')+'Edit anything that still feels misleading before freezing.';document.getElementById('answers').innerHTML=list.map((a,i)=>reviewHtml(a,i)).join('')}
function reviewHtml(a,i){if(!a.fields)return '<div class="card"><h3>'+(i+1)+'. '+escapeHtml(a.question_id)+'</h3><div class="answer">'+escapeHtml(a.answer||'')+'</div></div>';return '<div class="card"><h3>'+(i+1)+'. '+escapeHtml(a.question_id)+'</h3>'+a.fields.map(f=>'<div class="review-field"><div class="status">'+escapeHtml(f.field_id)+' · '+escapeHtml(f.status)+'</div><div class="answer">'+escapeHtml(f.answer||'(no narrative answer)')+'</div>'+(f.clarification?'<div class="answer uncertain"><strong>Clarification:</strong> '+escapeHtml(f.clarification)+'</div>':'')+'</div>').join('')+'<button onclick="editDomain(\''+escapeHtml(a.question_id)+'\')">Edit this section</button></div>'}
async function editDomain(qid){const d=await loadState();const list=mode==='clarification'?d.clarification_addendum.answers:d.answers;const existing=list.find(a=>a.question_id===qid);const q=await fetchQuestionDefinition(qid);editing=true;showQuestion(q,existing)}
async function fetchQuestionDefinition(qid){if(questionDefinitions[qid])return questionDefinitions[qid];const r=await fetch('/api/questions/'+encodeURIComponent(qid));const d=await r.json();if(!r.ok)throw new Error(d.detail||'Could not load question');questionDefinitions[qid]=d;return d}
function cancelEdit(){editing=false;loadReview()}
async function freezeCurrent(){const path='/api/sessions/'+sessionId+(mode==='clarification'?'/clarification':'')+'/freeze';const r=await fetch(path,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not freeze');showDone(d.freeze_sha256,mode==='clarification')}
function showDone(receipt,isAddendum=false,canClarify=false){document.getElementById('start').classList.add('hidden');document.getElementById('survey').classList.add('hidden');document.getElementById('review').classList.add('hidden');document.getElementById('done').classList.remove('hidden');document.getElementById('doneText').textContent=isAddendum?'Your clarification addendum is frozen separately from the original response.':'Your answers are sealed. A later classifier/reveal layer may use this frozen record without changing it.';document.getElementById('digest').textContent=(isAddendum?'Clarification freeze receipt: ':'Freeze receipt: ')+receipt;document.getElementById('clarifyLegacy').classList.toggle('hidden',!canClarify)}
async function startClarification(){const r=await fetch('/api/sessions/'+sessionId+'/clarification',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not start clarification');mode='clarification';editing=false;showQuestion(d.next_question)}
function escapeHtml(s){return String(s??'').replace(/[&<>'\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','\"':'&quot;'}[c]))}
async function resume(){if(!(sessionId&&token))return;try{const d=await loadState();if(d.status==='frozen'){if(d.clarification_addendum&&d.clarification_addendum.status==='in_progress'){mode='clarification';if(d.clarification_next_question)showQuestion(d.clarification_next_question);else loadReview();return}if(d.clarification_addendum&&d.clarification_addendum.status==='frozen'){showDone(d.clarification_addendum.freeze_sha256,true,false);return}showDone(d.freeze_sha256,false,d.can_start_clarification);return}mode='main';if(d.next_question)showQuestion(d.next_question);else loadReview()}catch(e){}}
resume();
</script></body></html>"""
