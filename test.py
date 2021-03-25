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
    import dancebots as db
    from dancebots import Move

    # Pseudocode
    db.load('./samples/dance_demo.mp3')
    db.metronome('metronome.wav') # write metronome file

    # Alt-1
    move = Move('beats')
    for i in range(5):
        move.forward(1)
        move.backward(1)
    move.stop(1)

    # # Alt-2
    # frame = Frame()
    # frame.create()
    # frame.create(l_motor, r_motor)
    # frame.create(leds)
    # frame.create(l_motor, r_motor, leds)
    
    # db.sync(move) # generate synchronized bitstream from moves and lights
    # db.sync(frame) # i.e. Move class should inherit Frame class
    # db.plot() # plot WAV file with L/R channels
    # db.save("output.wav")


    # import dancebots.utils.convert as convert
    # import dancebots.utils.plot as plt

    # from dancebots.core.move import Move

    # move = Move()
    # move.forward(1)
    # move.backward(1)
    # move.left(1)
    # move.right(1)
    # move.stop(1)

    # Convert moves to bitstream
    # bitstream = moves_to_bitstream(move.frames)
    # y, sr = convert.bitstream_to_wav(bitstream, bitstream)

    # Plot bitstream
    # plt.plot(bitstream, 44100)
    