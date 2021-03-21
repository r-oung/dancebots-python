#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wave
import struct

def bitstream_to_wav(ch_l, ch_r, filename="output.wav", sr=44100):
    if len(ch_l) != len(ch_r):
        raise ValueError("Left and right channel lists must be of equal length: ({}, {})".format(len(ch_l), len(ch_r)))

    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(2) # number of channels
        wav_file.setsampwidth(2) # sample with [bytes]
        wav_file.setframerate(sr) # frame-rate [Hz]
        wav_file.setnframes(len(ch_l))
        wav_file.setcomptype("NONE", "Not compressed") # compression type

        # WAV file here is using short (16-bit) signed integers
        # So we multiply each bit by 32767 to get the maximum value
        bin_list = []
        for i in range(len(ch_l)):
            # left-channel
            bin_data = struct.pack('h', int(ch_l[i] * 32767.0))
            bin_list.append(bin_data)

            # right-channel
            bin_data = struct.pack('h', int(ch_r[i] * 32767.0))
            bin_list.append(bin_data)

        bin_string = b''.join(bin_list)
        wav_file.writeframes(bin_string)
    
    return
