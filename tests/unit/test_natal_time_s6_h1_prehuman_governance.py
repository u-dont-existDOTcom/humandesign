from __future__ import annotations

import pytest

from tests.s6_h1_prehuman.acceptance import (
    check_requirement,
    hostile_case_ids,
    run_all_requirements,
    run_hostile_case,
)


@pytest.mark.parametrize("requirement_id", [f"S6H1-{index:02d}" for index in range(1, 61)])
def test_s6_h1_prehuman_requirement(requirement_id: str) -> None:
    check_requirement(requirement_id)


def test_s6_h1_prehuman_exact_total() -> None:
    assert run_all_requirements() == [f"S6H1-{index:02d}" for index in range(1, 61)]


@pytest.mark.parametrize("case_id", hostile_case_ids())
def test_s6_h1_epoch5_hostile_policy_case(case_id: str) -> None:
    run_hostile_case(case_id)


def test_s6_h1_epoch5_hostile_policy_exact_total() -> None:
    assert len(hostile_case_ids()) == 28
