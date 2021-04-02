#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


def plot(channel_l, channel_r, sample_rate=44100):
    if len(channel_l) != len(channel_r):
        raise ValueError(
            "Left and right channel lists must be of equal length: ({}, {})".format(
                len(channel_l), len(channel_r)
            )
        )

    t = []
    for x in range(len(channel_l)):
        t.append(x / float(sample_rate))  # [seconds]

    # @TODO Restrict panning in y-axis
    # https://stackoverflow.com/questions/16705452/matplotlib-forcing-pan-zoom-to-constrain-to-x-axes
    ax1 = plt.subplot(211)
    plt.plot(t, channel_l)
    plt.ylabel("Left Channel")

    ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
    plt.plot(t, channel_r)
    plt.ylabel("Right Channel")

    plt.xlim([0.00, 0.025])
    plt.xlabel("Seconds")

    plt.show()


# @TODO For any arbitrary input, show the start of a frame, left/right motor, and LEDs
# Guide: https://matplotlib.org/stable/tutorials/index.html
# Annotations: https://matplotlib.org/stable/tutorials/text/annotations.html#sphx-glr-tutorials-text-annotations-py
