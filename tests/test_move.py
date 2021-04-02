#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots as db
from dancebots.core import Frame, Move, Compose
import dancebots.utils as utils


# # 1. Check bit order
# move = Move()
# bin_l, bin_r = move.forward(1, 100)
# print("{} {}".format(bin_l, bin_r))

# move.clear()
# bin_l, bin_r = move.forward(1, 0)
# print("{} {}".format(bin_l, bin_r))

# move.clear()
# bin_l, bin_r = move.forward(1, 25)
# print("{} {}".format(bin_l, bin_r))


# # 2. Spin the motor for 5 seconds at full speed
# motor = [1, 0, 0, 0, 0, 0, 0, 1]
# zeros = [0] * 8
# frame = Frame(motor, motor, zeros)

# bitstream = []
# time = 0
# while time < 5:
#     bitstream += frame.bitstream
#     time += frame.duration

# utils.create_wav(channel_l=bitstream, channel_r=bitstream, filename="test_move.wav")


# 2. Spin the motor for 5 beats at full speed
move = Move()
move.forward(5)

# composition = Compose(move, None)
# bitstream = utils.convert.composition_to_bitstream(composition, None)
# print(len(bitstream))

db.insert(move)
db.save()
db.plot()
