"""Lossless, local-only owner survey packet for the experience pilot."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import stat
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tasks/life-patterns-experience-pilot-20261017/build_owner_source_packet.py"
SPEC = importlib.util.spec_from_file_location("owner_packet", SCRIPT)
assert SPEC and SPEC.loader
PACKET = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKET)


def fixtures(tmp_path: Path) -> tuple[Path, Path, Path, dict[str, str]]:
    content = {
        "latest_v33": (
            '{"schema":"local_life_patterns_v3_3_pilot_unsubmitted",'
            '"answers":{"TF1-A0":{"other":"Déjà vu and surprise","selected":["other"]}},'
            '"unique_behaviors":[{"behavior":"An unusual practice"}],'
            '"v3_2_answers":{},"role_entry_review":{"episodes":[]}} \n'
        ),
        "primary_84": (
            '{"schema":"life-patterns-full-survey-participant-export-v2",'
            '"turns":[{"turn_id":"V7-A0","question_text":"Tell me about a moment",'
            '"answer_text":"One text answer."}]}\n'
        ),
        "secondary_cf003": (
            '{"schema":"life-patterns-cf003-secondary-v0",'
            '"turns":[{"question_id":"CF003-1","question_text":"Separate follow-up",'
            '"answer_text":"Another answer."}]}\n'
        ),
    }
    paths = {name: tmp_path / (name + ".json") for name in content}
    for name, path in paths.items():
        path.write_bytes(content[name].encode("utf-8"))
    return (
        paths["latest_v33"],
        paths["primary_84"],
        paths["secondary_cf003"],
        content,
    )


def test_owner_packet_preserves_exact_raw_sources_without_response_interpretation(tmp_path: Path):
    latest, primary, secondary, content = fixtures(tmp_path)
    output = tmp_path / "private" / "full-survey-source-packet.json"
    receipt = PACKET.build(
        latest_v33=latest, primary=primary, secondary=secondary, output=output
    )
    assert receipt["sources"] == 3
    assert receipt["source_counts"] == {
        "v33_answers": 1,
        "unusual_behaviors": 1,
        "primary_turns": 1,
        "secondary_turns": 1,
    }
    assert stat.S_IMODE(output.stat().st_mode) == 0o600
    packet = json.loads(output.read_text())
    assert packet["schema"] == "life-patterns-owner-source-packet-v1"
    assert packet["no_new_experience_answers_imputed"] is True
    assert len(packet["sources"]) == 3
    for source in packet["sources"]:
        orig = content[source["source_id"]]
        assert source["text"] == orig
        assert source["sha256"] == hashlib.sha256(orig.encode("utf-8")).hexdigest()
        assert source["byte_count"] == len(orig.encode("utf-8"))
    assert not any("experience_pilot_answers" in x for x in packet)


def test_source_packet_rejects_mismatched_schemas_and_overwrites(tmp_path: Path):
    latest, primary, secondary, _ = fixtures(tmp_path)
    output = tmp_path / "secure.json"
    primary.write_text('{"schema":"someone-else","turns":[]}')
    with pytest.raises(ValueError, match="Unexpected source schema"):
        PACKET.build(
            latest_v33=latest, primary=primary, secondary=secondary, output=output
        )
    assert not output.exists()
    primary.write_text('{"schema":"life-patterns-full-survey-participant-export-v2","turns":[]}')
    PACKET.build(latest_v33=latest, primary=primary, secondary=secondary, output=output)
    original_bytes = output.read_bytes()
    with pytest.raises(FileExistsError):
        PACKET.build(latest_v33=latest, primary=primary, secondary=secondary, output=output)
    assert output.read_bytes() == original_bytes


def test_owner_data_never_in_checked_in_pilot_artifacts():
    html = (SCRIPT.parent / "EXPERIENCE-MEANING-PILOT-v1.html").read_text()
    assert "life-patterns-owner-source-packet-v1" in html
    assert "local_life_patterns_v3_3_pilot_unsubmitted" in html
    assert "setPriorSources" in html
    assert "sourceSchemas" in html
    assert "prior_sources:priorSources" in html
    assert not any(prefix in html for prefix in ("/mnt/hdd/", "/home/"))
    assert "new Function" not in html and "eval(" not in html
