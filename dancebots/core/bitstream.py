#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Frame():
    """A single Dancebot frame"""

    # Static variables
    _START = 2.0  # start bit duration [msec]
    _ONE = 0.7  # one bit duration [msec]
    _ZERO = 0.2  # zero bit duration [msec]

    def __init__(self, motor_l=[0] * 8, motor_r=[0] * 8, leds=[0] * 8)
        self.motor_l = motor_l
        self.motor_r = motor_r
        self.leds = leds 

    @property
    def data(self):
        return self.motor_l + self.motor_r + self.leds
    
    @property
    def bits(self):
        

class Bitstream():
    """A sequence of Dancebot frames"""

    # Static variables
    _START = 2.0  # start bit duration [msec]
    _ONE = 0.7  # one bit duration [msec]
    _ZERO = 0.2  # zero bit duration [msec]

    def __init__(self, frames=[], sample_rate=44100)
        for frame in frames:
            if not isinstance(frame, Frame):
                raise TypeError("Must be of type Frame")
        
        if sample_rate < 0 or not isinstance(sample_rate, int):
            raise ValueError("Sample rate must be a positive integer")

        self._last_value = 1
        self.frames = frames
        self.sample_rate = sample_rate
        self.bits = []

    def _convert_frames_to_bits():
        for frame in self.frames:
            for bit in frame:
                if x == 0:
                    self._append(self._ZERO)
                elif x == 1:
                    self._append(self._ONE)
                else:
                    raise ValueError("Frame must contain binary values, i.e. 0 or 1")

    def _append(self, duration):
        num_samples = int(duration * (self.sample_rate / 1000.0))
        self._last_value *= -1  # toggle value
        
        for x in range(num_samples):
            self.bits.append(self._last_value)

    def __len__(self):
        return len(self.bits)

    def __add__(self, other):
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sampling rates are different")

        new_frames = self.frames.copy()
        new_frames = new_frames + other.frames
        return self.__class__(new_frames, self.sample_rate)
    
    def __radd__(self, other):
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sampling rates are different")
        
        new_frames = self.frames.copy()
        new_frames = other.frames + new_frames
        return self.__class__(new_frames, self.sample_rate)
    
    def __iadd__(self, other):
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sampling rates are different")
        
        self.bits = []
        self.frames += other.frames
        _convert_frames_to_bits()
        return self

    def __str__(self):
        lines = []
        for frame in self._frames:
            lines.append(str(frame))
        return "\n".join(lines)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.frames}, {self.sample_rate})"

    @property
    def duration(self):
        sample_period = 1.0 / self._sample_rate
        return len(self._bits) * sample_period  # [seconds]
