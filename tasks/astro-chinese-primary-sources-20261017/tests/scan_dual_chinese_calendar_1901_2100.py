#!/usr/bin/env python3
"""Research-only deterministic 1901-2100 independent calendar disagreement census.

Not a calendar oracle, not authenticated historical Chinese calendar, and
not evidence that astrology can predict real humans. Reproducible with pinned
lunar_python 1.4.8 and sxtwl 2.0.7, installed separately, no network calls.

Run:
  PYTHONPATH=/path/to/optional/lunar_pkgs python3 scan_dual_chinese_calendar_1901_2100.py --output REPORT.json

Never substitute one oracle's result for a mismatch or unsupported date.
"""

import argparse
from collections import Counter
from datetime import date, timedelta
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import time
from lunar_python import Solar
import sxtwl

PIN = {"lunar_python": "1.4.8", "sxtwl": "2.0.7"}
for pkg, required in PIN.items():
    if version(pkg) != required:
        raise SystemExit(f"Refusing non-pinned {pkg}: actual={version(pkg)}, required={required}")


def result_6tail(d):
    x = Solar.fromYmd(d.year, d.month, d.day).getLunar()
    return [x.getYear(), abs(x.getMonth()), x.getDay(), bool(x.getMonth() < 0)]


def result_sxtwl(d):
    x = sxtwl.fromSolar(d.year, d.month, d.day)
    return [x.getLunarYear(), x.getLunarMonth(), x.getLunarDay(), bool(x.isLunarLeap())]


def run(first: date, last: date):
    summary_sha = hashlib.sha256()
    errors = []
    all_mismatches = []
    current = first
    count = 0
    matched = 0
    started = time.perf_counter()
    while current <= last:
        s = current.isoformat()
        try:
            a = result_6tail(current)
            b = result_sxtwl(current)
            line = f"{s}|6tail={a}|sxtwl={b}\n"
            summary_sha.update(line.encode("utf-8"))
            if a == b:
                matched += 1
            else:
                all_mismatches.append({"date": s, "lunar_python": a, "sxtwl": b})
        except Exception as exc:
            errors.append({"date": s, "exception_class": type(exc).__name__, "message": str(exc)})
            summary_sha.update(f"{s}|EXCEPTION|{type(exc).__name__}|{str(exc)}\n".encode())
        count += 1
        if count % 15000 == 0:
            print(f"PROGRESS {count} dates; mismatches {len(all_mismatches)}; failures {len(errors)}",flush=True)
        current += timedelta(days=1)
    windows = []
    current_window = None
    for issue in all_mismatches:
        curr = date.fromisoformat(issue["date"])
        if current_window and (curr - date.fromisoformat(current_window["end"])).days == 1:
            current_window["end"] = issue["date"]
            current_window["days"] += 1
            current_window["last_disagreement"] = issue
        else:
            current_window = {
                "start": issue["date"], "end": issue["date"], "days": 1,
                "first_disagreement": issue, "last_disagreement": issue
            }
            windows.append(current_window)
    result = {
        "title": "Original independent Chinese civil-to-lunar software disagreement census",
        "status": "CALENDAR-SOFTWARE CROSS-CHECK ONLY; mismatches always unresolved",
        "scope_gregorian_inclusive": [first.isoformat(),last.isoformat()],
        "packages_pinned": PIN,
        "date_count": count,
        "agreed_dates": matched,
        "disagreed_dates": len(all_mismatches),
        "exception_dates": len(errors),
        "disagreement_fraction": len(all_mismatches)/count,
        "comparison_input_output_stream_sha256": summary_sha.hexdigest(),
        "disagreement_windows": windows,
        "disagreement_dates": all_mismatches,
        "exception_examples": errors[:50],
        "all_exceptions_recorded": len(errors) <= 50,
        "per_year_disagreements": dict(sorted(Counter(x["date"][:4] for x in all_mismatches).items())),
        "elapsed_wall_seconds": round(time.perf_counter()-started,3),
        "HKO_1901_2100_truth_verified": False,
        "official_HKO_API_observed_dates": 10,
        "HKO_identified_near_midnight_future_dates": [
            "2057-09-28", "2089-09-04", "2097-08-07"
        ],
        "hko_caution_url": "https://www.hko.gov.hk/en/gts/time/conversion.htm",
        "independently_validated_traditional_natal_chart": False,
        "real_human_predictive_validations": 0,
        "script": "tasks/astro-chinese-primary-sources-20261017/tests/scan_dual_chinese_calendar_1901_2100.py",
    }
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--first", default="1901-01-01")
    parser.add_argument("--last", default="2100-12-31")
    parser.add_argument("--output", required=True)
    ns=parser.parse_args()
    first=date.fromisoformat(ns.first)
    last=date.fromisoformat(ns.last)
    if first>last:
        raise ValueError("Date range reversed")
    report=run(first,last)
    Path(ns.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print("REPORT",ns.output,"dates",report["date_count"],"agreed",report["agreed_dates"],
          "disagree",report["disagreed_dates"],"exceptions",report["exception_dates"],
          "windows",len(report["disagreement_windows"]),"digest",report["comparison_input_output_stream_sha256"])
    for w in report["disagreement_windows"]:
        print("WINDOW",w["start"],w["end"],w["days"])


if __name__=="__main__":
    main()
