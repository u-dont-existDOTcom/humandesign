"""Create private lossless owner-survey results with an appended experience module.

No actual respondent answers are committed in this repo. Run only on authorized
local source files. Refuses to overwrite existing files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sealed_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(raw)
    assert json.loads(path.read_bytes()) == data


def build(prior: Path, experience: Path, pilot_result: Path, master: Path) -> dict:
    prior_raw, experience_raw = prior.read_bytes(), experience.read_bytes()
    previous, added = json.loads(prior_raw), json.loads(experience_raw)
    assert previous["schema"] == "life-patterns-owner-source-packet-v1"
    assert len(previous["sources"]) == 3
    assert added["schema"] == "life-patterns-experience-pilot-answers-v1"
    assert added["instrument"] == "experience-meaning-v1-20261017"
    assert added["no_scoring"] is True
    assert not added.get("prior_sources")
    assert [x["question_id"] for x in added["responses"]] == [
        f"EM{i:02}" for i in range(1, 9)
    ]
    assert all(x["state"] == "ANSWERED" for x in added["responses"])
    for source in previous["sources"]:
        assert sha(source["text"].encode("utf-8")) == source["sha256"]
    resumed_pilot = dict(added)
    resumed_pilot["prior_sources"] = previous["sources"]
    assert resumed_pilot["responses"] == added["responses"]
    sealed_write(pilot_result, resumed_pilot)
    combined = {
        "schema": "life-patterns-owner-results-with-experience-addendum-v1",
        "status": "PRIVATE_POST_FREEZE_EXPLORATORY_NOT_ASTROLOGY_SCORED",
        "original_survey_packet_sha256": sha(prior_raw),
        "experience_uploaded_source_sha256": sha(experience_raw),
        "historical_original_sources": previous["sources"],
        "historical_source_content_preserved": True,
        "experience_addendum": added,
        "experience_timing": "After original primary and secondary survey freezes",
        "validity_boundary": (
            "Post-hoc self-reports do not enter original blind astrology/HD scores "
            "or redefine historical answers."
        ),
        "measurement_caution": (
            "Legacy intensity item represents occasional peaks in some responses. "
            "Reported usual intensity differs; preserve note, never impute it."
        ),
    }
    sealed_write(master, combined)
    assert json.loads(master.read_bytes())["experience_addendum"] == added
    return {
        "source_files": 3,
        "prior_source_records": 116,
        "experience_responses": 8,
        "uploaded_experience_sha256": sha(experience_raw),
        "pilot_bytes": pilot_result.stat().st_size,
        "master_bytes": master.stat().st_size,
        "preserved_source_hashes": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for arg in ("prior", "experience", "pilot-result", "master"):
        parser.add_argument("--" + arg, type=Path, required=True)
    a = parser.parse_args()
    print(json.dumps(build(a.prior, a.experience, a.pilot_result, a.master)))
