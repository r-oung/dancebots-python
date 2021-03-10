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
class Protocol:
	"""Dancebots protocol

	"""
	start = 2.0 #: start bit period [msec]
	one = 0.7 #: one bit period [msec]
	zero = 0.2 # zero bit period [msec]

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


if __name__ == "__main__":
	pass
