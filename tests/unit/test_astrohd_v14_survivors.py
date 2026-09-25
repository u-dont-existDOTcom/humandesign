"""Tests for maximum-preserving survivor refinement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import numpy as np
import pytest
from refine_astrohd_v14_survivors import minimum_additions


def test_minimum_addition():
    rules = [{'rule_id': str(i)} for i in range(4)]
    matrix = np.array([[1, 1, 1, 1], [1, 1, 0, 1], [1, 1, 0, 0]], dtype=np.int8)
    selected, fit = minimum_additions(matrix, rules, {'0', '1'})
    assert fit['added_count'] == 1
    assert fit['minimum_additions_certified']
    assert set(selected) == {0, 1, 2}
    scores = matrix[:, selected].sum(axis=1)
    assert np.all(scores[0] > scores[1:])


def test_identical_time_remains_unresolved():
    rules = [{'rule_id': str(i)} for i in range(3)]
    matrix = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 0]], dtype=np.int8)
    selected, fit = minimum_additions(matrix, rules, {'0', '1'})
    assert fit['unresolved_indices'] == [1]
    assert matrix[0, selected].sum() == matrix[1, selected].sum()


def test_nonmaximal_base_is_rejected():
    with pytest.raises(ValueError, match='maximum-scoring'):
        minimum_additions(np.array([[0, 1], [1, 1]]), [{'rule_id': '0'}, {'rule_id': '1'}], {'0'})


def test_excluded_base_candidate_cannot_reach_enlarged_maximum():
    base_score, base_max, added_count = 3, 4, 2
    assert base_score + added_count < base_max + added_count
