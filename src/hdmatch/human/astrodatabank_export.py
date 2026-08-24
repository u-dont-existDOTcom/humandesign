"""Streaming reader for the official Astro-Databank XML export format.

The reader is deliberately astronomy-agnostic.  It extracts source-rated birth
records, short biographies, and research categories without calculating any HD
or astronomical predictor.  This allows outcome/coverage eligibility audits to
be completed before a frozen external predictor is evaluated.

Format reference:
https://www.astro.com/astro-databank/Help:XML_export_format
"""

from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

UNIX_EPOCH_JULIAN_DAY = 2440587.5


@dataclass(frozen=True, slots=True)
class AstroDatabankCategory:
    cat_id: int
    text: str
    notes: str | None


@dataclass(frozen=True, slots=True)
class AstroDatabankRecord:
    adb_id: int
    name: str
    gender: str
    rodden_rating: str
    data_type: str
    jd_ut: float | None
    birth_utc: datetime | None
    has_alternative_birth_data: bool
    short_biography: str
    categories: tuple[AstroDatabankCategory, ...]

    @property
    def is_primary_timed_public_record(self) -> bool:
        """Whether this record satisfies the conservative external-test birth filter."""

        return (
            self.rodden_rating in {"AA", "A"}
            and self.data_type == "Public Figure"
            and self.birth_utc is not None
            and not self.has_alternative_birth_data
        )


def iter_astrodatabank_export(path: str | Path) -> Iterator[AstroDatabankRecord]:
    """Yield records from a potentially large ADB XML export with bounded memory."""

    source = Path(path)
    for _event, element in ET.iterparse(source, events=("end",)):
        if element.tag != "adb_entry":
            continue
        yield _parse_entry(element)
        element.clear()


def julian_day_ut_to_datetime(jd_ut: float) -> datetime:
    """Convert an absolute UT Julian day to proleptic-Gregorian UTC datetime."""

    if not math.isfinite(jd_ut):
        raise ValueError("jd_ut must be finite")
    seconds = (jd_ut - UNIX_EPOCH_JULIAN_DAY) * 86400.0
    try:
        return datetime(1970, 1, 1, tzinfo=UTC) + timedelta(seconds=seconds)
    except OverflowError as exc:
        raise ValueError("jd_ut is outside Python datetime range") from exc


def _parse_entry(element: ET.Element) -> AstroDatabankRecord:
    adb_id_text = element.attrib.get("adb_id")
    if adb_id_text is None:
        raise ValueError("ADB entry is missing adb_id")
    public = element.find("public_data")
    if public is None:
        raise ValueError(f"ADB entry {adb_id_text} is missing public_data")

    name = _text(public.find("name"))
    gender = _text(public.find("gender"))
    rodden_rating = _text(public.find("roddenrating"))
    datatype = public.find("datatype")
    data_type = "" if datatype is None else datatype.attrib.get("sdatatype", "")
    bdata = public.find("bdata")
    sbtime = None if bdata is None else bdata.find("sbtime")
    jd_ut = _optional_float(None if sbtime is None else sbtime.attrib.get("jd_ut"))
    birth_utc = None if jd_ut is None else julian_day_ut_to_datetime(jd_ut)

    text_data = element.find("text_data")
    short_biography = "" if text_data is None else _text(text_data.find("shortbiography"))

    category_items: list[AstroDatabankCategory] = []
    research_data = element.find("research_data")
    categories = None if research_data is None else research_data.find("categories")
    if categories is not None:
        for category in categories.findall("category"):
            cat_id_text = category.attrib.get("cat_id")
            if cat_id_text is None:
                raise ValueError(f"ADB entry {adb_id_text} category is missing cat_id")
            category_items.append(
                AstroDatabankCategory(
                    cat_id=int(cat_id_text),
                    text=_text(category),
                    notes=category.attrib.get("catnotes"),
                )
            )

    return AstroDatabankRecord(
        adb_id=int(adb_id_text),
        name=name,
        gender=gender,
        rodden_rating=rodden_rating,
        data_type=data_type,
        jd_ut=jd_ut,
        birth_utc=birth_utc,
        has_alternative_birth_data=public.find("bdata_alt") is not None,
        short_biography=short_biography,
        categories=tuple(category_items),
    )


def _text(element: ET.Element | None) -> str:
    if element is None or element.text is None:
        return ""
    return " ".join(element.text.split())


def _optional_float(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError("ADB jd_ut must be finite")
    return parsed
