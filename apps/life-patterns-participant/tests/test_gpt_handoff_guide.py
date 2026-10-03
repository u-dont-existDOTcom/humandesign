import copy
import json
from pathlib import Path

from test_gpt_submission_action import candidate_record

ROOT = Path(__file__).resolve().parents[3]
GUIDE = ROOT / "reference/custom_gpt/ACTION-HANDOFF-GUIDE-v1.md"


def test_documented_backup_builder_preserves_all_79_source_answers(tmp_path):
    candidate = candidate_record()
    seed = candidate["turns"][0]
    candidate["turns"] = [
        dict(
            seed,
            turn_id=f"synthetic-{i}",
            answer_text=f"  Answer {i}; if rested, perhaps …\nnot always.  ",
        )
        for i in range(79)
    ]
    before = copy.deepcopy(candidate)
    code = GUIDE.read_text().split("```python\n", 1)[1].split("```", 1)[0]
    destination = tmp_path / "candidate.json"
    handoff = tmp_path / "handoff.json"
    code = code.replace(
        "Path('/mnt/data/life-patterns-candidate-backup.json')", f"Path({str(destination)!r})"
    ).replace(
        "Path('/mnt/data/life-patterns-review-handoff.json')", f"Path({str(handoff)!r})"
    )
    scope = {"candidate": candidate}
    exec(compile(code, str(GUIDE), "exec"), scope)
    assert json.loads(destination.read_text()) == before
    saved_handoff = json.loads(handoff.read_text())
    assert saved_handoff == scope["body"]
    assert saved_handoff["candidate_record"] == before
    assert len(saved_handoff["request_id"]) == 32
    assert set(saved_handoff) == {"request_id", "research_use_consented", "candidate_record"}
    assert candidate == before


def test_backup_builder_does_not_manufacture_consent(tmp_path):
    import pytest

    candidate = candidate_record()
    candidate["consent"]["research_use_consented"] = False
    code = GUIDE.read_text().split("```python\n", 1)[1].split("```", 1)[0]
    with pytest.raises(AssertionError):
        exec(compile(code, str(GUIDE), "exec"), {"candidate": candidate})
    assert candidate["consent"]["research_use_consented"] is False


def test_delivery_rules_are_in_the_shipped_instruction_chain():
    # These checks establish instruction presence, not participant-visible compliance.
    instruction = (ROOT / "reference/custom_gpt/life_patterns_voice_interviewer_v2.md").read_text()
    text = GUIDE.read_text()
    assert "ACTION-HANDOFF-GUIDE-v1.md" in instruction
    assert "backup and real file link FIRST" in instruction
    assert "Please click Allow on this tool call to continue." in text
    assert text.count("Please click Allow on this tool call to continue.") == 1
    assert "life-patterns-review-handoff.json" in text
    assert "life-patterns-review-receipt.json" in text
    assert "idempotent replay" in text
    assert "Allow once" in text
    assert "life-patterns-participant-production.up.railway.app" in text
    assert "life-patterns-action-error.json" in text
    assert "not a percentage of 79 routes or 73 facets" in text
    assert "not a guarantee" in text
    assert "about **15 minutes**" in text
    assert "recommended_check_after_seconds" in text
    assert "send any message" in text


def test_owner_update_checkpoint_rules_are_present():
    guide = GUIDE.read_text()
    builder = (ROOT / "reference/custom_gpt/GPT-BUILDER-CONFIG.md").read_text()
    setup = (ROOT / "reference/custom_gpt/LIFE-PATTERNS-VOICE-GPT-SETUP.md").read_text()
    assert "Context-loss checkpoint for owner testing" in guide
    assert "life-patterns-live-recovery-checkpoint.json" in guide
    assert "never replace a prior record with an empty candidate" in guide
    assert "Builder Preview only for short smoke tests" in builder
    assert "Before clicking Update while an interview is in progress" in builder
    assert "verify its answer count before clicking Update" in setup
    assert "context loss, not evidence that the historical interview never existed" in setup
