"""Owner-only unresolved/rejected-synthesis continuation for the Life Patterns pattern-first probe.

This product-layer overlay keeps an already surfaced pattern proposal open when the participant
wants more questioning or says the current synthesis does not fit. Post-proposal material remains
post-proposal evidence; the accepted v2 semantic contract is unchanged and no replacement
person-level proposal is inferred automatically.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .life_patterns_v2_owner_app import PatternAdjudicationRequest
from .life_patterns_v2_owner_conversation import (
    ConversationMove,
    ConversationTurnRequest,
    CreateConversationSessionResponse,
    OwnerConversationModel,
)
from .life_patterns_v2_owner_conversation_ui import HTML as BASE_HTML
from .life_patterns_v2_owner_pattern_first import (
    OPENING,
    PatternFirstConversationalOwnerSession,
    PatternFirstOpenAIConversationModel,
    TemporaryModelProviderError,
)


def _refinement_html() -> str:
    html = BASE_HTML
    html = html.replace(
        '<button id="unresolved" class="subtle">I’m not sure</button>',
        '<button id="continuePattern" class="secondary">Keep trying to pin it down</button>\n'
        '    <button id="unresolved" class="subtle">Leave it unresolved for now</button>',
    )
    html = html.replace(
        '<button id="reject" class="danger">No</button>',
        '<button id="reject" class="danger">No — keep investigating</button>\n'
        '    <button id="rejectStop" class="subtle">Reject and stop this thread</button>',
    )
    html = html.replace(
        '<p class="note">This is the one place where your explicit judgment matters. The hidden episode facts are not being shown for routine approval.</p>',
        '<p class="note">Would you like to keep trying to pin this pattern down, or make a judgment now? Saying the synthesis does not fit keeps the underlying inquiry open; use Reject and stop only when you actually want to end this thread. The hidden episode facts are not being shown for routine approval.</p>',
    )
    html = html.replace(
        '  <div id="reviseBox" class="hidden">',
        '  <p class="note">Leaving it unresolved is valid, but this thread will not contribute a settled person-level pattern to later analysis.</p>\n'
        '  <div id="reviseBox" class="hidden">',
    )
    html = html.replace(
        'let sessionId=null;let groundingChoice=null;let completedResults=[];',
        'let sessionId=null;let groundingChoice=null;let completedResults=[];let refiningPattern=false;',
    )
    html = html.replace(
        "  sessionId=p.session_id;groundingChoice=null;\n",
        "  sessionId=p.session_id;groundingChoice=null;refiningPattern=false;\n",
    )
    html = html.replace(
        "    if(p.pattern_active){\n      hide('composer');\n      show('patternPanel');\n      $('patternPanel').scrollIntoView({behavior:'smooth'});\n    }",
        "    if(p.pattern_active){\n"
        "      show('patternPanel');\n"
        "      refiningPattern=Boolean(p.pattern_refining)||refiningPattern;\n"
        "      if(refiningPattern){show('composer')}else{hide('composer')}\n"
        "      $('patternPanel').scrollIntoView({behavior:'smooth'});\n"
        "    }",
    )
    html = html.replace(
        "$('unresolved').onclick=()=>decision('unresolved');",
        "$('continuePattern').onclick=async()=>{\n"
        "  $('continuePattern').disabled=true;\n"
        "  try{\n"
        "    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/continue`,{method:'POST'});\n"
        "    refiningPattern=true;show('composer');bubble('ai',p.reply);$('message').focus();\n"
        "  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}\n"
        "  finally{$('continuePattern').disabled=false}\n"
        "};\n"
        "$('unresolved').onclick=()=>decision('unresolved');",
    )
    html = html.replace(
        "$('reject').onclick=()=>decision('reject');",
        "$('reject').onclick=async()=>{\n"
        "  $('reject').disabled=true;\n"
        "  try{\n"
        "    const p=await api(`/api/owner-v2/conversation/sessions/${encodeURIComponent(sessionId)}/patterns/disagree`,{method:'POST'});\n"
        "    refiningPattern=true;show('composer');bubble('user','No — that synthesis does not fit.');bubble('ai',p.reply);$('message').focus();\n"
        "  }catch(e){$('patternStatus').textContent=e.message;$('patternStatus').className='error'}\n"
        "  finally{$('reject').disabled=false}\n"
        "};\n"
        "$('rejectStop').onclick=()=>decision('reject');",
    )
    html = html.replace(
        "function renderResult(p){\n  hide('patternPanel');",
        "function renderResult(p){\n  refiningPattern=false;hide('composer');hide('patternPanel');",
    )
    return html


HTML = _refinement_html()


class RefinablePatternFirstConversationalOwnerSession(PatternFirstConversationalOwnerSession):
    """Allow explicit same-thread questioning after a tentative proposal is surfaced."""

    def _plan_refinement_move(self) -> ConversationMove:
        move = self.model.plan_turn(
            current_episode_id=self.current_episode_id,
            episodes=self.core.record.episodes,
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation),
            boundary_answered=False,
        )
        if move.move_type == "request_contrast" and self.current_episode_id is None:
            return ConversationMove(
                reply="Stay with this situation for one more step: what happened next that most affected your interpretation?",
                move_type="follow_up",
            )
        if move.move_type == "boundary_question" and len(self.core.record.episodes) < 2:
            return ConversationMove(
                reply="Give me a different real situation where the pattern looked different or broke down.",
                move_type="request_contrast",
            )
        if move.move_type == "surface_hypothesis":
            return ConversationMove(
                reply="What part of the current synthesis still feels least settled, and what real case would most help decide between the possibilities?",
                move_type="follow_up",
            )
        return move

    def _apply_refinement_move(self, move: ConversationMove) -> dict[str, Any]:
        if move.move_type == "request_contrast":
            self.awaiting_new_episode = True
            self.current_episode_id = None
        elif move.move_type == "boundary_question":
            self.pending_boundary_question = True
        self.conversation.append(
            {
                "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                "role": "assistant",
                "text": move.reply,
            }
        )
        return {
            "reply": move.reply,
            "move_type": move.move_type,
            "pattern_active": True,
            "pattern_proposition": None,
            "episode_count": len(self.core.record.episodes),
            "pattern_refining": True,
        }

    def continue_pattern(self) -> dict[str, Any]:
        if self.core.active_proposal_id is None:
            raise ValueError("no active pattern proposal to continue")
        snapshot = self._snapshot_state()
        try:
            return self._apply_refinement_move(self._plan_refinement_move())
        except Exception:
            self._restore_state(snapshot)
            raise

    def disagree_with_pattern(self) -> dict[str, Any]:
        """Treat a failed synthesis as feedback, not as termination of the pattern inquiry."""

        if self.core.active_proposal_id is None:
            raise ValueError("no active pattern proposal to disagree with")
        snapshot = self._snapshot_state()
        try:
            self.conversation.append(
                {
                    "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                    "role": "user",
                    "text": "No — that synthesis does not fit.",
                }
            )
            reply = (
                "Okay. I’ll keep the underlying pattern inquiry open rather than treating that "
                "synthesis as the answer. What does that synthesis get wrong or miss?"
            )
            self.conversation.append(
                {
                    "turn_id": f"TURN-{uuid.uuid4().hex[:10].upper()}",
                    "role": "assistant",
                    "text": reply,
                }
            )
            return {
                "reply": reply,
                "move_type": "follow_up",
                "pattern_active": True,
                "pattern_proposition": None,
                "episode_count": len(self.core.record.episodes),
                "pattern_refining": True,
                "synthesis_disagreed": True,
            }
        except Exception:
            self._restore_state(snapshot)
            raise

    def _continue_active_pattern(self, clean: str) -> dict[str, Any]:
        if self.pending_boundary_question:
            self.pending_boundary_question = False

        turn_id = f"TURN-{uuid.uuid4().hex[:10].upper()}"
        self.conversation.append({"turn_id": turn_id, "role": "user", "text": clean})
        start_new_episode = self.awaiting_new_episode or self.current_episode_id is None
        extraction = self.model.extract_turn(
            message=clean,
            current_episode_id=self.current_episode_id,
            operative_facts=self.core.operative_facts(),
            recent_conversation=tuple(self.conversation),
        )
        self._apply_extraction(
            extraction=extraction,
            turn_id=turn_id,
            message=clean,
            start_new_episode=start_new_episode,
        )
        return self._apply_refinement_move(self._plan_refinement_move())

    def turn(self, message: str) -> dict[str, Any]:
        clean = message.strip()
        if not clean:
            raise ValueError("message is required")
        if self.core.active_proposal_id is None:
            return super().turn(clean)

        snapshot = self._snapshot_state()
        try:
            return self._continue_active_pattern(clean)
        except Exception:
            self._restore_state(snapshot)
            raise


@dataclass
class RefinablePatternFirstConversationRuntime:
    model: OwnerConversationModel
    sessions: dict[str, RefinablePatternFirstConversationalOwnerSession] = field(
        default_factory=dict
    )

    def create_session(self) -> RefinablePatternFirstConversationalOwnerSession:
        session_id = f"OWNER-{uuid.uuid4().hex[:12].upper()}"
        session = RefinablePatternFirstConversationalOwnerSession(
            session_id=session_id, model=self.model
        )
        self.sessions[session_id] = session
        return session

    def get(self, session_id: str) -> RefinablePatternFirstConversationalOwnerSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError(session_id)
        return session


def create_life_patterns_v2_owner_refinement_app(
    *, model: OwnerConversationModel | None = None
) -> FastAPI:
    resolved_model = model or PatternFirstOpenAIConversationModel.from_env()
    runtime = RefinablePatternFirstConversationRuntime(model=resolved_model)
    app = FastAPI(title="Life Patterns v2 refinable pattern-first owner conversation", version="0.5")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def landing() -> str:
        return HTML

    @app.get("/healthz")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "owner_only": True,
            "target_theory_blind": True,
            "hidden_evidence_ledger": True,
            "pattern_first": True,
            "unresolved_thread_continuation": True,
            "rejected_synthesis_continuation": True,
            "model_configured": bool(getattr(resolved_model, "configured", True)),
        }

    @app.post("/api/owner-v2/conversation/sessions")
    def create_session() -> CreateConversationSessionResponse:
        session = runtime.create_session()
        return CreateConversationSessionResponse(
            session_id=session.session_id,
            model_configured=bool(getattr(resolved_model, "configured", True)),
            opening=OPENING,
        )

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/turns")
    def interview_turn(session_id: str, request: ConversationTurnRequest) -> dict[str, Any]:
        try:
            return runtime.get(session_id).turn(request.message)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/continue")
    def continue_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).continue_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except TemporaryModelProviderError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/disagree")
    def disagree_with_pattern(session_id: str) -> dict[str, Any]:
        try:
            return runtime.get(session_id).disagree_with_pattern()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except (RuntimeError, ValueError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/owner-v2/conversation/sessions/{session_id}/patterns/adjudicate")
    def adjudicate_pattern(
        session_id: str, request: PatternAdjudicationRequest
    ) -> dict[str, Any]:
        try:
            return runtime.get(session_id).adjudicate(request)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="owner session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_life_patterns_v2_owner_refinement_app()
