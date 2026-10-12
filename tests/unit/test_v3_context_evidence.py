from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def test_v3_context_fields():
    for name in ("build_interactive_pilot.py","LIFE_PATTERNS_V3_OFFLINE_PILOT.html"):
        s=(ROOT/"tasks/life-patterns-idiographic-20261010"/name).read_text()
        assert all(k in s for k in ("context_rule:","recent_case:","no_stable_default:"))
