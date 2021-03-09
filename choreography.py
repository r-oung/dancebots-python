#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates dancebot choreography bitstream.

This script takes as input a dance choreography (.CSV) and a light choreography (.CSV), and generates a choreography-bitstream (.WAV) using dancebot-protocol.

Email from Philipp Reist:
	Given the 8MHz clock of the ATTiny, a pulse (i.e. time between to edges of the MP3 player voltage on the right channel) is considered a RESET, or start of a new 24bit message, if it is longer than 5805 ticks (0.73ms, or 32 samples at 44.1kHz), considered a 1 if it is between 3367 and 5805 ticks, and a 0 if it is below 3367 ticks. Then, the 24 bit message consists of 8bits for the left motor, 8bits for the right motor, and 8 bits for the 8 LEDs. The LSB is sent first. For the motors, bit 0-6 is speed (valid range 0-100), and bit 7 is direction (1 FWD, 0 BWD [this is wrongly labeled in the FW on Bitbucket). For the LEDs, each bit corresponds directly to the LED.

Summary:
	Messages are 24-bits long, LSB sent first.

	[ left-motor | right-motor | 8-LEDs ]
	[   8-bits   |   8-bits    | 8-bits ]

	Bit representation is time-modulated as follows:
	-------------------------------------------------
	TYPE | Ticks		| Interval (sec)
	-------------------------------------------------
	START:      > 5805 	              > 0.000725625 
		1: 3367 - 5805	  0.000420875 - 0.000725625
		0:      < 3367 	              < 0.000420875

	The following bit representation will be used in this script:
	---------------------
	TYPE | Interval (sec)
	---------------------
	START: 1.0 
		0: 0.4
		1: 0.6

	Therefore, the longest message will be 1.0 + (24 x 0.6) = 15.4 msec.

Example:
	This script can be run as follows:
		$ python db_choreography.py

Todo:
	LED should synchronize pattern to the music
	- Quantity of LEDs blinking should be a function of low-frequency beats/intensity
	- LED blinking frequency should be a function of music frequency


"""

# from __future__ import unicode_literals

import random


class Choreography:
	""" Dancebot base class.

	This class consists of the basic methods for moving the robot and blinking the LEDs.
	"""

	start = 1.0 #: start bit period [msec]
	one = 0.4 #: one bit period [msec]
	zero = 0.6 # zero bit period [msec]

	fwd = 1 # forward bit
	bwd = 0 # backward bit
	speed = 100 # speed [0,100]

	msg_intvl = 0.1 #: the interval between sequential messages [sec], this value cannot be less than 15.4 msec.

	samples = 0
	sampling_rate = 0
	song_length = 0

	moves = list()

	def __init__(self, samples, sampling_rate):
		self.samples = samples
		self.sampling_rate
		self.song_length = samples / sampling_rate; #: length of the song [sec]
		self.cmds_total = int(self.song_length / Choreography.msg_intvl) #: total number of commands
		self.cmds = [[0,0,0] for i in range(self.cmds_total)] #: list of all commands
		self.samples_start = self.start / sampling_rate
		self.samples_one = self.one / sampling_rate
		self.samples_zero = self.zero / sampling_rate
		self.samples_intvl = self.msg_intvl / sampling_rate

	def insert(self, index, move):
		self.moves.append([{move: move}])
		print(self.moves)
		return

	def bitstream(self):
		"""Generates dancebot-bitsream from list of moves

		Arg:
			None

		Returns:
			:obj:`list` of int

		"""



		data = []
		toggle = 1

		# step through all commands
		for i in range(self.cmds_total):
			s = 0

			# add START
			for l in range(self.samples_start):
				data.append(toggle)

			toggle ^= 0x01

			# step through motor and LED commands
			for j in range(len(self.cmds[i])):
				# convert byte to a list of bits
				bits = [int(x) for x in format(self.cmds[i][j],'08b')]

				# convert each bit to a predefined signal length
				for k in range(len(bits)):
					if k == 1:
						for l in range(self.samples_one):
							data.append(toggle)
					elif k == 0:
						for l in range(self.samples_zero):
							data.append(toggle)

					toggle ^= 0x01
					s += 1

			# pad the remaining message
			for m in range(self.samples_intvl - s):
				data.append(toggle)
				s += 1

			toggle ^= 0x01

		return data

	def move_forward(self, index, length):
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

	def move_backward(self, index, length):
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

	def twist_left(self, index, length):
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

	def twist_right(self, index, length):
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

	def turn_left_forward(self, index, length):
		"""Turns the robot left, by driving its right-wheel forward. 

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, 0x00)
			self.cmds[index + i][1] = self.motor(Choreography.speed, Choreography.fwd)

		return

	def turn_right_forward(self, index, length):
		"""Turns the robot right by driving its left-wheel forward.

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, Choreography.fwd)
			self.cmds[index + i][1] = self.motor(Choreography.speed, 0x00)
		
		return

	def turn_left_backward(self, index, length):
		"""Turns the robot left, by driving its left-wheel backwards. 

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, Choreography.bwd)
			self.cmds[index + i][1] = self.motor(Choreography.speed, 0x00)

		return

	def turn_right_backward(self, index, length):
		"""Turns the robot right by driving its right-wheel backwards.

		Args:
			index (int): Command index for inserting motion primitive
			length (int): Number of sequential commands to insert

		Returns:
			None
			
		"""
		for i in range(length):
			self.cmds[index + i][0] = self.motor(Choreography.speed, 0x00)
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
