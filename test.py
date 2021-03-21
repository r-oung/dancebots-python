#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core.frame import Frame

# Convert instructions / frames to audio
# @TODO Use beat_times instead of BPM
def moves_to_bitstream(moves, lights=None, bpm=120):
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

if __name__ == "__main__":
    import dancebots.utils.convert as convert
    import dancebots.utils.plot as plt

    from dancebots.core.move import Move

    move = Move()

    move = Move()
    move.forward(1)
    # move.backward(1)
    # move.left(1)
    # move.right(1)
    # move.stop(1)

    # Convert moves to bitstream
    bitstream = moves_to_bitstream(move.frames)
    y, sr = convert.bitstream_to_wav(bitstream, bitstream)

    # Plot bitstream
    plt.plot(bitstream, 44100)
    