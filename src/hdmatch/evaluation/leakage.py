"""Conservative leakage audit for public blind questionnaire payloads."""

from __future__ import annotations

import json
import re
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class LeakSeverity(StrEnum):
    WARNING = "warning"
    CRITICAL = "critical"


class LeakageFinding(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    severity: LeakSeverity
    code: str
    json_path: str
    detail: str
    redacted_excerpt: str | None = None


class LeakageReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    scanned_file: str | None
    findings: tuple[LeakageFinding, ...]

    @property
    def passed(self) -> bool:
        return not any(item.severity is LeakSeverity.CRITICAL for item in self.findings)


class LeakageDetectedError(RuntimeError):
    def __init__(self, report: LeakageReport) -> None:
        super().__init__(f"blind payload contains {len(report.findings)} leakage finding(s)")
        self.report = report


_SECRET_KEYS = {
    "answerkey",
    "correctanswer",
    "groundtruth",
    "hiddenbirthtuple",
    "hiddenchart",
    "knownbirthday",
    "targetdate",
    "targetstate",
    "truedate",
    "truestate",
    "truebirthdate",
    "truebirthday",
    "truebirthtime",
    "truelocaldate",
    "truelocaldatetime",
    "trueutc",
    "truechartfeatureshash",
}
_SECRET_KEY_FRAGMENTS = ("answerkey", "groundtruth", "concealedtruth", "secretkey")
_PREDICTION_FORBIDDEN_KEYS = {
    "actualrank",
    "birthdate",
    "birthdatetime",
    "birthtime",
    "birthutc",
    "correctrank",
    "targetrank",
    "truedaterank",
    "zeroclusterrank",
}
_DATE_PATTERNS = (
    ("iso-date-clue", re.compile(r"(?<!\d)(?:18|19|20|21)\d{2}-\d{2}-\d{2}(?!\d)", re.I)),
    ("numeric-date-clue", re.compile(r"(?<!\d)\d{1,2}[/.]\d{1,2}[/.](?:\d{2}|\d{4})(?!\d)")),
    (
        "written-date-clue",
        re.compile(
            r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
            r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|"
            r"dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?\b",
            re.I,
        ),
    ),
    (
        "birth-phrase-clue",
        re.compile(r"\b(?:born\s+(?:on|at)|date\s+of\s+birth|birthday\s+is)\b", re.I),
    ),
    (
        "zodiac-clue",
        re.compile(
            r"\b(?:aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|"
            r"capricorn|aquarius|pisces)\b",
            re.I,
        ),
    ),
)
_PATH_PATTERNS = (
    re.compile(
        r"(?:^|\s)/(?:home|Users|tmp|var|private|mnt|workspace|root|opt|srv|etc|data|"
        r"secrets)/[^\s]+"
    ),
    re.compile(r"\b[A-Za-z]:\\(?:Users|Temp|Windows|workspace)\\[^\s]+", re.I),
    re.compile(r"\bfile://[^\s]+", re.I),
)
_SECRET_FILE_PATTERN = re.compile(
    r"(?:answer[_-]?key|secret[_-]?key|reveal)[^\s/\\]*\.(?:json|enc|key|txt)", re.I
)


def _normalise_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.casefold())


def _redact(value: str, *, limit: int = 80) -> str:
    compact = " ".join(value.split())[:limit]
    return "[redacted text, " + str(len(compact)) + " visible character(s)]"


def scan_blind_payload(payload: Any, *, scanned_file: str | None = None) -> LeakageReport:
    """Scan field names and all user-visible text while allowing declared month/year inputs."""

    findings: list[LeakageFinding] = []
    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            known_date_record = value.get("candidate_universe") == "known_date"
            for key, item in value.items():
                child_path = f"{path}.{key}"
                normalized = _normalise_key(str(key))
                known_date_exception = known_date_record and normalized == "knownbirthday"
                if (
                    normalized in _SECRET_KEYS
                    or any(part in normalized for part in _SECRET_KEY_FRAGMENTS)
                ) and not known_date_exception:
                    findings.append(
                        LeakageFinding(
                            severity=LeakSeverity.CRITICAL,
                            code="secret-field",
                            json_path=child_path,
                            detail="A field name discloses or carries concealed target material.",
                        )
                    )
                walk(item, child_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{path}[{index}]")
        elif isinstance(value, str):
            for code, pattern in _DATE_PATTERNS:
                if pattern.search(value):
                    findings.append(
                        LeakageFinding(
                            severity=LeakSeverity.CRITICAL,
                            code=code,
                            json_path=path,
                            detail="Free text contains a direct or proxy birth-date clue.",
                            redacted_excerpt=_redact(value),
                        )
                    )
            if any(pattern.search(value) for pattern in _PATH_PATTERNS):
                findings.append(
                    LeakageFinding(
                        severity=LeakSeverity.CRITICAL,
                        code="absolute-path-leak",
                        json_path=path,
                        detail="Public data contains a host/workspace path.",
                        redacted_excerpt=_redact(value),
                    )
                )
            if _SECRET_FILE_PATTERN.search(value):
                findings.append(
                    LeakageFinding(
                        severity=LeakSeverity.CRITICAL,
                        code="secret-artifact-path",
                        json_path=path,
                        detail="Public data names an answer-key, reveal, or key artifact.",
                        redacted_excerpt=_redact(value),
                    )
                )

    walk(payload, "$")
    return LeakageReport(scanned_file=scanned_file, findings=tuple(findings))


def scan_blind_file(path: str | Path) -> LeakageReport:
    source = Path(path)
    try:
        payload = json.loads(source.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        finding = LeakageFinding(
            severity=LeakSeverity.CRITICAL,
            code="invalid-public-json",
            json_path="$",
            detail="Blind artifact is not valid UTF-8 JSON.",
        )
        return LeakageReport(scanned_file=source.name, findings=(finding,))
    return scan_blind_payload(payload, scanned_file=source.name)


def scan_prediction_payload(
    payload: Any, *, scanned_file: str | None = None
) -> LeakageReport:
    """Scan blind decoder output without flagging its public candidate date/time values."""

    findings: list[LeakageFinding] = []

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                child_path = f"{path}.{key}"
                normalized = _normalise_key(str(key))
                forbidden_prefix = normalized.startswith(
                    ("true", "truth", "hidden", "groundtruth", "target", "actual", "correct")
                )
                if (
                    forbidden_prefix
                    or normalized in _PREDICTION_FORBIDDEN_KEYS
                    or any(part in normalized for part in _SECRET_KEY_FRAGMENTS)
                ):
                    findings.append(
                        LeakageFinding(
                            severity=LeakSeverity.CRITICAL,
                            code="truth-derived-prediction-field",
                            json_path=child_path,
                            detail=(
                                "Blind predictions contain a concealed-target field or a rank "
                                "that can only be computed after reveal."
                            ),
                        )
                    )
                walk(item, child_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{path}[{index}]")
        elif isinstance(value, str):
            if any(pattern.search(value) for pattern in _PATH_PATTERNS):
                findings.append(
                    LeakageFinding(
                        severity=LeakSeverity.CRITICAL,
                        code="absolute-path-leak",
                        json_path=path,
                        detail="Prediction output contains a host/workspace path.",
                        redacted_excerpt=_redact(value),
                    )
                )
            if _SECRET_FILE_PATTERN.search(value):
                findings.append(
                    LeakageFinding(
                        severity=LeakSeverity.CRITICAL,
                        code="secret-artifact-path",
                        json_path=path,
                        detail="Prediction output names a key or reveal artifact.",
                        redacted_excerpt=_redact(value),
                    )
                )

    walk(payload, "$")
    return LeakageReport(scanned_file=scanned_file, findings=tuple(findings))


def scan_prediction_file(path: str | Path) -> LeakageReport:
    source = Path(path)
    try:
        payload = json.loads(source.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        finding = LeakageFinding(
            severity=LeakSeverity.CRITICAL,
            code="invalid-prediction-json",
            json_path="$",
            detail="Prediction artifact is not valid UTF-8 JSON.",
        )
        return LeakageReport(scanned_file=source.name, findings=(finding,))
    return scan_prediction_payload(payload, scanned_file=source.name)


def assert_no_prediction_leakage(payload_or_path: Any) -> LeakageReport:
    report = (
        scan_prediction_file(payload_or_path)
        if isinstance(payload_or_path, (str, Path))
        else scan_prediction_payload(payload_or_path)
    )
    if not report.passed:
        raise LeakageDetectedError(report)
    return report


def assert_no_blind_leakage(payload_or_path: Any) -> LeakageReport:
    report = (
        scan_blind_file(payload_or_path)
        if isinstance(payload_or_path, (str, Path))
        else scan_blind_payload(payload_or_path)
    )
    if not report.passed:
        raise LeakageDetectedError(report)
    return report
