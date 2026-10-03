#!/usr/bin/env python3
"""Run the legacy Plan+Admission pipeline on the same synthetic triage cases.

This is a development benchmark with no participant source. Output is limited
to case labels, route IDs, phases, token counts, and timing.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

from cryptography.fernet import Fernet
from participant.domain import load_instrument
from participant.engine import Engine
from participant.store import Store

HERE = Path(__file__).resolve()
SYNTHETIC = HERE.with_name("benchmark_shadow_synthetic_quality.py")


def load_synthetic_module():
    spec = importlib.util.spec_from_file_location("shadow_synthetic_cases", SYNTHETIC)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    synthetic = load_synthetic_module()
    worker = synthetic.load_worker_module()
    with tempfile.TemporaryDirectory(prefix="legacy-synthetic-") as folder:
        root = Path(folder)
        instrument = load_instrument(worker.authority_copy(root / "authority"))
        provider = worker.CodexCliProvider()
        output = []
        for index, (label, state, expected) in enumerate(synthetic.cases(instrument), 1):
            store = Store(root / f"case-{index:04d}.sqlite3", Fernet.generate_key().decode())
            state["instrument_version"] = store.pin_instrument(instrument)
            token, current = store.create(state, 2)
            engine = Engine(store, provider, maximum_calls=12)
            before = len(current.get("calls", []))
            for _ in range(2):
                current = engine.advance(token)
                if current["phase"] != "ready":
                    break
            calls = [
                {
                    key: call.get(key)
                    for key in (
                        "stage",
                        "duration_seconds",
                        "prompt_tokens",
                        "completion_tokens",
                    )
                }
                for call in current.get("calls", [])[before:]
                if call.get("stage") in {"Plan", "Admission"}
            ]
            route_id = (
                (current.get("pending_question") or {}).get("route_id")
                if current["phase"] == "awaiting_answer"
                else None
            )
            row = {
                "case_id": f"case-{index:04d}",
                "label": label,
                "phase": current["phase"],
                "selected_route_id": route_id,
                "expected_selected_route_id": expected,
                "semantic_calls": calls,
                "semantic_duration_seconds": round(
                    sum(float(call.get("duration_seconds") or 0) for call in calls), 3
                ),
            }
            output.append(row)
            print(json.dumps(row, separators=(",", ":")), flush=True)
        print(
            json.dumps(
                {
                    "schema": "life-patterns-legacy-synthetic-quality-v1",
                    "case_count": len(output),
                    "cases": output,
                },
                separators=(",", ":"),
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
