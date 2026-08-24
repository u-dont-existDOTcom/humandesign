from __future__ import annotations

import json
from pathlib import Path

from hdmatch.holistic_cli import main


def _write(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _fixtures(tmp_path: Path) -> tuple[Path, Path]:
    records = []
    charts = []
    for index in range(24):
        signal = "A" if index % 2 == 0 else "B"
        label = "L" if signal == "A" else "M"
        participant_id = f"p-{index}"
        features = {"signal": signal, "noise": "same"}
        records.append(
            {
                "participant_id": participant_id,
                "cohort": "development",
                "observed_labels": [label],
                "chart_features": features,
                "match_strata": {"sex": "x"},
            }
        )
        charts.append(
            {
                "chart_id": f"chart-{index}",
                "owner_participant_id": participant_id,
                "chart_features": features,
                "match_strata": {"sex": "x"},
            }
        )
    return _write(tmp_path / "records.json", records), _write(
        tmp_path / "charts.json", charts
    )


def test_holistic_cli_fit_and_evaluate(tmp_path: Path) -> None:
    records, charts = _fixtures(tmp_path)
    model = tmp_path / "model.json"
    evaluation = tmp_path / "evaluation.json"

    assert (
        main(
            [
                "fit",
                "--records",
                str(records),
                "--output",
                str(model),
                "--model-id",
                "cli-test",
                "--feature",
                "signal",
                "--feature",
                "noise",
                "--cluster",
                "signal=signal",
                "--cluster",
                "noise=noise",
                "--min-label-count",
                "5",
            ]
        )
        == 0
    )
    assert model.exists()

    assert (
        main(
            [
                "evaluate",
                "--model",
                str(model),
                "--people",
                str(records),
                "--charts",
                str(charts),
                "--output",
                str(evaluation),
                "--match-field",
                "sex",
                "--max-decoys",
                "10",
                "--seed",
                "7",
                "--randomization-iterations",
                "100",
            ]
        )
        == 0
    )
    payload = json.loads(evaluation.read_text(encoding="utf-8"))
    assert payload["people_evaluated"] == 24
    assert payload["mean_percentile"] > 0.70


def test_holistic_cli_minimize_removes_noise(tmp_path: Path) -> None:
    records, charts = _fixtures(tmp_path)
    model = tmp_path / "model.json"
    groups = _write(
        tmp_path / "groups.json",
        {"signal": ["signal"], "noise": ["noise"]},
    )
    minimized = tmp_path / "minimized.json"

    assert (
        main(
            [
                "fit",
                "--records",
                str(records),
                "--output",
                str(model),
                "--model-id",
                "cli-minimize-test",
                "--feature",
                "signal",
                "--feature",
                "noise",
                "--min-label-count",
                "5",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "minimize",
                "--model",
                str(model),
                "--people",
                str(records),
                "--charts",
                str(charts),
                "--feature-groups",
                str(groups),
                "--output",
                str(minimized),
                "--match-field",
                "sex",
                "--max-decoys",
                "10",
                "--seed",
                "9",
                "--max-percentile-loss",
                "0.001",
            ]
        )
        == 0
    )
    payload = json.loads(minimized.read_text(encoding="utf-8"))
    assert payload["retained_groups"] == ["signal"]
