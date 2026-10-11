#!/usr/bin/env python3
"""Focused reproducibility/parse safeguards for the outer-vs-Saturn transfer study."""
import csv
import collections
import importlib.util
import pathlib
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
PATH=ROOT/"scripts/research/mundane_outer_saturn_transfer_20261011.py"
spec=importlib.util.spec_from_file_location("outer_saturn_transfer",PATH)
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def make(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

class TestOuterSaturnTransfer(unittest.TestCase):
    def test_accepted_coup_attempt_and_success(self):
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/"c.csv"
            make(f,["country","ccode","year","month","day","coup"],[
                dict(country="A",ccode="11",year=1950,month=1,day=1,coup=1),
                dict(country="A",ccode="11",year=1950,month=1,day=2,coup=2),
                dict(country="A",ccode="11",year=2025,month=1,day=2,coup=2)])
            a,s,meta=p.read_coups(f)
            self.assertEqual((a[1950],s[1950],meta["events_in_scope"]), (2,1,2))
    def test_duplicate_coup_key_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/"c.csv"
            row=dict(country="A",ccode="11",year=1950,month=1,day=1,coup=1)
            make(f,list(row),[row,row])
            with self.assertRaisesRegex(ValueError,"Duplicated coup"):
                p.read_coups(f)
    def test_onset_one_with_separate_conflict_id_counts_separately(self):
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/"u.csv"
            make(f,["abc","year","onset1","conflict_ids"],[
                dict(abc="AAA",year=1975,onset1=1,conflict_ids=101),
                dict(abc="AAA",year=1975,onset1=1,conflict_ids=102),
                dict(abc="AAA",year=1975,onset1=0,conflict_ids=103),
                dict(abc="AAA",year=1948,onset1=1,conflict_ids=104)])
            a,meta=p.read_conflicts(f)
            self.assertEqual((a[1975],meta["onsets_in_scope"]), (2,2))
    def test_onset_duplicate_conflict_key_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            f=pathlib.Path(d)/"u.csv"
            row=dict(abc="AAA",year=1975,onset1=1,conflict_ids=101)
            make(f,list(row),[row,row])
            with self.assertRaisesRegex(ValueError,"Duplicate UCDP"):
                p.read_conflicts(f)
    def test_original_annual_index_and_aggregate(self):
        annual=p.load_astro()
        coup={};success={};conf={}
        blocks=p.aggregate(annual,collections.Counter(coup),collections.Counter(success),collections.Counter(conf))
        self.assertEqual((len(blocks),blocks[0]["period"],blocks[-1]["period"]),(15,"1950-1954","2020-2024"))
        for b in blocks:
            self.assertAlmostEqual(b["outer_minus_saturn"],b["outer_hard"]-b["saturn_hard"],12)
    def test_seed_and_frozen_permutations(self):
        self.assertEqual((p.old.SEED,p.old.COUNT_PERM),(20261012,20000))
    def test_both_independent_sources_have_expected_content_hashes(self):
        import hashlib
        if not all((p.SRC/name).exists() for name in p.FILES):
            self.skipTest("Original licensed/copyrighted snapshots are not tracked in public Git; run --fetch.")
        for name,meta in p.FILES.items():
            digest=hashlib.sha256((p.SRC/name).read_bytes()).hexdigest()
            self.assertEqual(digest,meta["sha256"])
if __name__=="__main__":
    import collections
    unittest.main()
