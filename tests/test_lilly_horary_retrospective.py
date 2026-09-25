from scripts.lilly_horary_retrospective import frozen_verdict


def test_frozen_verdict_positive_perfection_is_yes():
    assert frozen_verdict(
        perfection_state="composed",
        present_kinds={"translation_of_light"},
        indeterminate_kinds=set(),
    ) == "YES"


def test_frozen_verdict_indeterminate_positive_path_defers():
    assert frozen_verdict(
        perfection_state="composed",
        present_kinds=set(),
        indeterminate_kinds={"collection_of_light"},
    ) == "DEFER"


def test_frozen_verdict_no_positive_path_is_no():
    assert frozen_verdict(
        perfection_state="composed",
        present_kinds={"prohibition"},
        indeterminate_kinds=set(),
    ) == "NO"


def test_frozen_verdict_uncomposed_defers():
    assert frozen_verdict(
        perfection_state="not_evaluable",
        present_kinds=set(),
        indeterminate_kinds=set(),
    ) == "DEFER"
