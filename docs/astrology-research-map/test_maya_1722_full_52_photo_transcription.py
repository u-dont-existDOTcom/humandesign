#!/usr/bin/env python3
"""Check source-transcribed 1722 manuscript groups against independently fixed 260-day math.

Photographs copied from FAMSI are NOT in this repository; a source-table
reading is not evidence that anyone's personality is birth-day dependent.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import unittest

from maya_1722_five_by_52_reference import (
    all_reference_1722_almanac_groups, reference_1722_almanac_group
)

ROOT=Path(__file__).resolve().parent
B04=ROOT/"MAYA_1722_PRIMARY_FACSIMILE_HAND_READ_B04.json"
B05=ROOT/"MAYA_1722_B05_DIRECT_FOLIO_GROUPS_14_TO_52.txt"
B04_SHA256="b29a56bb39d355d55365a18beefa88b63fbad0fa24166520c3832477988a6ebf"

def source_groups():
    prior=json.loads(B04.read_text(encoding="utf-8"))
    original=[
        (v["group_serial"], v["coefficient"], tuple(v["names_in_photo_read_order"]), v["photo_id"])
        for v in prior["independently_read_5x52_group_rows"]
    ]
    new=[]
    for line in B05.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts=line.split("|")
        if len(parts)!=4:
            raise ValueError("Malformed hand-read source ledger row")
        serial,coefficient,names,page=parts
        new.append((int(serial),int(coefficient),tuple(names.split()),page))
    return original,new

def compare_to_reference(groups):
    bad=[]
    for serial,number,names,folio in groups:
        reference=reference_1722_almanac_group(serial)
        want=(reference[0].number, tuple(v.kiche_name for v in reference))
        if (number,names)!=want:
            bad.append((serial,folio,(number,names),want))
    return bad

class Complete1722PhotographicAlmanacTests(unittest.TestCase):
    def test_prior_immutable_source_file_sha(self):
        self.assertEqual(sha256(B04.read_bytes()).hexdigest(),B04_SHA256)

    def test_new_manual_transcriptions_are_the_missing_39_groups(self):
        earlier,new=source_groups()
        self.assertEqual(len(earlier),13)
        self.assertEqual(len(new),39)
        self.assertEqual([v[0] for v in earlier],list(range(1,14)))
        self.assertEqual([v[0] for v in new],list(range(14,53)))

    def test_complete_hand_read_group_order_matches_fixed_interval_engine(self):
        earlier,new=source_groups()
        self.assertEqual(compare_to_reference(earlier+new),[])

    def test_260_distinct_observed_coefficients_and_day_names(self):
        groups=sum((tuple((number,name) for name in names) for _,number,names,_ in sum(source_groups(),[])),())
        self.assertEqual(len(groups),260)
        self.assertEqual(len(set(groups)),260)
        self.assertEqual(len(Counter(k for _,k in groups)),20)
        self.assertEqual(len(Counter(n for n,_ in groups)),13)

    def test_document_photos_cover_folios_23_through_35(self):
        groups=sum(source_groups(),[])
        c=Counter(folio for *_,folio in groups)
        self.assertEqual(set(c),{f"body{page:04d}" for page in range(23,36)})
        self.assertEqual(c,Counter({f"body{page:04d}":4 for page in range(23,36)}))

    def test_all_numbered_days_appear_once_and_reference_positions_are_complete(self):
        flat=all_reference_1722_almanac_groups()
        self.assertEqual(len(flat),52)
        self.assertEqual({v.reference_position_1_based for group in flat for v in group},
                         set(range(1,261)))
        self.assertEqual({(v.number,v.kiche_name) for group in flat for v in group},
                         {(n,name) for _,n,names,_ in sum(source_groups(),[]) for name in names})

    def test_recorded_mutant_historical_name_is_detected(self):
        all_data=sum(source_groups(),[])
        mutant=list(all_data)
        serial,number,names,folio=mutant[17]
        bad=list(names)
        bad[2]="NO’J" if bad[2]!="NO’J" else "TOJ"
        mutant[17]=(serial,number,tuple(bad),folio)
        self.assertEqual(len(compare_to_reference(mutant)),1)
        self.assertEqual(compare_to_reference(mutant)[0][0],serial)

    def test_mutant_swapped_group_coefficients_are_detected(self):
        mutant=list(sum(source_groups(),[]))
        a=mutant[0]
        b=mutant[1]
        mutant[0]=(a[0],b[1],a[2],a[3])
        self.assertEqual([x[0] for x in compare_to_reference(mutant)],[1])

    def test_no_missing_or_duplicate_photo_group_after_prior_13(self):
        a,b=source_groups()
        ids=[r[0] for r in a+b]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(sorted(ids),list(range(1,53)))
        self.assertEqual(len({name for _,_,ns,_ in a+b for name in ns}),20)

    def test_source_text_does_not_claim_birth_predictions(self):
        src=B05.read_text(encoding="utf-8")
        self.assertIn("NOT calculated/generated",src)
        self.assertIn("older groups 1-13",src.lower())
        self.assertIn("body0035",src)
        self.assertFalse(any("horoscope" in v.lower() or "born" in v.lower()
                    for line in src.splitlines() if line and not line.startswith("#")
                    for v in line.split("|")[2:3]))

    def test_photo_sha_manifest_and_prior_overlap_match(self):
        file=ROOT/"MAYA_1722_B05_FACSIMILE_PHOTO_SHA256.txt"
        lines=[ln.split() for ln in file.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.startswith("#")]
        self.assertEqual(len(lines),9)
        self.assertEqual([row[0] for row in lines],
                         [f"body{n:04d}" for n in range(27,36)])
        for page,sha,size in lines:
            self.assertEqual(len(sha),64)
            int(sha,16)
            self.assertGreater(int(size),40000)
        previous=json.loads(B04.read_text(encoding="utf-8"))
        prior_sha={rec["id"]:rec["sha256"] for rec in previous["manuscript"]["visually_examined_image_sha256"]}
        for page,sha,_ in lines:
            if page in prior_sha:
                self.assertEqual(prior_sha[page],sha)

if __name__=="__main__":
    unittest.main()
