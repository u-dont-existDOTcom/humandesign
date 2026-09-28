#!/usr/bin/env python3
"""Manual Venice activation for the Railway Life Patterns participant app.

Run only from the owner's machine:
    python3 activate_venice.py --activate

No credential is printed or stored in Git. If activation fails after mutation,
the previous participant live flag and gateway credential are restored.
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

GW_PROJECT = "inner-child-humanization-exp"
GW_SERVICE = "venice-model-gateway"
GW_ENV = "production"
PART_PROJECT = "humandesign-relationship"
PART_SERVICE = "life-patterns-participant"
PART_ENV = "production"
GATEWAY_ORIGIN = "https://venice-model-gateway-production.up.railway.app"
DEFAULT_PARTICIPANT_ORIGIN = "https://life-patterns-participant-production.up.railway.app"
EXPECTED_BUILD = "f35a94f3e4feaf0dfa562f97516ed2c42a51fd82"
EXPECTED_VERSION = "railway-participant-v2.1-20260927"
PRIVATE_DIR = Path.home() / ".local/share/humandesign/private/participant-railway-20260927"


class ActivationError(RuntimeError):
    pass


def railway_bin() -> str:
    candidates = [
        shutil.which("railway"),
        str(Path.home() / ".local/lib/node_modules/@railway/cli/bin/railway"),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            subprocess.run(
                [candidate, "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                timeout=15,
            )
            return candidate
        except (OSError, subprocess.SubprocessError):
            continue
    raise ActivationError("Railway CLI is not working; repair it before activation.")


def run_railway(railway: str, args: list[str], *, stdin: str | None = None) -> str:
    env = dict(
        os.environ,
        RAILWAY_CALLER="manual:humandesign-participant-venice-activation",
        RAILWAY_AGENT_SESSION="humandesign-participant-venice-activation-20260927",
    )
    result = subprocess.run(
        [railway, *args],
        input=stdin,
        text=True,
        capture_output=True,
        env=env,
        timeout=120,
    )
    if result.returncode:
        raise ActivationError(
            f"Railway command failed ({args[0]}): "
            + (result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}")
        )
    return result.stdout


def variable_map(railway: str, project: str, service: str, environment: str) -> dict[str, str]:
    raw = run_railway(
        railway,
        [
            "variable",
            "list",
            "--project",
            project,
            "--service",
            service,
            "--environment",
            environment,
            "--json",
        ],
    )
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ActivationError("Railway returned unexpected variable JSON.")
    return {str(k): str(v) for k, v in value.items()}


def set_variable(railway: str, name: str, value: str) -> None:
    run_railway(
        railway,
        [
            "variable",
            "set",
            "--project",
            PART_PROJECT,
            "--service",
            PART_SERVICE,
            "--environment",
            PART_ENV,
            "--skip-deploys",
            "--stdin",
            name,
        ],
        stdin=value,
    )


def redeploy(railway: str) -> str:
    raw = run_railway(
        railway,
        [
            "redeploy",
            "--project",
            PART_PROJECT,
            "--service",
            PART_SERVICE,
            "--environment",
            PART_ENV,
            "--yes",
            "--json",
        ],
    )
    value = json.loads(raw)
    row = value.get("deployment", value)
    deployment_id = row.get("id")
    if not deployment_id:
        raise ActivationError("Railway redeploy did not return a deployment id.")
    return str(deployment_id)


def wait_deployment(railway: str, deployment_id: str) -> None:
    for _ in range(90):
        rows = json.loads(
            run_railway(
                railway,
                [
                    "deployment",
                    "list",
                    "--project",
                    PART_PROJECT,
                    "--service",
                    PART_SERVICE,
                    "--environment",
                    PART_ENV,
                    "--limit",
                    "20",
                    "--json",
                ],
            )
        )
        status = next(
            (str(row.get("status")) for row in rows if row.get("id") == deployment_id), None
        )
        if status == "SUCCESS":
            return
        if status in {"FAILED", "CRASHED", "REMOVED", "REMOVING", "SKIPPED", "NEEDS_APPROVAL"}:
            raise ActivationError(f"Participant deployment ended in {status}.")
        time.sleep(5)
    raise ActivationError("Participant deployment did not reach SUCCESS in time.")


def health(origin: str) -> dict:
    with urllib.request.urlopen(origin.rstrip("/") + "/healthz", timeout=30) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise ActivationError("Participant health response was malformed.")
    return value


def wait_health(origin: str, *, enabled: bool, configured: bool) -> None:
    last: dict | None = None
    for _ in range(40):
        try:
            last = health(origin)
            if (
                last.get("version") == EXPECTED_VERSION
                and last.get("participant_enabled") is enabled
                and last.get("provider_configured") is configured
            ):
                return
        except Exception:
            pass
        time.sleep(3)
    raise ActivationError(f"Participant health did not reach the expected state: {last!r}")


def gateway_smoke(token: str) -> dict:
    payload = {
        "model": "openai-gpt-56-sol",
        "reasoning_effort": "xhigh",
        "max_completion_tokens": 800,
        "stream": False,
        "store": False,
        "response_format": {"type": "json_object"},
        "venice_parameters": {
            "include_venice_system_prompt": False,
            "enable_web_search": "off",
            "enable_web_scraping": False,
            "enable_web_citations": False,
        },
        "messages": [
            {
                "role": "system",
                "content": "Synthetic connectivity check only. Return exactly valid JSON.",
            },
            {
                "role": "user",
                "content": '{"ok":true,"purpose":"life_patterns_activation_smoke"}',
            },
        ],
    }
    request = urllib.request.Request(
        GATEWAY_ORIGIN + "/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            value = json.load(response)
    except urllib.error.HTTPError as exc:
        raise ActivationError(f"Gateway smoke failed with HTTP {exc.code}.") from None
    choice = value["choices"][0]
    if choice.get("finish_reason") != "stop":
        raise ActivationError("Gateway smoke did not finish normally.")
    content = json.loads(choice["message"]["content"])
    if content.get("ok") is not True:
        raise ActivationError("Gateway smoke returned unexpected content.")
    model = value.get("model")
    if model not in {"openai-gpt-56-sol", "gpt-5.6-sol"}:
        raise ActivationError(f"Unexpected gateway model: {model!r}")
    return {"model": model, "reasoning_effort": "xhigh"}


def app_smoke(origin: str, join_token: str) -> dict:
    base = origin.rstrip("/")
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def request(
        path: str, body: dict | None = None, session: str | None = None, timeout: int = 700
    ):
        headers = {"Origin": base}
        data = None
        if body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        if session:
            headers["X-Life-Patterns-Session"] = session
        req = urllib.request.Request(base + path, data=data, headers=headers)
        try:
            with opener.open(req, timeout=timeout) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            try:
                detail = json.loads(exc.read()).get("detail")
            except Exception:
                detail = None
            suffix = f": {detail}" if detail else ""
            raise ActivationError(f"{path} failed HTTP {exc.code}{suffix}") from None

    state = request("/api/join", {"token": join_token}, timeout=60)
    session = state["session_id"]

    def operation(action: str, text: str = ""):
        nonlocal state
        state = request(
            "/api/operations",
            {
                "revision": state["revision"],
                "operation_id": secrets.token_hex(12),
                "action": action,
                "text": text,
                "target": None,
            },
            session,
        )
        return state

    operation("consent")
    state = request("/api/next", {}, session)
    if state.get("phase") != "awaiting_answer":
        raise ActivationError("First real model step did not produce a participant question.")
    question = (state.get("question") or {}).get("text") or ""
    if "[route:" not in question:
        raise ActivationError("First real model question lost its canonical route provenance.")

    synthetic_answer = (
        "I would first organize the concrete information I have, notice what conflicts, "
        "and check the unclear detail with the person or source most likely to know it."
    )
    operation("answer", synthetic_answer)
    if state.get("turns", [])[-1].get("answer_text") != synthetic_answer:
        raise ActivationError("Synthetic answer was not persisted exactly.")

    state = request("/api/next", {}, session)
    if state.get("phase") not in {"awaiting_answer", "review"}:
        raise ActivationError(
            "Answer-processing model step ended in unexpected phase: " + str(state.get("phase"))
        )

    operation("stop")
    if state.get("phase") != "stopped":
        raise ActivationError("Synthetic record did not freeze on Stop.")

    export_request = urllib.request.Request(
        base + "/api/export?session_id=" + session,
        headers={"X-Life-Patterns-Session": session},
    )
    with opener.open(export_request, timeout=60) as response:
        export = json.load(response)

    if export.get("interview_status") != "stopped_by_participant":
        raise ActivationError("Frozen synthetic export has wrong interview status.")
    answers = [turn.get("answer_text") for turn in export.get("turns", [])]
    if synthetic_answer not in answers:
        raise ActivationError("Frozen export lost the exact synthetic answer.")
    calls = export.get("model_call_telemetry", [])
    real_calls = [
        row
        for row in calls
        if row.get("provider") == "venice"
        and row.get("returned_model") in {"openai-gpt-56-sol", "gpt-5.6-sol"}
    ]
    if len(real_calls) < 4:
        raise ActivationError(
            f"Expected at least four real Venice planning/admission calls; got {len(real_calls)}."
        )
    if any(row.get("reasoning_effort") != "xhigh" for row in real_calls):
        raise ActivationError("A real participant model call did not use XHigh.")

    return {
        "ok": True,
        "synthetic_only": True,
        "do_not_use_as_participant_data": True,
        "created_at": datetime.now(UTC).isoformat(),
        "session_id": session,
        "provider": "venice",
        "requested_model": "openai-gpt-56-sol",
        "reasoning_effort": "xhigh",
        "real_model_calls": len(real_calls),
        "returned_models": sorted({row.get("returned_model") for row in real_calls}),
        "exact_answer_persisted": True,
        "final_export_frozen": True,
    }


def write_private_file(name: str, text: str) -> Path:
    PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(PRIVATE_DIR, 0o700)
    path = PRIVATE_DIR / name
    path.write_text(text)
    os.chmod(path, 0o600)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args()
    if not args.activate:
        parser.print_help()
        return 2

    railway = railway_bin()
    print("Checking Railway authentication...")
    run_railway(railway, ["whoami", "--json"])

    print("Reading existing Railway configuration without printing secrets...")
    gateway_vars = variable_map(railway, GW_PROJECT, GW_SERVICE, GW_ENV)
    participant_vars = variable_map(railway, PART_PROJECT, PART_SERVICE, PART_ENV)

    gateway_token = gateway_vars.get("MODEL_GATEWAY_TOKEN", "")
    if not gateway_token:
        raise ActivationError("Gateway MODEL_GATEWAY_TOKEN is not configured.")
    join_token = participant_vars.get("PARTICIPANT_JOIN_TOKEN", "")
    admin_token = participant_vars.get("PARTICIPANT_ADMIN_TOKEN", "")
    if not join_token or not admin_token:
        raise ActivationError("Participant join/admin credentials are missing.")
    if participant_vars.get("PARTICIPANT_BUILD_COMMIT") != EXPECTED_BUILD:
        raise ActivationError(
            "Refusing activation: deployed build marker is not the reviewed build " + EXPECTED_BUILD
        )

    origin = participant_vars.get("PARTICIPANT_PUBLIC_ORIGIN", "").rstrip("/")
    origin = origin or DEFAULT_PARTICIPANT_ORIGIN
    previous_live = participant_vars.get("PARTICIPANT_LIVE_ENABLED", "0")
    previous_token = participant_vars.get("UDA_MODEL_GATEWAY_TOKEN", "")

    staged_health = health(origin)
    if staged_health.get("version") != EXPECTED_VERSION:
        raise ActivationError("Unexpected participant application version.")
    print(
        "Disabled/staged health: "
        f"enabled={staged_health.get('participant_enabled')}, "
        f"provider_configured={staged_health.get('provider_configured')}"
    )

    print("Running direct authenticated Venice gateway smoke...")
    gateway_receipt = gateway_smoke(gateway_token)
    print(
        "Venice gateway smoke: PASS "
        f"({gateway_receipt['model']}, {gateway_receipt['reasoning_effort']})"
    )

    mutated = False
    success = False
    try:
        print("Installing existing gateway credential into participant service...")
        set_variable(railway, "UDA_MODEL_GATEWAY_TOKEN", gateway_token)
        set_variable(railway, "PARTICIPANT_LIVE_ENABLED", "1")
        mutated = True

        print("Redeploying only life-patterns-participant...")
        deployment_id = redeploy(railway)
        wait_deployment(railway, deployment_id)
        wait_health(origin, enabled=True, configured=True)
        print(f"Enabled deployment: PASS ({deployment_id})")

        print("Running real synthetic participant flow through Railway -> Venice...")
        receipt = app_smoke(origin, join_token)
        receipt["deployment_id"] = deployment_id
        receipt["gateway_smoke"] = gateway_receipt
        write_private_file(
            "venice-activation-smoke.json",
            json.dumps(receipt, indent=2) + "\n",
        )
        success = True
        print(
            "Real participant pipeline: PASS "
            f"({receipt['real_model_calls']} Venice calls, session {receipt['session_id']})"
        )
    finally:
        if mutated and not success:
            print(
                "Activation failed. Restoring previous participant activation state...",
                file=sys.stderr,
            )
            try:
                set_variable(railway, "PARTICIPANT_LIVE_ENABLED", previous_live)
                set_variable(railway, "UDA_MODEL_GATEWAY_TOKEN", previous_token)
                rollback_id = redeploy(railway)
                wait_deployment(railway, rollback_id)
                print("Previous activation state restored.", file=sys.stderr)
            except Exception as rollback_error:
                print(
                    "WARNING: automatic rollback also failed: " + str(rollback_error),
                    file=sys.stderr,
                )

    if not success:
        raise ActivationError("Participant activation did not complete.")

    join_path = write_private_file(
        "participant-join-link.txt",
        f"{origin}/#join={join_token}\n",
    )
    admin_path = write_private_file(
        "participant-admin-link.txt",
        f"{origin}/admin#key={admin_token}\n",
    )

    print()
    print("SUCCESS: Life Patterns participant interviewing is enabled through Venice.")
    print("Private links:")
    print(f"  {admin_path}")
    print(f"  {join_path}")
    print(f"Receipt: {PRIVATE_DIR / 'venice-activation-smoke.json'}")
    print("The synthetic smoke session is test data and must not be used in research analysis.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ActivationError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
