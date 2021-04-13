# -*- coding: utf-8 -*-
"""Frame object.

"""


class Frame:
    """A single Dancebot frame.

    Attributes:
            motor_l: List of bits for controlling the left motor.
            motor_r: List of bits for controlling the right motor.
            leds: List of bits for controlling the lights.
    """

    def __init__(self, motor_l, motor_r, leds):
        if len(motor_l) != 8:
            raise ValueError("Left motor must contain 8 values")

        if len(motor_r) != 8:
            raise ValueError("Right motor must contain 8 values")

        if len(leds) != 8:
            raise ValueError("LEDs must contain 8 values")

        for bit in motor_l:
            if bit not in (0, 1):
                raise ValueError("motor_l must be either 0 or 1")

        for bit in motor_r:
            if bit not in (0, 1):
                raise ValueError("motor_r must be either 0 or 1")

        for bit in leds:
            if bit not in (0, 1):
                raise ValueError("leds must be either 0 or 1")

        self._motor_l = motor_l
        self._motor_r = motor_r
        self._leds = leds

    @property
    def data(self):
        """Frame data getter"""
        return self._motor_l + self._motor_r + self._leds

    def __str__(self):
        return "\n" + str(self._motor_l + self._motor_r + self._leds)

    def __repr__(self):
        return "{}({},{},{})".format(
            self.__class__.__name__, self._motor_l, self._motor_r, self._leds
        )
