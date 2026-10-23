"""Deterministic, source-independent algebraic and vector invariants."""
import math
import random
import unittest
from geometry_reference import (
  EquatorialPoint, DomainError, proportional_semi_arc_direction,
  regiomontanus_position_circle_direction, placidean_under_pole_east_upper_north,
  semi_arcs, phase, hour_angle_from_phase, ascensional_difference,
  position_circle_residual, ptolemy_rounded_linear_interpolation,
  rational_mean_solar_years, one_degree_per_year)

class GeometryTests(unittest.TestCase):
  def test_gansten_three_geometry_example(self):
    f,m = EquatorialPoint(50,15),EquatorialPoint(80,-10)
    self.assertAlmostEqual(proportional_semi_arc_direction(45,0,f,m),42.174344028350475,places=10)
    self.assertAlmostEqual(placidean_under_pole_east_upper_north(45,0,f,m),42.200815048927836,places=10)
    self.assertAlmostEqual(regiomontanus_position_circle_direction(45,0,f,m),46.4491178512784,places=10)
    self.assertLess(abs(position_circle_residual(45,0,f,m,46.4491178512784)),1e-13)

  def test_book_second_example_latitude(self):
    def ecliptic_to_equatorial(lam,beta,eps):
      d=math.radians
      x=math.cos(d(beta))*math.cos(d(lam))
      y=math.cos(d(beta))*math.sin(d(lam))*math.cos(d(eps))-math.sin(d(beta))*math.sin(d(eps))
      z=math.cos(d(beta))*math.sin(d(lam))*math.sin(d(eps))+math.sin(d(beta))*math.cos(d(eps))
      return EquatorialPoint(math.degrees(math.atan2(y,x))%360,math.degrees(math.asin(z)))
    for beta,expected in [(0,10.653324067373134),(5,5.5081832727086635)]:
      p=ecliptic_to_equatorial(120,beta,23.44)
      arc=(p.ra_deg-ascensional_difference(45,p.dec_deg)-90)%360
      self.assertAlmostEqual(arc,expected,places=10)
      h=arc-p.ra_deg
      sin_alt=math.sin(math.radians(45))*math.sin(math.radians(p.dec_deg))+math.cos(math.radians(45))*math.cos(math.radians(p.dec_deg))*math.cos(math.radians(h))
      self.assertLess(abs(sin_alt),1e-13)

  def test_phase_inversion_all_quadrants_both_hemispheres(self):
    rnd=random.Random(20261023)
    for i in range(20000):
      lat=rnd.uniform(-70,70)
      dec=rnd.uniform(-55,55)
      try: a,b=semi_arcs(lat,dec)
      except DomainError: continue
      h=rnd.uniform(0,360)
      self.assertLess(abs((hour_angle_from_phase(phase(h,a,b),a,b)-h+180)%360-180),1e-10)
    self.assertGreater(i,19990)

  def test_semi_arc_phase_at_contact(self):
    rnd=random.Random(11997)
    checked=0
    for i in range(7000):
      lat=rnd.uniform(-66,66)
      theta=rnd.uniform(0,360)
      fixed=EquatorialPoint(rnd.uniform(0,360),rnd.uniform(-40,40))
      moving=EquatorialPoint(rnd.uniform(0,360),rnd.uniform(-40,40))
      try:
        af,bf=semi_arcs(lat,fixed.dec_deg)
        am,bm=semi_arcs(lat,moving.dec_deg)
        arc=proportional_semi_arc_direction(lat,theta,fixed,moving)
      except DomainError:
        continue
      u0=phase(theta-fixed.ra_deg,af,bf)
      u1=phase(theta+arc-moving.ra_deg,am,bm)
      self.assertLess(abs((u0-u1+180)%360-180),1e-10)
      checked+=1
    self.assertGreater(checked,6000)

  def test_regio_cartesian_residual_and_semicircle(self):
    rnd=random.Random(712)
    accepted=0; no_solution=0
    for i in range(5000):
      lat=rnd.uniform(-60,60)
      theta=rnd.uniform(0,360)
      f=EquatorialPoint(rnd.uniform(0,360),rnd.uniform(-40,40))
      m=EquatorialPoint(rnd.uniform(0,360),rnd.uniform(-40,40))
      try:
        arc=regiomontanus_position_circle_direction(lat,theta,f,m)
      except DomainError:
        no_solution+=1
        continue
      self.assertLess(abs(position_circle_residual(lat,theta,f,m,arc)),1e-10)
      self.assertTrue(0<=arc<360)
      accepted+=1
    self.assertGreater(accepted,2000)
    self.assertGreater(no_solution,20)

  def test_equator_limit(self):
    self.assertAlmostEqual(proportional_semi_arc_direction(0,0,EquatorialPoint(50,15),EquatorialPoint(80,-10)),30)
    self.assertAlmostEqual(regiomontanus_position_circle_direction(0,0,EquatorialPoint(50,15),EquatorialPoint(80,-10)),30)

  def test_source_rounded_interpolation(self):
    self.assertEqual(ptolemy_rounded_linear_interpolation(58,70,2),62)
    self.assertEqual(ptolemy_rounded_linear_interpolation(58,70,3),64)
    self.assertEqual(ptolemy_rounded_linear_interpolation(58,70,4),66)

  def test_key_diagnostic(self):
    self.assertEqual(one_degree_per_year(75),75)
    self.assertAlmostEqual(rational_mean_solar_years(75),76.09375)

  def test_domain_rejections(self):
    with self.assertRaises(DomainError):
      semi_arcs(70,50)
    with self.assertRaises(DomainError):
      placidean_under_pole_east_upper_north(-45,0,EquatorialPoint(50,15),EquatorialPoint(80,-10))
    with self.assertRaises(DomainError):
      ptolemy_rounded_linear_interpolation(58,70,7)

if __name__=='__main__': unittest.main()
