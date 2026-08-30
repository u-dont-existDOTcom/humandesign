from __future__ import annotations

import pytest

from tests.s6_h1_prehuman.acceptance import check_requirement, run_all_requirements


@pytest.mark.parametrize("requirement_id", [f"S6H1-{index:02d}" for index in range(1, 61)])
def test_s6_h1_prehuman_requirement(requirement_id: str) -> None:
    check_requirement(requirement_id)


def test_s6_h1_prehuman_exact_total() -> None:
    assert run_all_requirements() == [f"S6H1-{index:02d}" for index in range(1, 61)]
