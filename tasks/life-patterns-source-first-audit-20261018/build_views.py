"""Reproducible human-review views of source-first astrology/survey audit.

No participant files are loaded. Views are research audit artifacts, not a
proposal to add mandatory questions or map responses to prediction scores.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path

TASK = Path(__file__).resolve().parent


def read(filename: str) -> dict:
    return json.loads((TASK / filename).read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(text.getvalue(), encoding="utf-8")


def build() -> dict:
    audit = read("SOURCE-TO-SURVEY-CROSSWALK-v2.json")
    cf003 = read("CF003-PLANET-MAPPING-GAPS-v1.json")
    qbank = read("ADAPTIVE-QUESTION-CANDIDATES-v1.json")
    domains = [
        {
            "domain_id": row["domain_id"],
            "human_domain": row["label"],
            "source_attested_in_checked_corpus": row["historically_attested_in_this_snapshot"],
            "v7_status": row["v7_questionnaire_coverage"],
            "tf1_status": row["tf1_questionnaire_coverage"],
            "em_v2_direct_ids": ",".join(row["em_v2_direct_question_ids"]),
            "proposed_optional_question_ids": ",".join(row["optional_future_question_ids"]),
            "historical_claim_count": len(row["historical_source_claim_ids"]),
            "historical_claim_ids": ",".join(row["historical_source_claim_ids"]),
            "nearest_existing_questions_do_not_imply_equivalence": ",".join(
                row["related_existing_questions_not_necessarily_direct"]
            ),
            "interpretation_limit": row["interpretation_limit"],
        }
        for row in audit["domains"]
    ]
    write_csv(
        TASK / "DOMAIN-COVERAGE-REVIEW.csv",
        domains,
        [
            "domain_id",
            "human_domain",
            "source_attested_in_checked_corpus",
            "v7_status",
            "tf1_status",
            "em_v2_direct_ids",
            "proposed_optional_question_ids",
            "historical_claim_count",
            "historical_claim_ids",
            "nearest_existing_questions_do_not_imply_equivalence",
            "interpretation_limit",
        ],
    )
    write_csv(
        TASK / "CF003-PLANET-MAPPING-REVIEW.csv",
        [
            {
                "planet": item["planet"],
                "construct_id": item["construct_id"],
                "existing_mapping_role": item["existing_mapping_role"],
                "development_contract": item["actual_development_contract"],
                "classical_source_relationship": item["relationship_to_checked_classical_sources"],
                "anchor_claim_ids": ",".join(item["historical_claim_ids"]),
                "source_fidelity_limitation": item["limitation"],
                "classical_rule_admitted": item[
                    "translation_into_computational_natal_rule_admitted"
                ],
            }
            for item in cf003["rows"]
        ],
        [
            "planet",
            "construct_id",
            "existing_mapping_role",
            "development_contract",
            "classical_source_relationship",
            "anchor_claim_ids",
            "source_fidelity_limitation",
            "classical_rule_admitted",
        ],
    )
    write_csv(
        TASK / "HISTORICAL-SOURCE-CLAIMS.csv",
        [
            {
                "claim_id": item["claim_id"],
                "domain_id": item["domain_id"],
                "source_type": item["source_type"],
                "evidence_level": item["evidence_level"],
                "source_locator": item["source_locator"],
                "chart_condition": item["source_condition"] or "",
                "traditional_claim": item["historical_subject_paraphrase"],
                "source_limitation": item["source_caution"],
                "validated_prediction": False,
            }
            for item in audit["historical_source_claims"]
        ],
        [
            "claim_id",
            "domain_id",
            "source_type",
            "evidence_level",
            "source_locator",
            "chart_condition",
            "traditional_claim",
            "source_limitation",
            "validated_prediction",
        ],
    )
    lines = [
        "# Sixteen optional Life Patterns question candidates",
        "",
        "**2026-10-18.** Research candidates only; these are NOT in the currently",
        "deployed survey and have no natal predictor or scoring rule.",
        "",
        "Ask no additional question merely to reach a quota. Check whether the",
        "person already answered each area, let them select topics, allow full",
        "decline, and normally limit to at most five optional topics per session.",
        "",
    ]
    for item in qbank["questions"]:
        lines.extend(
            [
                f"## {item['id']} — {item['label']}",
                "",
                f"**Priority:** {item['priority']}. "
                f"**Type:** {item['mode']}. "
                f"**Time frame:** {item['recall_window']}. "
                f"**Privacy:** {item['sensitivity']}.",
                "",
                f"**Ask:** {item['question']}",
                "",
                f"**Optional follow-up:** {item['optional_followup']}",
                "",
                f"**Measure separately:** {', '.join(item['answer_dimensions'])}.",
                "",
                f"**Avoid interpreting as:** {item['interpretation_limit']}",
                "",
            ]
        )
        if item.get("source_note"):
            lines.extend([f"**Source note:** {item['source_note']}", ""])
    (TASK / "SIXTEEN-OPTIONAL-QUESTIONS.md").write_text(
        "\n".join(lines).rstrip() + "\n", encoding="utf-8"
    )
    files = [
        "DOMAIN-COVERAGE-REVIEW.csv",
        "CF003-PLANET-MAPPING-REVIEW.csv",
        "HISTORICAL-SOURCE-CLAIMS.csv",
        "SIXTEEN-OPTIONAL-QUESTIONS.md",
    ]
    return {
        "domain_rows": len(domains),
        "source_claim_rows": len(audit["historical_source_claims"]),
        "planet_map_rows": len(cf003["rows"]),
        "new_question_candidates": len(qbank["questions"]),
        "generated_hashes": {
            file: hashlib.sha256((TASK / file).read_bytes()).hexdigest() for file in files
        },
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
