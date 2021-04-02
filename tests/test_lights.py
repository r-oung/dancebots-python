#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Frame, Light, Compose
import dancebots.utils as utils


# 1. Keeps lights on for 5 seconds
leds = [1, 0, 1, 0, 1, 0, 1, 0]
zeros = [0] * 8
frame = Frame(zeros, zeros, leds)

time = 0
while time < 5:
    frame += frame
    time += frame.duration

utils.create_wav(channel_l=frame.data, channel_r=frame.data, filename="test_lights.wav")


# 2. Keeps lights on for 5 seconds
light = Light()
light.hold(leds, 5)
print(light)

composition = Compose(moves=None, lights=light)
print(composition)

bitstream = utils.convert.composition_to_bitstream(composition)
utils.create_wav(channel_l=bitstream, channel_r=bitstream, filename="test_lights2.wav")
