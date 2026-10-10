"""Owner-proposed idiographic inventory and non-leading example-supported interview V3.

All outputs are DEVELOPMENT ONLY. Current production v1, frozen v7, v2 and
existing respondent data are not modified by this script.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
V1 = ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
V2 = ROOT / "tasks/question-feedback-loop-20261008/tendency-first-v2-development.json"

# Concise diverse responses; these are neither exhaustive nor scorer labels.
# Free narration always wins over an option, and options are never trait votes.
ANSWER_EXAMPLES = {
    "TF1-A0": [
        "I enjoy solitude and intentionally arrange time for it.",
        "I enjoy solitude when it happens, but rarely seek it out.",
        "I prefer company most of the time.",
        "It varies with my activity, energy or the people involved.",
    ],
    "TF1-G19": [
        "I usually protect the time I already planned.",
        "I usually make room for the person, even if plans shift.",
        "I negotiate an alternative time or different kind of help.",
        "It depends on urgency and my relationship with the person.",
    ],
    "TF1-F0": [
        "I describe the same preference much the same way to everyone.",
        "I change my wording depending on the listener.",
        "I sometimes avoid stating a preference altogether.",
        "It depends on what I am asking for and the relationship.",
    ],
    "TF1-G05": [
        "My efforts often lead the other person to change position.",
        "Sometimes people change position; often they do not.",
        "I rarely try to persuade, so I cannot judge a usual outcome.",
        "My results vary strongly by topic or audience.",
    ],
    "TF1-M11": [
        "I usually consider everyone's share of effort or costs.",
        "I tend to prefer equal shares where feasible.",
        "I pay attention to need or what each person can afford.",
        "I usually discuss it until we find a suitable arrangement.",
    ],
    "TF1-G06": [
        "I step in without waiting to be asked.",
        "I offer a particular skill and see whether it is useful.",
        "I wait for a role or request to become clear.",
        "It depends on how well I know the group or task.",
    ],
    "TF1-G01": [
        "I first sort out what is known and unknown.",
        "I ask a person who understands it better.",
        "I test one possibility and see what happens.",
        "I search reference material or use a tool.",
    ],
    "TF1-G02": [
        "I start with a short explanation of the main point.",
        "I explain the steps and details in order.",
        "I adapt examples to what the listener already knows.",
        "I sometimes decide an explanation would not help.",
    ],
    "TF1-D0": [
        "Refining small details can be satisfying by itself.",
        "I repeat details mainly when it helps achieve a result.",
        "I find repetition tiring even when worthwhile.",
        "It varies a lot by skill and goal.",
    ],
    "TF1-G10": [
        "I adjust to the group's established method easily.",
        "I retain the parts of my own approach that matter to me.",
        "I discuss a compromise with the group.",
        "It depends on the consequences and my responsibilities.",
    ],
    "TF1-M03": [
        "I usually complete a commitment once I have accepted it.",
        "I renegotiate when the original commitment stops working.",
        "I sometimes drop minor commitments after interest fades.",
        "It depends on who is relying on me and what changed.",
    ],
    "TF1-B0": [
        "Someone else's mood often affects my mood too.",
        "I notice other people's moods but tend to stay steady.",
        "I feel affected while together and recover afterward.",
        "It depends on the person or the situation.",
    ],
    "TF1-G15": [
        "Absorbing activities often leave me energized afterward.",
        "I often feel tired but satisfied after engaging work.",
        "Even enjoyable tasks can leave me drained.",
        "It depends mainly on duration, intensity and my condition.",
    ],
    "TF1-G16": [
        "Seeing tangible progress keeps me going.",
        "Interest in the subject keeps me going.",
        "A sense of usefulness or purpose sustains effort.",
        "Promises or other people's reliance on me matter most.",
    ],
    "TF1-G18": [
        "I generally want more company after enjoyable company.",
        "I often want some time alone, even after enjoying people.",
        "I need solitude mostly after demanding interactions.",
        "It varies with duration, people and how I feel.",
    ],
    "TF1-G17": [
        "Even harmless errors can make me want to speak up.",
        "I usually ignore mistakes unless they matter practically.",
        "I notice them but often prefer not to mention them.",
        "It depends on whether my correction would be welcome.",
    ],
    "TF1-STATUS": [
        "Recognition is intrinsically rewarding to me in many settings.",
        "Recognition matters mainly when it comes from people close to me.",
        "Recognition has little value to me apart from practical effects.",
        "Its meaning depends on what the person actually recognizes.",
    ],
    "TF1-ROUTINE-CHANGE": [
        "I often choose a new experience over a familiar one.",
        "I usually prefer familiar things that already work.",
        "I like novelty in some parts of life and routine in others.",
        "It depends more on the stakes or practical circumstances.",
    ],
    "TF1-G23": [
        "I first notice a practical need that nobody is handling.",
        "I first notice who might need support or a role.",
        "I first notice a problem or inconsistency.",
        "I focus on the overall goal or how tasks connect.",
    ],
    "TF1-G04": [
        "I look for the exact point where something failed.",
        "I try a different method and watch the result.",
        "I start by checking the instructions or prior evidence.",
        "I consult someone else before investing more effort.",
    ],
    "TF1-G22": [
        "I can usually return to what I was doing easily.",
        "I need to rebuild the context before continuing.",
        "An interruption often shifts my attention elsewhere.",
        "It varies with my interest and how long I was interrupted.",
    ],
    "TF1-M05": [
        "I first notice something concrete that does not add up.",
        "I feel uneasy before I can explain the reason.",
        "A past experience or familiar pattern comes to mind.",
        "I usually cannot tell until more evidence appears.",
    ],
    "TF1-G20": [
        "I would use extra resources mainly for independence or time.",
        "I would prioritize security and reducing uncertainty.",
        "I would improve comfort or explore more experiences.",
        "Helping other people or projects is a major priority.",
    ],
    "TF1-M01": [
        "Other people's pressure makes me speed up.",
        "My pace stays similar when the real deadline is unchanged.",
        "I slow down or resist when I feel pressured.",
        "It depends on the person and the actual consequences.",
    ],
    "TF1-PREFER-EXCHANGE": [
        "I usually keep discussing until something is agreed.",
        "I offer one compromise, then accept the response.",
        "I often disengage when negotiation stops being useful.",
        "It depends on the importance and our relationship.",
    ],
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_v3() -> dict:
    current = json.loads(V1.read_text())
    previous = json.loads(V2.read_text())
    candidate = copy.deepcopy(previous)
    candidate["version"] = "tendency-first-v3-scaffold-development-20261010"
    candidate["status"] = "RESEARCH_CANDIDATE_NOT_ACTIVE_NOT_VALIDATED"
    candidate["parent_policy_version"] = previous["version"]
    candidate["source_integrity"] = {
        "active_v1_sha256": digest(V1),
        "previous_v2_sha256": digest(V2),
        "historical_v7_unchanged": True,
    }
    candidate["response_scaffolding_policy"] = {
        "default": "Show 2-4 short example answer paths with each new question, without asking permission first. The respondent may answer freely, choose one/multiple, mix possibilities, or say Other with their own wording.",
        "choice_vs_narrative": "Free wording and qualifications take priority. An example label is never treated as a personality trait, birth-chart feature or an independent evidence vote.",
        "options_never_forced": True,
        "multi_select_allowed": True,
        "spoken_interface": "Read at most 2 or 3 anchor examples aloud initially. State that other answers are welcome; do not make a spoken list overwhelming. Text can show all examples.",
        "examples_are_possible_answers_not_sources": True,
        "conditional_answer_valid": True,
        "never_repeat_answered_distinction": True,
        "response_options": [
            "Other — I'll explain in my own words",
            "Not sure / can't recall a pattern",
            "Prefer to skip",
        ],
        "randomization_for_future_experiment": "Freeze a participant-level example-order seed before any prediction; compare guided with open-only arms to measure suggestion bias.",
        "not_scoring": True,
    }
    questions = {q["id"]: q for q in candidate["questions"]}
    assert set(questions) == set(ANSWER_EXAMPLES)
    for rid, question in questions.items():
        question["example_answer_paths"] = ANSWER_EXAMPLES[rid]
        question["answer_format"] = "free_text_or_examples_multi_select_with_other_skip_unsure"
        question["examples_display_by_default"] = True
        question["automatic_chart_scoring"] = False
        question["non_normative_example_note"] = (
            "Examples are possible responses, not expected or better answers. Describe any conditions."
        )
        question["must_preserve_original_reply"] = True
    a0 = questions["TF1-A0"]
    a0["question"] = "How much do you enjoy spending time alone?"
    a0["measured_dimensions"] = [
        "intrinsic_enjoyment_of_solitude",
        "deliberately_arranging_solitude",
    ]
    a0["follow_up_only_if_not_already_answered"] = [
        {
            "id": "TF3-A0-TIME-MAKING",
            "question": "Do you actively arrange time alone, or mostly enjoy it when it happens?",
            "measures": "frequency_of_deliberately_sought_solitude_not_enjoyment_itself",
        },
        {
            "id": "TF3-A0-COMPANY-TRADEOFF",
            "question": "When you are enjoying time alone and a friend invites you out, what normally decides whether you join them or stay?",
            "measures": "social_invitation_tradeoff_preserved_from_historical_A0_but_not_inferred_from_solitude_enjoyment",
        },
    ]
    a0["development_revision_rationale"] = (
        "Ask solitude enjoyment directly; ask intentional time-making only when unresolved."
        " Keep acceptance of invitations as a separately identified conditional dimension."
    )
    a0["interpretation_limit"] += (
        " Enjoyment, actively arranging time alone, and declining invitations are"
        " different observations. Do not infer one from another."
    )
    status = questions["TF1-STATUS"]
    status["scoped_measured_dimension"] = "intrinsic_subjective_value_of_recognition"
    status["exclude_historical_joint_facet_without_new_admission"] = [
        "D19.status_ownership",
    ]
    status["historical_facet_display_note"] = (
        "Historic D19.status_ownership combined separate STATUS and OWNERSHIP routes."
        " Current STATUS concerns recognition alone and the laptop ownership example must not appear as its evidence."
    )
    status["interpretation_limit"] += (
        " Recognition value is not evidence of laptop ownership motivation,"
        " control of resources, or invitation-sensitive entry into a role."
    )
    candidate["scope_guard"] = (
        "This questionnaire is not live, no chart labels are exposed to participants,"
        " no old answers or frozen v7 guidance are changed, and suggestion choices"
        " do not score as stable personality without source-grounded confirmation."
    )
    assert len(candidate["questions"]) == len(current["questions"]) == 25
    return candidate


def make_idiographic_module() -> dict:
    return {
        "schema": "life-patterns-idiographic-inventory-protocol-v0",
        "status": "VOLUNTARY_DEV_ONLY_NOT_LIVE_NOT_SCORED",
        "module_id": "UNUSUAL-BEHAVIORS-V0",
        "intended_use": "Elicit concrete participant-specific behaviors not anticipated by the closed questionnaire; measure added information content and response process, not natal uniqueness a priori.",
        "opening_prompt": (
            "What are some specific things you do, like, notice, or handle differently from many people around you?"
            " Small everyday habits count. They need not be positive or impressive; if none come to mind, that's fine."
            " Start with one to three, and we can continue if you want."
        ),
        "target_list_size_if_willing": "up to 10–20 total; not a required quota",
        "initial_batch_size": 3,
        "optional_continuation": "Would you like to add more? We can work toward 10–20 if you have them, or stop whenever you prefer.",
        "can_record_zero": True,
        "example_categories_if_stuck": [
            "A small household or daily routine you do differently",
            "A decision rule or shortcut you use repeatedly",
            "A way you learn, fix, organize or adapt something",
            "A preference or reaction that differs within your peer group",
            "A social habit that surprises people who know you",
        ],
        "example_safety": "Do not prompt unsafe techniques or celebrate disregarding safety instructions. If a person describes a risky behavior, preserve it as source while avoiding operational encouragement.",
        "follow_up_per_item_only_if_informative": [
            "What exactly do you do, and how often in ordinary circumstances?",
            "Who are you comparing yourself with, and why do you think this differs?",
            "How long have you done it, and what circumstances make you do it or not do it?",
            "What do you get out of doing it that way, if anything?",
            "Can you recall a time you chose the usual approach instead?",
        ],
        "followup_limit": "At most one or two high-information clarifications per item, not all five every time.",
        "participant_control": [
            "Other free text",
            "Can't think of one now",
            "That's all for now",
            "Prefer to skip",
        ],
        "data_schema_per_item": {
            "verbatim_description": "string_required_if_item_submitted",
            "context_and_frequency": "string_or_unknown",
            "comparison_group": "string_or_unknown",
            "self_assessed_rarity": "common|somewhat_unusual|very_unusual|unknown",
            "reason_for_choice": "string_or_unknown",
            "conditions_and_counterexamples": "string_or_unknown",
            "spontaneously_recalled": "boolean",
            "prompted_category_used": "boolean",
            "neutral_behavioral_candidate_tags": "list_of_hypotheses_not_confirmed_traits",
            "objective_prevalence_verified": "false_by_default",
            "chart_prediction_admitted": "false_by_default",
        },
        "no_trait_from_count": "Number of volunteered items measures recall and response process as much as unusual behavior; zero/short lists do not imply an ordinary chart or hard-to-find DOB.",
        "coding_rule": "Distinguish concrete action, motivation, opportunity, costs and constraints. Do not infer creative/nonconformist/rational traits from one example; test competing explanations and counterexamples, with source quotes.",
        "birth_predictiveness_hypothesis": "Candidate only: independently measure within-cohort behavioral distinctiveness; test whether it incrementally predicts true-chart identification rank beyond existing respondent covariates and baseline survey. Never equate behavioral rarity with chart rarity by assumption.",
        "evaluation_design": {
            "design": "Prospective randomized open-only vs optional category-scaffold versions on new, untouched participants; measure recall count, specificity and perceived helpfulness; keep all answers unscored for birth matching until independent preregistered coding and mapping.",
            "later_blind_chart_test": "Same participants and candidate universe compared with standard questions alone, uniqueness inventory alone, and combined source; include a matched chart-permutation null and a simple non-chart personal-detail baseline.",
            "count_not_scoring": True,
            "birth_data_hidden_from_interviewer": True,
            "no_person_known_to_designer_as_validation": True,
            "no_unproven_birth_difficulty_inference": True,
        },
    }


if __name__ == "__main__":
    v3 = make_v3()
    mod = make_idiographic_module()
    out = HERE / "tendency-first-v3-scaffold-development.json"
    out.write_text(json.dumps(v3, indent=2, ensure_ascii=False) + "\n")
    (HERE / "unusual-behavior-inventory-v0.json").write_text(
        json.dumps(mod, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        "v3_questions",
        len(v3["questions"]),
        "with_examples",
        sum(bool(q["example_answer_paths"]) for q in v3["questions"]),
        "idiographic_status",
        mod["status"],
    )
