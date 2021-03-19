#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa

# Get the file path to an included audio example
filename = librosa.example('nutcracker')


# Load the audio as a waveform `y`
# Store the sampling rate as `sr`
y, sr = librosa.load(filename)

# Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# @TODO Separate harmonics and percussives from waveforms
# https://librosa.org/doc/latest/tutorial.html
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

# Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
