from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

import pytest

from hdmatch.model_b_v2_new.artifacts import (
    CompiledModelArtifactV2,
    ModelFreezeReceiptV2,
    PreregistrationArtifact,
    PreregistrationArtifactV2,
    load_preregistration,
)
from hdmatch.model_b_v2_new.compiler import (
    compile_model_b_v2_new,
    freeze_model_b_v2_new,
)
from hdmatch.model_b_v2_new.provenance import (
    SnapshotStatus,
    assert_preregistration_provenance_only_equivalent,
    assert_source_catalog_provenance_only_equivalent,
    load_retrieval_manifest,
    load_source_catalog_v2,
    validate_retrieval_manifest_against_source_catalog,
)

PROJECT_ROOT = Path(__file__).parents[2]
PREREG_V1 = Path("reference/prospective/model_b_detailed_v2_new_preregistration_v1.json")
PREREG_V2 = Path("reference/prospective/model_b_detailed_v2_new_preregistration_v2.json")
SOURCE_V1 = Path("reference/prospective/model_b_detailed_v2_new_sources_v1.json")
SOURCE_V2 = Path("reference/prospective/model_b_detailed_v2_new_sources_v2.json")
MANIFEST = Path("reference/prospective/model_b_detailed_v2_new_source_retrieval_manifest_v1.json")

EXPECTED_JOVIAN_CAPTURES = {
    "https://jovianarchive.com/blogs/chart-interpretations-components/the-mental-streams": (
        880282,
        "3869896f5b17460c2a5207150acde0d5e7dc29a8c05a6a538a5fa6fe29bdb7d2",
    ),
    "https://jovianarchive.com/blogs/chart-interpretations-components/logic-and-perfection": (
        875614,
        "a6d8a207cba2a1d9a71d7a82b7ee14d452a2be2edf06cdbd2601167d3200eeb5",
    ),
    "https://jovianarchive.com/blogs/chart-interpretations-components/the-gates-of-fear-18-28": (
        876963,
        "0eae5cc15082568767f9d1a3a9c3978d18925d5556afc08a2c1dd5e7fd2e68fc",
    ),
    "https://jovianarchive.com/pages/channels-in-human-design-the-life-force": (
        588323,
        "c928d9848c13d080c13a32253d26ee0e649c09a0594236d21134a5a1bd8b76bb",
    ),
    (
        "https://jovianarchive.com/blogs/transits-global-cycles/"
        "how-pluto-in-gate-61-affects-you-q3-2021"
    ): (
        878755,
        "27a4f08723c624a6e88d16326906ffcd57fc817f11fd9bdf482cb876a66f63c6",
    ),
    (
        "https://jovianarchive.com/blogs/chart-interpretations-components/"
        "how-channels-shape-your-energy-flow-and-relationships"
    ): (
        890296,
        "5ddf3bf57026d580e1abc63c9fd44125f5e18c9b1f1e8f333e80c7d4988657bb",
    ),
    (
        "https://jovianarchive.com/blogs/human-design-basics/"
        "what-your-definition-says-about-you-in-human-design"
    ): (
        887821,
        "710986370ccdafc29da2ee9a5acaf82c0657f3dfac62d35ee3d1cfa2a6de60ee",
    ),
    (
        "https://jovianarchive.com/blogs/chart-interpretations-components/"
        "planetary-accents-in-human-design"
    ): (
        902619,
        "e5dace190723f39832d3a46e1d8f28bf9234ba5f2665aa271d1ccb391cc9a0eb",
    ),
}


def _copied_v2_repository(tmp_path: Path) -> tuple[Path, Path]:
    raw = json.loads((PROJECT_ROOT / PREREG_V2).read_text(encoding="utf-8"))
    paths = {
        raw["behavioral_target"]["path"],
        raw["question_bank"]["path"],
        raw["model_a_base"]["path"],
        raw["previous_preregistration"]["path"],
        raw["previous_source_catalog"]["path"],
        raw["source_catalog_artifact"]["path"],
        raw["retrieval_manifest"]["path"],
        *(item["path"] for item in raw["local_methods"]),
        *(item["local_path"] for item in raw["source_catalog"]),
    }
    for relative in sorted(paths):
        source = PROJECT_ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    preregistration = tmp_path / PREREG_V2
    preregistration.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT_ROOT / PREREG_V2, preregistration)
    return tmp_path, preregistration


def test_retrieval_manifest_is_exact_hash_only_and_license_conservative() -> None:
    for relative in (MANIFEST, SOURCE_V2, PREREG_V2):
        raw = (PROJECT_ROOT / relative).read_bytes()
        parsed = json.loads(raw)
        expected = (
            json.dumps(parsed, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        assert raw == expected

    manifest = load_retrieval_manifest(PROJECT_ROOT / MANIFEST)
    assert len(manifest.sources) == 12
    assert manifest.retrieval_methods[0].tool_version == "8.5.0"
    assert manifest.source_catalog_v1.path == SOURCE_V1.as_posix()
    validate_retrieval_manifest_against_source_catalog(manifest, PROJECT_ROOT / SOURCE_V1)

    jovian = {
        item.exact_url: (item.raw_response_byte_length, item.raw_response_sha256)
        for item in manifest.sources
        if item.snapshot_status is SnapshotStatus.CAPTURED_HASH_ONLY
    }
    assert jovian == EXPECTED_JOVIAN_CAPTURES

    human_design = tuple(
        item for item in manifest.sources if item.snapshot_status is SnapshotStatus.LICENSE_BLOCKED
    )
    assert len(human_design) == 4
    assert all(item.exact_url.startswith("https://human.design/") for item in human_design)
    assert all(item.raw_response_byte_length is None for item in human_design)
    assert all(item.raw_response_sha256 is None for item in human_design)
    assert all(item.repository_snapshot_path is None for item in manifest.sources)
    assert all(not item.terms.redistribution_allowed for item in manifest.sources)
    assert all(not item.terms.repository_snapshot_allowed for item in manifest.sources)


def test_v2_artifacts_are_deterministic_provenance_only_amendments() -> None:
    previous = load_preregistration(PROJECT_ROOT / PREREG_V1)
    amended = load_preregistration(PROJECT_ROOT / PREREG_V2)
    assert type(previous) is PreregistrationArtifact
    assert isinstance(amended, PreregistrationArtifactV2)
    assert previous.sha256() == "f9e372865d76d397275f3549737fe6e71ff8c941839a72186490ee32b487b271"
    assert_preregistration_provenance_only_equivalent(previous, amended)

    source_v2 = load_source_catalog_v2(PROJECT_ROOT / SOURCE_V2)
    assert sha256(source_v2.canonical_bytes() + b"\n").hexdigest() == (
        "b79d5cc939fbd35d2de7d6f1ad932ea8f4b625a22c9781b2975e043c52fcd765"
    )
    assert source_v2.provenance.claim == "prospective-new-not-historical-reconstruction"
    assert not source_v2.provenance_amendment.mapping_semantics_changed
    assert_source_catalog_provenance_only_equivalent(PROJECT_ROOT / SOURCE_V1, source_v2)

    raw: dict[str, Any] = json.loads((PROJECT_ROOT / PREREG_V2).read_text(encoding="utf-8"))
    raw["observations"][0]["behavioral_confidence"] = 0.5
    changed = PreregistrationArtifactV2.model_validate(raw)
    with pytest.raises(ValueError, match="changes frozen preregistration semantics"):
        assert_preregistration_provenance_only_equivalent(previous, changed)


def test_compiler_and_freeze_bind_complete_v2_provenance_chain(tmp_path: Path) -> None:
    root, preregistration = _copied_v2_repository(tmp_path)
    first_path = root / "mappings" / "compiled-first.json"
    second_path = root / "mappings" / "compiled-second.json"
    first = compile_model_b_v2_new(
        repository_root=root,
        preregistration_path=preregistration,
        compiled_output_path=first_path,
    )
    second = compile_model_b_v2_new(
        repository_root=root,
        preregistration_path=preregistration,
        compiled_output_path=second_path,
    )
    assert isinstance(first, CompiledModelArtifactV2)
    assert first_path.read_bytes() == second_path.read_bytes()
    assert first.retrieval_manifest.path == MANIFEST.as_posix()
    assert first.retrieval_manifest == second.retrieval_manifest

    receipt = freeze_model_b_v2_new(
        repository_root=root,
        preregistration_path=preregistration,
        compiled_artifact_path=first_path,
        freeze_receipt_output_path=root / "mappings" / "freeze.json",
        source_software_commit="a" * 40,
        source_software_tree="b" * 40,
        frozen_at_utc=datetime(2026, 8, 22, tzinfo=UTC),
    )
    assert isinstance(receipt, ModelFreezeReceiptV2)
    assert receipt.retrieval_manifest == first.retrieval_manifest
    assert receipt.previous_preregistration == first.previous_preregistration
    assert receipt.previous_source_catalog == first.previous_source_catalog
    assert receipt.source_catalog_artifact == first.source_catalog_artifact

    manifest_path = root / MANIFEST
    manifest_path.write_bytes(manifest_path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="bound artifact hash mismatch"):
        compile_model_b_v2_new(
            repository_root=root,
            preregistration_path=preregistration,
            compiled_output_path=root / "mappings" / "must-not-compile.json",
        )
