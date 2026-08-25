from __future__ import annotations

import json
from pathlib import Path

from hdmatch.holistic_cli import main


def test_rich_humancase_cli_converts_and_crossfits_injected_signal(tmp_path: Path) -> None:
    cases = []
    for index in range(40):
        signal = "A" if index % 2 == 0 else "B"
        answer = "outgoing" if signal == "A" else "reserved"
        cases.append(
            {
                "participant_id": f"p-{index}",
                "cohort": "development",
                "responses": {"social.pattern": answer},
                "response_reliability": {"social.pattern": 1.0},
                "chart_features": {"signal": signal, "noise": str(index % 5)},
                "birth_year": 2000,
                "metadata": {"site": "synthetic"},
            }
        )
    dataset = tmp_path / "human.json"
    dataset.write_text(
        json.dumps(
            {
                "schema_version": "human-dataset-v1",
                "questionnaire_version": "synthetic-rich-v1",
                "cases": cases,
            }
        ),
        encoding="utf-8",
    )
    packet = tmp_path / "packet.json"
    evaluation = tmp_path / "crossfit.json"

    assert (
        main(
            [
                "convert-human-cases",
                "--dataset",
                str(dataset),
                "--questionnaire-version",
                "synthetic-rich-v1",
                "--output",
                str(packet),
                "--metadata-match-field",
                "site",
            ]
        )
        == 0
    )
    converted = json.loads(packet.read_text(encoding="utf-8"))
    assert len(converted["records"]) == 40
    assert len(converted["charts"]) == 40
    assert converted["skipped_no_scorable_evidence"] == []
    assert set(converted["label_opportunities"].values()) == {"social.pattern"}

    assert (
        main(
            [
                "crossfit-opportunity",
                "--packet",
                str(packet),
                "--output",
                str(evaluation),
                "--model-id",
                "synthetic-rich-crossfit",
                "--feature",
                "signal",
                "--match-field",
                "birth_year",
                "--match-field",
                "site",
                "--neighbor-count",
                "4",
                "--min-label-count",
                "3",
                "--min-opportunity-count",
                "4",
                "--folds",
                "4",
                "--max-decoys",
                "10",
                "--randomization-iterations",
                "100",
            ]
        )
        == 0
    )
    result = json.loads(evaluation.read_text(encoding="utf-8"))
    assert result["phase"] == "DEVELOPMENT"
    assert result["evaluation"]["people_evaluated"] == 40
    assert result["evaluation"]["mean_percentile"] > 0.70
