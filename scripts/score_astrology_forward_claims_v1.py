#!/usr/bin/env python3
"""Validate and score atomic, predeclared astrology-to-behavior claims.

This is an evaluation adapter, not a chart engine or evidence of predictive validity.
A source reading may remain exploratory, but only an admitted directional claim
can earn a score. Outcomes and source rules must be frozen independently before
participants answer; self-reported timestamps do not prove that chronology.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA = "astrology-forward-claims-v1"
RESPONSE_SCHEMA = "astrology-forward-responses-v1"
PHASES = {"DEVELOPMENT", "VALIDATION", "FINAL_TEST"}
PANELS = {"matched", "broad"}
KINDS = {"DECLARED_UNCALIBRATED", "DEVELOPMENT_CALIBRATED"}
ABSTAIN = {"__UNKNOWN__", "__MISSING__"}


class ContractError(ValueError):
    """The frozen package, labels or scoring request violates the contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _utc(value: Any, field: str) -> datetime:
    _require(_nonblank(value), f"{field} must be an ISO-8601 UTC instant")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{field} invalid timestamp") from exc
    _require(parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0,
             f"{field} must be timezone-aware UTC")
    return parsed


def _vector(value: Any, options: list[str], label: str) -> dict[str, float]:
    _require(isinstance(value, dict) and set(value) == set(options),
             f"{label}: probabilities must cover every option exactly once")
    checked: dict[str, float] = {}
    for option in options:
        number = value[option]
        _require(type(number) in (int, float) and math.isfinite(number)
                 and 0 < number < 1, f"{label}: {option} must have probability in (0,1)")
        checked[option] = float(number)
    _require(math.isclose(sum(checked.values()), 1.0, abs_tol=1e-9),
             f"{label}: probabilities must sum to 1")
    return checked


def validate_predictions(package: dict[str, Any]) -> dict[str, Any]:
    _require(isinstance(package, dict) and package.get("schema") == SCHEMA,
             "invalid prediction-package schema")
    for field in ("study_id", "arm_id", "ruleset_version", "questionnaire_sha256",
                  "chart_feature_sha256"):
        _require(_nonblank(package.get(field)), f"missing {field}")
    for field in ("questionnaire_sha256", "chart_feature_sha256"):
        _require(len(package[field]) == 64 and all(c in "0123456789abcdef" for c in package[field]),
                 f"{field} must be lowercase sha256")
    _utc(package.get("created_at_utc"), "created_at_utc")
    phase = package.get("phase")
    _require(phase in PHASES, "invalid phase")
    _require(package.get("probability_status") in KINDS,
             "probability_status must distinguish uncalibrated and development calibrated")
    decoys = package.get("decoy_panels")
    _require(isinstance(decoys, list), "decoy_panels must be a list")
    ids: set[str] = set()
    panel_types: set[str] = set()
    for d in decoys:
        _require(isinstance(d, dict) and _nonblank(d.get("id"))
                 and d.get("panel") in PANELS and _nonblank(d.get("panel_source_ref")),
                 "every decoy requires id, matched/broad panel, provenance")
        _require(d["id"] not in ids, "duplicate decoy id")
        ids.add(d["id"])
        panel_types.add(d["panel"])
    if phase in {"VALIDATION", "FINAL_TEST"}:
        _require(panel_types == PANELS, "evidential phase requires matched and broad decoys")
    claims = package.get("claims")
    _require(isinstance(claims, list) and len(claims) > 0, "nonempty claims list required")
    claim_ids: set[str] = set()
    question_ids: set[str] = set()
    directional = nulls = 0
    for claim in claims:
        _require(isinstance(claim, dict), "claim must be an object")
        cid = claim.get("claim_id")
        qid = claim.get("question_id")
        _require(_nonblank(cid) and _nonblank(qid), "claim_id and question_id required")
        _require(cid not in claim_ids and qid not in question_ids,
                 "duplicate claim_id or question_id; overlapping alternatives cannot score twice")
        claim_ids.add(cid)
        question_ids.add(qid)
        for key in ("domain", "context", "response_window", "operational_definition",
                    "dependency_cluster"):
            _require(_nonblank(claim.get(key)), f"{cid}: missing {key}")
        refs = claim.get("source_rule_refs")
        _require(isinstance(refs, list) and bool(refs)
                 and all(_nonblank(ref) for ref in refs), f"{cid}: source rules required")
        status = claim.get("status")
        _require(status in {"DIRECTIONAL", "NULL", "UNRESOLVED"}, f"{cid}: invalid status")
        if status != "DIRECTIONAL":
            nulls += 1
            _require(_nonblank(claim.get("reason")), f"{cid}: null/unresolved needs reason")
            for name in ("preferred_option", "predicted", "baseline", "decoys"):
                _require(name not in claim, f"{cid}: {status} must not claim predictive credit")
            continue
        directional += 1
        options = claim.get("outcomes")
        _require(isinstance(options, list) and len(options) >= 2
                 and all(_nonblank(option) for option in options)
                 and len(options) == len(set(options))
                 and not set(options) & ABSTAIN,
                 f"{cid}: at least two distinct exclusive outcomes required")
        _require(_nonblank(claim.get("baseline_source_ref")),
                 f"{cid}: baseline_source_ref required; no invented base rates")
        predicted = _vector(claim.get("predicted"), options, f"{cid}.predicted")
        baseline = _vector(claim.get("baseline"), options, f"{cid}.baseline")
        preferred = claim.get("preferred_option")
        _require(preferred in options, f"{cid}: preferred_option must be one of outcomes")
        _require(all(predicted[preferred] > predicted[option]
                     for option in options if option != preferred),
                 f"{cid}: no unique preferred option; both alternatives cannot be hits")
        _require(predicted[preferred] > baseline[preferred],
                 f"{cid}: no incremental preferred-option probability over baseline")
        other = claim.get("counterexample_outcomes")
        _require(isinstance(other, list) and set(other) == set(options) - {preferred}
                 and len(other) == len(options) - 1,
                 f"{cid}: enumerate all opposite outcomes as counterexamples")
        dv = claim.get("decoys")
        _require(isinstance(dv, dict) and set(dv) == ids,
                 f"{cid}: decoys must cover declared chart controls exactly")
        for decoy_id in ids:
            _vector(dv[decoy_id], options, f"{cid}.decoys.{decoy_id}")
    all_domains = {claim["domain"] for claim in claims}
    directional_domains = {claim["domain"] for claim in claims if claim["status"] == "DIRECTIONAL"}
    return {"total": len(claims), "directional": directional, "null_or_unresolved": nulls,
            "domain_count": len(all_domains), "directional_domain_count": len(directional_domains),
            "decoy_count": len(ids), "phase": phase,
            "probability_status": package["probability_status"]}


def _brier(prob: dict[str, float], observed: str) -> float:
    return sum((value - float(option == observed)) ** 2 for option, value in prob.items())


def _log(prob: dict[str, float], observed: str) -> float:
    return -math.log(prob[observed])


def score_predictions(package_bytes: bytes, response: dict[str, Any]) -> dict[str, Any]:
    package = json.loads(package_bytes)
    state = validate_predictions(package)
    _require(response.get("schema") == RESPONSE_SCHEMA, "invalid response schema")
    digest = hashlib.sha256(package_bytes).hexdigest()
    _require(response.get("prediction_sha256") == digest,
             "response is not bound to these exact prediction bytes")
    captured = _utc(response.get("captured_at_utc"), "captured_at_utc")
    _require(captured > _utc(package["created_at_utc"], "created_at_utc"),
             "response must be recorded after the declared prediction time")
    answers = response.get("answers")
    _require(isinstance(answers, dict), "answers must be object")
    _require(set(answers).issubset({c["question_id"] for c in package["claims"]}),
             "unexpected answer question id")
    decoy_metadata = {item["id"]: item["panel"] for item in package["decoy_panels"]}
    records: list[dict[str, Any]] = []
    per_cluster: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for claim in package["claims"]:
        if claim["status"] != "DIRECTIONAL":
            records.append({"claim_id":claim["claim_id"], "status":claim["status"],
                            "scored":False, "reason":"no directional prediction"})
            continue
        observed = answers.get(claim["question_id"], "__MISSING__")
        _require(observed in set(claim["outcomes"]) | ABSTAIN,
                 f"{claim['claim_id']}: observation is not a predeclared outcome")
        if observed in ABSTAIN:
            records.append({"claim_id":claim["claim_id"], "status":observed,
                            "scored":False, "reason":"missing/unknown; no credit"})
            continue
        model = claim["predicted"]
        baseline = claim["baseline"]
        outcome = {
            "claim_id":claim["claim_id"], "status":"SCORED", "scored":True,
            "question_id":claim["question_id"], "dependency_cluster":claim["dependency_cluster"],
            "predicted_option":claim["preferred_option"],
            "observed_option":observed,
            "directional_hit":observed == claim["preferred_option"],
            "model_brier":_brier(model, observed), "baseline_brier":_brier(baseline, observed),
            "brier_skill":_brier(baseline, observed) - _brier(model, observed),
            "model_logloss":_log(model, observed), "baseline_logloss":_log(baseline, observed),
            "log_skill":_log(baseline, observed) - _log(model, observed),
            "decoy_log_skill": {
                d: _log(dp, observed) - _log(model, observed)
                for d, dp in claim["decoys"].items()
            },
            "decoy_brier_skill": {
                d: _brier(dp, observed) - _brier(model, observed)
                for d, dp in claim["decoys"].items()
            },
        }
        records.append(outcome)
        per_cluster[claim["dependency_cluster"]].append(outcome)
    scored = [r for r in records if r["scored"]]
    def cluster_mean(field: str) -> float | None:
        if not per_cluster:
            return None
        return sum(sum(r[field] for r in group) / len(group)
                   for group in per_cluster.values()) / len(per_cluster)
    decoy_results = []
    for d, panel in decoy_metadata.items():
        if not scored:
            margin = None
        else:
            margin = sum(
                sum(r["decoy_log_skill"][d] for r in group) / len(group)
                for group in per_cluster.values()
            ) / len(per_cluster)
        decoy_results.append({"id":d, "panel":panel,
                              "mean_true_over_decoy_log_score":margin})
    missing = sum(r["status"] in ABSTAIN for r in records)
    summary = {
        **state,
        "scored":len(scored), "missing_or_unknown":missing,
        "scorable_coverage": len(scored) / state["directional"] if state["directional"] else 0.0,
        "directional_hits":sum(r.get("directional_hit",False) for r in scored),
        "cluster_count":len(per_cluster),
        "mean_brier_skill_by_dependency_cluster":cluster_mean("brier_skill"),
        "mean_log_skill_by_dependency_cluster":cluster_mean("log_skill"),
        "decoy_comparison":decoy_results,
        "independent_freeze_proven_by_this_tool":False,
        "human_predictive_validity_proven_by_this_tool":False,
        "warning":"Self-declared timestamps and hashes do not establish independent outcome-blind freezing, randomization, calibration, or held-out generalization.",
    }
    return {"schema":"astrology-forward-claim-evaluation-v1",
            "prediction_sha256":digest,"summary":summary,"records":records}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--responses", type=Path,
                        help="Optional: score frozen responses; otherwise only validate predictions")
    args = parser.parse_args()
    try:
        package_bytes = args.predictions.read_bytes()
        if args.responses:
            result = score_predictions(package_bytes, json.loads(args.responses.read_text()))
        else:
            result = {"schema":"astrology-forward-validation-v1",
                      "prediction_sha256":hashlib.sha256(package_bytes).hexdigest(),
                      "contract":validate_predictions(json.loads(package_bytes)),
                      "outcome_blind_freeze_independently_verified":False}
        print(json.dumps(result, indent=2, sort_keys=True))
    except (OSError, UnicodeError, json.JSONDecodeError, ContractError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()