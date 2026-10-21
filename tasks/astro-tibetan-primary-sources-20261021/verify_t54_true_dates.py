#!/usr/bin/env python3
"""Source-derived Phugpa/Tsurphu traditional date mathematics checks (Janson).
These are arithmetic and calendar parity checks, NOT astrological validation.
"""
from datetime import date, datetime
from pathlib import Path
import importlib.util
import subprocess
import sys
import json

ROOT = Path(__file__).resolve().parent
CODE = ROOT/"batches/T54/tibetan_true_dates.py"
spec = importlib.util.spec_from_file_location("tibetan_true_dates", CODE)
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

def raises(call, *args, **kwargs):
    try:
        call(*args, **kwargs)
    except ValueError:
        return True
    raise AssertionError(f"Improperly accepted {call.__name__}: {args} {kwargs}")

PHUGPA_LOSAR = {
    1950:date(1950,2,17),1951:date(1951,2,7),
    1984:date(1984,3,3),1985:date(1985,2,20),
    2000:date(2000,2,6),2023:date(2023,2,21),
    2024:date(2024,2,10),2025:date(2025,2,28),
    2026:date(2026,2,18),2027:date(2027,2,7),
}
for year,expected in PHUGPA_LOSAR.items():
    for epoch in (806,1927,1987):
        assert mod.losar_date(year,system="phugpa",epoch=epoch,anomaly_policy="rounded")==expected,(year,epoch)

assert mod.losar_date(2000,system="phugpa",epoch=1987,anomaly_policy="rounded")==date(2000,2,6)
assert mod.gregorian_day_to_tibetan(date(1985,2,19),
    system="phugpa",epoch=1987,anomaly_policy="rounded").year == 1984
assert mod.gregorian_day_to_tibetan(date(1985,2,20),
    system="phugpa",epoch=1987,anomaly_policy="rounded").year == 1985
cornu=mod.gregorian_day_to_tibetan(date(1950,11,15),
     system="phugpa",epoch=1987,anomaly_policy="rounded")
assert (cornu.year,cornu.month,cornu.lunar_day)==(1950,10,6)

# Different epochs in same tradition must lead to same civil calendar.
for system,epochs in (("phugpa",(806,1927,1987)),("tsurphu",(1732,1852))):
    for year in (1950,1984,1985,2000,2024,2025,2026,2027):
        assert len({mod.losar_jdn(year,system=system,epoch=e,
                       anomaly_policy="rounded") for e in epochs})==1,(system,year)
        for month in (1,2,6,11,12):
            instances=[mod.month_instances(year,month,system=system,epoch=e)
                       for e in epochs]
            assert len({len(inst) for inst in instances})==1,(system,year,month)
            for ordinal in range(len(instances[0])):
                samples=[mod.true_date_jdn(30,inst[ordinal][0],system=system,epoch=e,
                                          anomaly_policy="rounded")
                         for e,inst in zip(epochs,instances)]
                assert len(set(samples))==1,(system,year,month,samples)

# Calendar mapping must cover *every* Gregorian civil day exactly once,
# and distinguish skipped and repeated Tibetan labels.
type_counts={}
for system,epoch in (("phugpa",1987),("tsurphu",1852)):
    for year in (1950,1984,1985,2000,2024,2026):
        present=[]
        skipped=0
        repeats=0
        for month in range(1,13):
            for n,is_leap in mod.month_instances(year,month,system=system,epoch=epoch):
                days=mod.month_days(year,month,leap_month=is_leap,
                    system=system,epoch=epoch,anomaly_policy="rounded")
                assert 30<=len(days)<=35
                for d in days:
                    if d.skipped:
                        skipped+=1
                        assert d.jdn is None and d.gregorian_date is None
                        raises(mod.tibetan_date_to_jdn,year,month,d.lunar_day,
                               leap_month=is_leap,leap_day=False,
                               system=system,epoch=epoch,anomaly_policy="rounded")
                    else:
                        present.append(d)
                        assert mod.tibetan_date_to_jdn(year,month,d.lunar_day,
                                 leap_month=is_leap,leap_day=d.leap_day,system=system,
                                 epoch=epoch,anomaly_policy="rounded")==d.jdn
                        assert d.gregorian_date is not None
                    if d.leap_day: repeats+=1
        jd=[r.jdn for r in present]
        assert len(jd)==len(set(jd)),(system,year,"duplicate JDN")
        assert jd==list(range(mod.losar_jdn(year,system=system,epoch=epoch,
                                          anomaly_policy="rounded"),
                              mod.losar_jdn(year+1,system=system,epoch=epoch,
                                          anomaly_policy="rounded"))),(system,year)
        assert skipped>0 and repeats>0,(system,year,skipped,repeats)
        for tested in (present[0],present[12],present[len(present)//2],
                       present[-1],next(d for d in present if d.leap_day)):
            back=mod.jdn_to_tibetan(tested.jdn,system=system,epoch=epoch,
                                   anomaly_policy="rounded")
            assert back==tested,(system,year,tested,back)
        type_counts[(system,year)]=(skipped,repeats,len(jd))

# Source-stated two plausible anomaly increment variants are not silently mixed.
# Dates here should be fractional but the variants differ for ordinary tithis.
from fractions import Fraction
a=mod.true_date(17,1234,system="phugpa",epoch=1987,anomaly_policy="rounded")
b=mod.true_date(17,1234,system="phugpa",epoch=1987,anomaly_policy="dharmashri_exact")
assert type(a) is Fraction and type(b) is Fraction and a!=b
raises(mod.losar_date,1985,system="unknown",epoch=1987,anomaly_policy="rounded")
raises(mod.losar_date,1985,system="phugpa",epoch=1852,anomaly_policy="rounded")
raises(mod.losar_date,1985,system="phugpa",epoch=1987,anomaly_policy="unselected")
raises(mod.true_date,31,1234,system="phugpa",epoch=1987,anomaly_policy="rounded")
raises(mod.month_instances,1985,13,system="phugpa",epoch=1987)
raises(mod.gregorian_day_to_tibetan,datetime(1985,2,20),
       system="phugpa",epoch=1987,anomaly_policy="rounded")
# Source T53 symbolic attributes remain accepted and unchanged.
x=subprocess.run(["python3",str(ROOT/"verify_t51_t53_calendar.py")],
                 text=True,capture_output=True,check=True)
assert "prior 447 notes unchanged" in x.stdout
print("T54 TRUE-DATE SOURCE PASS: exact rational Phugpa/Tsurphu epochs, 10 published Losar dates,")
print("  full civil-day continuity for 12 calendar-years including skipped and duplicated days,")
print("  independent arithmetic under five epoch constants, human predictive results: ZERO.")
print("DAY_COUNTS",type_counts)
