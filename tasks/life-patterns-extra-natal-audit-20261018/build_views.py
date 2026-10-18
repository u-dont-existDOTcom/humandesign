"""Generate owner-reviewable optional questions and historical-source crosswalk.

Outputs contain cited historical translated topic paraphrases, not full
copyrighted source text, participant information or scoring/predictions.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
PREVIOUS = ROOT / "tasks/life-patterns-source-first-audit-20261018"


def load(name: str) -> dict:
    data = json.loads((TASK / name).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def save_csv(filename: str, data: list[dict], fields: list[str]) -> None:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(data)
    (TASK / filename).write_text(buffer.getvalue(), encoding="utf-8")


def build() -> dict:
    ext = load("EXPANDED-DOMAIN-AND-QUESTION-COVERAGE-v2.json")
    sources = load("SOURCE-ANCHORS-v2.json")
    questions = load("SEVEN-NEW-TOPICS-v2.json")
    prior_domains = json.loads(
        (PREVIOUS / "SOURCE-TO-SURVEY-CROSSWALK-v2.json").read_text(encoding="utf-8")
    )["domains"]
    source_by_id = {source["id"]: source for source in sources["new_sources"]}
    anchors_by_id = {a["id"]: a for a in sources["source_anchors"]}
    assert len(source_by_id) == 9
    assert len(anchors_by_id) == 28
    assert len(prior_domains) == 46
    rows = []
    for prev in prior_domains:
        rows.append(
            {
                "domain_id": prev["domain_id"],
                "human_domain": prev["label"],
                "domain_status": "accepted_prior_46_domain_registry",
                "v7_coverage": prev["v7_questionnaire_coverage"],
                "tf1_coverage": prev["tf1_questionnaire_coverage"],
                "em_v2_coverage": ("direct" if prev["em_v2_direct_question_ids"] else "absent"),
                "optional_16_question_ids": ",".join(prev["optional_future_question_ids"]),
                "new_question_id": "",
                "new_source_claim_ids": "",
                "interpretation_limit": prev["interpretation_limit"],
            }
        )
    for new in ext["new_domains"]:
        rows.append(
            {
                "domain_id": new["domain_id"],
                "human_domain": new["human_outcome"],
                "domain_status": "new_second_pass_candidate",
                "v7_coverage": new["v7_status"],
                "tf1_coverage": new["tf1_status"],
                "em_v2_coverage": new["em_v2"],
                "optional_16_question_ids": ",".join(new["existing_16_question_neighbor_ids"]),
                "new_question_id": new["suggested_optional_new_topic_id"],
                "new_source_claim_ids": ",".join(new["source_claim_ids"]),
                "interpretation_limit": (
                    "Translated traditional description, not a validated natal predictor; "
                    "use as optional developmental measurement only."
                ),
            }
        )
    assert len(rows) == 53
    save_csv(
        "FIFTY-THREE-DOMAIN-CROSSWALK.csv",
        rows,
        [
            "domain_id",
            "human_domain",
            "domain_status",
            "v7_coverage",
            "tf1_coverage",
            "em_v2_coverage",
            "optional_16_question_ids",
            "new_question_id",
            "new_source_claim_ids",
            "interpretation_limit",
        ],
    )
    save_csv(
        "TWENTY-EIGHT-NEW-SOURCE-ANCHORS.csv",
        [
            {
                "anchor_id": a["id"],
                "source_witness": a["witness_id"],
                "source_url": source_by_id[a["witness_id"]]["url"],
                "source_text_location": a["locator"],
                "short_verified_source_fragment": a["proof_fragment"],
                "source_claim_paraphrase": a["claim_paraphrase"],
                "current_or_new_domain": a["normalized_domain"],
                "survey_design_disposition": a["disposition"],
                "evidence_limit": a["caution"],
                "predictive_validation": False,
            }
            for a in sources["source_anchors"]
        ],
        [
            "anchor_id",
            "source_witness",
            "source_url",
            "source_text_location",
            "short_verified_source_fragment",
            "source_claim_paraphrase",
            "current_or_new_domain",
            "survey_design_disposition",
            "evidence_limit",
            "predictive_validation",
        ],
    )
    order = sorted(questions["candidates"], key=lambda q: q["priority"])
    lines = [
        "# Seven more optional Life Patterns question candidates",
        "",
        "These are **research-only proposals**, not questions already installed in the",
        "existing GPT or Railway completion. Do not ask all seven automatically.",
        "Select a topic only when important and not already answered adequately.",
        "Allow the respondent to decline or stop without scoring the refusal.",
        "",
    ]
    for q in order:
        lines.extend(
            [
                f"## {q['id']} — {q['domain'].replace('_', ' ').title()}",
                "",
                f"**Priority:** {q['priority']} (1 is most useful for the initial pilot).",
                "",
                f"**Ask:** {q['question']}",
                "",
                f"**Optional follow-up:** {q['followup']}",
                "",
                "**Record separately:** " + ", ".join(q["dimensions"]) + ".",
                "",
                "**Why this is different from earlier questions:** " + q["newness"],
                "",
                "**Privacy/interpretation rule:** " + q["caution"],
                "",
                "Historical translated source IDs: " + ", ".join(q["source_claim_ids"]),
                "",
            ]
        )
    text = "\n".join(lines).rstrip() + "\n"
    (TASK / "SEVEN-ADDITIONAL-OPTIONAL-QUESTIONS.md").write_text(text, encoding="utf-8")
    earlier = json.loads(
        (PREVIOUS / "ADAPTIVE-QUESTION-CANDIDATES-v1.json").read_text(encoding="utf-8")
    )
    normalized_questions = []
    for q in earlier["questions"]:
        normalized_questions.append(
            {
                "id": q["id"],
                "label": q["label"],
                "source_version": "2026-10-18-existing-sixteen",
                "priority": q["priority"],
                "question": q["question"],
                "optional_followup": q["optional_followup"],
                "answer_dimensions": q["answer_dimensions"],
                "time_window": q["recall_window"],
                "privacy_and_source_caution": q["interpretation_limit"],
                "source_domains": q["source_domains"],
                "already_live": False,
            }
        )
    for q in order:
        normalized_questions.append(
            {
                "id": q["id"],
                "label": q["domain"].replace("_", " ").title(),
                "source_version": "2026-10-18-second-pass-seven",
                "priority": q["priority"],
                "question": q["question"],
                "optional_followup": q["followup"],
                "answer_dimensions": q["dimensions"],
                "time_window": "source_specific_optional_timeline",
                "privacy_and_source_caution": q["caution"],
                "source_domains": [q["domain"]],
                "source_claim_ids": q["source_claim_ids"],
                "already_live": False,
            }
        )
    assert len(normalized_questions) == 23
    assert len({q["id"] for q in normalized_questions}) == 23
    combined = {
        "schema": "life-patterns-cross-tradition-23-optional-question-candidates-v2",
        "status": "EXPERIMENTAL_NOT_LIVE_NOT_SCORED",
        "version_date": "2026-10-18",
        "instrument_policy": (
            "Topic selection first; previously answered equivalents bypassed; "
            "never ask all 23; explicit refusal or skip; no more than five "
            "participant-selected optional topics in one sitting."
        ),
        "source_record_versions": [
            "ADAPTIVE-QUESTION-CANDIDATES-v1.json (unchanged existing 16)",
            "SEVEN-NEW-TOPICS-v2.json (additional seven)",
        ],
        "questions": normalized_questions,
    }
    (TASK / "TWENTY-THREE-OPTIONAL-QUESTIONS-v2.json").write_text(
        json.dumps(combined, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    combined_lines = [
        "# All 23 optional Life Patterns question candidates",
        "",
        "No candidate here is live, chart-scored or compulsory. Offer *topics* first,",
        "check the participant's prior answers and ask at most five relevant",
        "participant-selected optional topics in one sitting. Refusal is complete.",
        "",
    ]
    for idx, q in enumerate(normalized_questions):
        if idx in (0, 16):
            combined_lines.extend(
                [
                    "## Previous 16 source-first candidates"
                    if idx == 0
                    else "## Seven additional cross-tradition candidates",
                    "",
                ]
            )
        combined_lines.extend(
            [
                "### " + q["id"] + " — " + q["label"],
                "",
                "**Ask:** " + q["question"],
                "",
                "**Follow-up, only if helpful:** " + q["optional_followup"],
                "",
                "**Separate answer dimensions:** " + ", ".join(q["answer_dimensions"]),
                "",
                "**Interpretation and privacy boundary:** " + q["privacy_and_source_caution"],
                "",
            ]
        )
    (TASK / "TWENTY-THREE-OPTIONAL-QUESTIONS.md").write_text(
        "\n".join(combined_lines).rstrip() + "\n", encoding="utf-8"
    )
    generated = [
        "FIFTY-THREE-DOMAIN-CROSSWALK.csv",
        "TWENTY-EIGHT-NEW-SOURCE-ANCHORS.csv",
        "SEVEN-ADDITIONAL-OPTIONAL-QUESTIONS.md",
        "TWENTY-THREE-OPTIONAL-QUESTIONS-v2.json",
        "TWENTY-THREE-OPTIONAL-QUESTIONS.md",
    ]
    return {
        "domain_csv_rows": len(rows),
        "claim_csv_rows": len(anchors_by_id),
        "optional_question_entries": len(order),
        "output_hashes": {
            p: hashlib.sha256((TASK / p).read_bytes()).hexdigest() for p in generated
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
