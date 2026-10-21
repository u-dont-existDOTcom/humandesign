#!/usr/bin/env python3
"""Independent deterministic verification of the Tibetan documentary-source lane.

No interpretation, human outcome validation, or copyrighted source bytes required.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "SOURCE_CATALOG_V1.json"
DATA = (
    ROOT / "batches/T01/SOURCE_NOTES_T01.json",
    ROOT / "batches/T02/SOURCE_NOTES_T02.json",
    ROOT / "batches/T03/SOURCE_NOTES_T03.json",
)
EXPECTED_COUNTS = (20, 6, 6)
EXPECTED_IDS = [f"TIB-R{i:04d}" for i in range(1, 33)]


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    sources = {entry["id"] for entry in catalog["materials"]}
    assert len(sources) == len(catalog["materials"]), "duplicate source identity"
    all_notes: list[dict] = []
    for path, count in zip(DATA, EXPECTED_COUNTS, strict=True):
        payload = json.loads(path.read_text(encoding="utf-8"))
        notes = payload.get("source_notes", payload.get("notes"))
        assert isinstance(notes, list) and len(notes) == count, path
        all_notes.extend(notes)
        assert payload.get("model_promotions", 0) == 0
        assert payload.get("actual_blind_human_predictions", payload.get("human_blind_predictions", 0)) == 0
    assert [entry["id"] for entry in all_notes] == EXPECTED_IDS, "noncontiguous or duplicate IDs"
    for item in all_notes:
        assert item["source_id"] in sources, item["id"]
        assert item["anchor"]["pdf_page_1based"] is None or item["anchor"]["pdf_page_1based"] > 0
        assert item["human_outcome_validated"] is False, item["id"]
        assert isinstance(item["paraphrase"], str) and len(item["paraphrase"]) >= 40
        assert isinstance(item["required_inputs"], list)
        assert item["dependency_family"], item["id"]
    integration = (ROOT / "CROSS_LANE_INTEGRATION_T01.md").read_text(encoding="utf-8")
    for required in ("Phugpa", "Tsurphu", "BaZi", "Jyotish", "Lilly", "blinded", "prereg"):
        assert required.casefold() in integration.casefold(), required
    pdfs = list(ROOT.rglob("*.pdf"))
    assert not pdfs, f"source PDFs should remain external, found: {pdfs}"
    print(f"TIBETAN_T01_TO_T03_SOURCE_ONLY_PASS: {len(all_notes)} contiguous notes, "
          f"{len(sources)} catalogued sources; no human validation or model promotion")


if __name__ == "__main__":
    main()
