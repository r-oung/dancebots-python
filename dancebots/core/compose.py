# -*- coding: utf-8 -*-
"""Compose class

Copyright (C) 2021-2022 Raymond Oung

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from .step import Step


class Compose:
    """A class for converting a list of moves and/or lights into steps.

    Attributes:
            moves: A list of Move objects.
            lights: A list of Light objects.
    """

    def __init__(self, moves=None, lights=None):
        zeros = [0] * 8
        self._steps = []

        # Concatenate all moves steps
        move_steps = []
        if moves is not None:
            for move in moves:
                move_steps += move.steps

        # Concatenate all lights steps
        light_steps = []
        if lights is not None:
            for light in lights:
                light_steps += light.steps

        if light_steps:
            # Add lights to the composition

            for step in light_steps:
                if step.num_units > 1:
                    self._steps += [Step(zeros, zeros, step.leds, 1)] * step.num_units
                else:
                    self._steps += [Step(zeros, zeros, step.leds, step.num_units)]

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
                self._steps += [Step(step.motor_l, step.motor_r, zeros, 1)] * round(
                    step.num_units - unit_cnt
                )
                step_i += 1

            # No lights, add moves if they exist
            # If next step exists
            if step_i < len(move_steps):
                # Add steps to the composition
                for step in move_steps[step_i::]:
                    if step.num_units > 1:
                        # Expand composition list for steps lasting longer than a beat
                        self._steps += [
                            Step(step.motor_l, step.motor_r, zeros, 1)
                        ] * step.num_units
                    else:
                        self._steps.append(
                            Step(
                                step.motor_l,
                                step.motor_r,
                                zeros,
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

        header = ["Step", "Beats", "Count", "Left Motor", "Right Motor", "LEDs"]
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

        lines.append(
            "Total: {} beats".format(
                round(sum([step.num_units for step in self._steps]))
            )
        )

        return "\n".join(lines)
