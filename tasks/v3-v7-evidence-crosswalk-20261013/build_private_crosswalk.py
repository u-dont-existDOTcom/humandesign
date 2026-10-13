"""Private Life Patterns source-evidence crosswalk: 79/84 V7 vs new V3.

All sensitive participant text is read locally and emitted only to a private
owner-chosen directory. The public aggregate has ONLY route IDs and neutral
methodological classifications, never original answer excerpts or chart data.

This is a DEVELOPMENT source comparison, not a chart-scoring or prediction model.
"""

from __future__ import annotations

import argparse
import html
import json
import os
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any

# Classes are *development interpretation of the item*, not trait directions.
# Counts and severity must not be taken as objective psychometric measurements.
ROUTE_FLAGS: dict[str, tuple[str, str, str]] = {
    "TF1-A0": (
        "adds_condition_or_domain",
        "The new item elicits enjoyment of solitude; the original tests a particular friend-invitation tradeoff. These are distinct and not interchangeable.",
        "Ask enjoyment and proactively arranging solitude separately; preserve the friend-invitation boundary as its own follow-up.",
    ),
    "TF1-G19": (
        "compatible_narrow",
        "Both versions allow time negotiation based on consequences; the new answer partly repeats the old contingency.",
        "If useful, ask for one recent real case where the relationship and urgency point in different directions.",
    ),
    "TF1-F0": (
        "compatible_narrow",
        "Listener- and relationship-dependent communication is compatible with the historical answers; no change in actual communication capacity is demonstrated.",
        "Compare similar requests to two different audiences and ask which exact expression changed.",
    ),
    "TF1-G05": (
        "compatible_narrow",
        "Persuasion outcomes depend on audience and circumstances in both sources; neither alone proves persuasion effectiveness.",
        "Separate demonstrated capacity to persuade from preferred frequency/use.",
    ),
    "TF1-M11": (
        "adds_condition_or_domain",
        "New examples add need/affordability and willingness to negotiate; the older scripted allocation did not establish a stable priority.",
        "Compare two concrete allocations with opposed principles; avoid treating all practical fairness norms as traits.",
    ),
    "TF1-G06": (
        "compatible_narrow",
        "The earlier source has a specific learned group-helping pattern, whereas the new examples capture present conditional contributions.",
        "Keep childhood-to-current change and social learning separate from innate role preferences.",
    ),
    "TF1-G01": (
        "non_discriminating_choices",
        "All offered strategies can naturally occur in sequence. Selection does not establish one stable first action.",
        "Elicit a recent specific conflict and first step before presenting options.",
    ),
    "TF1-G02": (
        "non_discriminating_choices",
        "Explanation methods depend on listener, content and sequence; selecting all options supplies no stable choice preference.",
        "Ask what the person said first in an actual explanation and what response indicated success.",
    ),
    "TF1-D0": (
        "adds_condition_or_domain",
        "Refinement can be pleasurable, instrumental or tiring at different times; old instrumental example does not negate intrinsic enjoyment in another setting.",
        "Separate practising beyond adequate performance without external rewards from practice necessary to avoid errors.",
    ),
    "TF1-G10": (
        "compatible_narrow",
        "Both sources describe negotiating group expectations conditional on availability and practical responsibilities.",
        "Anchor to a real case of accepted group terms that later conflict with personal constraints.",
    ),
    "TF1-M03": (
        "scope_or_wording_tension",
        "Finishing a particular accepted feasible task does not logically exclude dropping a minor optional commitment when circumstances differ.",
        "Distinguish important feasible promises, minor favors, renegotiations and externally caused inability.",
    ),
    "TF1-B0": (
        "adds_condition_or_domain",
        "Old mood response may involve perceived responsibility for supporting someone; new qualifications introduce relationship closeness and self-involvement.",
        "Contrast emotional contagion with guilt/responsibility, then assess recovery after separation.",
    ),
    "TF1-G15": (
        "adds_condition_or_domain",
        "Ordinary engaging mental work and physically demanding tasks impose different loads; both can be enjoyable and tiring.",
        "Compare task type, duration, intensity, sleep and interest instead of collapsing energy into one pole.",
    ),
    "TF1-G16": (
        "non_discriminating_choices",
        "Multiple motives can simultaneously sustain effort; broad prompts do not establish which drives behavior when incentives conflict.",
        "Ask about a real stalled project and a meaningful tradeoff among motives.",
    ),
    "TF1-G18": (
        "adds_condition_or_domain",
        "Social recovery and desire for more company vary with group, duration and intimate relationships.",
        "Compare like-duration social situations and the subsequent voluntarily chosen activity.",
    ),
    "TF1-G17": (
        "adds_condition_or_domain",
        "Consequences and social receptiveness are separate axes affecting whether a known error is corrected.",
        "Separate internal impulse to correct from actual expression and choose matched minor/consequential examples.",
    ),
    "TF1-STATUS": (
        "adds_condition_or_domain",
        "Recognition from valued people can matter differently from generic approval; no laptop or resource-ownership inference follows.",
        "Ask exactly what was recognized, by whom and whether benefit/invitation accompanied it.",
    ),
    "TF1-ROUTINE-CHANGE": (
        "adds_condition_or_domain",
        "Seeking novelty in one domain can coexist with preference for stability or commitment in another; not one novelty score.",
        "Compare equivalent alternatives across clearly named domains and time periods.",
    ),
    "TF1-G23": (
        "non_discriminating_choices",
        "The prompt does not reliably determine a stable first-notice category; all offered possibilities depend on what occurs.",
        "Either retire as a chart-scoring item or ask an actual unfamiliar group episode with corroborable first observation.",
    ),
    "TF1-G04": (
        "adds_condition_or_domain",
        "The follow-up supplies a conditional troubleshooting decision rule, whereas the old vignette illustrated one available tool.",
        "Test whether the decision rule recurs in independent tasks; preserve critique of the item as instrument feedback.",
    ),
    "TF1-G22": (
        "compatible_narrow",
        "Ease of resuming depends on salience and duration of interruption in both accounts; no contradiction.",
        "Distinguish resumption from sustained concentration, with matched interrupted tasks.",
    ),
    "TF1-M05": (
        "non_discriminating_choices",
        "First warning indicators depend on the specific threat and evidence; all examples can fit different situations.",
        "Ask about the timing of felt signals vs objective cues in one actual uncertain situation.",
    ),
    "TF1-G20": (
        "non_discriminating_choices",
        "Practical resources can simultaneously serve independence, security, experiences and helping others; the choices are not mutually exclusive.",
        "Ask what a person actually funded and what option was forgone under matched costs.",
    ),
    "TF1-M01": (
        "scope_or_wording_tension",
        "Earlier specific response to unjustified pressure and broad endorsements of varied responses cannot establish one unconditional direction.",
        "Compare similar objective deadlines under different sources of pressure and track actual pace vs feelings.",
    ),
    "TF1-PREFER-EXCHANGE": (
        "novel_unmatched",
        "No exact historical PREFER-EXCHANGE route appears in the 79-turn base. Related allocation/negotiation questions exist but are not direct equivalents.",
        "Treat as new context-dependent evidence candidate, not independent corroboration of M11.",
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "Expected JSON object")
    return value


def source_routes(turn: dict[str, Any]) -> set[str]:
    labels = {turn.get("canonical_question_id"), turn.get("historical_question_id")}
    source = turn.get("source") or {}
    if isinstance(source, dict):
        labels.add(source.get("historical_question_id"))
        labels.add(source.get("canonical_question_id"))
    return {str(x) for x in labels if isinstance(x, str) and x.strip()}


def source_key(turn: dict[str, Any]) -> tuple[str, str]:
    return str(turn.get("question_text") or ""), str(turn.get("answer_text") or "")


def html_escape(v: Any) -> str:
    return html.escape(str(v if v is not None else ""), quote=True)


def build(old79: dict, frozen84: dict, current25: dict, bank: dict) -> tuple[dict, dict]:
    old = old79.get("turns")
    full = frozen84.get("turns")
    responses = current25.get("answers")
    questions = bank.get("questions")
    require(isinstance(old, list) and len(old) >= 50, "Historical source incomplete")
    require(isinstance(full, list) and len(full) >= len(old), "Reviewed source incomplete")
    require(isinstance(responses, dict), "Guided answers not an object")
    require(isinstance(questions, list) and len(questions) == 25, "Expected pinned V3 bank")
    require(
        set(responses) == {q["id"] for q in questions},
        "Guided responses don't match the 25 versioned routes",
    )
    require(set(ROUTE_FLAGS) == set(responses), "Assessment codebook does not cover question set")

    oldkeys = Counter(source_key(t) for t in old)
    fullkeys = Counter(source_key(t) for t in full)
    exact_old_to_frozen = sum((oldkeys & fullkeys).values())
    extras = sum((fullkeys - oldkeys).values())

    index: dict[str, list[dict]] = defaultdict(list)
    for turn in old:
        for route in source_routes(turn):
            index[route].append({"origin": "historical_79", "record": turn})
    for turn in full:
        for route in source_routes(turn):
            entry = index[route]
            if not any(source_key(x["record"]) == source_key(turn) for x in entry):
                entry.append({"origin": "reviewed_84_addition", "record": turn})

    unique = current25.get("unique_behaviors")
    require(isinstance(unique, list), "Unique behavior list missing")
    rows = []
    for q in questions:
        route = q["id"]
        hist = q["source_route_id"]
        answer = responses[route]
        require(isinstance(answer, dict), "Answer not an object")
        selected = answer.get("selected")
        options = q["example_answer_paths"]
        require(
            isinstance(selected, list) and all(x in options for x in selected),
            "Unknown selected example",
        )
        flags = ROUTE_FLAGS[route]
        source = list(index.get(hist, []))
        rows.append(
            {
                "question_id": route,
                "old_route_id": hist,
                "old_source_count": len(source),
                "old_direct_equivalence": bool(source),
                "category": flags[0],
                "scope_analysis": flags[1],
                "next_discriminator": flags[2],
                "new_question": q["question"],
                "selected_example_count": len(selected),
                "selected_examples": selected,
                "other": answer.get("other") or "",
                "unsure": bool(answer.get("unsure")),
                "skip": bool(answer.get("skip")),
                "new_conditional_detail": {
                    "context_rule": answer.get("context_rule") or "",
                    "recent_case": answer.get("recent_case") or "",
                    "no_stable_default": bool(answer.get("no_stable_default")),
                },
                "historical_sources": [
                    {
                        "phase": item["origin"],
                        "question_text": item["record"].get("question_text") or "",
                        "answer_text": item["record"].get("answer_text") or "",
                        "source_turn_id": item["record"].get("turn_id") or "",
                    }
                    for item in source
                ],
                "not_a_birth_chart_result": True,
            }
        )
    public = {
        "schema": "life-patterns-v3-v7-crosswalk-aggregate-v1",
        "participant_count": 1,
        "status": "DEVELOPMENT_ONLY_NOT_INDEPENDENT_TEST_NOT_BIRTH_VALIDATION",
        "old_79_count": len(old),
        "frozen_84_count": len(full),
        "old_questions_exactly_retained_in_frozen_84": exact_old_to_frozen,
        "historical_84_new_exact_pairs_vs_79": extras,
        "v3_question_count": len(rows),
        "direct_old_route_mappings": sum(bool(r["old_direct_equivalence"]) for r in rows),
        "without_direct_old_route": [
            r["question_id"] for r in rows if not r["old_direct_equivalence"]
        ],
        "v3_option_count_distribution": dict(
            sorted(Counter(r["selected_example_count"] for r in rows).items())
        ),
        "v3_with_free_text": sum(bool(r["other"]) for r in rows),
        "v3_with_saved_context_rule": sum(
            bool(r["new_conditional_detail"]["context_rule"]) for r in rows
        ),
        "v3_with_saved_recent_case": sum(
            bool(r["new_conditional_detail"]["recent_case"]) for r in rows
        ),
        "v3_with_unsure_or_skip": sum(r["unsure"] or r["skip"] for r in rows),
        "v3_unique_behavior_count": len(unique),
        "scope_category_counts": dict(Counter(r["category"] for r in rows)),
        "route_evidence_category": {
            r["question_id"]: {
                "source_route": r["old_route_id"],
                "category": r["category"],
                "historical_source_count": r["old_source_count"],
                # Individual per-question answer counts/free-text presence are private.
                # Publish only aggregate counts and item-method labels.
                "no_single_pole_inference": True,
            }
            for r in rows
        },
        "deidentified_only": True,
        "record_type": "question_route_conceptual_crosswalk_not_trait_scoring",
        "old_new_same_person_not_independent": True,
    }
    private = {
        "schema": "life-patterns-v3-v7-private-crosswalk-v1",
        "development_only": True,
        "source_warning": "One participant answered all instruments; route linkage does not imply identical question meaning or independent corroboration.",
        "source_integrity": {
            "old79_sha256": "",
            "old84_sha256": "",
            "v3_sha256": "",
            "bank_sha256": "",
        },
        "aggregate": public,
        "rows": rows,
        "unique_behaviors": unique,
    }
    return private, public


def markdown(private: dict) -> str:
    agg = private["aggregate"]
    lines = [
        "# Private Life Patterns source comparison — old interview versus guided V3",
        "",
        "**Development only, N=1.** This compares responses from the same person to related but not identical question wording. It is not a forward prediction, chart reverse-match, or independent replication.",
        "",
        "## At a glance",
        "",
        f"- The earlier {agg['old_79_count']}-answer source and the stored {agg['frozen_84_count']}-turn review share {agg['old_questions_exactly_retained_in_frozen_84']} exactly matching question-and-answer pairs. Do not count them as two independent surveys.",
        f"- **{agg['direct_old_route_mappings']}/{agg['v3_question_count']}** V3 questions have an explicit older route; the remaining item has related but not directly equivalent material.",
        f"- The V3 option-choice histogram is {agg['v3_option_count_distribution']}; **{agg['v3_with_free_text']}** answers include an additional free-text explanation.",
        "- Three self-generated distinctive behaviors are recorded, but their objective prevalence and connection to natal uniqueness are unknown.",
        "",
        "## Interpretation",
        "",
        "Repeated coverage of a theme suggests *source continuity*; it does not add independent birth-chart information. Multi-select answer anchors can introduce priming, so a change may reflect the prompt rather than personality change. To test the new format, ask blinded unfamiliar respondents with comparable contexts and a separately frozen chart-to-behavior model.",
        "",
        "The item categories are analyst-level **research notes**, not numerical personality or chart scores. A genuine contradiction requires overlapping contexts and incompatible concrete behavior, not one response that says a decision depends on circumstances.",
        "",
    ]
    for i, row in enumerate(private["rows"], 1):
        lines += [
            f"## {i}. {row['question_id']} ← historical {row['old_route_id']}",
            "",
            f"**Comparison class:** {row['category'].replace('_', ' ')}",
            "",
            f"**V3 question:** {row['new_question']}",
            "",
            f"**Selected V3 examples ({row['selected_example_count']}):**",
            "",
        ]
        lines += ["- " + str(x) for x in row["selected_examples"]] or ["- None"]
        lines += ["", "**Other, verbatim:** " + (row["other"] or "*No additional free text*"), ""]
        for entry in row["historical_sources"]:
            lines += [
                f"**Old source ({entry['phase']}) — question:** {entry['question_text']}",
                "",
                "> " + (entry["answer_text"] or "[No recorded answer]").replace("\n", "\n> "),
                "",
            ]
        if not row["historical_sources"]:
            lines += [
                "**No direct historical route.** Nearby topics may overlap conceptually but cannot be treated as a one-to-one answer.",
                "",
            ]
        lines += [
            "**Scoped comparison:** " + row["scope_analysis"],
            "",
            "**Next discriminating question if needed:** " + row["next_discriminator"],
            "",
        ]
    review = json.loads(
        (Path(__file__).resolve().parent / "INDEPENDENT-REVIEW-FACET-CROSSWALK.json").read_text()
    )
    lines += [
        "## Six independent-review findings versus the new pilot",
        "",
        "The six older independently admitted reviewer findings are NOT six new confirmations. Four V3 constructs overlap partially and two ask something materially different; NONE is an exact blind replication.",
        "",
    ]
    for item in review["items"]:
        lines += [
            "- **"
            + ", ".join(item["old_facet_ids"])
            + " → "
            + ", ".join(item["v3_route_ids"])
            + "** ("
            + item["alignment"].replace("_", " ")
            + "): "
            + item["reason"]
        ]
    lines += [
        "",
        "## Distinctive behaviors",
        "",
        "These are the participant's descriptions, **not objectively verified rare traits**. They must not be silently matched to a natal feature.",
        "",
    ]
    for item in private["unique_behaviors"]:
        lines += ["- " + str(item.get("behavior", ""))]
    lines += [
        "",
        "## Recommendation",
        "",
        "**Do not replace the current GPT's live interview bank yet.** The source comparison should inform a separately versioned optional cognitive pilot, then evaluation with previously unseen participants. A new natal rank for this already-known person would be in-sample development, not successful prediction.",
        "",
    ]
    return "\n".join(lines)


def html_report(private: dict) -> str:
    parts = []
    for row in private["rows"]:
        old_html = ""
        for item in row["historical_sources"]:
            old_html += (
                "<div class='source'><small>" + html_escape(item["phase"]) + "</small>"
                "<p>" + html_escape(item["question_text"]) + "</p>"
                "<blockquote>"
                + html_escape(item["answer_text"]).replace("\n", "<br>")
                + "</blockquote></div>"
            )
        if not old_html:
            old_html = "<p>No directly equivalent historical route.</p>"
        selected = "".join("<li>" + html_escape(s) + "</li>" for s in row["selected_examples"])
        parts.append(
            "<article class='item' data-class='" + html_escape(row["category"]) + "'>"
            "<h3>"
            + html_escape(row["question_id"])
            + " → "
            + html_escape(row["old_route_id"])
            + "</h3>"
            "<p class='category'>Comparison: "
            + html_escape(row["category"].replace("_", " "))
            + "</p>"
            "<div class='cols'><section><h4>New guided answer</h4><p>"
            + html_escape(row["new_question"])
            + "</p>"
            "<ul>"
            + selected
            + "</ul><p><b>Other:</b> "
            + html_escape(row["other"] or "(none)")
            + "</p></section>"
            "<section><h4>Historical source</h4>" + old_html + "</section></div>"
            "<p><b>What follows:</b> " + html_escape(row["scope_analysis"]) + "</p>"
            "<details><summary>Next useful behavioral contrast</summary><p>"
            + html_escape(row["next_discriminator"])
            + "</p></details>"
            "</article>"
        )
    review = json.loads(
        (Path(__file__).resolve().parent / "INDEPENDENT-REVIEW-FACET-CROSSWALK.json").read_text()
    )
    review_section = (
        "<h2>Older reviewer evidence is not six independent V3 confirmations</h2><p>Four domains overlap partially; two ask a different construct, and none is a like-for-like blind retest.</p>"
        + "".join(
            "<article><h3>"
            + html_escape(", ".join(item["old_facet_ids"]))
            + " → "
            + html_escape(", ".join(item["v3_route_ids"]))
            + "</h3><p>"
            + html_escape(item["alignment"].replace("_", " "))
            + ": "
            + html_escape(item["reason"])
            + "</p></article>"
            for item in review["items"]
        )
    )
    css = """body{font:15px/1.55 system-ui,sans-serif;margin:0;background:#f7f9fb;color:#223;max-width:1100px;padding:2rem 1rem}
h1{font-size:1.8rem}article{border:1px solid #d6dce3;border-radius:12px;padding:1.1rem;background:white;margin:1rem 0}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem}.cols section{background:#fafbfd;border-radius:8px;padding:.8rem}
.source{border-bottom:1px solid #ddd}blockquote{border-left:3px solid #bbc;padding-left:.7rem;white-space:pre-wrap}.category{font-size:.85rem;color:#4b647f}
select{font:inherit;padding:.5rem;border-radius:7px}summary{cursor:pointer}small{color:#677}
@media(max-width:700px){.cols{grid-template-columns:1fr}}
"""
    script = """const sel=document.querySelector('#category');sel.addEventListener('change',()=>{document.querySelectorAll('.item').forEach(el=>{el.hidden=sel.value!=='all'&&el.dataset.class!==sel.value})});"""
    cats = sorted(set(row["category"] for row in private["rows"]))
    options = "".join(
        "<option value='" + x + "'>" + x.replace("_", " ") + "</option>" for x in cats
    )
    header = (
        "<h1>Life Patterns — your V3 guided answers versus the historical interview</h1>"
        "<p>Private development review. Related question routes are not identical prompts; same-person comparisons are not independent birth-chart evidence.</p>"
        f"<p><b>{private['aggregate']['direct_old_route_mappings']} of {private['aggregate']['v3_question_count']} routes matched directly.</b>"
        f" {private['aggregate']['v3_with_free_text']} free-text supplements; "
        f"{private['aggregate']['v3_option_count_distribution'].get(4, 0)} four-way selections.</p>"
        "<label>Filter: <select id='category'><option value='all'>All question routes</option>"
        + options
        + "</select></label>"
    )
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Private Life Patterns V3–V7 evidence comparison</title><style>"
        + css
        + "</style></head><body>"
        + header
        + review_section
        + "\n".join(parts)
        + "<p>Every reported pattern here is a source-dependent research interpretation, not an astrological prediction or demonstrated innate trait.</p>"
        + "<script>"
        + script
        + "</script></body></html>"
    )


def safe_write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    for key in ("old79", "frozen84", "v3", "bank", "private_out"):
        parser.add_argument("--" + key.replace("_", "-"), type=Path, required=True)
    parser.add_argument("--public-aggregate-out", type=Path)
    args = parser.parse_args()
    data = [load(getattr(args, key)) for key in ("old79", "frozen84", "v3", "bank")]
    private, public = build(*data)
    for key, path in (
        ("old79", args.old79),
        ("old84", args.frozen84),
        ("v3", args.v3),
        ("bank", args.bank),
    ):
        private["source_integrity"][key + "_sha256"] = sha256(path.read_bytes()).hexdigest()
    output = args.private_out
    output.mkdir(parents=True, exist_ok=True, mode=0o700)
    output.chmod(0o700)
    safe_write(output / "My-Life-Patterns-V3-vs-Historical-Survey.md", markdown(private))
    safe_write(output / "My-Life-Patterns-V3-vs-Historical-Survey.html", html_report(private))
    safe_write(
        output / "My-Life-Patterns-V3-vs-Historical-Survey.json",
        json.dumps(private, indent=2, ensure_ascii=False) + "\n",
    )
    if args.public_aggregate_out:
        args.public_aggregate_out.parent.mkdir(parents=True, exist_ok=True)
        args.public_aggregate_out.write_text(json.dumps(public, indent=2) + "\n")
    print(
        json.dumps(
            {
                "private_report_count": 3,
                "direct_old_route_mappings": public["direct_old_route_mappings"],
                "new_questions": public["v3_question_count"],
                "categories": public["scope_category_counts"],
                "distribution": public["v3_option_count_distribution"],
                "old79_exact_retained_in_84": public["old_questions_exactly_retained_in_frozen_84"],
                "source_data_committed": False,
            }
        )
    )


if __name__ == "__main__":
    main()
