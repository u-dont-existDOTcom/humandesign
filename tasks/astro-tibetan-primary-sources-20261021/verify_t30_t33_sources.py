from pathlib import Path
from fractions import Fraction
import json,subprocess
R=Path(__file__).resolve().parent
def get(x): return json.loads((R/x).read_text())
a=get("batches/T30/CORNU_MEWA_PAPME_16_SOURCE_NOTES_V1.json")
b=get("batches/T32/HENNING_CALENDAR_15_NOTES_V1.json")
assert [z["id"] for z in a["source_notes"]]==[f"TIB-R{i:04d}" for i in range(282,298)]
assert [z["id"] for z in b["source_notes"]]==[f"TIB-R{i:04d}" for i in range(298,313)]
assert a["note_count"]==16 and b["note_count"]==15
assert "TIB-CONFLICT-006" in b["source_notes"][4]["source_issue"]
v=get("batches/T31/PAPME_CORNU_ERLEWINE_VARIANTS_V1.json")
assert v["Cornu"]["switch_input"]=="natal_sexagenary_year_polarity"
assert v["Erlewine"]["switch_input"]=="subject_sex"
q=get("batches/T33/HENNING_CALENDAR_MATH_PARITY_V1.json")
p=q["period_constants"]["phugpa_synodic_month_mixed_radix"]
d=p["digits"]
month=29+Fraction(d[0],60)+Fraction(d[1],3600)+Fraction(d[2],21600)+Fraction(d[3],21600*707)
assert month==Fraction(167025,5656)
n=q["period_identity"]
assert 39592*month==1169175==167025*7
assert n["source_printed_total_weeks"]==175682 and n["correct_total_weeks"]==167025
assert n["weekday_excess_weeks"]==8657
x=q["intercalation_zero"]["tsurphu_reference_mixed_lunar_mansions"]
deg=(Fraction(x[0])+Fraction(x[1],60)+Fraction(x[2],3600)+Fraction(x[3],21600)+Fraction(x[4],21600*67))*Fraction(360,27)
assert abs(float(deg)-6.573797678275291)<1e-9
for script in ("verify_t23_t29_obstacles.py","verify_t31_papme.py"):
 subprocess.run(["python3",str(R/script)],check=True,capture_output=True,text=True)
print("T30–T33 PASS: 31 notes; Cornu/Erlewine switch divergence; exact corrected Henning weeks; Tsurphu 6.574-degree calendar datum.")
