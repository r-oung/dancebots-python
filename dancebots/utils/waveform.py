# -*- coding: utf-8 -*-
"""Waveforms

Functions for generating standard audio waveforms.

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
import math


def sinewave(frequency, sample_rate, duration_milliseconds=100, volume=1.0):
    """Sine wave.

    Attributes:
            frequency: Frequency (Hz)
            sample_rate: Audio sampling rate (Hz).
            duration_milliseconds: Duration (msec).
            volume: Volume [0, 1]
    """
    num_samples = int(duration_milliseconds * (sample_rate / 1000.0))

    samples = []
    for sample in range(num_samples):
        samples.append(
            volume * math.sin(2 * math.pi * frequency * (sample / sample_rate))
        )

    return samples
