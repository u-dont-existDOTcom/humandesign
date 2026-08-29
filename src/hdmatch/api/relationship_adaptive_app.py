"""Adaptive wrapper around the public relationship capture service.

Adds a v2 single-construct field registry, live chart-blind answer quality,
bounded semantic clarification, visible progress, and targeted clarification for
legacy frozen sessions. No chart/model prediction is available to this layer.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field

import hdmatch.api.relationship_public_app as base_app
from hdmatch.api.relationship_public_app import (
    CreateSessionRequest,
    FreezeRequest,
    GuidedRegistry,
    RelationshipFileStore,
    _legacy_session,
    _load_guided_registry,
    _next_question,
    _public_question,
)
from hdmatch.relationship.answer_audit import (
    AUDIT_VERSION,
    ClarificationItem,
    FieldEvidence,
    FieldStatus,
    assess_field_answer,
    build_clarification_queue,
    legacy_clarification_queue,
)
from hdmatch.relationship.questionnaire import (
    RelationshipQuestionnaireSpec,
    load_relationship_questionnaire,
)

MAX_CLARIFICATIONS = 6
MAX_LEGACY_CLARIFICATIONS = 8


class QualityRequest(BaseModel):
    field_id: str = Field(min_length=1)
    status: FieldStatus
    answer: str = Field(default="", max_length=12000)
    clarification: str = Field(default="", max_length=12000)


class ClarificationAnswerRequest(BaseModel):
    token: str = Field(min_length=16)
    clarification_id: str = Field(min_length=1)
    status: str = Field(pattern="^(answered|unknown)$")
    answer: str = Field(default="", max_length=12000)


def _field_prompts(registry: GuidedRegistry) -> dict[str, str]:
    return {
        field.id: field.label
        for question in registry.questions.values()
        for field in question.fields
    }


def _field_question_map(registry: GuidedRegistry) -> dict[str, tuple[str, str]]:
    return {
        field.id: (question_id, field.label)
        for question_id, question in registry.questions.items()
        for field in question.fields
    }


def _flatten_evidence(answers: list[dict[str, Any]]) -> tuple[FieldEvidence, ...]:
    evidence: list[FieldEvidence] = []
    for record in answers:
        question_id = str(record["question_id"])
        for raw in cast(list[dict[str, Any]], record.get("fields", [])):
            evidence.append(
                FieldEvidence(
                    question_id=question_id,
                    field_id=str(raw["field_id"]),
                    status=cast(FieldStatus, str(raw["status"])),
                    answer=str(raw.get("answer", "")),
                    clarification=str(raw.get("clarification", "")),
                )
            )
    return tuple(evidence)


def _audit_answered_ids(audit: dict[str, Any]) -> set[str]:
    return {
        str(row["clarification_id"])
        for row in cast(list[dict[str, Any]], audit.get("answers", []))
    }


def _next_audit_item(audit: dict[str, Any]) -> ClarificationItem | None:
    answered = _audit_answered_ids(audit)
    for raw in cast(list[dict[str, Any]], audit.get("queue", [])):
        item = ClarificationItem.model_validate(raw)
        if item.id not in answered:
            return item
    return None


def _audit_progress(audit: dict[str, Any], *, cap: int) -> dict[str, Any]:
    total = len(cast(list[dict[str, Any]], audit.get("queue", [])))
    completed = len(cast(list[dict[str, Any]], audit.get("answers", [])))
    percent = 100 if total == 0 else 85 + round(15 * completed / total)
    return {
        "percent": min(percent, 100),
        "label": (
            "Core complete · no extra clarification needed"
            if total == 0
            else f"Clarification {min(completed + 1, total)} of {total} · hard cap {cap}"
        ),
        "clarifications_completed": completed,
        "clarifications_total": total,
        "clarification_cap": cap,
    }


def _public_audit_state(audit: dict[str, Any], *, cap: int) -> dict[str, Any]:
    item = _next_audit_item(audit)
    return {
        "complete": item is None,
        "next_clarification": item.model_dump() if item else None,
        "answers": audit.get("answers", []),
        "field_quality": audit.get("field_quality", []),
        "progress": _audit_progress(audit, cap=cap),
        "audit_version": audit.get("audit_version", AUDIT_VERSION),
    }


def _build_core_audit(
    payload: dict[str, Any],
    registry: GuidedRegistry,
) -> dict[str, Any]:
    evidence = _flatten_evidence(cast(list[dict[str, Any]], payload["answers"]))
    queue = build_clarification_queue(
        evidence,
        field_prompts=_field_prompts(registry),
        max_items=MAX_CLARIFICATIONS,
    )
    qualities = [
        {
            "question_id": row.question_id,
            "field_id": row.field_id,
            **assess_field_answer(
                row.field_id,
                row.status,
                row.answer,
                row.clarification,
            ).model_dump(),
        }
        for row in evidence
    ]
    return {
        "mode": "core_v2",
        "audit_version": AUDIT_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "queue": [item.model_dump() for item in queue],
        "answers": [],
        "field_quality": qualities,
    }


def _core_complete(payload: dict[str, Any], spec: RelationshipQuestionnaireSpec) -> bool:
    answered = {
        str(row["question_id"])
        for row in cast(list[dict[str, Any]], payload["answers"])
    }
    return set(spec.core_question_ids).issubset(answered)


def _addendum_digest(addendum: dict[str, Any]) -> str:
    frozen = {
        "parent_freeze_sha256": addendum["parent_freeze_sha256"],
        "audit_version": addendum["audit_version"],
        "queue": addendum["queue"],
        "answers": addendum["answers"],
    }
    encoded = json.dumps(frozen, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def create_relationship_adaptive_app_from_env() -> FastAPI:
    os.environ.setdefault(
        "HDMATCH_RELATIONSHIP_GUIDED_FIELDS",
        "reference/relationship/relationship_guided_response_fields_v2.json",
    )
    questionnaire_path = Path(
        os.environ.get(
            "HDMATCH_RELATIONSHIP_QUESTIONNAIRE",
            "reference/relationship/relationship_dynamic_questionnaire_v1.json",
        )
    )
    guided_path = Path(os.environ["HDMATCH_RELATIONSHIP_GUIDED_FIELDS"])
    store_value = os.environ.get("HDMATCH_RELATIONSHIP_STORE", "").strip()
    if not store_value:
        raise RuntimeError(
            "HDMATCH_RELATIONSHIP_STORE is required; point it at a private persistent volume"
        )

    spec = load_relationship_questionnaire(questionnaire_path)
    registry = _load_guided_registry(guided_path, spec)
    store = RelationshipFileStore(Path(store_value))

    base_app._HTML = _HTML
    app = base_app.create_relationship_public_app_from_env()
    app.title = "Relationship X-Ray Adaptive Pilot"
    app.version = "0.3.0"

    @app.middleware("http")
    async def protect_freeze_and_invalidate_edits(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        freeze_match = re.fullmatch(r"/api/sessions/([^/]+)/freeze", request.url.path)
        edit_match = re.fullmatch(r"/api/sessions/([^/]+)/answers/([^/]+)", request.url.path)

        token: str | None = None
        session_id: str | None = None
        if request.method in {"POST", "PUT"} and (freeze_match or edit_match):
            try:
                body_obj = cast(dict[str, Any], await request.json())
                token = str(body_obj.get("token", ""))
            except (json.JSONDecodeError, TypeError, ValueError):
                token = None

        if freeze_match and request.method == "POST" and token:
            session_id = freeze_match.group(1)
            payload = store.read(session_id, token)
            if payload.get("status") == "in_progress" and _core_complete(payload, spec):
                audit = payload.get("semantic_audit")
                if not isinstance(audit, dict):
                    raise HTTPException(
                        status_code=409,
                        detail="run the chart-blind semantic audit before freezing",
                    )
                if _next_audit_item(audit) is not None:
                    raise HTTPException(
                        status_code=409,
                        detail="complete the targeted clarifications before freezing",
                    )

        response = await call_next(request)

        if edit_match and request.method == "PUT" and token and response.status_code < 300:
            session_id = edit_match.group(1)
            payload = store.read(session_id, token)
            payload["semantic_audit"] = None
            payload["semantic_audit_invalidated_at"] = datetime.now(UTC).isoformat()
            store.save(payload)

        return response

    @app.post("/api/adaptive/sessions")
    def create_adaptive_session(request: CreateSessionRequest) -> dict[str, Any]:
        if not request.consent_to_store_responses:
            raise HTTPException(status_code=400, detail="consent is required")
        payload, token = store.create()
        payload["format_version"] = "guided-fields-v2"
        payload["semantic_audit_version"] = AUDIT_VERSION
        payload["semantic_audit"] = None
        store.save(payload)
        question = _next_question(spec, payload)
        return {
            "session_id": payload["session_id"],
            "resume_token": token,
            "next_question": _public_question(question, registry) if question else None,
            "progress": {
                "percent": 0,
                "label": (
                    f"Core section 1 of 6 · at most {MAX_CLARIFICATIONS} "
                    "clarifications afterward"
                ),
            },
        }

    @app.post("/api/quality")
    def quality(request: QualityRequest) -> dict[str, Any]:
        return assess_field_answer(
            request.field_id,
            request.status,
            request.answer,
            request.clarification,
        ).model_dump()

    @app.post("/api/sessions/{session_id}/semantic-audit")
    def semantic_audit(session_id: str, request: FreezeRequest) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        if not _core_complete(payload, spec):
            raise HTTPException(status_code=409, detail="complete all six core sections first")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict):
            audit = _build_core_audit(payload, registry)
            payload["semantic_audit"] = audit
            store.save(payload)
        return _public_audit_state(audit, cap=MAX_CLARIFICATIONS)

    @app.post("/api/sessions/{session_id}/semantic-audit/answers")
    def submit_semantic_clarification(
        session_id: str,
        request: ClarificationAnswerRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "in_progress":
            raise HTTPException(status_code=409, detail="session is already frozen")
        audit = payload.get("semantic_audit")
        if not isinstance(audit, dict):
            raise HTTPException(status_code=409, detail="semantic audit has not been generated")
        expected = _next_audit_item(audit)
        if expected is None:
            raise HTTPException(status_code=409, detail="no clarification is pending")
        if request.clarification_id != expected.id:
            raise HTTPException(status_code=409, detail="answer does not match pending clarification")
        answer = request.answer.strip()
        if request.status == "answered" and not answer:
            raise HTTPException(status_code=422, detail="write a clarification or mark it unknown")
        cast(list[dict[str, Any]], audit["answers"]).append(
            {
                "clarification_id": expected.id,
                "source_question_id": expected.source_question_id,
                "source_field_id": expected.source_field_id,
                "reason_code": expected.reason_code,
                "status": request.status,
                "answer": answer,
                "answered_at": datetime.now(UTC).isoformat(),
            }
        )
        store.save(payload)
        return _public_audit_state(audit, cap=MAX_CLARIFICATIONS)

    @app.post("/api/sessions/{session_id}/legacy-targeted-audit")
    def start_legacy_targeted_audit(
        session_id: str,
        request: FreezeRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        if payload["status"] != "frozen" or not _legacy_session(payload):
            raise HTTPException(
                status_code=409,
                detail="targeted clarification is only for frozen legacy-format sessions",
            )
        addendum = payload.get("semantic_legacy_addendum")
        if not isinstance(addendum, dict):
            broad = {
                str(row["question_id"]): str(row.get("answer", ""))
                for row in cast(list[dict[str, Any]], payload["answers"])
            }
            queue = legacy_clarification_queue(
                broad,
                field_questions=_field_question_map(registry),
                max_items=MAX_LEGACY_CLARIFICATIONS,
            )
            addendum = {
                "mode": "legacy_targeted_v2",
                "audit_version": AUDIT_VERSION,
                "status": "in_progress",
                "parent_freeze_sha256": payload["freeze_sha256"],
                "generated_at": datetime.now(UTC).isoformat(),
                "queue": [item.model_dump() for item in queue],
                "answers": [],
                "freeze_sha256": None,
            }
            payload["semantic_legacy_addendum"] = addendum
            store.save(payload)
        state = _public_audit_state(addendum, cap=MAX_LEGACY_CLARIFICATIONS)
        state["status"] = addendum["status"]
        state["freeze_sha256"] = addendum.get("freeze_sha256")
        return state

    @app.post("/api/sessions/{session_id}/legacy-targeted-audit/answers")
    def submit_legacy_targeted_audit(
        session_id: str,
        request: ClarificationAnswerRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("semantic_legacy_addendum")
        if not isinstance(addendum, dict) or addendum.get("status") != "in_progress":
            raise HTTPException(status_code=409, detail="targeted clarification is not active")
        expected = _next_audit_item(addendum)
        if expected is None:
            raise HTTPException(status_code=409, detail="no targeted clarification is pending")
        if request.clarification_id != expected.id:
            raise HTTPException(status_code=409, detail="answer does not match pending clarification")
        answer = request.answer.strip()
        if request.status == "answered" and not answer:
            raise HTTPException(status_code=422, detail="write a clarification or mark it unknown")
        cast(list[dict[str, Any]], addendum["answers"]).append(
            {
                "clarification_id": expected.id,
                "source_question_id": expected.source_question_id,
                "source_field_id": expected.source_field_id,
                "reason_code": expected.reason_code,
                "status": request.status,
                "answer": answer,
                "answered_at": datetime.now(UTC).isoformat(),
            }
        )
        store.save(payload)
        state = _public_audit_state(addendum, cap=MAX_LEGACY_CLARIFICATIONS)
        state["status"] = addendum["status"]
        return state

    @app.post("/api/sessions/{session_id}/legacy-targeted-audit/freeze")
    def freeze_legacy_targeted_audit(
        session_id: str,
        request: FreezeRequest,
    ) -> dict[str, Any]:
        payload = store.read(session_id, request.token)
        addendum = payload.get("semantic_legacy_addendum")
        if not isinstance(addendum, dict):
            raise HTTPException(status_code=409, detail="no targeted clarification addendum")
        if addendum.get("status") == "frozen":
            return {"status": "frozen", "freeze_sha256": addendum["freeze_sha256"]}
        if _next_audit_item(addendum) is not None:
            raise HTTPException(status_code=409, detail="complete targeted clarifications first")
        addendum["status"] = "frozen"
        addendum["freeze_sha256"] = _addendum_digest(addendum)
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
body{font-family:system-ui,sans-serif;max-width:900px;margin:0 auto;padding:28px 20px;line-height:1.5;color:#181818}
button,select,textarea{font:inherit}button{padding:10px 16px;margin:8px 8px 0 0;cursor:pointer}
textarea{width:100%;min-height:82px;padding:10px;box-sizing:border-box}.hidden{display:none}
.card{border:1px solid #ddd;border-radius:12px;padding:20px;margin-top:18px}.field{border-top:1px solid #e7e7e7;padding:18px 0}.field:first-of-type{border-top:0}
.field label{font-weight:650;display:block;margin-bottom:6px}.field select{padding:7px;min-width:205px}.hint{color:#666;font-size:.92rem;margin:4px 0 8px}
.clarify{background:#fff8e8;border-left:3px solid #d79d26;padding:10px;margin-top:8px}.answer{white-space:pre-wrap;background:#f6f6f6;padding:10px;border-radius:8px;margin:6px 0}
.progress-shell{height:12px;background:#eee;border-radius:999px;overflow:hidden;margin:10px 0 5px}.progress-bar{height:100%;background:#222;width:0%;transition:width .2s}.progress-label{font-size:.88rem;color:#555}
.quality{margin-top:7px;font-size:.86rem}.quality-track{height:7px;background:#eee;border-radius:999px;overflow:hidden}.quality-fill{height:100%;background:#555;width:0%;transition:width .15s}.quality-hint{color:#666;margin-top:3px}
.review-field{margin:8px 0 14px}.receipt{font-family:ui-monospace,monospace;overflow-wrap:anywhere}.badge{display:inline-block;padding:2px 7px;border-radius:999px;background:#eee;font-size:.8rem;margin-left:6px}
</style></head>
<body>
<h1>Relationship X-Ray</h1>
<p>Six finite sections map one relationship before any astrology or Human Design result is shown. Each distinction has its own field. After the core there are at most six targeted clarifications.</p>
<div id="progressWrap" class="hidden"><div class="progress-shell"><div id="progressBar" class="progress-bar"></div></div><div id="progressLabel" class="progress-label"></div></div>
<div id="start" class="card"><label><input id="consent" type="checkbox"> I consent to storing these responses privately for this research session.</label><br><button onclick="begin()">Begin</button></div>
<div id="survey" class="card hidden"><h2 id="title"></h2><p id="intro"></p><div id="fields"></div><button onclick="submitCore()" id="saveButton">Save & continue</button><button onclick="cancelEdit()" id="cancelEditButton" class="hidden">Cancel edit</button><p><small>Clarity meters score answer usability only. They never compare your answer with an Astro/HD prediction.</small></p></div>
<div id="clarification" class="card hidden"><h2>Targeted clarification</h2><p id="clarificationPrompt"></p><textarea id="clarificationAnswer" placeholder="Clarify this point without changing your underlying answer."></textarea><br><button onclick="submitClarification(false)">Save clarification</button><button onclick="submitClarification(true)">I genuinely don't know</button></div>
<div id="review" class="card hidden"><h2>Review before freezing</h2><p>Explicit unknowns are valid. Edit anything that still feels misleading. Editing a core section causes the semantic audit to be rerun.</p><div id="answers"></div><div id="clarificationReview"></div><button id="freezeButton" onclick="freezeCurrent()">Freeze these answers</button></div>
<div id="done" class="card hidden"><h2>Responses frozen</h2><p id="doneText">Your answers are sealed.</p><p class="receipt" id="digest"></p><button id="clarifyLegacy" class="hidden" onclick="startLegacyAudit()">Add targeted clarification</button></div>
<script>
let sessionId=localStorage.getItem('rr_session');let token=localStorage.getItem('rr_token');let current=null;let editing=false;let legacyAudit=false;let qualityTimers={};let coreAnswered=0;
const statuses=[['','Choose one…'],['clear','Clear enough'],['mixed','Mixed / both'],['context_dependent','Depends on context or time'],['unknown','I don\'t know'],['not_applicable','Not applicable']];
function hideAll(){['start','survey','clarification','review','done'].forEach(id=>document.getElementById(id).classList.add('hidden'))}
function setProgress(p){if(!p)return;document.getElementById('progressWrap').classList.remove('hidden');document.getElementById('progressBar').style.width=p.percent+'%';document.getElementById('progressLabel').textContent=p.label}
function coreProgress(n){coreAnswered=n;setProgress({percent:Math.round(85*n/6),label:(n<6?'Core section '+Math.min(n+1,6)+' of 6 · at most 6 targeted clarifications afterward':'Core complete · checking for targeted clarification')})}
async function begin(){if(!document.getElementById('consent').checked)return alert('Consent is required.');const r=await fetch('/api/adaptive/sessions',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({consent_to_store_responses:true})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not start');sessionId=d.session_id;token=d.resume_token;localStorage.setItem('rr_session',sessionId);localStorage.setItem('rr_token',token);coreProgress(0);showQuestion(d.next_question)}
function showQuestion(q,existing=null){hideAll();document.getElementById('survey').classList.remove('hidden');current=q;document.getElementById('title').textContent=q.title||q.prompt;document.getElementById('intro').textContent=q.intro||'';document.getElementById('fields').innerHTML=q.fields.map(f=>fieldHtml(f,existing)).join('');document.getElementById('saveButton').textContent=editing?'Save changes':'Save & continue';document.getElementById('cancelEditButton').classList.toggle('hidden',!editing);q.fields.forEach(f=>{toggleClarification(f.id);scheduleQuality(f.id)})}
function fieldHtml(f,existing){const old=existing&&existing.fields?existing.fields.find(x=>x.field_id===f.id):null;const st=old?old.status:'';const ans=old?old.answer:'';const cl=old?old.clarification:'';return '<div class="field"><label>'+esc(f.label)+'</label><div class="hint">'+esc(f.placeholder)+'</div><select id="status_'+f.id+'" onchange="toggleClarification(\''+f.id+'\');scheduleQuality(\''+f.id+'\')">'+statuses.map(x=>'<option value="'+x[0]+'" '+(x[0]===st?'selected':'')+'>'+esc(x[1])+'</option>').join('')+'</select><textarea id="answer_'+f.id+'" oninput="scheduleQuality(\''+f.id+'\')" placeholder="Your answer">'+esc(ans)+'</textarea><div id="clarify_'+f.id+'" class="clarify hidden"><div class="hint">'+esc(f.clarification_prompt)+'</div><textarea id="clarification_'+f.id+'" oninput="scheduleQuality(\''+f.id+'\')" placeholder="Clarify the difference or context">'+esc(cl)+'</textarea></div><div class="quality"><div class="quality-track"><div id="qualityFill_'+f.id+'" class="quality-fill"></div></div><div id="qualityText_'+f.id+'" class="quality-hint">Choose a status and start typing.</div></div></div>'}
function toggleClarification(id){const st=document.getElementById('status_'+id).value;document.getElementById('clarify_'+id).classList.toggle('hidden',!(st==='mixed'||st==='context_dependent'))}
function scheduleQuality(id){clearTimeout(qualityTimers[id]);qualityTimers[id]=setTimeout(()=>updateQuality(id),300)}
async function updateQuality(id){const st=document.getElementById('status_'+id).value;if(!st)return;const ans=document.getElementById('answer_'+id).value;const cl=document.getElementById('clarification_'+id)?document.getElementById('clarification_'+id).value:'';const r=await fetch('/api/quality',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({field_id:id,status:st,answer:ans,clarification:cl})});const d=await r.json();if(!r.ok)return;document.getElementById('qualityFill_'+id).style.width=d.score+'%';document.getElementById('qualityText_'+id).innerHTML='<strong>Clarity '+d.score+'/100</strong>'+(d.hints&&d.hints.length?' · '+esc(d.hints[0]):'')}
function collectFields(){return current.fields.map(f=>({field_id:f.id,status:document.getElementById('status_'+f.id).value,answer:document.getElementById('answer_'+f.id).value.trim(),clarification:document.getElementById('clarification_'+f.id)?document.getElementById('clarification_'+f.id).value.trim():''}))}
async function submitCore(){const fields=collectFields();if(fields.some(x=>!x.status))return alert('Choose a status for every field.');for(const x of fields){if(['clear','mixed','context_dependent'].includes(x.status)&&!x.answer)return alert('Write an answer or mark that field unknown/not applicable.');if(['mixed','context_dependent'].includes(x.status)&&!x.clarification)return alert('Clarify every field marked mixed or context-dependent.')}const base='/api/sessions/'+sessionId+'/answers';const r=await fetch(editing?base+'/'+encodeURIComponent(current.id):base,{method:editing?'PUT':'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token,question_id:current.id,field_answers:fields})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not save');if(editing){editing=false;return startAudit()}coreProgress(d.answered_count);if(d.next_question)showQuestion(d.next_question);else startAudit()}
async function startAudit(){const r=await fetch('/api/sessions/'+sessionId+'/semantic-audit',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not audit answers');setProgress(d.progress);if(d.next_clarification){legacyAudit=false;showAuditQuestion(d.next_clarification)}else loadReview(d)}
function showAuditQuestion(q){hideAll();document.getElementById('clarification').classList.remove('hidden');current=q;document.getElementById('clarificationPrompt').textContent=q.prompt;document.getElementById('clarificationAnswer').value=''}
async function submitClarification(unknown){const path=legacyAudit?'/api/sessions/'+sessionId+'/legacy-targeted-audit/answers':'/api/sessions/'+sessionId+'/semantic-audit/answers';const answer=document.getElementById('clarificationAnswer').value.trim();if(!unknown&&!answer)return alert('Write a clarification or choose I genuinely don\'t know.');const r=await fetch(path,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token,clarification_id:current.id,status:unknown?'unknown':'answered',answer})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not save clarification');setProgress(d.progress);if(d.next_clarification)showAuditQuestion(d.next_clarification);else{if(legacyAudit)loadLegacyReview(d);else loadReview(d)}}
async function loadState(){const r=await fetch('/api/sessions/'+sessionId+'?token='+encodeURIComponent(token));const d=await r.json();if(!r.ok)throw new Error(d.detail||'Could not load');return d}
async function loadReview(auditState=null){const d=await loadState();if(!auditState){const r=await fetch('/api/sessions/'+sessionId+'/semantic-audit',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});auditState=await r.json();if(!r.ok)return alert(auditState.detail||'Could not audit answers')}hideAll();document.getElementById('review').classList.remove('hidden');setProgress(auditState.progress);document.getElementById('answers').innerHTML=d.answers.map((a,i)=>reviewCore(a,i)).join('');document.getElementById('clarificationReview').innerHTML=(auditState.answers||[]).map((a,i)=>'<div class="card"><strong>Clarification '+(i+1)+'</strong><div class="answer">'+esc(a.answer||'(unknown)')+'</div></div>').join('');document.getElementById('freezeButton').textContent='Freeze these answers';document.getElementById('freezeButton').onclick=freezeCurrent}
function reviewCore(a,i){if(!a.fields)return '<div class="card"><h3>'+(i+1)+'. '+esc(a.question_id)+'</h3><div class="answer">'+esc(a.answer||'')+'</div></div>';return '<div class="card"><h3>'+(i+1)+'. '+esc(a.question_id)+'</h3>'+a.fields.map(f=>'<div class="review-field"><strong>'+esc(f.field_id)+'</strong><span class="badge">'+esc(f.status)+'</span><div class="answer">'+esc(f.answer||'(no narrative answer)')+'</div>'+(f.clarification?'<div class="answer"><strong>Clarification:</strong> '+esc(f.clarification)+'</div>':'')+'</div>').join('')+'<button onclick="editCore(\''+esc(a.question_id)+'\')">Edit this section</button></div>'}
async function editCore(qid){const d=await loadState();const existing=d.answers.find(a=>a.question_id===qid);const r=await fetch('/api/questions/'+encodeURIComponent(qid));const q=await r.json();editing=true;showQuestion(q,existing)}
function cancelEdit(){editing=false;loadReview()}
async function freezeCurrent(){const r=await fetch('/api/sessions/'+sessionId+'/freeze',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not freeze');showDone(d.freeze_sha256,false,false)}
function showDone(receipt,isAddendum,canClarify){hideAll();document.getElementById('progressWrap').classList.add('hidden');document.getElementById('done').classList.remove('hidden');document.getElementById('doneText').textContent=isAddendum?'Your targeted clarification addendum is frozen separately from the original response.':'Your answers are sealed.';document.getElementById('digest').textContent=(isAddendum?'Clarification freeze receipt: ':'Freeze receipt: ')+receipt;document.getElementById('clarifyLegacy').classList.toggle('hidden',!canClarify)}
async function startLegacyAudit(){const r=await fetch('/api/sessions/'+sessionId+'/legacy-targeted-audit',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not start targeted clarification');legacyAudit=true;setProgress(d.progress);if(d.next_clarification)showAuditQuestion(d.next_clarification);else loadLegacyReview(d)}
function loadLegacyReview(d){hideAll();document.getElementById('review').classList.remove('hidden');setProgress(d.progress);document.getElementById('answers').innerHTML='<p>Your original frozen response remains unchanged.</p>';document.getElementById('clarificationReview').innerHTML=(d.answers||[]).map((a,i)=>'<div class="card"><strong>Targeted clarification '+(i+1)+'</strong><div class="answer">'+esc(a.answer||'(unknown)')+'</div></div>').join('');document.getElementById('freezeButton').textContent='Freeze clarification addendum';document.getElementById('freezeButton').onclick=freezeLegacy}
async function freezeLegacy(){const r=await fetch('/api/sessions/'+sessionId+'/legacy-targeted-audit/freeze',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token})});const d=await r.json();if(!r.ok)return alert(d.detail||'Could not freeze clarification');showDone(d.freeze_sha256,true,false)}
function esc(s){return String(s??'').replace(/[&<>'\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','\"':'&quot;'}[c]))}
async function resume(){if(!(sessionId&&token))return;try{const d=await loadState();if(d.status==='frozen'){showDone(d.freeze_sha256,false,d.legacy_format);return}coreProgress(d.answers.length);if(d.next_question)showQuestion(d.next_question);else startAudit()}catch(e){}}
resume();
</script></body></html>"""
