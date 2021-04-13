# -*- coding: utf-8 -*-
"""Waveforms

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
