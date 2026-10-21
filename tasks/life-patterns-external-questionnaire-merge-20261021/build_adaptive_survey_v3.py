# ruff: noqa: E501  # Full instrument statements are preserved verbatim for provenance.
"""Merge useful external-questionnaire methodology into an opt-in survey candidate.

NO participant answers, birth dates, target chart information, or fixed external
prediction windows are inputs. Existing live and frozen instruments are unchanged.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
BANK = (
    ROOT / "tasks/life-patterns-extra-natal-audit-20261018/TWENTY-THREE-OPTIONAL-QUESTIONS-v2.json"
)
EM = ROOT / "apps/life-patterns-participant/participant/static/experience-meaning-v2.json"
TF = ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
OUTPUT = TASK / "LIFE-PATTERNS-ADAPTIVE-SURVEY-v3-CANDIDATE.json"
ITEM_AUDIT = TASK / "EXTERNAL-31-ITEM-DESIGN-AUDIT-v1.json"
MODES = {
    "DREAM": "subjective_experience",
    "BELIEF": "belief_and_actual_practice",
    "BELIEF_CHANGE": "life_course_change",
    "RENUNCIATION": "optional_actual_history",
    "ART": "creative_practice_and_appreciation_separate",
    "MYSTERY": "interest_and_reasoning_tendency",
    "TIMELINE": "actual_event_history",
    "VOCATION": "actual_work_history",
    "HOME": "experience_of_belonging",
    "KINSHIP": "optional_family_history",
    "BONDS": "optional_close_relationship_history",
    "TRAVEL": "actual_travel_history",
    "STATUS": "actual_role_history",
    "RESOURCES": "optional_material_life_history",
    "PARENTING": "optional_actual_caregiving",
    "PLAY": "recurring_lived_pleasure",
    "LEARNING_HISTORY": "actual_learning_history",
    "ANGER_REPAIR": "recurring_emotional_process",
    "RECIPROCITY": "recurring_helping_and_receiving",
    "CONTENTMENT": "recurring_inner_orientation",
    "UPBRINGING": "optional_sensitive_history",
    "PRIVACY": "recurring_disclosure_preference",
    "SENSORY_ENJOYMENT": "ordinary_sensory_experience",
}
STATES = [
    "ANSWERED",
    "CONTEXT_DEPENDENT",
    "NO_OPPORTUNITIES",
    "NEVER",
    "NOT_APPLICABLE",
    "UNCERTAIN",
    "SKIPPED",
    "ALREADY_COVERED",
    "NOT_ASKED",
    "FUTURE_PENDING",
]
FUTURE_IDS = [f"Q{i:02}" for i in range(27, 32)]
SAFE_DISPOSITIONS = {
    "ADAPT",
    "CONDITIONAL_PROBE",
    "REJECT_PERSONALITY_PROXY",
    "REJECT_FORCED_CHOICE",
    "DEPENDENT_EVENT",
    "FUTURE_ONLY",
}
BAD_FEATURES = [
    {
        "id": "F01",
        "condition": "paid_formal_work_only",
        "repair": (
            "Ask what work/activity actually occurred, then independently ask "
            "whether there was wages, donations, clients, indirect revenue or "
            "no compensation. Do not make money a prerequisite for a personality trait."
        ),
        "external_ids": ["Q02", "Q03", "Q13", "Q14", "Q15", "Q26"],
    },
    {
        "id": "F02",
        "condition": "arbitrary_dichotomized_threshold",
        "repair": (
            "Keep raw duration/quantity when known and the relevant opportunity "
            "denominator; do not call an arbitrary hours/dollars/audience cutoff a "
            "personality measure. Use a prespecified threshold only for a truly "
            "independent frozen prospective outcome."
        ),
        "external_ids": ["Q01", "Q07", "Q08", "Q09", "Q12", "Q13", "Q22"],
    },
    {
        "id": "F03",
        "condition": "forced_social_binary",
        "repair": (
            "Record the actual conditional preference and the people, purpose or "
            "situation that changes it; 'depends' is a complete answer."
        ),
        "external_ids": ["Q21"],
    },
    {
        "id": "F04",
        "condition": "restricted_ranking",
        "repair": (
            "Capture the full respondent-authored ranking where offered, allow "
            "ties, added attributes, uncertainty, and context."
        ),
        "external_ids": ["Q17"],
    },
    {
        "id": "F05",
        "condition": "observer_label_conflation",
        "repair": (
            "Separate the independent source who said something, the behavior "
            "they observed and the person's self-assessment; do not lump "
            "thoroughness, rigid perfectionism and criticism together."
        ),
        "external_ids": ["Q05"],
    },
    {
        "id": "F06",
        "condition": "unaffordable_aesthetic_spending_proxy",
        "repair": (
            "Aesthetic tastes and actual decoration/making are distinct from "
            "material resources. Spending a certain amount does not validate "
            "an artistic disposition."
        ),
        "external_ids": ["Q08", "Q29"],
    },
    {
        "id": "F07",
        "condition": "duplicate_or_dependent_event",
        "repair": (
            "Correlate overlapping life events at source level, retaining the "
            "narrower reference window without counting it as independent trait evidence."
        ),
        "external_ids": ["Q01", "Q18", "Q24", "Q25"],
    },
    {
        "id": "F08",
        "condition": "future_unobserved_as_no",
        "repair": (
            "A future observation cannot be scored before the specified interval "
            "and persistence condition have elapsed. Use FUTURE_PENDING."
        ),
        "external_ids": FUTURE_IDS,
    },
    {
        "id": "F09",
        "condition": "chart_age_or_selected_prediction_window_in_blind_survey",
        "repair": (
            "Do not reveal birthday-derived anchoring or chart-chosen time "
            "windows in a generic personality interviewer; keep confidential "
            "precommitted predictions in an evaluator-only outcome lane."
        ),
        "external_ids": ["Q01", "Q18", "Q23", "Q24", "Q25"],
    },
    {
        "id": "F10",
        "condition": "unjustified_personality_from_one_episode",
        "repair": (
            "For recurring personality, ask typical tendency, number of actual "
            "opportunities, exceptions, and age/setting changes; date one actual "
            "event only when the event itself is the target."
        ),
        "external_ids": ["Q04", "Q13", "Q19", "Q20"],
    },
]
GOOD_FEATURES = [
    {
        "id": "G01",
        "feature": "actual_activity_over_only_hypothetical_situations",
        "adopt": "Offer prior real-world activity as optional evidence without assuming stable personality from event occurrence.",
        "external_ids": ["Q02", "Q06", "Q11", "Q14", "Q16", "Q18"],
    },
    {
        "id": "G02",
        "feature": "explicit_recall_periods",
        "adopt": "Use participant-understandable recall windows for actual events and habitual reference periods, without leaking concealed birth/chart data.",
        "external_ids": ["Q01", "Q05", "Q11", "Q19", "Q23"],
    },
    {
        "id": "G03",
        "feature": "repeated_opportunities_and_duration",
        "adopt": "Ask exposure/opportunity and continuity when materially useful; avoid arbitrary hard binary cutoffs.",
        "external_ids": ["Q04", "Q07", "Q11", "Q13", "Q19"],
    },
    {
        "id": "G04",
        "feature": "unknown_distinct_from_no_and_verbatim_comments",
        "adopt": "Preserve status separately from label and note; do not silently recode or strip respondent-defined scope.",
        "external_ids": ["Q02", "Q03", "Q07", "Q21", "Q25"],
    },
    {
        "id": "G05",
        "feature": "independent_others_feedback_optional",
        "adopt": "Support separately sourced external observations, distinct from the person's own repeated behavior.",
        "external_ids": ["Q05"],
    },
    {
        "id": "G06",
        "feature": "eventual_future_outcomes_separate_from_current_survey",
        "adopt": "Keep a separate time-bound future-outcome evidence lane, never preregister personality ratings by using future blanks.",
        "external_ids": FUTURE_IDS,
    },
]
QUESTION_FIELDS = (
    "id",
    "related_existing_23_topics",
    "disposition",
    "evidence_class",
    "design_decision",
)


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError(f"Not an object: {path}")
    return obj


def decisions() -> list[dict[str, Any]]:
    with (TASK / "ITEM-DISPOSITION-SOURCE.psv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="|"))
    if len(rows) != 31:
        raise ValueError("All 31 external questions need an explicit disposition.")
    ids = [f"Q{i:02}" for i in range(1, 32)]
    if [row["id"] for row in rows] != ids:
        raise ValueError("External item order/identity changed.")
    candidate_topics = {item["id"] for item in read(BANK)["questions"]}
    for row in rows:
        if set(row) != set(QUESTION_FIELDS):
            raise ValueError(row)
        if row["disposition"] not in SAFE_DISPOSITIONS:
            raise ValueError(row["disposition"])
        refs = [x for x in row["related_existing_23_topics"].split(",") if x]
        if not set(refs) <= candidate_topics:
            raise ValueError(f"Unknown questionnaire destination {row['id']}")
        if row["id"] in FUTURE_IDS and row["disposition"] != "FUTURE_ONLY":
            raise ValueError("Future chart outcome leaked into current survey.")
        if row["id"] not in FUTURE_IDS and row["disposition"] == "FUTURE_ONLY":
            raise ValueError("Historical source item misclassified as future.")
    return [
        {
            "source_question_id": row["id"],
            "existing_topics": row["related_existing_23_topics"].split(","),
            "disposition": row["disposition"],
            "evidence_class": row["evidence_class"],
            "design_decision": row["design_decision"],
            "contains_private_user_answer": False,
            "new_chart_score": None,
        }
        for row in rows
    ]


def build() -> tuple[dict, dict]:
    original = read(BANK)
    experience = read(EM)
    tf = read(TF)
    micro = read(TASK / "CONDITIONAL-MICROPROBES-v1.json")
    decisions_list = decisions()
    assert len(original["questions"]) == 23
    assert {q["id"] for q in original["questions"]} == set(MODES)
    assert len(experience["items"]) == 8
    assert len(tf["questions"]) == 25
    assert len(micro["questions"]) == 7
    conditional_map = defaultdict(list)
    for probe in micro["questions"]:
        assert set(probe["related_topics"]) <= set(MODES)
        for ref in probe["related_topics"]:
            conditional_map[ref].append(probe["id"])
    source_refs = defaultdict(list)
    for row in decisions_list:
        if row["disposition"] in ("FUTURE_ONLY", "REJECT_PERSONALITY_PROXY"):
            continue
        for ref in row["existing_topics"]:
            source_refs[ref].append(row["source_question_id"])
    questions = []
    for q in original["questions"]:
        ident = q["id"]
        enhanced = {
            **q,
            "measurement_evidence_class": MODES[ident],
            "conditional_new_probe_ids": conditional_map.get(ident, []),
            "external_source_reference_ids": source_refs.get(ident, []),
            "eligibility": (
                "Only ask if topic is selected, applicable and not already adequately "
                "answered in earlier source. One source question cannot count twice."
            ),
            "followup_gate": "A needed distinction is still unresolved and useful.",
            "response_state_options": STATES[:-1],
            "answer_capture": {
                "first_person": True,
                "usually_frequency_if_tendency": True,
                "opportunity_count_only_if_known": True,
                "conditions_and_exceptions": "optional_when_decision_relevant",
                "date_or_age_approximate": "optional_for_actual_life_events_only",
                "typical_and_peak_intensity_separate": True,
                "actual_behavior_and_preference_separate": True,
                "ability_and_opportunity_separate": True,
                "activity_and_compensation_separate": True,
            },
        }
        questions.append(enhanced)
    combined = {
        "schema": "life-patterns-adaptive-evidence-questionnaire-candidate-v3",
        "status": "DEVELOPMENT_OPT_IN_NO_LIVE_OR_CHART_SCORING",
        "as_of": "2026-10-21",
        "source_question_bank_schema": original["schema"],
        "source_question_bank_sha256": file_sha(BANK),
        "source_experience_bank_sha256": file_sha(EM),
        "source_tendency_bank_sha256": file_sha(TF),
        "existing_questions_kept_verbatim": True,
        "existing_question_count": len(questions),
        "experience_items_existing_live_count": 8,
        "tendency_first_items_existing_count": 25,
        "optional_microprobe_count": len(micro["questions"]),
        "max_base_optional_topics_per_session": 5,
        "max_additional_conditional_probes_per_session": 2,
        "decline_all_allowed": True,
        "consent_rule": (
            "Additional questions are separate, explicitly optional and unscored. "
            "Do not silently treat them as completed or required in the current interview."
        ),
        "evidence_state_codes": STATES,
        "source_data_privacy": (
            "External interview QIDs are design lineage only; actual respondent "
            "answers, birth dates, reference windows and chosen options remain in "
            "a private exact-source addendum, never this reusable instrument."
        ),
        "interviewer_behavioral_invariants": [
            "Use usual tendencies over meaningful repeat opportunities for personality, not only the most recent episode.",
            "For actual biographies, ask what really occurred with an approximate period; event occurrence does not by itself prove a lasting trait.",
            "For future outcomes, use independent post-window evaluation; never ask them as current personality items.",
            "Allow respondent's own terms, ties, depends/context, no opportunity, unsure and prefer-not-to-answer.",
            "Do not enforce institutional salary or formal titles as a prerequisite for real work, teaching or leadership.",
            "Keep subjective strength and peak separate; count how many situations actually arose before drawing frequency conclusions.",
            "Do not infer creative taste from spending, self-worth from income, or falsehood from privacy.",
            "Preserve cross-question dependency and actual source references; never count one reported event as independent evidence twice.",
            "Never reveal date-of-birth-derived recall windows or chart-selected predicted outcomes in chart-blind interviewer wording.",
            "Freeze instrument and prediction before collecting any independently scored evidence; owner retrospective answers are development only.",
        ],
        "questions": questions,
        "optional_microprobes": micro["questions"],
        "external_future_outcome_ids_excluded": FUTURE_IDS,
    }
    review = {
        "schema": "life-patterns-external-31-item-design-audit-v1",
        "status": "DESIGN_REVIEW_ONLY_NO_PERSONAL_DATA",
        "source": "One user-provided 7-page OpenDocument Drawing with 31 numbered items.",
        "source_identity_privacy": (
            "Original marks/notes, exact date windows and personal identity are "
            "held only in the separate owner-private archive."
        ),
        "external_questions_reviewed": len(decisions_list),
        "decisions": decisions_list,
        "positive_features": GOOD_FEATURES,
        "bad_features_and_repairs": BAD_FEATURES,
        "disposition_counts": dict(Counter(d["disposition"] for d in decisions_list)),
        "source_frozen_json_available_and_verified": False,
        "participant_answers_retrospective_development_only": True,
        "archival_risk": (
            "A 96-answer interview associated with another participant was "
            "explicitly excluded from owner-only personal source merge."
        ),
    }
    return combined, review


def save() -> None:
    bank, review = build()
    OUTPUT.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n")
    ITEM_AUDIT.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "question_count_preserved": bank["existing_question_count"],
                "microprobe_count": bank["optional_microprobe_count"],
                "external_item_audit_count": review["external_questions_reviewed"],
                "source_book_sha256": bank["source_question_bank_sha256"],
                "decisions": review["disposition_counts"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    save()
