#!/usr/bin/env python
# -*- coding: utf-8 -*-
import protocol


class Move():
	"""Move

	"""
	_forward = 1 # forward bit
	_backward = 0 # backward bit

	def __init__(self):
		self.frames = []


	def _append_frame(self, left_wheel, right_wheel, beats):
		self.frames.append({
			"beats": beats,
			"left_wheel": left_wheel,
			"right_wheel": right_wheel,
		})
	

	def _wheel(self, speed, direction):
		if speed > 100 or speed < 0:
			raise ValueError("Speed must be a value between 0 and 100")

		if direction > 1 or direction < 0:
			raise ValueError("Direction must be either 0 or 1")

		speed_scaled = speed * 128.0 / 100.0
		binary_string = "{0:b}".format(speed_scaled)
		binary_list = list(binary_string)
		binary_list.append(direction)
		return binary_list


	def forward(self, speed, beats):
		self._append_frame(self._wheel(speed, self._forward), self._wheel(speed, self._forward), beats)
		return


	def backward(self, speed, beats):
		self._append_frame(self._wheel(speed, self._backward), self._wheel(speed, self._backward), beats)
		return


	def left(self, speed, beats):
		self._append_frame(self._wheel(speed, self._backward), self._wheel(speed, self._forward), beats)
		return
	

	def right(self, speed, beats):
		self._append_frame(self._wheel(speed, self._forward), self._wheel(speed, self._backward), beats)
		return

	
	def stop(self, beats):
		self._append_frame([0]*8], [0]*8, beats)
		return


	@property
	def frames(self):
		return self.frames


if __name__ == "__main__":
	robot = Move()
	robot.forward(100, 5)
	robot.stop(1)
	robot.backward(100, 5)
	robot.stop(1)
	robot.left(50, 5)
	robot.stop(1)


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
