from hdmatch.human.baselines import permute_chart_assignments
from hdmatch.human.dataset import HumanCase, HumanDataset
from hdmatch.human.empirical import EmpiricalChartResponseModel
from hdmatch.human.splits import create_person_splits


def _case(identifier: str, cohort: str, answer: str, chart_type: str) -> HumanCase:
    return HumanCase(
        participant_id=identifier,
        cohort=cohort,
        responses={"Q1": answer},
        chart_features={"type": chart_type},
    )


def test_person_splits_are_disjoint_and_deterministic() -> None:
    dataset = HumanDataset(
        questionnaire_version="Q1",
        cases=tuple(_case(str(i), "unassigned", "a", "X") for i in range(10)),
    )
    first = create_person_splits(dataset, 42)
    second = create_person_splits(dataset, 42)
    assert first == second
    assert not set(first.development_ids) & set(first.final_test_ids)


def test_empirical_fit_rejects_validation_person() -> None:
    case = _case("held-out", "validation", "a", "X")
    try:
        EmpiricalChartResponseModel.fit(
            [case],
            model_id="m",
            questionnaire_version="Q1",
            split_manifest_hash="0" * 64,
            feature_names=["type"],
        )
    except ValueError as exc:
        assert "development" in str(exc)
    else:
        raise AssertionError("validation person entered fit")


def test_empirical_distribution_shrinks_and_normalizes() -> None:
    cases = [
        _case("a", "development", "yes", "Generator"),
        _case("b", "development", "yes", "Generator"),
        _case("c", "development", "no", "Projector"),
    ]
    model = EmpiricalChartResponseModel.fit(
        cases,
        model_id="m",
        questionnaire_version="Q1",
        split_manifest_hash="0" * 64,
        feature_names=["type"],
    )
    distribution = model.response_distribution("Q1", {"type": "Generator"})
    assert abs(sum(distribution.values()) - 1.0) < 1e-12
    assert distribution["yes"] > distribution["no"]


def test_chart_permutation_moves_whole_records() -> None:
    cases = [_case(str(i), "development", "a", str(i)) for i in range(5)]
    first = permute_chart_assignments(cases, 7)
    second = permute_chart_assignments(cases, 7)
    assert first == second
    assert {row["type"] for row in first.values()} == {str(i) for i in range(5)}
