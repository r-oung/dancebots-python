#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

def sinewave(freq, sr, duration_milliseconds=100, volume=1.0):
    """
    The sine wave generated here is the standard beep. If you want something
    more aggresive you could try a square or saw tooth waveform.
    """
    num_samples = int(duration_milliseconds * (sr / 1000.0))

    samples = []
    for x in range(num_samples):
        samples.append(
            volume * math.sin(2 * math.pi * freq * (x / sr))
        )

    return samples