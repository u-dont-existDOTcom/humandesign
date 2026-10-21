"""Source-specific sign-aspect models. No default; not a natal prediction engine.

Saravali uploaded English Ch4.32-33 reverses the trinal vs square fractions
compared with original Sanskrit Ch4.32 (CSU, older Jain printing), Jataka II.30,
and Portuguese BPHS line2311. B37 documents the comparison.
"""
import itertools
from fractions import Fraction
ASPECTS_BY_VERSION={
 'english_uploaded':{3:Fraction(1,4),10:Fraction(1,4),4:Fraction(1,2),8:Fraction(1,2),5:Fraction(3,4),9:Fraction(3,4),7:Fraction(1)},
 'sanskrit_restored':{3:Fraction(1,4),10:Fraction(1,4),5:Fraction(1,2),9:Fraction(1,2),4:Fraction(3,4),8:Fraction(3,4),7:Fraction(1)}
}
MAX_INNER_SOLAR_SEPARATION={'Mercury':28,'Venus':48}
def whole_sign_minimum_gap(a,b):
 if type(a) is not int or type(b) is not int or not 0<=a<12 or not 0<=b<12:raise ValueError('12 integer sign indices required')
 steps=min((b-a)%12,(a-b)%12)
 return 30*max(0,steps-1)
def aspect_fraction(source_sign,target_sign,*,version):
 whole_sign_minimum_gap(source_sign,target_sign)
 if version not in ASPECTS_BY_VERSION:raise ValueError('Explicit source version required')
 return ASPECTS_BY_VERSION[version].get((target_sign-source_sign)%12+1,Fraction(0))
def solar_aspect_possible(planet,*,version):
 if planet not in MAX_INNER_SOLAR_SEPARATION:raise ValueError('Only Mercury/Venus have these verified caps')
 if version not in ASPECTS_BY_VERSION:raise ValueError('Explicit source version required')
 cap=MAX_INNER_SOLAR_SEPARATION[planet]
 return [(sun,body) for sun,body in itertools.product(range(12),repeat=2)
         if whole_sign_minimum_gap(sun,body)<=cap and aspect_fraction(sun,body,version=version)>0]
if __name__=='__main__':
 for version in ASPECTS_BY_VERSION:
  assert not solar_aspect_possible('Mercury',version=version)
  assert len(solar_aspect_possible('Venus',version=version))==12
 print('Both source versions pass Sun/Mercury geometry; aspect strengths differ by edition.')
