"""Synthetic-only regression for participant-private historical-to-V3 source crosswalk."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / "tasks/v3-v7-evidence-crosswalk-20261013"
SRC = FOLDER / "build_private_crosswalk.py"

spec = spec_from_file_location("private_source_crosswalk", SRC)
assert spec and spec.loader
mod = module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def fixtures():
    bank = json.loads(
        (
            ROOT
            / "tasks/life-patterns-idiographic-20261010/tendency-first-v3-scaffold-development.json"
        ).read_text()
    )
    old = []
    for i, question in enumerate(bank["questions"]):
        if question["id"] == "TF1-PREFER-EXCHANGE":
            continue
        old.append(
            {
                "turn_id": f"synthetic-old-{i}",
                "canonical_question_id": question["source_route_id"],
                "historical_question_id": question["source_route_id"],
                "question_text": f"synthetic question {i}",
                "answer_text": f"PRIVATE_SOURCE_DO_NOT_PUBLISH_{i}",
            }
        )
    while len(old) < 79:
        i = len(old)
        old.append(
            {
                "turn_id": f"synthetic-extra-{i}",
                "canonical_question_id": f"UNRELATED-{i}",
                "question_text": f"unrelated question {i}",
                "answer_text": f"PRIVATE_SOURCE_DO_NOT_PUBLISH_{i}",
            }
        )
    frozen = (
        deepcopy(old)
        + [
            {
                "canonical_question_id": "TF1-G17",
                "question_text": "clarifying",
                "answer_text": "PRIVATE_SOURCE_DO_NOT_PUBLISH_recent",
            }
        ]
        * 5
    )
    survey = {
        "schema": "local_life_patterns_v3_pilot_unsubmitted",
        "answers": {
            q["id"]: {
                "selected": [q["example_answer_paths"][0]],
                "other": "PRIVATE_RESPONSE_DO_NOT_PUBLISH",
                "unsure": False,
                "skip": False,
            }
            for q in bank["questions"]
        },
        "unique_behaviors": [{"behavior": "PRIVATE_UNIQUE_BEHAVIOR_DO_NOT_PUBLISH"}],
    }
    return {"turns": old}, {"turns": frozen}, survey, bank


def test_synthetic_source_crosswalk_counts_and_never_leaks_private_text():
    primary, frozen, survey, bank = fixtures()
    private, public = mod.build(primary, frozen, survey, bank)
    assert public["old_79_count"] == 79
    assert public["frozen_84_count"] == 84
    assert public["v3_question_count"] == 25
    assert public["direct_old_route_mappings"] == 24
    assert public["without_direct_old_route"] == ["TF1-PREFER-EXCHANGE"]
    assert len(public["route_evidence_category"]) == 25
    assert sum(public["scope_category_counts"].values()) == 25
    assert public["old_new_same_person_not_independent"] is True
    public_text = json.dumps(public)
    for prohibited in [
        "PRIVATE_SOURCE_DO_NOT_PUBLISH",
        "PRIVATE_RESPONSE_DO_NOT_PUBLISH",
        "PRIVATE_UNIQUE_BEHAVIOR_DO_NOT_PUBLISH",
    ]:
        assert prohibited not in public_text
    assert "PRIVATE_RESPONSE_DO_NOT_PUBLISH" in mod.markdown(private)
    assert "selected_option_count" not in json.dumps(public)
    assert "has_additional_free_text" not in json.dumps(public)
    assert "PRIVATE_SOURCE_DO_NOT_PUBLISH" in mod.html_report(private)
    assert "Six independent-review findings" in mod.markdown(private)


def test_malformed_options_rejected_without_guessing():
    primary, frozen, survey, bank = fixtures()
    survey["answers"]["TF1-G05"]["selected"] = ["fabricated choice"]
    with pytest.raises(ValueError, match="Unknown selected example"):
        mod.build(primary, frozen, survey, bank)
    survey["answers"]["TF1-G05"]["selected"] = [bank["questions"][3]["example_answer_paths"][0]]
    survey["answers"].pop("TF1-G05")
    with pytest.raises(ValueError, match="don't match"):
        mod.build(primary, frozen, survey, bank)


def test_private_renderer_does_not_interpret_untrusted_text(tmp_path):
    primary, frozen, survey, bank = fixtures()
    survey["answers"]["TF1-A0"]["other"] = '<script>alert("private")</script>'
    private, _ = mod.build(primary, frozen, survey, bank)
    page = mod.html_report(private)
    assert "&lt;script&gt;" in page
    assert '<script>alert("private")</script>' not in page
    dest = tmp_path / "a.html"
    mod.safe_write(dest, page)
    assert dest.stat().st_mode & 0o777 == 0o600
    assert "source warning" not in json.dumps(private["aggregate"]).lower()


def test_old_independent_reviewer_facets_not_misrepresented_as_retests():
    data = json.loads((FOLDER / "INDEPENDENT-REVIEW-FACET-CROSSWALK.json").read_text())
    assert len(data["items"]) == 6
    assert data["summary"] == {
        "historical_admitted_items": 6,
        "partial_related": 4,
        "different_target": 2,
        "exact_behavioral_retests": 0,
        "independent_birth_prediction_replications": 0,
    }
    joint = next(row for row in data["items"] if "D19.status_ownership" in row["old_facet_ids"])
    assert joint["v3_route_ids"] == ["TF1-STATUS"]
    assert joint["excluded_old_route"] == "OWNERSHIP"
    g05 = next(row for row in data["items"] if "TF1-G05" in row["v3_route_ids"])
    assert g05["alignment"] == "different_target"
    assert "outcomes" in g05["reason"]


def test_private_delivery_preserves_source_and_links_without_duplicate(tmp_path):
    import importlib.util

    p = FOLDER / "deliver_private_crosswalk.py"
    spec = importlib.util.spec_from_file_location("deliver_priv", p)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    source = tmp_path / "private"
    source.mkdir()
    for ext in ("html", "md"):
        (source / ("My-Life-Patterns-V3-vs-Historical-Survey." + ext)).write_text(
            "PRIVATE_DATA_DO_NOT_PUBLISH"
        )
    guide = tmp_path / "Life-Patterns-Researcher-Guide.html"
    guide.write_text("<html><body><h1>Existing</h1></body></html>")
    first = mod.install(source, tmp_path)
    second = mod.install(source, tmp_path)
    assert first["report_installed"] and first["guide_modified"]
    assert second["report_installed"] and not second["guide_modified"]
    assert guide.read_text().count("Life-Patterns-New-vs-Old-Answers-2026-10-13.html") == 1
    for ext in ("html", "md"):
        target = tmp_path / ("Life-Patterns-New-vs-Old-Answers-2026-10-13." + ext)
        assert target.read_text() == "PRIVATE_DATA_DO_NOT_PUBLISH"
        assert target.stat().st_mode & 0o777 == 0o600
