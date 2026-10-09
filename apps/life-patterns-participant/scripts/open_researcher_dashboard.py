#!/usr/bin/env python3
"""One-click researcher dashboard login with a private feedback snapshot fallback."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

from life_patterns_local_dashboard import (
    fetch_feedback,
    launch_browser,
    make_handoff,
    private_write,
    render_private_feedback,
)

CONFIG = Path.home() / ".config/life-patterns/dashboard-viewer.json"


def main() -> int:
    report = None
    bridge = None
    try:
        configuration = json.loads(CONFIG.read_text(encoding="utf-8"))
        report = Path(configuration["local_report"])
        feedback, key = fetch_feedback(configuration)
        private_write(report, render_private_feedback(feedback))
        bridge = make_handoff(configuration, key)
        try:
            launch_browser(bridge.as_uri())
            # The bridge contains a credential; remove it after browser navigation.
            time.sleep(25)
        finally:
            bridge.unlink(missing_ok=True)
        return 0
    except Exception:
        # No secret values are logged, shown or copied to the clipboard.
        message = (
            "The secure online dashboard did not open. "
            "Showing the most recently saved private feedback report instead."
        )
        if report is not None and report.exists():
            try:
                launch_browser(report.as_uri())
                return 0
            except Exception:
                pass
        print(message, file=sys.stderr)
        if os.getenv("WAYLAND_DISPLAY") or os.getenv("DISPLAY"):
            try:
                subprocess.run(
                    ["zenity", "--error", "--text=" + message],
                    timeout=60,
                    check=False,
                )
            except Exception:
                pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
