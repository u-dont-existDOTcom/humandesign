#!/usr/bin/env python3
"""Batch exploratory cohort experiment. Not an individual criminal-risk tool.

Run with --input ../murderer_birth_pattern_pilot_20261003/paired_cohort.csv
and --out <directory>. All source labels were previously exposed. No model is
exported or admitted for deployment. Nested CV is internal development evidence.
"""
from __future__ import annotations
import argparse
import calendar
import csv
import hashlib
import json
import math
import re
import unicodedata
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

import numpy as np
import scipy
import sklearn
import swisseph as swe
from dateutil.parser import parse
from scipy.optimize import linear_sum_assignment
from scipy.special import expit
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, export_text

SEED = 20261003
MASTERS = {11, 22, 33}
FAMILIES = ['dob_num', 'listed_name_num', 'num_combined', 'astro_aspects', 'fusion']
MODELS = ['tree2', 'tree4', 'boost2', 'boost3', 'rbf', 'extra']
PLANETS = [('Sun', swe.SUN), ('Mercury', swe.MERCURY), ('Venus', swe.VENUS),
           ('Mars', swe.MARS), ('Jupiter', swe.JUPITER), ('Saturn', swe.SATURN),
           ('Uranus', swe.URANUS), ('Neptune', swe.NEPTUNE), ('Pluto', swe.PLUTO)]
SOURCE_BLOB = 'fca43841a83f6efcfe4d1dde66d6887335954c3c'
RETURN_FLAGS: set[int] = set()


def reduce_number(n: int) -> int:
    while n > 9 and n not in MASTERS:
        n = sum(int(x) for x in str(n))
    return n


def categorical(out: dict, key: str, value: int, values=None) -> None:
    for v in (list(range(1, 10)) + [11, 22, 33] if values is None else values):
        out[f'{key}={v}'] = float(value == v)


def normalize_name(s: str) -> str:
    s = s.replace('ß', 'ss').replace('Æ', 'AE').replace('æ', 'ae')
    s = s.replace('Ø', 'O').replace('ø', 'o').replace('Ł', 'L').replace('ł', 'l')
    s = s.replace('ı', 'i')
    return ''.join(c for c in unicodedata.normalize('NFKD', s).upper() if 'A' <= c <= 'Z')


@lru_cache(None)
def dob_features(d: date) -> dict:
    yr = reduce_number(sum(int(x) for x in str(d.year)))
    vals = {
        'component_path': reduce_number(reduce_number(d.month) + reduce_number(d.day) + yr),
        'digit_sum_path': reduce_number(sum(int(c) for c in f'{d.year:04d}{d.month:02d}{d.day:02d}')),
        'birth_day': reduce_number(d.day), 'attitude': reduce_number(d.month + d.day),
        'year_root': yr,
    }
    out: dict = {}
    for key, val in vals.items():
        categorical(out, key, val)
    categorical(out, 'month', d.month, range(1, 13))
    return out


@lru_cache(None)
def name_features(s: str) -> dict:
    letters = normalize_name(s)
    if not letters:
        raise ValueError('Name contains no supported letters; do not impute.')
    number = lambda c: (ord(c) - ord('A')) % 9 + 1
    vals = {'expression': sum(number(c) for c in letters),
            'vowels': sum(number(c) for c in letters if c in 'AEIOU'),
            'consonants': sum(number(c) for c in letters if c not in 'AEIOU')}
    out: dict = {}
    for key, val in vals.items():
        categorical(out, key, reduce_number(val), [0] + list(range(1, 10)) + [11, 22, 33])
    return out


@lru_cache(None)
def astro_features(d: date) -> dict:
    jd = swe.julday(d.year, d.month, d.day, 0.)
    values = []
    speeds = []
    for hour in np.linspace(-14., 36., 9):
        lons, vel = [], []
        for _, p in PLANETS:
            xx, flags = swe.calc_ut(jd + hour / 24., p, swe.FLG_MOSEPH | swe.FLG_SPEED)
            if not (flags & swe.FLG_MOSEPH):
                raise RuntimeError(f'Unexpected ephemeris mode: {flags}')
            RETURN_FLAGS.add(int(flags))
            lons.append(xx[0] % 360.)
            vel.append(xx[3])
        values.append(lons)
        speeds.append(vel)
    a = np.asarray(values)
    signs = (a // 30).astype(int)
    out: dict = {}
    for i, (name, _) in enumerate(PLANETS):
        out[name + '_sin'] = float(np.sin(np.deg2rad(a[:, i])).mean())
        out[name + '_cos'] = float(np.cos(np.deg2rad(a[:, i])).mean())
        out[name + '_retrograde_fraction'] = float((np.asarray(speeds)[:, i] < 0).mean())
        for sign in range(12):
            out[f'{name}_sign{sign}_fraction'] = float((signs[:, i] == sign).mean())
    for modulus, label in [(3, 'modality'), (4, 'element')]:
        for v in range(modulus):
            out[f'{label}_{v}_count'] = float((signs % modulus == v).sum(axis=1).mean())
    for i in range(len(PLANETS)):
        for j in range(i + 1, len(PLANETS)):
            sep = np.abs((a[:, i] - a[:, j] + 180.) % 360. - 180.)
            for angle in [0, 60, 90, 120, 180]:
                orb = 8. if angle in [0, 180] else 6.
                proximity = np.maximum(0., 1. - np.abs(sep - angle) / orb)
                out[f'{PLANETS[i][0]}_{PLANETS[j][0]}_{angle}deg'] = float(proximity.mean())
    return out


def conventional_features(r: dict, family: str) -> dict:
    if family == 'year_only':
        return {'year': float(r['date'].year)}
    s = r['name']; letters = normalize_name(s)
    return {'initials': float(len(re.findall(r'\b[A-Z]\.', s))),
            'letters': float(len(letters)), 'tokens': float(len(s.split())),
            'vowel_fraction': sum(c in 'AEIOU' for c in letters) / max(1, len(letters)),
            'non_ascii': float(sum(ord(c) > 127 for c in s)),
            'punctuation': float(sum(not c.isalnum() and not c.isspace() for c in s))}


def feature_dict(r: dict, family: str) -> dict:
    if family in ['year_only', 'name_format']:
        return conventional_features(r, family)
    out = {}
    if family in ['dob_num', 'num_combined', 'fusion']:
        out.update({'dob_' + k: v for k, v in dob_features(r['date']).items()})
    if family in ['listed_name_num', 'num_combined', 'fusion']:
        out.update({'name_' + k: v for k, v in name_features(r['name']).items()})
    if family in ['astro_aspects', 'fusion']:
        out.update({'astro_' + k: v for k, v in astro_features(r['date']).items()})
    return out


def matrix(rows: list[dict], family: str):
    ds = [feature_dict(r, family) for r in rows]
    cols = sorted(ds[0])
    assert all(sorted(d) == cols for d in ds)
    return np.asarray([[d[c] for c in cols] for d in ds]), cols


def model(name: str):
    if name.startswith('tree'):
        return DecisionTreeClassifier(max_depth=int(name[-1]), min_samples_leaf=4,
                                      random_state=SEED)
    if name.startswith('boost'):
        return GradientBoostingClassifier(n_estimators=60, learning_rate=.05,
                                          max_depth=int(name[-1]), min_samples_leaf=4,
                                          random_state=SEED)
    if name == 'rbf':
        return make_pipeline(StandardScaler(), SVC(C=3., gamma='scale'))
    if name == 'extra':
        return ExtraTreesClassifier(n_estimators=80, min_samples_leaf=3,
                                    max_features=.7, random_state=SEED, n_jobs=1)
    if name == 'logistic':
        return make_pipeline(StandardScaler(), LogisticRegression(C=1., solver='liblinear'))
    raise ValueError(name)


def score(m, x):
    return m.predict_proba(x)[:, 1] if hasattr(m, 'predict_proba') else expit(m.decision_function(x))


def group_splits(groups: np.ndarray, n: int, seed: int):
    unique = np.unique(groups)
    if len(unique) < n:
        raise ValueError('Too few independent groups.')
    cv = KFold(n_splits=n, shuffle=True, random_state=seed)
    for a, b in cv.split(unique):
        yield np.flatnonzero(np.isin(groups, unique[a])), np.flatnonzero(np.isin(groups, unique[b]))


def summary(y, p):
    return {'auc': float(roc_auc_score(y, p)),
            'balanced_accuracy': float(balanced_accuracy_score(y, p >= .5))}


def mean_metrics(items):
    return {key: float(np.mean([x[key] for x in items])) for key in ['auc', 'balanced_accuracy']}


def nested(rows: list[dict], groups: np.ndarray, families: list[str], repeats: int = 3) -> dict:
    mats = {f: matrix(rows, f)[0] for f in families}
    y = np.asarray([r['y'] for r in rows])
    results = {f: [] for f in families + ['selected_pipeline']}
    choices = []
    for rep in range(repeats):
        predictions = {f: np.zeros(len(y)) for f in results}
        for fold, (train, test) in enumerate(group_splits(groups, 5, SEED + rep)):
            best_each = {}
            for f in families:
                x = mats[f]; ranked = []
                for name in MODELS:
                    aucs = []
                    for ia, ib in group_splits(groups[train], 3, SEED + 100 + rep * 10 + fold):
                        a, b = train[ia], train[ib]
                        m = model(name); m.fit(x[a], y[a])
                        aucs.append(roc_auc_score(y[b], score(m, x[b])))
                    ranked.append((float(np.mean(aucs)), name))
                # Fixed ordering breaks exact ties; no outcome-guided tie changes.
                best_auc, best_name = max(ranked, key=lambda z: z[0])
                best_each[f] = (best_auc, best_name)
                m = model(best_name); m.fit(x[train], y[train])
                predictions[f][test] = score(m, x[test])
            chosen = max(families, key=lambda f: best_each[f][0])
            predictions['selected_pipeline'][test] = predictions[chosen][test]
            choices.append({'repeat': rep, 'fold': fold, 'family': chosen,
                            'model': best_each[chosen][1], 'inner_auc': best_each[chosen][0]})
        for f in results:
            results[f].append(summary(y, predictions[f]))
        print('NESTED_REPEAT', rep, {f: results[f][-1] for f in results}, flush=True)
    return {'mean': {f: mean_metrics(v) for f, v in results.items()},
            'repetitions': results, 'selection_log': choices,
            'feature_counts': {f: mats[f].shape[1] for f in families}}


def baselines(rows, groups):
    y = np.asarray([r['y'] for r in rows]); out = {}
    for family, mn in [('year_only', 'logistic'), ('name_format', 'tree2')]:
        x, _ = matrix(rows, family); metrics = []
        for rep in range(3):
            p = np.zeros(len(y))
            for a, b in group_splits(groups, 5, SEED + rep):
                m = model(mn);m.fit(x[a],y[a]);p[b]=score(m,x[b])
            metrics.append(summary(y,p))
        out[family] = {'mean': mean_metrics(metrics), 'repetitions': metrics}
    return out


def load_pairs(path):
    rows = list(csv.DictReader(path.open(encoding='utf-8')))
    pairs = []
    for r in rows:
        o = {'name': r['offender_name'], 'date': parse(r['offender_dob']).date(),
             'sex': r['offender_sex'], 'y': 1}
        c = {'name': r['control_name'], 'date': parse(r['control_dob']).date(),
             'sex': {'Male': 'M', 'Female': 'F'}.get(r['control_sex'], 'U'), 'y': 0}
        pairs.append((o, c))
    assert len({p[0]['name'] for p in pairs}) == len(pairs)
    assert len({p[1]['name'] for p in pairs}) == len(pairs)
    return pairs


def exact_year_pairs(pairs):
    n = len(pairs); cost = np.full((n, n), 10000.)
    rng = np.random.default_rng(SEED)
    for i, (o, _) in enumerate(pairs):
        for j, (_, c) in enumerate(pairs):
            if o['date'].year == c['date'].year and (o['sex'] == 'U' or o['sex'] == c['sex']):
                cost[i, j] = (1. if o['sex'] == 'U' else 0.) + rng.uniform(0., .001)
    ii, jj = linear_sum_assignment(cost)
    out = [(pairs[i][0].copy(), pairs[j][1].copy()) for i, j in zip(ii, jj) if cost[i, j] < 100.]
    assert all(o['date'].year == c['date'].year for o, c in out)
    return out


def make_rows(pairs, by_year=False):
    rows = []; groups = []
    for i, (o, c) in enumerate(pairs):
        rows.extend([o.copy(), c.copy()])
        group = o['date'].year if by_year else i
        groups.extend([group, group])
    return rows, np.asarray(groups)


def fitting_diagnostic(rows):
    y = np.asarray([r['y'] for r in rows]); x, cols = matrix(rows, 'fusion')
    out = {}
    for depth in [2, 4, None]:
        m = DecisionTreeClassifier(max_depth=depth, min_samples_leaf=1, random_state=SEED)
        m.fit(x, y)
        out[str(depth)] = {**summary(y, score(m, x)), 'leaves': int(m.get_n_leaves())}
        if depth == 4:
            out['depth4_rule_text'] = export_text(m, feature_names=cols, decimals=3)
    rng = np.random.default_rng(SEED)
    vals = []
    for _ in range(10):
        yy = y.copy()
        for i in range(0, len(y), 2):
            if rng.random() < .5:
                yy[i:i+2] = yy[i:i+2][::-1]
        m = DecisionTreeClassifier(random_state=SEED);m.fit(x,yy)
        vals.append(summary(yy,score(m,x)))
    out['shuffled_label_apparent_fit'] = vals
    return out


def self_tests():
    assert reduce_number(11) == 11 and reduce_number(29) == 11
    assert reduce_number(33) == 33 and reduce_number(34) == 7
    assert normalize_name('Hâle') == 'HALE' and normalize_name('Çolak') == 'COLAK'
    assert len(astro_features(date(1960, 1, 1))) == 322
    g = np.repeat(np.arange(20),2)
    for a,b in group_splits(g,5,SEED):
        assert not set(g[a]) & set(g[b])
    print('SELF_TESTS_PASS', flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--repeats',type=int,default=3)
    p.add_argument('--calendar-draws',type=int,default=0)
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    data=args.input.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob != SOURCE_BLOB:
        raise ValueError('Input is not the frozen source CSV.')
    self_tests(); pairs=load_pairs(args.input); matched=exact_year_pairs(pairs)
    yr_o=np.array([o['date'].year for o,c in pairs]);yr_c=np.array([c['date'].year for o,c in pairs])
    report={'source_blob':blob,'input_sha256':hashlib.sha256(data).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seed':SEED,'versions':{'numpy':np.__version__,'scipy':scipy.__version__,
                                  'sklearn':sklearn.__version__,'swisseph':swe.__version__},
            'status':'EXPLORATORY_INTERNAL_ONLY','audit':{
                'original_pairs':len(pairs),'exact_year_rematched_pairs':len(matched),
                'distinct_matched_years':len({o['date'].year for o,c in matched}),
                'unknown_offender_sex_in_matched':sum(o['sex']=='U' for o,c in matched),
                'later_year':int(sum(yr_o>yr_c)),'equal_year':int(sum(yr_o==yr_c)),
                'earlier_year':int(sum(yr_o<yr_c)),
                'younger_member_pairwise_accuracy_ties_half':float(np.mean((yr_o>yr_c)+.5*(yr_o==yr_c)))}}
    print('AUDIT',report['audit'],flush=True)
    # Aggregate results and input matching are saved after each arm for recovery.
    def save():
        report['ephemeris_returned_flags']=sorted(RETURN_FLAGS)
        (args.out/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    save()
    with (args.out/'exact_year_pairs.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['pair','offender','offender_dob','recorded_sex','control','control_dob','control_sex'])
        for i,(o,c) in enumerate(matched):
            w.writerow([i+1,o['name'],o['date'],o['sex'],c['name'],c['date'],c['sex']])
    for name, cohort, by_year in [('original',pairs,False),('exact_year',matched,True)]:
        rows,groups=make_rows(cohort,by_year)
        print('ARM',name,'people',len(rows),'groups',len(set(groups)),flush=True)
        report[name]={'baselines':baselines(rows,groups),'fitting_diagnostic':fitting_diagnostic(rows)}
        save()
        report[name]['nested']=nested(rows,groups,FAMILIES,args.repeats);save()
    if args.calendar_draws:
        report['calendar_null']=[]
        for draw in range(args.calendar_draws):
            rng=np.random.default_rng(SEED+500+draw); synthetic=[]
            for o,_ in pairs:
                days=366 if calendar.isleap(o['date'].year) else 365
                c={'name':'UNUSED','date':date(o['date'].year,1,1)+timedelta(days=int(rng.integers(days))),
                   'sex':o['sex'],'y':0}
                synthetic.append((o.copy(),c))
            rows,groups=make_rows(synthetic,True)
            # The name families are inapplicable to generated calendar controls.
            ans=nested(rows,groups,['dob_num','astro_aspects'],1)
            report['calendar_null'].append(ans);save()
    print('COMPLETE',args.out/'results.json',flush=True)

if __name__=='__main__':
    main()
