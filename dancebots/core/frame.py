#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Frame object.

Defines a single Dancebot frame.
"""
class Frame(object):
    """A single Dancebot frame.
    
    Attributes:
            motor_l: List of bits for controlling the left motor.
            motor_r: List of bits for controlling the right motor.
            leds: List of bits for controlling the lights.
    """

    def __init__(self, motor_l=[], motor_r=[], leds=[]):
        if len(motor_l) != 0 and len(motor_l) != 8:
            raise ValueError("Left motor must contain 8 values")

        if len(motor_r) != 0 and len(motor_r) != 8:
            raise ValueError("Right motor must contain 8 values")

        if len(leds) != 0 and len(leds) != 8:
            raise ValueError("LEDs must contain 8 values")

        self._motor_l = motor_l
        self._motor_r = motor_r
        self._leds = leds

    @property
    def data(self):
        return self._motor_l + self._motor_r + self._leds

    def __str__(self):
        return str(self._motor_l + self._motor_r + self._leds)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self._motor_l}, {self._motor_r}, {self._leds})"
        )
