# -*- coding: utf-8 -*-
"""Plot module.

@TODO Show the start of a frame, left/right motor, and LEDs
- Guide: https://matplotlib.org/stable/tutorials/index.html
- Annotations: https://matplotlib.org/stable/tutorials/text/annotations.html#sphx-glr-tutorials-text-annotations-py
"""
import matplotlib.pyplot as plt
from ..core import Frame, Bitstream


def plot1ch(data, sample_rate=44100, xlim=None):
    """Plot single channel time-series data.

    Attributes:
            data: Time-series.
            channel_r: Right channel time-series.
            sample_rate: Audio sampling rate (Hz).
            xlim: List of x-axis limits [minimum, maximum]
    """
    bits = []
    if isinstance(data, Frame):
        print("Printing Frames")
        bits = Bitstream([data], sample_rate).bits
    elif isinstance(data, Bitstream):
        print("Printing Bitstream")
        bits = data.bits
        sample_rate = data.sample_rate
    elif isinstance(data, list):
        if isinstance(data[0], Frame):
            bits = Bitstream(data, sample_rate).bits
        elif isinstance(data[0], int):
            print("Printing List")
            bits = data
        else:
            raise ValueError("Unsupported data type")
    else:
        raise ValueError("Unsupported data type")

    time = []
    for sample in range(len(bits)):
        time.append(sample / float(sample_rate))  # [seconds]

    if xlim is None:
        xlim = [0.00, 0.015]

    plt.plot(time, bits)
    plt.xlim(xlim)
    plt.xlabel("Seconds")
    plt.show()


def plot2ch(channel_l, channel_r=None, sample_rate=44100, xlim=None):
    """Plot dual channel time-series data.

    Attributes:
            channel_l: Left channel time-series.
            channel_r: Right channel time-series.
            sample_rate: Audio sampling rate (Hz).
            xlim: List of x-axis limits [minimum, maximum]
    """
    if len(channel_l) != len(channel_r):
        raise ValueError(
            "Left and right channel lists must be of equal length: ({}, {})".format(
                len(channel_l), len(channel_r)
            )
        )

    time = []
    for sample in range(len(channel_l)):
        time.append(sample / float(sample_rate))  # [seconds]

    if xlim is None:
        xlim = [0.00, 0.015]

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


def plot(channel_l, channel_r=None, sample_rate=44100, xlim=None):
    """Plot time-series data.

    Attributes:
            channel_l: Left channel time-series.
            channel_r: Right channel time-series.
            sample_rate: Audio sampling rate (Hz).
            xlim: List of x-axis limits [minimum, maximum]
    """
    if channel_r is None:
        plot1ch(channel_l, sample_rate, xlim)
    else:
        plot2ch(channel_l, channel_r, sample_rate, xlim)
