#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create dancebot choreography through user input.


Reference:
	- https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/

Todo:
	- play song in a thread:
	- https://gist.github.com/guysoft/bda8ff5be7eb708fd7057850d788dbdf

Workflow:
- Play music
- Visualise the music and the "beats"
- Visualise light patterns
- User can tap at the keyboard to generate light patterns
- How to control robot motion???

"""

import time
import sys
import threading

import numpy as np
import colorama  # platform independent way of colouring terminal output

from pydub import AudioSegment  # Python 2.7.x
from pydub.playback import play
from scipy.io import wavfile


user_val = None
stored_exception = None


def t_player(song):
    """Player thread function."""
    play(song)
    return


def t_input():
    while True:
        user_val = sys.stdin.read(1)
        print ("HELLO")


max_val = 2 ** 16
bars = 20

sub_sampling_frequency = 24.0  #: sub-sampling frequency [Hz]
sub_sampling_period = 1.0 / sub_sampling_frequency  #: sub-sampling period [sec]

filename = "test.wav"  # filename of the WAV file
song = AudioSegment.from_wav(filename)
sampling_rate, samples = wavfile.read(filename)

inc = int(sub_sampling_period * sampling_rate)

# t = threading.Thread(target=t_player, args=(song,))
# t.setDaemon(True)
# t.start()
t = threading.Thread(target=t_input)
t.setDaemon(True)
t.start()

for i in range(0, len(samples), inc):
    # user_val = sys.stdin.read()

    try:
        if stored_exception:
            break

        # collect a subset of all left and right channel samples
        dataL = samples[i : i + inc][0]
        dataR = samples[i : i + inc][1]

        # calculate peak value
        factor = 5
        peakL = factor * float(abs(max(dataL) - min(dataL))) / max_val
        peakR = factor * float(abs(max(dataR) - min(dataR))) / max_val
        # print("L:{0:0.2f}\tR:{0:0.2f}".format(peakL, peakR))

        # visualize values
        lString = "■" * int(bars * peakL) + " " * int(bars * (1.0 - peakL))
        rString = "■" * int(bars * peakR) + " " * int(bars * (1.0 - peakR))
        print ("L[%s]\tR[%s]\t[%s]" % (lString, rString, user_val))

        # sleep for visualization purposes
        time.sleep(sub_sampling_period)

    except KeyboardInterrupt:
        stored_exception = sys.exc_info()

if stored_exception:
    print "Exiting gracefully."
    # raise stored_exception[0], stored_exception[1], stored_exception[2]

sys.exit()
