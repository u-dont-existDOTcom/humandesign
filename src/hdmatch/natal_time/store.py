"""Append-only private storage namespace for natal-time evidence."""

from __future__ import annotations

from pathlib import Path

from hdmatch.experiments.canonical import load_json_bytes, write_new_canonical_json
from hdmatch.natal_time.models import EvidenceLineage
from hdmatch.natal_time.records import NatalTimeFreeze, NatalTimeManifest, NatalTimeResult


class NatalTimePrivateStore:
    """Store private natal records without sharing relationship storage paths."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self._intakes = self.root / "natal-time" / "intakes"
        self._scientific = self.root / "natal-time" / "scientific"

    def append_lineage(self, lineage: EvidenceLineage) -> Path:
        directory = self._intakes / lineage.lineage_id
        destination = directory / f"evidence-v{lineage.version:04d}.private.json"
        return write_new_canonical_json(destination, lineage)

    def load_latest_lineage(self, lineage_id: str) -> EvidenceLineage:
        directory = self._intakes / lineage_id
        candidates = sorted(directory.glob("evidence-v*.private.json"))
        if not candidates:
            raise KeyError(f"unknown natal-time lineage: {lineage_id}")
        return EvidenceLineage.model_validate(
            load_json_bytes(candidates[-1], require_canonical=True)
        )

    def append_manifest(self, manifest: NatalTimeManifest) -> Path:
        return write_new_canonical_json(
            self._scientific / manifest.manifest_id / "manifest.private.json", manifest
        )

    def append_freeze(self, manifest_id: str, freeze: NatalTimeFreeze) -> Path:
        return write_new_canonical_json(
            self._scientific / manifest_id / f"freeze-{freeze.freeze_id}.private.json", freeze
        )

    def append_result(self, manifest_id: str, result: NatalTimeResult) -> Path:
        return write_new_canonical_json(
            self._scientific / manifest_id / f"result-{result.result_id}.private.json", result
        )
