# ruff: noqa: E501  # Long embedded HTML/JS and private report text are kept readable as strings.
"""Private, same-person V3 -> guided V3 -> V3.2 candidate -> historical interview comparison.

Owner text remains local, never committed. Public receipt includes counts only.
The new questions have no chart mapping, so this does not manufacture a DOB score.
"""

from __future__ import annotations

import argparse
import html
import json
import os
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REVISION = (
    ROOT
    / "tasks/life-patterns-guided-eight-assessment-20261015/V3_2_COGNITIVE_QUESTION_CANDIDATES.json"
)
BANK = ROOT / "tasks/life-patterns-idiographic-20261010/tendency-first-v3-scaffold-development.json"
FROZEN_RESULT = (
    ROOT
    / "tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V14-EXACT-CENTURY-RECEIPT-20260925.md"
)
ROUTES = ["TF1-G01", "TF1-G02", "TF1-G16", "TF1-G23", "TF1-M05", "TF1-G20", "TF1-M01", "TF1-M03"]
SCHEMA = "local_life_patterns_v3_pilot_unsubmitted"


def load(p: Path) -> dict:
    v = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(v, dict):
        raise ValueError("Expected JSON object")
    return v


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def private_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    path.chmod(0o600)


def summarize(
    prior: dict, updated: dict, cross: dict, bank: dict, revision: dict, baseline: str
) -> tuple[dict, list]:
    require(prior.get("schema") == updated.get("schema") == SCHEMA, "Expected original V3 exports")
    old = prior.get("answers")
    new = updated.get("answers")
    require(
        isinstance(old, dict) and isinstance(new, dict) and set(old) == set(new),
        "Question IDs do not match",
    )
    require(len(old) == 25, "Expected 25 historic original V3 answers")
    require(
        prior.get("unique_behaviors") == updated.get("unique_behaviors"),
        "Unusual behaviors mutated",
    )
    require(len(new["TF1-G01"].get("selected", [])) <= 4, "Corrupted responses")
    for route in old:
        for field in ("selected", "other", "unsure", "skip"):
            require(
                old[route].get(field) == new[route].get(field),
                f"Original answer changed: {route}/{field}",
            )
    require(len(updated["unique_behaviors"]) == 3, "Expected all three prior unusual behaviors")
    questions = bank["questions"]
    require(len(questions) == 25, "Unexpected V3 bank size")
    require(
        not any(q.get("planning_targets") or q.get("automatic_chart_scoring") for q in questions),
        "V3 bank unexpectedly acquired a scored target",
    )
    candidates = revision["items"]
    require(
        len(candidates) == 8 and {q["id"] for q in candidates} == set(ROUTES),
        "Candidate ID mismatch",
    )
    require(
        revision["status"] == "DEVELOPMENT_ONLY_NOT_LIVE_NOT_SCORED",
        "Candidate unexpectedly activated",
    )
    assert "Exactly nine instants reach it" in baseline, "Accepted V1.4d maxima not confirmed"
    assert "recorded 10:25 is jointly first" in baseline, "Accepted V1.4d instant not confirmed"
    assert "January 29, 1985 is the sole maximum-scoring date" in baseline, "Accepted V1.4d date not confirmed"

    prior_rows = {r["question_id"]: r for r in cross["rows"]}
    require(
        len(prior_rows) == 25 and set(prior_rows) == set(old), "Historical crosswalk route mismatch"
    )
    candidate_by_id = {q["id"]: q for q in candidates}
    rows = []
    for question in questions:
        route = question["id"]
        answer = new[route]
        prior_row = prior_rows[route]
        rev = candidate_by_id.get(route)
        rows.append(
            {
                "route": route,
                "historical_route": prior_row["old_route_id"],
                "historical_direct": prior_row["old_direct_equivalence"],
                "original_crosswalk_class": prior_row["category"],
                "old_comparison": prior_row["scope_analysis"],
                "historical_sources": prior_row["historical_sources"],
                "v3_question": question["question"],
                "v3_choices": answer["selected"],
                "v3_other": answer.get("other", ""),
                "new_context_rule": answer.get("context_rule", ""),
                "new_recent_case": answer.get("recent_case", ""),
                "guided_present": route in ROUTES,
                "guided_answered": route in ROUTES
                and bool(
                    answer.get("context_rule")
                    or answer.get("recent_case")
                    or answer.get("no_stable_default")
                    or answer.get("context_skipped")
                ),
                "revision_question": rev["candidate_question"] if rev else None,
                "revision_action": rev["action"] if rev else "unchanged_source_question",
                "revision_comparison_target": rev["what_to_compare"] if rev else None,
                "revision_abstain": rev["abstain_if"] if rev else None,
                "v32_current_status": "not_administered_to_developer"
                if rev
                else "unchanged_from_v3",
                "chart_scoring": "no_admitted_mapping",
            }
        )
    require(
        all(r["guided_answered"] for r in rows if r["guided_present"]), "Guided source incomplete"
    )
    counts = Counter(r["original_crosswalk_class"] for r in rows)
    receipt = {
        "schema": "life-patterns-v32-source-comparison-aggregate-v1",
        "research_status": "SAME_PERSON_DEVELOPMENT_NOT_BLIND_NATAL_TEST",
        "v3_original_question_count": len(old),
        "v3_original_answer_fields_preserved": True,
        "v3_original_unique_behaviors_preserved": True,
        "historical_direct_mapped_routes": sum(r["historical_direct"] for r in rows),
        "historical_crosswalk_classes": dict(counts),
        "v3_context_guided_routes_complete": sum(r["guided_answered"] for r in rows),
        "guided_distinct_conditional_rules": sum(bool(new[x].get("context_rule")) for x in ROUTES),
        "guided_distinct_recent_cases": sum(bool(new[x].get("recent_case")) for x in ROUTES),
        "v32_revised_prompts": len(candidates),
        "v32_core_cognitive_prompts": 6,
        "v32_optional_scoring_suspended_prompts": 2,
        "v32_newly_administered_answers": 0,
        "v32_newly_admitted_chart_features": 0,
        "existing_chart_scorer_modified": False,
        "new_birth_date_search_executed": False,
        "accepted_reference_model": "astrohd-v14-v1.4d",
        "accepted_reference_recorded_instant_joint_first": True,
        "accepted_reference_tied_minute_count": 9,
        "accepted_reference_unique_maximum_date": "1985-01-29",
        "birth_date_found_by_new_v32_answers": "NOT_TESTABLE_NO_ADMITTED_BRIDGE",
        "owner_private_text_in_repo": False,
        "source_reuse_warning": "79/84-turn records overlap; guided responses are same-person development, not independent observations.",
    }
    return receipt, rows


def html_report(receipt: dict, rows: list) -> str:
    def esc(x):
        return html.escape(str(x or ""))

    parts = [
        "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
        "<title>Private Life Patterns V3.2 comparison</title><style>body{font:16px/1.55 system-ui,sans-serif;max-width:950px;margin:auto;padding:1rem 1rem 4rem;color:#213043}h1{font-size:1.75rem}details{padding:.8rem;border:1px solid #ccd7e3;border-radius:8px;margin:1rem 0}summary{font-weight:700;cursor:pointer}blockquote{padding:.3rem .9rem;border-left:3px solid #9bb}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f6f8;border-radius:6px;padding:.7rem}small{color:#56606f}table{border-collapse:collapse}th,td{border:1px solid #cbd3de;padding:.5rem}th{text-align:left}</style><main>",
        "<h1>Private V3.2 vs V3 vs earlier interview</h1>",
        "<p><strong>Development, N=1:</strong> same person, no independent birth-chart inference. Your preexisting V3 choices and three unusual behaviors were preserved exactly. Earlier 79-turn and 84-turn versions largely repeat the same material. The new eight guided context answers increase descriptive specificity, not necessarily between-person discrimination.</p>",
        "<p><strong>Accepted birth-date reference:</strong> AstroHD V1.4d, six equal-vote clauses, 52,596,001 minute-grid candidates: January 29, 1985 is the only maximum-scoring calendar day. Nine nearby minutes (10:18–10:26 UTC) tie for first, including the recorded 10:25 UTC. This six-rule signature was fitted to the known owner case; it is not independent DOB recovery. The older V4.3/NetInformation comparison is a different, discarded diagnostic and must not replace this benchmark. No new V3.2 reranking was performed. The existing V1.5 five-domain behavioral bridge and its unconfirmed role-entry interpretation remain separate.</p>",
        "<h2>Measured source continuity</h2><table><tr><th>Item</th><th>Count / state</th></tr>",
    ]
    for label, key in [
        ("Historical V3 questions", "v3_original_question_count"),
        ("Direct old-question source links", "historical_direct_mapped_routes"),
        ("Guided routes addressed", "v3_context_guided_routes_complete"),
        ("New conditional explanations", "guided_distinct_conditional_rules"),
        ("New real-case fields", "guided_distinct_recent_cases"),
        ("V3.2 revised prompts", "v32_revised_prompts"),
        ("Optional, scoring-suspended prompts", "v32_optional_scoring_suspended_prompts"),
        ("New scored chart features", "v32_newly_admitted_chart_features"),
    ]:
        parts.append("<tr><td>" + esc(label) + "</td><td>" + esc(receipt[key]) + "</td></tr>")
    parts.append("</table><h2>Eight redesigned routes and your saved context</h2>")
    for r in rows:
        if not r["guided_present"]:
            continue
        parts.append(
            "<details open><summary>"
            + esc(r["route"])
            + " — "
            + esc(r["revision_action"])
            + "</summary>"
        )
        parts.append(
            "<p><b>Earlier interview route:</b> "
            + esc(r["historical_route"])
            + "; original alignment: "
            + esc(r["original_crosswalk_class"])
            + "</p>"
        )
        parts.append("<p><b>Earlier comparison:</b> " + esc(r["old_comparison"]) + "</p>")
        parts.append("<p><b>V3 question:</b> " + esc(r["v3_question"]) + "</p>")
        parts.append("<p><b>V3 selected options:</b> " + esc(" | ".join(r["v3_choices"])) + "</p>")
        for label, key in [
            ("V3 own words", "v3_other"),
            ("New guided decision rule", "new_context_rule"),
            ("New guided real example", "new_recent_case"),
        ]:
            if r[key]:
                parts.append("<p><b>" + label + ":</b></p><pre>" + esc(r[key]) + "</pre>")
        parts.append("<p><b>Updated V3.2 prompt:</b> " + esc(r["revision_question"]) + "</p>")
        parts.append(
            "<p><b>Prospective observable:</b> " + esc(r["revision_comparison_target"]) + "</p>"
        )
        parts.append(
            "<p><small>V3.2 wording not separately administered here. No chart-scored polarity. Abstain if: "
            + esc(r["revision_abstain"])
            + "</small></p>"
        )
        parts.append("<details><summary>Previous historical source excerpts</summary>")
        for event in r["historical_sources"]:
            if isinstance(event, dict):
                for k, v in event.items():
                    if isinstance(v, (str, int)):
                        parts.append("<p><b>" + esc(k) + ":</b> " + esc(v) + "</p>")
        parts.append("</details></details>")
    parts.append(
        "<h2>All 25 original source mappings</h2><table><tr><th>V3 route</th><th>Prior class</th><th>V3.2 status</th></tr>"
    )
    for r in rows:
        parts.append(
            "<tr><td>"
            + esc(r["route"])
            + "</td><td>"
            + esc(r["original_crosswalk_class"])
            + "</td><td>"
            + esc(r["v32_current_status"])
            + "</td></tr>"
        )
    parts.append(
        "</table><p><small>There is no DOB in the question model. The recorded date is used solely as an answer key for historical evaluation. Do not share this private file.</small></p></main></html>"
    )
    return "\n".join(parts)


def markdown_report(receipt: dict, rows: list) -> str:
    out = [
        "# Private V3.2 / V3 / historical interview comparison",
        "",
        "**DEVELOPMENT, N=1, not a blind birth-chart test.** Original V3 source (25 questions, 3 unique behaviors) unchanged. The original 79/84 turns substantially overlap.",
        "",
        f"- Historical direct old route links: {receipt['historical_direct_mapped_routes']}/25.",
        f"- Guided routes answered: {receipt['v3_context_guided_routes_complete']}/8; condition fields: {receipt['guided_distinct_conditional_rules']}; real-case fields: {receipt['guided_distinct_recent_cases']}.",
        f"- Revised V3.2 candidates: {receipt['v32_revised_prompts']} (six core, two optional/retired for scoring).",
        "- All revised wording remains unadministered to the developer. Do not count old context as a new question response.",
        "",
        "## Birth-date result",
        "",
        "**Accepted reference:** AstroHD V1.4d's fixed six-rule century scan found the recorded 10:25 UTC instant **joint #1** among nine maximum-scoring minutes, all on January 29, 1985, within a 52,596,001-minute grid. It was fitted using the known development case and is not independent recovery. The older V4.3/NetInformation #1,562 diagnostic is **discarded as the comparison benchmark**, not retconned as the latest result. None of the eight new V3.2 prompts added a scored mapping or new rank. The existing V1.5 bridge can score confirmed five-domain responses, but the usual role-entry interpretation remains unresolved.",
        "",
        "## Eight revised question crosswalks",
        "",
    ]
    for r in rows:
        if not r["guided_present"]:
            continue
        out.extend(
            [
                f"### {r['route']} — {r['revision_action']}",
                f"Original old-route class: {r['original_crosswalk_class']} (historical {r['historical_route']}).",
                f"Old source comparison: {r['old_comparison']}",
                "",
                f"**Earlier V3 prompt:** {r['v3_question']}",
                "V3 selected examples: " + "; ".join(r["v3_choices"]),
                "**Decision rule (guided answer):**",
                "> "
                + (
                    r["new_context_rule"].replace("\n", "\n> ")
                    if r["new_context_rule"]
                    else "(none recorded)"
                ),
                "**Concrete example (guided answer):**",
                "> "
                + (
                    r["new_recent_case"].replace("\n", "\n> ")
                    if r["new_recent_case"]
                    else "(none recorded)"
                ),
                f"**V3.2 candidate:** {r['revision_question']}",
                f"**Proposed neutral comparison:** {r['revision_comparison_target']}",
                f"**No inference if:** {r['revision_abstain']}",
                "",
            ]
        )
    out.extend(["## Remaining 17 V3 items", ""])
    out.extend(
        f"- {r['route']}: {r['original_crosswalk_class']} (unchanged V3; historical {r['historical_route']})."
        for r in rows
        if not r["guided_present"]
    )
    return "\n".join(out) + "\n"


def run(args):
    prior, updated, cross = map(load, [args.prior, args.updated, args.crosswalk])
    bank, rev = load(BANK), load(REVISION)
    baseline = FROZEN_RESULT.read_text()
    receipt, rows = summarize(prior, updated, cross, bank, rev, baseline)
    output = args.output
    private_write(
        output / "Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.html", html_report(receipt, rows)
    )
    private_write(
        output / "Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.md", markdown_report(receipt, rows)
    )
    private_write(
        output / "Life-Patterns-V32-vs-V3-vs-Old-PRIVATE.json",
        json.dumps(
            {
                "schema": "life-patterns-v32-private-source-crosswalk-v1",
                "aggregate": receipt,
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
    )
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    downloads = Path.home() / "Téléchargements"
    cli.add_argument(
        "--prior", type=Path, default=downloads / "my-life-patterns-v3-local-pilot.json"
    )
    cli.add_argument(
        "--updated", type=Path, default=downloads / "my-life-patterns-v3-local-pilot (1).json"
    )
    cli.add_argument(
        "--crosswalk",
        type=Path,
        default=downloads
        / ".life-patterns-private-v3-v7-crosswalk-20261013/My-Life-Patterns-V3-vs-Historical-Survey.json",
    )
    cli.add_argument(
        "--output", type=Path, default=downloads / ".life-patterns-private-v32-20261015"
    )
    cli.add_argument("--receipt", type=Path, default=HERE / "AGGREGATE_SOURCE_RESULT.json")
    run(cli.parse_args())
