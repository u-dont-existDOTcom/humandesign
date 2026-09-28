from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from hdmatch.empirical_astrology import (
    ContractError,
    LiteratureModelV1,
    load_frozen_contract,
    verify_required_git_ancestor,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_frozen_contract_hashes_versions_and_authorization() -> None:
    contract = load_frozen_contract(REPOSITORY_ROOT)
    assert (
        contract.decision_sha256
        == hashlib.sha256(
            (
                REPOSITORY_ROOT / "reference/empirical_astrology/literature_model_v1b_decision.json"
            ).read_bytes()
        ).hexdigest()
    )
    assert (
        contract.wave4_gate_sha256
        == hashlib.sha256(
            (
                REPOSITORY_ROOT
                / "reference/empirical_astrology/literature_model_v1b_wave4_gate.json"
            ).read_bytes()
        ).hexdigest()
    )
    assert contract.decision["review_base_commit"] == ("e7f82ab4a1b08705bf4429958a0d577b2758c407")
    assert (
        contract.model["work_authorization"][
            "prospective_recruitment_or_outcome_collection_authorized"
        ]
        is False
    )
    verify_required_git_ancestor(contract)


def test_assembled_model_has_only_theory_neutral_feature() -> None:
    model = LiteratureModelV1.load(REPOSITORY_ROOT)
    assert model.executable_feature_ids == ("TN-001",)
    assert model.executable_astrology_feature_ids == ()
    assert model.contract.model["astrology_weights"] == {}
    assert model.contract.model["aspect_to_trait_mappings"] == []


def _copy_contract(tmp_path: Path) -> None:
    for relative in (
        "reference/empirical_astrology/literature_model_v1b_decision.json",
        "reference/empirical_astrology/literature_feature_registry_v1.json",
        "reference/empirical_astrology/literature_model_v1.json",
        "reference/empirical_astrology/literature_model_v1b_wave4_gate.json",
    ):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPOSITORY_ROOT / relative, target)


def test_contract_rejects_injected_astrology_weight(tmp_path: Path) -> None:
    _copy_contract(tmp_path)
    path = tmp_path / "reference/empirical_astrology/literature_model_v1.json"
    model = json.loads(path.read_text())
    model["astrology_weights"] = {"CF-007": 1.0}
    model["astrology_coefficient_vector_length"] = 1
    path.write_text(json.dumps(model))
    with pytest.raises(ContractError, match="Wave 4 Pro-reviewed bytes"):
        load_frozen_contract(tmp_path)


def test_contract_rejects_injected_feature_mapping(tmp_path: Path) -> None:
    _copy_contract(tmp_path)
    registry_path = tmp_path / "reference/empirical_astrology/literature_feature_registry_v1.json"
    registry = json.loads(registry_path.read_text())
    registry["aspect_to_trait_mappings"] = [{"body_pair": "invented"}]
    registry_path.write_text(json.dumps(registry))
    model_path = tmp_path / "reference/empirical_astrology/literature_model_v1.json"
    model = json.loads(model_path.read_text())
    model["feature_registry"]["sha256"] = hashlib.sha256(registry_path.read_bytes()).hexdigest()
    model_path.write_text(json.dumps(model))
    with pytest.raises(ContractError, match="Wave 4 Pro-reviewed bytes"):
        load_frozen_contract(tmp_path)


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("randomness_and_determinism", "base_seed"), 1),
        (("primary_model", "minimum_effect_beta"), 0.0),
        (("eligibility", "language"), "Any language"),
        (("primary_null", "draws"), 99),
        (("multiplicity", "primary"), "changed"),
        (
            ("work_authorization", "prospective_recruitment_or_outcome_collection_authorized"),
            True,
        ),
        (("executable_astrology_features",), ["CF-007"]),
    ],
)
def test_contract_rejects_any_reviewed_model_drift(
    tmp_path: Path,
    path: tuple[str, ...],
    replacement: object,
) -> None:
    _copy_contract(tmp_path)
    model_path = tmp_path / "reference/empirical_astrology/literature_model_v1.json"
    model = json.loads(model_path.read_text())
    target = model
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    model_path.write_text(json.dumps(model))
    with pytest.raises(ContractError, match="Wave 4 Pro-reviewed bytes"):
        load_frozen_contract(tmp_path)


def test_contract_rejects_scoring_key_and_column_order_drift(tmp_path: Path) -> None:
    _copy_contract(tmp_path)
    model_path = tmp_path / "reference/empirical_astrology/literature_model_v1.json"
    model = json.loads(model_path.read_text())
    model["outcome"]["scoring_key"]["extraversion"]["positive"][0] = 2
    columns = model["primary_model"]["nuisance_columns_in_order"]
    columns[0], columns[1] = columns[1], columns[0]
    model_path.write_text(json.dumps(model))
    with pytest.raises(ContractError, match="Wave 4 Pro-reviewed bytes"):
        load_frozen_contract(tmp_path)


def test_contract_rejects_gate_rewrite_even_if_scientific_files_stay_fixed(
    tmp_path: Path,
) -> None:
    _copy_contract(tmp_path)
    gate_path = tmp_path / "reference/empirical_astrology/literature_model_v1b_wave4_gate.json"
    gate = json.loads(gate_path.read_text())
    gate["work_authorization"]["prospective_recruitment_or_outcome_collection_authorized"] = True
    gate_path.write_text(json.dumps(gate))
    with pytest.raises(ContractError, match="gate bytes"):
        load_frozen_contract(tmp_path)


def test_assembled_model_source_does_not_import_dormant_astrology_calculators() -> None:
    source = (REPOSITORY_ROOT / "src/hdmatch/empirical_astrology/model.py").read_text()
    assert "geometry" not in source
    assert "karaka" not in source
