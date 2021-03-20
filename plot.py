#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa
import matplotlib
import matplotlib.pyplot as plt
import numpy as np 

# https://librosa.org/doc/latest/generated/librosa.load.html
y, sr = librosa.load('./output.wav', sr=None, mono=False)
print('Sampling rate: {} Hz | Channels: {} | Samples: {}'.format(sr, np.size(y, 0), np.size(y, 1)))

ch_l = y[0]
ch_r = y[1]

t = []
for i in range(np.size(y, 1)):
    t.append(float(i) / sr)

# Plot bitstream
ax1 = plt.subplot(211)
plt.plot(ch_l)
plt.ylabel('Left Channel')

ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
plt.plot(ch_r)
plt.ylabel('Right Channel')
plt.xlabel('Samples')

plt.show()

# @TODO For any arbitrary input, show the start of a frame, left/right motor, and LEDs
# Guide: https://matplotlib.org/stable/tutorials/index.html
# Annotations: https://matplotlib.org/stable/tutorials/text/annotations.html#sphx-glr-tutorials-text-annotations-py