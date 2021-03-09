#!/usr/bin/env python

'''
librosa_test.py: Test libROSA audio library
'''

# Beat tracking example
from __future__ import print_function
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np



hop_length = 512 # The number of samples between successive frames, e.g. the columns of a spectrogram.

# load song file
y, sr = librosa.load("test.mp3")

# separate harmonics and percussives into two waveforms
y_harm, y_perc = librosa.effects.hpss(y)

# beat track on the percussive signal
bpm, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sr)

# generate spectrogram
S = librosa.feature.melspectrogram(y=y_harm, sr=sr)

# unit conversion
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# output some data
print('Estimated tempo: {:.2f} beats per minute'.format(bpm))
librosa.output.times_csv('beat_times.csv', beat_times)

# plot data
plt.figure()
plt.subplot(211)
librosa.display.waveplot(y_harm, sr=sr, alpha=0.25)
librosa.display.waveplot(y_perc, sr=sr, color='r', alpha=0.5)
plt.subplot(212)
librosa.display.specshow(librosa.power_to_db(S, ref=np.max), x_axis='time', y_axis='mel')
plt.show()
