#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa
import math
import wave
import struct
import matplotlib
import matplotlib.pyplot as plt
import numpy as np 

def get_beats(y):
    # Separate harmonics and percussives into two waveforms
    y_harm, y_perc = librosa.effects.hpss(y)

    # Beat track on the percussive signal
    bpm, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sr)

    # Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return bpm, beat_times


def bitstream_to_wav(ch_l, ch_r, filename="output.wav", framerate=44100):
    if len(ch_l) != len(ch_r):
        raise ValueError("Left and right channel lists must be of equal length: ({}, {})".format(len(ch_l), len(ch_r)))

    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(2) # number of channels
        wav_file.setsampwidth(2) # sample with [bytes]
        wav_file.setframerate(framerate) # frame-rate [Hz]
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

def sinewave(freq, sample_rate, duration_milliseconds=100, volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :)
    """
    num_samples = int(duration_milliseconds * (sample_rate / 1000.0))

    samples = []
    for x in range(num_samples):
        samples.append(
            volume * math.sin(2 * math.pi * freq * (x / sample_rate))
        )

    return samples


if __name__ == "__main__":
    # Load song file
    y, sr = librosa.load("./samples/dance_demo.mp3", sr=None, mono=False)
    print('Sampling rate: {} Hz | Channels: {} | Samples: {}'.format(sr, np.size(y, 0), np.size(y, 1)))

    ch_l = y[0]
    ch_r = y[1]
    beep = sinewave(440, sr)

    # Get beats
    bpm, beat_times = get_beats(ch_l) # @TODO need mono to properly get beats?
    print('Number of beats: {}'.format(len(beat_times)))
    print('Estimated tempo: {:.2f} BPM'.format(bpm))

    # Construct bitstream
    bitstream = []
    beat_index = 0
    sample_index = 0
    while sample_index < np.size(y, 1):
        if beat_index >= len(beat_times):
            bitstream.append(0)
            sample_index += 1
        else:
            if sample_index / float(sr) < beat_times[beat_index]:
                bitstream.append(0)
                sample_index += 1
            else:
                # bitstream.append(1) # @TODO Append beep sound
                bitstream += beep
                sample_index += len(beep)
                beat_index += 1
    
    # Construct WAV file
    print("Constructing WAV file...")
    bitstream_to_wav(ch_l, bitstream)
    print("Done")
    
    # Plot bitstream
    # ax1 = plt.subplot(211)
    # plt.title('Bitstream')
    # plt.plot(bitstream)
    # plt.show()