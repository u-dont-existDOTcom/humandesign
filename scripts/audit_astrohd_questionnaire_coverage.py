#!/usr/bin/env python3
"""Describe current AstroHD questionnaire coverage without inventing a target count."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from hdmatch.evaluation.theory_language_exposure import (
    LanguageSpecificity,
    load_theory_language_codebook,
)
from hdmatch.model.mapping_library import MappingStatus, load_mapping_library
from hdmatch.questionnaire.bank import load_question_bank

STATUS_ORDER = {
    MappingStatus.FROZEN: 0,
    MappingStatus.EMPIRICAL_ONLY: 1,
    MappingStatus.UNRESOLVED: 2,
}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--question-bank",
        type=Path,
        default=Path("reference/core/question_bank_v1.json"),
    )
    parser.add_argument(
        "--mapping-library",
        type=Path,
        default=Path("mappings/mapping_library_v1.json"),
    )
    parser.add_argument(
        "--language-codebook",
        type=Path,
        default=Path("reference/research/astrohd_theory_language_codebook_v0_1.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reference/research/astrohd_current_questionnaire_coverage_audit_v1.json"),
    )
    return parser.parse_args()


def build_report(
    question_bank_path: Path,
    mapping_library_path: Path,
    language_codebook_path: Path,
) -> dict[str, Any]:
    bank = load_question_bank(question_bank_path)
    library = load_mapping_library(mapping_library_path)
    library.validate_against_question_bank(bank)
    codebook, codebook_sha256 = load_theory_language_codebook(language_codebook_path)

    mappings_by_question = defaultdict(list)
    for mapping in library.mappings:
        for question_id in mapping.question_ids:
            mappings_by_question[question_id].append(mapping)

    questions: list[dict[str, Any]] = []
    phase_disposition_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for question in bank.questions:
        mappings = mappings_by_question[question.id]
        statuses = sorted({mapping.status for mapping in mappings}, key=STATUS_ORDER.__getitem__)
        if len(statuses) != 1:
            raise ValueError(f"question {question.id} has ambiguous mapping status: {statuses}")
        disposition = statuses[0]
        phase_disposition_counts[question.phase][disposition.value] += 1
        lexical_matches = _scan_text(
            " ".join((question.prompt, *question.followups)), codebook.entries
        )
        questions.append(
            {
                "question_id": question.id,
                "phase": question.phase,
                "domain": question.domain,
                "mapping_disposition": disposition.value,
                "mapping_ids": sorted(mapping.mapping_id for mapping in mappings),
                "behavioral_constructs": list(question.behavioral_constructs),
                "theory_language_prompt_scan": lexical_matches,
            }
        )

    disposition_counts = Counter(row["mapping_disposition"] for row in questions)
    frozen_directness = Counter(
        mapping.mapping_directness_class.value
        for mapping in library.frozen_mappings
        if mapping.mapping_directness_class is not None
    )
    frozen_structural_classes = Counter(
        mapping.structural_class.value
        for mapping in library.frozen_mappings
        if mapping.structural_class is not None
    )
    dependency_clusters: dict[str, list[Any]] = defaultdict(list)
    for mapping in library.frozen_mappings:
        dependency_clusters[mapping.dependency_cluster].append(mapping)
    repeated_clusters = [
        {
            "dependency_cluster": cluster,
            "mapping_count": len(mappings),
            "question_ids": sorted(
                {question_id for mapping in mappings for question_id in mapping.question_ids}
            ),
            "interpretation": (
                "multiple indicators of one dependency cluster; not independent confirmations"
            ),
        }
        for cluster, mappings in sorted(dependency_clusters.items())
        if len(mappings) > 1
    ]
    shared_question_mappings = [
        {
            "question_id": question_id,
            "frozen_mapping_ids": sorted(mapping.mapping_id for mapping in mappings),
            "interpretation": (
                "one response contributes to multiple frozen rules; do not count it as "
                "independent evidence"
            ),
        }
        for question_id, mappings in sorted(mappings_by_question.items())
        if sum(mapping.status is MappingStatus.FROZEN for mapping in mappings) > 1
    ]
    multi_question_rules = [
        {
            "mapping_id": mapping.mapping_id,
            "status": mapping.status.value,
            "question_ids": list(mapping.question_ids),
            "interpretation": (
                "repeated probes of one mapped statement; not independent confirmations"
            ),
        }
        for mapping in library.mappings
        if len(mapping.question_ids) > 1
    ]
    prompt_scan_counts = Counter(
        match["specificity"] for row in questions for match in row["theory_language_prompt_scan"]
    )

    nonvalidation_count = sum(question.phase != "validation" for question in bank.questions)
    report: dict[str, Any] = {
        "schema_version": "astrohd-current-questionnaire-coverage-audit-v1",
        "audit_date": "2026-09-02",
        "status": "descriptive_draft_no_expansion_authorized",
        "scope": {
            "question": (
                "Should future validation use more questions than the present questionnaire?"
            ),
            "answer": (
                "Not established by item count. Evaluate current construct and rule coverage "
                "before authoring additions."
            ),
            "questionnaire_expansion_authorized": False,
            "required_additional_question_count": None,
            "numeric_target_prohibited": True,
        },
        "source_receipt": {
            "question_bank_path": _display_path(question_bank_path),
            "question_bank_version": bank.version,
            "question_bank_file_sha256": _sha256_file(question_bank_path),
            "mapping_library_path": _display_path(mapping_library_path),
            "mapping_library_version": library.model_version,
            "mapping_library_file_sha256": _sha256_file(mapping_library_path),
            "language_codebook_path": _display_path(language_codebook_path),
            "language_codebook_sha256": codebook_sha256,
        },
        "counts": {
            "question_bank_total": len(bank.questions),
            "nonvalidation_question_records": nonvalidation_count,
            "validation_question_records": len(bank.questions) - nonvalidation_count,
            "mapping_rules_total": len(library.mappings),
            "frozen_mapping_rules": len(library.frozen_mappings),
            "unique_frozen_question_records": disposition_counts[MappingStatus.FROZEN.value],
            "unique_empirical_only_question_records": disposition_counts[
                MappingStatus.EMPIRICAL_ONLY.value
            ],
            "unique_unresolved_question_records": disposition_counts[
                MappingStatus.UNRESOLVED.value
            ],
        },
        "coverage_interpretation": [
            "The bank already contains more records than the currently frozen scoreable subset.",
            (
                "The 76 non-validation records and 23 frozen-mapped records are "
                "descriptive facts, not completion policies or target sample sizes."
            ),
            (
                "Unresolved and empirical-only records must not be silently promoted into "
                "confirmatory scoring."
            ),
            (
                "Before adding items, examine whether existing non-frozen records cover the "
                "prospective construct gap with acceptable response process and burden."
            ),
            (
                "Any candidate addition and its mapping, scoring rule, and analysis lane must "
                "be frozen before participant answers are inspected."
            ),
        ],
        "phase_by_disposition": {
            phase: {
                status: counts.get(status, 0)
                for status in (
                    MappingStatus.FROZEN.value,
                    MappingStatus.EMPIRICAL_ONLY.value,
                    MappingStatus.UNRESOLVED.value,
                )
            }
            for phase, counts in sorted(phase_disposition_counts.items())
        },
        "frozen_rule_characteristics": {
            "mapping_directness_counts": dict(sorted(frozen_directness.items())),
            "structural_class_counts": dict(sorted(frozen_structural_classes.items())),
            "repeated_dependency_clusters": repeated_clusters,
            "questions_shared_by_multiple_frozen_rules": shared_question_mappings,
            "rules_using_multiple_question_records": multi_question_rules,
        },
        "prompt_language_scan": {
            "purpose": (
                "detect codebook wording already introduced by the questionnaire; lexical "
                "observation only"
            ),
            "specificity_counts": dict(sorted(prompt_scan_counts.items())),
            "theory_specific_occurrence_requires_prompt_echo_handling": any(
                match["specificity"] == LanguageSpecificity.THEORY_SPECIFIC.value
                for row in questions
                for match in row["theory_language_prompt_scan"]
            ),
            "not_a_measure_of_participant_exposure": True,
        },
        "questions": questions,
    }
    return report


def _scan_text(text: str, entries: tuple[Any, ...]) -> list[dict[str, str]]:
    normalized = " ".join(text.casefold().split())
    matches: list[dict[str, str]] = []
    for entry in entries:
        for expression in entry.expressions:
            escaped = re.escape(" ".join(expression.casefold().split())).replace(r"\ ", r"\s+")
            if re.search(rf"(?<!\w){escaped}(?!\w)", normalized):
                matches.append(
                    {
                        "entry_id": entry.entry_id,
                        "expression": expression,
                        "specificity": entry.specificity.value,
                    }
                )
                break
    return matches


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def main() -> None:
    args = parse_args()
    report = build_report(args.question_bank, args.mapping_library, args.language_codebook)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
