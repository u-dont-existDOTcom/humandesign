import json
from pathlib import Path


QUESTIONNAIRE_PATH = Path("reference/relationship/relationship_dynamic_questionnaire_v1.json")
RUBRIC_PATH = Path("reference/relationship/relationship_outcome_rubrics_v1.json")


def test_every_question_target_axis_exists_in_frozen_rubric() -> None:
    questionnaire = json.loads(QUESTIONNAIRE_PATH.read_text(encoding="utf-8"))
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))
    axis_ids = {axis["id"] for axis in rubric["axes"]}
    used_axes = {
        axis_id
        for question in questionnaire["questions"]
        for axis_id in question["target_axes"]
    }
    assert used_axes <= axis_ids


def test_rubric_axis_ids_are_unique() -> None:
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))
    axis_ids = [axis["id"] for axis in rubric["axes"]]
    assert len(axis_ids) == len(set(axis_ids))
