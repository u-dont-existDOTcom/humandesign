#!/usr/bin/env python3
"""Build reusable AstroHD coarse ephemeris cache.

This cache is intended for broad candidate scans. Finalists and exact
boundaries must be recomputed directly with the production ephemeris engine.
"""
from __future__ import annotations
import argparse, hashlib, json, lzma, math, os, struct
from datetime import datetime, timezone
import numpy as np
import swisseph as swe

BODIES = {
    "sun": swe.SUN, "moon": swe.MOON, "mercury": swe.MERCURY,
    "venus": swe.VENUS, "mars": swe.MARS, "jupiter": swe.JUPITER,
    "saturn": swe.SATURN, "uranus": swe.URANUS, "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO, "true_node": swe.TRUE_NODE,
}
STEPS_HOURS = {
    "moon": 1, "sun": 3, "mercury": 3, "venus": 3, "mars": 3,
    "true_node": 3, "jupiter": 6, "saturn": 6,
    "uranus": 12, "neptune": 12, "pluto": 12,
}
FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED
Q = 100_000  # 1e-5 degree

def jd(dt: datetime) -> float:
    h = dt.hour + dt.minute / 60 + dt.second / 3600
    return swe.julday(dt.year, dt.month, dt.day, h, swe.GREG_CAL)

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
    out = args.out
    os.makedirs(out, exist_ok=True)
    start = datetime(1926, 5, 15, 10, 42, tzinfo=timezone.utc)
    end = datetime(2026, 8, 24, 10, 42, tzinfo=timezone.utc)
    sj, ej = jd(start), jd(end)
    manifest = {
        "version": "astrohd-generic-ephemeris-cache-v1",
        "start_utc": start.isoformat(), "end_utc": end.isoformat(),
        "start_jd": sj, "end_jd": ej,
        "ephemeris": "Swiss Ephemeris library with explicit Moshier flags",
        "flags": int(FLAGS), "node": "true",
        "longitude_quantization_deg": 1e-5,
        "codec": "unwrapped longitude -> 1e-5deg integer -> second differences -> XZ extreme",
        "bodies": {},
    }
    for name, body_id in BODIES.items():
        step = STEPS_HOURS[name]
        n = int(math.floor((ej - sj) * 24 / step)) + 1
        values = np.empty(n, dtype=np.float64)
        for i in range(n):
            values[i] = swe.calc_ut(sj + i * step / 24, body_id, FLAGS)[0][0] % 360
        payload = encode(values, step)
        fn = f"{name}.d2xz"
        with open(os.path.join(out, fn), "wb") as f:
            f.write(payload)
        manifest["bodies"][name] = {
            "step_hours": step, "n": n, "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2); f.write("\n")
    decoder = '''#!/usr/bin/env python3\nimport lzma, struct, numpy as np\ndef decode(path):\n    raw=lzma.decompress(open(path,"rb").read()); q0,d1,n,step=struct.unpack("<qiId",raw[:24]); dd=np.frombuffer(raw[24:],dtype="<i4").astype(np.int64); d=np.empty(n-1,dtype=np.int64); d[0]=d1\n    if n>2: d[1:]=d1+np.cumsum(dd)\n    q=np.empty(n,dtype=np.int64); q[0]=q0; q[1:]=q0+np.cumsum(d); return ((q/1e5)%360).astype(np.float64),step\ndef interpolate(path,start_jd,target_jd):\n    a,step=decode(path); x=(np.asarray(target_jd)-start_jd)*24/step; i=np.floor(x).astype(int); f=x-i; i=np.clip(i,0,len(a)-2); b=a[i]; c=a[i+1]; delta=((c-b+180)%360)-180; return (b+f*delta)%360\n'''
    with open(os.path.join(out, "decode_cache.py"), "w", encoding="utf-8") as f:
        f.write(decoder)
    readme = '''# AstroHD generic ephemeris cache v1\n\nReusable coarse-scan longitude cache for HD / Western / AstroHD reverse matching. It starts ~101 days before the declared 100-year scan so HD Design times are covered. Houses are intentionally not cached because they are birthplace-specific and cheap to calculate.\n\nSampling: Moon 1h; Sun/Mercury/Venus/Mars/true Node 3h; Jupiter/Saturn 6h; Uranus/Neptune/Pluto 12h. Finalists and exact boundaries must be recalculated directly with the production ephemeris rather than trusted to interpolation.\n'''
    with open(os.path.join(out, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
if __name__ == "__main__": main()
