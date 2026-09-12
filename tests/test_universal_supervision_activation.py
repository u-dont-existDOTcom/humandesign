from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"


def test_root_agents_activates_current_universal_supervision() -> None:
    text = AGENTS.read_text(encoding="utf-8")
    required = (
        "## Universal development supervision activation",
        "u-dont-existDOTcom/universal-dev-architecture",
        "beginning with `LESSON-INDEX.md`",
        "activate only the task-relevant current patterns",
        "Record how that guidance entered the current reasoning path",
        "`the rule exists in GitHub` is not activation evidence",
    )
    for phrase in required:
        assert phrase in text


def test_root_agents_blocks_manufactured_prerequisite_hardening() -> None:
    text = AGENTS.read_text(encoding="utf-8")
    required = (
        "method-necessity / manufactured-prerequisite check",
        "Keep the owner outcome, genuine constraint, and proposed method separate",
        "strongest materially simpler live alternative",
        "`UNRESOLVED` permits a bounded reversible discriminating experiment, not architecture hardening",
        "Routine reversible implementation choices do not trigger this gate",
        "treat that as a supervision escape",
    )
    for phrase in required:
        assert phrase in text
