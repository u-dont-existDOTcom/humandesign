#!/usr/bin/env python3
"""Contract checks for the 2026-10-11 frozen historical mundane backtest."""
import csv
import importlib.util
import pathlib
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
FILE=ROOT/"scripts"/"research"/"mundane_historical_backtest_20261011.py"
spec=importlib.util.spec_from_file_location("mundane_historical_backtest", FILE)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class TestMundaneHistory(unittest.TestCase):
    def test_aspect_geometry(self):
        angles=(0,90,180)
        self.assertTrue(min(abs(358-360),abs(358))<=3) # angular wrap handled by minimum arc
        for separation in (1,89,179):
            self.assertLessEqual(min(abs(separation-a) for a in angles),3)
        self.assertEqual(len(h.PAIRS),6)

    def test_ert_onset_denominator(self):
        rows=[
            ["Alpha","AAA",1900,1],
            ["Alpha","AAA",1901,2], # start
            ["Alpha","AAA",1902,2], # continuation no new start
            ["Alpha","AAA",1903,1], # stabilizing
            ["Alpha","AAA",1904,3], # start
            ["Beta","BBB",1901,5], # missing prior year, not a new start
            ["Beta","BBB",1902,4],
            ["Beta","BBB",1903,4], # stable, eligible no onset
            ["Beta","BBB",1904,5], # start
            ["Gamma","CCC",1900,0],
            ["Gamma","CCC",1901,3], # dynamic -> dynamic not onset
            ["World","OWID_WRL",1901,3], # excluded
        ]
        old=h.SOURCES
        with tempfile.TemporaryDirectory() as d:
            h.SOURCES=pathlib.Path(d)
            with (h.SOURCES/"ERT_v16_OWID.csv").open("w",newline="") as f:
                w=csv.writer(f);w.writerow(("Entity","Code","Year","Political regime"));w.writerows(rows)
            out,meta=h.get_ert()
        h.SOURCES=old
        self.assertEqual(out[1901]["onsets"],1)
        self.assertEqual(out[1901]["eligible"],1)
        self.assertEqual(out[1902]["onsets"],0)
        self.assertEqual(out[1903]["eligible"],1)
        self.assertEqual(out[1904]["onsets"],2)
        self.assertEqual(out[1904]["eligible"],2)
        self.assertEqual(meta["countries"],3)

    def test_cow_earliest_participant_deduplicated(self):
        old=h.SOURCES
        with tempfile.TemporaryDirectory() as d:
            h.SOURCES=pathlib.Path(d)
            with (h.SOURCES/"Inter-StateWarData_v4.0.csv").open("w",newline="") as f:
                w=csv.writer(f);w.writerow(("WarNum","WarName","StartYear1"))
                w.writerows([("10","War A",1939),("10","War A",1941),("11","War B",1941),
                             ("12","War C",-9),("13","War D",1818),("14","War E",2005)])
            out,meta=h.get_wars()
        h.SOURCES=old
        self.assertEqual(out[1939],1)
        self.assertEqual(out[1941],1)
        self.assertEqual(meta["war_starts_in_scope"],2)

    def test_permutation_deterministic(self):
        a=[{"hard_pair_days":i*0.12,"rate_per_100_eligible":i*0.9,
            "start_year":1900+5*i,"end_year":1904+5*i,"era":1900,"period":str(i),
            "eligible_country_years":100,"onsets":i} for i in range(5)]
        result1=h.test(a,"rate_per_100_eligible")
        result2=h.test(a,"rate_per_100_eligible")
        self.assertEqual(result1,result2)
        self.assertEqual(result1["n_5yr_bins"],5)

if __name__=="__main__":unittest.main()
