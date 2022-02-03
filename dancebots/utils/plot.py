# -*- coding: utf-8 -*-
"""Plot module

Functions for displaying audio waveform plots.

Copyright (C) 2021-2022 Raymond Oung

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
        bits = Bitstream([data], sample_rate).bits
    elif isinstance(data, Bitstream):
        bits = data.bits
        sample_rate = data.sample_rate
    elif isinstance(data, list):
        if isinstance(data[0], Frame):
            bits = Bitstream(data, sample_rate).bits
        elif isinstance(data[0], int):
            bits = data
        else:
            raise ValueError("👎 Unsupported data type")
    else:
        raise ValueError("👎 Unsupported data type")

    time = []
    for sample in range(len(bits)):
        time.append(sample / float(sample_rate))  # [seconds]

    if xlim is None:
        xlim = [0.00, 0.015]

    plt.plot(time, bits)
    plt.xlim(xlim)
    plt.xlabel("Seconds")
    plt.show()


def plot2ch(channel_l, channel_r=None, beat_times=None, sample_rate=44100, xlim=None):
    """Plot dual channel time-series data.

    Attributes:
            channel_l: Left channel time-series.
            channel_r: Right channel time-series.
            sample_rate: Audio sampling rate (Hz).
            xlim: List of x-axis limits [minimum, maximum]
    """
    if len(channel_l) != len(channel_r):
        raise ValueError(
            "👎 Left and right channel lists must be of equal length: ({}, {})".format(
                len(channel_l), len(channel_r)
            )
        )

    time = []
    for sample in range(len(channel_l)):
        time.append(sample / float(sample_rate))  # [seconds]

    # if xlim is None:
    #     xlim = [0.00, 0.015]

    # @TODO Restrict panning in y-axis
    # https://stackoverflow.com/questions/16705452/matplotlib-forcing-pan-zoom-to-constrain-to-x-axes
    ax1 = plt.subplot(211)
    plt.plot(time, channel_l)
    if beat_times is not None:
        plt.vlines(x=beat_times, ymin=-1, ymax=+1, colors="red", label="beats")
    plt.ylabel("Left Channel")

    _ = plt.subplot(212, sharex=ax1, sharey=ax1)
    plt.plot(time, channel_r)
    plt.ylabel("Right Channel")

    plt.xlim(xlim)
    plt.xlabel("Seconds")

    plt.show()


def plot(channel_l, channel_r=None, beat_times=None, sample_rate=44100, xlim=None):
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
        plot2ch(channel_l, channel_r, beat_times, sample_rate, xlim)
