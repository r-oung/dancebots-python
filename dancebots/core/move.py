#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .step import Step

class Move():
    """Move"""

    _FORWARD = 1 # forward bit
    _BACKWARD = 0 # backward bit
    _SPEED_MAX = 100 # maximum speed [0, 100]
    _SPEED_MIN = 0 # minimum speed [0, 100]

    def __init__(self, unit="beats"):
        if unit != "beats" and unit != "seconds":
            raise ValueError("unit must either be 'beats' or 'seconds'")
 
        self._steps = []
        self._unit = unit

    def _append_step(self, num_units, motor_l, motor_r):
        if num_units < 1 or not isinstance(num_units, int):
            raise ValueError("num_units must be a positive integer")

        self._steps.append(Step(motor_l, motor_r, [0] * 8, self._unit, num_units))

    def _motor(self, speed, direction):
        """Convert speed and direction to binary list"""
        if speed > self._SPEED_MAX or speed < self._SPEED_MIN:
            raise ValueError("Speed must be a value between 0 and 100")

        if direction != self._FORWARD and direction != self._BACKWARD:
            raise ValueError("Direction must be either 0 or 1")

        # Normalize speed
        speed_norm = int(round(speed * 127.0 / 100.0))

        # Convert decimal to binary list, with LSB first
        binary_list = [0] * 8
        binary_value = str(bin(speed_norm)[2:])
        for i, bit in enumerate(reversed(binary_value)):
            binary_list[i] = int(bit)

        # Include direction bit
        binary_list[-1] = direction

        return binary_list

    def forward(self, num_units, speed=100):
        motor_l = self._motor(speed, self._FORWARD)
        motor_r = self._motor(speed, self._FORWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def backward(self, num_units, speed=100):
        motor_l = self._motor(speed, self._BACKWARD)
        motor_r = self._motor(speed, self._BACKWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def left(self, num_units, speed=100):
        motor_l = self._motor(speed, self._BACKWARD)
        motor_r = self._motor(speed, self._FORWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def right(self, num_units, speed=100):
        motor_l = self._motor(speed, self._FORWARD)
        motor_r = self._motor(speed, self._BACKWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def stop(self, num_units):
        self._append_step(num_units, [0] * 8, [0] * 8)

    def clear(self):
        self._steps = []

    @property
    def steps(self):
        return self._steps

    def __str__(self):
        # pretty print steps
        lines = []

        if self._unit == "beats":
            header = ["Step", "Beats", "Left Motor", "Right Motor"]
        elif self._unit == "seconds":
            header = ["Step", "Seconds", "Left Motor", "Right Motor"]

        format_row = "{:<6} {:<7} {:<26} {:<26}"
        lines.append(format_row.format(*header))

        for num, step in enumerate(self._steps, start=1):
            lines.append(format_row.format(
                num, step.num_units, str(step.motor_l), str(step.motor_r),
            ))

        return "\n".join(lines)
