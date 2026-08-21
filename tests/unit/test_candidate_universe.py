from datetime import UTC, datetime

import pytest

from hdmatch.search.candidate_universe import local_month_utc_bounds, split_interval_by_local_date


def test_local_month_bounds_include_dst_short_day() -> None:
    start, end = local_month_utc_bounds(2024, 3, "America/New_York")
    assert start == datetime(2024, 3, 1, 5, tzinfo=UTC)
    assert end == datetime(2024, 4, 1, 4, tzinfo=UTC)


def test_split_interval_measures_dst_days() -> None:
    start, end = local_month_utc_bounds(2024, 3, "America/New_York")
    overlaps = split_interval_by_local_date(start, end, "America/New_York")
    by_day = {str(item.date): item.seconds for item in overlaps}
    assert by_day["2024-03-10"] == 23 * 3600
    assert sum(by_day.values()) == (end - start).total_seconds()


def test_split_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        split_interval_by_local_date(datetime(2024, 1, 1), datetime(2024, 1, 2), "UTC")
