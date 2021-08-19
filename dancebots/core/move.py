# -*- coding: utf-8 -*-
"""Moves sequence class.

Defines a move sequence.
"""
from .step import Step


class Move:
    """Defines a move sequence.

    Attributes:
            unit: Can either be "beats" or "seconds".
    """

    _FORWARD = 1  # forward bit
    _BACKWARD = 0  # backward bit
    _SPEED_MAX = 100  # maximum speed [0, 100]
    _SPEED_MIN = 0  # minimum speed [0, 100]

    def __init__(self):
        self._steps = []

    def _append_step(self, num_units, motor_l, motor_r):
        if num_units < 1 or not isinstance(num_units, int):
            raise ValueError("👎 num_units must be a positive integer")

        self._steps.append(Step(motor_l, motor_r, [0] * 8, num_units))

    def _motor(self, speed, direction):
        """Convert speed and direction to binary list"""
        if speed > self._SPEED_MAX or speed < self._SPEED_MIN:
            raise ValueError("👎 Speed must be a value between 0 and 100")

        if direction not in (self._FORWARD, self._BACKWARD):
            raise ValueError("👎 Direction must be either 0 or 1")

        # Convert decimal to binary list, with LSB first
        binary_list = [0] * 8
        binary_value = str(bin(speed)[2:]) # remove '0b'
        for i, bit in enumerate(reversed(binary_value)):
            binary_list[i] = int(bit)

        # Include direction bit
        binary_list[-1] = direction

        return binary_list

    def forward(self, num_units, speed=100):
        """Move forward

        Attributes:
                num_units: Number of units to run this step.
                speed: Speed [0-100]
        """
        motor_l = self._motor(speed, self._FORWARD)
        motor_r = self._motor(speed, self._FORWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def backward(self, num_units, speed=100):
        """Move backward

        Attributes:
                num_units: Number of units to run this step.
                speed: Speed [0-100]
        """
        motor_l = self._motor(speed, self._BACKWARD)
        motor_r = self._motor(speed, self._BACKWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def left(self, num_units, speed=100):
        """Turn left

        Attributes:
                num_units: Number of units to run this step.
                speed: Speed [0-100]
        """
        motor_l = self._motor(speed, self._BACKWARD)
        motor_r = self._motor(speed, self._FORWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def right(self, num_units, speed=100):
        """Turn right

        Attributes:
                num_units: Number of units to run this step.
                speed: Speed [0-100]
        """
        motor_l = self._motor(speed, self._FORWARD)
        motor_r = self._motor(speed, self._BACKWARD)
        self._append_step(num_units, motor_l, motor_r)
        return motor_l, motor_r

    def stop(self, num_units):
        """Stop moving

        Attributes:
                num_units: The number of units to hold position.
        """
        self._append_step(num_units, [0] * 8, [0] * 8)

    def clear(self):
        """Clear steps.

        Clears the move sequence.
        """
        self._steps = []

    @property
    def steps(self):
        """List of move sequence steps"""
        return self._steps

    def __str__(self):
        """Pretty print steps"""
        lines = []

        header = ["Step", "Beats", "Left Motor", "Right Motor"]
        format_row = "{:<6} {:<7} {:<26} {:<26}"
        lines.append(format_row.format(*header))

        for num, step in enumerate(self._steps, start=1):
            lines.append(
                format_row.format(
                    num,
                    step.num_units,
                    str(step.motor_l),
                    str(step.motor_r),
                )
            )

        return "\n" + "\n".join(lines)
