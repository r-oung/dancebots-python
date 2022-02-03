# -*- coding: utf-8 -*-
"""Step class

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


class Step:
    """A single Dancebot step.

    Attributes:
            motor_l: List of bits for controlling the left motor.
            motor_r: List of bits for controlling the right motor.
            leds: List of bits for controlling the lights.
            num_units: Number of units to run this step.
    """

    def __init__(self, motor_l, motor_r, leds, num_units=1):
        self._motor_l = motor_l
        self._motor_r = motor_r
        self._leds = leds
        self._num_units = num_units  # number of units

        if num_units < 0:
            raise ValueError("👎 num_units must be a positive value")

    @property
    def motor_l(self):
        """Left motor getter"""
        return self._motor_l

    @motor_l.setter
    def motor_l(self, val):
        """Left motor setter"""
        self._motor_l = val

    @property
    def motor_r(self):
        """Right motor getter"""
        return self._motor_r

    @motor_r.setter
    def motor_r(self, val):
        """Right motor setter"""
        self._motor_r = val

    @property
    def leds(self):
        """LEDs getter"""
        return self._leds

    @leds.setter
    def leds(self, val):
        """LEDs setter"""
        self._leds = val

    @property
    def num_units(self):
        """Number of units getter"""
        return self._num_units

    def __repr__(self):
        return "{}({},{},{},{})".format(
            self.__class__.__name__,
            self._motor_l,
            self._motor_r,
            self._leds,
            self._num_units,
        )
