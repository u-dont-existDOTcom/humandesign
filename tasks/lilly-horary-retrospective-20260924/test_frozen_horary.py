import unittest
from run_frozen_horary import verdict
class FrozenVerdictTests(unittest.TestCase):
 def test_present_wins(self): self.assertEqual(verdict([('DIRECT','PRESENT'),('TRANSLATION','INDETERMINATE')]),'YES')
 def test_all_absent(self): self.assertEqual(verdict([('DIRECT','ABSENT'),('TRANSLATION','ABSENT'),('COLLECTION','ABSENT')]),'NO')
 def test_indeterminate(self): self.assertEqual(verdict([('DIRECT','INDETERMINATE'),('TRANSLATION','ABSENT')]),'DEFER')
 def test_not_evaluable(self): self.assertEqual(verdict([],False),'DEFER')
 def test_blocker_not_scored_twice(self): self.assertEqual(verdict([('DIRECT','ABSENT'),('PROHIBITION','PRESENT')]),'NO')
 def test_translation(self): self.assertEqual(verdict([('DIRECT','ABSENT'),('TRANSLATION','PRESENT')]),'YES')
 def test_collection(self): self.assertEqual(verdict([('COLLECTION','PRESENT')]),'YES')
if __name__=='__main__':unittest.main()
