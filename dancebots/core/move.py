#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Move:
    """Move"""

    _forward = 1  # forward bit
    _backward = 0  # backward bit
    _speed_max = 100  # maximum speed [0, 100]
    _speed_min = 0  # minimum speed [0, 100]

    def __init__(self):
        self._steps = []

    def _append_step(self, beats, motor_l, motor_r, description=""):
        self._steps.append(
            {
                "beats": beats,
                "motor_l": motor_l,
                "motor_r": motor_r,
                "description": description,
            }
        )

    def _motor(self, speed, direction):
        """Convert speed and direction to binary list"""
        if speed > self._speed_max or speed < self._speed_min:
            raise ValueError("Speed must be a value between 0 and 100")

        if direction != self._forward and direction != self._backward:
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

    def forward(self, beats, speed=100):
        bin_l = self._motor(speed, self._forward)
        bin_r = self._motor(speed, self._forward)
        self._append_step(beats, bin_l, bin_r, "Forward")
        return bin_l, bin_r

    def backward(self, beats, speed=100):
        bin_l = self._motor(speed, self._backward)
        bin_r = self._motor(speed, self._backward)
        self._append_step(beats, bin_l, bin_r, "Backward")
        return bin_l, bin_r

    def left(self, beats, speed=100):
        bin_l = self._motor(speed, self._backward)
        bin_r = self._motor(speed, self._forward)
        self._append_step(beats, bin_l, bin_r, "Left")
        return bin_l, bin_r

    def right(self, beats, speed=100):
        bin_l = self._motor(speed, self._forward)
        bin_r = self._motor(speed, self._backward)
        self._append_step(beats, bin_l, bin_r, "Right")
        return bin_l, bin_r

    def stop(self, beats):
        self._append_step(beats, [0] * 8, [0] * 8, "Stop")

    def clear(self):
        self._steps = []

    @property
    def steps(self):
        return self._steps

    def __str__(self):
        summary = "\n"

        header = ["Step", "Description", "Beats", "Left Motor", "Right Motor"]
        format_row = "{:<6} {:<15} {:<7} {:<26} {:<26}"
        summary += format_row.format(*header)
        summary += "\n"

        for num, step in enumerate(self._steps, start=1):
            summary += format_row.format(
                num, step["description"], step["beats"], str(step["motor_l"]), str(step["motor_r"]),
            )
            summary += "\n"

        return summary


if __name__ == "__main__":
    move = Move()
    move.forward(5, 100)
    move.backward(5, 100)
    move.left(5, 100)
    move.right(5, 100)
    move.stop(1)
    print(move)
