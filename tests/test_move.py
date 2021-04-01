#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Frame, Move, Compose
import dancebots.utils as utils


# Spin the motor for 5 seconds at full speed
motor = [1, 0, 0, 0, 0, 0, 0, 1]
zeros = [0] * 8
frame = Frame(motor, motor, zeros)

bitstream = []
time = 0
while time < 5:
    bitstream += frame.bitstream
    time += frame.duration

utils.create_wav(channel_l=bitstream, channel_r=bitstream, filename="test_move.wav")


# Spin the motor for 5 beats at full speed
move = Move()
move.forward(5)
print(move)

composition = Compose(moves=move, lights=None)
print(composition)

bitstream = utils.convert.composition_to_bitstream2(composition)
utils.create_wav(channel_l=bitstream, channel_r=bitstream, filename="test_move2.wav")
utils.plot(channel_l=bitstream, channel_r=bitstream)
