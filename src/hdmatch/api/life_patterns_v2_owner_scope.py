"""Global-label scope guard for the Life Patterns recoverability interviewer.

The participant-facing interviewer remains target-theory-blind. This overlay repairs a
reasoning defect in which a broad self-description could be silently narrowed to the
first well-evidenced subdomain (or silently generalized beyond it) without checking the
participant's intended scope.
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import FastAPI

from .life_patterns_v2_owner_recoverability import (
    RecoverabilityCoverageOpenAIModel,
    create_life_patterns_v2_owner_recoverability_app,
)


GLOBAL_LABEL_SCOPE_INSTRUCTIONS = (
    "GLOBAL-LABEL SCOPE: Preserve the semantic scope of the participant's own claim. A broad or global "
    "self-description such as 'I am balanced in general', 'I am very stable', 'I am independent', or a similar "
    "person-wide label must not be silently reduced to the first subdomain for which evidence happens to be available, "
    "and it must not be generalized beyond the evidence either. If the participant's claim is broad but the evidence "
    "collected so far is confined to one materially narrower domain (for example mood/emotional steadiness), then the "
    "scope itself is unresolved and decision-changing. Before surfacing or finalizing a formulation that either narrows "
    "or generalizes that claim, ask ONE neutral cross-domain scope question unless the participant already explicitly "
    "defined the scope. A good question makes the contrast concrete with a few non-exhaustive examples, such as whether "
    "'balanced' means mainly emotional steadiness or also shows up in work/rest or work-life balance, practical versus "
    "spiritual priorities, functional versus emotional life, relationships, or handling competing demands. The examples "
    "are prompts for meaning, not a checklist and not assumptions that these domains are balanced. The participant may "
    "answer that it is mostly one domain, applies across several domains, varies by domain, or is unclear. Preserve that "
    "answer rather than forcing one global trait pole. If the participant has just said that the current synthesis may be "
    "too narrow because only one domain was checked, prioritize this scope question over another observer-view question. "
    "Do not re-ask scope once the participant has already settled it. This is a semantic-scope check, not an episode quota "
    "and not a requirement to run the full standardized coverage checklist before every synthesis."
)

CROSS_THREAD_CONTEXT_INSTRUCTIONS = (
    "CROSS-THREAD CONTEXT: recent_conversation may contain an assistant message beginning 'INTERNAL PRIOR CONTEXT'. "
    "That message is planning-only context summarizing previously participant-adjudicated patterns and neutral coverage "
    "metadata. Use it to avoid asking the participant to repeat already settled information and to make transitions more "
    "natural. It is NOT a participant utterance, NOT a source of episode facts, and NOT evidence that a new proposition is "
    "true in the current thread. Never quote the internal note to the participant. Never extract hidden facts from it. "
    "Coverage reasons inside it are model-generated planning metadata, not participant statements. New evidence still "
    "must come from participant messages and the operative hidden ledger."
)


class ScopeAwareRecoverabilityOpenAIModel(RecoverabilityCoverageOpenAIModel):
    """Recoverability model with scope and cross-thread continuity guards."""

    def _conversation_call_json(
        self,
        *,
        instructions: str,
        payload: dict[str, Any],
        schema: dict[str, Any],
        effort: Literal["low", "medium"],
        max_output_tokens: int,
        schema_name: str,
    ) -> dict[str, Any]:
        if schema_name in {
            "life_patterns_conversation_move_v1",
            "life_patterns_refinement_move_v1",
            "life_patterns_pattern_specificity_v1",
        }:
            instructions += "\n\n" + GLOBAL_LABEL_SCOPE_INSTRUCTIONS
        if schema_name.startswith("life_patterns_"):
            instructions += "\n\n" + CROSS_THREAD_CONTEXT_INSTRUCTIONS
        return super()._conversation_call_json(
            instructions=instructions,
            payload=payload,
            schema=schema,
            effort=effort,
            max_output_tokens=max_output_tokens,
            schema_name=schema_name,
        )


def create_life_patterns_v2_owner_scope_app() -> FastAPI:
    """Serve the recoverability interview with the global-label scope guard active."""

    model = ScopeAwareRecoverabilityOpenAIModel.from_env()
    app = create_life_patterns_v2_owner_recoverability_app(model=model)
    app.state.global_label_scope_guard = True
    app.state.cross_thread_planning_context = True
    return app
