from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/"batches/T31"))
from papme_variants import papme, four_years, square_for_mewa
data=json.loads((R/"batches/T31/PAPME_CORNU_ERLEWINE_VARIANTS_V1.json").read_text(encoding="utf-8"))
assert square_for_mewa(5)==((4,9,2),(3,5,7),(8,1,6))
assert square_for_mewa(8)==((7,3,5),(6,8,1),(2,4,9))
assert square_for_mewa(7)==((6,2,4),(5,7,9),(1,3,8))
for case in data["Cornu"]["examples"]:
 actual=four_years(case["natal_mewa"],"cornu_natal_year_polarity",natal_year_polarity=case["year_polarity"])
 assert actual==case["ages1_to4"],(case,actual)
for case in data["independent_difference_cases"]:
 cornu=four_years(case["natal_mewa"],"cornu_natal_year_polarity",natal_year_polarity=case["natal_year_polarity"])
 erlewine=four_years(case["natal_mewa"],"erlewine_subject_sex",subject_sex=case["sex"])
 assert cornu==case["cornu_ages1_to4"],(cornu,case)
 assert erlewine==case["erlewine_ages1_to4"],(erlewine,case)
 assert cornu!=erlewine
for i in range(1,10):
 for p in ("cornu_natal_year_polarity","erlewine_subject_sex"):
  kw={"natal_year_polarity":"masculine"} if p.startswith("cornu") else {"subject_sex":"male"}
  cycle=[papme(natal_mewa=i,age_tibetan_inclusive=age,policy=p,**kw) for age in range(1,10)]
  assert len(set(cycle))==9
  assert papme(natal_mewa=i,age_tibetan_inclusive=10,policy=p,**kw)==i
for bad in (
 dict(natal_mewa=1,age_tibetan_inclusive=1,policy="unknown"),
 dict(natal_mewa=1,age_tibetan_inclusive=0,policy="erlewine_subject_sex",subject_sex="female"),
 dict(natal_mewa=1,age_tibetan_inclusive=1,policy="cornu_natal_year_polarity"),
 dict(natal_mewa=1,age_tibetan_inclusive=1,policy="erlewine_subject_sex"),
 ):
 try: papme(**bad)
 except ValueError: pass
 else: raise AssertionError("missing fail-closed error: "+repr(bad))
print("T31 PAPME PASS: Cornu 1956/1957 fixtures, sex/year-polarity divergence, nine-position cycles, invalid-input gates")
