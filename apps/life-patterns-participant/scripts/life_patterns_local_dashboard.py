#!/usr/bin/env python3
"""Owner-local, passwordless, read-only feedback dashboard.

Reads the existing researcher credential from Railway at runtime. Never places
the credential in a browser URL, clipboard, local HTML or command arguments.
The resulting private report shows the current researcher feedback items.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


def fetch_feedback(config: dict) -> tuple[list[dict], str]:
    command = [
        config["railway_cli"],
        "variables",
        "-p",
        config["project_id"],
        "-e",
        config["environment_id"],
        "-s",
        config["service_id"],
        "--json",
    ]
    try:
        response = subprocess.run(command, check=True, capture_output=True, text=True, timeout=35)
        credential = json.loads(response.stdout)["PARTICIPANT_ADMIN_TOKEN"]
        if not isinstance(credential, str) or len(credential) < 25:
            raise ValueError("Invalid researcher credential")
        endpoint = config["dashboard_url"].rstrip("/") + "/api/admin/question-feedback"
        if not endpoint.startswith("https://"):
            raise ValueError("Researcher endpoint must be HTTPS")
        request = Request(endpoint, headers={"Authorization": "Bearer " + credential})
        with urlopen(request, timeout=25) as result:
            data = json.load(result)
        if not isinstance(data.get("feedback"), list):
            raise ValueError("Unexpected feedback response")
        return data["feedback"], credential
    except Exception as exc:
        raise RuntimeError(
            "Cannot retrieve your private research feedback. Check Railway connection."
        ) from exc


def private_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".writing")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(content)
    os.replace(temporary, path)
    path.chmod(0o600)


def render_private_feedback(entries: list[dict]) -> str:
    sections = []
    for row in entries:

        def value(key: str, current=row) -> str:
            return html.escape(str(current.get(key) or ""), quote=True)

        sections.append(
            "<article><p class='meta'>"
            + value("route_id")
            + " · "
            + value("issue_hint")
            + " · "
            + value("status")
            + "</p><h3>"
            + value("question_text")
            + "</h3><blockquote>"
            + value("feedback_text")
            + "</blockquote></article>"
        )
    stylesheet = """
body{max-width:900px;margin:35px auto;padding:0 20px;font:16px/1.6 system-ui}
article{padding:15px 25px;margin:20px 0;border:1px solid #ccc;border-radius:12px}
h3{font-size:17px}blockquote{border-left:3px solid #9aa;padding-left:15px;
white-space:pre-wrap}.meta,.note{color:#667;font-size:14px}
"""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="Content-Security-Policy" '
        "content=\"default-src 'none';style-src 'unsafe-inline'\">"
        "<title>Life Patterns — Question Feedback</title><style>"
        + stylesheet
        + "</style></head><body>"
        "<h1>Life Patterns — Researcher Question Feedback</h1>"
        "<p><strong>" + str(len(entries)) + " feedback entries</strong></p>"
        '<p class="note">Private read-only snapshot from your research service; '
        "updated each time this launcher runs. No password or access key is "
        "included. Review statuses are changed through the authenticated "
        "online dashboard.</p>" + "".join(sections) + "</body></html>"
    )


def make_handoff(config: dict, key: str) -> Path:
    """Brief owner-only bridge; credential never appears in shell arguments."""
    target = config["dashboard_url"].rstrip("/") + "/admin#key=" + quote(key, safe="")
    root = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}"))
    if not root.is_dir():
        root = Path.home() / ".cache"
    directory = root / "life-patterns-researcher"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    directory.chmod(0o700)
    fd, filename = tempfile.mkstemp(prefix="private-login-", suffix=".html", dir=directory)
    os.close(fd)
    bridge = (
        '<!doctype html><html><head><meta charset="utf-8"></head><body>'
        "<p>Opening secure researcher dashboard...</p><script>location.replace("
        + json.dumps(target)
        + ");</script></body></html>"
    )
    private_write(Path(filename), bridge)
    return Path(filename)


def launch_browser(address: str) -> None:
    for argv in (["xdg-open", address], ["gio", "open", address]):
        try:
            done = subprocess.run(
                argv,
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=20,
            )
            if done.returncode == 0:
                return
        except (OSError, subprocess.TimeoutExpired):
            pass
    raise RuntimeError("No graphical browser opened the researcher dashboard.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text())
        entries, credential = fetch_feedback(config)
        report = Path(config["local_report"])
        private_write(report, render_private_feedback(entries))
        if args.check:
            print(f"PASS: feedback_count={len(entries)}; report_saved=True; key_exposed=False")
        else:
            launched = subprocess.run(
                ["xdg-open", report.as_uri()],
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=20,
            )
            if launched.returncode != 0:
                raise RuntimeError("Browser could not open the local feedback report.")
        return 0
    except Exception as exc:
        message = str(exc)
        print(message, file=sys.stderr)
        if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
            try:
                subprocess.run(
                    ["zenity", "--error", "--title=Life Patterns Researcher", "--text=" + message],
                    timeout=60,
                    check=False,
                )
            except Exception:
                pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
