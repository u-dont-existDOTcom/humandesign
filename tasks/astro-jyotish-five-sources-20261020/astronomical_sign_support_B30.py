"""Research-only same-sign feasibility sweep. Does not use birth/person data.

Source: Saravali 19.8; see SARAVALI_CONJUNCTION_SKY_SUPPORT_B30.json.
This uses Moshier ephemeris for exploratory support, NEVER production Swiss .se1.
Run: python astronomical_sign_support_B30.py [--events] [--check]
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations
import json
import swisseph as swe

BODIES = (('Sun',swe.SUN),('Moon',swe.MOON),('Mars',swe.MARS),
          ('Mercury',swe.MERCURY),('Jupiter',swe.JUPITER),
          ('Venus',swe.VENUS),('Saturn',swe.SATURN))
FLAGS = swe.FLG_MOSEPH | swe.FLG_SIDEREAL
BEGIN, END = (1800,1,1), (2200,1,1)

def coordinates(jd: float) -> dict[str, float]:
    result = {}
    for name, body in BODIES:
        xx, returned = swe.calc_ut(jd, body, FLAGS)
        if not ((returned & swe.FLG_MOSEPH) and (returned & swe.FLG_SIDEREAL)):
            raise RuntimeError(f'Wrong astronomy flag: {returned}')
        result[name] = xx[0] % 360
    return result

def main(*, events: bool = False, check: bool = False) -> dict:
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    first = swe.julday(*BEGIN, 0.0, swe.GREG_CAL)
    last = swe.julday(*END, 0.0, swe.GREG_CAL)
    exact = Counter()
    candidate_five = Counter()
    episodes: list[dict] = []
    max_group = 0
    for step in range(round(last-first)):
        jd = first + step
        pos = coordinates(jd)
        by_sign = [[n for n in pos if int(pos[n]//30) == sign]
                   for sign in range(12)]
        max_group = max(max_group, *(len(group) for group in by_sign))
        for sign, group in enumerate(by_sign):
            if len(group) < 5:
                continue
            group = sorted(group)
            exact[len(group)] += 1
            for subset in combinations(group, 5):
                candidate_five['|'.join(subset)] += 1
            yy, mm, dd, _ = swe.revjul(jd, swe.GREG_CAL)
            day = f'{yy:04d}-{mm:02d}-{dd:02d}'
            key = '|'.join(group)
            if (episodes and episodes[-1]['sign_index'] == sign and
                episodes[-1]['group'] == key and episodes[-1]['last_jd'] == jd - 1):
                episodes[-1]['end'] = day
                episodes[-1]['days'] += 1
                episodes[-1]['last_jd'] = jd
            else:
                episodes.append({'start':day,'end':day,'sign_index':sign,
                                 'group':key,'days':1,'last_jd':jd})
    for episode in episodes:
        del episode['last_jd']
    durations = Counter(len(ep['group'].split('|')) for ep in episodes)
    seven = [ep for ep in episodes if len(ep['group'].split('|')) == 7]
    result = {
        'schema_version':1, 'date_range_utc':'1800-01-01 inclusive to 2200-01-01 exclusive',
        'daily_sample_utc':'00:00', 'sidereal':'Lahiri',
        'engine':'Moshier built into pyswisseph '+str(swe.version),
        'returned_mode_required':'FLG_MOSEPH | FLG_SIDEREAL',
        'days_sampled':round(last-first), 'exactly_five_six_seven':{str(k):exact[k] for k in (5,6,7)},
        'episodes_by_size':{str(k):durations[k] for k in (5,6,7)},
        'maximum_same_sign_occupancy':max_group,
        'five_planet_subsets_ever_observed':len(candidate_five),
        'seven_planet_episodes':seven,
        'scope':'Exploratory 30-degree sidereal sign co-location only; not narrow conjunction, not house-system parity, not human prediction.'
    }
    if check:
        assert result['days_sampled']==146097
        assert result['exactly_five_six_seven']=={'5':1274,'6':106,'7':4}
        assert result['episodes_by_size']=={'5':444,'6':42,'7':2}
        assert result['five_planet_subsets_ever_observed']==21
        assert [(x['start'],x['end'],x['sign_index']) for x in seven] == [
            ('1821-04-02','1821-04-03',11),('1962-02-04','1962-02-05',9)]
    if events:
        result['all_episodes'] = episodes
    return result

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--events', action='store_true', help='Print full ~488 episode ledger')
    ap.add_argument('--check', action='store_true', help='Assert expected reproducibility counts')
    args = ap.parse_args()
    print(json.dumps(main(events=args.events,check=args.check),ensure_ascii=False,indent=2))
