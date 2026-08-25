#!/usr/bin/env python3
"""Build reusable AstroHD coarse ephemeris cache.

This cache is intended for broad candidate scans. Finalists and exact
boundaries must be recomputed directly with the production ephemeris engine.

Production policy: verified Swiss Ephemeris `.se1` files only. Any Moshier
fallback is a hard error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import math
import os
import struct
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import swisseph as swe

BODIES = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
    "true_node": swe.TRUE_NODE,
}
STEPS_HOURS = {
    "moon": 1,
    "sun": 3,
    "mercury": 3,
    "venus": 3,
    "mars": 3,
    "true_node": 3,
    "jupiter": 6,
    "saturn": 6,
    "uranus": 12,
    "neptune": 12,
    "pluto": 12,
}
FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED
Q = 100_000  # 1e-5 degree
REQUIRED_EPHEMERIS_FILES = ("sepl_18.se1", "semo_18.se1")


def jd(dt: datetime) -> float:
    h = dt.hour + dt.minute / 60 + dt.second / 3600
    return swe.julday(dt.year, dt.month, dt.day, h, swe.GREG_CAL)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def calc_longitude(jd_ut: float, body_id: int) -> float:
    xx, retflags = swe.calc_ut(jd_ut, body_id, FLAGS)
    used = retflags & swe.FLG_EPHMASK
    if used != swe.FLG_SWIEPH:
        raise RuntimeError(
            "EPHEMERIS_FALLBACK: requested SWIEPH but "
            f"body={body_id} jd={jd_ut} returned_mode={used} retflags={retflags}"
        )
    return xx[0] % 360


def encode(longitudes: np.ndarray, step_hours: int) -> bytes:
    uw = np.rad2deg(np.unwrap(np.deg2rad(longitudes)))
    q = np.rint(uw * Q).astype(np.int64)
    d = np.diff(q)
    dd = np.diff(d).astype("<i4")
    raw = struct.pack("<qiId", int(q[0]), int(d[0]), len(q), float(step_hours)) + dd.tobytes()
    return lzma.compress(raw, preset=9 | lzma.PRESET_EXTREME)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    ephe_dir = repo_root / "data" / "ephemeris"
    missing = [name for name in REQUIRED_EPHEMERIS_FILES if not (ephe_dir / name).is_file()]
    if missing:
        raise SystemExit(
            "Missing production Swiss Ephemeris files: "
            + ", ".join(missing)
            + ". Run: python scripts/fetch_swisseph_ephemeris.py"
        )

    swe.set_ephe_path(str(ephe_dir))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    start = datetime(1926, 5, 15, 10, 42, tzinfo=timezone.utc)
    end = datetime(2026, 8, 24, 10, 42, tzinfo=timezone.utc)
    sj, ej = jd(start), jd(end)

    # Fail closed before doing expensive cache work.
    for probe_jd in (sj, (sj + ej) / 2, ej):
        for body_id in BODIES.values():
            calc_longitude(probe_jd, body_id)

    ephemeris_files = {
        name: {
            "bytes": (ephe_dir / name).stat().st_size,
            "sha256": sha256(ephe_dir / name),
        }
        for name in REQUIRED_EPHEMERIS_FILES
    }

    manifest = {
        "version": "astrohd-generic-ephemeris-cache-v2-swieph",
        "start_utc": start.isoformat(),
        "end_utc": end.isoformat(),
        "start_jd": sj,
        "end_jd": ej,
        "ephemeris_requested": "SWIEPH",
        "ephemeris_returned": "SWIEPH",
        "ephemeris_files": ephemeris_files,
        "flags": int(FLAGS),
        "node": "true",
        "longitude_quantization_deg": 1e-5,
        "codec": "unwrapped longitude -> 1e-5deg integer -> second differences -> XZ extreme",
        "bodies": {},
    }

    for name, body_id in BODIES.items():
        step = STEPS_HOURS[name]
        n = int(math.floor((ej - sj) * 24 / step)) + 1
        values = np.empty(n, dtype=np.float64)
        for i in range(n):
            values[i] = calc_longitude(sj + i * step / 24, body_id)
        payload = encode(values, step)
        fn = f"{name}.d2xz"
        target = out / fn
        target.write_bytes(payload)
        manifest["bodies"][name] = {
            "step_hours": step,
            "n": n,
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }

    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    decoder = '''#!/usr/bin/env python3\nimport lzma, struct, numpy as np\ndef decode(path):\n    raw=lzma.decompress(open(path,"rb").read()); q0,d1,n,step=struct.unpack("<qiId",raw[:24]); dd=np.frombuffer(raw[24:],dtype="<i4").astype(np.int64); d=np.empty(n-1,dtype=np.int64); d[0]=d1\n    if n>2: d[1:]=d1+np.cumsum(dd)\n    q=np.empty(n,dtype=np.int64); q[0]=q0; q[1:]=q0+np.cumsum(d); return ((q/1e5)%360).astype(np.float64),step\ndef interpolate(path,start_jd,target_jd):\n    a,step=decode(path); x=(np.asarray(target_jd)-start_jd)*24/step; i=np.floor(x).astype(int); f=x-i; i=np.clip(i,0,len(a)-2); b=a[i]; c=a[i+1]; delta=((c-b+180)%360)-180; return (b+f*delta)%360\n'''
    (out / "decode_cache.py").write_text(decoder, encoding="utf-8")

    readme = '''# AstroHD generic ephemeris cache v2 (SWIEPH)\n\nReusable coarse-scan longitude cache for HD / Western / AstroHD reverse matching. It starts ~101 days before the declared 100-year scan so HD Design times are covered. Houses are intentionally not cached because they are birthplace-specific and cheap to calculate.\n\nSampling: Moon 1h; Sun/Mercury/Venus/Mars/true Node 3h; Jupiter/Saturn 6h; Uranus/Neptune/Pluto 12h. Every calculation requests SWIEPH and checks returned ephemeris flags; any Moshier fallback aborts the build. Finalists and exact boundaries must be recalculated directly with the production ephemeris rather than trusted to interpolation.\n'''
    (out / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
