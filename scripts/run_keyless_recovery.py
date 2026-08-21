#!/usr/bin/env python3
"""Execute the fixed claim-grade keyless recovery wrapper from a source checkout."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

main = importlib.import_module("hdmatch.runtime.keyless_boundary").main


if __name__ == "__main__":
    raise SystemExit(main())
