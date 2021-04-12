#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plot module.

@TODO Show the start of a frame, left/right motor, and LEDs
- Guide: https://matplotlib.org/stable/tutorials/index.html
- Annotations: https://matplotlib.org/stable/tutorials/text/annotations.html#sphx-glr-tutorials-text-annotations-py
"""
import matplotlib.pyplot as plt
from ..core import Frame, Bitstream


def plot(channel_l, channel_r=[], sample_rate=44100, xlim=[0.00, 0.015]):
    """Plot time-series data.

    Attributes:
            channel_l: Left channel time-series.
            channel_r: Right channel time-series.
            sample_rate: Audio sampling rate (Hz).
            xlim: List of x-axis limits [minimum, maximum]
    """
    if not channel_r:
        bitstream = []
        sr = sample_rate
        if isinstance(channel_l, Frame):
            bitstream = channel_l.bits
            sr = channel_l.sample_rate
        elif isinstance(channel_l, Bitstream):
            bitstream = channel_l.bits
        elif isinstance(channel_l, list):
            bitstream = channel_l

        time = []
        for sample in range(len(bitstream)):
            time.append(sample / float(sr))  # [seconds]

        plt.plot(time, bitstream)
        plt.xlim(xlim)
        plt.xlabel("Seconds")
        plt.show()

    else:
        if len(channel_l) != len(channel_r):
            raise ValueError(
                "Left and right channel lists must be of equal length: ({}, {})".format(
                    len(channel_l), len(channel_r)
                )
            )

        time = []
        for sample in range(len(channel_l)):
            time.append(sample / float(sample_rate))  # [seconds]

        # @TODO Restrict panning in y-axis
        # https://stackoverflow.com/questions/16705452/matplotlib-forcing-pan-zoom-to-constrain-to-x-axes
        ax1 = plt.subplot(211)
        plt.plot(time, channel_l)
        plt.ylabel("Left Channel")

        _ = plt.subplot(212, sharex=ax1, sharey=ax1)
        plt.plot(time, channel_r)
        plt.ylabel("Right Channel")

        plt.xlim(xlim)
        plt.xlabel("Seconds")

        plt.show()
