from scripts.lilly_horary_job_v1 import compose_v1_verdict


def test_any_affirmative_clause_is_yes():
    assert compose_v1_verdict(
        affirmative_clauses={"RECEPTION": True},
        perfection_state="composed",
        indeterminate_positive_perfection=False,
    ) == "YES"


def test_indeterminate_positive_path_defers_without_affirmative_clause():
    assert compose_v1_verdict(
        affirmative_clauses={"RECEPTION": False},
        perfection_state="composed",
        indeterminate_positive_perfection=True,
    ) == "DEFER"


def test_composed_without_affirmative_is_no():
    assert compose_v1_verdict(
        affirmative_clauses={"RECEPTION": False},
        perfection_state="composed",
        indeterminate_positive_perfection=False,
    ) == "NO"
