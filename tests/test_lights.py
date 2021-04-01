#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Frame, Light, Compose
import dancebots.utils as utils


# Spin the motor for 5 seconds
leds = [1, 0, 1, 0, 1, 0, 1, 0]
zeros = [0] * 8
frame = Frame(zeros, zeros, leds)

bitstream = []
time = 0
while time < 5:
    bitstream += frame.bitstream
    time += frame.duration

utils.create_wav(channel_l=bitstream, channel_r=bitstream, filename="test_lights.wav")


# Spin the motor for 5 beats
light = Light()
light.hold(leds, 5)
print(light)

composition = Compose(moves=None, lights=light)
print(composition)

bitstream = utils.convert.composition_to_bitstream2(composition)
utils.create_wav(channel_l=bitstream, channel_r=bitstream, filename="test_lights2.wav")
