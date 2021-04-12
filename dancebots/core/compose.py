#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compose class.

A class for converting a list of moves and/or lights into steps.
"""
from .step import Step


class Compose(object):
    """A class for converting a list of moves and/or lights into steps.

    Attributes:
            moves: A list of Move objects.
            lights: A list of Light objects.
    """

    def __init__(self, moves=[], lights=[]):
        zeros = [0] * 8
        self._steps = []

        # Concatenate all moves steps
        move_steps = []
        for move in moves:
            move_steps += move.steps

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

        if light_steps:
            # Add lights to the composition

            for step in light_steps:
                if step.num_units > 1:
                    self._steps += [Step(zeros, zeros, step.leds, step.unit, 1)] * step.num_units
                else:
                    self._steps += [Step(zeros, zeros, step.leds, step.unit, 1)]

        # Notes:
        # - moves num_units >= 1
        # - lights num_units <= 1
        # - lights num_units will always add up to a whole number

        if move_steps:
            step_i = 0  # move step counter
            unit_cnt = 0  # lights unit counter

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
                self._steps += [Step(step.motor_l, step.motor_r, zeros, step.unit, 1)] * round(step.num_units - unit_cnt)
                step_i += 1

            # No lights, add moves if they exist
            # If next step exists
            if step_i < len(move_steps):
                # Add steps to the composition
                for step in move_steps[step_i::]:
                    if step.num_units > 1:
                        # Expand composition list for steps lasting longer than a beat
                        self._steps += [Step(step.motor_l, step.motor_r, zeros, step.unit, 1)] * step.num_units
                    else:
                        self._steps.append(
                            Step(
                                step.motor_l,
                                step.motor_r,
                                zeros,
                                step.unit,
                                step.num_units,
                            )
                        )

    @property
    def steps(self):
        """List of composition steps"""
        return self._steps

    def __str__(self):
        """Pretty print steps"""
        lines = []

        if not self._steps:
            return ""

        if self._steps[0].unit == "beats":
            header = ["Step", "Beats", "Count", "Left Motor", "Right Motor", "LEDs"]
        elif self._steps[0].unit == "seconds":
            header = ["Step", "Seconds", "Count", "Left Motor", "Right Motor", "LEDs"]

        format_row = "{:<6} {:<7} {:<7} {:<26} {:<26} {:<26}"
        lines.append(format_row.format(*header))

        cnt = 0
        for num, step in enumerate(self._steps, start=1):
            lines.append(
                format_row.format(
                    num,
                    round(step.num_units, 2),
                    round(cnt, 2),
                    str(step.motor_l),
                    str(step.motor_r),
                    str(step.leds),
                )
            )
            cnt += step.num_units

        if self._steps[0].unit == "beats":
            lines.append(
                "Total: {} beats".format(
                    round(sum([step.num_units for step in self._steps]))
                )
            )
        elif self._steps[0].unit == "seconds":
            lines.append(
                "Total: {} seconds".format(
                    round(sum([step.num_units for step in self._steps]))
                )
            )

        return "\n".join(lines)
