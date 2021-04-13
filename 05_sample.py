#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots import utils

# Load song file
audio, sample_rate = utils.load("./samples/dance_demo.mp3")

# Get beats
bpm, beat_times = utils.get_beats(audio, sample_rate)
print("Number of beats: {}".format(len(beat_times)))
print("Estimated tempo: {:.2f} BPM".format(bpm))

# Construct metronome bitstream
bitstream = utils.convert.beats_to_bitstream(beat_times, sample_rate)

# Make bitstream the same length as audio channel
bitstream += [0] * (audio.shape[1] - len(bitstream))

# Construct WAV file
print("Constructing WAV file...")
utils.create_wav(
    channel_l=audio[0],
    channel_r=bitstream,
    filename="output.wav",
    sample_rate=sample_rate,
)
print("Done")
