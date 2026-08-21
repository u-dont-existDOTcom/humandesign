#!/usr/bin/env python3
"""Build/check the provenance-only MODEL-B-DETAILED-V2-NEW V2 amendment.

This script never copies external page bodies into the repository.  With
``--verify-capture-dir`` it verifies the ephemeral Jovian response bytes used
to create the hash-only retrieval records and inspects headers for all records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from hdmatch.model_b_v2_new.artifacts import (
    PreregistrationArtifact,
    PreregistrationArtifactV2,
)
from hdmatch.model_b_v2_new.provenance import (
    RetrievalManifest,
    SourceCatalogArtifactV2,
    assert_preregistration_provenance_only_equivalent,
    assert_source_catalog_provenance_only_equivalent,
    validate_retrieval_manifest_against_source_catalog,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_V1 = Path("reference/prospective/model_b_detailed_v2_new_sources_v1.json")
PREREG_V1 = Path("reference/prospective/model_b_detailed_v2_new_preregistration_v1.json")
RETRIEVAL_V1 = Path(
    "reference/prospective/model_b_detailed_v2_new_source_retrieval_manifest_v1.json"
)
SOURCE_V2 = Path("reference/prospective/model_b_detailed_v2_new_sources_v2.json")
PREREG_V2 = Path("reference/prospective/model_b_detailed_v2_new_preregistration_v2.json")

AMENDED_AT_UTC = "2026-08-21T22:20:18Z"
CURL_VERSION = "8.5.0"
JOVIAN_TERMS = "https://jovianarchive.com/pages/terms-and-conditions"
HUMAN_DESIGN_TERMS = "https://human.design/about-us/terms-and-conditions"


CAPTURE_FACTS: tuple[dict[str, object], ...] = (
    {
        "source_id": "SRC-P1-MENTAL-STREAMS",
        "url": "https://jovianarchive.com/blogs/chart-interpretations-components/the-mental-streams",
        "stem": "mental_streams",
        "accessed_at_utc": "2026-08-21T22:08:56Z",
        "bytes": 880282,
        "sha256": "3869896f5b17460c2a5207150acde0d5e7dc29a8c05a6a538a5fa6fe29bdb7d2",
        "etag": (
            '"page_cache:87249846576:BlogArticleDetailsController:'
            '2453ebd363aed6a098d17b3bcf628a32:9928cb3b4a1cdcafeb1b95555d53afb6"'
        ),
    },
    {
        "source_id": "SRC-P1-LOGIC-PERFECTION",
        "url": "https://jovianarchive.com/blogs/chart-interpretations-components/logic-and-perfection",
        "stem": "logic_perfection",
        "accessed_at_utc": "2026-08-21T22:08:56Z",
        "bytes": 875614,
        "sha256": "a6d8a207cba2a1d9a71d7a82b7ee14d452a2be2edf06cdbd2601167d3200eeb5",
        "etag": (
            '"page_cache:87249846576:BlogArticleDetailsController:'
            '20b4aaa9cfce59e55b00a4d65292b6aa:7a697a162b49a14e70b5860f2d514a37"'
        ),
    },
    {
        "source_id": "SRC-P1-GATES-FEAR-18-28",
        "url": "https://jovianarchive.com/blogs/chart-interpretations-components/the-gates-of-fear-18-28",
        "stem": "gates_fear_18_28",
        "accessed_at_utc": "2026-08-21T22:08:57Z",
        "bytes": 876963,
        "sha256": "0eae5cc15082568767f9d1a3a9c3978d18925d5556afc08a2c1dd5e7fd2e68fc",
        "etag": (
            '"page_cache:87249846576:BlogArticleDetailsController:'
            '27ae1ea19278c1af465b8317326cd0f3:f042d4079abdc65c74cd6d83f9ed7bb6"'
        ),
    },
    {
        "source_id": "SRC-P2-CHANNELS-LIFE-FORCE",
        "url": "https://jovianarchive.com/pages/channels-in-human-design-the-life-force",
        "stem": "channels_life_force",
        "accessed_at_utc": "2026-08-21T22:08:58Z",
        "bytes": 588323,
        "sha256": "c928d9848c13d080c13a32253d26ee0e649c09a0594236d21134a5a1bd8b76bb",
        "etag": (
            '"page_cache:87249846576:PageDetailsController:'
            '3121259ad4969d4395ed4a609d9cd5b7:69ff20784e7c0f27657ae54604289eb8"'
        ),
    },
    {
        "source_id": "SRC-P2-PLUTO61",
        "url": "https://jovianarchive.com/blogs/transits-global-cycles/how-pluto-in-gate-61-affects-you-q3-2021",
        "stem": "pluto61",
        "accessed_at_utc": "2026-08-21T22:08:56Z",
        "bytes": 878755,
        "sha256": "27a4f08723c624a6e88d16326906ffcd57fc817f11fd9bdf482cb876a66f63c6",
        "etag": (
            '"page_cache:87249846576:BlogArticleDetailsController:'
            'f7fd08c64767a34c9bf99588457c2496:8f71a3f499508f068003f17d08535b57"'
        ),
    },
    {
        "source_id": "SRC-S1-GATES",
        "url": "https://human.design/the-human-design-system/gates",
        "stem": "human_design_gates",
        "accessed_at_utc": "2026-08-21T22:08:58Z",
    },
    {
        "source_id": "SRC-S1-CHANNELS",
        "url": "https://human.design/the-human-design-system/channels",
        "stem": "human_design_channels",
        "accessed_at_utc": "2026-08-21T22:09:19Z",
    },
    {
        "source_id": "SRC-S1-PROVENANCE",
        "url": "https://human.design/about-us/richard-beaumont",
        "stem": "human_design_richard_beaumont",
        "accessed_at_utc": "2026-08-21T22:09:16Z",
    },
    {
        "source_id": "SRC-S1-PROVENANCE",
        "url": "https://human.design/the-human-design-system",
        "stem": "human_design_system",
        "accessed_at_utc": "2026-08-21T22:09:19Z",
    },
    {
        "source_id": "SRC-S2-CHANNELS-RELATIONSHIPS",
        "url": "https://jovianarchive.com/blogs/chart-interpretations-components/how-channels-shape-your-energy-flow-and-relationships",
        "stem": "rh_channels_relationships",
        "accessed_at_utc": "2026-08-21T22:09:17Z",
        "bytes": 890296,
        "sha256": "5ddf3bf57026d580e1abc63c9fd44125f5e18c9b1f1e8f333e80c7d4988657bb",
        "etag": (
            '"page_cache:87249846576:BlogArticleDetailsController:'
            '68c21c01f57f00b591c4090de614eab2:abb9fd9115fb6def633f6ea9ac5611ae"'
        ),
    },
    {
        "source_id": "SRC-S2-DEFINITION",
        "url": "https://jovianarchive.com/blogs/human-design-basics/what-your-definition-says-about-you-in-human-design",
        "stem": "rh_definition",
        "accessed_at_utc": "2026-08-21T22:09:15Z",
        "bytes": 887821,
        "sha256": "710986370ccdafc29da2ee9a5acaf82c0657f3dfac62d35ee3d1cfa2a6de60ee",
        "etag": (
            '"page_cache:87249846576:BlogArticleDetailsController:'
            'd4a022cdc88b35b2a4c601e76741162c:c5ffca559a6d2046f856c3288766893e"'
        ),
    },
    {
        "source_id": "SRC-S2-PLANETARY-ACCENTS",
        "url": "https://jovianarchive.com/blogs/chart-interpretations-components/planetary-accents-in-human-design",
        "stem": "planetary_accents",
        "accessed_at_utc": "2026-08-21T22:09:17Z",
        "bytes": 902619,
        "sha256": "e5dace190723f39832d3a46e1d8f28bf9234ba5f2665aa271d1ccb391cc9a0eb",
        "etag": (
            '"page_cache:87249846576:BlogArticleDetailsController:'
            'ab5b4997bf0c3d4d92e3c80e306963bb:80e132686831fbb5e5ebf6cd145b7822"'
        ),
    },
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _binding(role: str, path: Path) -> dict[str, str]:
    return {"role": role, "path": path.as_posix(), "sha256": _sha256(ROOT / path)}


def _source_lookup(source_v1: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["source_id"]: item for item in source_v1["source_catalog"]}


def _terms(url: str) -> dict[str, object]:
    if url.startswith("https://jovianarchive.com/"):
        return {
            "capture_basis": (
                "One-time internal provenance verification; only bibliographic facts, "
                "frozen paraphrases, response size, and an exact hash are retained."
            ),
            "checked_on": "2026-08-21",
            "constraints": (
                "Individual noncommercial access does not grant republication or database "
                "redistribution; the captured body remains external and is not committed."
            ),
            "redistribution_allowed": False,
            "repository_snapshot_allowed": False,
            "terms_url": JOVIAN_TERMS,
        }
    return {
        "capture_basis": (
            "Reachability and response metadata were checked under private/internal-use "
            "constraints; no content bytes or content hash are retained in this manifest."
        ),
        "checked_on": "2026-08-21",
        "constraints": (
            "Automated extraction and network redistribution restrictions make a repository "
            "snapshot or published content hash indefensible without written permission."
        ),
        "redistribution_allowed": False,
        "repository_snapshot_allowed": False,
        "terms_url": HUMAN_DESIGN_TERMS,
    }


def build_artifacts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_v1 = json.loads((ROOT / SOURCE_V1).read_text(encoding="utf-8"))
    prereg_v1 = json.loads((ROOT / PREREG_V1).read_text(encoding="utf-8"))
    sources = _source_lookup(source_v1)
    url_counts = {
        source_id: len(source["url"].split(" | ")) for source_id, source in sources.items()
    }
    url_indexes: dict[str, int] = {}

    retrievals: list[dict[str, Any]] = []
    for fact in CAPTURE_FACTS:
        source_id = str(fact["source_id"])
        source = sources[source_id]
        url_indexes[source_id] = url_indexes.get(source_id, 0) + 1
        count = url_counts[source_id]
        locator = (
            source_id if count == 1 else f"{source_id}:url-{url_indexes[source_id]}-of-{count}"
        )
        proposition_ids = [
            item["proposition_id"] for item in source["frozen_paraphrased_propositions"]
        ]
        is_jovian = str(fact["url"]).startswith("https://jovianarchive.com/")
        suffix = "" if count == 1 else f"-URL-{url_indexes[source_id]}"
        retrievals.append(
            {
                "accessed_at_utc": fact["accessed_at_utc"],
                "etag": fact.get("etag") if is_jovian else None,
                "exact_url": fact["url"],
                "http_status": 200,
                "locator": locator,
                "proposition_ids": proposition_ids,
                "raw_response_byte_length": fact.get("bytes") if is_jovian else None,
                "raw_response_sha256": fact.get("sha256") if is_jovian else None,
                "repository_snapshot_path": None,
                "response_content_encoding": "br",
                "response_mime_type": "text/html; charset=utf-8",
                "retrieval_id": f"RETRIEVAL-{source_id}{suffix}",
                "retrieval_method_id": "curl-http-get-compressed-v1",
                "snapshot_status": (
                    "captured-hash-only-no-repository-snapshot"
                    if is_jovian
                    else "license-blocked-no-snapshot-or-content-hash"
                ),
                "source_id": source_id,
                "terms": _terms(str(fact["url"])),
            }
        )

    manifest: dict[str, Any] = {
        "created_at_utc": AMENDED_AT_UTC,
        "manifest_id": "MODEL-B-DETAILED-V2-NEW-SOURCE-RETRIEVAL-V1",
        "model_id": "MODEL-B-DETAILED-V2-NEW",
        "retrieval_methods": [
            {
                "method_id": "curl-http-get-compressed-v1",
                "raw_response_representation": (
                    "exact decoded HTTP entity-body bytes written by curl after content decoding"
                ),
                "repository_body_storage": "forbidden",
                "request_profile": (
                    "HTTP GET with --compressed; response headers and decoded entity body "
                    "captured ephemerally"
                ),
                "tool": "curl",
                "tool_version": CURL_VERSION,
            }
        ],
        "schema_version": "model-b-v2-new-source-retrieval-manifest-v1",
        "source_catalog_v1": _binding("previous_source_catalog", SOURCE_V1),
        "sources": retrievals,
    }
    manifest_model = RetrievalManifest.model_validate(manifest)
    validate_retrieval_manifest_against_source_catalog(manifest_model, ROOT / SOURCE_V1)
    manifest_bytes = _canonical_bytes(manifest_model.model_dump(mode="json", exclude_none=False))
    manifest_binding = {
        "role": "source_retrieval_manifest",
        "path": RETRIEVAL_V1.as_posix(),
        "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
    }

    source_v2 = deepcopy(source_v1)
    source_v2["artifact_id"] = "MODEL-B-DETAILED-V2-NEW-SOURCES-V2"
    source_v2["schema_version"] = "model-b-detailed-v2-new-sources-v2"
    source_v2["provenance_amendment"] = {
        "amendment_scope": (
            "external-source-retrieval-metadata-only; no behavioral or scoring changes"
        ),
        "mapping_semantics_changed": False,
        "previous_source_catalog": _binding("previous_source_catalog", SOURCE_V1),
        "retrieval_manifest": manifest_binding,
    }
    source_v2_model = SourceCatalogArtifactV2.model_validate(source_v2)
    assert_source_catalog_provenance_only_equivalent(ROOT / SOURCE_V1, source_v2_model)
    source_v2_bytes = _canonical_bytes(source_v2_model.model_dump(mode="json", exclude_none=True))
    source_v2_binding = {
        "role": "source_catalog",
        "path": SOURCE_V2.as_posix(),
        "sha256": hashlib.sha256(source_v2_bytes).hexdigest(),
    }

    prereg_v2 = deepcopy(prereg_v1)
    prereg_v2["schema_version"] = "model-b-v2-new-preregistration-v2"
    prereg_v2["compiler_version"] = "model-b-v2-new-compiler-v2"
    prereg_v2["provenance_amended_at_utc"] = AMENDED_AT_UTC
    prereg_v2["previous_preregistration"] = _binding("previous_preregistration", PREREG_V1)
    prereg_v2["previous_source_catalog"] = _binding("previous_source_catalog", SOURCE_V1)
    prereg_v2["source_catalog_artifact"] = source_v2_binding
    prereg_v2["retrieval_manifest"] = manifest_binding
    for source in prereg_v2["source_catalog"]:
        if source["public_url"] is not None:
            source["local_path"] = SOURCE_V2.as_posix()
            source["local_sha256"] = source_v2_binding["sha256"]
    prereg_v2_model = PreregistrationArtifactV2.model_validate(prereg_v2)
    prereg_v1_model = PreregistrationArtifact.model_validate(prereg_v1)
    assert_preregistration_provenance_only_equivalent(prereg_v1_model, prereg_v2_model)

    return (
        manifest_model.model_dump(mode="json", exclude_none=False),
        source_v2_model.model_dump(mode="json", exclude_none=True),
        prereg_v2_model.model_dump(mode="json", exclude_none=False),
    )


def verify_capture_dir(capture_dir: Path) -> None:
    """Verify ephemeral captures without hashing Human.Design response bodies."""

    for fact in CAPTURE_FACTS:
        stem = str(fact["stem"])
        header_path = capture_dir / f"{stem}.headers"
        headers = header_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^HTTP/2 200\s*$", headers):
            raise ValueError(f"capture did not return HTTP 200: {stem}")
        if "content-type: text/html; charset=utf-8" not in headers.casefold():
            raise ValueError(f"capture MIME mismatch: {stem}")
        if str(fact["url"]).startswith("https://jovianarchive.com/"):
            body_path = capture_dir / f"{stem}.body"
            if body_path.stat().st_size != fact["bytes"]:
                raise ValueError(f"capture body-size mismatch: {stem}")
            if _sha256(body_path) != fact["sha256"]:
                raise ValueError(f"capture body-hash mismatch: {stem}")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--verify-capture-dir", type=Path)
    args = parser.parse_args()

    if args.verify_capture_dir is not None:
        verify_capture_dir(args.verify_capture_dir.resolve())
    values = build_artifacts()
    paths = (RETRIEVAL_V1, SOURCE_V2, PREREG_V2)
    for path, value in zip(paths, values, strict=True):
        expected = _canonical_bytes(value)
        target = ROOT / path
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(expected)
        elif not target.is_file() or target.read_bytes() != expected:
            raise SystemExit(f"provenance artifact is missing or stale: {path}")
        print(f"{path} {hashlib.sha256(expected).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
