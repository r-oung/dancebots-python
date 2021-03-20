#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wave
import struct
import random

from dancebots import Move
from dancebots import Frame

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

# Convert bitstream to WAV file
def bitstream_to_wav(bitstream, filename="output.wav", framerate=44100):
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(2) # number of channels
        wav_file.setsampwidth(2) # sample with [bytes]
        wav_file.setframerate(framerate) # frame-rate [Hz]
        wav_file.setnframes(len(bitstream))
        wav_file.setcomptype("NONE", "Not compressed") # compression type

        # WAV file here is using short (16-bit) signed integers
        # So we multiply each bit by 32767 to get the maximum value
        bin_list = []
        for bit in bitstream:
            # channel-1
            bin_data = struct.pack('h', 0)
            bin_list.append(bin_data)

            # channel-2
            bin_data = struct.pack('h', int(bit * 32767.0))
            bin_list.append(bin_data)

        bin_string = b''.join(bin_list)
        wav_file.writeframes(bin_string)
    
    return


if __name__ == "__main__":
    import matplotlib
    import matplotlib.pyplot as plt

    move = Move()
    move.forward(1)
    # move.backward(1)
    # move.left(1)
    # move.right(1)
    # move.stop(1)

    # Convert moves to bitstream
    bitstream = moves_to_bitstream(move.frames)
    bitstream_to_wav(bitstream)

    # Plot bitstream
    plt.title('Bitstream')
    plt.plot(bitstream[0:1000])
    plt.yticks([0, 1])
    plt.xlabel('Samples')
    plt.ylabel('Binary Value')
    plt.show()
