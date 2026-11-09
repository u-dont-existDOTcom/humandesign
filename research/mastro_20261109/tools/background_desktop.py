#!/usr/bin/env python3
"""Create a private local X display and a separate, reusable Wine prefix snapshot.

No display is attached to the normal desktop, no network listener is opened, and
the original prefix/process is not stopped or modified. This isolates UI, not
research secrets from other processes running under the same Linux account.
"""
import argparse
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import time
import hashlib


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-prefix", type=Path, required=True)
    p.add_argument("--runtime-root", type=Path, required=True)
    p.add_argument("--xvfb", type=Path, required=True)
    p.add_argument("--display", default=":91")
    a = p.parse_args()
    source, root = a.source_prefix.resolve(), a.runtime_root.resolve()
    if root.is_relative_to(source) or source.is_relative_to(root):
        raise ValueError("Independent source and automation prefix paths required")
    number = int(a.display.removeprefix(":"))
    if number < 50 or Path(f"/tmp/.X11-unix/X{number}").exists():
        raise ValueError("Choose an unused high-numbered display")
    if str(root).startswith("/mnt/hdd/"):
        subprocess.run(["findmnt", "--mountpoint", "/mnt/hdd"], check=True, stdout=subprocess.DEVNULL)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    if (root / "session.json").exists():
        previous = json.loads((root / "session.json").read_text())
        for pid in (previous["display_pid"], previous["launcher_pid"]):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                continue
            raise RuntimeError("Existing background session is alive; reuse it")
    prefix = root / "wine32"
    if not prefix.exists():
        size = int(subprocess.check_output(["du", "-sb", str(source)], text=True).split()[0])
        if shutil.disk_usage(root).free < size + 500_000_000:
            raise ValueError("Insufficient free space for isolated prefix")
        staging = root / "wine32-copying"
        if staging.exists():
            raise RuntimeError("Incomplete snapshot exists; inspect it before retry")
        shutil.copytree(source, staging, symlinks=True)
        # Keep output directories off the owner's live Desktop/Documents.
        for user in (staging / "drive_c/users").iterdir():
            if user.is_dir():
                for name in ("Desktop", "Documents", "My Documents", "Downloads", "Pictures", "Music", "Videos"):
                    folder = user / name
                    if folder.is_symlink():
                        folder.unlink()
                        folder.mkdir()
        marker = {"complete": True, "ui_isolation_only": True,
                  "mastro_sha256": hashlib.sha256((staging / "drive_c/Program Files/Mastro/Mastro.exe").read_bytes()).hexdigest()}
        (staging / ".mastro-prefix-snapshot.json").write_text(json.dumps(marker) + "\n")
        staging.rename(prefix)
    marker = prefix / ".mastro-prefix-snapshot.json"
    if not marker.exists() or not json.loads(marker.read_text()).get("complete"):
        raise RuntimeError("Prefix snapshot is not certified complete")
    if prefix.resolve() == source:
        raise ValueError("Refusing shared mutable Wine prefix")
    auth = root / "Xauthority"
    auth.touch(mode=0o600)
    os.chmod(auth, 0o600)
    subprocess.run(["xauth", "-f", str(auth), "add", a.display, "MIT-MAGIC-COOKIE-1", secrets.token_hex(16)], check=True)
    env = dict(os.environ, DISPLAY=a.display, XAUTHORITY=str(auth),
               WINEPREFIX=str(prefix), WINEDEBUG="-all", MASTRO_BACKGROUND_DISPLAY=a.display,
               WINEDLLOVERRIDES="winemenubuilder.exe=d", DBUS_SESSION_BUS_ADDRESS="unix:path=/dev/null")
    with (root / "xvfb.log").open("ab") as log:
        server = subprocess.Popen([str(a.xvfb.resolve()), a.display, "-screen", "0", "1920x1080x24",
                                   "-nolisten", "tcp", "-auth", str(auth)], stdout=log, stderr=log, start_new_session=True)
    ready = False
    for _ in range(40):
        if server.poll() is not None:
            raise RuntimeError("Background display exited; inspect private xvfb.log")
        if Path(f"/tmp/.X11-unix/X{number}").exists():
            ready = True
            break
        time.sleep(.1)
    if not ready:
        server.terminate()
        raise RuntimeError("Background display did not become ready")
    exe = prefix / "drive_c/Program Files/Mastro/Mastro.exe"
    with (root / "mastro.log").open("ab") as log:
        app = subprocess.Popen(["wine", str(exe)], cwd=exe.parent, env=env,
                               stdout=log, stderr=log, start_new_session=True)
    state = {"display_pid": server.pid, "launcher_pid": app.pid,
             "environment": {k: env[k] for k in ("DISPLAY", "XAUTHORITY", "WINEPREFIX", "WINEDEBUG", "MASTRO_BACKGROUND_DISPLAY", "WINEDLLOVERRIDES", "DBUS_SESSION_BUS_ADDRESS")}}
    (root / "session.json").write_text(json.dumps(state, indent=2) + "\n")
    os.chmod(root / "session.json", 0o600)
    print("Isolated background display started; private session.json records process and environment state.")


if __name__ == "__main__":
    main()
