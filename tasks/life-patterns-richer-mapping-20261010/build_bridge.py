"""Reproducible, target-blind QUESTION-to-CONSTRUCT-to-THEORY audit.

This is NOT a scoring or chart decoder. Live interview questions remain unchanged.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
ACTIVE = ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
V2 = ROOT / "tasks/question-feedback-loop-20261008/tendency-first-v2-development.json"

# Theory's own stated hypotheses; they are not empirically validated predictions.
# Exact chart features are kept OUTSIDE participant-visible interview metadata.
TARGETS = [
    (
        "HD-TYPE-PROJECTOR",
        "Type: Projector",
        {"feature": "type", "equals": "Projector"},
        "Recognition for a specific contribution followed by an invitation matters for entering interpersonal roles; not simply liking praise.",
        "https://jovianarchive.com/pages/projector-human-design",
        "TYPE_ENTRY",
    ),
    (
        "HD-AUTH-SPLENIC",
        "Authority: Splenic",
        {"feature": "authority", "equals": "Splenic"},
        "A quick and non-repeating felt safety/correctness signal may precede reasoning, versus clarity emerging after time.",
        "https://jovianarchive.com/pages/splenic-authority-in-human-design-the-bodys-quiet-instant-knowing",
        "DECISION_TIMING",
    ),
    (
        "HD-AUTH-EMOTIONAL",
        "Authority: Emotional",
        {"feature": "authority", "equals": "Emotional"},
        "For personally consequential decisions, clarity may change over time with an emotional wave rather than being immediate.",
        "https://jovianarchive.com/pages/projector-human-design",
        "DECISION_TIMING",
    ),
    (
        "HD-SP-OPEN",
        "Solar Plexus: undefined",
        {"feature": "center", "name": "Solar Plexus", "defined": False},
        "A close person’s mood may be felt or amplified, with relief or return toward baseline after separation; distinct from empathy.",
        "https://jovianarchive.com/blogs/human-design-daily-life/type-childhood-the-emotional-system",
        "EMOTIONAL_CONDITIONING",
    ),
    (
        "HD-ROOT-OPEN",
        "Root: undefined",
        {"feature": "center", "name": "Root", "defined": False},
        "Interpersonal urgency can create pressure to hurry even when the objective deadline has not changed.",
        "https://jovianarchive.com/pages/the-nine-centers-of-the-bodygraph-in-human-design",
        "EXTERNAL_PRESSURE",
    ),
    (
        "HD-SACRAL-DEFINED",
        "Sacral: defined",
        {"feature": "center", "name": "Sacral", "defined": True},
        "Sustained access to work energy for suitably engaging activity; effects of prolonged extreme load are a separate question.",
        "https://jovianarchive.com/pages/the-nine-centers-of-the-bodygraph-in-human-design",
        "WORK_ENERGY",
    ),
    (
        "HD-HEART-DEFINED",
        "Heart/Ego: defined",
        {"feature": "center", "name": "Heart", "defined": True},
        "Reliable willpower for consciously accepted meaningful commitments; not every casual promise or obligation.",
        "https://jovianarchive.com/blogs/human-design-basics/the-9-centers-in-human-design",
        "COMMITMENT",
    ),
    (
        "HD-CH-16-48",
        "Channel: 16–48",
        {"feature": "channel", "equals": "16-48"},
        "Fine-detail practice/refinement can be intrinsically compelling, separable from instrumental rehearsal to avoid future mistakes.",
        "https://jovianarchive.com/pages/channels-in-human-design-the-life-force",
        "PRACTICE_REFINEMENT",
    ),
    (
        "HD-CH-43-23",
        "Channel: 43–23",
        {"feature": "channel", "equals": "43-23"},
        "Distinctive insights are converted into communicable expression; ordinary politeness or summarizing for an audience is insufficient.",
        "https://jovianarchive.com/blogs/chart-interpretations-components/how-to-read-your-human-design-chart-a-step-by-step-intro",
        "INSIGHT_EXPRESSION",
    ),
    (
        "HD-CH-58-18",
        "Channel: 58–18",
        {"feature": "channel", "equals": "58-18"},
        "Repeated impulse to detect and improve patterns/problems; distinguish noticing flaws from choosing to speak up, and stakes.",
        "https://jovianarchive.com/blogs/human-design-daily-life/understanding-the-logic-circuit-group",
        "CORRECTION",
    ),
    (
        "HD-CH-52-9",
        "Channel: 52–9",
        {"feature": "channel", "equals": "52-9"},
        "Ability/drive to sustain concentrated attention on a worthy task; ease of resuming after interruption alone is not sufficient.",
        "https://jovianarchive.com/blogs/human-design-daily-life/understanding-the-logic-circuit-group",
        "CONCENTRATION",
    ),
    (
        "HD-G-DEFINED",
        "G Center: defined",
        {"feature": "center", "name": "G", "defined": True},
        "Relative stability of identity/direction across environments, not mere refusal to change a working style.",
        "https://jovianarchive.com/blogs/human-design-basics/the-9-centers-in-human-design",
        "IDENTITY_DIRECTION",
    ),
]

# Row columns: neutral measured construct, contrast required to interpret,
# confound / why current wording underdetermines, scope of defect,
# proposed revision (empty = preserve), mapping hypotheses behind separate firewall.
CONTRACTS = {
    "TF1-A0": (
        "company preference conditioned on closeness and available solitude",
        "frequency of company-seeking vs protected solo time at comparable opportunity",
        "recent contact, obligations, money and energy",
        "broad_context",
        "",
        [],
    ),
    "TF1-G19": (
        "boundaries under competing commitments",
        "helping vs protecting prior plans when request consequences are matched",
        "emergency, obligation, relationship and negotiation options",
        "mixed_context",
        "",
        [],
    ),
    "TF1-F0": (
        "voluntary audience-specific expression adaptation",
        "choice of explanation for different audiences beyond ordinary courtesy",
        "communication skill, safety, trust and social norms",
        "weak_target_alignment",
        "",
        [],
    ),
    "TF1-G05": (
        "reported persuasion outcomes and engagement",
        "willingness to try versus actual influence success and feedback",
        "self-rated skill, selection of easy targets, urgency, relationship",
        "mixed_constructs",
        "When you try to persuade someone about a shared plan, how often does the other person actually change position, and what tends to make the difference?",
        [],
    ),
    "TF1-M11": (
        "criteria for allocating shared work or costs",
        "relative contribution, equality, need and agreement-seeking",
        "fairness conventions and actual power to decide",
        "obvious_normative_response",
        "",
        [],
    ),
    "TF1-G06": (
        "entry into unassigned group roles",
        "independent initiative versus waiting to be asked for specific contribution",
        "task competence, hierarchy and cultural politeness",
        "target_mismatch",
        "In a group where you have something useful to contribute, what usually determines whether you speak up before anyone asks or wait for someone to request your help?",
        ["HD-TYPE-PROJECTOR"],
    ),
    "TF1-G01": (
        "first approach to ambiguous information",
        "self-organizing, asking, testing and seeking tools under similar constraints",
        "task size, urgency, expertise and external assistance",
        "broad_construct",
        "",
        [],
    ),
    "TF1-G02": (
        "tailoring information for listeners",
        "original insight-to-expression versus ordinary listener-tailoring",
        "listener knowledge, teachability, professional role",
        "target_mismatch",
        "When an idea feels new to you, what usually happens between first understanding it and trying to put it into words for someone else?",
        ["HD-CH-43-23"],
    ),
    "TF1-D0": (
        "motivation for repeated fine-detail refinement",
        "intrinsic enjoyment of refinement vs practice only for a practical goal",
        "novice level, performance stakes, available time",
        "instrumental_intrinsic_confound",
        "If your skill is already adequate and there is no outside reward, when do you still find yourself refining small details?",
        ["HD-CH-16-48"],
    ),
    "TF1-G10": (
        "adaptation to established group practices",
        "own preference retention vs negotiated adjustment",
        "role authority, group constraints and consequences",
        "normative_context",
        "",
        [],
    ),
    "TF1-M03": (
        "follow-through when enthusiasm changes",
        "serious voluntary commitments versus small casual promises",
        "objective feasibility, obligation to others, uncertainty",
        "target_mismatch",
        "For an important commitment you freely accepted and could realistically keep, what usually happens if your enthusiasm fades?",
        ["HD-HEART-DEFINED"],
    ),
    "TF1-B0": (
        "mood coupling with other people",
        "in-the-moment mood absorption versus independent emotional changes, and recovery after separation",
        "empathy, conflict, baseline mood and distress",
        "incomplete_contrast",
        "When someone close is upset but not upset with you, what happens to your own mood while you are together and after you part?",
        ["HD-SP-OPEN"],
    ),
    "TF1-G15": (
        "work-energy response across task loads",
        "sustainable ordinary engagement versus exhaustion under comparable prolonged demand",
        "sleep, health, task interest, duration and exertion",
        "multi_construct_energy",
        "When you work on something worthwhile at an ordinary pace for several hours, what happens to your energy afterward? How does unusually long or intense work differ?",
        ["HD-SACRAL-DEFINED"],
    ),
    "TF1-G16": (
        "persistence motives for meaningful tasks",
        "effort for purpose, progress, recognition or commitment",
        "importance, rewards and prior obligations",
        "non_specific_target",
        "",
        [],
    ),
    "TF1-G18": (
        "social recovery vs reflective withdrawal",
        "withdrawal to think/process versus recovery from fatigue",
        "social demands, sleep, group size and intimacy",
        "weak_target_alignment",
        "",
        [],
    ),
    "TF1-G17": (
        "correction impulse across practical stakes",
        "noticed trivial mistakes vs consequential errors; internal pull vs interpersonal correction",
        "risk, social receptiveness and personal expertise",
        "target_mismatch",
        "When you notice a harmless mistake versus one with important consequences, how does your immediate urge to correct it differ from what you actually do?",
        ["HD-CH-58-18"],
    ),
    "TF1-STATUS": (
        "intrinsic reward from others’ recognition",
        "personal appreciation vs being specifically invited into a meaningful role",
        "relationship closeness, flattery, practical benefit",
        "target_mismatch",
        "",
        [],
    ),
    "TF1-ROUTINE-CHANGE": (
        "preference for novelty across life domains",
        "new vs familiar when both equally available and meaningful",
        "affordability, accessibility, social context",
        "broad_context",
        "",
        [],
    ),
    "TF1-G23": (
        "first attention in an unassigned group",
        "noticing needs, people, roles, resources or errors first",
        "scene dependence and social desirability",
        "under_specified",
        "In a group task that has not been organized yet, what do you usually notice before anyone has decided what to do? Include a recent example and what you did with that observation.",
        [],
    ),
    "TF1-G04": (
        "method for diagnosing failure",
        "check evidence, isolate causes, try alternatives, consult others",
        "task difficulty and expertise",
        "low_discrimination",
        "When an approach fails, what is the first thing you usually check, and how does that differ between a familiar task and one you have never done?",
        [],
    ),
    "TF1-G22": (
        "resuming attention after interruption",
        "ease of reacquisition vs sustained focus without interruption",
        "interruptions themselves, sleep, motivation and ADHD/health factors",
        "target_mismatch",
        "For a problem you consider worth solving, how often can you stay deeply focused without switching tasks, and what changes when you are interrupted?",
        ["HD-CH-52-9"],
    ),
    "TF1-M05": (
        "first signals of possible danger or mismatch",
        "immediate bodily alert vs later reasoned inference",
        "prior experience, anxiety and objective cues",
        "target_mismatch",
        "When you first suspect something may be unsafe, what usually alerts you, if anything, and how does that impression change as you learn more?",
        ["HD-AUTH-SPLENIC"],
    ),
    "TF1-G20": (
        "preferred function of extra resources",
        "autonomy/control vs status/security/helping others",
        "economic constraint and family obligations",
        "non_specific_target",
        "",
        [],
    ),
    "TF1-M01": (
        "external urgency effects with unchanged deadline",
        "speeding up under other people’s pressure vs objective urgency",
        "real consequences of delaying and power dynamics",
        "near_source_construct",
        "",
        ["HD-ROOT-OPEN"],
    ),
    "TF1-PREFER-EXCHANGE": (
        "willingness to negotiate contested allocation",
        "continuing vs withdrawing after disagreement, separate from negotiation success",
        "power, importance, practicality and fairness",
        "not_direct_chart_target",
        "",
        [],
    ),
}

# Additional missing chart-discriminating constructs are not derivable from the
# existing 25 prompts. These questions are brand new and NOT for live use.
ADDITIONAL = [
    (
        "NEW-DECISION-TIMING",
        "HD-AUTH-SPLENIC",
        "HD-AUTH-EMOTIONAL",
        "On a consequential choice with no urgent deadline, what first tells you yes or no, and how—if at all—does that sense change over the next day or two?",
        "Separate quick bodily reaction from emotional evolution and deliberate analysis; allow none/variable.",
    ),
    (
        "NEW-RECOGNIZED-ENTRY",
        "HD-TYPE-PROJECTOR",
        None,
        "Think of times you had useful input for a group. What determines whether you volunteer it immediately or wait until someone asks for your contribution?",
        "Evidence must distinguish invitation/recognition from courtesy, role hierarchy and being asked to help.",
    ),
    (
        "NEW-EMOTIONAL-TIMING",
        "HD-AUTH-EMOTIONAL",
        None,
        "When you care about a decision, does the answer usually feel stable from the beginning, or change with your feelings over time? Describe exceptions.",
        "Do not count deliberate research or indecisiveness as an emotional wave.",
    ),
    (
        "NEW-IDENTITY-DIRECTION",
        "HD-G-DEFINED",
        None,
        "Across major changes of work, home or social circles, which parts of your sense of direction have stayed stable and which have changed?",
        "No identity label and no assumption that stable direction is better.",
    ),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict:
    active = json.loads(ACTIVE.read_text())
    v2 = json.loads(V2.read_text())
    proposed = {q["id"]: q for q in v2["questions"]}
    qids = {q["id"] for q in active["questions"]}
    assert set(CONTRACTS) == qids, {
        "extra": set(CONTRACTS) - qids,
        "missing": qids - set(CONTRACTS),
    }
    hypothesis = [
        {
            "hypothesis_id": k,
            "source_feature_label": label,
            "chart_predicate": pred,
            "theory_claim": claim,
            "theory_source_url": url,
            "dependency_cluster": group,
            "epistemic_status": "HD_SOURCE_THEORY_ONLY_NOT_HUMAN_VALIDATED",
            "scoring_status": "UNSCORED_PROSPECTIVE_DRAFT",
        }
        for k, label, pred, claim, url, group in TARGETS
    ]
    hypothesis_ids = {h["hypothesis_id"] for h in hypothesis}
    rows = []
    for q in active["questions"]:
        qid = q["id"]
        construct, contrast, confounds, defect, new, links = CONTRACTS[qid]
        assert set(links) <= hypothesis_ids
        inherited = proposed[qid]["question"]
        revised = new or (inherited if inherited != q["question"] else "")
        status = "no_chart_claim" if not links else "needs_new_evidence_then_theory_link_trial"
        if qid == "TF1-M01":
            status = "question_near_claim_still_unscored"
        rows.append(
            {
                "question_id": qid,
                "source_route_id": q["source_route_id"],
                "original_question": q["question"],
                "original_question_sha256": hashlib.sha256(q["question"].encode()).hexdigest(),
                "measured_construct": construct,
                "discriminating_contrast": contrast,
                "important_confounders": confounds,
                "defect_or_limit": defect,
                "draft_revised_question": revised,
                "draft_revision_origin": "new_mapping_audit"
                if new
                else "existing_v2_development"
                if revised
                else "none",
                "hypothesis_ids_behind_blind_wall": links,
                "target_link_status": status,
                "evidence_rule": "Do not code a trait without an answer supporting one side plus its conditions; otherwise unknown or mixed. A self-report is never observed performance.",
                "contrast_rule": "Missing/conditional replies are not contradictions. A chart with the feature absent does not automatically predict the opposite behavior.",
                "participant_blinding": "Keep chart hypotheses and feature predicates out of the interviewer or participant questionnaire.",
            }
        )
    addition = [
        {
            "draft_id": rid,
            "candidate_question": question,
            "hypothesis_ids": [x for x in (a, b) if x],
            "coding_limit": limit,
            "status": "NOT_ASKED_NOT_ACTIVE_NOT_SCORED",
        }
        for rid, a, b, question, limit in ADDITIONAL
    ]
    result = {
        "schema": "life-patterns-question-target-bridge-development-v0",
        "status": "DRAFT_UNSCORED_NOT_LIVE_NOT_VALIDATED",
        "input_versions": {
            "active_v1": active["version"],
            "active_v1_sha256": sha(ACTIVE),
            "existing_proposed_v2_sha256": sha(V2),
        },
        "scope": "human_design_theory_separate_from_astrohd_six_rule_astrology",
        "epistemology": "Predictions from a theoretical source are not evidence those predictions match real people or birth data.",
        "blinding": "No chart predicate/true DOB/time/owner answer data may be shown to the interviewer or used to select answers.",
        "testing_rule": "No re-tuning on owner-known chart; pre-freeze chart features, predictions, codebook, missingness and decoys; evaluate on untouched people against non-HD baselines.",
        "score_status": "NOT_ADMITTED_FOR_ANY_BIRTH_RANKING",
        "theory_hypotheses": hypothesis,
        "current_question_contracts": rows,
        "supplement_question_candidates": addition,
        "non_evidence_critical": [
            "unanswered item",
            "normative response with no contrast",
            "participant objects to a question",
            "unrelated context answer",
            "response conditioned on incentives not matched",
            "two correlated routes same pattern",
            "chart feature absent (not automatic inverse)",
            "post-target-reveal researcher interpretation",
        ],
    }
    return result


if __name__ == "__main__":
    out = build()
    path = TASK / "question_to_chart_hypotheses_v0.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(
        "question_count",
        len(out["current_question_contracts"]),
        "theory_hypotheses",
        len(out["theory_hypotheses"]),
        "draft_additions",
        len(out["supplement_question_candidates"]),
        "chart_links",
        sum(bool(x["hypothesis_ids_behind_blind_wall"]) for x in out["current_question_contracts"]),
    )
