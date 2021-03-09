#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generates dancebot choreography bitstream.

This script takes as input a dance choreography (.CSV) and a light choreography (.CSV), and generates a choreography-bitstream (.WAV) using dancebot-protocol.

Email from Philipp Reist:
	Given the 8MHz clock of the ATTiny, a pulse (i.e. time between to edges of the MP3 player voltage on the right channel) is considered a RESET, or start of a new 24bit message, if it is longer than 5805 ticks (0.73ms, or 32 samples at 44.1kHz), considered a 1 if it is between 3367 and 5805 ticks, and a 0 if it is below 3367 ticks. Then, the 24 bit message consists of 8bits for the left motor, 8bits for the right motor, and 8 bits for the 8 LEDs. The LSB is sent first. For the motors, bit 0-6 is speed (valid range 0-100), and bit 7 is direction (1 FWD, 0 BWD [this is wrongly labeled in the FW on Bitbucket). For the LEDs, each bit corresponds directly to the LED.

Summary:
	=================================================
	COMMAND FORMAT
	=================================================
	Messages are 24-bits long, LSB sent first.

	[ left-motor | right-motor | 8-LEDs ]
	[   8-bits   |   8-bits    | 8-bits ]

	=================================================
	BIT REPRESENTATION
	=================================================
	TYPE | Ticks		| Seconds
	-------------------------------------------------
	START:      > 5805 	              > 0.000725625 
	    1: 3367 - 5805	  0.000420875 - 0.000725625
	    0:      < 3367 	              < 0.000420875

	The following bit representation will be used in this script:
	
		START: 1.0 msec
			0: 0.4 msec
			1: 0.6 msec

	Therefore, the longest message will be 1.0 + (24 x 0.6) = 15.4 msec.

Example:
	This script can be run as follows:
		$ python db_protocol.py

Todo:
	* Write this into a class?

	Notes to self:

	Dance Primitives
	- To and fro (frequency, period)
	- Twist(frequency, period)

	Motion Primitives
	- Forward, motion_fwd(index, period)
	- Backwards, motion_bwd(index, period)
	- Turn, motion_turn(index, period)

	LED should synchronize pattern to the music
	- Quantity of LEDs blinking should be a function of low-frequency beats/intensity
	- LED blinking frequency should be a function of music frequency

"""

# from __future__ import unicode_literals

import sys
import random
import numpy as np
import matplotlib.pyplot as plt 


FORWARD = 1
BACKWARD = 0
SPEED = 100


def motor(speed, direction):
	""" Converts motor command to a dancebot bitstream.
	
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


def move_forward(cmds, index, length):
	""" Move robot forward.

	Args:
		cmds (list): Motor speed; a value between 0-100. 
		index (bool): Motor direction

	Returns:
		None
		
	"""
	for j in range(length):
		cmds[index + j][0] = motor(SPEED, FORWARD)
		cmds[index + j][1] = motor(SPEED, FORWARD)
	
	return


def move_backward(cmds, index, length):
	"""	Move robot backwards """
	for j in range(length):
		cmds[index + j][0] = motor(SPEED, BACKWARD)
		cmds[index + j][1] = motor(SPEED, BACKWARD)
	
	return


def twist_left(cmds, index, length):
	"""	Twist robot left """
	for j in range(length):
		cmds[index + j][0] = motor(SPEED, BACKWARD)
		cmds[index + j][1] = motor(SPEED, FORWARD)

	return


def twist_right(cmds, index, length):
	"""	Twist robot right """
	for j in range(length):
		cmds[index + j][0] = motor(SPEED, FORWARD)
		cmds[index + j][1] = motor(SPEED, BACKWARD)
	
	return


def turn_left(cmds, index, length):
	"""	Turn robot left forward """
	for j in range(length):
		cmds[index + j][0] = motor(SPEED, 0x00)
		cmds[index + j][1] = motor(SPEED, FORWARD)

	return


def turn_right(cmds, index, length):
	"""	Turn robot right forward """
	for j in range(length):
		cmds[index + j][0] = motor(SPEED, FORWARD)
		cmds[index + j][1] = motor(SPEED, 0x00)
	
	return


def dance_tandf(cmds, index, reps, length):
	"""	Robot moves forwards and backwards for a set number of repetitions
	[cmds] 	 Complete list of all commands sent to the robot
	[index]  Starting command index for the dance primitive
	[reps]   Number of dance primitive repetitions
	[length] Number of commands for a single repetition of the dance primitive
	"""

	# insert dance move
	for i in range(reps):
		move_forward(cmds, index, int(0.5 * length))
		index += length

		move_backward(cmds, index, int(0.5 * length))
		index += length

	return index


def dance_twist(cmds, index, reps, length):
	"""	Robot twists for a set number of repetitions
	[cmds] 	 Complete list of all commands sent to the robot
	[index]  Starting command index for the dance primitive
	[reps]   Number of dance primitive repetitions
	[length] Number of commands for a single repetition of the dance primitive
	"""

	# insert dance move
	for i in range(reps):
		twist_left(cmds, index, int(0.5 * length))
		index += length
		
		twist_right(cmds, index, int(0.5 * length))
		index += length

	return index


def dance_shuffle(cmds, index, reps, length):
	""" Robot shuffles for a set number of repetitions
	[cmds] 	 Complete list of all commands sent to the robot
	[index]  Starting command index for the dance primitive
	[reps]   Number of dance primitive repetitions
	[length] Number of commands for a single repetition of the dance primitive
	"""

	# [insert dance move]
	return


def light_pattern_a(cmds, index, beats, length):
	""" LEDs change randomly for a set number of repetitions
	[cmds] 	 Complete list of all commands sent to the robot
	[index]  Starting command index for the light pattern
	[beats]  Number of beats; LEDs change for every beat
	[length] Number of commands for a single repetition of the light pattern
	"""

	# insert LED pattern
	for i in range(beats):
		val = random.getrandbits(8)
		for j in range(int(0.5 * length)):
			cmds[index + j][2] = val

		index += int(0.5 * length)

		val = random.getrandbits(8)
		for j in range(int(0.5 * length)):
			cmds[index + j][2] = val

		index += int(0.5 * length)

	return


def light_pattern_b(cmds, index, beats, length):
	""" LEDs change turn on and off for a set number of repetitions
	[cmds] 	 Complete list of all commands sent to the robot
	[index]  Starting command index for the light pattern
	[beats]  Number of beats; LEDs change for every beat
	[length] Number of commands for a single repetition of the light pattern
	"""

	# insert LED pattern
	for i in range(beats):
		for j in range(int(0.5 * length)):
			cmds[index + j][2] = 0xFF
		
		index += int(0.5 * length)

		for j in range(int(0.5 * length)):
			cmds[index + j][2] = 0x00

		index += int(0.5 * length)

	return


def light_pattern_c(cmds, index, beats, length):
	""" 
	[cmds] 	 Complete list of all commands sent to the robot
	[index]  Starting command index for the light pattern
	[beats]  Number of beats; LEDs change for every beat
	[length] Number of commands for a single repetition of the light pattern
	"""

	# insert LED pattern
	val1 = random.getrandbits(8)
	val2 = ~val1
	
	for i in range(beats):
		for j in range(int(0.5 * length)):
			cmds[index + j][2] = val1

		index += int(0.5 * length)

		for j in range(int(0.5 * length)):
			cmds[index + j][2] = val2

		index += int(0.5 * length)

	return


def get_youtube_mp3(html):
	# try:
	#     os.remove("*.mp3")
	# except OSError:
	#     pass

	print("Downloading", html, "as MP3 from YouTube...")
	ytdl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}

	with yt.YoutubeDL(ytdl_opts) as ytdl:
	    ytdl.download(['https://www.youtube.com/watch?v=HCjNJDNzw8Y'])

	return


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
	choreography = [
		('TANDF', 5, 1, 10),
		('TWIST', 10, 2, 5),
		('TANDF', 30, 1, 7),
		('TWIST', 60, 2, 4),
	]

	lights = [
		('A', 5, 1, 10),
		('B', 15, 5, 10),
		('C', 25, 2, 5)]


	# initialise list of commands
	length = data.shape[0] / rate # song length [sec]
	cmds_max = int(length / 0.002) # total number of commands to send; where 0.002 is the length of a single command
	cmds = [[0,0,0] for i in range(cmds_max)] # predefined list of all commands

	# reverse choreography-list such that the first element we pop from the list if the first dance primitive
	choreography.reverse()

	# step through the choreography-list and convert from dance primitives to motor commands
	for i in range(len(choreography)):
		param = choreography.pop()

		primitive = param[0] # name of the dance primitive
		index = param[1] # time index for when to start the dance primitive [sec]
		freq = param[2] # frequency in which to operate the dance primitive [Hz]
		period = param[3] # length of time in which to operate the dance primitive [sec]

		# dance primitive period for a single repetition [sec]
		one_rep_period = 1.0 / freq

		# number of dance primitive repetitions
		reps = freq * period 

		# unit conversion from [sec] to [commands]
		cmd_index = int(index / 0.002)
		cmd_one_rep_period = int(one_rep_period / 0.002)

		# insert dance primitives
		if primitive == "TANDF":
			dance_tandf(cmds, cmd_index, reps, cmd_one_rep_period)
		elif primitive == "TWIST":
			dance_twist(cmds, cmd_index, reps, cmd_one_rep_period)
		else:
			print("No such primitive exists!")

	# reverse lights-list such that the first element we pop from the list if the first light pattern
	lights.reverse()

	# step through the lights-list and convert from light pattern to LED commands
	for i in range(len(lights)):
		param = lights.pop()

		pattern = param[0] # name of the light pattern
		index = param[1] # time index for when to start the light pattern [sec]
		freq = param[2] # frequency in which to operate the light pattern [Hz]
		period = param[3] # length of time in which to operate the light pattern [sec]

		# light pattern period for a single repetition [sec]
		one_rep_period = 1.0 / freq

		# number of light pattern repetitions
		reps = freq * period 

		# unit conversion from [sec] to [commands]
		cmd_index = int(index / 0.002)
		cmd_one_rep_period = int(one_rep_period / 0.002)

		# insert light pattern
		if pattern == "A":
			light_pattern_a(cmds, cmd_index, reps, cmd_one_rep_period)
		elif pattern == "B":
			light_pattern_b(cmds, cmd_index, reps, cmd_one_rep_period)
		elif pattern == "C":
			light_pattern_c(cmds, cmd_index, reps, cmd_one_rep_period)
		else:
			print("No such pattern exists!")


	# plot stuff
	t = range(0, cmds_max)
	t = [x * 0.002 for x in t]

	motor_left = [i[0] for i in cmds]
	motor_right = [i[1] for i in cmds]
	leds = [i[2] for i in cmds]	

	plt.figure(1)
	plt.subplot(211)
	plt.title("Motor Commands")
	plt.plot(t, motor_left, label="Left Motor")
	plt.plot(t, motor_right, label="Right Motor")
	plt.xlabel("Time (sec)")
	plt.ylabel("Value")
	plt.legend()
	plt.subplot(212)
	plt.title("LED Commands")
	plt.plot(t, leds)
	plt.xlabel("Time (sec)")
	plt.ylabel("Value")
	plt.show()


if __name__ == "__main__":
	main()