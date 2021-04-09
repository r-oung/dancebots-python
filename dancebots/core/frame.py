#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy

class Frame:
    """A single Dancebots frame"""

    # Static variables
    _START = 2.0  # start bit duration [msec]
    _ONE = 0.7  # one bit duration [msec]
    _ZERO = 0.2  # zero bit duration [msec]

    def __init__(self, motor_l=[0] * 8, motor_r=[0] * 8, leds=[0] * 8, sample_rate=44100):
        # Non-static variables
        self._sample_rate = sample_rate
        self._last_value = 1  # WAV value; toggles between -1 and +1
        self._bits = [] # list of bits
        self._frames = [] # list of frames

        if len(motor_l) != 8:
            raise ValueError("Left motor must contain at least 8 values")

        if len(motor_r) != 8:
            raise ValueError("Right motor must contain at least 8 values")

        if len(leds) != 8:
            raise ValueError("LEDs must contain at least 8 values")

        self._append(self._START)

        frame = motor_l + motor_r + leds
        self._frames.append(frame)
        for x in frame:
            if x == 1:
                self._append(self._ONE)
            elif x == 0:
                self._append(self._ZERO)
            else:
                raise ValueError("Frame must contain binary values, i.e. 0 or 1")

    def _append(self, duration):
        self._last_value *= -1  # toggle value
        num_samples = int(duration * (self._sample_rate / 1000.0))
        for x in range(num_samples):
            self._bits.append(self._last_value)

    @property
    def bits(self):
        return self._bits

    @property
    def frames(self):
        return self._frames

    @property
    def length(self):
        return len(self._bits)

    @property
    def duration(self):
        sample_period = 1.0 / self._sample_rate
        return len(self._bits) * sample_period  # [seconds]

    def __str__(self):
        lines = []
        for frame in self._frames:
            lines.append(str(frame))
        return "\n".join(lines)

    def __add__(self, other):
        if self._sample_rate != other._sample_rate:
            raise ValueError("Sampling rates are different")

        # Make a copy of this instance
        frame = deepcopy(self)

        # Append other instance
        frame._frames += other._frames

        # If last bit of this frame is the same as the first 
        # bit of the other frame, then flip the bits in the other frame
        # Note: First bit of a frame is always -1
        if frame._last_value == -1:
            frame._bits = self.bits + [x*-1 for x  in other.bits]
        else:
            frame._bits = self.bits + other.bits

        frame._last_value = other._last_value
        
        return frame

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
