#!/usr/bin/env python3
"""Audit Didier Castille a00 family/wedding data for relationship research.

Downloads the public zip from tig12/g5-other at runtime and writes only compact
aggregate counts. No source rows are committed. This is data engineering, not
an astrology test.
"""
from __future__ import annotations

import csv
import io
import json
import urllib.request
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "reference" / "research" / "castille_a00_pair_audit_v1.json"
URL = "https://raw.githubusercontent.com/tig12/g5-other/main/castille/a00/a00.csv.zip"


def iv(row, key):
    try:
        v = int((row.get(key) or "0").strip())
        return v
    except Exception:
        return 0


def valid_date(y,m,d):
    try:
        date(y,m,d)
        return True
    except Exception:
        return False


def dob_tuple(row, prefix):
    if prefix == "m":
        d,m,y = iv(row,"JNAISM"),iv(row,"MNAISM"),iv(row,"ANAISM")
    else:
        d,m,y = iv(row,"JNAISP"),iv(row,"MNAISP"),iv(row,"ANAISP")
    return (y,m,d) if valid_date(y,m,d) else None


def wedding_tuple(row):
    d,m,y = iv(row,"JMAR"),iv(row,"MMAR"),iv(row,"AMAR")
    return (y,m,d) if valid_date(y,m,d) else None


def main():
    req = urllib.request.Request(URL, headers={"User-Agent":"humandesign-castille-audit/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = r.read()
    z = zipfile.ZipFile(io.BytesIO(raw))
    members = z.namelist()
    csv_names = [n for n in members if n.lower().endswith('.csv')]
    if len(csv_names) != 1:
        raise RuntimeError(f"expected one CSV, got {csv_names}")
    with z.open(csv_names[0]) as fb:
        text = io.TextIOWrapper(fb, encoding="utf-8-sig", errors="replace", newline="")
        reader = csv.DictReader(text)
        fields = reader.fieldnames or []
        row_count = 0
        both_parent_dob = 0
        with_wedding = 0
        all_three = 0
        plausible_all_three = 0
        mother_years=Counter(); father_years=Counter(); wedding_years=Counter()
        id_nonempty=0; id2_nonempty=0
        ids=set(); id2s=set(); pairkeys=set(); pairweddkeys=set(); pairweddidkeys=set()
        duplicate_pairwedd_rows=0
        seen_pairwedd=set()
        wedding_before_birth=0
        parent_age_diff_bins=Counter()
        marriage_age_m_bins=Counter(); marriage_age_f_bins=Counter()
        for row in reader:
            row_count += 1
            md = dob_tuple(row,"m"); fd = dob_tuple(row,"f"); wd = wedding_tuple(row)
            if md and fd:
                both_parent_dob += 1
                mother_years[md[0]] += 1; father_years[fd[0]] += 1
                pairkeys.add((md,fd))
            if wd:
                with_wedding += 1; wedding_years[wd[0]] += 1
            if md and fd and wd:
                all_three += 1
                pairwedd=(md,fd,wd)
                pairweddkeys.add(pairwedd)
                if pairwedd in seen_pairwedd: duplicate_pairwedd_rows += 1
                seen_pairwedd.add(pairwedd)
                mdate=date(*md); fdate=date(*fd); wdate=date(*wd)
                mage=(wdate-mdate).days/365.2425; fage=(wdate-fdate).days/365.2425
                if mage < 0 or fage < 0: wedding_before_birth += 1
                if 14 <= mage <= 85 and 14 <= fage <= 85:
                    plausible_all_three += 1
                    parent_age_diff_bins[str(int(abs((mdate-fdate).days)/365.2425)//5*5)] += 1
                    marriage_age_m_bins[str(int(mage)//5*5)] += 1
                    marriage_age_f_bins[str(int(fage)//5*5)] += 1
            idv=(row.get("id") or "").strip(); id2v=(row.get("id2") or "").strip()
            if idv:
                id_nonempty += 1; ids.add(idv)
            if id2v:
                id2_nonempty += 1; id2s.add(id2v)
            if md and fd and wd:
                pairweddidkeys.add((md,fd,wd,idv,id2v))

    def yrange(c):
        return [min(c),max(c)] if c else [None,None]
    summary={
        "status":"data_sufficiency_audit_only",
        "source":URL,
        "zip_bytes":len(raw),
        "zip_members":members,
        "csv_fields":fields,
        "row_count":row_count,
        "valid_records":{
            "both_parent_birth_dates":both_parent_dob,
            "wedding_date":with_wedding,
            "both_parent_birth_dates_and_wedding":all_three,
            "plausible_parent_ages_14_to_85_at_wedding":plausible_all_three,
            "wedding_before_parent_birth":wedding_before_birth,
        },
        "deduplication_diagnostics":{
            "unique_parent_birthdate_pairs":len(pairkeys),
            "unique_parent_birthdate_plus_wedding_tuples":len(pairweddkeys),
            "duplicate_rows_by_parent_birthdates_plus_wedding":duplicate_pairwedd_rows,
            "id_nonempty_rows":id_nonempty,
            "unique_id_values":len(ids),
            "id2_nonempty_rows":id2_nonempty,
            "unique_id2_values":len(id2s),
            "unique_parent_birthdate_wedding_id_id2_tuples":len(pairweddidkeys),
        },
        "date_ranges":{
            "mother_birth_year":yrange(mother_years),
            "father_birth_year":yrange(father_years),
            "wedding_year":yrange(wedding_years),
        },
        "coarse_distributions":{
            "absolute_parent_age_difference_5y_bins":dict(sorted(parent_age_diff_bins.items(), key=lambda kv:int(kv[0]))),
            "mother_age_at_wedding_5y_bins":dict(sorted(marriage_age_m_bins.items(), key=lambda kv:int(kv[0]))),
            "father_age_at_wedding_5y_bins":dict(sorted(marriage_age_f_bins.items(), key=lambda kv:int(kv[0]))),
        },
        "source_notice":[
            "Data are Didier Castille adaptations of INSEE files, not official INSEE files.",
            "Source README states the files are neither official nor scientifically valid and depend on Castille's good faith.",
            "Birth and wedding data are untimed.",
        ],
        "next_decision":"Use audit to freeze deduplication and independent untimed partner-selection / wedding-timing tests; do not inspect astrology before freeze."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2,sort_keys=True),flush=True)

if __name__=="__main__": main()
