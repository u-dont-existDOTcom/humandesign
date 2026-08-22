"""Single-pass logical-universe validation without century-wide accumulation."""

from __future__ import annotations

import hashlib
import sqlite3
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hdmatch.experiments.canonical import canonical_json_bytes

from .models import CenturyStateRecord, discrete_chart_identity_sha256


class CenturyCacheStreamError(ValueError):
    """A streamed logical universe violates the exact-state cache contract."""


@dataclass(frozen=True, slots=True)
class LogicalUniverseStreamAudit:
    """Bounded-memory audit result for one complete logical universe."""

    utc_start: datetime
    utc_end_exclusive: datetime
    interval_count: int
    boundary_event_count: int
    canonical_rows_sha256: str


def canonical_row_json_line(row: CenturyStateRecord) -> bytes:
    """Return the exact bytes participating in the logical-universe hash."""

    return canonical_json_bytes(row.model_dump(mode="json")) + b"\n"


class LogicalUniverseStreamValidator:
    """Incrementally validate ordering, continuity, maximality, IDs, and hash.

    State-ID uniqueness uses a temporary on-disk SQLite index.  The validator
    retains only the immediately preceding logical row and therefore does not
    turn a century verification into a century-sized Python collection.
    """

    def __init__(
        self,
        *,
        utc_start: datetime,
        utc_end_exclusive: datetime,
        validate_row: Callable[[CenturyStateRecord], None],
    ) -> None:
        if utc_end_exclusive <= utc_start:
            raise CenturyCacheStreamError("streamed universe range must be positive")
        self._utc_start = utc_start
        self._utc_end_exclusive = utc_end_exclusive
        self._validate_row = validate_row
        self._digest = hashlib.sha256()
        self._interval_count = 0
        self._boundary_event_count = 0
        self._previous: CenturyStateRecord | None = None
        self._finished = False
        self._temporary_directory = tempfile.TemporaryDirectory(
            prefix="hdmatch-cache-state-ids-"
        )
        database_path = Path(self._temporary_directory.name) / "state-ids.sqlite3"
        self._database = sqlite3.connect(database_path)
        self._database.execute("PRAGMA temp_store=FILE")
        self._database.execute("PRAGMA cache_size=-2048")
        self._database.execute("CREATE TABLE state_ids (state_id TEXT PRIMARY KEY)")

    def __enter__(self) -> LogicalUniverseStreamValidator:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object,
    ) -> None:
        del exc_type, exc_value, traceback
        self.close()

    def ingest(self, row: CenturyStateRecord) -> None:
        """Validate and add exactly one row to the running audit."""

        if self._finished:
            raise CenturyCacheStreamError("streamed universe audit is already finished")
        self._validate_row(row)
        try:
            self._database.execute(
                "INSERT INTO state_ids(state_id) VALUES (?)",
                (row.state_id,),
            )
        except sqlite3.IntegrityError as exc:
            raise CenturyCacheStreamError(
                f"century cache contains duplicate state ID: {row.state_id}"
            ) from exc

        previous = self._previous
        if previous is None:
            if row.utc_start != self._utc_start:
                raise CenturyCacheStreamError(
                    "first cache interval does not start at the declared universe start"
                )
        else:
            if previous.utc_end != row.utc_start:
                raise CenturyCacheStreamError(
                    "century-cache intervals contain a gap or overlap"
                )
            if discrete_chart_identity_sha256(previous) == (
                discrete_chart_identity_sha256(row)
            ):
                raise CenturyCacheStreamError(
                    "century-cache intervals are not maximal: adjacent rows have the "
                    "same discrete chart identity"
                )

        self._digest.update(canonical_row_json_line(row))
        self._interval_count += 1
        self._boundary_event_count += len(row.boundary_events)
        self._previous = row

    def finish(
        self,
        *,
        expected_interval_count: int | None = None,
        expected_boundary_event_count: int | None = None,
        expected_canonical_rows_sha256: str | None = None,
    ) -> LogicalUniverseStreamAudit:
        """Close and return the audit, optionally binding aggregate provenance."""

        if self._finished:
            raise CenturyCacheStreamError("streamed universe audit is already finished")
        self._finished = True
        previous = self._previous
        if previous is None:
            self.close()
            raise CenturyCacheStreamError(
                "century cache must contain at least one interval"
            )
        if previous.utc_end != self._utc_end_exclusive:
            self.close()
            raise CenturyCacheStreamError(
                "last cache interval does not end at the declared universe end"
            )
        digest = self._digest.hexdigest()
        mismatches = {
            "interval count": (self._interval_count, expected_interval_count),
            "boundary-event count": (
                self._boundary_event_count,
                expected_boundary_event_count,
            ),
            "canonical-row hash": (digest, expected_canonical_rows_sha256),
        }
        for label, (actual, expected) in mismatches.items():
            if expected is not None and actual != expected:
                self.close()
                raise CenturyCacheStreamError(
                    f"streamed universe {label} differs from aggregate provenance"
                )
        audit = LogicalUniverseStreamAudit(
            utc_start=self._utc_start,
            utc_end_exclusive=self._utc_end_exclusive,
            interval_count=self._interval_count,
            boundary_event_count=self._boundary_event_count,
            canonical_rows_sha256=digest,
        )
        self.close()
        return audit

    def close(self) -> None:
        """Release the disk-backed uniqueness index; safe after failure."""

        database = getattr(self, "_database", None)
        if database is not None:
            database.close()
            self._database = None  # type: ignore[assignment]
        temporary_directory = getattr(self, "_temporary_directory", None)
        if temporary_directory is not None:
            temporary_directory.cleanup()
            self._temporary_directory = None  # type: ignore[assignment]
