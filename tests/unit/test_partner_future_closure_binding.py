"""Regression coverage for the loop-local astronomy residual closures."""

from __future__ import annotations

import ast
from pathlib import Path

SCRIPT = Path(__file__).parents[2] / "scripts" / "partner_future_pilot.py"


def _residual_closures() -> list[ast.FunctionDef]:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "f"
        and [argument.arg for argument in node.args.args]
        == [
            "t",
            *(
                ["mp_id", "target_lon", "asp"]
                if node.lineno < 200
                else ["pp_id", "target_lon", "asp"]
            ),
        ]
    ]


def test_loop_local_residuals_bind_each_iteration_value_as_a_default() -> None:
    closures = sorted(_residual_closures(), key=lambda node: node.lineno)
    assert len(closures) == 2
    for closure in closures:
        bound_names = [argument.arg for argument in closure.args.args[1:]]
        assert len(closure.args.defaults) == 3
        assert all(isinstance(default, ast.Name) for default in closure.args.defaults)
        assert [default.id for default in closure.args.defaults] == bound_names


def test_representative_bound_residuals_are_deterministic() -> None:
    def make_residual(moving_id: int, target_lon: float, aspect: int):
        return lambda moment, moving_id=moving_id, target_lon=target_lon, aspect=aspect: (
            moment + moving_id - target_lon - aspect
        )

    residuals = [
        make_residual(moving_id, target_lon, aspect)
        for moving_id, target_lon, aspect in [(1, 10.0, 0), (2, 20.0, 60), (3, 30.0, 120)]
    ]
    assert [residual(5.0) for residual in residuals] == [-4.0, -73.0, -142.0]
    assert [residual(5.0) for residual in residuals] == [-4.0, -73.0, -142.0]
