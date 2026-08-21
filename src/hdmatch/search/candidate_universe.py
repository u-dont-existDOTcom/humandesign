"""Exact local candidate-universe boundaries and interval/date overlap handling."""

from __future__ import annotations

import calendar
from collections.abc import Iterable
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from hdmatch.schemas import LocalDateOverlap


def local_month_utc_bounds(year: int, month: int, timezone_name: str) -> tuple[datetime, datetime]:
    """Return the UTC half-open interval covering an entire local civil month."""

    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    zone = ZoneInfo(timezone_name)
    local_start = datetime.combine(date(year, month, 1), time.min, tzinfo=zone)
    next_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    local_end = datetime.combine(next_date, time.min, tzinfo=zone)
    return local_start.astimezone(UTC), local_end.astimezone(UTC)


def local_date_utc_bounds(local_date: date, timezone_name: str) -> tuple[datetime, datetime]:
    zone = ZoneInfo(timezone_name)
    start = datetime.combine(local_date, time.min, tzinfo=zone).astimezone(UTC)
    end = datetime.combine(local_date + timedelta(days=1), time.min, tzinfo=zone).astimezone(UTC)
    return start, end


def split_interval_by_local_date(
    start_utc: datetime, end_utc: datetime, timezone_name: str
) -> tuple[LocalDateOverlap, ...]:
    """Measure overlap with every local date, including 23/25-hour DST days."""

    if start_utc.tzinfo is None or end_utc.tzinfo is None:
        raise ValueError("interval timestamps must be timezone-aware")
    start_utc = start_utc.astimezone(UTC)
    end_utc = end_utc.astimezone(UTC)
    if end_utc <= start_utc:
        raise ValueError("interval must have positive duration")
    zone = ZoneInfo(timezone_name)
    cursor_date = start_utc.astimezone(zone).date()
    final_date = (end_utc - timedelta(microseconds=1)).astimezone(zone).date()
    overlaps: list[LocalDateOverlap] = []
    while cursor_date <= final_date:
        day_start, day_end = local_date_utc_bounds(cursor_date, timezone_name)
        overlap_start = max(start_utc, day_start)
        overlap_end = min(end_utc, day_end)
        if overlap_end > overlap_start:
            overlaps.append(
                LocalDateOverlap(
                    date=cursor_date,
                    seconds=(overlap_end - overlap_start).total_seconds(),
                )
            )
        cursor_date += timedelta(days=1)
    return tuple(overlaps)


def expected_days_in_month(year: int, month: int) -> tuple[date, ...]:
    count = calendar.monthrange(year, month)[1]
    return tuple(date(year, month, day) for day in range(1, count + 1))


def assert_month_coverage(
    overlaps: Iterable[LocalDateOverlap], year: int, month: int, timezone_name: str
) -> None:
    actual: dict[date, float] = {}
    for item in overlaps:
        actual[item.date] = actual.get(item.date, 0.0) + item.seconds
    for local_day in expected_days_in_month(year, month):
        start, end = local_date_utc_bounds(local_day, timezone_name)
        expected = (end - start).total_seconds()
        if abs(actual.get(local_day, 0.0) - expected) > 1e-3:
            raise ValueError(f"candidate intervals do not cover local date {local_day}")
