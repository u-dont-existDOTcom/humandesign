from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import life_patterns_owner_v43_crosswalk_rerun as subject  # noqa: E402


def test_cap_confidence_preserves_both_upper_bounds() -> None:
    assert subject.cap_confidence(0.9, 0.5) == 0.5
    assert subject.cap_confidence(0.65, 0.75) == 0.65
    assert subject.cap_confidence(1.0, 0.25) == 0.25


def test_profile_mapping_uses_mapping_id_as_observable() -> None:
    mapping = {"id": "PROFILE_LINE5_PROJECTION", "cluster": "PROFILE_STRUCTURE"}
    assert subject.observable_id(mapping) == "PROFILE_LINE5_PROJECTION"
    ordinary = {"id": "CH_24_61_MYSTERY", "cluster": "EXISTENTIAL_MYSTERY"}
    assert subject.observable_id(ordinary) == "EXISTENTIAL_MYSTERY"


def test_neutral_core_merge_ignores_uninstantiated_core_state() -> None:
    score = {
        "matches": (("A", "M1"),),
        "contra_matches": (),
        "net": 1.0,
        "evidence": 1.0,
        "contra": 0.0,
        "meaningful": 0,
        "detail": 50.0,
        "core": 0.0,
        "winner_by_cluster": {"A": "M1"},
        "contra_winners": {},
    }
    rows = [
        {
            "state": {
                "start": 1.0,
                "end": 2.0,
                "dur": 1.0,
                "type": "Projector",
                "auth": "Splenic",
                "profile": "2/4",
                "centers": frozenset({"G"}),
            },
            "score": score,
        },
        {
            "state": {
                "start": 2.0,
                "end": 3.0,
                "dur": 1.0,
                "type": "Generator",
                "auth": "Sacral",
                "profile": "1/3",
                "centers": frozenset({"Sacral"}),
            },
            "score": score,
        },
    ]
    merged = subject.merge_scored_neutral_core(rows)
    assert len(merged) == 1
    assert merged[0]["state"]["start"] == 1.0
    assert merged[0]["state"]["end"] == 3.0
    assert merged[0]["state"]["dur"] == 2.0
