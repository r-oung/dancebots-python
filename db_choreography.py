#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates dancebot choreography bitstream.

This script takes as input a dance choreography (.CSV) and a light choreography (.CSV), and generates a choreography-bitstream (.WAV) using dancebot-protocol.

Example:
	This script can be run as follows:
		$ python db_choreography.py

Todo:
	LED should synchronize pattern to the music
	- Quantity of LEDs blinking should be a function of low-frequency beats/intensity
	- LED blinking frequency should be a function of music frequency
	- Add special functions to add, subtract, multiply, and divide the moves such that we can easily concatenate primitives
		- move1 = move.forward(time) + move.backward(time) + twist.left(time) + twist.right(time)
		- move2 = twistf(freq, time) + movef(freq, time)
		- move3 = move2 * 2
		- choreography.append(index, move1)
		- choreography.append(index, move2)
		- choreography.append(index, move3)
		- choreography.bitstream

"""

# from __future__ import unicode_literals

import sys
import random
import numpy as np
import matplotlib.pyplot as plt 

from scipy.io import wavfile


class Dancebot:
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

	def bitstream(self):
		"""Generates dancebot-bitsream from choreography

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

class Choreography(Dancebot):
	""" Choreography base class.

	This class consists of both motion and LED choreographies.
	"""

	def insert_motion_tandf(self, index, freq, period):
		"""Moves the robot forwards and backwards repeatedly.

		Args:
			index (int): Time index for when to start the dance primitive [sec]
			freq (float): Frequency in which to operate the dance primitive [Hz]
			period (int): Length of time in which to operate the dance primitive [sec]

		Returns:
			None

		"""
		reps = freq * period # number of dance primitive repetitions

		# unit conversion from [sec] to [commands]
		cmd_index, cmd_period = self.time2cmd(index, freq)

		# insert dance primitive
		for i in range(reps):
			self.move_forward(cmd_index, int(0.5 * cmd_period))
			cmd_index += cmd_period

			self.move_backward(cmd_index, int(0.5 * cmd_period))
			cmd_index += cmd_period

		return 

	def insert_motion_twist(self, index, freq, period):
		"""Twists the robot left and right repeatedly.
		
		Args:
			index (int): Time index for when to start the dance primitive [sec]
			freq (float): Frequency in which to operate the dance primitive [Hz]
			period (int): Length of time in which to operate the dance primitive [sec]

		Returns:
			None

		"""
		reps = freq * period # number of dance primitive repetitions

		# unit conversion from [sec] to [commands]
		cmd_index, cmd_period = self.time2cmd(index, freq)

		# insert dance primitive
		for i in range(reps):
			self.twist_left(cmd_index, int(0.5 * cmd_period))
			cmd_index += cmd_period

			self.twist_right(cmd_index, int(0.5 * cmd_period))
			cmd_index += cmd_period

		return 

	def insert_light_pattern_a(self, index, freq, period):
		"""LEDs change randomly for a set number of repetitions.
		
		Args:
			index (int): Time index for when to start the light pattern [sec]
			freq (float): Frequency in which to operate the light pattern [Hz]
			period (int): Length of time in which to operate the dance primitive [sec]

		Returns:
			None

		"""
		reps = freq * period # number of light pattern repetitions

		# insert LED pattern
		for i in range(reps):
			val = random.getrandbits(8)
			self.blink_led(index, freq, val, val)

		return

	def insert_light_pattern_b(self, index, freq, period):
		"""LEDs change turn on and off for a set number of repetitions.
		
		Args:
			index (int): Time index for when to start the light pattern [sec]
			freq (float): Frequency in which to operate the light pattern [Hz]
			period (int): Length of time in which to operate the dance primitive [sec]

		Returns:
			None

		"""
		reps = freq * period # number of light pattern repetitions

		# insert LED pattern
		for i in range(reps):
			self.blink_led(index, freq, 0xFF, 0x00)

		return

	def insert_light_pattern_c(self, index, freq, period):
		""" Description not provided.
		
		Args:
			index (int): Time index for when to start the light pattern [sec]
			freq (float): Frequency in which to operate the light pattern [Hz]
			period (int): Length of time in which to operate the dance primitive [sec]

		Returns:
			None

		"""
		reps = freq * period # number of light pattern repetitions

		# insert LED pattern
		val1 = random.getrandbits(8)
		val2 = ~val1
		
		for i in range(reps):
			self.blink_led(index, freq, val1, val2)

		return

	def __repr__(self):
		return "Choreography({}, {})".format(self.samples, self.sampling_rate)


def main():
	"""
	INPUT
		arg0: dance choreography (.CSV)
		arg1: light choreographyc (.CSV)

	OUTPUT
		choreography file (.WAV) in Dancebot protocol
	"""


	"""
	A dance choreography consists of a list of dance primitives with associated parameters:

	['DANCE-PRIMITIVE-NAME', INDEX, FREQUENCY, PERIOD]
	
	  DANCE-PRIMITIVE-NAME: Name of the dance primitive [to_and_fro, twist]
	 				 INDEX: Time index in which to start the dance primitive [sec]
	 			 FREQUENCY: Frequency in which to operate the dance primitive [Hz]
	  				PERIOD: Length of time in which to operate the dance primitive [sec]
	"""
	rate, data = wavfile.read("test.wav")

	motion_list = [
		('TANDF', 5, 1, 10),
		('TWIST', 10, 2, 5),
		('TANDF', 30, 1, 7),
		('TWIST', 60, 2, 4),
	]

	lights_list = [
		('A', 5, 1, 10),
		('B', 15, 5, 10),
		('C', 25, 2, 5)]

	print("No. Samples: {}".format(data.shape[0]))
	print("Sampling Rate: {} Hz".format(rate))

	c = Choreography(data.shape[0], rate)
	print(c)

	# reverse motion-list such that the first element we pop from the list if the first dance primitive
	motion_list.reverse()

	# step through the motion-list and convert from dance primitives to motor commands
	for i in range(len(motion_list)):
		primitive, index, freq, period = motion_list.pop()
		"""
		primitive: name of the dance primitive
		index: time index for when to start the dance primitive [sec]
		freq: frequency in which to operate the dance primitive [Hz]
		period: length of time in which to operate the dance primitive [sec]
		"""

		# insert dance primitives
		if primitive == "TANDF":
			print("Add To and Fro")
			c.insert_motion_tandf(index, freq, period)
		elif primitive == "TWIST":
			print("Add Twist")
		else:
			print("No such primitive exists!")

	# step through the lights-list and convert from light pattern to LED commands
	for i in range(len(lights_list)):
		pattern, index, freq, period = lights_list.pop()
		"""
		pattern: name of the light pattern
		index: time index for when to start the light pattern [sec]
		freq: frequency in which to operate the light pattern [Hz]
		period: length of time in which to operate the light pattern [sec]
		"""

		# insert light pattern
		if pattern == "A":
			c.insert_light_pattern_a(index, freq, period)
		elif pattern == "B":
			c.insert_light_pattern_b(index, freq, period)
		elif pattern == "C":
			c.insert_light_pattern_c(index, freq, period)
		else:
			print("No such pattern exists!")

	# plot stuff
	t = range(0, c.cmds_total)
	t = [x * c.msg_intvl for x in t]

	plt.figure(1)
	plt.subplot(211)
	plt.title("Motor Commands")
	plt.plot(t, c.cmds_motor_left, label="Left Motor")
	plt.plot(t, c.cmds_motor_right, label="Right Motor")
	plt.xlabel("Time (sec)")
	plt.ylabel("Value")
	plt.legend()
	plt.subplot(212)
	plt.title("LED Commands")
	plt.plot(t, c.cmds_led)
	plt.xlabel("Time (sec)")
	plt.ylabel("Value")
	plt.show()

if __name__ == "__main__":
	main()
