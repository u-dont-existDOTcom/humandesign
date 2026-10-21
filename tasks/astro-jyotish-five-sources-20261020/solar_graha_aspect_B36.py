"""Research-only Saravali Ch4 ordinary sign-aspect feasibility, not human validation."""
import itertools
from fractions import Fraction
ASPECTS={3:Fraction(1,4),10:Fraction(1,4),4:Fraction(1,2),8:Fraction(1,2),5:Fraction(3,4),9:Fraction(3,4),7:Fraction(1)}
MAX_INNER_SOLAR_SEPARATION={'Mercury':28,'Venus':48}
def whole_sign_minimum_gap(a,b):
    if type(a)!=int or type(b)!=int or not 0<=a<12 or not 0<=b<12: raise ValueError('12 zodiacal signs required')
    steps=min((b-a)%12,(a-b)%12)
    return 30*max(0,steps-1)
def aspect_fraction(source_sign,target_sign):
    whole_sign_minimum_gap(source_sign,target_sign)
    target_house=(target_sign-source_sign)%12+1
    return ASPECTS.get(target_house,Fraction(0))
def solar_aspect_possible(planet):
    cap=MAX_INNER_SOLAR_SEPARATION[planet]
    return [(sun,body) for sun,body in itertools.product(range(12),repeat=2)
            if whole_sign_minimum_gap(sun,body)<=cap and aspect_fraction(sun,body)>0]
if __name__=='__main__':
    assert not solar_aspect_possible('Mercury')
    assert solar_aspect_possible('Venus')
    assert whole_sign_minimum_gap(0,2)==30
    print({'Sun_aspects_Mercury_possibilities':0,'Sun_aspects_Venus_sign_pairs':len(solar_aspect_possible('Venus'))})
