#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Step():
  """Step"""

  def __init__(self, motor_l, motor_r, leds, unit="beats", num_units=1):
    self._motor_l = motor_l
    self._motor_r = motor_r
    self._leds = leds
    self._unit = unit # unit [beats, seconds]
    self._num_units = num_units # number of units

    if unit != "beats" and unit != "seconds":
      raise ValueError("unit must either be 'beats' or 'seconds'")
    
    if num_units < 0:
      raise ValueError("num_units must be a positive value")

  @property
  def motor_l(self):
    return self._motor_l
  
  @motor_l.setter
  def motor_l(self, val):
    self._motor_l = val

  @property
  def motor_r(self):
    return self._motor_r
  
  @motor_r.setter
  def motor_r(self, val):
    self._motor_r = val

  @property
  def leds(self):
    return self._leds
  
  @leds.setter
  def leds(self, val):
    self._leds = val
  
  @property
  def unit(self):
    return self._unit

  @property
  def num_units(self):
    return self._num_units

