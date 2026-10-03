from __future__ import annotations
import hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import swisseph as swe
from scipy.optimize import minimize_scalar

from hdmatch.evaluation.astrohd_v13_traditions import (
    build_snapshot, sign_name, RULERS, _hellenistic_planet_testimonies,
    _lilly_planet_testimonies, _parashari_planet_testimonies,
)
from hdmatch.evaluation.astrohd_v14_rules import registry, feature_row
from hdmatch.evaluation.astrohd_v13b_native import lilly_planet_native_strength
from hdmatch.relationship.western import within_chart_aspects

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("CALCULATIONS.json")
EPHE = Path(os.environ["EPHEMERIS_ROOT"])
LAT, LON = 41.0138429552247, 28.9496612548828
LOCAL = datetime(1994, 1, 28, 0, 35, tzinfo=ZoneInfo("Europe/Istanbul"))
BIRTH = LOCAL.astimezone(timezone.utc)
FLAGS = int(swe.FLG_SWIEPH) | int(swe.FLG_SPEED)
TROPICAL_YEAR = 365.24219
ASPECTS = {"conjunction":0.0,"sextile":60.0,"square":90.0,"trine":120.0,"opposition":180.0}

BODY_IDS = {
    "sun":swe.SUN, "moon":swe.MOON, "mercury":swe.MERCURY, "venus":swe.VENUS,
    "mars":swe.MARS, "jupiter":swe.JUPITER, "saturn":swe.SATURN,
    "uranus":swe.URANUS, "neptune":swe.NEPTUNE, "pluto":swe.PLUTO,
    "north_node":swe.TRUE_NODE,
}
TRAD_PLANETS = ("sun","moon","mercury","venus","mars","jupiter","saturn")
TRANSIT_BODIES = ("jupiter","saturn","uranus","neptune","pluto")
PROG_BODIES = ("sun","moon","mercury","venus","mars")
TARGETS = ("sun","moon","mercury","venus","mars","jupiter","saturn","ASC","MC")
LETTERS = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
MASTERS = {11,22,33}
KARMIC = {13,14,16,19}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def jd(dt: datetime) -> float:
    u = dt.astimezone(timezone.utc)
    h = u.hour + u.minute/60 + u.second/3600 + u.microsecond/3.6e9
    return float(swe.julday(u.year,u.month,u.day,h,swe.GREG_CAL))

def calc(j: float, body: str) -> tuple[float,float]:
    vals, ret = swe.calc_ut(j, BODY_IDS[body], FLAGS)
    if ret & int(swe.FLG_MOSEPH) or not ret & int(swe.FLG_SWIEPH):
        raise RuntimeError(f"Swiss fallback: {body} flags={ret}")
    return float(vals[0]) % 360.0, float(vals[3])

def sep(a: float, b: float) -> float:
    d = abs((a-b) % 360.0)
    return min(d, 360.0-d)

def deg_fmt(x: float) -> dict:
    x %= 360.0
    return {"longitude":x, "sign":sign_name(x), "degree_in_sign":x % 30.0}

def revjul(j: float) -> str:
    y,m,d,h = swe.revjul(j, swe.GREG_CAL)
    hh=int(h); mmf=(h-hh)*60; mm=int(mmf); ss=int(round((mmf-mm)*60))
    if ss == 60: ss=59
    return datetime(y,m,d,hh,mm,ss,tzinfo=timezone.utc).isoformat().replace("+00:00","Z")

def reduce_num(n: int, preserve_master: bool=True) -> tuple[int,list[int]]:
    chain=[int(n)]
    while n >= 10 and not (preserve_master and n in MASTERS):
        n = sum(int(x) for x in str(n)); chain.append(n)
    return n, chain

def reduce_single(n: int) -> tuple[int,list[int]]:
    return reduce_num(n, preserve_master=False)

def component_name(name: str, mode: str) -> dict:
    rows=[]
    for part in name.upper().split():
        chars=[c for c in part if c in LETTERS]
        if mode=="vowels": chars=[c for c in chars if c in "AEIOU"]
        elif mode=="consonants": chars=[c for c in chars if c not in "AEIOU"]
        raw=sum(LETTERS[c] for c in chars)
        red,chain=reduce_num(raw, True)
        rows.append({"part":part,"letters":chars,"values":[LETTERS[c] for c in chars],
                     "raw":raw,"reduced":red,"chain":chain})
    total=sum(r["reduced"] for r in rows)
    final,chain=reduce_num(total, True)
    return {"parts":rows,"component_sum":total,"number":final,"final_chain":chain}

def name_profile(name: str) -> dict:
    return {"name":name,"expression":component_name(name,"all"),
            "soul_urge":component_name(name,"vowels"),
            "personality":component_name(name,"consonants")}

def active_letter(name: str, age: int) -> tuple[str,int]:
    chars=[c for c in name.upper() if c in LETTERS]
    pos=age % sum(LETTERS[c] for c in chars)
    cursor=0
    for c in chars:
        v=LETTERS[c]
        if pos < cursor+v: return c,v
        cursor += v
    raise AssertionError
def personal_year(year: int) -> dict:
    raw = 1 + 28 + year
    red, chain = reduce_single(raw)
    return {"year":year,"raw":raw,"number":red,"chain":chain}

def numerology() -> dict:
    month_raw, day_raw, year_raw = 1, 28, 1994
    month_n, month_chain = reduce_num(month_raw, True)
    day_n, day_chain = reduce_num(day_raw, True)
    year_digits = sum(map(int,str(year_raw)))
    year_n, year_chain = reduce_num(year_digits, True)
    lp_raw = month_n + day_n + year_n
    lp, lp_chain = reduce_num(lp_raw, True)
    attitude_raw = month_raw + day_raw
    attitude, attitude_chain = reduce_single(attitude_raw)
    birth = name_profile("Hatice Baysan")
    current = name_profile("Hale Denizden")

    p1,_ = reduce_num(month_n+day_n, True)
    p2,_ = reduce_num(day_n+year_n, True)
    p3,_ = reduce_num(p1+p2, True)
    p4,_ = reduce_num(month_n+year_n, True)
    m1,_=reduce_single(month_raw); d1,_=reduce_single(day_raw); y1,_=reduce_single(year_digits)
    c1=abs(m1-d1); c2=abs(d1-y1); c3=abs(c1-c2); c4=abs(m1-y1)
    lp_single,_=reduce_single(lp)
    first_end = 36 - lp_single
    transits=[]
    for age in range(0,61):
        pl,pv=active_letter("Hatice",age)
        sl,sv=active_letter("Baysan",age)
        essence=pv+sv+sv
        er,_=reduce_single(essence)
        transits.append({
            "age":age, "birthday_start":f"{1994+age}-01-28",
            "physical":{"letter":pl,"value":pv},
            "mental":{"letter":sl,"value":sv,"source":"last_name_no_middle_fallback"},
            "spiritual":{"letter":sl,"value":sv},
            "essence":{"compound":essence,"reduced":er,
                       "master":essence if essence in MASTERS else None,
                       "karmic_debt":essence if essence in KARMIC else None},
        })
    maturity_raw = lp + birth["expression"]["number"]
    maturity, maturity_chain = reduce_num(maturity_raw, True)

    return {
      "method":{"system":"Pythagorean/Decoz-style","y_treatment":"consonant",
                "birth_name_primary":True,"current_name_role":"minor/static overlay only",
                "no_middle_transit":"last name supplies both mental and spiritual"},
      "date_components":{"month":{"raw":month_raw,"reduced":month_n,"chain":month_chain},
                         "day":{"raw":day_raw,"reduced":day_n,"chain":day_chain},
                         "year":{"raw":year_raw,"digit_sum":year_digits,
                                 "reduced":year_n,"chain":year_chain}},
      "life_path":{"pre_final_sum":lp_raw,"number":lp,"chain":lp_chain},
      "birthday":{"compound":28,"reduced":1},
      "attitude_sun":{"raw":attitude_raw,"number":attitude,"chain":attitude_chain,
                      "masters_reduced_by_convention":True},
      "birth_name":birth, "current_name_overlay":current,
      "maturity":{"raw":maturity_raw,"number":maturity,"chain":maturity_chain,
                  "karmic_debt":maturity_raw if maturity_raw in KARMIC else None},
      "period_cycles":{"numbers":[month_n,day_n,year_n],
                       "formal_duration_markers":[0,first_end,first_end+27],
                       "transition_note":"Decoz: first Period lasts 36 minus the single-digit Life Path; second lasts 27 years. Boundary wording is age-based. Here Period 1 and Period 2 are both number 1, so the first boundary does not change the Period number."},
      "pinnacles":{"numbers":[p1,p2,p3,p4],
                   "age_boundaries":[0,first_end,first_end+9,first_end+18]},
      "challenges":{"numbers":[c1,c2,c3,c4],
                    "duration_note":"Decoz convention: challenge durations are fluid/overlapping; first roughly to age 30-35, second roughly to 55-60, third/main throughout life, fourth strongest from ~55-60 onward",
                    "main_challenge":c3},
      "personal_years":[personal_year(y) for y in range(1994,2042)],
      "birth_name_transits_essences":transits,
    }

def natal() -> tuple[dict,dict[str,float]]:
    swe.set_ephe_path(str(EPHE))
    snap=build_snapshot(BIRTH,latitude=LAT,longitude=LON,ephemeris_root=EPHE)
    bj=jd(BIRTH)
    wide={}; speeds={}
    for body in BODY_IDS:
        wide[body],speeds[body]=calc(bj,body)
    raw_cusps,ascmc=swe.houses_ex(bj,LAT,LON,b"P",0)
    placidus={"cusps":[float(x)%360 for x in raw_cusps[:12]],
              "ascendant":float(ascmc[0])%360,"midheaven":float(ascmc[1])%360}
    planet_rows={}
    for p in TRAD_PLANETS:
        planet_rows[p]={
          "tropical":deg_fmt(snap.tropical_longitudes[p]),
          "tropical_speed":snap.tropical_speeds[p],
          "regiomontanus_house":snap.regio_houses[p],
          "tropical_whole_sign_house":snap.tropical_whole_houses[p],
          "sidereal_lahiri":deg_fmt(snap.sidereal_longitudes[p]),
          "sidereal_speed":snap.sidereal_speeds[p],
          "sidereal_whole_sign_house":snap.sidereal_whole_houses[p],
          "lilly_native_strength":lilly_planet_native_strength(snap,p),
          "strength_testimonies":{
            "hellenistic":_hellenistic_planet_testimonies(snap,p),
            "lilly":_lilly_planet_testimonies(snap,p),
            "parashari":_parashari_planet_testimonies(snap,p),
          }}
    aspects=[{"a":a.body_a,"b":a.body_b,"aspect":a.aspect,"orb":a.orb_degrees}
             for a in within_chart_aspects(wide,max_orb=3.0)]
    angle_aspects=[]
    for body, blong in wide.items():
        for angle_name, along in (("ASC",placidus["ascendant"]),("MC",placidus["midheaven"])):
            separation=sep(blong,along)
            aspect_name, aspect_angle=min(ASPECTS.items(), key=lambda kv: abs(separation-kv[1]))
            orb=abs(separation-aspect_angle)
            if orb <= 3.0:
                angle_aspects.append({"body":body,"angle":angle_name,"aspect":aspect_name,"orb":orb})
    house_lords={}
    for h,cusp in enumerate(snap.regio_cusps,start=1):
        lord=RULERS[sign_name(cusp)]
        house_lords[str(h)]={"cusp":deg_fmt(cusp),"lord":lord,
                             "lord_house":snap.regio_houses[lord],
                             "lord_lilly_native":lilly_planet_native_strength(snap,lord)}
    model=json.loads((ROOT/"tasks/scenario-owner-recovery-calibration-20260923/ASTROHD-V14-SIX-RULE-MODEL-20260925.json").read_text())
    consensus=json.loads((ROOT/model["source_map_path"]).read_text())
    rows=registry(consensus,{d["domain_id"] for d in consensus["domains"]})
    lookup={r["rule_id"]:r for r in rows}
    selected=[lookup[k] for k in model["selected_rule_ids"]]
    vals=feature_row(snap,selected)
    six={"score":int(vals.sum()),"max":6,
         "role":"secondary Joel-fitted fingerprint only",
         "rule_values":dict(zip(model["selected_rule_ids"],[int(x) for x in vals]))}
    out={
      "birth_local":LOCAL.isoformat(),"birth_utc":BIRTH.isoformat().replace("+00:00","Z"),
      "location":{"latitude":LAT,"longitude":LON,"role":"GeoNames city point"},
      "day_chart":snap.day_chart,
      "angles":{"regiomontanus_ascendant":deg_fmt(snap.tropical_ascendant),
                "regiomontanus_cusps":[deg_fmt(x) for x in snap.regio_cusps],
                "placidus_ascendant":deg_fmt(placidus["ascendant"]),
                "placidus_midheaven":deg_fmt(placidus["midheaven"]),
                "sidereal_lahiri_ascendant":deg_fmt(snap.sidereal_ascendant)},
      "planets":planet_rows,
      "wide_tropical":{p:{**deg_fmt(wide[p]),"speed":speeds[p]} for p in wide},
      "major_aspects_3deg":aspects,
      "angle_aspects_3deg":angle_aspects,
      "regiomontanus_house_lords":house_lords,
      "six_rule_secondary_fingerprint":six,
    }
    targets={p:wide[p] for p in TRAD_PLANETS}
    targets["ASC"]=placidus["ascendant"]; targets["MC"]=placidus["midheaven"]
    return out, targets

def exact_events(targets: dict[str,float], progressed: bool=False) -> list[dict]:
    start=jd(BIRTH)
    end=float(swe.julday(2041,12,31,0.0,swe.GREG_CAL))
    step=10.0 if progressed else 3.0
    bodies=PROG_BODIES if progressed else TRANSIT_BODIES
    samples=[]
    x=start
    while x <= end:
        samples.append(x); x += step
    cache={}
    def lon_at(obs_j: float, body: str) -> float:
        key=(round(obs_j,7),body,progressed)
        if key in cache: return cache[key]
        source_j = start + (obs_j-start)/TROPICAL_YEAR if progressed else obs_j
        v,_=calc(source_j,body); cache[key]=v; return v
    events=[]
    for body in bodies:
      for target,tlong in targets.items():
        for aspect,angle in ASPECTS.items():
          ds=[abs(sep(lon_at(x,body),tlong)-angle) for x in samples]
          for i in range(1,len(samples)-1):
            if ds[i] <= ds[i-1] and ds[i] < ds[i+1] and ds[i] < 1.2:
              lo=max(start,samples[i]-step); hi=min(end,samples[i]+step)
              res=minimize_scalar(lambda z: abs(sep(lon_at(float(z),body),tlong)-angle),
                                  bounds=(lo,hi),method="bounded",options={"xatol":1e-6})
              if res.fun <= 0.02:
                events.append({"kind":"secondary_progression" if progressed else "transit",
                               "body":body,"aspect":aspect,"target":target,
                               "exact_utc":revjul(float(res.x)),"orb_degrees":float(res.fun)})
    events.sort(key=lambda e:(e["exact_utc"],e["body"],e["target"],e["aspect"]))
    dedup=[]
    for ev in events:
        same=[x for x in dedup[-30:] if x["body"]==ev["body"] and x["target"]==ev["target"]
              and x["aspect"]==ev["aspect"]]
        if same:
            ej=jd(datetime.fromisoformat(ev["exact_utc"].replace("Z","+00:00")))
            sj=jd(datetime.fromisoformat(same[-1]["exact_utc"].replace("Z","+00:00")))
            if abs(ej-sj)<5: continue
        dedup.append(ev)
    return dedup

def main() -> None:
    assert BIRTH.isoformat()=="1994-01-27T22:35:00+00:00"
    assert sha(EPHE/"sepl_18.se1")=="ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66"
    assert sha(EPHE/"semo_18.se1")=="1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7"
    natal_out, targets=natal()
    transit_events=exact_events(targets,False)
    prog_events=exact_events(targets,True)
    calc_out={
      "schema":"hale-cleanroom-calculations-v1",
      "provenance":{
        "base_commit":"f4fa0b86593e895328a18d13ec90432c8cb99662",
        "swisseph_version":swe.version,
        "sepl_18_sha256":sha(EPHE/"sepl_18.se1"),
        "semo_18_sha256":sha(EPHE/"semo_18.se1"),
        "timezone":"Europe/Istanbul","historical_offset_seconds":int(LOCAL.utcoffset().total_seconds()),
        "coordinates_source":"GeoNames city point; exact birth facility unavailable",
      },
      "natal":natal_out,
      "numerology":numerology(),
      "timing":{
        "transits_exact_major_aspects_1994_2041":transit_events,
        "secondary_progressions_exact_major_aspects_1994_2041":prog_events,
        "notes":["transits: Jupiter-Saturn-Uranus-Neptune-Pluto to natal Sun-Saturn plus ASC/MC",
                 "progressions: Sun-Moon-Mercury-Venus-Mars to same natal targets",
                 "major aspects: 0/60/90/120/180; exact numerical threshold <=0.02 deg"],
      }}
    OUT.write_text(json.dumps(calc_out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"output":str(OUT),"sha256":sha(OUT),
                      "transit_events":len(transit_events),"progression_events":len(prog_events),
                      "birth_utc":natal_out["birth_utc"],
                      "six_rule":natal_out["six_rule_secondary_fingerprint"],
                      "numerology":{"life_path":calc_out["numerology"]["life_path"],
                                    "birth_name":calc_out["numerology"]["birth_name"],
                                    "pinnacles":calc_out["numerology"]["pinnacles"],
                                    "challenges":calc_out["numerology"]["challenges"]}},indent=2))

if __name__=="__main__":
    main()
