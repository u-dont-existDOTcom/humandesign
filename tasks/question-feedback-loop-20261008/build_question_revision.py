"""Prepare a prospective, non-active question wording candidate from audited defects."""

from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "apps/life-patterns-participant/participant/static/tendency-first-v1.json"
DEST = Path(__file__).resolve().parent / "tendency-first-v2-development.json"
CROSSWALK = Path(__file__).resolve().parent / "QUESTION-REVISION-CROSSWALK.md"

REVISIONS = {
    "TF1-G10": (
        "When you join a group with routines different from yours, how do you decide what to adapt and what to keep?",
        "This concerns the boundary you usually use, not whether adapting is sensible in one specific group.",
        "Elicit an actual adaptation boundary without presuming fixed resistance or demanding a repeat of a settled answer.",
    ),
    "TF1-D0": (
        "When you can already perform a skill adequately, what, if anything, makes refining a small detail worth repeating?",
        "For example, enjoyment of refinement, avoiding future errors, external demands, or other conditions are possible answers—not a required list.",
        "Separate the intrinsic value of repetition from rational practice toward a specific result.",
    ),
    "TF1-M11": (
        "When negotiating how to share work or costs, what considerations usually carry the most weight for you?",
        "An arrangement may depend on the people, prior commitments, proportional contributions, or other factors.",
        "Ask for the deciding considerations, not an obviously fair split under forced practical assumptions.",
    ),
    "TF1-G15": (
        "How does an ordinary amount of work you find worthwhile affect your energy, and what changes when the workload becomes unusually long or stressful?",
        "Do not equate an engaging activity with unlimited stamina; separate duration, intensity and context.",
        "Distinguish baseline work-energy response from fatigue under excessive load.",
    ),
    "TF1-STATUS": (
        "Apart from practical benefits, how, if at all, does recognition from people close to you affect you differently from recognition from others?",
        "No difference or no interest in either kind of recognition is also a valid answer.",
        "Preserve relationship-qualified recognition instead of collapsing all praise into one trait.",
    ),
    "TF1-G04": (
        "When a familiar approach stops working, what do you usually try first to figure out why?",
        "The method you prefer is relevant; merely saying you would try to fix the problem is not.",
        "Avoid coding the obvious fact of troubleshooting as a personality finding.",
    ),
    "TF1-M03": (
        "When a small voluntary commitment becomes less appealing, what normally determines whether you complete it, renegotiate, or drop it?",
        "An answer may depend on other people's reliance on you, the cost, or the kind of commitment.",
        "Elicit the boundary behind follow-through rather than treating waning enthusiasm as dishonesty.",
    ),
    "TF1-ROUTINE-CHANGE": (
        "In which parts of life do you usually prefer familiar routines, and in which do you tend to seek something new when both are available?",
        "Different preferences across activities are valid; don't force a global novelty-versus-routine label.",
        "Capture domain-specific novelty preference rather than a forced binary.",
    ),
    "TF1-G17": (
        "When you notice a harmless factual mistake, what normally determines whether you feel like correcting it or letting it pass?",
        "Practical consequences are excluded here; relationships and the likelihood of appreciation may still matter.",
        "Capture the individual's low-stakes correction threshold beyond the obvious consequence calculation.",
    ),
}

original = json.loads(SOURCE.read_text(encoding="utf-8"))
proposal = copy.deepcopy(original)
proposal["version"] = "tendency-first-v2-development-20261008"
proposal["status"] = "prospective_wording_candidate_NOT_DEPLOYED_or_validated"
proposal["historical_evidence_authority"] = original["historical_evidence_authority"]
proposal["parent_policy_version"] = original["version"]
proposal["revision_basis"] = "One-person October 2026 owner pilot; development evidence only"
proposal["activation_requirement"] = (
    "New independently pinned prospective policy version plus compatibility for existing "
    "v1 saved review hashes; never overwrite v1 source or active in-flight reviews."
)
for route in ("ROMANCE-FADE", "ROOM-EFFECT", "CORRECTION-REASON"):
    if route not in proposal["retired_from_new_elicitation"]:
        proposal["retired_from_new_elicitation"].append(route)
proposal["retired_from_new_elicitation"] = sorted(set(proposal["retired_from_new_elicitation"]))
rows = []
for question in proposal["questions"]:
    route = question["id"]
    if route in REVISIONS:
        wording, example, reason = REVISIONS[route]
        prior = next(q for q in original["questions"] if q["id"] == route)
        rows.append((route, prior["question"], wording, reason))
        question["question"] = wording
        question["example_if_needed"] = example
        question["development_revision_rationale"] = reason
        question["interpretation_limit"] += (
            " This development wording is not scored as equivalent to earlier phrasing; "
            "conditions and missingness remain first-class."
        )
DEST.write_text(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
parts = [
    "# Prospective question wording revision — development draft, NOT live",
    "",
    "This edits **9 current tendency-first wordings**, in a separately versioned proposed bank. "
    "It is not the frozen v7 survey or the current TF1 v1 runtime policy. The retirement list also adds "
    "three historically weak optional routes: ROMANCE-FADE, ROOM-EFFECT and CORRECTION-REASON.",
    "",
    "The source is one development participant. No accuracy or population discrimination claim is made. "
    "The next methodological step is an independently administered cognitive interview comparing "
    "the existing and revised versions, followed by a new prospective freeze.",
    "",
]
for route, old, new, why in rows:
    parts.extend([f"## {route}", "", f"Old: {old}", "", f"Revised: {new}", "", f"Why: {why}", ""])
parts.extend(
    [
        "## Activation safety",
        "",
        "Do not overwrite `tendency-first-v1.json` or rewrite `TENDENCY-FIRST-GUIDE-v1.json` "
        "for an existing saved review. Introduce the proposed version with a new pinned "
        "identity and state-aware old/new review routing only after wording tests and evidence checks.",
        "",
    ]
)
CROSSWALK.write_text("\n".join(parts), encoding="utf-8")
print(f"revised_question_count={len(rows)} retired_additions=3 deployed=false")
