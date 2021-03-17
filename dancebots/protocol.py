#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Protocol:
	"""Dancebots protocol

	"""
	_start_duration = 2.0 # start bit duration [msec]
	_one_duration = 0.7 # one bit duration [msec]
	_zero_duration = 0.2 # zero bit duration [msec]


	def __init__(self, sample_rate=44100):
		self.samples = []
		self.sample_rate = sample_rate
		

	def _start(self):
		num_samples = int(self._start_duration * (self.sample_rate / 1000.0))

		for x in range(num_samples):
			self.samples.append(1.0)
		
		return


	def _one(self):
		num_samples = int(self._one_duration * (self.sample_rate / 1000.0))

		for x in range(num_samples):
			self.samples.append(1.0)
		
		return


	def _zero(self):
		num_samples = int(self._zero_duration * (self.sample_rate / 1000.0))

		for x in range(num_samples):
			self.samples.append(0.0)
		
		return


	def append_frame(self, l_motor=[0]*8, r_motor=[0]*8, leds=[0]*8):
		if len(l_motor) is not 8:
			raise ValueError("Left motor must contain at least 8 values")

		if len(r_motor) is not 8:
			raise ValueError("Right motor must contain at least 8 values")

		if len(leds) is not 8:
			raise ValueError("LEDs must contain at least 8 values")
		
		self._start()
		
		frame = l_motor + r_motor + leds
		for x in frame:
			if x is 1:
				self._one()
			elif x is 0:
				self._zero()
			else:
				raise ValueError("Frame must contain binary values, i.e. 0 or 1")
		
		return 0


	@property
	def bitstream(self):
		return self.samples;


if __name__ == "__main__":
	protocol = Protocol()
	l_motor = [0,1,1,1,1,0,1,0]
	r_motor = [0,1,1,1,1,0,1,0]
	leds = [0,1,0,1,0,1,0,1]
	protocol.append_frame(l_motor, r_motor, leds)
	print(protocol.bitstream)
