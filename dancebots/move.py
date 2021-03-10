#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import random
import numpy as np
import matplotlib.pyplot as plt 

from scipy.io import wavfile


class Move:
	"""Move

	"""
	def __init__(self, samples, sampling_rate):
		pass
	
	def left_wheel(self):
		pass
	
	def right_wheel(self):
		pass

	def forward(self, index, length):
		"""Moves robot forwards.

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, Choreography.fwd)
			self.cmds[index + i][1] = self.motor(Choreography.speed, Choreography.fwd)
		
		return

	def backward(self, index, length):
		"""Moves robot forwards.

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, Choreography.bwd)
			self.cmds[index + i][1] = self.motor(Choreography.speed, Choreography.bwd)
		
		return

	def turn_left(self, index, length):
		"""Twists the robot left.

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, Choreography.bwd)
			self.cmds[index + i][1] = self.motor(Choreography.speed, Choreography.fwd)

		return

	def turn_right(self, index, length):
		"""Twists the robot right

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, Choreography.fwd)
			self.cmds[index + i][1] = self.motor(Choreography.speed, Choreography.bwd)
		
		return

	@property
	def cmds_motor_left(self):
		""":obj:`list` of int: One-dimensional list of left motor commands."""
		return [i[0] for i in self.cmds]

	@property
	def cmds_motor_right(self):
		""":obj:`list` of int: One-dimensional list of right motor commands."""
		return [i[1] for i in self.cmds]

	@property
	def cmds_led(self):
		""":obj:`list` of int: One-dimensional list of LED commands."""
		return [i[2] for i in self.cmds]

	def blink_led(self, index, freq, val1, val2):
		"""Inserts LED commands to the dancebot-bitstream.
		
		Args:
			index (int):
			freq (float):
			val1 (int):
			val2 (int):

		Returns:
			None

		"""
		# unit conversion from [sec] to [commands]
		cmd_index, cmd_period = self.time2cmd(index, freq)

		# insert LED blink
		for i in range(int(0.5 * cmd_period)):
			self.cmds[cmd_index + i][2] = val1

		cmd_index += int(0.5 * cmd_period)

		for i in range(int(0.5 * cmd_period)):
			self.cmds[cmd_index + i][2] = val2

		cmd_index += int(0.5 * cmd_period)

	@staticmethod
	def time2cmd(index, freq):
		"""Converts index and dance-primitive from time-domain into command-domain.

		Args:
			index (int): Command time index [sec]
			freq (float): Motion primitive frequency [Hz]

		Returns:
			None
			
		"""
		# dance primitive period for a single repetition [sec]
		period = 1.0 / freq

		# unit conversion from [sec] to [commands]
		cmd_index = int(index / Choreography.msg_intvl)
		cmd_period = int(period / Choreography.msg_intvl)

		return cmd_index, cmd_period

	@staticmethod
	def motor(speed, direction):
		""" Converts motor command to the dancebot bitstream.
		
		A dancebot motor command consists of 8-bits, LSB-first.
		
			[ Motor Direction | Motor Speed ]
			[        7        |    6:0      ]

		where the direction bit is defined as:
			1: Forward
			0: Backward

		Args:
			speed (int): Motor speed; a value between 0-100. 
			direction (bool): Motor direction.

		Returns:
			int: 8-bit motor command.

		"""
		return ((0x01 & direction) << 7) | speed

	def __repr__(self):
		"""Default string representation of this class."""
		return "Dancebot({}, {})".format(self.samples, self.sampling_rate)

	def __str__(self):
		"""String representation of this class."""
		return "Number of Commands: {}".format(self.cmds_total)

	def __len__(self):
		"""Returns the total number of commands"""
		return  self.cmds_total

