"""Exact printed-coordinate checks for two historical figures, not sky parity.

Missing sign/degree/minute values remain missing. Any conditional completion is
named separately. No physical contact date, symbolic forecast or outcome score
is computed. Pure longitude arithmetic is reused unchanged from B02f.
"""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parent
HELPER = ROOT.parent / 'B02f' / 'lilly_presence_ship_reference.py'
SPEC = importlib.util.spec_from_file_location('retained_lilly_numeric_geometry', HELPER)
GEO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEO)


def exact_longitude(row):
    """Reject an incomplete transcription instead of supplying a hidden zero."""
    if any(row.get(k) is None for k in ('sign','degrees','minutes')):
        raise ValueError('Complete source sign, degree and minute are required')
    return GEO.longitude(row['sign'],row['degrees'],row['minutes'])


def _between_cusps(position, cusps):
    """Half-open geometric sectors; this is not Lilly's cusp influence rule."""
    for h in range(1,13):
        left = cusps[f'H{h:02d}']
        right = cusps[f'H{h%12+1:02d}']
        if (position-left)%21600 < (right-left)%21600:
            return h
    raise ValueError('Position is not contained in the supplied cusp sequence')


def reconcile():
    raw = json.loads((ROOT/'WORKED_NUMERIC_TABLES.json').read_text())
    charts = {c['id']:c for c in raw['charts']}
    exact = {}
    omitted = {}
    cusps = {}
    chart_checks = {}
    for cid,c in charts.items():
        cusps[cid] = {k:exact_longitude(v) for k,v in c['cusps'].items()}
        exact[cid], omitted[cid] = {}, []
        for kind in ('planets','nodes','lots'):
            for name,row in c[kind].items():
                try: exact[cid][name] = exact_longitude(row)
                except ValueError: omitted[cid].append(name)
        p,h = exact[cid],cusps[cid]
        computed = GEO.fortune(h['H01'],p['Moon'],p['Sun'],profile=GEO.FORTUNE_PROFILE)
        chart_checks[cid] = {
            'opposite_cusp_pairs_exact':[GEO.separation(h[f'H{i:02d}'],h[f'H{i+6:02d}'])==10800 for i in range(1,7)],
            'Fortune':{'computed':list(GEO.as_sign(computed)),
                       'printed_matches':computed==p['PartOfFortune'],
                       'profile':GEO.FORTUNE_PROFILE,
                       'profile_is_retained_from_XXIII_not_restated_here':True},
            'skipped_incomplete_exact_positions':omitted[cid],
            'geometric_houses_from_printed_cusps':{name:_between_cusps(pos,h) for name,pos in p.items()},
            'house_note':'Half-open geometric sectors only; source cusp influence and drawn placement remain separate.'
        }
    p1,p2 = exact['CH01'],exact['CH02']
    h1,h2 = cusps['CH01'],cusps['CH02']
    alternatives=[]
    for degree in charts['CH01']['planets']['Jupiter']['degree_reading_candidates']:
        for sign in ('Gemini','Cancer'):
            value=GEO.longitude(sign,degree,55)
            if _between_cusps(value,h1)==6:
                directed=(p1['Moon']-value)%21600
                alternatives.append({'degree':degree,'sign_if_diagram_sector_is_used':sign,
                    'minutes':55,'directed_Moon_minus_Jupiter_arcminutes':directed,
                    'signed_residual_from_trine_arcminutes':directed-7200,
                    'status':'CONDITIONAL_UNCERTAIN_INPUT_NOT_CANONICAL'})
    unknown_venus=charts['CH02']['planets']['Venus']
    if unknown_venus['minutes'] is not None:
        raise ValueError('The source Venus minute is expected to remain absent')
    conditional_venus=[
        (GEO.longitude('Gemini',unknown_venus['degrees'],m)-p2['Moon'])%21600
        for m in range(60)
    ]
    return {
        'status':'STATIC_PRINTED_ARITHMETIC_ONLY',
        'source_id':raw['source_id'],'source_sha256':raw['source_sha256'],
        'charts':chart_checks,
        'absent_brother':{
            'radical_eighth':8,'eighth_from_brother_third':GEO.turned_house(3,8),
            'Moon_to_printed_Sun_MC_gap_arcminutes':(p1['Sun']-p1['Moon'])%21600,
            'Sun_MC_separation_arcminutes':GEO.separation(p1['Sun'],h1['H10']),
            'Sun_MC_shared_printed_entry_not_independent_measurements':True,
            'Venus_Saturn_trine_residual_arcminutes':GEO.aspect_residual(p1['Venus'],p1['Saturn'],120),
            'Venus_to_Capricorn_gap_arcminutes':(GEO.longitude('Capricorn',0,0)-p1['Venus'])%21600,
            'source_described_degrees_to_ingress':1,
            'source_qualitative_week_conversion_not_executed':True,
            'Jupiter_canonical_longitude':None,'Jupiter_canonical_trine_residual':None,
            'Jupiter_conditional_readings':alternatives
        },
        'cambridge':{
            'Mars_to_MC_gap_arcminutes':(h2['H10']-p2['Mars'])%21600,
            'Saturn_to_seventh_gap_arcminutes':(h2['H07']-p2['Saturn'])%21600,
            'NorthNode_to_Ascendant_gap_arcminutes':(h2['H01']-p2['NorthNode'])%21600,
            'Mars_Saturn_square_residual_arcminutes':GEO.aspect_residual(p2['Mars'],p2['Saturn'],90),
            'Moon_Jupiter_sextile_residual_arcminutes':GEO.aspect_residual(p2['Moon'],p2['Jupiter'],60),
            'Moon_Venus_exact_square_gap':None,
            'Moon_Venus_conditional_gap_arcminutes':{'minimum':min(conditional_venus),'maximum':max(conditional_venus),
                'assumption':'Venus15 means degree15 with an unprinted integer minute00–59. Not a certified source precision or rounded-value model.'},
            'cusp_influence_threshold_inferred':None,
            'angle_signs':[charts['CH02']['cusps'][f'H{h:02d}']['sign'] for h in (1,4,7,10)],
            'all_angles_movable':all(charts['CH02']['cusps'][f'H{h:02d}']['sign'] in ('Aries','Cancer','Libra','Capricorn') for h in (1,4,7,10)),
            'short_ascension_signs_in_hypothetical_square':['Gemini','Pisces']
        },
        'physical_contact_times_computed':False,'modern_calendar_resolved':False,
        'historical_events_independently_verified':False,'predictive_accuracy_tested':False,
        'source_predictions_replaced_by_arithmetic':False
    }


if __name__=='__main__':
    result=reconcile()
    (ROOT/'ARITHMETIC_CHECKS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False))
