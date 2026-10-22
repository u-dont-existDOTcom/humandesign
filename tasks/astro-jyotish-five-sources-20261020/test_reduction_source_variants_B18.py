import unittest
from reduction_source_variants_B18 import (
    DUAL_LORD_PAIRS,
    SIGNS,
    reduce_same_lord_pair,
    reduce_same_lord_signs,
    reduce_trines,
)


class TestScriptAsResearchFixture(unittest.TestCase):
    def test_names_and_pairs(self):
        self.assertEqual(len(SIGNS), 12)
        self.assertEqual(len(DUAL_LORD_PAIRS), 5)
        self.assertEqual(len(set(i for pair in DUAL_LORD_PAIRS for i in pair)), 10)
        self.assertNotIn(3, set(i for pair in DUAL_LORD_PAIRS for i in pair))
        self.assertNotIn(4, set(i for pair in DUAL_LORD_PAIRS for i in pair))

    def test_pair_agreements(self):
        cases = [
            (0, 4, False, True, (0, 4)),
            (3, 0, True, False, (3, 0)),
            (4, 8, True, True, (4, 8)),
            (3, 3, False, False, (0, 0)),
            (3, 3, True, False, (3, 0)),
            (3, 3, False, True, (0, 3)),
            (5, 2, True, False, (5, 0)),
            (2, 5, False, True, (0, 5)),
        ]
        for x, y, occupied_x, occupied_y, expected in cases:
            for method in ("equalize", "difference"):
                with self.subTest(method=method, case=(x, y, occupied_x, occupied_y)):
                    self.assertEqual(reduce_same_lord_pair(x, y, first_occupied=occupied_x,
                       second_occupied=occupied_y, method=method), expected)

    def test_disagreements_occupied_lower(self):
        self.assertEqual(reduce_same_lord_pair(2,5,first_occupied=True,second_occupied=False,
            method="equalize"),(2,2))
        self.assertEqual(reduce_same_lord_pair(2,5,first_occupied=True,second_occupied=False,
            method="difference"),(2,3))
        self.assertEqual(reduce_same_lord_pair(5,2,first_occupied=False,second_occupied=True,
            method="equalize"),(2,2))
        self.assertEqual(reduce_same_lord_pair(5,2,first_occupied=False,second_occupied=True,
            method="difference"),(3,2))

    def test_disagreements_both_empty(self):
        self.assertEqual(reduce_same_lord_pair(2,5,first_occupied=False,second_occupied=False,
            method="equalize"),(2,2))
        self.assertEqual(reduce_same_lord_pair(2,5,first_occupied=False,second_occupied=False,
            method="difference"),(0,3))

    def test_nonincrease_and_swapping(self):
        for method in ("equalize", "difference"):
            for x in range(9):
                for y in range(9):
                    for a in (False, True):
                        for b in (False, True):
                            result = reduce_same_lord_pair(x,y,first_occupied=a,
                                second_occupied=b, method=method)
                            self.assertTrue(0 <= result[0] <= x and 0 <= result[1] <= y)
                            swapped = reduce_same_lord_pair(y,x,first_occupied=b,
                                second_occupied=a,method=method)
                            self.assertEqual(result, swapped[::-1])

    def test_trikona_examples_and_skip(self):
        for x,y,z,expected in [
            (0,3,6,(0,3,6)),(2,3,6,(0,1,4)),
            (4,4,4,(0,0,0)),(3,7,3,(0,4,0))
        ]:
            counts=[0]*12
            counts[0],counts[4],counts[8]=x,y,z
            result=reduce_trines(counts)
            self.assertEqual(tuple(result[k] for k in (0,4,8)),expected)

    def test_full_pair_no_dasha_or_chart(self):
        counts = [2,3,0,2,4,1,5,5,3,5,4,2]
        # Occupancy only in Aries for the Aries-Scorpio pair.
        eq=reduce_same_lord_signs(counts,occupied_sign_indices=[0],method="equalize")
        dif=reduce_same_lord_signs(counts,occupied_sign_indices=[0],method="difference")
        self.assertEqual(eq[0],2)
        self.assertEqual(eq[7],2)
        self.assertEqual(dif[0],2)
        self.assertEqual(dif[7],3)
        self.assertEqual(eq[3:5],(2,4))
        self.assertEqual(dif[3:5],(2,4))
        self.assertNotEqual(eq,dif)

    def test_fail_closed(self):
        with self.assertRaises(ValueError):
            reduce_same_lord_pair(3,4,first_occupied=True,second_occupied=False,method="unknown")
        with self.assertRaises(ValueError):
            reduce_same_lord_signs([1]*11,occupied_sign_indices=[],method="equalize")
        with self.assertRaises(ValueError):
            reduce_trines([1]*11)
        with self.assertRaises(ValueError):
            reduce_same_lord_pair(-1,2,first_occupied=False,second_occupied=False,method="equalize")
        with self.assertRaises(ValueError):
            reduce_same_lord_signs([1]*12,occupied_sign_indices=[12],method="equalize")


if __name__ == "__main__":
    unittest.main(verbosity=2)
