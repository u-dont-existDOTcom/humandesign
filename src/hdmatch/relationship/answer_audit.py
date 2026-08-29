"""Chart-blind answer-quality and ambiguity audit for relationship capture.

The auditor is deliberately independent of Human Design, astrology, candidate charts,
and model fit. It scores only whether a participant answer is usable for the frozen
relationship phenotype vocabulary and generates bounded clarification prompts when
known construct conflations or hidden context-dependence remain.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

FieldStatus = Literal["clear", "mixed", "context_dependent", "unknown", "not_applicable"]
QualityBand = Literal["explicit_unknown", "needs_detail", "usable", "strong"]

AUDIT_VERSION = "relationship-answer-audit-v1"


class _FrozenModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class FieldEvidence(_FrozenModel):
    question_id: str = Field(min_length=1)
    field_id: str = Field(min_length=1)
    status: FieldStatus
    answer: str = ""
    clarification: str = ""


class AnswerQuality(_FrozenModel):
    score: int = Field(ge=0, le=100)
    band: QualityBand
    hints: tuple[str, ...] = ()
    ambiguity_codes: tuple[str, ...] = ()
    needs_clarification: bool
    audit_version: str = AUDIT_VERSION


class ClarificationItem(_FrozenModel):
    id: str = Field(min_length=1)
    source_question_id: str = Field(min_length=1)
    source_field_id: str = Field(min_length=1)
    reason_code: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    priority: int = Field(ge=1)
    quality_score: int = Field(ge=0, le=100)
    audit_version: str = AUDIT_VERSION


_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9'’-]*")

_INTENSITY = (
    "very",
    "extremely",
    "strong",
    "strongly",
    "high",
    "low",
    "moderate",
    "little",
    "rarely",
    "often",
    "usually",
    "never",
    "always",
    "sometimes",
)
_EXAMPLE_MARKERS = (
    "for example",
    "for instance",
    "because",
    "specifically",
    "one time",
    "once",
    "when ",
    "after ",
    "before ",
    "during ",
)
_CONTEXT_MARKERS = (
    "sometimes",
    "depends",
    "depending",
    "but",
    "except",
    "varied",
    "changed",
    "different when",
    "early",
    "later",
    "at first",
    "over time",
    "distance",
    "apart",
    "together",
    "cohabit",
    "living together",
    "reunion",
)
_HEDGES = ("maybe", "probably", "i think", "i guess", "seemed", "seems", "perhaps")
_PARTNER_EVIDENCE = (
    "said",
    "told",
    "asked",
    "initiated",
    "showed",
    "wrote",
    "texted",
    "complained",
    "wanted",
    "refused",
    "avoided",
    "described",
)

_PARTNER_INFERENCE_FIELDS = {
    "b_physical_attraction",
    "b_eros_in_love",
    "b_love_attachment",
    "b_commitment_intent",
    "b_baseline_libido",
    "b_partner_specific_desire",
    "b_sexual_satisfaction",
}
_CONTEXT_SENSITIVE_FIELDS = {
    "relationship_timeline",
    "physical_togetherness",
    "major_constraints_transitions",
    "desire_change_with_familiarity",
    "sexual_constraints",
    "communication_abundance",
    "internal_emotional_ease",
    "autonomy_engulfment",
    "romantic_priority_jealousy",
    "proximity_attachment_sensitivity",
    "practical_life_fit",
    "continuation_breakup_factors",
}

_CODE_PRIORITY: Mapping[str, int] = {
    "love_eros_conflation": 1,
    "attraction_chemistry_conflation": 2,
    "libido_partner_desire_conflation": 3,
    "partner_evidence_weak": 4,
    "intellect_interaction_conflation": 5,
    "stimulation_compatibility_conflation": 6,
    "communication_quality_amount_conflation": 7,
    "drama_conflict_conflation": 8,
    "jealousy_type_conflation": 9,
    "practical_vague": 10,
    "hidden_context_dependence": 11,
    "low_detail": 20,
}

_CODE_PROMPTS: Mapping[str, str] = {
    "love_eros_conflation": (
        "Your answer could mean deep love/attachment without necessarily being romantically "
        "in love. Which was actually present, and how strongly?"
    ),
    "attraction_chemistry_conflation": (
        "Physical attraction and sexual chemistry are different here. What was the physical "
        "attraction itself, independent of how good or bad the sexual interaction was?"
    ),
    "libido_partner_desire_conflation": (
        "General libido and desire for this specific partner are being kept separate. What was "
        "the person's general sexual appetite outside this relationship-specific desire?"
    ),
    "partner_evidence_weak": (
        "This is about the other person's internal experience. What direct statements or "
        "behavior support your inference, and what remains uncertain?"
    ),
    "intellect_interaction_conflation": (
        "General intelligence is not the target. What happened when you actually reasoned "
        "together or worked through a difficult idea?"
    ),
    "stimulation_compatibility_conflation": (
        "Good conversation and mental compatibility do not necessarily mean self-expansion. "
        "Did this person actually change or expand your thinking? Give an example or say no."
    ),
    "communication_quality_amount_conflation": (
        "Communication amount and communication quality are separate. Was the communication "
        "clear/useful when it happened, independent of how much you talked?"
    ),
    "drama_conflict_conflation": (
        "Was this expressive/playful/theatrical drama, genuinely hostile conflict, or both? "
        "Describe the distinction rather than using one word for both."
    ),
    "jealousy_type_conflation": (
        "Jealousy about sex and jealousy about losing romantic priority are separate. Which "
        "kind was present here?"
    ),
    "practical_vague": (
        "Which concrete life domains were compatible or incompatible—such as geography, money, "
        "work, children/family, religion, domestic life, relationship structure, or community?"
    ),
    "hidden_context_dependence": (
        "You marked this answer as clear, but the wording suggests it changed by time or context. "
        "What differed, and under which condition or phase?"
    ),
    "low_detail": (
        "Add one concrete example, degree, or directly observed fact so this answer can be "
        "classified without guessing."
    ),
}


def assess_field_answer(
    field_id: str,
    status: FieldStatus,
    answer: str,
    clarification: str = "",
) -> AnswerQuality:
    """Score answer usability without seeing any chart/model information."""
    answer_clean = answer.strip()
    clarification_clean = clarification.strip()
    if status in {"unknown", "not_applicable"}:
        return AnswerQuality(
            score=100,
            band="explicit_unknown",
            hints=("Explicit unknown/not-applicable is a complete answer when it is accurate.",),
            needs_clarification=False,
        )

    combined = f"{answer_clean} {clarification_clean}".strip()
    lowered = combined.lower()
    word_count = len(_TOKEN_RE.findall(combined))
    score = 25 + min(word_count * 2, 45)
    codes: list[str] = []
    hints: list[str] = []

    if _contains_any(lowered, _INTENSITY):
        score += 5
    if _contains_any(lowered, _EXAMPLE_MARKERS) or any(char.isdigit() for char in combined):
        score += 7
    if field_id in _CONTEXT_SENSITIVE_FIELDS and _contains_any(lowered, _CONTEXT_MARKERS):
        score += 5

    if status == "clear" and _contains_any(lowered, _CONTEXT_MARKERS):
        codes.append("hidden_context_dependence")
        score -= 12

    if field_id in _PARTNER_INFERENCE_FIELDS:
        if _contains_any(lowered, _PARTNER_EVIDENCE):
            score += 8
        elif _contains_any(lowered, _HEDGES) or word_count < 12:
            codes.append("partner_evidence_weak")
            score -= 12

    _apply_field_specific_rules(field_id, lowered, word_count, codes)

    if word_count < 8 and not codes:
        codes.append("low_detail")
        score -= 10

    if status in {"mixed", "context_dependent"}:
        if clarification_clean:
            score += min(len(_TOKEN_RE.findall(clarification_clean)), 10)
        else:
            score -= 20
            hints.append("Explain what is mixed or what changes by context/time.")

    score = max(0, min(100, score))
    for code in _ordered_unique(codes):
        prompt = _CODE_PROMPTS.get(code)
        if prompt is not None:
            hints.append(prompt)
    hints = list(_ordered_unique(hints))
    needs_clarification = bool(codes) or score < 60
    if score >= 85:
        band: QualityBand = "strong"
    elif score >= 60:
        band = "usable"
    else:
        band = "needs_detail"
    return AnswerQuality(
        score=score,
        band=band,
        hints=tuple(hints[:2]),
        ambiguity_codes=_ordered_unique(codes),
        needs_clarification=needs_clarification,
    )


def build_clarification_queue(
    evidence: Sequence[FieldEvidence],
    *,
    field_prompts: Mapping[str, str] | None = None,
    max_items: int = 6,
) -> tuple[ClarificationItem, ...]:
    """Return a bounded, deterministic clarification queue after core capture."""
    if max_items < 0:
        raise ValueError("max_items must be non-negative")
    prompt_lookup = field_prompts or {}
    candidates: list[ClarificationItem] = []
    for item in evidence:
        quality = assess_field_answer(item.field_id, item.status, item.answer, item.clarification)
        if not quality.needs_clarification or item.status in {"unknown", "not_applicable"}:
            continue
        code = quality.ambiguity_codes[0] if quality.ambiguity_codes else "low_detail"
        prompt = _CODE_PROMPTS.get(code)
        if prompt is None:
            original = prompt_lookup.get(item.field_id, "this answer")
            prompt = f"Please clarify {original} without changing your underlying answer."
        digest = hashlib.sha256(
            f"{AUDIT_VERSION}|{item.question_id}|{item.field_id}|{code}".encode()
        ).hexdigest()[:16]
        candidates.append(
            ClarificationItem(
                id=f"RC-{digest}",
                source_question_id=item.question_id,
                source_field_id=item.field_id,
                reason_code=code,
                prompt=prompt,
                priority=_CODE_PRIORITY.get(code, 50),
                quality_score=quality.score,
            )
        )
    candidates.sort(key=lambda row: (row.priority, row.quality_score, row.source_field_id))
    return tuple(candidates[:max_items])


def legacy_clarification_queue(
    question_answers: Mapping[str, str],
    *,
    field_questions: Mapping[str, tuple[str, str]],
    max_items: int = 8,
) -> tuple[ClarificationItem, ...]:
    """Find likely missing distinctions in frozen legacy one-textarea answers.

    This is conservative: it only asks a field when the legacy response lacks the
    field's concept vocabulary or contains a known conflation. It never rewrites the
    original freeze.
    """
    if max_items < 0:
        raise ValueError("max_items must be non-negative")
    candidates: list[ClarificationItem] = []
    for field_id, (question_id, prompt) in field_questions.items():
        broad = question_answers.get(question_id, "").strip()
        if not broad:
            code = "low_detail"
            quality_score = 0
        else:
            covered = _legacy_concept_covered(field_id, broad.lower())
            quality = assess_field_answer(field_id, "clear", broad)
            if covered and not quality.ambiguity_codes:
                continue
            code = quality.ambiguity_codes[0] if quality.ambiguity_codes else "low_detail"
            quality_score = quality.score
        digest = hashlib.sha256(
            f"{AUDIT_VERSION}|legacy|{question_id}|{field_id}|{code}".encode()
        ).hexdigest()[:16]
        candidates.append(
            ClarificationItem(
                id=f"RC-{digest}",
                source_question_id=question_id,
                source_field_id=field_id,
                reason_code=code,
                prompt=prompt,
                priority=_CODE_PRIORITY.get(code, 40),
                quality_score=quality_score,
            )
        )
    candidates.sort(key=lambda row: (row.priority, row.quality_score, row.source_field_id))
    return tuple(candidates[:max_items])


def _apply_field_specific_rules(
    field_id: str, lowered: str, word_count: int, codes: list[str]
) -> None:
    if field_id in {"a_eros_in_love", "b_eros_in_love"}:
        if _contains_any(lowered, ("love", "loved", "care", "attached")) and not _contains_any(
            lowered, ("in love", "romantic", "longing", "romantically")
        ):
            codes.append("love_eros_conflation")
    if field_id in {"a_physical_attraction", "b_physical_attraction"}:
        if _contains_any(lowered, ("sex", "chemistry", "sexual")) and not _contains_any(
            lowered, ("attract", "physical", "appearance", "looks", "hot", "beautiful", "handsome")
        ):
            codes.append("attraction_chemistry_conflation")
    if field_id in {"a_baseline_libido", "b_baseline_libido"}:
        if not _contains_any(lowered, ("general", "overall", "libido", "sexual appetite", "other partner", "normally")):
            codes.append("libido_partner_desire_conflation")
    if field_id in {"intellectual_compatibility", "conceptual_comprehension"}:
        if _contains_any(lowered, ("smart", "intelligent", "educated", "iq")) and not _contains_any(
            lowered, ("reason", "understand", "disagree", "idea", "concept", "explain", "apply")
        ):
            codes.append("intellect_interaction_conflation")
    if field_id == "intellectual_stimulation":
        if _contains_any(lowered, ("good conversation", "talked", "smart", "compatible")) and not _contains_any(
            lowered, ("new", "surprise", "expand", "changed my", "learned", "challenged", "new way")
        ):
            codes.append("stimulation_compatibility_conflation")
    if field_id == "communication_quality":
        if _contains_any(lowered, ("a lot", "often", "hours", "every day", "constantly")) and not _contains_any(
            lowered, ("clear", "honest", "understood", "easy", "productive", "misunderstand")
        ):
            codes.append("communication_quality_amount_conflation")
    if field_id in {"visible_drama", "serious_conflict"}:
        if _contains_any(lowered, ("drama", "dramatic", "fight", "fought", "conflict")) and not _contains_any(
            lowered, ("playful", "theatrical", "hostile", "harmful", "aggression", "contempt", "coerc")
        ):
            codes.append("drama_conflict_conflation")
    if field_id in {"sexual_jealousy", "romantic_priority_jealousy"}:
        if "jealous" in lowered and not _contains_any(
            lowered, ("sex", "sexual", "sleep with", "in love", "romantic", "priority", "attention")
        ):
            codes.append("jealousy_type_conflation")
    if field_id in {"practical_life_fit", "continuation_breakup_factors"}:
        if word_count < 14 and not _contains_any(
            lowered,
            (
                "money",
                "work",
                "job",
                "geograph",
                "country",
                "city",
                "children",
                "family",
                "religion",
                "domestic",
                "monog",
                "open relationship",
                "community",
                "lifestyle",
            ),
        ):
            codes.append("practical_vague")


def _legacy_concept_covered(field_id: str, lowered: str) -> bool:
    groups: Mapping[str, tuple[str, ...]] = {
        "a_physical_attraction": ("attract", "physical", "beautiful", "hot"),
        "a_eros_in_love": ("in love", "romantic", "longing"),
        "a_love_attachment": ("love", "attached", "care"),
        "a_commitment_intent": ("marry", "marriage", "commit", "long-term", "lasting"),
        "b_physical_attraction": ("attract", "physical", "beautiful", "handsome", "hot"),
        "b_eros_in_love": ("in love", "romantic", "longing"),
        "b_love_attachment": ("love", "attached", "care"),
        "b_commitment_intent": ("marry", "marriage", "commit", "long-term", "lasting"),
        "a_baseline_libido": ("libido", "general", "sex drive"),
        "a_partner_specific_desire": ("wanted", "desire", "sexually"),
        "b_baseline_libido": ("libido", "general", "sex drive"),
        "b_partner_specific_desire": ("wanted", "desire", "sexually"),
        "a_sexual_satisfaction": ("satisf", "good sex", "bad sex", "enjoy"),
        "b_sexual_satisfaction": ("satisf", "good sex", "bad sex", "enjoy"),
        "dyadic_sexual_chemistry": ("chemistry", "sexual fit"),
        "intellectual_compatibility": ("reason", "intellectual", "disagree", "understand"),
        "intellectual_stimulation": ("stimulat", "expand", "new way", "mind-blow"),
        "communication_quality": ("communication", "understood", "honest", "talk"),
        "shared_interests": ("interest", "common", "shared"),
        "psychological_intimacy": ("confid", "disclos", "intimacy", "safe"),
        "visible_drama": ("drama", "dramatic", "theatrical", "playful"),
        "serious_conflict": ("conflict", "fight", "hostile", "aggression"),
        "repair_difficulty": ("repair", "recover", "apolog", "make up", "resolved"),
        "autonomy_engulfment": ("space", "freedom", "engulf", "pressure", "cling"),
        "sexual_jealousy": ("sexual jealousy", "sex with", "sleep with"),
        "romantic_priority_jealousy": ("romantic jealousy", "in love with", "priority", "attention"),
        "practical_life_fit": ("money", "work", "country", "children", "family", "religion", "lifestyle"),
    }
    terms = groups.get(field_id)
    if terms is None:
        return len(_TOKEN_RE.findall(lowered)) >= 10
    return _contains_any(lowered, terms)


def _contains_any(text: str, terms: Sequence[str]) -> bool:
    return any(term in text for term in terms)


def _ordered_unique(items: Sequence[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))
