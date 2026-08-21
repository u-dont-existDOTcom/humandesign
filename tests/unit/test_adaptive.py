from hdmatch.search.adaptive import expected_information_gain, select_next_question


def test_perfect_split_has_one_bit_information_gain() -> None:
    likelihoods = [{"yes": 1.0, "no": 0.0}, {"yes": 0.0, "no": 1.0}]
    assert expected_information_gain([1.0, 1.0], likelihoods) == 1.0


def test_selector_accounts_for_reliability_and_burden() -> None:
    utility = select_next_question(
        [1.0, 1.0],
        {
            "costly": [{"a": 1.0}, {"b": 1.0}],
            "cheap": [{"a": 0.9, "b": 0.1}, {"a": 0.1, "b": 0.9}],
        },
        burden={"costly": 0.6},
    )
    assert utility is not None
    assert utility.question_id == "cheap"
