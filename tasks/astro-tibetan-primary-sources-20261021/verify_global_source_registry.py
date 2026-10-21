#!/usr/bin/env python3
"""Global Tibetan documentary-source registry audit (T01–T50).

Annexes/tables do not create new historical annotation IDs.
This checks identity and provenance, not predictive validity.
"""
from pathlib import Path
import json

R = Path(__file__).resolve().parent
BATCH_IDS = (
    "T01","T02","T03","T04","T05","T07","T09","T11",
    "T13","T16","T18","T21","T23","T25","T27","T30",
    "T32","T34","T36","T38","T42","T44","T47","T49"
)
SPECIAL_NOTE_KEY = {"T02": "notes", "T25": "notes"}
EXPECTED_COUNT = 447
ids = []
detail = {}
sources = set()

for batch in BATCH_IDS:
    folder = R / "batches" / batch
    if batch == "T04":
        source_file = folder / "WHITE_BERYL_60_PROFILES_V1.json"
        data = json.loads(source_file.read_text(encoding="utf-8"))
        local_ids = [data["methodology_note"]["id"]]
        for profile in data["profiles"]:
            if not profile["reuses_prior_note"]:
                local_ids.append(profile["source_note_id"])
        assert len(local_ids) == 59, "T04 60 profiles must reuse 2 earlier records"
        sources.add("TIB-DORJE-2001")
    else:
        paths = sorted(folder.glob("*NOTES*.json"))
        if batch == "T07":
            paths = [folder / "WHITE_BERYL_NATAL_OMENS_AND_TRIPLES_V1.json"]
        assert len(paths) == 1, f"{batch} must have one source-note ledger, got {paths}"
        source_file = paths[0]
        data = json.loads(source_file.read_text(encoding="utf-8"))
        notes = data[SPECIAL_NOTE_KEY.get(batch, "source_notes")]
        local_ids = [record["id"] for record in notes]
        assert len(local_ids) == len(set(local_ids)), batch
        count_key = "source_note_count" if batch == "T03" else "note_count"
        assert len(local_ids) == data[count_key], batch
        for record in notes:
            assert record.get("source_id"), f"missing source witness in {batch}"
            sources.add(record["source_id"])
    ids += local_ids
    detail[batch] = len(local_ids)
assert len(ids) == EXPECTED_COUNT, f"count mismatch: {len(ids)}"
assert ids == [f"TIB-R{i:04d}" for i in range(1,EXPECTED_COUNT + 1)], (
    "noncontiguous registry, duplication or wrong ordering"
)
assert sources == {
    "TIB-DORJE-2001", "TIB-CORNU-1997", "TIB-HENNING-2007",
    "TIB-ERLEWINE-2007", "TIB-JANSON-2014"
}, sources
assert not list(R.rglob("*.pdf")), "copyrighted source PDF erroneously committed into reader folder"
assert sum(detail[b] for b in ("T36","T38","T42","T44","T47","T49")) == 123
assert sum(detail[b] for b in BATCH_IDS if b not in ("T36","T38","T42","T44","T47","T49")) == 324
print(f"TIBETAN_GLOBAL_SOURCE_ONLY_PASS: {EXPECTED_COUNT} contiguous documentary notes; "
      "123 added in T36–T50, 324 previously accepted; zero human successes claimed.")
print("BATCH_COUNTS:", " ".join(f"{key}:{value}" for key,value in detail.items()))
