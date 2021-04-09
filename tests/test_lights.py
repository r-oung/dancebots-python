#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Light
import dancebots.utils as utils


# 1. Prints lights
light = Light("seconds")
light.blink([1, 0, 1, 0, 1, 0, 1, 0], 3, 2)
light.hold([1, 1, 0, 0, 1, 1, 0, 0], 2)
light.stop(1)
print(light)


# # 2. Keeps lights on for 5 seconds
# light = Light()
# light.hold(leds, 5)
# print(light)

# composition = Compose(moves=None, lights=light)
# print(composition)

# bitstream = utils.convert.composition_to_bitstream(composition)
# utils.create_wav(channel_l=bitstream, channel_r=bitstream, filename="test_lights2.wav")
