"""Recoverability-oriented standardized coverage for the Life Patterns development interview.

This module keeps participant execution target-theory-blind while strengthening the
measurement surface enough to preserve the behavioral distinctions that carried the
historical owner AstroHD recovery and the clean V3.6 holistic information audit.

The historical chart/model crosswalk is deliberately *not* imported here. Runtime
receives only neutral behavioral dimensions, definitions, and screeners.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import (
    ConversationTurnRequest,
    CreateConversationSessionResponse,
    OwnerConversationModel,
)
from .life_patterns_v2_owner_coverage import (
    COVERAGE_COMPLETE_STATUSES,
    COVERAGE_HTML,
    COVERAGE_STATUSES,
    CoverageDomain,
    CoverageSessionRequest,
    CoverageStatus,
    StandardizedCoverageOpenAIModel,
)
from .life_patterns_v2_owner_pattern_first import TemporaryModelProviderError
from .life_patterns_v2_owner_reasoning import ADAPTIVE_OPENING, AdaptiveRefinablePatternSession

RECOVERABILITY_BLUEPRINT_VERSION = "life-patterns-recoverability-coverage-v2"


RECOVERABILITY_DOMAINS: tuple[CoverageDomain, ...] = (
    CoverageDomain(
        "complex_structure",
        "Complexity, detail, and structure",
        "How complex material is decomposed, organized, classified, tested, or kept holistic.",
        "When you are trying to understand something genuinely complicated, what do you naturally do with the details—organize them into definitions or categories, keep a looser overall picture, test examples, or something else?",
    ),
    CoverageDomain(
        "insight_translation",
        "Insight and translation",
        "What happens after an insight forms: private knowing, explanation, demonstration, protocol, system, or other translation.",
        "When you finally understand something difficult, what tends to happen next—does it stay mostly intuitive or private, become a concise explanation, turn into a reusable system or protocol, or depend on the situation?",
    ),
    CoverageDomain(
        "recurring_mystery",
        "Unresolved questions and return",
        "Whether consequential unresolved questions recur, how they return, and what creates enough closure to stop returning.",
        "What tends to happen with an important question you cannot resolve—do you keep returning to it, put it down for long periods, revisit only when something prompts you, or something else? What makes it feel finished enough to stop?",
    ),
    CoverageDomain(
        "original_contribution",
        "Original contribution versus inherited method",
        "When established methods are adopted, modified, rejected, or replaced by a personally developed approach.",
        "When you work in an area that already has established methods, what makes you use them as they are versus modify them or develop your own way?",
    ),
    CoverageDomain(
        "persuasion_strategy",
        "Persuasion capacity and preferred use",
        "Ability to adapt framing or leverage to an audience, separated from whether the person prefers to use that ability.",
        "When you really need another person to understand or agree with something, how much do you adapt the framing to what will move them—and is that different from how you prefer to communicate when persuasion is not necessary?",
    ),
    CoverageDomain(
        "recognition_entry",
        "Entry, recognition, and role acceptance",
        "How social, romantic, communal, or work roles begin and what signals that stepping in is appropriate.",
        "In a new relationship, group, or role, how do you usually know when to step in—do you initiate, wait for a clear opening or recognition, respond to a request, or does it depend on the setting?",
    ),
    CoverageDomain(
        "network_pathways",
        "Networks and opportunity pathways",
        "How important opportunities, collaborators, customers, roles, or influence usually propagate through social versus impersonal channels.",
        "How do important opportunities or connections usually reach you—through people who already know you or your work, direct outreach, impersonal discovery, deliberate self-promotion, or some mixture?",
    ),
    CoverageDomain(
        "role_projection",
        "Role projection and misrecognition",
        "Whether other people assign capabilities, responsibilities, or identities beyond what the person claimed, and what follows when expectations diverge.",
        "Do people ever assign you a broader role or capability than you actually claimed? If so, what tends to happen when their expectation and what you can or want to provide diverge?",
    ),
    CoverageDomain(
        "immediate_body_signal",
        "Immediate bodily or felt signals",
        "Rapid bodily/felt information before extended reasoning, including clarity, repeatability, confidence, override, and state dependence.",
        "When an important choice or safety question comes up, do you ever get an immediate bodily or felt signal before you have reasoned it through? If so, how clear, repeatable, and trustworthy is it—and when is it easy to miss or override?",
    ),
    CoverageDomain(
        "autonomy_direction",
        "Autonomy, direction, and external roles",
        "What remains self-directed versus what changes under roles, institutions, relationships, or environmental pressure.",
        "When a role, institution, relationship, or environment pushes you in a direction, what tends to stay stable about your own direction or way of operating, and what is more likely to change?",
    ),
    CoverageDomain(
        "sanctuary_sensory",
        "Home, sensory baseline, and sanctuary",
        "Physical, sensory, environmental, privacy, and home-base conditions that materially alter functioning or restoration.",
        "What physical or sensory conditions in your home or surroundings make a large difference to how well you think, work, or recover, if any?",
    ),
    CoverageDomain(
        "romantic_attachment",
        "Romantic and attachment dynamics",
        "Attraction, closeness, reciprocity, sensuality, attachment, autonomy, and what deepens or weakens romantic connection.",
        "In romantic or sexual connection, what tends to create attraction for you, and what makes closeness deepen or fade? You can say you do not know or prefer not to answer.",
    ),
    CoverageDomain(
        "emotion_permeability",
        "Emotional baseline and permeability",
        "Baseline affect alone, response to other people's emotional states, conflict amplification, and recovery after separation or decompression.",
        "What is your emotional baseline like when you are on your own, and what changes when you are around someone who is strongly emotional or in conflict? How quickly do you usually return to baseline afterward?",
    ),
    CoverageDomain(
        "work_energy_range",
        "Work energy across intensity and duration",
        "Energy under engaging work, ordinary workload, concentrated bursts, prolonged overload, stopping signals, and recovery.",
        "How does meaningful or engaging work affect your energy at ordinary workload versus an intense burst or a prolonged period of overwork, and how do you know when you genuinely need to stop?",
    ),
    CoverageDomain(
        "consequential_effort",
        "Consequential effort, struggle, and purpose",
        "What makes a problem worth sustained effort or risk, how purpose changes the form of effort, and what makes a previously important struggle no longer worth continuing.",
        "What makes a problem important enough that you will sustain serious effort or struggle for it, and what makes you disengage even after you have already invested a lot?",
    ),
    CoverageDomain(
        "correction_threshold",
        "Correction threshold",
        "What determines whether an error, falsehood, inefficiency, or broken rule is challenged versus ignored.",
        "When you believe something is wrong, what determines whether you correct or challenge it versus simply let it go?",
    ),
    CoverageDomain(
        "retreat_privacy",
        "Retreat, privacy, and re-entry",
        "Need for withdrawal after social intensity or major experience, what happens during retreat, and what permits re-entry.",
        "After intense social contact or a major life experience, what do you usually need before you want to re-engage with people or outward activity?",
    ),
    CoverageDomain(
        "value_tension",
        "Value tension and competing priorities",
        "How persistent conflict between important values, obligations, needs, or ideals is experienced and resolved.",
        "When two things that both matter to you pull in different directions, what do you tend to do—resolve it quickly, live with the tension, prioritize one, keep switching, or something else?",
    ),
    CoverageDomain(
        "resource_motivation",
        "Resources, status, security, and sovereignty",
        "What money, material control, status, ownership, and enterprise are for in practice: autonomy, comfort, security, achievement, influence, rank, or other motives.",
        "What do money, resources, ownership, or status mainly mean to you in practice—security, autonomy, comfort, achievement, influence, rank, something else, or different things in different contexts?",
    ),
    CoverageDomain(
        "developmental_phases",
        "Developmental phases and learned change",
        "Distinct life phases, childhood-to-adult continuity, learned management, and major changes in how recurring tendencies are expressed.",
        "Looking across your life, are there clear phases where the way you engage with problems, people, or the world changed substantially? Which tendencies feel continuous from childhood and which were learned or transformed?",
    ),
    CoverageDomain(
        "rhythm_continuity",
        "Rhythm, routine, and continuity",
        "Preference for routine versus novelty, self-directed scheduling, continuity, stable baselines, and conditions under which rhythm is disrupted.",
        "How important are stable routines or continuity in your daily life, and when do you prefer novelty or major change instead?",
    ),
    CoverageDomain(
        "focus_repetition",
        "Concentrated focus and repetition",
        "Depth and duration of focus, stillness, practice, repetition, mastery, and whether repetition is intrinsically rewarding or merely instrumental.",
        "When you become deeply focused on something, what keeps you there—and how do you relate to repetition or practice? Is repeating the activity satisfying in itself, useful only for a goal, or does it depend?",
    ),
    CoverageDomain(
        "needs_responsibility",
        "Sensitivity to needs and responsibility",
        "How readily other people's or a group's needs are noticed, what creates felt responsibility, and when care or intervention is deliberately withheld.",
        "When you notice that someone or a group needs support, how quickly do you notice it, and what determines whether you feel responsible to step in versus leave it alone?",
    ),
)

_RECOVERY_DOMAIN_BY_ID = {domain.domain_id: domain for domain in RECOVERABILITY_DOMAINS}


def _recovery_blueprint_payload() -> list[dict[str, str]]:
    return [
        {
            "domain_id": domain.domain_id,
            "title": domain.title,
            "definition": domain.definition,
            "canonical_screener": domain.canonical_screener,
        }
        for domain in RECOVERABILITY_DOMAINS
    ]


RECOVERABILITY_BLUEPRINT_SHA256 = hashlib.sha256(
    json.dumps(
        {"version": RECOVERABILITY_BLUEPRINT_VERSION, "domains": _recovery_blueprint_payload()},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()


class RecoverabilityCoverageOpenAIModel(StandardizedCoverageOpenAIModel):
    """Target-blind assessor for the recoverability-oriented neutral dimensions."""

    def assess_required_coverage(
        self,
        *,
        operative_facts: tuple[Any, ...],
        recent_conversation: tuple[dict[str, str], ...],
    ) -> dict[str, Any]:
        domain_ids = [domain.domain_id for domain in RECOVERABILITY_DOMAINS]
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
                "Assess standardized behavioral-dimension COVERAGE only. These dimensions were selected because "
                "development work showed that broad personality buckets can lose useful discriminating information, "
                "but you are not given any external theory, target mapping, chart, score, or expected answer direction. "
                "Return exactly one row for every required neutral dimension. Use unassessed for no meaningful "
                "information; partial for relevant information that does not yet support a stable person-specific "
                "characterization; sufficient for a narrow interpretable person-specific characterization; unknown "
                "only when the participant directly addressed the dimension and cannot tell; inapplicable only when "
                "the participant says it genuinely does not apply; declined only for explicit refusal. Silence is never "
                "absence. Generic human regularities are not sufficient. Preserve context, intensity/duration, "
                "capacity-versus-preference, developmental change, and self-versus-observer distinctions when they "
                "materially affect meaning. Do not require a fixed number of episodes. For partial or sufficient, cite "
                "only supplied operative fact IDs that actually support the status.\n\nREQUIRED DIMENSIONS:\n"
                + "\n".join(
                    f"- {domain.domain_id}: {domain.definition}" for domain in RECOVERABILITY_DOMAINS
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
            max_output_tokens=3600,
            schema_name="life_patterns_recoverability_coverage_v2",
        )
        return result


def _normalize_recoverability_coverage(
    raw: dict[str, Any], *, operative_facts: tuple[Any, ...]
) -> dict[str, Any]:
    known_fact_ids = {fact.fact_id for fact in operative_facts}
    raw_rows = raw.get("assessments", [])
    row_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(raw_rows, list):
        for row in raw_rows:
            if isinstance(row, dict) and row.get("domain_id") in _RECOVERY_DOMAIN_BY_ID:
                row_by_id[str(row["domain_id"])] = row

    assessments: list[dict[str, Any]] = []
    for domain in RECOVERABILITY_DOMAINS:
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
        "blueprint_version": RECOVERABILITY_BLUEPRINT_VERSION,
        "blueprint_sha256": RECOVERABILITY_BLUEPRINT_SHA256,
        "assessments": assessments,
        "complete_domain_count": sum(
            1 for row in assessments if row["status"] in COVERAGE_COMPLETE_STATUSES
        ),
        "required_domain_count": len(RECOVERABILITY_DOMAINS),
    }


class RecoverabilityCoverageSession(AdaptiveRefinablePatternSession):
    """Pattern thread that emits recoverability-oriented neutral coverage metadata."""

    def coverage_report(self) -> dict[str, Any]:
        assessor = getattr(self.model, "assess_required_coverage", None)
        if not callable(assessor):
            return _normalize_recoverability_coverage(
                {}, operative_facts=self.core.operative_facts()
            )
        raw = assessor(
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation),
        )
        return _normalize_recoverability_coverage(
            raw, operative_facts=self.core.operative_facts()
        )

    def adjudicate(self, request: PatternAdjudicationRequest) -> dict[str, Any]:
        result = super().adjudicate(request)
        result["coverage"] = self.coverage_report()
        return result


@dataclass
class RecoverabilityCoverageRuntime:
    model: OwnerConversationModel
    sessions: dict[str, RecoverabilityCoverageSession] = field(default_factory=dict)

    def create_session(self) -> RecoverabilityCoverageSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = RecoverabilityCoverageSession(session_id=session_id, model=self.model)
        self.sessions[session_id] = session
        return session

    def create_coverage_session(
        self, domain_id: str
    ) -> tuple[RecoverabilityCoverageSession, CoverageDomain]:
        domain = _RECOVERY_DOMAIN_BY_ID.get(domain_id)
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

    def get(self, session_id: str) -> RecoverabilityCoverageSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def create_life_patterns_v2_owner_recoverability_app(
    *, model: OwnerConversationModel | None = None,
) -> FastAPI:
    resolved_model = model or RecoverabilityCoverageOpenAIModel.from_env()
    runtime = RecoverabilityCoverageRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns recoverability development interview", version="1.2")

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
            "recoverability_preservation_candidate": True,
            "coverage_blueprint_version": RECOVERABILITY_BLUEPRINT_VERSION,
            "coverage_blueprint_sha256": RECOVERABILITY_BLUEPRINT_SHA256,
            "required_domain_count": len(RECOVERABILITY_DOMAINS),
            "adaptive_wording_with_fixed_domains": True,
            "fixed_episode_quota": False,
            "mandatory_counterexample_gate": False,
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.get("/api/owner-v2/conversation/coverage/blueprint")
    def coverage_blueprint() -> dict[str, Any]:
        return {
            "version": RECOVERABILITY_BLUEPRINT_VERSION,
            "sha256": RECOVERABILITY_BLUEPRINT_SHA256,
            "statuses": list(COVERAGE_STATUSES),
            "complete_statuses": sorted(COVERAGE_COMPLETE_STATUSES),
            "domains": _recovery_blueprint_payload(),
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
    def create_coverage_session(
        request: CoverageSessionRequest,
    ) -> CreateConversationSessionResponse:
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
    def adjudicate_pattern(
        session_id: str, request: PatternAdjudicationRequest
    ) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="development session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_recoverability_app()
