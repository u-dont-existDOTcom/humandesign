#!/usr/bin/env python3
"""Reproduce numeric comparisons from independent Swiss Ephemeris and geometry.

Not a Morinus GUI driver. Requires swisseph module from locally authorized
independent astronomy bundle plus geometry_reference.py alongside this file.
No personal birth data.
"""
import math
import json
import swisseph as swe
import geometry_reference as ref

def equatorial_zero_beta(lon, eps):
    v=math.radians(lon);e=math.radians(eps)
    return ref.EquatorialPoint(
       math.degrees(math.atan2(math.sin(v)*math.cos(e),math.cos(v)))%360,
       math.degrees(math.asin(math.sin(v)*math.sin(e)))
    )

def ecliptic(jd,body):
    xx,flag,err=swe.calc_ut(jd,body,swe.FLG_MOSEPH)
    return xx[0]

def equatorial(jd,body):
    xx,flag,err=swe.calc_ut(jd,body,swe.FLG_MOSEPH|swe.FLG_EQUATORIAL)
    if flag&(swe.FLG_MOSEPH|swe.FLG_EQUATORIAL)!=(swe.FLG_MOSEPH|swe.FLG_EQUATORIAL):
        raise AssertionError(("unexpected ephemeris mode",flag))
    return ref.EquatorialPoint(xx[0],xx[1])

def west_upper_utp(lat,ramc,fixed,moving):
    ad=ref.ascensional_difference(lat,fixed.dec_deg)
    upper_md=(ramc-fixed.ra_deg+180)%360-180
    assert 0<upper_md<90+ad
    r=upper_md/(90+ad)
    pole=math.degrees(math.atan2(math.sin(math.radians(r*ad)),
                                 math.tan(math.radians(fixed.dec_deg))))
    q=lambda p:math.degrees(math.asin(math.tan(math.radians(p.dec_deg))*math.tan(math.radians(pole))))
    return (moving.ra_deg+q(moving)-fixed.ra_deg-q(fixed))%360

jd2000=swe.julday(2000,1,1,12)
ramc=swe.sidtime(jd2000)*15
sun=equatorial(jd2000,swe.SUN)
sun_mc=(sun.ra_deg-ramc)%360
eps=swe.calc_ut(jd2000,swe.ECL_NUT,swe.FLG_MOSEPH)[0][1]
moon=equatorial_zero_beta(ecliptic(jd2000,swe.MOON),eps)
uranus_square=equatorial_zero_beta(ecliptic(jd2000,swe.URANUS)-90,eps)
baseline={
  "sun_mc":sun_mc,
  "uranus_square_moon_semi":ref.proportional_semi_arc_direction(45,ramc,moon,uranus_square),
  "uranus_square_moon_utp":west_upper_utp(45,ramc,moon,uranus_square),
  "uranus_square_moon_regio":ref.regiomontanus_position_circle_direction(45,ramc,moon,uranus_square),
}
assert abs(baseline["sun_mc"]-.821)<.0005
assert abs(baseline["uranus_square_moon_semi"]-1.070)<.0011
assert abs(baseline["uranus_square_moon_utp"]-1.075)<.0005
assert abs(baseline["uranus_square_moon_regio"]-.993)<.0005

jd=swe.julday(2026,3,19,6)
ramc2=(swe.sidtime(jd)*15+24)%360
fixed=equatorial(jd,swe.MOON)
moving=equatorial(jd,swe.SUN)
arc=ref.placidean_under_pole_east_upper_north(45,ramc2,fixed,moving)
ad=ref.ascensional_difference(45,fixed.dec_deg)
md=(fixed.ra_deg-ramc2)%360
r=md/(90+ad)
aodo=fixed.ra_deg-r*ad
assert aodo<0
predicted_converse=(-(arc-2*abs(aodo)))%360
assert abs(arc-.61870556178)<1e-6
assert abs(predicted_converse-2.29710750026)<1e-6
out={"independent_swiss_version":swe.version,"baseline":baseline,
     "seam":{"birth":"2026-03-19T06:00:00Z","lon_east":24,"lat_north":45,
      "moon_ra":fixed.ra_deg,"moon_dec":fixed.dec_deg,"sun_ra":moving.ra_deg,
      "ramc":ramc2,"signed_AODO":aodo,
      "correct_direct_arc":arc,"abs_value_artifact_converse_arc":predicted_converse,
      "observed_GUI_converse_arc":2.295},
     "no_predictive_validation":True}
print(json.dumps(out,indent=2))
