from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from hdmatch.util import sha256_json
from scripts.audit_natal_time_real_engine_identity import build_packet

PROJECT_ROOT = Path(__file__).parents[2]


def test_real_engine_identity_packet_is_pinned_synthetic_and_self_hashing() -> None:
    ephemeris = PROJECT_ROOT / "data" / "ephemeris"
    if not (ephemeris / "sepl_18.se1").is_file() or not (ephemeris / "semo_18.se1").is_file():
        pytest.skip("verified local Swiss ephemeris files are unavailable")

    packet = build_packet(PROJECT_ROOT, "synthetic-real-engine-commit", ephemeris)

    assert packet["synthetic_only"] is True
    assert packet["qualification_status"] == "pending_pro_review"
    assert packet["canonical_engine"]["selection_status"] == ("unambiguous_repository_default")
    assert packet["ephemeris"]["fallback_permitted"] is False
    assert packet["mandala_equality_probe"]["equality_enters_new_half_open_sector"] is True
    assert packet["claim_limits"]["production_qualification"] is False
    assert packet["field_inventory"]["complete_against_runtime_dataclasses"] is True
    unhashed = deepcopy(packet)
    expected = unhashed.pop("packet_sha256")
    assert expected == sha256_json(unhashed)
