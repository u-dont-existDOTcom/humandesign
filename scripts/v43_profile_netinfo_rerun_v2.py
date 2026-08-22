from __future__ import annotations

import json
import os
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import swisseph as swe

import swieph_ab_rerun as base
import v43_profile_netinfo_rerun as runner


def load_frozen_model() -> tuple[dict, Path, Path]:
    base_path = Path(
        os.environ.get(
            "HD_MAPPING",
            "reference/core/profile_v3_6_v43_mapping_frozen_2026_08_22.json",
        )
    ).resolve()
    overlay_path = Path(
        os.environ.get(
            "HD_MAPPING_OVERLAY",
            "reference/core/profile_v3_6_v43_mapping_overlay_v2_2026_08_22.json",
        )
    ).resolve()
    model = json.loads(base_path.read_text(encoding="utf-8"))
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    by_id = {mapping["id"]: mapping for mapping in model["mappings"]}
    for mapping_id, patch in overlay.get("overrides", {}).items():
        if mapping_id not in by_id:
            raise KeyError(f"overlay override references missing mapping: {mapping_id}")
        by_id[mapping_id].update(patch)
    existing = set(by_id)
    for mapping in overlay.get("add_mappings", []):
        if mapping["id"] in existing:
            raise ValueError(f"duplicate overlay mapping id: {mapping['id']}")
        model["mappings"].append(mapping)
        existing.add(mapping["id"])
    model["audit_overlay"] = {
        "schema": overlay["schema"],
        "status": overlay["status"],
        "base_mapping": overlay["base_mapping"],
    }
    return model, base_path, overlay_path


def main() -> None:
    model, base_mapping, overlay_path = load_frozen_model()
    target_path = Path(
        os.environ.get("HD_TARGET", "reference/core/behavioral_target_combined_v3_6.md")
    ).resolve()
    print("BASE_MAPPING_SHA256", runner.sha256_path(base_mapping), flush=True)
    print("OVERLAY_SHA256", runner.sha256_path(overlay_path), flush=True)
    print("TARGET_SHA256", runner.sha256_path(target_path), flush=True)
    print("MAPPING_COUNT", len(model["mappings"]), flush=True)

    ephe = Path(os.environ.get("EPHE_PATH", "data/ephemeris")).resolve()
    swe.set_ephe_path(str(ephe))
    print("EPHE_PATH", ephe, flush=True)
    for filename in ["sepl_18.se1", "semo_18.se1"]:
        path = ephe / filename
        if not path.exists():
            raise RuntimeError(f"missing {path}")
        print("EPHE_FILE", filename, path.stat().st_size, runner.sha256_path(path), flush=True)
    for dt in [base.START_DT, datetime(1985, 1, 29, tzinfo=timezone.utc), base.END_DT]:
        jd = base.jd_from_dt(dt)
        for name in ["sun", "moon", "mars", "pluto"]:
            base.lon_speed(jd, base.BODY_IDS[name])
        print("SWIEPH_PROBE_OK", dt.isoformat(), flush=True)

    t0 = time.time()
    states = runner.build_exact_states()
    prevalence, min_parent_duration = runner.build_prevalence(states, model)
    print(
        "PREVALENCE_POLICY",
        json.dumps(
            {
                "median_state_hours": round(statistics.median(s["dur"] for s in states) * 24, 6),
                "minimum_parent_state_equivalents": model["constants"]["minimum_parent_state_equivalents"],
                "minimum_parent_duration_days": round(min_parent_duration, 6),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    print("PREVALENCE_TABLE")
    for mapping_id in sorted(prevalence):
        p = prevalence[mapping_id]
        print(
            json.dumps(
                {
                    "id": mapping_id,
                    "p": round(p["prevalence"], 9),
                    "bits": round(
                        runner.information_bits(
                            p["prevalence"], model["constants"]["information_cap_bits"]
                        ),
                        6,
                    ),
                    "denominator_days": round(p["denominator_days"], 6),
                    "backoff_steps": p["backoff_steps"],
                    "parents_used": p["parents_used"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    runner.run_variant(states, model, prevalence, False, "NO_POST_SELECTION_CARRIERS_V2")
    runner.run_variant(states, model, prevalence, True, "BEST_CURRENT_V3_6_V2")
    print("DONE", round(time.time() - t0, 1), flush=True)


if __name__ == "__main__":
    main()
