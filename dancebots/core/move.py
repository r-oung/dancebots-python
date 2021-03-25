#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Move:
    """Move"""

    _forward = 1 # forward bit
    _backward = 0 # backward bit
    _speed_max = 100 # maximum speed [0, 100]
    _speed_min = 0 # minimum speed [0, 100]

    def __init__(self, unit='beats'):
        self._frames = []
        self._unit = unit # `beats` or `seconds`

    def _append_frame(self, beats, left_motor, right_motor):
        self._frames.append(
            {
                "beats": beats,
                "seconds": "",  # @TODO overload at class level or function level?
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
        self._append_frame(
            beats, self._motor(speed, self._forward), self._motor(speed, self._forward)
        )
        return

    def backward(self, beats, speed=100):
        self._append_frame(
            beats,
            self._motor(speed, self._backward),
            self._motor(speed, self._backward),
        )
        return

    def left(self, beats, speed=100):
        self._append_frame(
            beats, self._motor(speed, self._backward), self._motor(speed, self._forward)
        )
        return

    def right(self, beats, speed=100):
        self._append_frame(
            beats, self._motor(speed, self._forward), self._motor(speed, self._backward)
        )
        return

    def stop(self, beats):
        self._append_frame(beats, [0] * 8, [0] * 8)
        return

    @property
    def frames(self):
        return self._frames


if __name__ == "__main__":
    move = Move()
    move.forward(5, 100)
    move.backward(5, 100)
    move.left(5, 100)
    move.right(5, 100)
    move.stop(1)

    print(move.frames)
    print(len(move.frames))


# import sys
# import random
# import numpy as np
# import matplotlib.pyplot as plt

# from scipy.io import wavfile


# def blink_led(self, index, freq, val1, val2):
# 	"""Inserts LED commands to the dancebot-bitstream.

# 	Args:
# 		index (int):
# 		freq (float):
# 		val1 (int):
# 		val2 (int):

# 	Returns:
# 		None

# 	"""
# 	# unit conversion from [sec] to [commands]
# 	cmd_index, cmd_period = self.time2cmd(index, freq)

# 	# insert LED blink
# 	for i in range(int(0.5 * cmd_period)):
# 		self.cmds[cmd_index + i][2] = val1

# 	cmd_index += int(0.5 * cmd_period)

# 	for i in range(int(0.5 * cmd_period)):
# 		self.cmds[cmd_index + i][2] = val2

# 	cmd_index += int(0.5 * cmd_period)

# @staticmethod
# def time2cmd(index, freq):
# 	"""Converts index and dance-primitive from time-domain into command-domain.

# 	Args:
# 		index (int): Command time index [sec]
# 		freq (float): Motion primitive frequency [Hz]

# 	Returns:
# 		None

# 	"""
# 	# dance primitive period for a single repetition [sec]
# 	period = 1.0 / freq

# 	# unit conversion from [sec] to [commands]
# 	cmd_index = int(index / Choreography.msg_intvl)
# 	cmd_period = int(period / Choreography.msg_intvl)

# 	return cmd_index, cmd_period

# @staticmethod
# def motor(speed, direction):
# 	""" Converts motor command to the dancebot bitstream.

# 	A dancebot motor command consists of 8-bits, LSB-first.

# 		[ Motor Direction | Motor Speed ]
# 		[        7        |    6:0      ]

# 	where the direction bit is defined as:
# 		1: Forward
# 		0: Backward

# 	Args:
# 		speed (int): Motor speed; a value between 0-100.
# 		direction (bool): Motor direction.

# 	Returns:
# 		int: 8-bit motor command.

# 	"""
# 	return ((0x01 & direction) << 7) | speed

# def __repr__(self):
# 	"""Default string representation of this class."""
# 	return "Dancebot({}, {})".format(self.samples, self.sampling_rate)

# def __str__(self):
# 	"""String representation of this class."""
# 	return "Number of Commands: {}".format(self.cmds_total)

# def __len__(self):
# 	"""Returns the total number of commands"""
# 	return  self.cmds_total
