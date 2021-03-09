#!/usr/bin/env python
# -*- coding: utf-8 -*-

# - move1 = move.forward(time) + move.backward(time) + twist.left(time) + twist.right(time)
# - move2 = twistf(freq, time) + movef(freq, time)
# - move3 = move2 * 2
# - choreography.append(index, move1)
# - choreography.append(index, move2)
# - choreography.append(index, move3)
# - choreography.bitstream

from scipy.io import wavfile

import move
import choreography as c

def main():
	# import some data
	rate, data = wavfile.read("test.wav")
	print("No. Samples: {}".format(data.shape[0]))
	print("Sampling Rate: {} Hz".format(rate))

	# instantiate dance class
	dance = c.Choreography(data.shape[0], rate)

	# create moves
	move1 = move.forward(5) + move.backward(10)
	move2 = move1 * 2
	move2.append(move1)

	# insert moves into the dance
	dance.insert(4, move1)
	dance.insert(5, move2)
	# return bitstream
	# dance.bitstream()

if __name__ == "__main__":
	main()
