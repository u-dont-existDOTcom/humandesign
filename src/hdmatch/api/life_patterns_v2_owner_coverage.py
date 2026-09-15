"""Standardized coverage layer for the adaptive Life Patterns development interview.

The scientific checklist is a versioned set of required behavioral domains and coverage states.
Question wording remains adaptive so already-observed material is not re-asked mechanically.
The runtime stays target-theory-blind: it never receives a participant chart, expected answer,
score, or target-model mapping.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import (
    ConversationTurnRequest,
    CreateConversationSessionResponse,
    OwnerConversationModel,
)
from .life_patterns_v2_owner_pattern_first import TemporaryModelProviderError
from .life_patterns_v2_owner_reasoning import (
    ADAPTIVE_HTML,
    ADAPTIVE_OPENING,
    AdaptivePatternFirstOpenAIConversationModel,
    AdaptiveRefinablePatternSession,
)

CoverageStatus = Literal[
    "unassessed",
    "partial",
    "sufficient",
    "unknown",
    "inapplicable",
    "declined",
]

COVERAGE_BLUEPRINT_VERSION = "life-patterns-required-coverage-v1"
COVERAGE_STATUSES: tuple[CoverageStatus, ...] = (
    "unassessed",
    "partial",
    "sufficient",
    "unknown",
    "inapplicable",
    "declined",
)
COVERAGE_COMPLETE_STATUSES = frozenset({"sufficient", "unknown", "inapplicable", "declined"})


@dataclass(frozen=True)
class CoverageDomain:
    domain_id: str
    title: str
    definition: str
    canonical_screener: str


REQUIRED_COVERAGE_DOMAINS: tuple[CoverageDomain, ...] = (
    CoverageDomain(
        "decision_process",
        "Decision and choice process",
        "What tends to happen first when an important choice is genuinely uncertain, including immediate versus delayed clarity.",
        "When an important choice is genuinely uncertain, what usually happens first for you—something bodily or felt, a thought or reason, an urge to act, or do you usually need time before anything feels clear?",
    ),
    CoverageDomain(
        "energy_recovery",
        "Energy, work, stopping, and recovery",
        "Engagement, sustainable range, overload, stopping signals, retreat, and restoration.",
        "What tends to distinguish work that leaves you with energy from work that drains you, and how do you usually know you have reached your stopping point?",
    ),
    CoverageDomain(
        "attention_cognition_work",
        "Attention, cognition, learning, and work style",
        "Focus, interruption, learning and synthesis, persistence, novelty versus continuity, project selection, and stopping.",
        "When something really matters to you, what happens to your attention—how do you get into it, what interrupts you, and what tends to make you persist or stop?",
    ),
    CoverageDomain(
        "emotion_regulation",
        "Emotional baseline and regulation",
        "Ordinary emotional baseline, reliable triggers, intensity or duration, recovery, and interpersonal atmosphere where relevant.",
        "Across an ordinary day, what is your emotional baseline like, and what kinds of situations reliably change it or take time to recover from?",
    ),
    CoverageDomain(
        "relationships_conflict_boundaries",
        "Relationships, conflict, trust, and boundaries",
        "Closeness and reciprocity, conflict response, repair versus withdrawal, trust, and access boundaries.",
        "When a close relationship becomes tense or you stop trusting someone, what do you tend to do first, and what makes you repair, withdraw, or close the door?",
    ),
    CoverageDomain(
        "social_entry_roles",
        "Social entry, recognition, groups, and roles",
        "How the person enters social situations or roles, one-to-one versus group behavior, recognition or invitation, and leadership stance.",
        "In new groups or roles, do you usually step forward yourself, wait for an opening or recognition, get pulled in by others, or does it depend on the setting?",
    ),
    CoverageDomain(
        "communication_influence",
        "Communication and influence",
        "Communication style, persuasion capacity, directness versus adaptation, and capacity versus preferred use.",
        "When you really need another person to understand or agree with something, how do you tend to communicate—do you adapt to what will move them, state it directly, demonstrate it, or something else?",
    ),
    CoverageDomain(
        "values_purpose",
        "Values, purpose, motivation, and salience",
        "What reliably mobilizes serious effort, what feels consequential, and what can be ignored or abandoned.",
        "What kinds of problems or goals reliably become important enough that you will invest serious effort in them, and what kinds are easy for you to ignore?",
    ),
    CoverageDomain(
        "environment_body_security",
        "Environment, body, comfort, and security",
        "Sensory, environmental, bodily, material-comfort, or security conditions that materially change functioning.",
        "What conditions in your surroundings or physical baseline make a large difference to how well you function, if any?",
    ),
    CoverageDomain(
        "developmental_change",
        "Developmental continuity and change",
        "Earlier-life continuity, major shifts, learned management, compensation, and adaptations over time.",
        "Which parts of how you respond to life feel as though they were already there when you were young, and which feel learned or changed substantially over time?",
    ),
)

_DOMAIN_BY_ID = {domain.domain_id: domain for domain in REQUIRED_COVERAGE_DOMAINS}


def _blueprint_payload() -> list[dict[str, str]]:
    return [
        {
            "domain_id": domain.domain_id,
            "title": domain.title,
            "definition": domain.definition,
            "canonical_screener": domain.canonical_screener,
        }
        for domain in REQUIRED_COVERAGE_DOMAINS
    ]


COVERAGE_BLUEPRINT_SHA256 = hashlib.sha256(
    json.dumps(
        {"version": COVERAGE_BLUEPRINT_VERSION, "domains": _blueprint_payload()},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()


class CoverageSessionRequest(BaseModel):
    domain_id: str


class StandardizedCoverageOpenAIModel(AdaptivePatternFirstOpenAIConversationModel):
    """Adaptive interviewer plus a fixed target-blind coverage-assessment contract."""

    def assess_required_coverage(
        self,
        *,
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> dict[str, Any]:
        domain_ids = [domain.domain_id for domain in REQUIRED_COVERAGE_DOMAINS]
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["assessments"],
            "properties": {
                "assessments": {
                    "type": "array",
                    "minItems": len(domain_ids),
                    "maxItems": len(domain_ids),
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["domain_id", "status", "evidence_fact_ids", "reason"],
                        "properties": {
                            "domain_id": {"type": "string", "enum": domain_ids},
                            "status": {"type": "string", "enum": list(COVERAGE_STATUSES)},
                            "evidence_fact_ids": {
                                "type": "array",
                                "maxItems": 16,
                                "items": {"type": "string"},
                            },
                            "reason": {"type": "string", "minLength": 1, "maxLength": 700},
                        },
                    },
                }
            },
        }
        result = self._conversation_call_json(
            instructions=(
                "Assess standardized behavioral-domain COVERAGE only. This is measurement-process metadata, not a "
                "personality score and not a theory interpretation. Return exactly one row for every required domain. "
                "Use unassessed when there is no meaningful information; partial when there is relevant information "
                "but not yet a stable person-specific characterization; sufficient when the available participant "
                "evidence supports a narrow interpretable person-specific characterization; unknown only when the "
                "participant was actually asked or directly addressed the domain and says they do not know/cannot "
                "tell; inapplicable only when the participant indicates the domain genuinely does not apply; declined "
                "only for an explicit refusal. Never infer unknown, inapplicable, declined, or real-world absence from "
                "silence. A generic human regularity is not sufficient. Preserve self-report, direct behavioral report, "
                "and reported observer impressions as different evidence sources. Do not require a fixed number of "
                "episodes. For partial or sufficient, cite only supplied operative fact IDs that actually support the "
                "status. Do not mention or infer any external theory, chart, target, score, or expected answer.\n\n"
                "REQUIRED DOMAINS:\n"
                + "\n".join(
                    f"- {domain.domain_id}: {domain.definition}"
                    for domain in REQUIRED_COVERAGE_DOMAINS
                )
            ),
            payload={
                "operative_facts": [
                    {
                        "fact_id": fact.fact_id,
                        "assertion_type": fact.assertion_type,
                        "proposition": fact.proposition,
                    }
                    for fact in operative_facts
                ],
                "recent_conversation": list(recent_conversation[-30:]),
            },
            schema=schema,
            effort="medium",
            max_output_tokens=2200,
            schema_name="life_patterns_required_coverage_v1",
        )
        return result


def _normalize_coverage(
    raw: dict[str, Any], *, operative_facts: tuple[Any, ...]
) -> dict[str, Any]:
    known_fact_ids = {fact.fact_id for fact in operative_facts}
    raw_rows = raw.get("assessments", [])
    row_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(raw_rows, list):
        for row in raw_rows:
            if isinstance(row, dict) and row.get("domain_id") in _DOMAIN_BY_ID:
                row_by_id[str(row["domain_id"])] = row

    assessments: list[dict[str, Any]] = []
    for domain in REQUIRED_COVERAGE_DOMAINS:
        row = row_by_id.get(domain.domain_id, {})
        status = str(row.get("status", "unassessed"))
        if status not in COVERAGE_STATUSES:
            status = "unassessed"
        evidence_ids = tuple(
            dict.fromkeys(
                fact_id
                for fact_id in row.get("evidence_fact_ids", [])
                if isinstance(fact_id, str) and fact_id in known_fact_ids
            )
        )
        if status in {"partial", "sufficient"} and not evidence_ids:
            status = "unassessed"
        assessments.append(
            {
                "domain_id": domain.domain_id,
                "title": domain.title,
                "status": status,
                "evidence_fact_ids": list(evidence_ids),
                "reason": str(row.get("reason", "No supported assessment returned.")),
            }
        )

    return {
        "blueprint_version": COVERAGE_BLUEPRINT_VERSION,
        "blueprint_sha256": COVERAGE_BLUEPRINT_SHA256,
        "assessments": assessments,
        "complete_domain_count": sum(
            1 for row in assessments if row["status"] in COVERAGE_COMPLETE_STATUSES
        ),
        "required_domain_count": len(REQUIRED_COVERAGE_DOMAINS),
    }


class StandardizedCoverageSession(AdaptiveRefinablePatternSession):
    """One pattern thread that can emit standardized domain-coverage metadata."""

    def coverage_report(self) -> dict[str, Any]:
        assessor = getattr(self.model, "assess_required_coverage", None)
        if not callable(assessor):
            return _normalize_coverage({}, operative_facts=self.core.operative_facts())
        raw = assessor(
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation),
        )
        return _normalize_coverage(raw, operative_facts=self.core.operative_facts())

    def adjudicate(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        result = super().adjudicate(request)
        result["coverage"] = self.coverage_report()
        return result


@dataclass
class StandardizedCoverageRuntime:
    model: OwnerConversationModel
    sessions: dict[str, StandardizedCoverageSession] = field(default_factory=dict)

    def create_session(self) -> StandardizedCoverageSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = StandardizedCoverageSession(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def create_coverage_session(self, domain_id: str) -> tuple[StandardizedCoverageSession, CoverageDomain]:
        domain = _DOMAIN_BY_ID.get(domain_id)
        if domain is None:
            raise ValueError("unknown required coverage domain")
        session = self.create_session()
        session.pattern_focus_established = True
        session.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "assistant",
                "text": domain.canonical_screener,
            }
        )
        return session, domain

    def get(self, session_id: str) -> StandardizedCoverageSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def _coverage_html() -> str:
    html = ADAPTIVE_HTML
    html = html.replace("Private conversational probe", "Development conversational probe")
    html = html.replace(
        "You can explore another separate pattern thread, or finish for now. This summary does not claim scientific completeness.",
        "You can explore another pattern, continue the standardized coverage checklist, or finish with any remaining domains explicitly marked incomplete.",
    )
    html = html.replace(
        '<button id="finishForNow" class="secondary">Finish for now</button>',
        '<button id="continueCoverage" class="secondary">Continue required coverage</button>\n    <button id="finishForNow" class="secondary">Finish for now</button>',
    )
    html = html.replace(
        "let sessionId=null;let groundingChoice=null;let completedResults=[];let refiningPattern=false;",
        "let sessionId=null;let groundingChoice=null;let completedResults=[];let refiningPattern=false;let coverageBlueprint=[];let coverageAggregate={};",
    )
    html = html.replace(
        "    sessionId=p.session_id;\n    $('sessionState').textContent='Development conversational probe';",
        "    sessionId=p.session_id;\n    const b=await api('/api/owner-v2/conversation/coverage/blueprint');coverageBlueprint=b.domains||[];\n    $('sessionState').textContent='Development conversational probe';",
    )
    html = html.replace(
        "  completedResults.push({status:p.status,wording:p.wording||null});",
        "  completedResults.push({status:p.status,wording:p.wording||null,coverage:p.coverage||null});mergeCoverage(p.coverage);renderCoverageStatus();",
    )
    marker = "$('exploreAnother').onclick=async()=>{"
    functions = """
function coverageRank(status){return status==='sufficient'?5:(status==='unknown'||status==='inapplicable'||status==='declined')?4:status==='partial'?2:1}
function mergeCoverage(report){if(!report||!report.assessments)return;for(const row of report.assessments){const old=coverageAggregate[row.domain_id];if(!old||coverageRank(row.status)>coverageRank(old.status))coverageAggregate[row.domain_id]=row}}
function incompleteCoverage(){return coverageBlueprint.filter(d=>{const row=coverageAggregate[d.domain_id];return !row||!(row.status==='sufficient'||row.status==='unknown'||row.status==='inapplicable'||row.status==='declined')})}
function coverageText(){const missing=incompleteCoverage();const done=coverageBlueprint.length-missing.length;return `Required coverage: ${done}/${coverageBlueprint.length} domains complete${missing.length?'. Still open: '+missing.map(d=>d.title).join(', '):'. Complete.'}`}
function renderCoverageStatus(){if(coverageBlueprint.length){$('sessionSummary').textContent=coverageText();show('sessionSummary')}}
async function startCoverageDomain(domain){const p=await api('/api/owner-v2/conversation/coverage/sessions',{method:'POST',body:JSON.stringify({domain_id:domain.domain_id})});sessionId=p.session_id;groundingChoice=null;refiningPattern=false;hide('result');hide('continuation');hide('patternPanel');show('composer');$('message').value='';$('sessionState').textContent='Development conversational probe · required coverage';bubble('ai',p.opening);$('message').focus()}
$('continueCoverage').onclick=async()=>{const missing=incompleteCoverage();if(!missing.length){$('sessionSummary').textContent='Required coverage is complete.';show('sessionSummary');return}try{await startCoverageDomain(missing[0])}catch(e){$('sessionSummary').textContent=e.message;$('sessionSummary').className='error';show('sessionSummary')}};
"""
    if marker not in html:
        raise RuntimeError("coverage UI insertion point not found")
    html = html.replace(marker, functions + marker, 1)
    old_finish = "$('finishForNow').onclick=()=>{const summary=completedResults.map((r,i)=>`${i+1}. ${r.status}${r.wording?' — '+r.wording:''}`).join('\\n');$('sessionSummary').textContent=summary||'No completed pattern threads yet.';show('sessionSummary')};"
    new_finish = "$('finishForNow').onclick=()=>{const summary=completedResults.map((r,i)=>`${i+1}. ${r.status}${r.wording?' — '+r.wording:''}`).join('\\n');const coverage=coverageBlueprint.length?'\\n\\n'+coverageText():'';$('sessionSummary').textContent=(summary||'No completed pattern threads yet.')+coverage;show('sessionSummary')};"
    if old_finish not in html:
        raise RuntimeError("coverage finish-summary insertion point not found")
    return html.replace(old_finish, new_finish, 1)


COVERAGE_HTML = _coverage_html()


def create_life_patterns_v2_owner_coverage_app(
    *, model: OwnerConversationModel | None = None,
) -> FastAPI:
    resolved_model = model or StandardizedCoverageOpenAIModel.from_env()
    runtime = StandardizedCoverageRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns standardized adaptive development interview", version="1.1")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return COVERAGE_HTML

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "development_surface": True,
            "target_theory_blind": True,
            "hidden_evidence_ledger": True,
            "pattern_first": True,
            "person_specificity_gate": True,
            "observer_triangulation": True,
            "neutral_person_model_discriminators": True,
            "refinement_repetition_guard": True,
            "standardized_required_coverage": True,
            "coverage_blueprint_version": COVERAGE_BLUEPRINT_VERSION,
            "coverage_blueprint_sha256": COVERAGE_BLUEPRINT_SHA256,
            "required_domain_count": len(REQUIRED_COVERAGE_DOMAINS),
            "adaptive_wording_with_fixed_domains": True,
            "fixed_episode_quota": False,
            "mandatory_counterexample_gate": False,
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.get("/api/owner-v2/conversation/coverage/blueprint")
    def coverage_blueprint() -> dict[str, Any]:
        return {
            "version": COVERAGE_BLUEPRINT_VERSION,
            "sha256": COVERAGE_BLUEPRINT_SHA256,
            "statuses": list(COVERAGE_STATUSES),
            "complete_statuses": sorted(COVERAGE_COMPLETE_STATUSES),
            "domains": _blueprint_payload(),
        }

    @app.post("/api/owner-v2/conversation/sessions")
    def create_session() -> CreateConversationSessionResponse:
        session = runtime.create_session()
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=ADAPTIVE_OPENING,
        )

    @app.post("/api/owner-v2/conversation/coverage/sessions")
    def create_coverage_session(request: CoverageSessionRequest) -> CreateConversationSessionResponse:
        try:
            session, domain = runtime.create_coverage_session(request.domain_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=domain.canonical_screener,
        )

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def interview_turn(session_id: str, request: ConversationTurnRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).turn(request.message)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/continue")
    def continue_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).continue_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/disagree")
    def disagree_with_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).disagree_with_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/adjudicate")
    def adjudicate_pattern(session_id: str, request: PatternAdjudicationRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_coverage_app()
