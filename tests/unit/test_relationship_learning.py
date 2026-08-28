import pytest

from hdmatch.relationship.learning import (
    RelationshipAxisEvaluation,
    detect_revision_signals,
    summarize_relationship_learning,
)


def test_learning_summary_aggregates_hits_misses_context_and_error() -> None:
    summary = summarize_relationship_learning(
        (
            RelationshipAxisEvaluation(
                case_id="case-1",
                model_id="astro-v1",
                axis_id="eros_in_love",
                direction="a_to_b",
                outcome="hit",
                classifier_confidence=0.9,
                predicted_ordinal=4,
                observed_ordinal=4,
                context_tags=("distance",),
                question_ids=("RRQ_LOVE_EROS_DIRECTION",),
            ),
            RelationshipAxisEvaluation(
                case_id="case-2",
                model_id="astro-v1",
                axis_id="eros_in_love",
                direction="a_to_b",
                outcome="miss",
                classifier_confidence=0.8,
                predicted_ordinal=4,
                observed_ordinal=1,
                context_tags=("cohabitation",),
                observability_limits=("language",),
                question_ids=("RRQ_LOVE_EROS_DIRECTION",),
            ),
        )
    )
    assert summary.case_count == 2
    assert summary.evaluation_count == 2
    item = summary.axis_summaries[0]
    assert item.hit_count == 1
    assert item.miss_count == 1
    assert item.hit_rate_scored == pytest.approx(0.5)
    assert item.mean_classifier_confidence == pytest.approx(0.85)
    assert item.mean_absolute_ordinal_error == pytest.approx(1.5)
    assert item.context_counts == {"cohabitation": 1, "distance": 1}
    assert item.observability_limit_counts == {"language": 1}


def test_revision_thresholds_are_caller_supplied_and_can_flag_misses() -> None:
    summary = summarize_relationship_learning(
        RelationshipAxisEvaluation(
            case_id=f"case-{index}",
            model_id="astro-v1",
            axis_id="intellectual_stimulation_self_expansion",
            direction="a_to_b",
            outcome="miss" if index < 3 else "hit",
        )
        for index in range(4)
    )
    signals = detect_revision_signals(
        summary,
        min_scored_cases=4,
        miss_rate_threshold=0.7,
        unresolved_rate_threshold=0.8,
        context_miss_share_threshold=0.8,
        directional_hit_rate_gap_threshold=0.5,
    )
    assert len(signals) == 1
    assert signals[0].signal_type == "high_miss_rate"
    assert signals[0].value == pytest.approx(0.75)


def test_directional_asymmetry_is_flagged_without_pooling_directions() -> None:
    evaluations = []
    for index in range(4):
        evaluations.append(
            RelationshipAxisEvaluation(
                case_id=f"case-{index}",
                model_id="astro-v1",
                axis_id="eros_in_love",
                direction="a_to_b",
                outcome="hit",
            )
        )
        evaluations.append(
            RelationshipAxisEvaluation(
                case_id=f"case-{index}",
                model_id="astro-v1",
                axis_id="eros_in_love",
                direction="b_to_a",
                outcome="miss",
            )
        )
    summary = summarize_relationship_learning(evaluations)
    signals = detect_revision_signals(
        summary,
        min_scored_cases=4,
        miss_rate_threshold=1.0,
        unresolved_rate_threshold=1.0,
        context_miss_share_threshold=1.0,
        directional_hit_rate_gap_threshold=0.75,
    )
    assert any(signal.signal_type == "directional_asymmetry" for signal in signals)


def test_invalid_revision_threshold_fails_closed() -> None:
    summary = summarize_relationship_learning(())
    with pytest.raises(ValueError):
        detect_revision_signals(
            summary,
            min_scored_cases=1,
            miss_rate_threshold=1.1,
            unresolved_rate_threshold=0.5,
            context_miss_share_threshold=0.5,
            directional_hit_rate_gap_threshold=0.5,
        )
