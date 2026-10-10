"""Explicit hypothesis-to-observation prototypes, no runtime weights/scoring."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIDGE = json.loads((HERE / "question_to_chart_hypotheses_v0.json").read_text())
# Only data from theory and neutral behavioral contrasts. These are NOT actual
# human-based predictive effect sizes, probabilistic calibrations, or diagnoses.
CODEBOOK = {
    "HD-TYPE-PROJECTOR": (
        "Repeated real role entry becomes easier or more effective when invited on the basis of specific recognized contribution, contrasted with matched uninvited advice.",
        "Matched self-initiated/solicited contributions show no invitation-related difference across occasions.",
        "Praise without invitation; ordinary politeness; role hierarchy; one anecdote without counterfactual.",
    ),
    "HD-AUTH-SPLENIC": (
        "A subtle bodily signal usually precedes explicit reasoning on real consequential decisions, is immediate and does not recur with deliberation.",
        "Matched real choices are repeatedly decided only after delayed emotional shifts, with no reported early bodily signal.",
        "Learned bodily vocabulary; obvious danger cues; general anxious feelings; theoretical authority labels.",
    ),
    "HD-AUTH-EMOTIONAL": (
        "The reported yes/no about real important choices predictably changes as emotions settle over time rather than feeling decisively clear at the outset.",
        "Decisions across matched important choices have immediate stable clarity despite emotional changes.",
        "More information arriving over time; avoidance of accountability; minor preferences.",
    ),
    "HD-SP-OPEN": (
        "Person reports mood intensification in proximity to an upset other, then return toward baseline after separation in comparable situations.",
        "No detectable affective shifts across repeated exposure to others’ strong moods, with context and relationship controlled.",
        "General compassion, interpersonal conflict directed at participant, preexisting mood, acute mental-health changes.",
    ),
    "HD-ROOT-OPEN": (
        "Imposed urgency changes felt pressure/pace despite constant objective deadline, and pressure drops when interpersonal urgency is removed.",
        "Equal objective deadlines and workload produce similar pace despite different external urgency signals across cases.",
        "Urgent requests with genuine penalties; practical prioritization; medical anxiety.",
    ),
    "HD-SACRAL-DEFINED": (
        "Reports sustainable interest-matched ordinary work compared with similarly engaged peers, with clear duration and recovery qualifiers.",
        "Repeating large depletion during ordinary feasible workloads despite sleep, health, motivation and workload matching.",
        "Extraordinary all-night work, health or sleep disorders, noncomparable work intensity, success/self-image.",
    ),
    "HD-HEART-DEFINED": (
        "Freely adopted important feasible commitments are repeatedly delivered after enthusiasm wanes, with separately reported selection threshold.",
        "Repeated failures of deeply chosen feasible important promises without changed conditions or external obstacles.",
        "Casual favors, imposed duties, coercion, inaccessible resources and moral judgments.",
    ),
    "HD-CH-16-48": (
        "Repeatedly initiates optional fine-detail refinement after competence is adequate and despite no external reward, not only to prevent known mistakes.",
        "Across valued skills, no tendency toward voluntary refinement once sufficient for the purpose.",
        "Required rehearsal, performance pressure, one language-learning example, perfectionism label alone.",
    ),
    "HD-CH-43-23": (
        "New personally generated insight is frequently translated into a communicable explanation and changes others’ understanding according to actual examples.",
        "Insights are not expressed or repeatedly fail to become communicable even in receptive contexts.",
        "Summarizing public information, courtesy explanations, teacher title, success judged by speaker alone.",
    ),
    "HD-CH-58-18": (
        "Notices recurring correctable flaws and feels improvement impulse across real stakes, independent of whether speaking up would be appreciated.",
        "Consistently lacks improvement impulse for noticed consequential, feasible-to-correct problems.",
        "One trivial error, duty-bound correction, criticism for status, objective harm judgments after the fact.",
    ),
    "HD-CH-52-9": (
        "Sustains stationary concentration on intrinsically valuable tasks over time with controls for interests and interruptions.",
        "Repeated inability to remain on any meaningful interest-matched task despite suitable conditions.",
        "Ability to resume after interruption, hyperfocus on entertainment, sleep/health factors, motivational inconsistency.",
    ),
    "HD-G-DEFINED": (
        "Narrative reports stable personally chosen direction across materially different life contexts and relationships.",
        "Multiple concrete life contexts show radically externally determined direction changes without self-directed continuity.",
        "A single fixed career label, moral desirability of consistency, personality inventory self-description without examples.",
    ),
}
assert set(CODEBOOK) == {h["hypothesis_id"] for h in BRIDGE["theory_hypotheses"]}
book = {
    "schema": "life-patterns-theory-evidence-codebook-v0",
    "status": "UNSCORED_HYPOTHESES_NO_INFERENCE",
    "theory_bridge_sha256": __import__("hashlib")
    .sha256((HERE / "question_to_chart_hypotheses_v0.json").read_bytes())
    .hexdigest(),
    "interpretation": "These examples are prospective operationalizations of source claims and potential contradictions, not empirically demonstrated causal correlates.",
    "admission_policy": [
        "Use only exact answer quotes from blinded respondents; never ask for birth/chart clues.",
        "No fact inferred merely from job/sex/occupation/age/education or prompt premise.",
        "A matched repeated counterexample can challenge a positive claim; unknown and chart absence are not negative scores.",
        "Allow partial conditional coding and abstain; do not transform missing into opposite pole.",
        "Dependent questions count as one evidence family, not multiple independent hits.",
        "Blinded neutral coder must not see target features, rule weights, true-chart rank, or expected answers.",
        "No numeric weights or probabilities until independently estimated from a separate training cohort and frozen.",
    ],
    "hypotheses": [
        {
            "hypothesis_id": k,
            "positive_evidence_if_multiple_situations": yes,
            "possible_counterevidence_not_automatic_inverse": no,
            "must_abstain_if": abstain,
            "unknown_is_valid": True,
            "chart_feature_absence_does_not_imply_opposite": True,
            "score_weight": None,
            "probability": None,
            "status": "PROVISIONAL_NOT_ACTIVE",
        }
        for k, (yes, no, abstain) in CODEBOOK.items()
    ],
}
(HERE / "source_to_target_evidence_codebook_v0.json").write_text(
    json.dumps(book, ensure_ascii=False, indent=2) + "\n"
)
print(
    len(book["hypotheses"]), "hypotheses with explicit evidence/counterevidence/abstention coding"
)
