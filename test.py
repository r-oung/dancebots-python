#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots import Move
from dancebots import Frame


# Convert instructions / frames to audio
def moves_to_bitstream(moves, bpm=120):
    beat_length = 60.0 / bpm  # seconds per beat

    bitstream = []
    for move in moves:
        move_duration = move["beats"] * beat_length  # convert beats to seconds

        time = 0
        while time < move_duration:
            frame = Frame()
            frame.create(move["left_motor"], move["right_motor"], [0] * 8)
            time += frame.duration
            bitstream += frame.bitstream

    return bitstream


def bitsream_to_wav(bitstream, sample_rate=44100):
    # see create.py
    pass


if __name__ == "__main__":
    move = Move()

    move.forward(5)
    move.backward(5)
    move.left(5)
    move.right(5)
    move.stop(1)

    bitstream = moves_to_bitstream(move.frames)
    print(len(bitstream))

    # Python plotting libraries
    # https://opensource.com/article/20/4/plot-data-python
    
    # Firmware: https://github.com/philippReist/dancebots_electronics/blob/master/DancebotsFirmware/src/MP3DanceBot.c
    # Watchdog set to 500 msec
