"""Blind-safe compiled rule evaluation for the prospective detailed model."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import replace

from hdmatch.model_b.types import EvaluatedPathway, StructuralEvidence
from hdmatch.questionnaire.response import normalize_answer_token
from hdmatch.schemas import BehavioralResponse

from .artifacts import AssignmentScope, CompiledModelArtifact, CompiledPathway, CompiledRule
from .selectors import selector_matches


class CanonicalAnswerConflict(ValueError):
    """Retained for callers that elect to reject an explicit ``unknown`` tie."""


class CompiledRuleEvaluator:
    """Protocol adapter from a declarative compiled rule to scoring evidence."""

    def __init__(self, rule: CompiledRule) -> None:
        self._rule = rule

    @property
    def rule_id(self) -> str:
        return self._rule.rule_id

    @property
    def question_id(self) -> str:
        return self._rule.prediction.question_id

    def evaluate(
        self,
        chart: object,
        responses: object,
        *,
        force_neutral: bool = False,
    ) -> tuple[EvaluatedPathway, ...]:
        response = _one_response(responses, self._rule.prediction.question_id)
        if response is None:
            return ()
        answer = "unknown" if force_neutral else normalize_answer_token(response.answer)
        confidence = (
            response.behavioral_confidence
            * response.measurement_reliability
            * self._rule.behavioral_confidence
        )
        contradiction = (
            float(self._rule.prediction.contradiction_severity)
            if answer in self._rule.prediction.contradiction_answer_tokens
            else 0.0
        )
        main_pathways = (self._rule.primary, *self._rule.alternatives)
        return tuple(
            EvaluatedPathway(
                rule_id=self._rule.rule_id,
                dependency_cluster=self._rule.dependency_cluster,
                pathway_id=pathway.pathway_id,
                effective_confidence=confidence,
                primary=_evidence(
                    chart,
                    pathway,
                    response_supports=answer in self._rule.prediction.support_answer_tokens,
                    inactive_identity=f"{self._rule.rule_id}:{pathway.pathway_id}:primary",
                ),
                corroborators=(
                    (
                        _evidence(
                            chart,
                            self._rule.corroborator,
                            response_supports=(
                                answer in self._rule.prediction.support_answer_tokens
                            ),
                            inactive_identity=(
                                f"{self._rule.rule_id}:{pathway.pathway_id}:corroborator"
                            ),
                        ),
                    )
                    if self._rule.corroborator is not None
                    else ()
                ),
                contradiction_severity=(
                    contradiction if selector_matches(chart, pathway.selector) else 0.0
                ),
            )
            for pathway in main_pathways
        )


def compiled_rule_evaluators(
    artifact: CompiledModelArtifact,
    scope: AssignmentScope = AssignmentScope.DISCOVERY,
) -> tuple[CompiledRuleEvaluator, ...]:
    return tuple(CompiledRuleEvaluator(rule) for rule in artifact.rules_for_scope(scope))


def evaluate_compiled_model(
    artifact: CompiledModelArtifact,
    chart: object,
    responses: Iterable[BehavioralResponse],
    scope: AssignmentScope = AssignmentScope.DISCOVERY,
) -> tuple[EvaluatedPathway, ...]:
    """Evaluate all rules and conservatively align confidence within a cluster."""

    response_tuple = tuple(responses)
    _validate_unique_responses(response_tuple)
    candidate_answers = canonical_detailed_answers(artifact, chart, scope)
    evaluated_items: list[EvaluatedPathway] = []
    for evaluator in compiled_rule_evaluators(artifact, scope):
        evaluated_items.extend(
            evaluator.evaluate(
                chart,
                response_tuple,
                force_neutral=candidate_answers[evaluator.question_id] == "unknown",
            )
        )
    evaluated = tuple(evaluated_items)
    cluster_confidence: dict[str, float] = {}
    for pathway in evaluated:
        previous = cluster_confidence.get(pathway.dependency_cluster)
        cluster_confidence[pathway.dependency_cluster] = (
            pathway.effective_confidence
            if previous is None
            else min(previous, pathway.effective_confidence)
        )
    return tuple(
        replace(
            pathway,
            effective_confidence=cluster_confidence[pathway.dependency_cluster],
        )
        for pathway in evaluated
    )


def canonical_detailed_answers(
    artifact: CompiledModelArtifact,
    chart: object,
    scope: AssignmentScope = AssignmentScope.DISCOVERY,
) -> dict[str, str]:
    """Return every detailed answer, preserving no-match/conflict as ``unknown``."""

    scoped_rules = artifact.rules_for_scope(scope)
    scoped_questions = {rule.prediction.question_id for rule in scoped_rules}
    matched_answers: dict[str, set[str]] = {
        question_id: set() for question_id in sorted(scoped_questions)
    }
    for rule in sorted(scoped_rules, key=lambda item: item.rule_id):
        matches = [
            pathway.pathway_id
            for pathway in (rule.primary, *rule.alternatives)
            if selector_matches(chart, pathway.selector)
        ]
        if not matches:
            continue
        question_id = rule.prediction.question_id
        canonical = rule.prediction.canonical_answer_token
        matched_answers.setdefault(question_id, set()).add(canonical)
    return {
        question_id: next(iter(values)) if len(values) == 1 else "unknown"
        for question_id, values in sorted(matched_answers.items())
    }


def detailed_question_clusters(
    artifact: CompiledModelArtifact,
    scope: AssignmentScope = AssignmentScope.DISCOVERY,
) -> Mapping[str, tuple[str, ...]]:
    clusters: dict[str, set[str]] = {}
    for rule in artifact.rules_for_scope(scope):
        clusters.setdefault(rule.prediction.question_id, set()).add(rule.dependency_cluster)
    return {question_id: tuple(sorted(values)) for question_id, values in sorted(clusters.items())}


def _evidence(
    chart: object,
    pathway: CompiledPathway,
    *,
    response_supports: bool,
    inactive_identity: str,
) -> StructuralEvidence:
    matches = selector_matches(chart, pathway.selector)
    return StructuralEvidence(
        anchor_id=(pathway.anchor_id if matches else f"inactive:{inactive_identity}"),
        dependency_keys=(
            pathway.dependency_keys if matches else (f"inactive:{inactive_identity}",)
        ),
        supports_response=response_supports and matches,
        structural_salience=pathway.structural_salience,
        mapping_directness=pathway.mapping_directness,
    )


def _one_response(responses: object, question_id: str) -> BehavioralResponse | None:
    if isinstance(responses, Mapping):
        raw = responses.get(question_id)
        if raw is None:
            return None
        if isinstance(raw, BehavioralResponse):
            return raw
        raise ValueError("response mappings must contain BehavioralResponse values")
    values: Sequence[object]
    if isinstance(responses, Sequence):
        values = responses
    elif isinstance(responses, Iterable):
        values = tuple(responses)
    else:
        raise ValueError("responses must be an iterable of BehavioralResponse")
    matches = [
        item
        for item in values
        if isinstance(item, BehavioralResponse) and item.question_id == question_id
    ]
    if len(matches) > 1:
        raise ValueError(f"duplicate response for question {question_id}")
    return matches[0] if matches else None


def _validate_unique_responses(responses: tuple[BehavioralResponse, ...]) -> None:
    question_ids = tuple(item.question_id for item in responses)
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("detailed scoring rejects duplicate question responses")
