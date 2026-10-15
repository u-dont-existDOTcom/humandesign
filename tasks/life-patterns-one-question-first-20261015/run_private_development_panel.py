"""Development-only source-preserving sensitivity check against frozen AstroHD V1.5.

Never publish personal source, exact birth input, target rank or profile from here.
This is NOT an independent prediction: the six astronomical rules were selected
using the known owner's birth date, and neutral source coding is researcher-drafted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

from hdmatch.evaluation import astrohd_v15_decoder as score


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def private_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(value, out, indent=2, ensure_ascii=False)
        out.write("\n")
    path.chmod(0o600)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ephemeris", type=Path, required=True)
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)
    parser.add_argument("--actual-utc", required=True)
    parser.add_argument("--count", type=int, choices=(99, 999, 9999), default=999)
    args = parser.parse_args()
    data = json.loads(args.source.read_text())
    if data["schema"] != "local_life_patterns_v3_3_pilot_unsubmitted":
        raise ValueError("Expected original V3.3 respondent export")
    role = data["role_entry_review"]
    if len(data["answers"]) != 25 or not isinstance(data["unique_behaviors"], list):
        raise ValueError("Unexpected source completeness")
    private_review = json.loads(args.profile.read_text())
    if private_review.get("source_sha256") != digest(args.source):
        raise ValueError("Private source hash does not match frozen profile")
    profile = score.normalize_profile(private_review["profile"])
    if role.get("pattern") == "context_dependent" and profile["recognition_entry"] not in (
        "mixed",
        "unknown",
        "not_applicable",
    ):
        raise ValueError("Context-dependent role response cannot become an automatic signed vote")
    # Researcher-entered interpretations are development hypotheses, not participant confirmations.
    signs = score.answer_signs(profile)
    if not all((args.ephemeris / item).is_file() for item in ("sepl_18.se1", "semo_18.se1")):
        raise FileNotFoundError("Canonical production Swiss files missing")
    metadata = {
        "status": "FROZEN_BEFORE_DEVELOPMENT_SCORE",
        "source_sha256": digest(args.source),
        "source_schema": data["schema"],
        "profile": profile,
        "profile_judgment": private_review.get("profile_judgment", "UNCONFIRMED"),
        "score_signs": list(signs),
        "model_sha256": digest(score.MODEL_PATH),
        "behavioral_bridge_sha256": digest(score.BRIDGE_PATH),
        "scorer_sha256": digest(Path(score.__file__)),
        "ephemeris_sha256": {
            item: digest(args.ephemeris / item) for item in ("sepl_18.se1", "semo_18.se1")
        },
        "primary_panel_seed": 150925,
        "candidate_count": args.count,
        "birthplace": {"latitude": args.latitude, "longitude": args.longitude},
        "important": [
            "Same-person development only, not independent DOB prediction",
            "Selected astronomical conditions were fitted using the known birth",
            "Do not infer role-entry polarity from conditional examples",
            "No source answer was changed to produce a desired natal result",
        ],
    }
    private_json(args.output / "FROZEN-BEFORE-SCORE.json", metadata)
    panel = score.run_panel(
        profile,
        latitude=args.latitude,
        longitude=args.longitude,
        count=args.count,
        ephemeris_root=args.ephemeris,
    )
    private_json(args.output / "DECOY-PANEL-BEFORE-TARGET.json", panel)
    checked = score.check_instant(
        profile,
        datetime.fromisoformat(args.actual_utc),
        latitude=args.latitude,
        longitude=args.longitude,
        count=args.count,
        ephemeris_root=args.ephemeris,
    )
    checked["development_not_independent"] = True
    checked["role_entry_code"] = profile["recognition_entry"]
    checked["participant_confirmed_five_domain_profile"] = False
    checked["panel_signature_sha256"] = panel["panel_sha256"]
    private_json(args.output / "OWNER-ANSWER-COMPARISON.json", checked)
    # Only aggregate results leave the private device log.
    print(
        json.dumps(
            {
                "panel_size": args.count,
                "answer_signs": list(signs),
                "target_score": checked["score"],
                "rank_best": checked["rank_best"],
                "rank_worst": checked["rank_worst"],
                "ties": checked["tied_other_candidates"],
                "higher": checked["higher_candidates"],
                "target_joint_first": checked["joint_first"],
                "control": "SAME_PERSON_DEVELOPMENT_NOT_BLIND",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
