#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .move import Move
from .light import Light
from .step import Step

class Compose:
  """Combine moves and lights into a single composition"""

  def __init__(self, moves=[], lights=[]):
    ZEROS = [0] * 8
    self._steps = []

    # Concatenate all moves steps
    move_steps = []
    for move in moves:
      move_steps += move.steps
    print("Move steps: {}".format(len(move_steps)))

    # Concatenate all lights steps
    light_steps = []
    for light in lights:
      light_steps += light.steps

    # Check that moves and lights have the same units
    move_units = [step.unit for step in move_steps]
    light_units = [step.unit for step in light_steps]
    all_units = move_units + light_units
    if all_units.count(all_units[0]) != len(all_units):
      raise ValueError("Units are not identical") 

    if len(light_steps) != 0:
      # Add lights to the composition

      for step in light_steps:        
        if step.num_units > 1:
          # Expand composition list for lights lasting longer than 1
          for i in range(step.num_units):
            self._steps.append(Step(ZEROS, ZEROS, step.leds, step.unit, 1))
        else:
          self._steps.append(Step(ZEROS, ZEROS, step.leds, step.unit, step.num_units))

    # Notes:
    # - moves num_units >= 1
    # - lights num_units <= 1
    # - lights num_units will always add up to a whole number
      
    if len(move_steps) != 0:
      step_i = 0 # move step counter
      unit_cnt = 0 # lights unit counter

      # Merge lights and moves
      for this_step in self._steps:
        # If next step exists
        if step_i < len(move_steps):
          step = move_steps[step_i]
          this_step.motor_l = step.motor_l
          this_step.motor_r = step.motor_r
          unit_cnt += this_step.num_units

          if unit_cnt >= step.num_units:
            # Go to the next step
            step_i += 1
            unit_cnt = 0

      # If there are any remaining steps in the move
      if unit_cnt != 0:
        step = move_steps[step_i]
        for i in range(round(step.num_units - unit_cnt)): # @TODO Why is this not an integer?
          self._steps.append(Step(step.motor_l, step.motor_r, ZEROS, step.unit, 1))
        step_i += 1

      # No lights, add moves if they exist
      # If next step exists
      if step_i < len(move_steps):
        # Add steps to the composition
        for step in move_steps[step_i::]:
          if step.num_units > 1:
            # Expand composition list for steps lasting longer than a beat
            for i in range(step.num_units):
              self._steps.append(Step(step.motor_l, step.motor_r, ZEROS, step.unit, 1))
          else:
            self._steps.append(Step(step.motor_l, step.motor_r, ZEROS, step.unit, step.num_units))

  @property
  def steps(self):
    return self._steps

  def __str__(self):
    # pretty print steps
    lines = []

    if len(self._steps) == 0:
      return ""

    if self._steps[0].unit == "beats":
      header = ["Step", "Beats", "Count", "Left Motor", "Right Motor", "LEDs"]
    elif self._steps[0].unit == "seconds":
      header = ["Step", "Seconds", "Count", "Left Motor", "Right Motor", "LEDs"]

    format_row = "{:<6} {:<7} {:<7} {:<26} {:<26} {:<26}"
    lines.append(format_row.format(*header))

    cnt = 0
    for num, step in enumerate(self._steps, start=1):
      lines.append(format_row.format(
        num,
        round(step.num_units, 2),
        round(cnt, 2),
        str(step.motor_l),
        str(step.motor_r),
        str(step.leds),
      ))
      cnt += step.num_units
    
    if self._steps[0].unit == "beats":
      lines.append("Total: {} beats".format(round(sum([step.num_units for step in self._steps]))))
    elif self._steps[0].unit == "seconds":
      lines.append("Total: {} seconds".format(round(sum([step.num_units for step in self._steps]))))

    return "\n".join(lines)
