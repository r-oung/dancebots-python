#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Move:
    """Move"""

    _forward = 1 # forward bit
    _backward = 0 # backward bit
    _speed_max = 100 # maximum speed [0, 100]
    _speed_min = 0 # minimum speed [0, 100]

    def __init__(self):
        self._steps = []

    def _append_step(self, beats, left_motor, right_motor):
        self._steps.append(
            {
                "beats": beats,
                "left_motor": left_motor,
                "right_motor": right_motor,
            }
        )

    def _motor(self, speed, direction):
        """Convert speed and direction to binary list"""
        if speed > self._speed_max or speed < self._speed_min:
            raise ValueError("Speed must be a value between 0 and 100")

        if direction != self._forward and direction != self._backward:
            raise ValueError("Direction must be either 0 or 1")

        # normalize speed
        speed_norm = speed * 128.0 / 100.0

        # convert decimal to binary list
        binary_list = [int(x) for x in "{:08b}".format(int(round(speed_norm)))]

        # include direction bit
        binary_list[-1] = direction

        return binary_list

    def forward(self, beats, speed=100):
        self._append_step(
            beats, self._motor(speed, self._forward), self._motor(speed, self._forward)
        )

    def backward(self, beats, speed=100):
        self._append_step(
            beats,
            self._motor(speed, self._backward),
            self._motor(speed, self._backward),
        )

    def left(self, beats, speed=100):
        self._append_step(
            beats, self._motor(speed, self._backward), self._motor(speed, self._forward)
        )

    def right(self, beats, speed=100):
        self._append_step(
            beats, self._motor(speed, self._forward), self._motor(speed, self._backward)
        )

    def stop(self, beats):
        self._append_step(beats, [0] * 8, [0] * 8)

    @property
    def steps(self):
        return self._steps


if __name__ == "__main__":
    move = Move()
    move.forward(5, 100)
    move.backward(5, 100)
    move.left(5, 100)
    move.right(5, 100)
    move.stop(1)

    print(move.steps)
    print(len(move.steps))
