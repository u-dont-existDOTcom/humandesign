#!/usr/bin/env python3
"""Bounded Wine UI helper. Complete stdout is drained; failures never open dialogs.

Use only a verified Mastro control handle from a fresh `list`. The helper reads
ordinary window controls and ListView UI text; it does not inspect app databases.
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prefix", type=Path, required=True)
    p.add_argument("--compile", action="store_true")
    p.add_argument("operation", choices=("list", "items", "clipboard", "click", "set", "key", "shortcut", "mouse", "close"))
    p.add_argument("arguments", nargs="*")
    args = p.parse_args()
    if args.operation not in {"list", "items"} and (not os.environ.get("MASTRO_BACKGROUND_DISPLAY") or os.environ.get("MASTRO_BACKGROUND_DISPLAY") != os.environ.get("DISPLAY")):
        raise RuntimeError("UI changes require the isolated background display; foreground automation is disabled")
    tools = Path(__file__).resolve().parent
    env = dict(os.environ, WINEPREFIX=str(args.prefix.resolve()), WINEDEBUG="-all")

    def wine(parts):
        result = subprocess.run(["wine", *parts], env=env, capture_output=True, timeout=15)
        output = (result.stdout + result.stderr).decode("cp1252", errors="replace")
        if result.returncode:
            raise RuntimeError(output or f"Wine returned {result.returncode}")
        return output

    helper = tools / "OperatorSafe.exe"
    if args.compile or not helper.exists():
        windows_path = lambda path: "Z:" + str(path).replace("/", "\\")
        wine([r"C:\windows\Microsoft.NET\Framework\v3.5\csc.exe", "/nologo",
              "/r:System.Drawing.dll", "/r:System.Windows.Forms.dll", "/out:" + windows_path(helper), windows_path(tools / "WineControls.cs")])
    output = wine([str(helper), args.operation, *args.arguments])
    # A text snapshot after each mutation detects any modal failure without
    # relying on the owner to provide screenshots. Never click unknown dialogs.
    state = output if args.operation == "list" and not args.arguments else wine([str(helper), "list"])
    if "Application Error" in state or "could not be handled" in state:
        raise RuntimeError("Application error detected; stop UI actions and inspect:\n" + state[:3000])
    sys.stdout.write(output)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
